from rest_framework import serializers
from transaction.models import User, Transaction
from transaction.validators import date_validation, time_validation


class UserSerializers(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    from_date = serializers.DateField(required=True, write_only=True)
    to_date = serializers.DateField(required=True, write_only=True)
    total_spend = serializers.DecimalField(max_digits=10, read_only=True, decimal_places=2)
    daily_average = serializers.DecimalField(max_digits=10, read_only=True, decimal_places=2)
    by_category = serializers.DictField(child=serializers.DecimalField(max_digits=12, decimal_places=2),
                                        read_only=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'from_date',
            'to_date',
            'total_spend',
            'daily_average',
            'by_category'
        ]

    def validate(self, data):
        date_validation(data['from_date'], data['to_date'])
        time_validation(data['to_date'])
        return data

    def get_calculate(self, user_id, from_date, to_date):
        transaction = Transaction.objects.filter(user_id=user_id)
        total_spend = 0
        by_category = {}
        for i in transaction:
            transaction_date = i.timestamp.date()
            if not (from_date <= transaction_date <= to_date):
                continue
            if i.amount >= 0:
                continue
            amount = abs(i.amount)
            total_spend += amount
            if i.category not in by_category:
                by_category[i.category] = 0
            by_category[i.category] += amount

        days = (to_date - from_date).days + 1
        daily_average = total_spend / days if days > 0 else 0
        return {
            'total_spent': total_spend,
            'by_category': by_category,
            'daily_average': daily_average
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        stats = self.get_calculate(
            user_id=self.validated_data['user_id'],
            from_date=self.validated_data['from_date'],
            to_date=self.validated_data['to_date']
        )
        data.update(stats)
        return data
