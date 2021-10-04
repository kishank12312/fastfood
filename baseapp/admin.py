from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from leaflet.admin import LeafletGeoAdmin
from .models import *
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(LeafletGeoAdmin):
    list_display = ('user', 'CustomerName', 'Address', 'DateOfBirth')

admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Orders)

