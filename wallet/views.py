from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from datetime import datetime
from .forms import AddIncomeForm, AddExpenseForm
from .forms import AddWalletForm
from .models import Wallet, Income, Expense
from .service import getIncomesSumInThisMonth, getExpansesSumInThisMonth, updateWalletAmount, getExpansesSumInLastWeek, \
    getIncomesSumInLastWeek


# Home
def home(request):
    if request.user.is_authenticated:
        income_list = Income.objects.filter(user=request.user).order_by('-updatedAt')[:3]
        expense_list = Expense.objects.filter(user=request.user).order_by('-updatedAt')[:3]
        wallet_list = Wallet.objects.filter(user=request.user).order_by('-updatedAt')[:3]

        income_sum_month = getIncomesSumInThisMonth(request.user)
        expense_sum_month = getExpansesSumInThisMonth(request.user)

        expense_sum_in_last_week = getExpansesSumInLastWeek(request.user)
        income_sum_in_last_week = getIncomesSumInLastWeek(request.user)

        context = {
            'income_list': income_list,
            'expense_list': expense_list,
            'wallet_list': wallet_list,
            'income_sum_month': income_sum_month,
            'expense_sum_month': expense_sum_month,
            'expense_sum_in_last_week': expense_sum_in_last_week,
            'income_sum_in_last_week': income_sum_in_last_week,
        }
        return render(request, 'wallet/home.html', context)
    else:
        return render(request, 'wallet/home.html')


# Wallet
def walletDetails(request, wallet_id):
    if request.user.is_authenticated:
        try:
            wallet = Wallet.objects.get(pk=wallet_id)
        except Wallet.DoesNotExist:
            raise Http404("Wallet does not exist")
        last_incomes = Income.objects.filter(wallet=wallet_id).order_by('-createdAt')[:5]
        last_expenses = Expense.objects.filter(wallet=wallet_id).order_by('-createdAt')[:5]

        context = {
            'wallet': wallet,
            'lastIncomes': last_incomes,
            'lastExpenses': last_expenses
        }
        return render(request, 'wallet/walletDetails.html', context)
    else:
        return redirect("/login")


def addWallet(request):
    if request.user.is_authenticated:
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = AddWalletForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                name = form.cleaned_data['name']
                amount = form.cleaned_data['amount']
                new_wallet = Wallet(name=name, amount=amount)
                new_wallet.save()
                request.user.wallets.add(new_wallet)

                return HttpResponseRedirect('/wallet/' + str(new_wallet.id))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = AddWalletForm()

        return render(request, 'wallet/walletAdd.html', {'form': form})
    else:
        return redirect("/login")


def walletList(request):
    if request.user.is_authenticated:
        wallet_list = Wallet.objects.filter(user=request.user).order_by('-updatedAt')

        context = {
            'walletList': wallet_list,
        }
        return render(request, 'wallet/walletList.html', context)
    else:
        return redirect("/login")


def deleteWallet(request, wallet_id):
    if request.user.is_authenticated:
        Wallet.objects.get(pk=wallet_id).delete()
        return walletList(request)
    else:
        raise Http404("Wallet does not exist")


# Income


def incomeDetails(request, income_id):
    if request.user.is_authenticated:
        try:
            income = Income.objects.get(pk=income_id)
        except Income.DoesNotExist:
            raise Http404("Income does not exist")
        context = {'income': income}
        return render(request, 'wallet/incomeDetails.html', context)
    else:
        return redirect("/login")


def incomeAdd(request, wallet_id):
    if request.user.is_authenticated:

        # if this is a POST request we need to process the form data
        wallet = Wallet.objects.get(pk=wallet_id)
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = AddIncomeForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                wallet = Wallet.objects.get(pk=wallet_id)

                source = form.cleaned_data['source']
                amount = form.cleaned_data['amount']
                date = form.cleaned_data['date']
                category = form.cleaned_data['category']
                new_income = Income(source=source, amount=amount, executionDate=date, category=category, wallet=wallet,
                                    user=request.user)
                updateWalletAmount(wallet_id, amount, 'add')
                new_income.save()

                return HttpResponseRedirect('/wallet/income/' + str(new_income.id))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = AddIncomeForm()

        return render(request, 'wallet/incomeAdd.html', {'form': form, 'wallet_id': wallet_id, 'wallet': wallet})
    else:
        return redirect("/login")


def incomeList(request):
    if request.user.is_authenticated:
        income_list = Income.objects.filter(user=request.user).order_by('-updatedAt')

        context = {
            'incomeList': income_list,
        }
        return render(request, 'wallet/incomeList.html', context)
    else:
        return redirect("/login")


def deleteIncome(request, income_id):
    if request.user.is_authenticated:

        income = Income.objects.get(pk=income_id)
        updateWalletAmount(income.wallet_id, income.amount, 'subtract')
        income.delete()
        return incomeList(request)
    else:
        raise Http404("Income does not exist")


# Expense
def expenseDetails(request, expense_id):
    if request.user.is_authenticated:
        try:
            expense = Expense.objects.get(pk=expense_id)
        except Expense.DoesNotExist:
            raise Http404("expense does not exist")
        context = {'expense': expense}
        return render(request, 'wallet/expenseDetails.html', context)
    else:
        return redirect("/login")


def expenseAdd(request, wallet_id):
    if request.user.is_authenticated:
        try:
            wallet = Wallet.objects.get(pk=wallet_id)
        except Expense.DoesNotExist:
            raise Http404("Wallet does not exist")

        if request.method == 'POST':
            form = AddExpenseForm(request.POST)
            if form.is_valid():
                wallet = Wallet.objects.get(pk=wallet_id)

                name = form.cleaned_data['name']
                amount = form.cleaned_data['amount']
                execution_date = form.cleaned_data['executionDate']
                category = form.cleaned_data['category']
                done = form.cleaned_data['done']
                new_expense = Expense(name=name, amount=amount, executionDate=execution_date, category=category,
                                      wallet=wallet, done=done, user=request.user)
                updateWalletAmount(wallet_id, amount, 'subtract')
                new_expense.save()

                return HttpResponseRedirect('/wallet/expense/' + str(new_expense.id))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = AddExpenseForm()

        return render(request, 'wallet/expenseAdd.html', {'form': form, 'wallet_id': wallet_id, 'wallet': wallet})
    else:
        return redirect("/login")


def expenseList(request):
    if request.user.is_authenticated:
        expense_list = Expense.objects.filter(user=request.user).order_by('-updatedAt')

        context = {
            'expenseList': expense_list,
        }
        return render(request, 'wallet/expenseList.html', context)
    else:
        return redirect("/login")


def deleteExpense(request, expense_id):
    if request.user.is_authenticated:
        expense = Expense.objects.get(pk=expense_id)
        updateWalletAmount(expense.wallet_id, expense.amount, 'add')
        expense.delete()
        return expenseList(request)
    else:
        raise Http404("Expense does not exist")
