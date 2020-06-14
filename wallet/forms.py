from django import forms
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _

from wallet.models import Category, Wallet, Income, Expense


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'description']
        widgets = {
            'name': TextInput(attrs={'class': "form-control"}),
            'description': TextInput(attrs={'class': "form-control"}),
        }


class IncomeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.filter(user=user), required=False,
                                                         widget=forms.Select(attrs={'class': "form-control"}))

    class Meta:
        model = Income
        fields = ['source', 'amount', 'executionDate', 'category']
        labels = {
            'executionDate': _("Execution Date")
        }
        widgets = {
            'source': forms.TextInput(attrs={'class': "form-control"}),
            'amount': forms.NumberInput(attrs={'class': "form-control", 'min': '0.01'}),
            'executionDate': forms.DateTimeInput(attrs={'class': "form-control"}),
            'category': forms.Select(attrs={'class': "form-control"})
        }


class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.filter(user=user), required=False,
                                                         widget=forms.Select(attrs={'class': "form-control"}))

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'executionDate', 'category']
        labels = {
            'executionDate': _("Execution Date")
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'amount': forms.NumberInput(attrs={'class': "form-control", 'min': '0.01'}),
            'executionDate': forms.DateTimeInput(attrs={'class': "form-control"}),
            'category': forms.Select(attrs={'class': "form-control"})
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'priority']
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'priority': forms.TextInput(attrs={'class': "form-control", 'type': 'number', 'min': '1', 'max': '10'}),
        }
