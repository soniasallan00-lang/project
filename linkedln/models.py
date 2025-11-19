from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class fruits(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='')
    price=models.FloatField()


class CartItem(models.Model):
    fruits = models.ForeignKey(fruits, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)   

class BillingDetails(models.Model):
     firstname=models.CharField(max_length=50)  
     lastname=models.CharField(max_length=50)  
     address=models.CharField(max_length=50)
     emailaddress=models.EmailField(max_length=50)
     zip=models.CharField(max_length=50)
     phone=models.CharField(max_length=50)
     cart_id = models.ForeignKey(CartItem,on_delete=models.CASCADE)
     user = models.ForeignKey(User, on_delete=models.CASCADE)


class cnt(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    subject=models.CharField(max_length=50)
    message=models.CharField(max_length=50)



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(fruits, on_delete=models.CASCADE)

class UserRegistration(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)  # store hashed password later
    created_at = models.DateTimeField(auto_now_add=True)

