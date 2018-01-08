from rest_framework import serializers
from .models import Incident

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ('description', 'painlevel', 'headaches', 'fainting', 'speechloss', 'occurence', 'duration', 'userid')
