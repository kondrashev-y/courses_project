from django import forms

from .models import Comments


class CommentForm(forms.ModelForm):
    """Форма коммнтариев"""

    class Meta:
        model = Comments
        fields = ('text',)
