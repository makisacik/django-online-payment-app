from django.shortcuts import render
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    user_emails = None

    email_query = request.GET.get('email')
    if email_query:
        user_emails = User.objects.filter(email__icontains=email_query).values_list('email', flat=True).exclude(email=request.user.email)

    return render(request, 'payapp/home.html', {'user_emails': user_emails})

