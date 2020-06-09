from django.test import TestCase

from wallet.models import Wallet
from wallet.service import updateWalletAmount, WalletAction


class updateWalletAmountTest(TestCase):
    def setUp(self):
        Wallet.objects.create(name="w1", amount=100)

    def test_add_income_wallet_amount(self):
        w1 = Wallet.objects.get(name="w1")
        updateWalletAmount(w1.id, 100, WalletAction.ADD)
        w1 = Wallet.objects.get(name="w1")
        self.assertEqual(w1.amount, 200)

    def test_add_expense_wallet_amount(self):
        w1 = Wallet.objects.get(name="w1")
        updateWalletAmount(w1.id, 1, WalletAction.SUBTRACT)
        w1 = Wallet.objects.get(name="w1")
        self.assertEqual(w1.amount, 99)
