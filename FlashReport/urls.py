# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stats/', views.stats_view, name='Stats'),
    path('reports/', views.reports_view, name='reports'),
]