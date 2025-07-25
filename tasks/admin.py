from django.contrib import admin
from tasks.models import Event,Category

# Register your models here.
admin.site.register(Event)
# admin.site.register(Particpant)
admin.site.register(Category)