from django.urls import path
from . import views
from . import webhooks


app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('completed/', views.pyment_completed, name='completed'),
    path('canceled/', views.pyment_canceled, name='canceled'),
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
]