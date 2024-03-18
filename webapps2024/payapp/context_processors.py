from .models import UserAccount


def add_user_balance_to_context(request):
    user_balance_info = {'balance': 'N/A', 'currency': 'N/A'}
    if request.user.is_authenticated:
        try:
            user_account = UserAccount.objects.get(user=request.user)
            user_balance_info = {
                'balance': user_account.balance,
                'currency': user_account.currency,
            }
            print("user_account.currency")
            print(user_account.currency)
        except UserAccount.DoesNotExist:
            pass

    return {'user_balance_info': user_balance_info}
