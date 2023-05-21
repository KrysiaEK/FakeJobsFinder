from .openai import request
from dataclasses import dataclass

PROMPT = """
Popraw formatowanie tekstu, usuń niepotrzebne nowe linie, powtarzający się elementy oraz nieprzydatne informacje z punktu widzenia osoby poszukującej pracy (takie jak liczba wyświetleń, id, napis aplikuj).
Zamień wszystkie krótkie informacje zapisane w dwóch liniach na jedna linie. Nie zmieniaj elementów opisu, zachowaj jak najbardziej orginalne słowa.
Treść ogłoszenia do poprawy:

"""

def get_fomatted_offer(offer) -> str:
    data = request(PROMPT + offer, use_json=False)
    return data['response']
