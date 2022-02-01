from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    product_name = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    mrp = models.IntegerField()

class Shipping(models.Model):
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    pin = models.CharField(max_length=200)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
