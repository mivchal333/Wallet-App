import datetime

from django import forms

from wallet.models import Category


class AddWalletForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    amount = forms.DecimalField(label='Initial amount', min_value=0, initial=0,
                                widget=forms.TextInput(attrs={'class': "form-control"}))


class AddIncomeForm(forms.Form):
    source = forms.CharField(label='Source', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    amount = forms.DecimalField(label='Amount', min_value=1, required=True,
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    date = forms.DateTimeField(initial=datetime.date.today, label='Date',
                               widget=forms.DateTimeInput(attrs={'class': "form-control"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False,
                                      widget=forms.Select(attrs={'class': "form-control"}))


class AddExpenseForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    amount = forms.DecimalField(label='Amount', min_value=1, required=True,
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    executionDate = forms.DateTimeField(initial=datetime.date.today, label='Date',
                                        widget=forms.TextInput(attrs={'class': "form-control"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False,
                                      widget=forms.Select(attrs={'class': "form-control"}))
    done = forms.BooleanField(required=False)
