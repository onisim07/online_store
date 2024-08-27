from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,    # Нечувствительное к регистру совпадение
                                        valid_from__lte=now,  # Меньше или ровно чем now
                                        valid_to__gte=now,    # Больше или равно чем now
                                        active=True)
            # ID купона сохраняется в сеансе пользователя:
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')

