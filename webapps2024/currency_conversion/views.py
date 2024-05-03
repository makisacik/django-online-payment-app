from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

# Hardcoded exchange rates will be used if API is down or response has an error
FALLBACK_EXCHANGE_RATES = {
    'USD': {'EUR': 0.92, 'GBP': 0.78},
    'EUR': {'USD': 1.09, 'GBP': 0.85},
    'GBP': {'USD': 1.28, 'EUR': 1.18},
}


class CurrencyConversion(APIView):
    def get(self, request, currency1, currency2, amount):
        converted_amount = self.convert_currency(currency1, currency2, amount)
        if converted_amount is None:
            return Response("One or both specified currencies are not supported or invalid amount.",
                            status=status.HTTP_404_NOT_FOUND)

        return Response({"converted_amount": converted_amount})

    @staticmethod
    def get_live_rate(currency1, currency2):
        api_url = f'https://open.er-api.com/v6/latest/{currency1}'
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            rates = response.json().get('rates')
            return rates[currency2]
        except Exception:
            return None

    @classmethod
    def convert_currency(cls, currency1, currency2, amount):
        try:
            amount = max(0, float(amount))
        except ValueError:
            return None

        rate = cls.get_live_rate(currency1, currency2)
        if rate is None:
            try:
                rate = FALLBACK_EXCHANGE_RATES[currency1][currency2]
            except KeyError:
                return None

        return rate * amount

    @staticmethod
    def build_conversion_url(request, currency1, currency2, amount):
        view_name = 'currency_conversion'
        url = reverse(view_name, args=[currency1, currency2, amount])
        return request.build_absolute_uri(url)
