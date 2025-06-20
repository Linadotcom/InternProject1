# admin.py
from django.contrib import admin
from .models import IncidentReport

@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'incident_type', 'severity', 'reporter_name', 'status', 'created_at']
    list_filter = ['incident_type', 'severity', 'status', 'created_at']
    search_fields = ['reporter_name', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at']
