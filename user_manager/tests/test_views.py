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
        self.assertEqual(response.data,serializer.data)
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
            injury = "Concussion.",
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
