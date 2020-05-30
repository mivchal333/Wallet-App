from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.walletList, name='walletList'),
    path('<int:wallet_id>/', views.walletDetails, name='walletDetail'),
    path('<int:wallet_id>/delete', views.deleteWallet, name='deleteWallet'),
    path('<int:wallet_id>/income/add', views.incomeAdd, name='incomeAdd'),
    path('<int:wallet_id>/update', views.updateWallet, name='updateWallet '),
    path('add/', views.addWallet, name='addWallet'),
    path('income/', views.incomeList, name='incomeList'),
    path('income/<int:income_id>/', views.incomeDetails, name='incomeDetail'),
    path('income/<int:income_id>/delete', views.deleteIncome, name='incomeDelete'),
    path('income/<int:income_id>/update', views.updateIncome, name='incomeUpdate'),
    path('expense/', views.expenseList, name='expenseList'),
    path('expense/<int:expense_id>/', views.expenseDetails, name='expenseDetails'),
    path('<int:wallet_id>/expense/add', views.expenseAdd, name='expenseAdd'),
    path('expense/<int:expense_id>/delete', views.deleteExpense, name='expenseDelete'),
    path('expense/<int:expense_id>/update', views.updateExpense, name='updateExpense'),
    path('category/', views.categoryList, name='categoryList'),
    path('category/add', views.categoryAdd, name='categoryAdd'),
    path('category/<int:category_id>', views.categoryDetails, name='categoryDetails'),
    path('category/<int:category_id>/delete', views.deleteCategory, name='deleteCategory'),
    path('category/<int:category_id>/update', views.updateCategory, name='updateCategory'),
]
