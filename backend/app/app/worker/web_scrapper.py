from celery.schedules import crontab
from datetime import datetime

from app.core.celery_app import celery_app
from app.platforms.olx import OLX, OfferDetails
from app.db.session import SessionLocal
from app.models.job_offer import JobOffer

import app.openai as openai

PROVIDERS = {
    'olx': OLX
}

@celery_app.on_after_configure.connect
def setup_web_scrapper(sender, **kwargs):
    # run web scrapper after 15 seconds
    web_scrapper.apply_async(countdown=15, args=[0])

@celery_app.task
def web_scrapper(run):
    try:
        db = SessionLocal()
        offers = OLX().get_offers(1)
        for url in offers:
            if db.query(JobOffer).filter(JobOffer.url == url).first() is not None:        
                continue  # offer already exists
            get_offer.apply_async(args=['olx', url])
    except Exception as e:
        print("Exception", e)
        pass

    web_scrapper.apply_async(countdown=60, args=[run + 1 % 1000])


@celery_app.task
def get_offer(provider, url):
    db = SessionLocal()
    if db.query(JobOffer).filter(JobOffer.url == url).first() is not None:        
        return  # offer already exists

    provider_service = PROVIDERS[provider]()
    offer = provider_service.get_offer(url)

    categories = openai.get_offer_categories(offer.description)
    keywords = openai.get_offer_keywords(offer.description)
    information = openai.get_offer_information(offer.description)

    # create a new JobOffer
    new_offer = JobOffer(
        provider=provider,
        url=url,
        title=offer.title,
        description=offer.description,
        author=offer.author,
        company="",
        date=offer.date,
        score=3,
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

