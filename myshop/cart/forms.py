from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    # Позволяет выбирать кол-во от 1 до 20:
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    # Должно ли существующее кол-во быть переопределено данным кол-вом:
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)