from django.contrib import admin
from measurement.models import Sensor, Measurement

admin.site.site_title = 'Электронный сервис "Умный дом"'
admin.site.site_header = 'Электронный сервис "Умный дом"'
admin.site.index_title = 'Администрирование'


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', ]
    list_filter = ['id', 'name', 'description', ]
    search_fields = ['name', 'description', ]


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['id', 'temperature', 'created_at', 'sensor', ]
    list_filter = ['id', 'temperature', 'created_at',  'sensor', ]
    search_fields = ['temperature', 'created_at', 'sensor', ]
