from django.urls import path
from . import views
from . import webhooks
from django.utils.translation import gettext_lazy as _


app_name = 'payment'

urlpatterns = [
    path(_('process/'), views.payment_process, name='process'),
    path(_('completed/'), views.pyment_completed, name='completed'),
    path(_('canceled/'), views.pyment_canceled, name='canceled'),
]