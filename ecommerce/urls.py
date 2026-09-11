from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.svg", permanent=False)),
    path("", include("marketplace.urls")),
] + static(settings.STATIC_URL, document_root=str(settings.STATICFILES_DIRS[0]))
