from django.shortcuts import render
from django.views.generic import DetailView, View
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Customer, Cart, CartProduct, Product, Order
from .forms import OrderForms, LoginForm, RegistrationForm
from .mixins import CartMixin
from .utils import recalc_cart
from products.models import Category
from progress.models import Progress, CheckLessons, CheckHomeworks
from progress.forms import ProgressForms, CheckHomeworkForms, CheckLessonsForms
from coupons.forms import CouponApplyForm

from django.contrib.auth.views import LoginView


class AddToCartView(LoginRequiredMixin, CartMixin, View):
    """Добавление товаров в корзину"""

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        # self.cart.save()
        messages.add_message(request, messages.INFO, "Товар успешно добавлен")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteFromCartView(LoginRequiredMixin, CartMixin, View):
    """Удаление товаров из корзины"""

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        # self.cart.save()
        messages.add_message(request, messages.INFO, "Товар удален из корзины")
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(LoginRequiredMixin, CartMixin, View):
    """Изменение количества товаров"""

    def post(self, request, *args, **kwargs):
        try:
            product_slug = kwargs.get('slug')
            product = Product.objects.get(slug=product_slug)
            cart_product = CartProduct.objects.get(
                user=self.cart.owner, cart=self.cart, product=product
            )
            qty = int(request.POST.get('qty'))
            cart_product.qty = qty
            cart_product.save()
            recalc_cart(self.cart)
            self.cart.save()
            messages.add_message(request, messages.INFO, "Кол-во успешно изменено")
        except:
            messages.add_message(request, messages.INFO, "Что то пошло не так, введите число меньше 100")
        return HttpResponseRedirect('/cart/')



class CartView(LoginRequiredMixin, CartMixin, View):
    """Отображение корзины"""

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = CouponApplyForm
        context = {
            'categories': categories,
            'cart': self.cart,
            'apply_form': form
        }
        return render(request, 'carts/cart.html', context)


class CheckoutView(LoginRequiredMixin, CartMixin, View):
    """Оформление заказа"""

    def get(self, request, *args, **kwargs):
        form = OrderForms(request.POST or None)
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'form': form,
            'categories': categories,
        }
        return render(request, 'carts/checkout.html', context)


class MakeOrderView(LoginRequiredMixin, CartMixin, View):
    """Совершение и сохранение заказа"""

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForms(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if self.cart.coupon:
            if not self.cart.coupon.active:
                messages.add_message(request, messages.INFO, 'Промокод не активный')
                return HttpResponseRedirect('/cart/')
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            # new_order.first_name = form.cleaned_data['first_name']
            # new_order.last_name = form.cleaned_data['last_name']
            # new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            # new_order.buying_type = form.cleaned_data['buying_type']
            # new_order.order_date = form.cleaned_data['order_date']
            # new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            cart_products = [i.product for i in self.cart.products.all().select_related('product')]
            if self.cart.products.exists():
                new_order.products.set(cart_products)
                for product in cart_products:
                    form_progress = ProgressForms()
                    new_progress = form_progress.save(commit=False)
                    new_progress.customer = customer
                    new_progress.product = product
                    new_progress.save()
                    lessons = product.lessons.all().select_related('homework')
                    if lessons.exists():
                        for lesson in lessons:
                            form_cheklesson = CheckLessonsForms()
                            new_checklesson = form_cheklesson.save(commit=False)
                            new_checklesson.progress = new_progress
                            new_checklesson.lesson = lesson
                            new_checklesson.save()
                            form_chekhomework = CheckHomeworkForms()
                            if lesson.homework:
                                new_checkhomework = form_chekhomework.save(commit=False)
                                new_checkhomework.checklesson = new_checklesson
                                new_checkhomework.homework = lesson.homework
                                new_checkhomework.save()
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class LoginView(CartMixin, LoginView):
    """Отображение входа"""

    form_class = LoginForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        context['categories'] = Category.objects.all()
        context['login_form'] = LoginForm()
        return context


class RegistrationView(CartMixin, View):
    """Отображение регистрации"""
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories, 'cart': self.cart, 'login_form': LoginForm()}
        return render(request, 'users/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST, request.FILES or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.bio = form.cleaned_data['bio']
            new_user.birth_date = form.cleaned_data['birth_date']
            new_user.image = form.cleaned_data['image']
            new_user.gender = form.cleaned_data['gender']
            new_user.number = form.cleaned_data['number']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                # phone = form.cleaned_data['phone'],
                # address = form.cleaned_data['bio'],
                # birth_date = form.cleaned_data['birth_date'],
                # image = form.cleaned_data['image'],
                # gender = form.cleaned_data['gender'],
            )
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {'form': form, 'cart': self.cart}
        return render(request, 'users/registration.html', context)


class ProfileView(LoginRequiredMixin, CartMixin, View):
    """Отображение личного кабинета"""
    # redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        categories = Category.objects.all()
        orders = Order.objects.filter(customer=customer).order_by('-created_at')  # сортировка по дате создания
        customer_progress = Progress.objects.select_related('product').filter(customer=customer)

        return render(
            request, 'carts/profile.html', {'customer': customer, 'categories': categories, 'orders': orders,
                                            'cart': self.cart, 'customer_progress': customer_progress}
        )


class TimeOutView(LoginRequiredMixin, CartMixin, View):
    """Отображение отказа доступа к курсу"""

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        categories = Category.objects.all()
        orders = Order.objects.filter(customer=customer).order_by('-created_at')  # сортировка по дате создания

        return render(
            request, 'carts/time_out.html', {'customer': customer, 'categories': categories, 'orders': orders, 'cart': self.cart}
        )
