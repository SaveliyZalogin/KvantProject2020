from django.contrib import admin
from .models import Processor

admin.site.register(Processor, admin.ModelAdmin)
