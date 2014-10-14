import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files import File

class UserProfile(models.Model):
    Rol_Types = (
        ('A', 'Admin'),
        ('O', 'Operador'),
        ('D', 'Domiciliario'),
        ('C', 'Cliente')
    )
    rol=models.CharField(max_length=1, choices=Rol_Types)
    user = models.OneToOneField(User)

    
    
class Product(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=500)
    photo = models.ImageField(upload_to='fotos')
    def __unicode__(self):
        return "[id%s] %s - %s (%s USD)" % (self.code, self.name, self.description, self.price)

class Cart(models.Model):
    user_id = models.OneToOneField(UserProfile)
    
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    


class Request(models.Model):
    State_Types = (
        ('C', 'Created'),
        ('P', 'PreCreated'),
        ('A', 'Asigned'),
        ('S', 'Send'),
        ('P', 'Paid'),
        ('X', 'Incomplete')
    )
    state=models.CharField(max_length=1, choices=State_Types)
    user = models.ForeignKey(User)
    pur_date = models.DateField()
    total = models.IntegerField()
    
class RequestProduct(models.Model):
    request = models.ForeignKey(Request)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
