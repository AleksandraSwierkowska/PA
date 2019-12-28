from django.db import models
from django.utils import timezone


class Acid(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=8)
    V = models.FloatField(default=0)
    mol_H = models.FloatField('nH', default=1.0)
    Cm = models.IntegerField('Cm')
    when_added = models.DateTimeField(default=timezone.now())


class Hydroxide(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=8)
    V = models.FloatField(default=0)
    mol_OH = models.FloatField('nOH', default=1)
    Cm = models.IntegerField('Cm')
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
    pHs = models.CharField(max_length=255, default='', blank=True)
    Vs = models.CharField(max_length=255, default='', blank=True)
    Plot = models.ImageField(upload_to='media/', default=None)
