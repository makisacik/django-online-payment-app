from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from payapp.models import UserAccount, Transaction
from django.contrib.auth.decorators import login_required
from django.db import models
import decimal


def home(request):
    user_emails = None
    email_query = request.GET.get('email')
    if email_query:
        user_emails = User.objects.filter(email__icontains=email_query).exclude(email=request.user.email).values_list(
            'email', flat=True)

    recent_transactions = Transaction.objects.filter(
        models.Q(sender=request.user) | models.Q(receiver=request.user)).order_by('-timestamp')[:10]

    context = {
        'user_emails': user_emails,
        'recent_transactions': recent_transactions,
    }

    return render(request, 'payapp/home.html', context)


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

                Transaction.objects.create(sender=request.user, receiver=recipient_user, amount=amount)

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
