from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=20, default='')
    priority = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Family(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    userList = models.ManyToManyField(User)


class Wallet(models.Model):
    name = models.CharField(max_length=20)
    amount = models.FloatField(default='0')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.SET_NULL, related_name='wallets', null=True, blank=True)
    family = models.ForeignKey(Family, models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    name = models.CharField(max_length=20)
    amount = models.FloatField(default='0')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    executionDate = models.DateTimeField(blank=True, null=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    done = models.BooleanField()

    def __str__(self):
        return self.name


class Income(models.Model):
    source = models.CharField(max_length=20)
    amount = models.FloatField(default='0')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    executionDate = models.DateTimeField(blank=True, null=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.source
