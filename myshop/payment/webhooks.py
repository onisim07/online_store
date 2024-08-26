import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .tasks import payment_completed


@csrf_exempt  # <-- Предотвращает выполнение CSRF
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        # Недопустимая полезная нагрузка:
        return HttpResponse(status=400)
    except stripe.error.SignatureVarificationError as e:
        # Недопустимая подпись:
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':   # <-- Событие успешного завершения платежа
        session = event.data.object  # <-- Извлекается сеансовый объект
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=400)
            # Пометить заказ как оплаченный:
            order.paid = True
            # Сохранить ID платежа Stripe:
            order.stripe_id = session.payment_intent
            order.save()
            # Запустить асинхронное задание:
            payment_completed.delay(order.id)

    return HttpResponse(status=200)