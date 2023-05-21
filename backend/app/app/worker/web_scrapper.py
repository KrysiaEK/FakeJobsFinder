from celery.schedules import crontab
from datetime import datetime

from app.core.celery_app import celery_app
from app.platforms import Olx, Sprzedajemy, Ogloszenia24
from app.db.session import SessionLocal
from app.models.job_offer import JobOffer
from app import biznes_gov, openai

PROVIDERS = {
    'olx': Olx,
    'sprzedajemy': Sprzedajemy,
    'ogloszenia24': Ogloszenia24
}

@celery_app.on_after_configure.connect
def setup_web_scrapper(sender, **kwargs):
    # run web scrapper after 15 seconds
    web_scrapper.apply_async(countdown=15, args=[1])

@celery_app.task
def web_scrapper(run):
    providers = list(PROVIDERS.keys())
    try:
        db = SessionLocal()

        selected_provider = run % len(providers)
        page = run // len(providers)

        provider = PROVIDERS[providers[selected_provider]]()
        offers = provider.get_offers(page)
        print("Offers for", provider, offers)
        for url in offers:
            if db.query(JobOffer).filter(JobOffer.url == url).first() is not None:        
                continue  # offer already exists
            get_offer.apply_async(args=[providers[selected_provider], url])
    except Exception as e:
        print("Exception", e)
        pass

    web_scrapper.apply_async(countdown=60, args=[run + 1 % 1000])


@celery_app.task
def get_offer(provider, url):
    print(provider, url)
    db = SessionLocal()
    if db.query(JobOffer).filter(JobOffer.url == url).first() is not None:        
        return  # offer already exists

    provider_service = PROVIDERS[provider]()
    offer = provider_service.get_offer(url)

    categories = openai.get_offer_categories(offer.description)
    keywords = openai.get_offer_keywords(offer.description)
    information = openai.get_offer_information(offer.description)
    #description = openai.get_fomatted_offer(offer.description)
    description = offer.description

    company_exists = False
    try:
        if information.nip and biznes_gov.get_by_nip(information.nip):
            company_exists = True
        elif information.regon and biznes_gov.get_by_regon(information.regon):
            company_exists = True
        elif information.company_name and biznes_gov.get_by_name(information.company_name):
            company_exists = True
    except:
        pass

    # simple scoring, to be improved later
    score = 5
    if len(categories.negative) < len(categories.positive):
        score -= 1 
    if len(keywords.red_flag_keywords) < 4:
        score -= 1 
    if len(keywords.red_flag_keywords) < len(keywords.green_flag_keywords):
        score -= 1 
    if len(categories.positive) > 4:
        score -= 1 
    if company_exists:
        score -= 1 
    score = max(score, 1)

    # create a new JobOffer
    new_offer = JobOffer(
        provider=provider,
        url=url,
        title=offer.title,
        description=description,
        author=offer.author,
        company=information.company_name if information.company_name else "",
        date=offer.date,
        score=score,
        positives=";".join(categories.positive),
        negatives=";".join(categories.negative),
        positive_keywords=";".join(keywords.green_flag_keywords),
        negative_keywords=";".join(keywords.red_flag_keywords),
        email_text='EmailText',
        website_copy=offer.screenshot,
    )

    db.add(new_offer)
    db.commit()

    print(offer.title, categories, keywords, information)

