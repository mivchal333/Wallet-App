from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import Wallet, Income, Expense


def index(request):
    return HttpResponse("Hello world from wallet app!")


def walletDetails(request, wallet_id):
    try:
        wallet = Wallet.objects.get(pk=wallet_id)
    except Wallet.DoesNotExist:
        raise Http404("Wallet does not exist")
    lastIncomes = Income.objects.order_by('-createdAt')[:5]
    lastExpenses = Expense.objects.order_by('-createdAt')[:5]

    context = {
        'wallet': wallet,
        'lastIncomes': lastIncomes,
        'lastExpenses': lastExpenses
    }
    return render(request, 'wallet/walletDetails.html', context)


def incomeDetails(request, income_id):
    try:
        income = Income.objects.get(pk=income_id)
    except Income.DoesNotExist:
        raise Http404("Income does not exist")
    context = {'income': income}
    return render(request, 'wallet/incomeDetails.html', context)
