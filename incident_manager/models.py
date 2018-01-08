from django.db import models

# Create your models here.
class Incident(models.Model):
    description = models.CharField(max_length=200)
    painlevel = models.IntegerField()
    headaches = models.BooleanField()
    fainting = models.BooleanField()
    speechloss = models.BooleanField()
    occurence = models.DateTimeField()
    duration = models.IntegerField()
    userid = models.IntegerField()

    def get_incident(self):
        return self

    def get_description(self):
        return self.description

    def __repr__(self):
        return "Incident ID: " + self.pk + ' is created.'
