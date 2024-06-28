from django.db import models


class Symptom(models.Model):
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name
    
class Disease(models.Model):
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name
    

class SymptomSeverity(models.Model):
    symptom = models.CharField(max_length=100)
    weight = models.IntegerField()

    def __str__(self):
        return self.symptom
