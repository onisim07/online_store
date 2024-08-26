from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@shared_task
def payment_completed(order_id):
    '''
    Задание по отправке уведомления по электронной почте
    при успешном оформлении заказа.
    '''
    order = Order.objects.get(id=order_id)
    # создать электронное письмо для выставления счета
    subject = f"Мой магазин - номер счета-фактуры. {order.id}"
    message = 'Пожалуйста, ознакомьтесь с приложенным счетом-фактурой за вашу недавнюю покупку.'
    email = EmailMessage(subject, message, [order.email])

    # Сгенерировать PDF:
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # Прикрепить PDF-файл:
    email.attach(f"order_{order.id}.pdf",
                 out.getvalue(),
                 'application/pdf')

    # Отправить электронное письмо:
    email.send()