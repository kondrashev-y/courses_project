from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# from carts.models import Cart


class Coupon(models.Model):
    """Модель скидочного промокода"""
    code = models.SlugField(max_length=30, unique=True, verbose_name='Промокод')
    valid_from = models.DateTimeField(verbose_name='Дата начала действия')
    valid_to = models.DateTimeField(verbose_name='Дата окончания действия')
    active = models.BooleanField(verbose_name='Активный')
    # discount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Размер скидки')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   verbose_name='Размер скидки')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

