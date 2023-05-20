import requests
import json
import os

def send_big_gov_request(self, url, parameter):
    token = os.getenv('BIZNES_GOV_API_KEY')
    headers = {
            'Authorization': f'Bearer {token}'
        }
    response = requests.get(url, headers=headers)
    if response.status_code == 204:
        return []
    if response.status_code != 200:
        return None
    return(json.loads(response.text)[str(parameter)])

def get_by_nip(self, nip_number):
    url = f'https://dane.biznes.gov.pl/api/ceidg/v1/firma?nip={nip_number}'
    return send_big_gov_request(url, 'firma')

def get_by_regon(self, regon_number):
    url = f'https://dane.biznes.gov.pl/api/ceidg/v1/firma?regon={regon_number}'
    return send_big_gov_request(url, 'firma')

def get_by_name(self, name):
    url=f'https://dane.biznes.gov.pl/api/ceidg/v1/firmy?nazwa={name}'
    return send_big_gov_request(url, 'firmy')