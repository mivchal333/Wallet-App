import datetime

from django import forms
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _

from wallet.models import Category, Wallet, Income


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'amount']
        widgets = {
            'name': TextInput(attrs={'class': "form-control"}),
            'amount': forms.NumberInput(attrs={'class': "form-control"})
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
            'amount': forms.TextInput(attrs={'class': "form-control"}),
            'executionDate': forms.DateTimeInput(attrs={'class': "form-control"}),
            'category': forms.Select(attrs={'class': "form-control"})
        }


class AddExpenseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddExpenseForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.filter(user=user), required=False,
                                                         widget=forms.Select(attrs={'class': "form-control"}))

    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    amount = forms.DecimalField(label='Amount', min_value=1, required=True,
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    executionDate = forms.DateTimeField(initial=datetime.date.today, label='Date',
                                        widget=forms.TextInput(attrs={'class': "form-control"}))
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.filter(user__id=1),
                                      widget=forms.Select(attrs={'class': "form-control"}))
    done = forms.BooleanField(required=False)


class AddCategoryForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    priority = forms.DecimalField(label='Priority', min_value=1, required=True, max_value=10,
                                  widget=forms.TextInput(attrs={'class': "form-control", 'type': 'number'}))
