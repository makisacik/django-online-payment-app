from .models import UserAccount


def add_user_balance_to_context(request):
    user_balance = None
    if request.user.is_authenticated:
        try:
            user_account = UserAccount.objects.get(user=request.user)
            user_balance = user_account.balance
        except UserAccount.DoesNotExist:
            user_balance = 'N/A'

    return {'user_balance': user_balance}
