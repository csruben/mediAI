from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from website.models import Symptom, Disease, SymptomSeverity


class DiagnoseViewTests(TestCase):

    def setUp(self):
        # Setting up test client
        self.client = Client()

    @patch('website.models.Symptom.objects.all')
    @patch('website.models.SymptomSeverity.objects.all')
    @patch('website.models.Disease.objects.get')
    def test_diagnose_valid_data(self, mock_get_disease, mock_all_severities, mock_all_symptoms):
        # Mocking the database responses
        mock_all_symptoms.return_value = [
            MagicMock(id=1, name="fever"),
            MagicMock(id=2, name="cough")
        ]
        mock_all_severities.return_value = [
            MagicMock(symptom="fever", weight=1),
            MagicMock(symptom="cough", weight=2)
        ]
        mock_get_disease.return_value = MagicMock(name="Common Cold", display_name="Common Cold")

        # Test valid symptom data for diagnose view
        response = self.client.post(
            reverse('diagnose'),
            {'symptoms': [1, 2]},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('disease_name', response.json())
        self.assertIn('disease_description', response.json())

    def test_diagnose_invalid_data(self):
        # Test invalid symptom data for diagnose view
        response = self.client.post(
            reverse('diagnose'),
            {'symptoms': []},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['disease_name'], 'Eroare')

    def test_diagnose_get_request(self):
        # Test GET request for diagnose view
        response = self.client.get(reverse('diagnose'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diagnose.html')


class BloodPressureViewTests(TestCase):

    def setUp(self):
        # Setting up test client
        self.client = Client()

    def test_evaluate_bp_valid_data(self):
        # Test valid blood pressure data for evaluate_bp view
        form_data = {'systolic': 120, 'diastolic': 80, 'pulse': 70}
        response = self.client.post(
            reverse('evaluate_bp'),
            form_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('bp_evaluation', response.json())
        self.assertIn('pulse_evaluation', response.json())
        self.assertTrue(response.json()['bp_is_normal'])

    def test_evaluate_bp_invalid_data(self):
        # Test invalid blood pressure data for evaluate_bp view
        form_data = {'systolic': 'invalid', 'diastolic': 'invalid', 'pulse': 'invalid'}
        response = self.client.post(
            reverse('evaluate_bp'),
            form_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['bp_evaluation'], 'Datele introduse nu sunt valide. Vă rugăm să verificați și să încercați din nou.')
        self.assertFalse(response.json()['bp_is_normal'])

    def test_evaluate_bp_get_request(self):
        # Test GET request for evaluate_bp view
        response = self.client.get(reverse('evaluate_bp'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'evaluate_bp.html')
