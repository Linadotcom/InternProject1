# models.py
from django.db import models

class Zone(models.Model):
    """Represents a specific physical zone or location in the data center."""
    LEVEL_CHOICES = [
        ('L1', 'Level 1'),
        ('L2', 'Level 2'),
        ('L3', 'Level 3'),
        ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class IncidentType(models.Model):
    """Represents the type/category of an incident."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Incident(models.Model):
    """Represents a reported incident in the data center."""
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 200, null=False)
    incident_type = models.ForeignKey(IncidentType, on_delete=models.SET_NULL, null=True, related_name='incidents')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='Low')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='incidents')
    description = models.TextField()
    reporter_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Incident {self.id} - {self.severity} - {self.status}"


class IncidentImage(models.Model):
    """Stores images related to a specific incident."""
    id = models.AutoField(primary_key=True)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='images')
    media = models.ImageField(upload_to = 'statics/incident_image', blank = True, null = True)

    def __str__(self):
        if self.incident and self.incident.id:
            return f"Image for Incident #{self.incident.id}"
        return "Image for unsaved Incident"