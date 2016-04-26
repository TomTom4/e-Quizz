# coding: utf8

from __future__ import unicode_literals

from django.db import models

"""Une séance représente une séance de cours.
Elle est crée par l'enseignant.
Elle contient plusieurs questions."""
class Seance(models.Model):
    #titre = models.CharField(max_length=100)
    #contenu = models.TextField(null=True)
    #date = models.DateTimeField(auto_now_add=True, auto_now=False,
    #                            verbose_name="Date de parution")
    id = models.AutoField(primary_key = True) # inutile, généré automatiquement
    code = models.IntegerField(unique = True) #check for lengthpython


    def __str__(self):
        return self.id

"""Une réponse correspond à un choix A, B, C ou D d'un élève à un question."""
class Answers(models.Model):
    question = models.ForeignKey('Question')
    answer = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.answer_id

"""Une question appartient à une séance. Elle va posséder plusieurs réponses."""
class Question(models.Model):
	seance = models.ForeignKey('Seance')
	commentaire = models.TextField(null = True)

	def __str__(self):
		return self.question_id
