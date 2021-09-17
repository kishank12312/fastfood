from django.db import models
from django.contrib.auth.models import User
from django.utils import tree


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    CustomerName = models.CharField(max_length=300, null=True, blank=True)
    Address = models.TextField(null=True, blank=True)
    DateOfBirth = models.DateField(auto_now_add=False)

class Products(models.Model):
    ProductID = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=200, null=True, blank=True)
    Stock = models.IntegerField()
    Category = models.CharField(max_length=200, null=True, blank=True)
    Price = models.IntegerField()
    Description = models.CharField(max_length=600, blank=True, null=True)
    Vegetarian = models.BooleanField(default=False)
    Image = models.ImageField(null= True, blank=True)

    def __str__(self):
        return self.ProductName
class Cart(models.Model):
    Cart_ID = models.AutoField(primary_key=True)
    CustomerID = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True)
    ProductID = models.ForeignKey(Products,on_delete=models.SET_NULL, null=True)
    Quantity = models.IntegerField(default=1)

class Orders(models.Model):
    OrderID = models.AutoField(primary_key=True)
    OrderNumber = models.CharField(null=True, max_length=400)
    CustomerID = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True)
    ProductID = models.ForeignKey(Products,on_delete=models.SET_NULL, null=True)
    DateOrdered = models.DateTimeField(auto_now_add=True)
    OrderStatus = models.CharField(max_length=100, null=True, blank=True)
    Address = models.TextField(null=True, blank=True)
    ItemPrice = models.IntegerField(null=True)
    Qty = models.IntegerField(default=1)