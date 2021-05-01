from django.contrib import admin

from .models import CartProduct, Cart, Customer, Order


admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
