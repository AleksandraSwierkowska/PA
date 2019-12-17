from django.db import models


# Create your models here.

class Acid(models.Model):
    name = models.CharField(max_length=8)
    mol_H = models.IntegerField('[H+]')
    all_mol = models.IntegerField('Cm')


class Hydroxide(models.Model):
    name = models.CharField(max_length=8)
    mol_OH = models.IntegerField('[OH-]')
    all_mol = models.IntegerField('Cm')
