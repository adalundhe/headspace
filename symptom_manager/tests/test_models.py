from django.test import TestCase
from datetime import datetime, timedelta
from ..models import Symptom

class SymptomTest(TestCase):
    """ Test module for Symptom model """

    def setUp(self):
        Symptom.objects.create(
            incidentid = 1,
            userid = 1,
            type_of = 'BRAIN INJURY',
            name = 'Moderate Dizziness',
            location = 'Head',
            description = 'Intermittent dizziness resulting in loss of balance or notable impedance of movement where consciousness is retained.',
            commonality = 6
        )

        Symptom.objects.create(
            incidentid = 1,
            userid = 1,
            type_of = 'BRAIN INJURY',
            name = 'Minor Loss of Vision',
            location = 'Head',
            description = 'Infrequent, temporary loss of vision. Usually accompanied by other brain trauma symptoms (nausea, headaches, dizziness).',
            commonality = 3
        )

    def test_symptom(self):
        symptom_dizziness = Symptom.objects.get(name='Moderate Dizziness')
        symptoms_visionloss = Symptom.objects.get(name='Minor Loss of Vision')
        self.assertEqual(
            symptom_dizziness.get_symptomname(), "Moderate Dizziness"
        )
        self.assertEqual(
            symptoms_visionloss.get_symptomname(), "Minor Loss of Vision"
        )
