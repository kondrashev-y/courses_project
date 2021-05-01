from django.db import models
from django.core.validators import MaxValueValidator
from django.urls import reverse

from carts.models import Customer
from products.models import Product, Lessons, HomeWork


class Progress(models.Model):
    """Прогресс поьзователя"""
    customer = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    finish = models.BooleanField(verbose_name='Пройден', default=False)
    created_at = models.DateField(auto_now=True, verbose_name='Дата начала')
    passed = models.PositiveSmallIntegerField(default=0, verbose_name='Процент прохождения',
                                              validators=[MaxValueValidator(100),])

    def __str__(self):
        return f'{self.customer} - {self.product}'

    class Meta:
        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогрессы'

    def get_absolute_url(self):
        return reverse('product_learn_detail', kwargs={'slug': self.product.slug, 'pk': self.id})


class CheckLessons(models.Model):
    """Чекпоинт по урокам"""
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, verbose_name='Урок')
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE, verbose_name='Прогресс')
    finish = models.BooleanField(verbose_name='Пройден', default=False)

    def __str__(self):
        return str(self.finish)

    class Meta:
        verbose_name = 'Чекпоинт урока'
        verbose_name_plural = 'Чекпоинты уроков'


class CheckHomeworks(models.Model):
    """Чекпоинт по заданиям"""
    homework = models.ForeignKey(HomeWork, on_delete=models.CASCADE, verbose_name='Задание')
    checklesson = models.ForeignKey(CheckLessons, on_delete=models.CASCADE, verbose_name='Чекпоинт урока')
    finish = models.BooleanField(verbose_name='Пройден', default=False)

    def __str__(self):
        return str(self.finish)

    class Meta:
        verbose_name = 'Чекпоинт задания'
        verbose_name_plural = 'Чекпоинты заданий'
