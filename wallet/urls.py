from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.walletList, name='walletList'),
    path('<int:wallet_id>/', views.walletDetails, name='walletDetail'),
    path('<int:wallet_id>/income/add', views.incomeAdd, name='incomeAdd'),
    path('add/', views.addWallet, name='addWallet'),
    path('income/', views.incomeList, name='incomeList'),
    path('income/<int:income_id>/', views.incomeDetails, name='incomeDetail'),
]
