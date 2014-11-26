from django.contrib import admin
from delivery.models import Product, UserProfile, Request, RequestProduct

admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Request)
admin.site.register(RequestProduct)
