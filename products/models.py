from datetime import timedelta

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


User = get_user_model()


def curse_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'curse_{0}/{1}'.format(instance.slug, filename)


class Category(models.Model):
    """Категории"""
    STATUS_COMPLETED = 'completed'
    STATUS_ACTIVE = 'active'
    STATUS_FUTURE = 'future'

    STATUS_CHOICES = (
        (STATUS_COMPLETED, 'Завершенный'),
        (STATUS_ACTIVE, 'Активный'),
        (STATUS_FUTURE, 'В разработке')
    )

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение', upload_to=curse_directory_path, blank=True)
    description = models.TextField(max_length=1000, verbose_name='Описание категории', default='text')
    status = models.CharField(max_length=25,
                              choices=STATUS_CHOICES, default=STATUS_FUTURE, verbose_name='Статус категории продукта')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


    class Meta:
        verbose_name = 'Катеогря продукта'
        verbose_name_plural = 'Катеогрии продукта'


class Lessons(models.Model):
    """Уроки"""
    slug = models.SlugField(unique=True, verbose_name='slug')
    title = models.CharField(max_length=150, verbose_name='Заголовок урока')
    descriptions = models.TextField(max_length=1000, verbose_name='Описание урока', blank=True)
    video = models.FileField(upload_to='video/%y')
    position = models.PositiveSmallIntegerField()
    homework = models.ForeignKey('HomeWork', verbose_name='Домашнее задание', on_delete=models.SET_NULL, null=True,
                                 blank=True)

    def __str__(self):
        return self.slug

    # def get_absolute_url(self):
    #     return reverse('lesson_detail', kwargs={'slug': self.product.slug, 'pk': self.id})

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Documents(models.Model):
    """Документы"""
    title = models.CharField(max_length=150, verbose_name='Заголовок доп. матерала')
    descriptions = models.TextField(max_length=500, verbose_name='Описание доп. матерала')
    doc = models.FileField(verbose_name='Документ')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"


class Speakers(models.Model):
    """Спикеры курсов"""
    slug = models.SlugField(unique=True, verbose_name='slug')
    name = models.CharField(max_length=80, verbose_name='Имя')
    last_name = models.CharField(max_length=80, verbose_name='Фамилия')
    description = models.TextField(max_length=1000, verbose_name='Описание спикира')
    photo = models.ImageField(verbose_name='Фотография')

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = "Спикер"
        verbose_name_plural = "Спикеры"


class Product(models.Model):
    """Модель продукта"""
    TYPE_FREE = 'Free'
    TYPE_SPRINT = 'Sprint'
    TYPE_COURSE = 'Course'

    PRODUCT_CHOICES = (
        (TYPE_FREE, 'Бесплатный'),
        (TYPE_SPRINT, 'Спринт'),
        (TYPE_COURSE, 'Курс'),
    )
    slug = models.SlugField(unique=True, verbose_name='slug')
    title = models.CharField(max_length=255, verbose_name='Заголовок продука')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, 
                                 related_name='products')
    teaser = models.TextField(verbose_name='Тизер продукта', blank=True)
    description = models.TextField(max_length=1000, verbose_name='Описание продукта')
    product_type = models.CharField(max_length=100, choices=PRODUCT_CHOICES,
                                    default='Course', verbose_name='Тип продукта')
    timestamp = models.DateField(auto_now_add=True, verbose_name='Дата создания курса')
    speakers = models.ManyToManyField(Speakers, verbose_name='Спикеры')
    image = models.ImageField(verbose_name='Изображение')
    draft = models.BooleanField(default=True, verbose_name='Черновик')
    documents = models.ManyToManyField(Documents, verbose_name='Дополнительные документы', blank=True)
    lessons = models.ManyToManyField(Lessons, verbose_name='Уроки',
                                     related_name='related_product', blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    active_time = models.DurationField(default=timedelta(days=30), blank=True, verbose_name='Продолжительность')
    comments = GenericRelation('comments')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_comment(self):
        return self.comments.filter(parent__isnull=True)


    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class HomeWork(models.Model):
    """Домашние задания"""
    title = models.CharField(max_length=150, verbose_name='Заголовок домашнего задания')
    description = models.TextField(max_length=500, verbose_name='Описание домашнего задания')
    document = models.FileField(verbose_name='Прикрепленный файл')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class Comments(models.Model):
    """Коментарии"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField("Текст комментария", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.CASCADE,
        blank=True, null=True, related_name="children"
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name='Id объекта')
    timestamp = models.DateField(auto_now_add=True, verbose_name='Дата создания комментария')
    is_child = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_parent(self):
        if not self.parent:
            return ""
        return self.parent

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"




