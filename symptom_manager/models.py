from django.db import models

# Create your models here.
class Symptom(models.Model):
    incidentid = models.IntegerField()
    userid = models.IntegerField()
    type_of = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    commonality = models.IntegerField()
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def get_symptom(self):
        return self

    def get_symptomname(self):
        return self.name

    def __repr__(self):
        return self.name + ' is added.'
