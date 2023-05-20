from .openai import request
from dataclasses import dataclass

RED_FLAG_KEYWORDS = [
    "sprzedam konto",
     "kupię konto",
     "zapłacę za założenie konta",
     "konto bankowe bez komornika",
     "udostępnię konto bankowe",
     "czyste konto bankowe",
     "bezpieczne konto bankowe",
     "przelewy za %",
     "procent od kwoty przelewu",
     "konto na słupa",
     "słup",
     "tester bankowości",
     "mam konto bankowe",
     "konto bankowe od ręki",
     "przyjąć przelew",
     "nawiążę długotrwałą współpracę",
     "przelew na wskazane konto",
     "nie na moje dane",
     "konta bankowe w różnych bankach",
     "prowizja",
     "otworzyć konto bankowe",
     "zajęcie komornicze",
     "oferta mocno ograniczona",
     "zakładane w oddziale",
     "brak blokad",
     "brak limitów",
     "dokumenty z banku",
     "umowa bankowa",
     "karta sim",
     "skan dowodu",
     "długa współpraca",
     "stała współpraca",
     "zbudowanie zaufania",
     "gwarancja zadowolenia",
     "czyjeś konto",
     "do legalnych rzeczy",
     "legalne",
     "tylko poważne propozycje"
]

GREEN_FLAGS_KEYWORDS = [
    "umowa o pracę",
    "urlop",
    "prawo do urlopu",
    "benefity",
    "umowa zlecenie",
    "umowa o dzieło",
    "ubezpieczenie zdrowotne",
    "emerytalne",
    "fundusz socjalny",
    "elastyczny czas pracy",
    "szkolenia",
    "rozwój zawodowy",
    "wynagrodzenie netto/brutto",
    "stabilne zatrudnienie",
    "prawo do zwolnienia lekarskiego",
    "praca stacjonarna",
    "doświadczenie",
    "kwalifikacje",
    "wymagane umiejętności",
    "wynagrodzenie zależne od umiejętności",
    "podpisane referencje",
    "dodatki służbowe",
    "wynagrodzenie podstawowe",
    "dodatek za nadgodziny",
    "opis stanowiska",
    "obowiązki",
    "wymagania",
    "proces rekrutacji",
    "kontakt z HR",
    "numer telefonu do biura",
    "adres biura",
    "nazwa firmy",
    "NIP firmy",
    "informacje o firmie",
    "wartości firmy",
    "misja firmy",
    "kultura organizacyjna"
]

PROMPT = """
You are an AI bot deployed on an external server, dedicated to the detection of malicious job offers often used for money laundering or financial scams. Your primary mode of communication is via an HTTP API server, and your responses must be strictly formatted in JSON. Any other format will result in an error.
You will receive the details of a job offer written in the Polish language. Your primary task is to scrutinize the job description and identify any potential 'red flag' keywords that might suggest malicious intent, as well as 'green flag' keywords indicative of a safe, legitimate job offer.

Red flag keywords: {}
Green flag keywords: {}

Your role is not just limited to identifying these specific keywords. You are also required to seek out similar keywords or phrases that might signal the job offer's legitimacy or potential harmfulness. This involves a dynamic understanding and interpretation of the context in which these keywords are used.

Respond in JSON format only, as follows:
{{
    "red_flag_keywords": [],
    "green_flag_keywords": []
}}
Remember, only output in JSON format will be accepted. Do not add any additional information or summary. The message starts after this line:

""".format(",".join(RED_FLAG_KEYWORDS), ",".join(GREEN_FLAGS_KEYWORDS))

@dataclass
class OfferKeywords:
    red_flag_keywords: list[str]
    green_flag_keywords: list[str]

def get_offer_keywords(offer) -> OfferKeywords:
    data = request(PROMPT, offer)
    return OfferKeywords(data['red_flag_keywords'], data['green_flag_keywords'])
