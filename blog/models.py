from django.db import models

# Create your models here.

class MyModel(models.Model):
    myfile = models.FileField(null=True)