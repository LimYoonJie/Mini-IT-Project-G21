from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from marketplace import views as marketplace_views
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.svg", permanent=False)),
    path("", include("marketplace.urls")),
    path('admin-register/', marketplace_views.quick_admin_register, name='quick_admin_register'),
] + static(settings.STATIC_URL, document_root=str(settings.STATICFILES_DIRS[0])) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
