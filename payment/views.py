from django.shortcuts import render
from delivery import services, models
from models import Payment
from django.contrib.auth.decorators import login_required
from delivery.services import get_request
from datetime import timedelta
from django.contrib.auth.models import User
import dabbawala.settings as settings
import stripe
import datetime

#@login_required
def menu_charge(request,request_id=0):
    if request.method == "POST":        
        stripe.api_key = settings.STRIPE_API_KEY
        card = request.POST.get("stripeToken")
        m = []   
        #food_request = get_request(request_id)
        payment = Payment()
        #payment.amount = food_request.total
        payment.amount = 20
        payment.paidBy = request.user
        payment.description = "food delivery: " #+ item_list              
        x = payment.amount*100 #Convert from dolars to cents
        y = (x/100)*2.9 #Adjust stripe fees
        print card
        success, instance = payment.charge(int((x+y)+30), card)
        if not success:
            raise forms.ValidationError("Error: %s" % instance.message)
            
        else:
                instance.amount = payment.amount
                instance.save()                   
                return HttpResponseRedirect("/")        

    else:
        context = {'user': request.user,'stripe_key':settings.STRIPE_PUB_KEY}
        return render(request, 'pay.html', context)
