# coding: utf8
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from Quizz.forms import *
import random
from Quizz.models import *

# Create your views here.
#    myfield = models.CharField(validators=[RegexValidator(regex='^.{4}$', message='Length has to be 4', code='nomatch')])

def home(request):

	#if request.method == 'POST':
		#form = AccessQuizz(request.POST['code'])
		#if form.is_valid():

			#room=form.cleaned_data['code'];
	#code=0 Pourquoi ne passe pas dans les variables locales?
	return render(request, 'Quizz/home.html', locals())


def ppl(request):

	# nom = request.POST['name']
	# request.session['name'] = nom
	# name=request.session['name']
	# code = request.code

	code = request.POST['code']
	try:
		sess=Seance.objects.all()
		sess=Seance.objects.filter(code=code)
		if not sess:
			addr='Quizz/error.html'
			error="Impossible de trouver cette salle"
		else:
			addr='Quizz/etudiant.html'
			request.session['code']=code

	except ValueError:
		addr='Quizz/error.html'
		error="Veuillez entrer un numéro de salle valide."

	return render(request, addr, locals())


def prof(request):
	#on ne passe jamais à l'interieur du try, on va direct a l'except
	try:
		if form.is_valid():
			code=request.code
			if request.POST['question_type']=="qcm":
				#creation de ask, une ligne de la table Question
				ask = Question(seance=code)
				if request.POST['commentaire'] !="votre commentaire ici":
					# ajout d'un commentaire à la question si il y a
					ask.commentaire = request.POST['commentaire']

			elif request.POST['question_type'] == "open_question":
				#creation de ask, une ligne de la table Question
				ask = Question(seance=code)
				if request.POST['commentaire'] !="votre commentaire ici":
					# ajout d'un commentaire à la question si il y a
					ask.commentaire = request.POST['commentaire']
				else:
					ask=Question(seance=code)
		ask.save()
		#elif request.POST['question_type'] == "close session":

	except AttributeError:
		code=0
		for index in range(0,9):
			numb=random.randint(1, 9)
			numb=numb*(10**index)
			code=code+numb

		session = Seance(code=code)
		session.save()
		request.session['code']=code #Sauvegarde dans la session pour un usage ultérieur

	# if code == 0:
		# for index in range(0,9):
			# numb=random.randint(1, 9)
			# numb=numb*(10**index)
			# code=code+numb

		# session = Seance(code=code)
		# session.save()
		# request.session['code']=code
	# elif request.POST['question_type']=="qcm":
		# ask=Question(code=code)

	return render(request, 'Quizz/prof.html', locals())

def error(request, errmsg):
	if errmsg==1:
		error="Impossible de trouver cette salle"
	return render(request, 'Quizz/error.html', locals())
