from django.db.models.signals import post_save
from django.dispatch import receiver
from payapp.models import UserAccount
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        UserAccount.objects.create(user=instance)
    else:
        user_account, created = UserAccount.objects.get_or_create(user=instance)
        user_account.save()
