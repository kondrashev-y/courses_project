from django.contrib import admin
from .models import (Product, Lessons, HomeWork, Comments,
                     Documents, Speakers, Category)


@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    """Задания"""
    list_display = ("id", "title",)
    list_display_links = ("title",)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Комментарии"""
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Комментарии"""
    pass


@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    """Уроки"""
    pass


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    """Документы"""
    pass


@admin.register(Speakers)
class SpeakersAdmin(admin.ModelAdmin):
    """Спикеры"""
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Курсы"""
    list_display = ("id", "title", "category", "slug", "product_type", "price", "draft")
    list_display_links = ("title",)
    search_fields = ("title", "slug")
    list_editable = ("draft",)

