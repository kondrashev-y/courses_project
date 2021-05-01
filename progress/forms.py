from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Progress, CheckHomeworks, CheckLessons


class ProgressForms(forms.ModelForm):
    """Форма прогресса по продукту"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Progress
        fields = '__all__'


class CheckLessonsForms(forms.ModelForm):
    """Форма прогресса по продукту"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CheckLessons
        fields = '__all__'


class CheckHomeworkForms(forms.ModelForm):
    """Форма прогресса по продукту"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CheckHomeworks
        fields = '__all__'
