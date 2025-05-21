from datetime import datetime
import json
import logging
from django.core.management import BaseCommand
from django.utils import timezone
from django.core.exceptions import ValidationError
from transaction.models import Transaction, User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('static/transaction.json', encoding='UTF-8') as file:
            data = json.load(file)
            for i in data:
                transaction_id = i.get('id')

                if not transaction_id:
                    logger.warning('Пропущена транзакция, отсутствует id')
                    continue

                if Transaction.objects.filter(pk=transaction_id).exists():
                    logger.warning(f'Транзакция с id "{transaction_id}" уже существует в БД')
                    continue

                user_id = i['user']
                try:
                    user = User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    logger.warning(f'Пользователь с id: "{user_id}" не существует для транзакции {transaction_id}"')
                    continue

                timestamp_str = i['timestamp']
                try:
                    timestamp = timezone.make_aware(datetime.fromisoformat(timestamp_str))
                except ValueError:
                    logger.warning(f'Неверный формат даты и времени: "{timestamp_str}" для транзакции {transaction_id}"')
                    continue

                transaction = Transaction(
                    id=transaction_id,
                    user=user,
                    timestamp=timestamp,
                    currency=i['currency'],
                    amount=i['amount'],
                    description=i['description']
                )

                try:
                    transaction.save()
                except ValidationError as e:
                    logger.error(f'Ошибка валидации для транзакции {transaction_id}: {e.messages}')