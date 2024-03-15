from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from payapp.models import UserAccount
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.urls import reverse
from django.core.exceptions import ValidationError
import decimal


# Create your views here.
def home(request):
    user_emails = None
    email_query = request.GET.get('email')
    if email_query:
        user_emails = User.objects.filter(email__icontains=email_query).values_list('email', flat=True).exclude(
            email=request.user.email)

    user_account = UserAccount.objects.get(user__email='test5@gmail.com')

    return render(request, 'payapp/home.html', {'user_emails': user_emails})


@login_required
def transfer_money(request):
    if request.method == "POST":
        recipient_email = request.POST.get('recipient_email')
        try:
            amount = decimal.Decimal(request.POST.get('amount'))
            if amount <= 0:
                messages.error(request, "The amount must be greater than 0.")
                return redirect('home')
        except decimal.InvalidOperation:
            messages.error(request, "Invalid amount entered.")
            return redirect('home')

        try:
            sender_account = UserAccount.objects.get(user=request.user)
            recipient_user = User.objects.get(email=recipient_email)
            recipient_account, created = UserAccount.objects.get_or_create(user=recipient_user)

            try:
                sender_account.deduct_money(amount)
                recipient_account.add_money(amount)
                messages.success(request, f"Successfully transferred £{amount} to {recipient_email}.")
            except ValueError as e:
                messages.error(request, str(e))

        except User.DoesNotExist:
            messages.error(request, "Recipient user does not exist.")
        except UserAccount.DoesNotExist:
            messages.error(request, "Sender account does not exist.")
    else:
        messages.error(request, "Invalid request.")

    return redirect('home')
