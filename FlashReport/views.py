# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import IncidentReport

def home(request):
    return render(request, 'home.html')

def reports_view(request):
    if request.method == 'POST':
        # Handle form submission
        incident_report = IncidentReport.objects.create(
            incident_type=request.POST['incident_type'],
            severity=request.POST['severity'],
            location=request.POST['location'],
            description=request.POST['description'],
            reporter_name=request.POST['reporter_name']
        )
        messages.success(request, f'Report FR-{incident_report.id} submitted successfully!')
        return redirect('reports')
    
    # Get recent reports for display
    recent_reports = IncidentReport.objects.all()[:10]
    
    context = {
        'recent_reports': recent_reports,
    }
    return render(request, 'reports.html', context)

def stats_view(request):
    # Calculate statistics
    current_month = timezone.now().replace(day=1)
    
    # Basic counts
    total_reports = IncidentReport.objects.filter(created_at__gte=current_month).count()
    resolved_reports = IncidentReport.objects.filter(
        created_at__gte=current_month,
        status='resolved'
    ).count()
    critical_reports = IncidentReport.objects.filter(
        created_at__gte=current_month,
        severity='critical'
    ).count()
    
    # Calculate average response time (in hours)
    resolved_with_time = IncidentReport.objects.filter(
        resolved_at__isnull=False,
        created_at__gte=current_month
    )
    
    if resolved_with_time.exists():
        total_time = sum([
            (report.resolved_at - report.created_at).total_seconds() / 3600
            for report in resolved_with_time
        ])
        avg_response_time = f"{total_time / resolved_with_time.count():.1f}h"
    else:
        avg_response_time = "--"
    
    # Get recent reports
    recent_reports = IncidentReport.objects.all()[:10]
    
    context = {
        'total_reports': total_reports,
        'resolved_reports': resolved_reports,
        'critical_reports': critical_reports,
        'avg_response_time': avg_response_time,
        'recent_reports': recent_reports,
    }
    return render(request, 'stats.html', context)
