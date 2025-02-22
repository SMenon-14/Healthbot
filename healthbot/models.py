# health/models.py

from django.db import models

class MedicalCondition(models.Model):
    name = models.CharField(max_length=255)  # For the name of the condition
    description = models.TextField(blank=True)  # Optional field for a description of the condition

    def __str__(self):
        return self.name  # This will return the name of the condition when you print the object
