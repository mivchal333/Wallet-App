from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Wallet


def index(request):
    return HttpResponse("Hello world from wallet app!")


def walletDetails(request, wallet_id):
    wallet = Wallet.objects.get(pk=wallet_id)
    context = {
        'wallet': wallet,
    }
    return render(request, 'wallet/walletDetails.html', context)
