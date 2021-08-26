from django.contrib import admin

# Register your models here.
from .models import Availability
from .models import Schedule

admin.site.register(Availability)
admin.site.register(Schedule)