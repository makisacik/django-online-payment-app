from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

EXCHANGE_RATES = {
    'USD': {'EUR': 0.92, 'GBP': 0.78},
    'EUR': {'USD': 1.09, 'GBP': 0.85},
    'GBP': {'USD': 1.28, 'EUR': 1.18},
}

class CurrencyConversion(APIView):
    def get(self, request, currency1, currency2, amount):
        try:
            amount_of_currency1 = max(0, float(amount))
        except ValueError:
            return Response("Invalid amount specified.", status=status.HTTP_400_BAD_REQUEST)

        try:
            rate = EXCHANGE_RATES[currency1][currency2]
            converted_amount = rate * amount_of_currency1
            return Response({"converted_amount": converted_amount})
        except KeyError:
            return Response("One or both specified currencies are not supported.", status=status.HTTP_404_NOT_FOUND)
