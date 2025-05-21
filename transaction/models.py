from datetime import timedelta
from _decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
import logging
from transaction.category_utils import auto_categorize
from transaction.validators import time_validation, negative_amount

logger = logging.getLogger(__name__)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    daily_limit = models.DecimalField(max_digits=10, decimal_places=2, default=5000)
    week_limit = models.DecimalField(max_digits=10, decimal_places=2, default=35000)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def check_daily_limit(self, amount, date=None):
        if date is None:
            date = timezone.now().date()

        total_spent = Transaction.objects.filter(
            user=self,
            timestamp__date=date,
            amount__lt=0
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal(0)

        return abs(total_spent) + abs(Decimal(str(amount))) > self.daily_limit

    def check_weekly_limit(self, amount, date=None):
        if date is None:
            date = timezone.now().date()

        start_date = date - timedelta(days=date.weekday())
        end_date = start_date + timedelta(days=6)

        total_spent = Transaction.objects.filter(
            user=self,
            timestamp__date__range=[start_date, end_date],
            amount__lt=0
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal(0)

        return abs(total_spent) + abs(Decimal(str(amount))) > self.week_limit


class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('TRANSPORT', 'Transport'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('UTILITIES', 'Utilities'),
        ('OTHER', 'Other'),
    ]
    id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.CharField(choices=CATEGORY_CHOICES, verbose_name='Категория', default='OTHER', blank=True,
                                null=True)
    timestamp = models.DateTimeField(verbose_name='Время', validators=[time_validation])
    currency = models.CharField(max_length=3, default='RUB')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[negative_amount])
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        trans_date = self.timestamp.date() if self.pk else timezone.now().date()
        if self.user.check_daily_limit(self.amount, trans_date):
            raise ValidationError("Превышен дневной лимит!")

        if self.user.check_weekly_limit(self.amount, trans_date):
            raise ValidationError("Превышен недельный лимит!")

        self.category = auto_categorize(self.description) if self.description else 'OTHER'

        self.full_clean()
        super().save(*args, **kwargs)
