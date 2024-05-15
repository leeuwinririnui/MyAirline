from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Airport, Flight, Plane

# CustomUser model
admin.site.register(CustomUser, UserAdmin)
# Airport model
admin.site.register(Airport)
# Flight model
admin.site.register(Flight)
# Plane model
admin.site.register(Plane)