from django.test import TestCase
from datetime import datetime, timedelta
from ..models import User

class UserTest(TestCase):
    """ Test module for User model """

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

    def test_user(self):
        user_john = User.objects.get(firstname="John")
        user_george = User.objects.get(firstname="George")
        self.assertEqual(
            user_john.get_username(), "John Cena"
        )
        self.assertEqual(
            user_george.get_username(), "George Clooney"
        )
