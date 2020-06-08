from datetime import datetime, timedelta

from django.db.models import Sum

from wallet.models import Income, Expense, Wallet


def getIncomeSum(user):
    income_sum_all = Income.objects.filter(user=user).aggregate(Sum('amount'))
    if income_sum_all.get('amount__sum'):
        return income_sum_all.get('amount__sum')
    else:
        return 0


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

    expense_sum = Expense.objects.filter(user=user, done=True, createdAt__gte=first_day_of_month).aggregate(
        Sum('amount'))

    if expense_sum.get('amount__sum'):
        return expense_sum.get('amount__sum')
    else:
        return 0


def getIncomesSumInLastWeek(user):
    today_date = datetime.today().date()
    last_week_start_date = today_date - timedelta(days=7)

    incomes_sum = Income.objects.filter(user=user, createdAt__gte=last_week_start_date).aggregate(Sum('amount'))

    if incomes_sum.get('amount__sum'):
        return incomes_sum.get('amount__sum')
    else:
        return 0


def getExpansesSumInLastWeek(user):
    today_date = datetime.today().date()
    last_week_start_date = today_date - timedelta(days=7)

    expense_sum = Expense.objects.filter(user=user, done=True, createdAt__gte=last_week_start_date).aggregate(
        Sum('amount'))

    if expense_sum.get('amount__sum'):
        return expense_sum.get('amount__sum')
    else:
        return 0


def updateWalletAmount(wallet_id, amount, action_type):
    wallet = Wallet.objects.get(pk=wallet_id)

    today__date = datetime.now()
    wallet.updatedAt = today__date
    old_amount = wallet.amount
    if action_type == 'add':
        new_amount = float(old_amount) + float(amount)
    else:
        new_amount = float(old_amount) - float(amount)

    wallet.amount = new_amount
    wallet.save()
