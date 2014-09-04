from django.shortcuts import render

def menu_charge(request,request_id):
    if request.method == "POST":        
        stripe.api_key = settings.STRIPE_API_KEY
        card = request.POST.get("stripeToken")
        m = []   
        payment = Payment()
        payment.paidBy = request.user
        payment.description = "food delivery: " + item_list              
        x = price*100 #Convert from dolars to cents
        y = (x/100)*2.9 #Adjust stripe fees
        success, instance = payment.charge(int((x+y)+30), card)
        if not success:
            raise forms.ValidationError("Error: %s" % instance.message)
            
        else:
                instance.amount = amount
                instance.save()                   
                return HttpResponseRedirect("URL PARA DESPUES DE LOS PAGOS")        

    else:
        return HttpResponseRedirect("/payments/methods/")
