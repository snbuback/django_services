from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=255)


class Model(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand)


class Car(models.Model):
    model = models.ForeignKey(Model)
    year = models.PositiveIntegerField()
