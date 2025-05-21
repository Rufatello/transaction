from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

def time_validation(value):  # Renamed for clarity
    """Validates a datetime value, ensuring it's in the past and timezone-aware."""
    if not value:
        return value

    if isinstance(value, datetime.date):  # Handle date objects
        value = datetime.datetime.combine(value, datetime.time.min)  # Convert to datetime

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
    """Проверяет корректность диапазона дат"""
    if not isinstance(from_date, datetime.date) or not isinstance(to_date, datetime.date):
        raise TypeError("from_date and to_date must be datetime.date objects")

    if from_date > to_date:
        raise ValidationError('Конечная дата не может быть раньше начальной')
    return
