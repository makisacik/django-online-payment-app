from django.db import models, transaction
from django.contrib.auth.models import User
from django.conf import settings
import thrift_app.thrift_client
import datetime
from datetime import timedelta, datetime
import pytz

CURRENCY_CHOICES = [
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
    ('GBP', 'British Pound'),
]


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='GBP')

    def __str__(self):
        return f"{self.user.username} - Balance:  {self.balance} {self.currency}"

    def add_money(self, amount):
        with transaction.atomic():
            user_account = UserAccount.objects.select_for_update().get(pk=self.pk)
            user_account.balance += amount
            user_account.save()

    def deduct_money(self, amount):
        with transaction.atomic():
            user_account = UserAccount.objects.select_for_update().get(pk=self.pk)
            if user_account.balance >= amount:
                user_account.balance -= amount
                user_account.save()
            else:
                raise ValueError("Insufficient funds.")

def get_safe_current_timestamp():
    try:
        timestamp = thrift_app.thrift_client.get_current_timestamp()
        if isinstance(timestamp, str):
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        utc_zone = pytz.utc
        timestamp = utc_zone.localize(timestamp)
        timestamp += timedelta(hours=1)
        return timestamp
    except Exception as e:
        print(f"Failed to get timestamp from Thrift service: {str(e)}")
        uk_time = datetime.now(pytz.utc) + timedelta(hours=1)
        return uk_time

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_transactions', on_delete=models.CASCADE)
    receivedAmount = models.DecimalField(max_digits=10, decimal_places=2)
    sentAmount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=get_safe_current_timestamp)

    def __str__(self):
        return f"Transaction from {self.sender} to {self.receiver} amount {self.receivedAmount} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

class MoneyRequest(models.Model):
    id = models.AutoField(primary_key=True)
    sentBy = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
    sentTo = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)
    requestedAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    receivingAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    timestamp = models.DateTimeField(default=get_safe_current_timestamp)

    def __str__(self):
        return f"Money Request from {self.sentBy} to {self.sentTo} amount {self.requestedAmount} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
