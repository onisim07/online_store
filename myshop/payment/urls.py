from django.urls import path
from . import views


app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('completed/', views.pyment_completed, name='completed'),
    path('ccanceled/', views.pyment_canceled, name='canceled'),
]