from django import forms

class AddWalletForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    amount = forms.DecimalField(label='Initial amount', min_value=0)