from django.contrib import admin
from .models import AdminId, AdminLoggedIn

# Register your models here.
admin.site.register(AdminId)
admin.site.register(AdminLoggedIn)