from delivery.models import Request, UserProfile, Cart, CartProduct

def get_request(request_id):
    request = Request.objects.get(id=request_id)
    return request

def get_user_cart(u):
    pu = UserProfile.objects.get(user=u.id)
    try:
        cart = Cart.objects.get(user_id=pu)
    except Cart.DoesNotExist:
        cart = Cart(user_id=pu)
        cart.save()
    
    return cart

def empty_cart(cart):
    list = get_cart_list(cart)
    for item in list:
        item.delete()

def get_cart_list(cart):
    list = CartProduct.objects.filter(cart=cart)
    return list

def get_user_rol(user):
    user = UserProfile.objects.get(user=user)
    return user.rol
        
    