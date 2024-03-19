import requests


def convert_currency(from_currency, to_currency, amount):
    service_url = f'http://localhost:8000/conversion/{from_currency}/{to_currency}/{amount}/'
    response = requests.get(service_url)

    if response.status_code == 200:
        result = response.json()
        return result.get('converted_amount')
    else:
        return None
