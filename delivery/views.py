from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from delivery.models import Product, Request, Cart, UserProfile, CartProduct, RequestProduct
from delivery.forms import UserForm, UserProfileForm
from delivery.services import get_user_cart
import datetime

def index(request):
    if request.method == "POST":
        if request.POST.get("add_item"):
            item = request.POST.get("add_item")
            u = request.user
            cart = get_user_cart(u.id)
            p = Product.objects.get(pk=item)
            cp = CartProduct(cart=cart,product=p,amount=int(request.POST.get("quantity")))
            cp.save()      
            print cp
            
            
    latest_products = Product.objects.all()
    context = {'latest_products': latest_products}
    return render(request, 'index.html', context)

def checkout(request):
    u = request.user
    cart = get_user_cart(u.id)
    total=0    
    all_products = CartProduct.objects.filter(cart_id=cart.id)
    r = Request(state='C',user=request.user, pur_date=datetime.datetime.now(), total=0)
    r.save()
    for p in all_products:
        print p.product.name
        print p.amount
        request_item = RequestProduct(request=r, product=p.product, amount=p.amount)
        request_item.save()
        total+=p.product.price
            
    r.total=total
    r.save() 

    context = {'total': total, 'cents_total': total * 100, 'request_id': r.id}
    return render(request, 'cart.html', context)
    
        
    
    

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)       
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = UserProfile(rol="C")
            profile.user = user
            profile.save()
            new_cart = Cart()
            new_cart.user_id = profile           
            new_cart.save()
            registered = True
            return HttpResponseRedirect('/')
            
            
    user_form = UserForm()
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'registered': registered},
            context)

def cart(request):
    products = {k: v for k, v in request.POST.iteritems() if k != u'csrfmiddlewaretoken' and v != '0'}
    
    # Integer validation
    try:
        amounts = [int(v) for v in products.itervalues()]
    except ValueError:
        return HttpResponse('Invalid amounts')

    order = {}
    total = 0
    for c, amount in products.iteritems():
        name = Product.objects.get(pk=c).name
        order[name] = (amount, Product.objects.get(pk=c).price * int(amount))
        total += order[name][1]

    product_list = [name for name in order.iterkeys()]

    product_queryset = [Product.objects.get(name=c) for c in order.iterkeys() ]
    r = Request(user=request.user, pur_date=datetime.datetime.now(), total=total)
    r.save()
    for p in product_queryset:
        r.products.add(p)

    context = {'order': order, 'total': total, 'cents_total': total * 100, 'request_id': r.id}
    return render(request, 'cart.html', context)

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            print user.is_active
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/delivery/')
            else:
                return HttpResponse('Invalid login details.')
        else:
            print 'Invalid login details: {0}:{1}'.format(username, password)
            return HttpResponse('Your Dabbawala account is disabled')
    else:
        return render_to_response('login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/delivery/')
