from django.contrib import admin
from .models import Processor, GPU

admin.site.register(Processor, admin.ModelAdmin)
admin.site.register(GPU, admin.ModelAdmin)
