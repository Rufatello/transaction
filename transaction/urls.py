from django.urls import path
from .views import UserStatsAPIView
app_name = 'transaction'
urlpatterns = [
    path('users/<int:user_id>/stats/', UserStatsAPIView.as_view(), name='user-stats'),
]