from django.shortcuts import render
from django.contrib.auth.models import User
from payapp.models import UserAccount


# Create your views here.
def home(request):
    user_emails = None

    email_query = request.GET.get('email')
    if email_query:
        user_emails = User.objects.filter(email__icontains=email_query).values_list('email', flat=True).exclude(email=request.user.email)

    user_account = UserAccount.objects.get(user__email='test5@gmail.com')

    try:
        user_account.add_money(100)
        print(f"Money added successfully. New balance is £{user_account.balance}")

        user_account.deduct_money(50)
        print(f"Money deducted successfully. New balance is £{user_account.balance}")
    except ValueError as e:
        print(e)

    return render(request, 'payapp/home.html', {'user_emails': user_emails})

