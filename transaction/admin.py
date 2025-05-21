from django.contrib import admin
from transaction.models import User, Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'category',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email',)
