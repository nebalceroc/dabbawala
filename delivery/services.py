from delivery.models import Request, UserProfile, Cart, CartProduct

def get_request(request_id):
    request = Request.objects.get(id=request_id)
    return request

def get_user_cart(u):
    pu = UserProfile.objects.get(user=u)
    try:
        cart = Cart.objects.get(user_id=pu)
    except Cart.DoesNotExist:
        cart = Cart(user_id=pu)
        cart.save()
    
    return cart

def get_cart_list(cart):
    list = CartProduct.objects.filter(cart=cart)
    print list
    return list