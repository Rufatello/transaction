from django.core.management import BaseCommand

from transaction.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='1@mail.ru',
            first_name='Rufat',
            is_active=True,
            is_superuser=True,
            is_staff=True
        )
        user.set_password('12345')
        user.save()