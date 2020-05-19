from django.contrib import admin
from .models import Processor, GPU, Motherboard

admin.site.register(Processor, admin.ModelAdmin)
admin.site.register(GPU, admin.ModelAdmin)
admin.site.register(Motherboard, admin.ModelAdmin)