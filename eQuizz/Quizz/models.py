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
    code = models.IntegerField(unique=True) #check for lengthpython

    
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.id

class Answers(models.Model):
    answer_id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey('Question')
    answer = models.TextField(null=True)

    def __str__(self):
        return self.answer_id
		
class Question(models.Model):
	quesion_id = models.AutoField(primary_key=True)
	code=models.ForeignKey('Seance')
	
	def __str__(self):
		return self.question_id

