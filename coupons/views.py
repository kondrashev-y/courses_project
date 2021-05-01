from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone

from carts.utils import recalc_cart
from .models import Coupon
from .forms import CouponApplyForm
from carts.models import Cart



@require_POST
def coupon_apply(request, cart_id):
    """Применение купона"""
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    cart = Cart.objects.filter(id=cart_id).first()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True
                                        )
            cart.coupon = coupon
            recalc_cart(cart)
            cart.save()
        except Coupon.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Не верный купон')
        return redirect('cart')


def coupon_remove(request, cart_id):
    """Удаление купона"""
    cart = Cart.objects.filter(id=cart_id).first()
    cart.coupon = None
    recalc_cart(cart)
    cart.save()
    return redirect('cart')


