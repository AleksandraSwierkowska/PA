from django.db import models
from django.utils import timezone


# Create your models here.

class Acid(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=8)
    V = models.FloatField(default=0)
    mol_H = models.IntegerField('[H+]')
    all_mol = models.IntegerField('Cm')
    when_added = models.DateTimeField(default=timezone.now())


class Hydroxide(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=8)
    V = models.FloatField(default=0)
    mol_OH = models.IntegerField('[OH-]')
    all_mol = models.IntegerField('Cm')
    when_added = models.DateTimeField(default=timezone.now())


class Container(models.Model):
    def __str__(self):
        return "Container nr " + str(self.nr)

    nr = models.PositiveIntegerField(default=1)
    V = models.FloatField(default=0.0)
    pH = models.PositiveSmallIntegerField(default=7)
    aim_pH = models.PositiveSmallIntegerField(default=7)
    hydroxides = models.ManyToManyField(Hydroxide, default=None)
    acids = models.ManyToManyField(Acid, default=None)
    CmH = models.FloatField(default=0.0000001)
