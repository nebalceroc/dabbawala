import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files import File

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    credit_card = models.CharField(max_length=200)
    cvv = models.CharField(max_length=200)

    def __unicode__(self):
        return '%s: %s' % (self.credit_card, self.cvv)

class Product(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=500)
    photo = models.ImageField(upload_to='fotos')
    def __unicode__(self):
        return "[id%s] %s - %s (%s USD)" % (self.code, self.name, self.description, self.price)

class Request(models.Model):
    user = models.ForeignKey(User)
    pur_date = models.DateField()
    products = models.ManyToManyField(Product)
    total = models.IntegerField()
