from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:wallet_id>/', views.walletDetails, name='walletDetail'),
    path('add/', views.addWallet, name='addWallet'),
    path('income/<int:income_id>/', views.incomeDetails, name='incomeDetail'),
]