from django.contrib import admin

# Register your models here.

from .models import CustomUser,Calendar

admin.site.register(CustomUser)
admin.site.register(Calendar)
