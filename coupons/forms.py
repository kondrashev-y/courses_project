from django import forms
from .models import Coupon


class CouponApplyForm(forms.Form):
    code = forms.SlugField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))




    # class Meta:
    #     model = Coupon
    #     fields = (
    #         'code',
    #     )