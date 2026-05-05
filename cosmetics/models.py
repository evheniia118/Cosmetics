from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.FloatField()
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} | {self.login_time}"