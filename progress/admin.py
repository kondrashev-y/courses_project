from django.contrib import admin
from .models import Progress, CheckLessons, CheckHomeworks


@admin.register(Progress)
class CategoryAdmin(admin.ModelAdmin):
    """Прогресс"""
    list_display = ("id", "product", "created_at", "passed", "finish")
    list_display_links = ("product",)


@admin.register(CheckHomeworks)
class CategoryAdmin(admin.ModelAdmin):
    """Чекпоинт задания"""
    list_display = ("id", "checklesson", "homework", "finish")
    list_display_links = ("id", "checklesson",)


@admin.register(CheckLessons)
class CategoryAdmin(admin.ModelAdmin):
    """Чекпоинт Урока"""
    list_display = ("id", "lesson", "progress", "finish")
    list_display_links = ("id", "progress",)
