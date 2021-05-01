from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Модель профиля пользователя"""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    GENDER_CHOICE = (
        ('Male', 'Мужской'),
        ('Female', 'Женский')
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name='Информация о себе')
    number = models.CharField(max_length=30, verbose_name='Номер телефона')
    birth_date = models.DateField(null=True, verbose_name='День рожения')
    gender = models.CharField(choices=GENDER_CHOICE, max_length=30, blank=True, verbose_name='Пол')
    image = models.ImageField(verbose_name='Изображение', blank=True, upload_to='avatar/')
    # group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

