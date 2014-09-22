import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    credit_card = models.CharField(max_length=200)
    cvv = models.CharField(max_length=200)

    def __unicode__(self):
        return '%s: %s' % (self.credit_card, self.cvv)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=500)

    def __unicode__(self):
        return "%s: %s" % (self.name, self.description)

class Request(models.Model):
    user = models.ForeignKey(User)
    pur_date = models.DateField()
    products = models.ManyToManyField(Product)
    total = models.IntegerField()