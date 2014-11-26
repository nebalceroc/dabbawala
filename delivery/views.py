from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from delivery.models import Product, Request, Cart, UserProfile, CartProduct, RequestProduct
from delivery.forms import UserForm
from delivery.services import get_user_cart, get_cart_list, get_user_rol, empty_cart, get_request
import datetime

def index(request):
    u = request.user
    cart_list=[]  
    if request.user.is_authenticated():
        cart = get_user_cart(u)
        cart_list = get_cart_list(cart)  
        
    if request.method == "POST":
        if request.POST.get("add_item"):
            item = request.POST.get("add_item")    
            p = Product.objects.get(pk=item)
            q =int(request.POST.get("quantity"))
            try:
                up_q = int(CartProduct.objects.get(cart=cart,product=p).amount) + int(q)
                CartProduct.objects.filter(cart=cart,product=p).update(amount=up_q)
            except:       
                cproduct = CartProduct(product=p,cart=cart,amount=q)
                cproduct.save()  
                
                  
            
          
    latest_products = Product.objects.all()                 
    
    context = {'latest_products': latest_products, 'cart_list':cart_list}
    return render(request, 'index.html', context)

def op_panel(request):
    if request.method == "POST":
        rid = request.POST.get("r_id")
        did = request.POST.get("d_id")
        req = get_request(rid)
        dom = UserProfile.objects.get(pk=did)
        req.delivery_man = dom
        req.state="A"
        req.save()        
    
    d_list = UserProfile.objects.filter(rol='D')
    pending_requests = Request.objects.filter(state='C')
    context = {'pending_requests': pending_requests, 'd_list':d_list}
    return render(request, 'panel.html', context)

def dom_panel(request):     
    up = UserProfile.objects.get(user=request.user)
    pending_requests = Request.objects.filter(delivery_man=up)
    context = {'pending_requests': pending_requests}
    return render(request, 'dom_panel.html', context)

def checkout(request):
    u = request.user
    cart = get_user_cart(u)
    total=0    
    all_products = CartProduct.objects.filter(cart_id=cart.id)
    product_list=all_products
    for p in all_products:
                total+=p.product.price*p.amount
    
    context = {'product_list':product_list ,'total': total ,'cents_total':total*100}            
    if request.method == "POST":
        if request.POST.get("mod_item"):
            item = request.POST.get("mod_item")    
            p = Product.objects.get(pk=item)
            q =int(request.POST.get("quantity"))
            print p.name
            print q
            try:
                CartProduct.objects.filter(cart=cart,product=p).update(amount=q)
                return HttpResponseRedirect('/delivery/checkout/')
            except:       
                print "error"
            
        if request.POST.get("dir"):
            product_list=[]
            r = Request(state='C',user=request.user, pur_date=datetime.datetime.now(), total=0)
            r.save()
            for p in all_products:
                request_item = RequestProduct(request=r, product=p.product, amount=p.amount)
                request_item.save()
                product_list.append(request_item)
            
            r.total=total
            r.dir = request.POST.get("dir")
            r.save() 
            empty_cart(cart)
            context = {'product_list':product_list ,'total': total , 'rid':r.id, 'cents_total':total*100}
            return render(request, 'order.html', context)      
    
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
                rol = get_user_rol(user)
                if rol == "A":
                    return HttpResponseRedirect('/admin/')
                
                if rol == "C":               
                    return HttpResponseRedirect('/delivery/')
                
                if rol == "O":               
                    return HttpResponseRedirect('/delivery/op/')
                
                if rol == "D":               
                    return HttpResponseRedirect('/delivery/dom/')
                
            else:
                return HttpResponse('Invalid login details.')
        else:
            print 'Invalid login details: {0}:{1}'.format(username, password)
            return HttpResponse('Invalid login data')
    else:
        return render_to_response('login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/delivery/')
