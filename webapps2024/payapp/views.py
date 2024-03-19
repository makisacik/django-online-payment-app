from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from payapp.models import UserAccount, Transaction, MoneyRequest
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
import decimal
from .utils import convert_currency


@login_required
def home(request):
    user_emails = None
    email_query = request.GET.get('email')
    if email_query:
        user_emails = User.objects.filter(email__icontains=email_query).exclude(email=request.user.email).values_list('email', flat=True)

    recent_transactions = Transaction.objects.filter(models.Q(sender=request.user) | models.Q(receiver=request.user)).order_by('-timestamp')[:10]

    money_requests = MoneyRequest.objects.filter(models.Q(sentBy=request.user) | models.Q(sentTo=request.user)).order_by('-timestamp')[:10]

    context = {
        'user_emails': user_emails,
        'recent_transactions': recent_transactions,
        'money_requests': money_requests,
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

            if sender_account.currency != recipient_account.currency:
                converted_amount = convert_currency(sender_account.currency, recipient_account.currency, amount)
                if converted_amount is None:
                    messages.error(request, "Failed to convert currency.")
                    return redirect('home')
            else:
                converted_amount = amount

            try:
                sender_account.deduct_money(amount)
                recipient_account.add_money(decimal.Decimal(converted_amount))

                Transaction.objects.create(
                    sender=request.user,
                    receiver=recipient_user,
                    receivedAmount=decimal.Decimal(converted_amount),
                    sentAmount=decimal.Decimal(amount),
                )

                messages.success(request, f"Successfully transferred {sender_account.currency} {amount} to {recipient_email}, converted to {recipient_account.currency} {converted_amount:.2f}.")
            except ValueError as e:
                messages.error(request, str(e))

        except User.DoesNotExist:
            messages.error(request, "Recipient user does not exist.")
        except UserAccount.DoesNotExist:
            messages.error(request, "Sender account does not exist.")
    else:
        messages.error(request, "Invalid request.")

    return redirect('home')


@login_required
def request_money(request):
    if request.method == "POST":
        recipient_email = request.POST.get('recipient_email')
        try:
            requested_amount = decimal.Decimal(request.POST.get('amount'))
            if requested_amount <= 0:
                messages.error(request, "The amount must be greater than 0.")
                return redirect('home')
        except decimal.InvalidOperation:
            messages.error(request, "Invalid amount entered.")
            return redirect('home')

        try:
            sent_by_user = request.user
            sent_to_user = User.objects.get(email=recipient_email)
            sent_by_account = UserAccount.objects.get(user=sent_by_user)
            sent_to_account, created = UserAccount.objects.get_or_create(user=sent_to_user)

            if sent_by_account.currency != sent_to_account.currency:
                receiving_amount = convert_currency(sent_by_account.currency, sent_to_account.currency, requested_amount)
                if receiving_amount is None:
                    messages.error(request, "Failed to convert currency.")
                    return redirect('home')
            else:
                receiving_amount = requested_amount

            MoneyRequest.objects.create(
                sentBy=sent_by_user,
                sentTo=sent_to_user,
                requestedAmount=requested_amount,
                receivingAmount=receiving_amount
            )

            messages.success(request, "Money request submitted successfully.")
        except User.DoesNotExist:
            messages.error(request, "Recipient user does not exist.")
        except UserAccount.DoesNotExist:
            messages.error(request, "Sender or recipient account does not exist.")
    else:
        messages.error(request, "Invalid request.")

    return redirect('home')


@login_required
def cancel_money_request(request, request_id):
    money_request = MoneyRequest.objects.filter(pk=request_id).first()
    if money_request:
        money_request.delete()
        messages.success(request, "Money request cancelled successfully.")
    else:
        messages.error(request, "Money request not found or you don't have permission to cancel it.")
    return HttpResponseRedirect(reverse('home'))


@login_required
def accept_money_request(request, request_id):
    money_request = MoneyRequest.objects.filter(pk=request_id, sentTo=request.user).first()

    if not money_request:
        messages.error(request, "Money request not found.")
        return HttpResponseRedirect(reverse('home'))

    sender_account = UserAccount.objects.get(user=money_request.sentBy)
    recipient_account = UserAccount.objects.get(user=request.user)

    try:
        recipient_account.deduct_money(money_request.receivingAmount)
    except ValueError:
        messages.error(request, "Insufficient funds to complete this request.")
        return HttpResponseRedirect(reverse('home'))

    sender_account.add_money(money_request.requestedAmount)

    Transaction.objects.create(
        sender=money_request.sentBy,
        receiver=request.user,
        receivedAmount=money_request.requestedAmount,
        sentAmount=money_request.receivingAmount,
    )

    money_request.delete()
    messages.success(request, "Money request accepted and processed successfully.")

    return HttpResponseRedirect(reverse('home'))