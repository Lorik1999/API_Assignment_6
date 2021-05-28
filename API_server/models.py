from django.db import models

# Create your models here.
class Topping(models.Model):
    Topping_name= models.CharField(max_length=200)

class Pizza(models.Model):
    pizza_id= models.IntegerField()
    name=models.CharField(max_length=200)
    vegetarian= models.BooleanField()
    price= models.DecimalField(decimal_places=2,max_digits=4)
    toppings= models.ManyToManyField(Topping)

class Pizza_Ordered(models.Model):
    pizza= models.ManyToManyField(Pizza, blank=True)
    number_ordered = models.IntegerField()

class Order(models.Model):
    takeaway= models.BooleanField()
    payment_type= models.CharField(max_length=200)
    customer_id= models.IntegerField()
    note= models.CharField(max_length=250)
    street= models.CharField(max_length=50)
    city= models.CharField(max_length=50)
    country= models.CharField(max_length=50)
    zipcode=models.CharField(max_length=50)
    ordered_at=models.DateTimeField()
    delivery_time=models.DateTimeField()
    status=models.CharField(max_length=50)
    pizzas=models.ManyToManyField(Pizza_Ordered, blank=True)
    cancelled = models.BooleanField(default=False)













