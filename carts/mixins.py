from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages

from products.models import Product
from .models import Cart, Customer, Order

from datetime import timedelta, datetime, date


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)


class CustomPermissionMixin(UserPassesTestMixin):

    def test_func(self):
        customer = Customer.objects.get(user=self.request.user)
        product = self.kwargs.get('slug')
        customer_products = Product.objects.filter(order__customer=customer).values_list('slug', flat=True)
        customer_product = Product.objects.filter(slug=product, order__customer=customer).first()
        order = Order.objects.filter(products=customer_product, customer=customer).first()
        if customer_product:
            today = date.today()
            active_time = customer_product.active_time
            delta = today - datetime.date(order.created_at)
            if (active_time - delta) < timedelta(0):
                return 'time'
        if product in customer_products:
            return 'yes'
        else:
            return 'no'

    def dispatch(self, request, *args, **kwargs):
        status = self.get_test_func()()
        if status == 'time':
            return HttpResponseRedirect('/time_out/')
        elif status == 'no':
            return self.handle_no_permission()
        else:
            return super().dispatch(request, *args, **kwargs)




