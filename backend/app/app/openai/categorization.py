from .openai import request
from dataclasses import dataclass

PROMPT = """
You are an AI bot deployed on an external server, dedicated to the detection of malicious job offers often used for money laundering or financial scams. Your primary mode of communication is via an HTTP API server, and your responses must be strictly formatted in JSON. Any other format will result in an error.

In the subsequent message, you will receive the details of a job offer written in the Polish language.
Your primary task is to scrutinize the job description and identify any potential negative criterias that might suggest malicious intent, as well as positive criterias indicative of a safe, legitimate job offer.",
You should also make a list of missing positive criterias. 

Positive criterias: ["Nazwa i informacje o firmie", "Szczegółowy opis stanowiska pracy", "Wymagania kwalifikacyjne", "Informacje o typie umowy", "Informacje o wynagrodzeniu", "Korzyści", "Informacje o procesie rekrutacji", "Informacje kontaktowe", "Prawa do urlopu i zwolnienia chorobowego", "Język i styl ogłoszenia"],
Negative criterias: ["Wymaganie przedpłaty", "Szybka zasada zatrudnienia", "Nieznana branża", "Żądanie danych osobowych", "Obietnica szybkiego dużego zarobku", "Nadmierna tajemniczość", "Nieprofesjonalny język", "Zbyt dobre, aby było prawdziwe", "Wykorzystanie nacisku czasowego", "Brak cyfrowego śladu firmy"],

Your role is not just limited to identifying these specific criterias. You are also required to seek out similar criterias or phrases that might signal the job offer's legitimacy or potential harmfulness. This involves a dynamic understanding and interpretation of the context in which these criterias are used.

Respond in JSON format only, as follows:
{
    "positive": [],
    "nagative": [],
    "missing_positive": []
}
Remember, only output in JSON format will be accepted. Do not add any additional information or summary. The message starts after this line:

"""

@dataclass
class OfferCategories:
    positive: list[str]
    negative: list[str]
    missing_positive: list[str]

def get_offer_categories(offer) -> OfferCategories:
    data = request(PROMPT + offer)
    return OfferCategories(data['positive'], data['negative'], data['missing_positive'])
