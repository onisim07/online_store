from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    '''Модель для хранения купонов'''
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    # Применяемый уровень скидки:
    discount = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)],
        help_text='Процентное значение (0 до 100)')
    active = models.BooleanField()

    def __str__(self):
        return self.code
