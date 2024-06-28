from django.contrib import admin
from .models import SymptomSeverity, Symptom, Disease

admin.site.register(Disease)
admin.site.register(Symptom)
admin.site.register(SymptomSeverity)
