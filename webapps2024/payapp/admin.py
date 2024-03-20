from django.contrib import admin
from .models import Transaction, UserAccount, MoneyRequest

# Register your models here.
admin.site.register(Transaction)
admin.site.register(UserAccount)
admin.site.register(MoneyRequest)
