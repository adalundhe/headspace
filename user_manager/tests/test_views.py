import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User
from ..serializers import UserSerializer
from datetime import datetime, timedelta

#initialize APIClient application

client = Client()

class GetAllUsersTest(TestCase):
    """ Test module for GET all users API """

    def setUp(self):
        User.objects.create(
            firstname = "John",
            lastname = "Cena",
            injury = "Broken back, punctured lung.",
            incidents = 1,
            incidentdate = datetime.now(),
            recoverydate = datetime.now() + timedelta(days=90)
        )
        User.objects.create(
            firstname = "George",
            lastname = "Clooney",
            injury = "Concussion.",
            incidents = 1,
            incidentdate = datetime.now(),
            recoverydate = datetime.now() + timedelta(days=30)
        )

    def test_get_all_users(self):
        response = client.get(reverse('get_post_users'))

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSingleUserTest(TestCase):
    """ Test module for GET single user API """

    def setUp(self):
        self.john_cena = User.objects.create(
            firstname = "John",
            lastname = "Cena",
            injury = "Broken back, punctured lung.",
            incidents = 1,
            incidentdate = datetime.now(),
            recoverydate = datetime.now() + timedelta(days=90)
        )
        self.george_clooney = User.objects.create(
            firstname = "George",
            lastname = "Clooney",
            injury = "Minor Concussion",
            incidents = 1,
            incidentdate = datetime.now(),
            recoverydate = datetime.now() + timedelta(days=30)
        )


    def test_get_valid_single_user(self):
        response = client.get(
            reverse('get_delete_update_user', kwargs={'pk': self.john_cena.pk})
        )
        user = User.objects.get(pk=self.john_cena.pk)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_invalid_single_user(self):
        response = client.get(
            reverse('get_delete_update_user', kwargs={'pk': 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewUserTest(TestCase):
    """ Test module for inserting a new user API """

    def setUp(self):
        incidentdate = datetime.now()
        recoverydate = incidentdate + timedelta(days=120)

        self.valid_payload = {
            'firstname': 'Toby',
            'lastname': 'MacGuire',
            'injury': 'Major Concussion',
            'incidents': 2,
            'incidentdate': incidentdate.strftime('%b %d %Y %I:%M%p'),
            'recoverydate': recoverydate.strftime('%b %d %Y %I:%M%p')
        }

        self.invalid_payload = {
            'firstname': '',
            'lastname': 'Spears',
            'incidents': 1,
            'injury': 'Minor Concussion',
            'incidentdate': incidentdate.strftime('%b %d %Y %I:%M%p'),
        }

    def convert_date(self, date):
        if isinstance(date, datetime):
            return date.__str__()

    def test_create_valid_user(self):
        response = client.post(
            reverse('get_post_users'),
            data = json.dumps(self.valid_payload, default=self.convert_date),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = client.post(
            reverse('get_post_users'),
            data = json.dumps(self.invalid_payload, default=self.convert_date),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleUserTest(TestCase):
    """ Test module for updating single user API """

    def setUp(self):
        incidentdate = datetime.now()
        recoverydate = incidentdate + timedelta(days=90)

        self.john_cena = User.objects.create(
            firstname = "John",
            lastname = "Cena",
            injury = "Broken back, punctured lung.",
            incidents = 1,
            incidentdate = incidentdate,
            recoverydate = recoverydate
        )
        self.valid_payload = {
            'firstname': 'John',
            'lastname': 'Cena',
            'injury': 'Broken back, punctured lung.',
            'incidents': 2,
            'incidentdate': incidentdate.strftime('%b %d %Y %I:%M%p'),
            'recoverydate': recoverydate.strftime('%b %d %Y %I:%M%p')
        }
        self.invalid_payload = {
            'firstname': '',
            'lastname': 'Cena',
            'injury': 'Broken back, punctured lung.',
            'incidents': 2,
            'incidentdate': incidentdate.strftime('%b %d %Y %I:%M%p'),
            'recoverydate': recoverydate.strftime('%b %d %Y %I:%M%p')
        }

    def convert_date(self, date):
        if isinstance(date, datetime):
            return date.__str__()

    def test_valid_update_user(self):
        response = client.put(
            reverse('get_delete_update_user', kwargs={'pk': self.john_cena.pk}),
            data = json.dumps(self.valid_payload, default=self.convert_date),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_user(self):
        response = client.put(
            reverse('get_delete_update_user', kwargs={'pk': self.john_cena.pk}),
            data = json.dumps(self.invalid_payload, default=self.convert_date),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleUserTest(TestCase):
    """ Test module for deleting an existing user record API """

    def setUp(self):
        incidentdate = datetime.now()
        recoverydate = incidentdate + timedelta(days=90)

        self.john_cena = User.objects.create(
            firstname = "John",
            lastname = "Cena",
            injury = "Broken back, punctured lung.",
            incidents = 1,
            incidentdate = incidentdate,
            recoverydate = recoverydate
        )

    def test_valid_delete_user(self):
        response = client.delete(
            reverse('get_delete_update_user', kwargs={'pk': self.john_cena.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_user(self):
        response = client.delete(
            reverse('get_delete_update_user', kwargs={'pk': 909})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
