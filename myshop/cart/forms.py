from django import forms
from django.utils.translation import gettext_lazy as _


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    # Позволяет выбирать кол-во от 1 до 20:
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int,
                                      label=_('Quantity'))
    # Должно ли существующее кол-во быть переопределено данным кол-вом:
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)