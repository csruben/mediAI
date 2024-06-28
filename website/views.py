from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from .forms import BloodPressureForm
from .forms import SymptomsForm
from .models import Symptom, SymptomSeverity, Disease
import joblib
import numpy as np
import traceback
import pandas as pd
import sys

def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def diagnose(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("Request received")  # Log
        form = SymptomsForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            symptoms = form.cleaned_data['symptoms']
            symptom_names = [symptom.name for symptom in symptoms]

            print(f"Symptoms: {symptom_names}")  # Log
            
            try:
                # Obtaining diagnosis from the model using the symptom vector
                diagnosis_result = predd(model, *symptom_names)
                print(f"Diagnosis: {diagnosis_result}")
                return JsonResponse(diagnosis_result)
            except Exception as e:
                print(f"Error during prediction: {e}")
                traceback.print_exc()
                return JsonResponse({'disease_name': 'Error', 'disease_description': 'An error occurred during the prediction. Please try again.'})
        else:
            print("Form is invalid")  # Log
            return JsonResponse({'disease_name': 'Error', 'disease_description': 'The data entered is not valid. Please check and try again.'})
    else:
        print("Non-AJAX request or not POST")  # Log
        form = SymptomsForm()
        symptoms = Symptom.objects.all()
        return render(request, 'diagnose.html', {'form': form, 'symptoms': symptoms})

def blood_pressure(request):
    return render(request, 'blood_pressure.html', {})

def evaluate_bp(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = BloodPressureForm(request.POST)
        if form.is_valid():
            systolic = form.cleaned_data['systolic']
            diastolic = form.cleaned_data['diastolic']
            pulse = form.cleaned_data['pulse']

            # Evaluation logic
            if systolic < 90 or diastolic < 60:
                bp_evaluation = "Blood pressure is too low!"
                bp_is_normal = False
            elif 90 <= systolic < 121 and 60 <= diastolic < 81:
                bp_evaluation = "Blood pressure is normal."
                bp_is_normal = True
            elif 120 <= systolic < 140 or 80 <= diastolic < 90:
                bp_evaluation = "Blood pressure is slightly elevated."
                bp_is_normal = False
            else:
                bp_evaluation = "Blood pressure is too high!"
                bp_is_normal = False

            if 60 <= pulse <= 100:
                pulse_evaluation = "Pulse is normal."
                pulse_is_normal = True
            else:
                pulse_evaluation = "Pulse is abnormal."
                pulse_is_normal = False

            return JsonResponse({
                'bp_evaluation': bp_evaluation,
                'pulse_evaluation': pulse_evaluation,
                'bp_is_normal': bp_is_normal,
                'pulse_is_normal': pulse_is_normal
            })
        else:
            return JsonResponse({
                'bp_evaluation': 'The data entered is not valid. Please check and try again.',
                'pulse_evaluation': '',
                'bp_is_normal': False,
                'pulse_is_normal': False
            })

    return render(request, 'evaluate_bp.html', {'form': BloodPressureForm()})

# Set the default encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Load the model globally
try:
    model = joblib.load('website/ml_models/random_forest_model.pkl')
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def predd(model, *symptoms):
    try:
        severity_map = {symptom.symptom: symptom.weight for symptom in SymptomSeverity.objects.all()}
        symptom_vector = []

        for symptom in symptoms:
            if symptom in severity_map:
                symptom_vector.append(severity_map[symptom])
            else:
                symptom_vector.append(0)  # Assuming 0 if the symptom is not found

        print(f"Symptom vector: {symptom_vector}")  # Log

        # Ensure the vector has 17 elements
        symptom_vector = symptom_vector + [0] * (17 - len(symptom_vector))

        # Convert to numpy array
        symptom_vector = np.array(symptom_vector).reshape(1, -1)

        # Make prediction
        prediction = model.predict(symptom_vector)
        disease_name = prediction[0]
        print(f"Predicted disease name: {disease_name}")  # Log

        # Get disease description from the database
        try:
            disease = Disease.objects.get(name=disease_name)
            disease_display_name = disease.name
        except Disease.DoesNotExist:
            print(f"Disease not found in database: {disease_name}")  # Log
            disease_display_name = "Disease Name: Unavailable"

        return {
            "disease_name": disease_display_name
        }
    except Exception as e:
        print(f"Error during prediction: {e}")
        traceback.print_exc()
        return {
            "disease_name": "Error",
            "disease_description": "An error occurred during the prediction. Please try again."
        }
