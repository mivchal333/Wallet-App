from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=20)
    priority = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)


class Family(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    userList = models.ManyToManyField(AppUser)


class Expense(models.Model):
    name = models.CharField(max_length=20)
    amount = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    executionDate = models.DateTimeField(auto_now_add=True)
    wallet = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    done = models.BooleanField()

    def __str__(self):
        return self.name


class Income(models.Model):
    source = models.CharField(max_length=20)
    amount = models.BooleanField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    executionDate = models.DateTimeField(auto_now_add=True)
    wallet = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Wallet(models.Model):
    name = models.CharField(max_length=20)
    amount = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
