from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Family)
admin.site.register(Category)
admin.site.register(Wallet)
admin.site.register(Income)
admin.site.register(Expense)

