from django.contrib import admin
from .models import CustomUserModel , Task ,TaskProgress

# Register your models here.
admin.site.register(CustomUserModel)
admin.site.register(Task)
admin.site.register(TaskProgress)