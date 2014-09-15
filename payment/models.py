from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
import dabbawala.settings as settings
import stripe
import datetime
         
class Payment(models.Model):
    datetime_created = models.DateTimeField(default=datetime.datetime.now()- timedelta(hours=5))
    amount = models.IntegerField()
    #paidBy= models.ForeignKey(User)
    charge_id = models.CharField(max_length=100)
    payment_id =models.CharField(max_length=100)
        
    def __init__(self, *args,**kwargs):
        super(Payment,self).__init__(*args,**kwargs)
        stripe.api_key= settings.STRIPE_API_KEY
        self.stripe = stripe
        
    def charge(self, price_in_cents, card_instance):
        """ 
        Returns a tuple: (Boolean, Class) where the boolean is if
        the charge was successful, and the class is response (or error)
        instance.
        """
 
        if self.charge_id: # don't let this be charged twice!
            return False, Exception(message="Already charged.")
 
        try:
            response = self.stripe.Charge.create(
                amount = price_in_cents,
                currency = "usd",
                card = card_instance,
                description=self.description
                )
 
            self.charge_id = response.id
 
        except self.stripe.CardError, ce:
            # charge failed
            return False, ce
 
        return True, self