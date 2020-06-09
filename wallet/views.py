from datetime import datetime
from itertools import chain

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import IncomeForm, ExpenseForm, CategoryForm
from .forms import WalletForm
from .models import Wallet, Income, Expense, Category
from .service import getIncomesSumInThisMonth, getExpansesSumInThisMonth, updateWalletAmount, getExpansesSumInLastWeek, \
    getIncomesSumInLastWeek, WalletAction


# Contact

def contact(request):
    context = {}
    context['api_key'] = 'AIzaSyAN-F4MEa1DFERJwgxQmI5VcX4OgMlHFd0'
    return render(request, 'wallet/about.html', context)


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
            if wallet.user != request.user:
                raise PermissionDenied
        except Wallet.DoesNotExist:
            raise Http404("Wallet does not exist")
        last_incomes = Income.objects.filter(wallet=wallet_id).order_by('-createdAt')[:5]
        last_expenses = Expense.objects.filter(wallet=wallet_id).order_by('-createdAt')[:5]

        data = []
        income_list = Income.objects.filter(wallet=wallet_id)
        for income in income_list:
            data.append(income.amount)

        income_sum = sum(data)
        context = {
            'wallet': wallet,
            'lastIncomes': last_incomes,
            'lastExpenses': last_expenses,
            'income_sum': income_sum,
        }
        return render(request, 'wallet/wallet/walletDetails.html', context)
    else:
        return redirect("/login")


def addWallet(request):
    if request.user.is_authenticated:
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = WalletForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                new_wallet = Wallet(name=name, description=description)
                new_wallet.save()
                request.user.wallets.add(new_wallet)

                return HttpResponseRedirect('/wallet/' + str(new_wallet.id))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = WalletForm()

        return render(request, 'wallet/wallet/walletForm.html', {'form': form})
    else:
        return redirect("/login")


def walletList(request):
    if request.user.is_authenticated:
        wallet_list = Wallet.objects.filter(user=request.user).order_by('-updatedAt')

        context = {
            'walletList': wallet_list,
        }
        return render(request, 'wallet/wallet/walletList.html', context)
    else:
        return redirect("/login")


def deleteWallet(request, wallet_id):
    if request.user.is_authenticated:
        try:
            wallet = Wallet.objects.get(pk=wallet_id)
        except Wallet.DoesNotExist:
            raise Http404("Wallet does not exist")
        if wallet.user != request.user:
            raise PermissionDenied
        wallet.delete()
        return walletList(request)

    else:
        return redirect("/login")


def updateWallet(request, wallet_id):
    if request.user.is_authenticated:
        try:
            wallet = Wallet.objects.get(pk=wallet_id)
        except Wallet.DoesNotExist:
            raise Http404("Wallet does not exist")
        if wallet.user != request.user:
            raise PermissionDenied
        form = WalletForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                wallet.name = name
                wallet.description = description
                wallet.save()
            return redirect("/wallet/" + str(wallet_id))
        else:
            form = WalletForm(instance=wallet)

        return render(request, 'wallet/wallet/walletForm.html', {'form': form})
    else:
        return redirect("/login")


def walletTimeline(request, wallet_id):
    if request.user.is_authenticated:
        try:
            wallet = Wallet.objects.get(pk=wallet_id)
        except Wallet.DoesNotExist:
            raise Http404("Wallet does not exist")
        if wallet.user != request.user:
            raise PermissionDenied

        defaultLimit = 50
        limitParam = int(request.GET.get('limit', defaultLimit))

        today_date = datetime.today().date()

        incomes = Income.objects.filter(wallet=wallet_id, executionDate__isnull=False,
                                        executionDate__lte=today_date) \
                      .order_by('-createdAt')[:limitParam]

        expenses = Expense.objects.filter(wallet=wallet_id, done=True, executionDate__isnull=False,
                                          executionDate__lte=today_date) \
                       .order_by('-createdAt')[:limitParam]

        action_list = sorted(
            chain(incomes, expenses),
            key=lambda instance: instance.createdAt
        )[:limitParam]

        context = {
            'wallet': wallet,
            'actionList': action_list,
        }
        return render(request, 'wallet/wallet/timeline.html', context)
    else:
        return redirect("/login")


# Income


