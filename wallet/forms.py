import datetime

from django import forms

from wallet.models import Category


class AddWalletForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    amount = forms.DecimalField(label='Initial amount', min_value=0, initial=0,
                                widget=forms.TextInput(attrs={'class': "form-control"}))


class AddIncomeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddIncomeForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.filter(user=user), required=False,
                                                         widget=forms.Select(attrs={'class': "form-control"}))

    source = forms.CharField(label='Source', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    amount = forms.DecimalField(label='Amount', min_value=1, required=True,
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    date = forms.DateTimeField(initial=datetime.date.today, label='Date',
                               widget=forms.DateTimeInput(attrs={'class': "form-control"}))
    category = forms.ModelChoiceField(queryset=Category.objects.filter(user__id=1), required=False,
                                      widget=forms.Select(attrs={'class': "form-control"}))


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
