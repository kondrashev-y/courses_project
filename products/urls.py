from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import BaseView, CategoryDetailView, ProductDetailView, LessonDetailView,\
    ProductLearnView, AddComments, create_child_comment
from carts.views import (ProfileView, LoginView, RegistrationView, ChangeQTYView, TimeOutView,
                         CartView, AddToCartView, DeleteFromCartView,
                         CheckoutView, MakeOrderView,
                         )
from coupons.views import coupon_apply, coupon_remove

urlpatterns = [
    path("", BaseView.as_view(), name='base'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
    path('apply/<int:cart_id>/', coupon_apply, name='apply'),
    path('remove/<int:cart_id>/', coupon_remove, name='remove'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order', MakeOrderView.as_view(), name='make_order'),
    path('course/<str:slug>/lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('course/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('course-learn/<str:slug>/<int:pk>/', ProductLearnView.as_view(), name='product_learn_detail'),
    path('time_out/', TimeOutView.as_view(), name='time_out'),
    path("comment/<int:pk>/", AddComments.as_view(), name="add_comment"),
    path('create-child-comment/', create_child_comment, name='comment_child_create'),

]
