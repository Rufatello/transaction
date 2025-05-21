from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime


def time_validation(value):
    if not value:
        return value
    if isinstance(value, datetime.date):
        value = datetime.datetime.combine(value, datetime.time.min)

    if timezone.is_naive(value):
        value = timezone.make_aware(value)

    if value > timezone.now():
        raise ValidationError('Дата не может быть больше нынешней')
    return value


def negative_amount(value):
    if value >= 0:
        raise ValidationError('Сумма не может быть положительной или равняться 0')
    return value


def date_validation(from_date, to_date):
    if not isinstance(from_date, datetime.date) or not isinstance(to_date, datetime.date):
        raise TypeError("from_date и to_date должны быть объектами datetime.date")

    if from_date > to_date:
        raise ValidationError('Конечная дата не может быть раньше начальной')
    return