def incomeDetails(request, income_id):
    if request.user.is_authenticated:
        try:
            income = Income.objects.get(pk=income_id)
        except Income.DoesNotExist:
            raise Http404("Income does not exist")
        if income.user != request.user:
            raise PermissionDenied
        context = {'income': income}
        return render(request, 'wallet/income/incomeDetails.html', context)
    else:
        return redirect("/login")


def incomeAdd(request, wallet_id):
    if request.user.is_authenticated:

        # if this is a POST request we need to process the form data
        wallet = Wallet.objects.get(pk=wallet_id)
        if wallet.user != request.user:
            raise PermissionDenied
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = IncomeForm(request.POST, user=request.user)
            # check whether it's valid:
            if form.is_valid():
                wallet = Wallet.objects.get(pk=wallet_id)

                source = form.cleaned_data['source']
                amount = form.cleaned_data['amount']
                executionDate = form.cleaned_data['executionDate']
                category = form.cleaned_data['category']
                new_income = Income(source=source, amount=amount, executionDate=executionDate, category=category,
                                    wallet=wallet,
                                    user=request.user)
                updateWalletAmount(wallet_id, amount, WalletAction.ADD)
                new_income.save()

                return HttpResponseRedirect('/wallet/income/' + str(new_income.id))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = IncomeForm(user=request.user)

        return render(request, 'wallet/income/incomeForm.html',
                      {'form': form, 'wallet_id': wallet_id, 'wallet': wallet})
    else:
        return redirect("/login")


def incomeList(request):
    if request.user.is_authenticated:
        income_list = Income.objects.filter(user=request.user).order_by('-updatedAt')

        labels = []
        data = []

        for income in income_list:
            labels.append(income.source)
            data.append(income.amount)

        context = {
            'incomeList': income_list,
            'labels': labels,
            'data': data,
        }
        return render(request, 'wallet/income/incomeList.html', context)
    else:
        return redirect("/login")


def deleteIncome(request, income_id):
    if request.user.is_authenticated:
        try:
            income = Income.objects.get(pk=income_id)
        except Income.DoesNotExist:
            raise Http404("Income does not exist")
        if income.user != request.user:
            raise PermissionDenied
        updateWalletAmount(income.wallet_id, income.amount, WalletAction.SUBTRACT)
        income.delete()
        return incomeList(request)
    else:
        raise PermissionDenied


def updateIncome(request, income_id):
    if request.user.is_authenticated:
        try:
            income = Income.objects.get(pk=income_id)
        except Income.DoesNotExist:
            raise Http404("Income does not exist")

        if income.user != request.user:
            raise PermissionDenied
        form = IncomeForm(request.POST, user=request.user)
        if request.method == 'POST':
            if form.is_valid():
                source = form.cleaned_data['source']
                amount = form.cleaned_data['amount']
                execution_date = form.cleaned_data['executionDate']
                category = form.cleaned_data['category']
                income.source = source
                income.amount = amount
                income.executionDate = execution_date
                income.category = category

                income.save()

            return redirect('/wallet/income/' + str(income_id))
        else:
            form = IncomeForm(instance=income, user=request.user)

        return render(request, 'wallet/income/incomeForm.html', {'form': form, 'wallet': income.wallet})
    else:
        return redirect("/login")


# Expense
def expenseDetails(request, expense_id):
    if request.user.is_authenticated:
        try:
            expense = Expense.objects.get(pk=expense_id)
        except Expense.DoesNotExist:
            raise Http404("expense does not exist")
        if expense.user != request.user:
            raise PermissionDenied
        context = {'expense': expense}
        return render(request, 'wallet/expense/expenseDetails.html', context)
    else:
        return redirect("/login")


