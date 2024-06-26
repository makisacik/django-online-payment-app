# Generated by Django 5.0.3 on 2024-03-19 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payapp", "0010_rename_amount_moneyrequest_requestedamount"),
    ]

    operations = [
        migrations.AddField(
            model_name="moneyrequest",
            name="receivingAmount",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="moneyrequest",
            name="requestedAmount",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
