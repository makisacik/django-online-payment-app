# Generated by Django 5.0.3 on 2024-03-19 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payapp", "0009_alter_transaction_sentamount"),
    ]

    operations = [
        migrations.RenameField(
            model_name="moneyrequest",
            old_name="amount",
            new_name="requestedAmount",
        ),
    ]