def expenseAdd(request, wallet_id):
    if request.user.is_authenticated:
        try:
            wallet = Wallet.objects.get(pk=wallet_id, user=request.user)
        except Wallet.DoesNotExist:
            raise Http404("Wallet does not exist")
        if wallet.user != request.user:
            raise PermissionDenied
        if request.method == 'POST':
            form = ExpenseForm(request.POST, user=request.user)
            if form.is_valid():
                wallet = Wallet.objects.get(pk=wallet_id)

                name = form.cleaned_data['name']
                amount = form.cleaned_data['amount']
                execution_date = form.cleaned_data['executionDate']
                category = form.cleaned_data['category']
                done = form.cleaned_data['done']
                new_expense = Expense(name=name, amount=amount, executionDate=execution_date, category=category,
                                      wallet=wallet, done=done, user=request.user)
                updateWalletAmount(wallet_id, amount, WalletAction.SUBTRACT)
                new_expense.save()

                return HttpResponseRedirect('/wallet/expense/' + str(new_expense.id))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = ExpenseForm(user=request.user)

        return render(request, 'wallet/expense/expenseForm.html',
                      {'form': form, 'wallet_id': wallet_id, 'wallet': wallet})
    else:
        return redirect("/login")


def expenseList(request):
    if request.user.is_authenticated:
        expense_list = Expense.objects.filter(user=request.user).order_by('-updatedAt')

        context = {
            'expenseList': expense_list,
        }
        return render(request, 'wallet/expense/expenseList.html', context)
    else:
        return redirect("/login")


def deleteExpense(request, expense_id):
    if request.user.is_authenticated:
        try:
            expense = Expense.objects.get(pk=expense_id)
        except Expense.DoesNotExist:
            raise Http404("Expense does not exist")

        if expense.user != request.user:
            raise PermissionDenied
        updateWalletAmount(expense.wallet_id, expense.amount, WalletAction.ADD)
        expense.delete()
        return expenseList(request)
    else:
        return redirect("/login")


def updateExpense(request, expense_id):
    if request.user.is_authenticated:
        try:
            expense = Expense.objects.get(pk=expense_id)
        except:
            raise Http404("Expense does not exist")

        if expense.user != request.user:
            raise PermissionDenied
        form = ExpenseForm(request.POST, user=request.user)
        if request.method == 'POST':
            if form.is_valid():
                name = form.cleaned_data['name']
                amount = form.cleaned_data['amount']
                execution_date = form.cleaned_data['executionDate']
                category = form.cleaned_data['category']
                done = form.cleaned_data['done']

                expense.name = name
                expense.amount = amount
                expense.execution_date = execution_date
                expense.category = category
                expense.done = done
                expense.save()

            return redirect('/wallet/expense/' + str(expense_id))
        else:
            form = ExpenseForm(instance=expense, user=request.user)

        return render(request, 'wallet/expense/expenseForm.html', {'form': form, 'wallet': expense.wallet})
    else:
        return redirect("/login")


# Category

def categoryDetails(request, category_id):
    if request.user.is_authenticated:
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise Http404("category does not exist")
        if category.user != request.user:
            raise PermissionDenied
        context = {'category': category}
        return render(request, 'wallet/category/categoryDetails.html', context)
    else:
        return redirect("/login")


def categoryAdd(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                priority = form.cleaned_data['priority']
                new_category = Category(name=name, priority=priority, user=request.user)
                new_category.save()
                return HttpResponseRedirect('/wallet/category/' + str(new_category.id))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = CategoryForm()

        return render(request, 'wallet/category/categoryForm.html', {'form': form})
    else:
        return redirect("/login")


def categoryList(request):
    if request.user.is_authenticated:
        category_list = Category.objects.filter(user=request.user).order_by('-createdAt')

        context = {
            'categoryList': category_list,
        }
        return render(request, 'wallet/category/categoryList.html', context)
    else:
        return redirect("/login")


def deleteCategory(request, category_id):
    if request.user.is_authenticated:
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise Http404("category does not exist")

        if category.user == request.user:
            category.delete()
        else:
            raise PermissionDenied
        return categoryList(request)
    else:
        return redirect("/login")


def updateCategory(request, category_id):
    if request.user.is_authenticated:
        try:
            category = Category.objects.get(pk=category_id)
        except:
            raise Http404("category does not exist")
        if category.user != request.user:
            raise PermissionDenied
        form = CategoryForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                name = form.cleaned_data['name']
                priority = form.cleaned_data['priority']
                category.name = name
                category.priority = priority
                category.save()

            return redirect('/wallet/category/' + str(category_id))
        else:
            form = CategoryForm(instance=category)

        return render(request, 'wallet/expense/expenseForm.html', {'form': form})
    else:
        return redirect("/login")
