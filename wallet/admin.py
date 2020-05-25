from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)

admin.site.site_header = 'Wallet Administration'
admin.site.site_url = '/wallet'
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('source', 'amount', 'wallet', 'user')
    list_editable = ['amount', 'user', 'wallet']
    search_fields = ('name', 'user__username', 'wallet__name')
admin.site.register(Income, IncomeAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'wallet', 'user')
    list_editable = ['amount', 'user', 'wallet']
    search_fields = ('name', 'user__username', 'wallet__name')
admin.site.register(Expense, ExpenseAdmin)

class WalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'user', 'updatedAt', 'createdAt')
    list_editable = ['amount', 'user']
    search_fields = ('name', 'user__username')
    fields = (
        'name',
        'amount',
        'user'
    )

admin.site.register(Wallet, WalletAdmin)


