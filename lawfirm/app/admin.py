from django.contrib import admin

# Register your models here.


from .models import *
admin.site.register(Clients)
admin.site.register(courtAttendance)