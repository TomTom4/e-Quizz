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
	#							verbose_name="Date de parution")
	id = models.AutoField(primary_key = True) # inutile, généré automatiquement
	code = models.IntegerField(unique = True) #check for lengthpython
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.id

"""Une réponse correspond à un choix A, B, C ou D d'un élève à un question."""
class Reponse_QCM(models.Model):
	question = models.ForeignKey('Question')
	valeur = models.PositiveSmallIntegerField() # 0 => A | 1 => B | 2 => C...
	id_etudiant = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.answer_id

class Reponse_OPEN(models.Model):
	question = models.ForeignKey('Question')
	text = models.CharField(max_length=100)
	id_etudiant = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.answer_id

"""Une question appartient à une séance. Elle va posséder plusieurs réponses."""
class Question(models.Model):
	QCM = 'QCM'
	OPEN = 'OPE'
	QUESTION_TYPE = (
		(QCM, 'QCM'),
		(OPEN, 'Open'),
	)
	seance = models.ForeignKey('Seance')
	numero = models.PositiveSmallIntegerField()
	commentaire = models.TextField(null = True)
	question_type = models.CharField(max_length=3, choices=QUESTION_TYPE, default=QCM)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.id)

class Lost(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	id_etudiant = models.IntegerField()
	seance = models.ForeignKey('seance')
	def __str__(self):
		return str(self.id)
