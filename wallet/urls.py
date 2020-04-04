from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:wallet_id>/', views.walletDetails, name='detail'),

]