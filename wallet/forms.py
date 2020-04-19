from django import forms
import datetime
from wallet.models import Category



class AddWalletForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    amount = forms.DecimalField(label='Initial amount', min_value=0, initial=0, help_text="start")


class AddIncomeForm(forms.Form):
    source = forms.CharField(label='Source', max_length=100)
    amount = forms.DecimalField(label='Amount', min_value=0, initial=0)
    date = forms.DateTimeField(initial=datetime.date.today, label='Date')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
