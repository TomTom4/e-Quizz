# coding: utf8

from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Seance(models.Model):
    #titre = models.CharField(max_length=100)
    #contenu = models.TextField(null=True)
    #date = models.DateTimeField(auto_now_add=True, auto_now=False, 
    #                            verbose_name="Date de parution")
    id = models.AutoField(primary_key=True)
    code = models.IntegerField() #check for lengthpython

    
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.id
