from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

from .models import Order


class OrderForms(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].label = 'Адрес покупателя'

    # order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), help_text='дд.мм.гггг')

    class Meta:
        model = Order
        fields = (
            'address',
        )


class LoginForm(forms.ModelForm):
    """Форма входа"""

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['password'].label = 'Пароль'

    def get_user(self):
        return self.user_cache

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Пользователь с логином {email} не найден.')
        user = User.objects.filter(email=email).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        self.user_cache = authenticate(self.request, email=email, password=password)
        return self.cleaned_data

    class Meta:

        model = User
        fields = ['email', 'password']


class RegistrationForm(forms.ModelForm):
    """Форма регистрации пользователя"""
    GENDER_CHOICE = (
        ('Male', 'Мужской'),
        ('Female', 'Женский')
    )

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    number = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    bio = forms.CharField(required=False)
    birth_date = forms.DateField(required=False)
    image = forms.ImageField(required=False)
    gender = forms.ChoiceField(required=False, choices=GENDER_CHOICE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Ваш email'
        # self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['number'].label = 'Номер телефона'
        self.fields['first_name'].label = 'Ваше имя'
        self.fields['last_name'].label = 'Ваша фамилия'
        self.fields['bio'].label = 'Ваш аккаунт instagram'
        self.fields['image'].label = 'Ваша аватарка'
        self.fields['gender'].label = 'Ваш пол'
        self.fields['birth_date'].label = 'Ваша дата рожденпия'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1 ]
        if domain in ['uk', 'net']:
            raise forms.ValidationError(f'Регистрация для домена "{domain}" не возможна')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Почтовый адрес {email} уже зарегестрирован')
        return email

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            'email', 'password', 'confirm_password', 'first_name', 'last_name', 'bio', 'number', 'birth_date', 'gender',
            'image'
        ]