from django.contrib.admin.apps import AdminConfig

class SecureSimpleUIConfig(AdminConfig):
    default_site = 'django.contrib.admin.sites.AdminSite'
