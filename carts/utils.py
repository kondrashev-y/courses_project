from django.db import models
from decimal import Decimal


def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if cart_data.get('final_price__sum'):
        cart.total_price = cart_data['final_price__sum']
        if cart.coupon:
            cart.final_price = cart.total_price - cart.total_price * (cart.coupon.discount / Decimal('100'))
        else:
            cart.final_price = cart.total_price
    else:
        cart.final_price = 0
    cart.total_product = cart_data['id__count']
    cart.save()