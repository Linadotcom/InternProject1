from django.shortcuts import render, get_object_or_404, redirect
from .models import Incident, Zone, IncidentType, IncidentImage
from .forms import Zoneform, Incidentform, IncidentImageform, IncidentTypeform
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required



                    ################## home page view ##################
@login_required
def home(request):
    return render(request, 'FlashReports/Base/home.html')

                   ################## Displays all the incidents ################
@login_required
def incidents_list_view(request):
    incidents = Incident.objects.prefetch_related('images').all()
    return render(request, 'FlashReports/incidents/incidents_list.html', {'incidents': incidents})

@login_required
def incident_details_view(request, incident_id):
    incident = get_object_or_404(Incident, id= incident_id)
    return render(request, 'FlashReports/incidents/incident_details.html', {'incident' : incident})


                    ################### Submits the form of an incident ###################
def reports_view(request):
    if request.method == 'POST':
        form = Incidentform(request.POST)
        image_form = IncidentImageform(request.POST, request.FILES) 

        if form.is_valid() and image_form.is_valid:

            incident = form.save(commit=False) 
            incident.status = 'pending'  # default status
            incident.save()

            for file in request.FILES.getlist('media'): # multiple media handeling 
                IncidentImage.objects.create(incident=incident, media=file)


            messages.success(request, f'Report #{incident.id} submitted successfully!')
            return redirect('reports')
        
        else:
            print("Form errors:", form.errors)
            print("Image form errors:", image_form.errors)
            messages.error(request, "Please correct the errors below.") 
    else:
        form = Incidentform()
        image_form = IncidentImageform()
    return render(request, 'FlashReports/Base/reports.html', {'form': form, 'image_form': image_form,})

                    ################## update an incident ####################
def incident_update(request, incident_id):
    incident = get_object_or_404(Incident, id=incident_id)
    if request.method == 'POST':
        form = Incidentform(request.POST,request.FILES, instance=incident)
        if form.is_valid():
            form.save()
            return redirect('incidents_list')
    else:
        form = Incidentform(instance=incident)
    return render(request, 'FlashReports/incidents/incident_update.html', {'form': form,
        'is_update': True,
        'incident': incident,})

                    ################# delete an incident from the list #################
def incident_delete_view(request, incident_id):
    incident = get_object_or_404(Incident, id=incident_id)
    if request.method == 'POST':
        incident.delete()
        messages.success(request, f'Report deleted successfully.')
        return redirect('incidents_list')
    return render(request, 'FlashReports/incidents/incident_confirm_delete.html', {'incident': incident})


                    ############### Display all zones ##################
@login_required
def zones_list(request):
    zones = Zone.objects.all()
    return render(request, 'FlashReports/zones/zones_list.html', {'zones' : zones})

                    #################  Create or add a new zone ##################
@login_required
def zones_create(request):
    if request.method == 'POST':
        form = Zoneform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('zones_list')
    else:
        form = Zoneform()
    return render(request, 'FlashReports/zones/zones_form.html', {'form': form})

                    ################## update a zone ####################
def zones_update(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    if request.method == 'POST':
        form = Zoneform(request.POST, instance=zone)
        if form.is_valid():
            form.save()
            return redirect('zones_list')
    else:
        form = Zoneform(instance=zone)
    return render(request, 'FlashReports/zones/zones_form.html', {'form': form})

                    ##################  soft-delete a zone ####################
def zones_disable(request, zone_id):
    zone = get_object_or_404(Zone,id = zone_id)
    if request.method == 'POST':
        zone.is_active = False
        zone.save()
        return redirect('zones_list')
    return render(request, 'FlashReports/zones/zones_confirm_delete.html', {'zone': zone})

def zones_activate(request, zone_id):
    zone = get_object_or_404(Zone, id=zone_id)
    zone.is_active = True
    zone.save()
    return redirect('zones_list')


                    ############### Display all incident types ################
@login_required
def incident_type_list_view(request):
    types = IncidentType.objects.all()
    return render(request, 'FlashReports/incident_type/incident_type_list.html', {'types': types})

                        ############### Add a new type ################
def incident_type_create(request):
    if request.method == 'POST':
        form = IncidentTypeform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('incident_type_list')
    else:
        form = IncidentTypeform()
    return render(request, 'FlashReports/incident_type/incident_type_form.html', {'form': form})

                    ############### update an incident type ################
def incident_type_update(request, pk):
    type = get_object_or_404(IncidentType, pk=pk)
    if request.method == 'POST':
        form = IncidentTypeform(request.POST, instance=type)
        if form.is_valid():
            form.save()
            return redirect('incident_type_list')
    else:
        form = IncidentTypeform(instance=type)
    return render(request, 'FlashReports/incident_type/incident_type_form.html', {'form': form})

                    ############### Delete an incident type ################
def incident_type_delete(request, pk):
    type = get_object_or_404(IncidentType, pk=pk)
    if request.method == 'POST':
        type.delete()
        return redirect('incident_type_list')
    return render(request, 'FlashReports/incident_type/incident_type_confirm_delete.html', {'type' : type})


















    
    
def stats_view(request):
    current_month = timezone.now().replace(day=1)

    total_reports = Incident.objects.filter(created_at__gte=current_month).count()
    resolved_reports = Incident.objects.filter(
        created_at__gte=current_month,
        status='Resolved'
    ).count()
    critical_reports = Incident.objects.filter(
        created_at__gte=current_month,
        severity='Critical'
    ).count()

    resolved_with_time = Incident.objects.filter(
        resolved_at__isnull=False,
        created_at__gte=current_month
    )

    if resolved_with_time.exists():
        total_time = sum([
            (report.resolved_at - report.created_at).total_seconds() / 3600 # type: ignore
            for report in resolved_with_time
        ])
        avg_response_time = f"{total_time / resolved_with_time.count():.1f}h"
    else:
        avg_response_time = "--"

    recent_reports = Incident.objects.all().order_by('-created_at')[:10]

    context = {
        'total_reports': total_reports,
        'resolved_reports': resolved_reports,
        'critical_reports': critical_reports,
        'avg_response_time': avg_response_time,
        'recent_reports': recent_reports,
    }
    return render(request, 'FlashReport/Stats.html', context)

              ##################  Display list of all zones  ####################
