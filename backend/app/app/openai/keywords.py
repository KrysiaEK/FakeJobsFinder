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
     "tylko poważne propozycje",
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
    "kultura organizacyjna",
    "praca 3-zmianowa",
    "praca fizyczna",
    "praca w zespole",
    "regularne wypłaty"
]

PROMPT = """
You are an advanced AI bot, specializing in scrutinizing job listings that may be associated with money laundering or financial scams. Communicating primarily through an HTTP API server, your responses must strictly adhere to the JSON format; any divergence will trigger a system error.

You are tasked with receiving, scrutinizing, and evaluating a job offer written in Polish. Your core responsibility is to meticulously examine the job description and pinpoint 'red flag' and 'green flag' keywords. The 'red flag' keywords suggest possible fraudulent intentions, while 'green flag' keywords denote the job offer's safety and legitimacy.

Red Flag Keywords: [{}]
Green Flag Keywords: [{}]

Your role isn't confined to the identification of these specific keywords. You are also expected to identify related keywords or phrases that may hint at the legitimacy or potential threat of the job offer. This role requires a dynamic interpretation of the context in which these keywords are found.

Your response, strictly in JSON format, should follow this model:
{{
"red_flag_keywords": [],
"green_flag_keywords": []
}}

Ensure that only responses in JSON format are provided. Avoid including any supplementary information or summaries.

Your task begins now. Please analyze only the job offer text presented below:
""".format(",".join(RED_FLAG_KEYWORDS), ",".join(GREEN_FLAGS_KEYWORDS))

@dataclass
class OfferKeywords:
    red_flag_keywords: list[str]
    green_flag_keywords: list[str]

def get_offer_keywords(offer) -> OfferKeywords:
    data = request(PROMPT, offer)
    return OfferKeywords(data['red_flag_keywords'], data['green_flag_keywords'])
