from django import forms

from .models import Symptom

class BloodPressureForm(forms.Form):
    systolic = forms.IntegerField(label='Tensiunea Arterială Mare (Systolic)', min_value=0)
    diastolic = forms.IntegerField(label='Tensiunea Arterială Mică (Diastolic)', min_value=0)
    pulse = forms.IntegerField(label='Pulsul', min_value=0)

class SymptomsForm(forms.Form):
    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True
    )
