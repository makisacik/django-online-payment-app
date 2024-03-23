from django.db.models.signals import post_migrate
from django.contrib.auth.models import User
from django.dispatch import receiver


@receiver(post_migrate)
def create_initial_superuser(sender, **kwargs):
    if not User.objects.filter(username='admin1').exists():
        User.objects.create_superuser('admin1', 'admin1@admin.com', 'admin1')
        print("admin1 is created")
