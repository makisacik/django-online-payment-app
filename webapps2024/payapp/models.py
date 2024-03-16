from django.db import models, transaction
from django.contrib.auth.models import User
from django.conf import settings


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)

    def __str__(self):
        return f"{self.user.username} - Balance: £{self.balance}"

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


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction from {self.sender} to {self.receiver} amount £{self.amount} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"




