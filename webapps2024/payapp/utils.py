import requests
from django.urls import reverse
from django.conf import settings

def convert_currency(from_currency, to_currency, amount):
    relative_url = reverse('currency_conversion', args=[from_currency, to_currency, amount])

    scheme = getattr(settings, 'DEFAULT_SCHEME', 'http')
    domain = getattr(settings, 'DEFAULT_DOMAIN', 'localhost:8000')

    service_url = f'{scheme}://{domain}{relative_url}'

    response = requests.get(service_url)

    if response.status_code == 200:
        result = response.json()
        return result.get('converted_amount')
    else:
        return None
