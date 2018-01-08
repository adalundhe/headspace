from rest_framework import serializers
from .models import Symptom

class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ('incidentid', 'userid', 'type_of', 'description', 'commonality', 'name', 'location')
