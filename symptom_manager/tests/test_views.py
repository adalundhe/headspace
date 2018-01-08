import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Symptom
from ..serializers import SymptomSerializer

#initialize APIClient application

client = Client()

class GetAllSymptomsTest(TestCase):
    """ Test module for GET all symptoms API """

    def setUp(self):
        Symptom.objects.create(
            incidentid = 1,
            userid = 1,
            type_of = 'BRAIN INJURY',
            description = 'Intermittent dizziness resulting in loss of balance or notable impedance of movement where consciousness is retained.',
            commonality = 6,
            name = 'Moderate Dizziness',
            location = 'Head'
        )
        Symptom.objects.create(
            incidentid = 1,
            userid = 1,
            type_of = 'BRAIN INJURY',
            description = 'Infrequent, temporary loss of vision. Usually accompanied by other brain trauma symptoms (nausea, headaches, dizziness).',
            commonality = 3,
            name = 'Minor Loss of Vision',
            location = 'Head',
        )

    def test_get_all_symptoms(self):
        response = client.get(reverse('get_post_symptoms'))

        symptoms = Symptom.objects.all()
        serializer = SymptomSerializer(symptoms, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleSymptomTest(TestCase):
    """ Test module for GET single symptom API """

    def setUp(self):
        self.moderate_dizziness = Symptom.objects.create(
            incidentid = 1,
            userid = 1,
            type_of = 'BRAIN INJURY',
            description = 'Intermittent dizziness resulting in loss of balance or notable impedance of movement where consciousness is retained.',
            commonality = 6,
            name = 'Moderate Dizziness',
            location = 'Head',
        )

    def test_get_valid_single_symptom(self):
        response = client.get(
            reverse('get_delete_update_symptom', kwargs={'pk': self.moderate_dizziness.pk})
        )
        symptom = Symptom.objects.get(pk=self.moderate_dizziness.pk)
        serializer = SymptomSerializer(symptom)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_symptom(self):
        response = client.get(
            reverse('get_delete_update_symptom', kwargs={'pk': 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewSymptomTest(TestCase):
    """ Test module for inserting a new symptom API """

    def setUp(self):
        self.valid_payload = {
            'incidentid': 1,
            'userid': 1,
            'type_of': 'BRAIN INJURY',
            'description': 'Intermittent dizziness resulting in loss of balance or notable impedance of movement where consciousness is retained.',
            'commonality': 6,
            'name': 'Moderate Dizziness',
            'location': 'Head'
        }

        self.invalid_payload = {
            'incidentid': 1,
            'userid': 1,
            'type_of': '',
            'description': 'Intermittent dizziness resulting in loss of balance or notable impedance of movement where consciousness is retained.',
            'commonality': 6,
            'name': 'Moderate Dizziness',
            'location': 'Head'
        }

    def test_create_valid_symptom(self):
        response = client.post(
            reverse('get_post_symptoms'),
            data = json.dumps(self.valid_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_symptom(self):
        response = client.post(
            reverse('get_post_symptoms'),
            data = json.dumps(self.invalid_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleSymptomTest(TestCase):
    """ Test module for updating single symptom API """

    def setUp(self):
        self.moderate_dizziness = Symptom.objects.create(
            incidentid = 1,
            userid = 1,
            type_of = 'BRAIN INJURY',
            description = 'Intermittent dizziness resulting in loss of balance or notable impedance of movement where consciousness is retained.',
            commonality = 6,
            name = 'Moderate Dizziness',
            location = 'Head',
        )
        self.valid_payload = {
            'incidentid': 1,
            'userid': 1,
            'type_of': 'BRAIN INJURY',
            'description': 'Intermittent dizziness resulting in loss of balance or notable impedance of movement where consciousness is retained.',
            'commonality': 6,
            'name': 'Moderate Dizziness',
            'location': 'Head'
        }
        self.invalid_payload = {
            'incidentid': 1,
            'userid': 1,
            'type_of': '',
            'description': 'Intermittent dizziness resulting in loss of balance or notable impedance of movement where consciousness is retained.',
            'commonality': 6,
            'name': 'Moderate Dizziness',
            'location': 'Head'
        }

    def test_valid_update_symptom(self):
        response = client.put(
            reverse('get_delete_update_symptom', kwargs={'pk': self.moderate_dizziness.pk}),
            data = json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_symptom(self):
        response = client.put(
            reverse('get_delete_update_symptom', kwargs={'pk': self.moderate_dizziness.pk}),
            data = json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleSymptomTest(TestCase):
    """ Test module for deleting an existing symptom record API """

    def setUp(self):
        self.moderate_dizziness = Symptom.objects.create(
            incidentid = 1,
            userid = 1,
            type_of = 'BRAIN INJURY',
            description = 'Intermittent dizziness resulting in loss of balance or notable impedance of movement where consciousness is retained.',
            commonality = 6,
            name = 'Moderate Dizziness',
            location = 'Head'
        )

    def test_valid_delete_symptom(self):
        response = client.delete(
            reverse('get_delete_update_symptom', kwargs={'pk': self.moderate_dizziness.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_symptom(self):
        response = client.delete(
            reverse('get_delete_update_symptom', kwargs={'pk': 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetSymptomsByUserAndIncident(TestCase):
    """ Test module for getting symptoms by userid and incidentid API """

    def setUp(self):
        self.moderate_dizziness = Symptom.objects.create(
            incidentid = 1,
            userid = 1,
            type_of = 'BRAIN INJURY',
            description = 'Intermittent dizziness resulting in loss of balance or notable impedance of movement where consciousness is retained.',
            commonality = 6,
            name = 'Moderate Dizziness',
            location = 'Head'
        )

    def test_get_valid_symptoms(self):
        response = client.get(
            reverse('get_symptoms_by_user_and_incident', kwargs={'userid': self.moderate_dizziness.userid, 'incidentid': self.moderate_dizziness.incidentid})
        )
        symptoms = Symptom.objects.filter(userid=self.moderate_dizziness.userid, incidentid=self.moderate_dizziness.incidentid)
        serializer = SymptomSerializer(symptoms, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_userid_symptoms(self):
        response = client.get(
            reverse('get_symptoms_by_user_and_incident', kwargs={'userid': 30, 'incidentid': self.moderate_dizziness.incidentid})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_invalid_incidentid_symptoms(self):
        response = client.get(
            reverse('get_symptoms_by_user_and_incident', kwargs={'userid': self.moderate_dizziness.userid, 'incidentid': 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetSymptomsByUser(TestCase):
    """ Test module for getting symptoms by userid API """

    def setUp(self):
        self.moderate_dizziness = Symptom.objects.create(
            incidentid = 1,
            userid = 1,
            type_of = 'BRAIN INJURY',
            description = 'Intermittent dizziness resulting in loss of balance or notable impedance of movement where consciousness is retained.',
            commonality = 6,
            name = 'Moderate Dizziness',
            location = 'Head'
        )

    def test_get_valid_symptoms_by_user(self):
        response = client.get(
            reverse('get_symptoms_by_user', kwargs={'userid': self.moderate_dizziness.userid})
        )
        symptoms = Symptom.objects.filter(userid=self.moderate_dizziness.userid)
        serializer = SymptomSerializer(symptoms, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_symptoms_by_user(self):
        response = client.get(
            reverse('get_symptoms_by_user', kwargs={'userid': 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
