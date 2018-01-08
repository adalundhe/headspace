from django.test import TestCase
from datetime import datetime, timedelta
from ..models import Incident
from datetime import datetime

class IncidentTest(TestCase):
    """ Test module for Incident model """

    def setUp(self):
        Incident.objects.create(
            description = "I had fainting and dizzy spells accompanied by strong headaches.",
            painlevel = 5,
            headaches = True,
            fainting = True,
            speechloss = False,
            duration = 5,
            occurence = datetime.now(),
            userid = 1
        )
        Incident.objects.create(
            description = "I had severe headaches for 15 minutes.",
            painlevel = 7,
            headaches = True,
            fainting = True,
            speechloss = False,
            duration = 30,
            occurence = datetime.now(),
            userid = 1
        )

    def test_incident(self):
        all_incidents = Incident.objects.all()
        self.assertEqual(
            all_incidents[0].get_description(), "I had fainting and dizzy spells accompanied by strong headaches."
        )
        self.assertEqual(
            all_incidents[1].get_description(), "I had severe headaches for 15 minutes."
        )
