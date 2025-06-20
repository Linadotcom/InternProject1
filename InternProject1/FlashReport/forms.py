from django import forms
from .models import Zone, IncidentType, Incident, IncidentImage

class Zoneform(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'level']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.TextInput(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['level'].widget.attrs.update({'class': 'form-select'})

class IncidentTypeform(forms.ModelForm):
    class Meta:
        model = IncidentType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

class Incidentform(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['title', 'incident_type', 'severity', 'zone', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.fields['zone'].queryset = Zone.objects.filter(is_active=True) # Show only active zones in the dropdown
        self.fields['incident_type'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['zone'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['severity'].widget.attrs.update({
            'class': 'form-select'
        })

        widget = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'incident_type': forms.TextInput(attrs={'class': 'form-select'}),
            'severity': forms.TextInput(attrs={'class': 'form-select'}),
            'zone':  forms.TextInput(attrs={'class': 'form-select'}),
            'description':  forms.TextInput(attrs={'class': 'form-control'}),
            
        }
        
class IncidentImageform(forms.ModelForm):
    class Meta:
        model = IncidentImage
        fields = ['media']