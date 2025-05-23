from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('transaction/', include('transaction.urls', namespace='transaction'))
]+static(settings.MEDIA_URL, documetn_root=settings.MEDIA_ROOT)
