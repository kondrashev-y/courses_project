from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from carts.forms import LoginForm
from carts.mixins import CartMixin, CustomPermissionMixin
from .forms import CommentForm
from .models import Product, Lessons, Category, Comments
from carts.models import Customer
from .utils import create_comments_tree


from progress.models import Progress, CheckLessons, CheckHomeworks

from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect

User = get_user_model()


class BaseView(CartMixin, generic.View):
    """Отображение всех товаров"""
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'cart': self.cart,
            'login_form': LoginForm()
        }
        return render(request, 'home.html', context)


class CategoryDetailView(CartMixin, generic.DetailView):
    """Категория продукта"""

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'products/category_detail.html'
    # slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.select_related('category').filter(draft=False, category__slug=self.kwargs.get('slug'))
        context['cart'] = self.cart
        context['categories'] = self.queryset
        return context


class ProductDetailView(LoginRequiredMixin, CustomPermissionMixin, CartMixin, generic.DetailView):
    """Отображение продукта"""

    model = Product
    queryset = Product.objects.filter(draft=False)
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cart'] = self.cart
        context['categories'] = Category.objects.all()
        return context


class ProductLearnView(LoginRequiredMixin, CustomPermissionMixin, CartMixin, generic.View):
    """Отображение продуката и прогресса"""

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        progress = Progress.objects.select_related('product').get(id=self.kwargs.get('pk'))
        checklessons = CheckLessons.objects.select_related('lesson').filter(progress=progress)
        comments = progress.product.comments.all()
        result = create_comments_tree(comments)
        # js_lessons = serializers.serialize("json", checklessons)
        context = {
            'cart': self.cart,
            'progress': progress,
            'categories': Category.objects.all(),
            'customer': customer,
            'product': progress.product,
            'checklessons': checklessons,
            'comment_form': CommentForm(),
            'comments': result,
        }
        return render(request, 'products/product_learn.html', context)


class LessonDetailView(LoginRequiredMixin, CustomPermissionMixin, CartMixin, generic.DetailView):
    """Отображение урока"""
    model = Lessons
    template_name = 'products/lesson_detail.html'
    context_object_name = 'lesson'
    queryset = Lessons.objects.all()
    pk_url_kwarg = 'pk'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cart'] = self.cart
        context['categories'] = Category.objects.all()
        context['product'] = Product.objects.get(slug=self.kwargs.get('slug'))
        return context


class AddComments(generic.View):
    """Комментарий"""
    def post(self, request, pk):
        comment_form = CommentForm(request.POST)
        progress = Progress.objects.get(id=pk)
        if comment_form.is_valid():
            new_comment_form = comment_form.save(commit=False)
            new_comment_form.user = request.user
            new_comment_form.text = comment_form.cleaned_data['text']
            new_comment_form.content_type = ContentType.objects.get(model='product')
            new_comment_form.object_id = progress.product.pk
            new_comment_form.parent = None
            new_comment_form.is_child = False
            new_comment_form.save()
        return redirect(progress.get_absolute_url())


@transaction.atomic
def create_child_comment(request):
    user_id = request.POST.get('user')
    current_id = request.POST.get('id')
    text = request.POST.get('text')
    user = User.objects.get(id=user_id)
    content_type = ContentType.objects.get(model='product')
    parent = Comments.objects.get(id=int(current_id))
    object_id = parent.object_id
    is_child = False if not parent else True
    Comments.objects.create(
        user=user, text=text, content_type=content_type, object_id=object_id,
        parent=parent, is_child=is_child
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

