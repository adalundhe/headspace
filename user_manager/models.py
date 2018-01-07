from django.db import models

# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    injury = models.CharField(max_length=200)
    incidents = models.IntegerField()
    incidentdate = models.DateTimeField()
    recoverydate = models.DateTimeField()

    def get_user(self):
        return self

    def get_username(self):
        return self.firstname+ ' '+ self.lastname

    def __repr__(self):
        return self.firstname+ ' '+ self.lastname + ' is added.'
