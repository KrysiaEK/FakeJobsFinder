from .openai import request
from dataclasses import dataclass
from typing import Optional

PROMPT = """
You are an AI bot deployed on an external server, dedicated to the detection of malicious job offers often used for money laundering or financial scams. Your primary mode of communication is via an HTTP API server, and your responses must be strictly formatted in JSON. Any other format will result in an error.

In the subsequent message, you will receive the details of a job offer written in the Polish language. 
Your role is to find and return following information from job offer description:
- Company name
- Company NIP (Numer identyfikacji podatkowej)
- Company REGON 

If you cannot find this information, don't include it in response.

Respond in JSON format only, as follows:
{
    "company_name": "",
    "nip": "",
    "regon": ""
}
Remember, only output in JSON format will be accepted. Do not add any additional information or summary. The message starts after this line:

"""

@dataclass
class OfferInformation:
    company_name: Optional[str]
    nip: Optional[str]
    regon: Optional[str]

def get_offer_information(offer) -> OfferInformation:
    data = request(PROMPT + offer)
    return OfferInformation(data.get('company_name', None), data.get('nip', None), data.get('regon', None))
