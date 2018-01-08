import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Incident
from ..serializers import IncidentSerializer
from datetime import datetime

client = Client()

class GetAllIncidentsTest(TestCase):
    """ Test module for GET all incidents API """

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

    def test_get_all_incidents(self):
        response = client.get(reverse('get_post_incidents'))

        incidents = Incident.objects.all()
        serializer = IncidentSerializer(incidents, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleIncidentTest(TestCase):
    """ Test module for GET single incident API """

    def setUp(self):
        self.first_incident = Incident.objects.create(
            description = "I had fainting and dizzy spells accompanied by strong headaches.",
            painlevel = 5,
            headaches = True,
            fainting = True,
            speechloss = False,
            duration = 5,
            occurence = datetime.now(),
            userid = 1
        )


    def test_get_valid_single_incident(self):
        response = client.get(
            reverse('get_delete_update_incident', kwargs={'pk': self.first_incident.pk})
        )
        incident  = Incident.objects.get(pk=self.first_incident.pk)
        serializer = IncidentSerializer(incident)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_symptom(self):
        response = client.get(
            reverse('get_delete_update_incident', kwargs={'pk': 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewIncidentTest(TestCase):
    """ Test module for inserting a new incident API """

    def setUp(self):
        occurence = datetime.now()

        self.valid_payload = {
            'description': "I had fainting and dizzy spells accompanied by strong headaches.",
            'painlevel': 5,
            'headaches': True,
            'fainting': True,
            'speechloss': False,
            'occurence': occurence.strftime('%b %d %Y %I:%M%p'),
            'duration': 5,
            'userid': 1
        }

        self.invalid_payload = {
            'description': "",
            'painlevel': 5,
            'headaches': True,
            'fainting': True,
            'speechloss': False,
            'duration': 5,
            'occurence': occurence.strftime('%b %d %Y %I:%M%p'),
            'userid': 1
        }

    def test_create_valid_incident(self):
        response = client.post(
            reverse('get_post_incidents'),
            data = json.dumps(self.valid_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_incident(self):
        response = client.post(
            reverse('get_post_incidents'),
            data = json.dumps(self.invalid_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleIncidentTest(TestCase):
    """ Test module for updating single incident API """

    def setUp(self):

        occurence = datetime.now()

        self.first_incident = Incident.objects.create(
            description = "I had fainting and dizzy spells accompanied by strong headaches.",
            painlevel = 5,
            headaches = True,
            fainting = True,
            speechloss = False,
            duration = 5,
            occurence =  occurence,
            userid = 1
        )

        self.valid_payload = {
            'description': "I had fainting and dizzy spells accompanied by strong headaches.",
            'painlevel': 5,
            'headaches': True,
            'fainting': True,
            'speechloss': False,
            'duration': 15,
            'occurence': occurence.strftime('%b %d %Y %I:%M%p'),
            'userid': 1
        }

        self.invalid_payload = {
            'description': "",
            'painlevel': 5,
            'headaches': True,
            'fainting': True,
            'speechloss': False,
            'duration': 5,
            'occurence': occurence.strftime('%b %d %Y %I:%M%p'),
            'userid': 1
        }

    def test_valid_update_incident(self):
        response = client.put(
            reverse('get_delete_update_incident', kwargs={'pk': self.first_incident.pk}),
            data = json.dumps(self.valid_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_incident(self):
        response = client.put(
            reverse('get_delete_update_incident', kwargs={'pk': self.first_incident.pk}),
            data = json.dumps(self.invalid_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleIncidentTest(TestCase):
    """ Test module for deleting an existing incident record API """

    def setUp(self):
        occurence = datetime.now()

        self.first_incident = Incident.objects.create(
            description = "I had fainting and dizzy spells accompanied by strong headaches.",
            painlevel = 5,
            headaches = True,
            fainting = True,
            speechloss = False,
            duration = 5,
            occurence =  occurence,
            userid = 1
        )

    def test_valid_delete_incident(self):
        response = client.delete(
            reverse('get_delete_update_incident', kwargs={'pk': self.first_incident.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_incident(self):
        response = client.delete(
            reverse('get_delete_update_incident', kwargs={'pk': 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetIncidentsByUser(TestCase):
    """ Test module for getting incidents by userid API """

    def setUp(self):
        occurence = datetime.now()

        self.first_incident = Incident.objects.create(
            description = "I had fainting and dizzy spells accompanied by strong headaches.",
            painlevel = 5,
            headaches = True,
            fainting = True,
            speechloss = False,
            duration = 5,
            occurence =  occurence,
            userid = 1
        )

        self.second_incident = Incident.objects.create(
            description = "I had severe headaches for 15 minutes.",
            painlevel = 7,
            headaches = True,
            fainting = True,
            speechloss = False,
            duration = 30,
            occurence = datetime.now(),
            userid = 1
        )

    def convert_date(self, date):
        if isinstance(date, datetime):
            return date.__str__()

    def test_get_valid_incidents_by_user(self):
        response = client.get(
            reverse('get_incidents_by_user', kwargs={'userid': self.first_incident.userid})
        )
        incidents = Incident.objects.filter(userid=self.first_incident.userid)
        serializer = IncidentSerializer(incidents, default=self.convert_date, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_incidents_by_user(self):
        response = client.get(
            reverse('get_incidents_by_user', kwargs={'userid': 30})
        )
        incidents = Incident.objects.filter(userid=self.first_incident.userid)
        serializer = IncidentSerializer(incidents, default=self.convert_date, many=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
