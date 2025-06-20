from django.urls import path, include
from . import views
# For media handeling
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
# BASE URLS
    path('', views.home, name='home'),
    path('stats/', views.stats_view, name='Stats'),
    path('reports/', views.reports_view, name='reports'), # Adds an incident

# URLS FOR INCIDENTS LIST
    path('incidents_list', views.incidents_list_view, name='incidents_list'),
    path('update_incident/<int:incident_id>/', views.incident_update, name='incident_update'),
    path('delete/<int:incident_id>/', views.incident_delete_view, name='incident_delete'),
    path('incident_details/<int:incident_id>/', views.incident_details_view, name='incident_details'),

# URLS FOR INCIDENTS TYPES 
    path('incident-types/', views.incident_type_list_view, name='incident_type_list'),
    path('add_type/', views.incident_type_create, name = 'incident_type_create'),
    path('update/<int:pk>/', views.incident_type_update, name='incident_type_update'),
    path('incident_type_delete/<int:pk>/', views.incident_type_delete, name='incident_type_delete'),

# URLS FOR ZONES LIST
    path('zones_list/', views.zones_list, name='zones_list'),
    path('add/', views.zones_create, name='zones_create'),
    path('edit/<int:pk>/', views.zones_update, name='zones_update'),
    path('zone/disable/<int:zone_id>/', views.zones_disable, name='zone_disable'),
    path('zone/activate/<int:zone_id>/', views.zones_activate, name='zone_activate'),
]

# FOR MEDIA HANDELING
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)