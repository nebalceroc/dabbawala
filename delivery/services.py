from delivery.models import Request, UserProfile, Cart

def get_request(request_id):
    request = Request.objects.get(id=request_id)
    return request

def get_user_cart(u):
    pu = UserProfile.objects.get(user_id=u)
    cart = Cart.objects.get(user_id=pu.id)
    return cart