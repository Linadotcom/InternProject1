# admin.py
from django.contrib import admin
from .models import Incident, IncidentType, Zone, IncidentImage

@admin.register(Incident)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'incident_type', 'severity', 'status', 'created_at']
    list_filter = ['incident_type', 'severity', 'status', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']

@admin.register(IncidentType)
class IncidentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(IncidentImage)
class IncidentImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'incident']

