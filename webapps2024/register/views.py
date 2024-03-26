from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from register.forms import RegisterForm, AdminRegisterForm
from payapp.models import UserAccount
from currency_conversion.views import CurrencyConversion
from django.contrib.auth.decorators import login_required, user_passes_test


@csrf_protect
def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            currency = form.cleaned_data.get('currency')

            initial_balance_gbp = 1000
            converted_balance = CurrencyConversion.convert_currency('GBP', currency, initial_balance_gbp)
            if converted_balance is None:
                messages.error(request, "Failed to convert currency or unsupported currency selected.")
                return render(request, "register/register.html", {"register_form": form})

            user_account = UserAccount.objects.get(user=user)
            user_account.currency = currency
            user_account.balance = converted_balance
            user_account.save()

            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RegisterForm()
    return render(request, "register/register.html", {"register_form": form})


@csrf_protect
@login_required
@user_passes_test(lambda user: user.is_superuser)
def register_admin(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_superuser = True
            user.is_staff = True
            user.save()
            messages.success(request, f"Admin registration successful for {user.email}.")

            return redirect('admin_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = AdminRegisterForm()
    return render(request, 'register/admin-register.html', {'AdminRegisterForm': form})


@csrf_protect
def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser or user.is_staff:
                    messages.info(request, f"Welcome back, Admin {username}.")
                    return redirect("admin_home")
                else:
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "register/login.html", {"login_form": form})


@csrf_protect
def logout_user(request):
    logout(request)
    return redirect("login")
