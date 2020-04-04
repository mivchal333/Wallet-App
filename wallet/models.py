from django.db import models
from django.contrib.auth.models import User


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=20, default='')
    priority = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Family(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    userList = models.ManyToManyField(AppUser)


class Wallet(models.Model):
    name = models.CharField(max_length=20)
    amount = models.FloatField(default='0')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Expense(models.Model):
    name = models.CharField(max_length=20)
    amount = models.FloatField(default='0')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    executionDate = models.DateTimeField(blank=True, null=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
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
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.source

