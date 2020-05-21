from datetime import datetime
from django.db.models import Sum

from wallet.models import Income, Expense, Wallet


def getIncomesSumInThisMonth(user):
    today_date = datetime.today().date()
    first_day_of_month = today_date.replace(day=1)

    income_sum = Income.objects.filter(user=user, createdAt__gte=first_day_of_month).aggregate(Sum('amount'))

    if income_sum.get('amount__sum'):
        return income_sum.get('amount__sum')
    else:
        return 0


def getExpansesSumInThisMonth(user):
    today_date = datetime.today().date()
    first_day_of_month = today_date.replace(day=1)

    expense_sum = Expense.objects.filter(user=user, createdAt__gte=first_day_of_month).aggregate(Sum('amount'))

    if expense_sum.get('amount__sum'):
        return expense_sum.get('amount__sum')
    else:
        return 0

def updateWalledUpdatedAtTime(wallet_id):
    wallet = Wallet.objects.get(pk=wallet_id)

    today__date = datetime.now()
    wallet.updatedAt = today__date
    wallet.save()
