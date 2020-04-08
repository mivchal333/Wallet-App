from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from .forms import AddWalletForm

from .models import Wallet, Income, Expense


def index(request):
    return HttpResponse("Hello world from wallet app!")


def walletDetails(request, wallet_id):
    try:
        wallet = Wallet.objects.get(pk=wallet_id)
    except Wallet.DoesNotExist:
        raise Http404("Wallet does not exist")
    lastIncomes = Income.objects.filter(wallet = wallet_id).order_by('-createdAt')[:5]
    lastExpenses = Expense.objects.filter(wallet = wallet_id).order_by('-createdAt')[:5]

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


def addWallet(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddWalletForm(request.POST)
        print(form)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            amount = form.cleaned_data['amount']
            newWallet = Wallet(name=name, amount=amount)
            newWallet.save()

            return HttpResponseRedirect('/wallet/'+str(newWallet.id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddWalletForm()

    return render(request, 'wallet/walletAdd.html', {'form': form})
