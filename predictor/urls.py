from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home),
    path("banana/", include("banana.urls")),
    path("accounts/", include("accounts.urls")),
    path("about/", views.about),
    path("admin/", admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
