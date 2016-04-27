# coding: utf8
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
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


def etudiant(request, code):

	# nom = request.POST['name']
	# request.session['name'] = nom
	# name=request.session['name']
	# code = request.code

	try:
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

def etudiant_refresh(request, code):
	try:
		seance = Seance.objects.filter(code=code)
	except ValueError:
		return error_json(ERR_CODE_INVALIDE)
	if not seance:
		return error_json(ERR_SALLE_INTROUVABLE)

	question = Question.objects.filter(seance=seance).latest('id')
	if not question:
		return JsonResponse({})

	return JsonResponse({
		'id':question.id,
		'question_type':question.question_type,
		'numero':question.numero,
	})

def etudiant_post(request):
	if 'question_type' in request.POST:
		if request.POST['question_type']=="qcm":
			question = Question.objects.get(id=request.POST['id'])
			reponse = Reponse_QCM(question=question)
			valeur = request.POST['valeur']
			reponse.valeur = valeur
			reponse.save()
		elif request.POST['question_type']=="open":
			question = Question.objects.get(id=request.POST['id'])
			reponse = Reponse_OPEN(question=question)
			text = request.POST['valeur']
			reponse.text = text
			reponse.save()
	return JsonResponse({'success':1})

def prof(request):
	addr = 'Quizz/prof.html'
	if 'code' not in request.session:
		code=0
		for index in range(0,9):
			numb=random.randint(1, 9)
			numb=numb*(10**index)
			code=code+numb

		session = Seance(code=code)
		session.save()
		request.session['code']=code #Sauvegarde dans la session pour un usage ultérieur
	else:
		code=request.session['code']
		if 'question_type' in request.POST:
			if request.POST['question_type']=="qcm":
				#creation de ask, une ligne de la table Question
				seance = Seance.objects.get(code=code)
				ask = Question(seance=seance, question_type="QCM")
				check = Question.objects.filter(seance=seance)
				if not check:
					ask.numero = 1
				else:
					ask.numero = Question.objects.filter(seance=seance).latest('numero').numero + 1
				# if request.POST['commentaire'] !="votre commentaire ici":
					# ajout d'un commentaire à la question si il y a
				ask.commentaire = request.POST['commentaire']
				ask.save()

			elif request.POST['question_type'] == "open":
				#creation de ask, une ligne de la table Question
				seance = Seance.objects.get(code=code)
				ask = Question(seance=seance, question_type="Open")
				check = Question.objects.filter(seance=seance)
				if not check:
					ask.numero = 1
				else:
					ask.numero = Question.objects.filter(seance=seance).latest('numero').numero + 1
				# if request.POST['commentaire'] !="votre commentaire ici":
					# ajout d'un commentaire à la question si il y a
				ask.commentaire = request.POST['commentaire']
				ask.save()

			elif request.POST['question_type'] == "close":
				request.session.flush()
				return redirect('/')

	return render(request, addr, locals())


ERR_SALLE_INTROUVABLE = 1
ERR_CODE_INVALIDE = 2

def error_message(errmsg):
	if errmsg == ERR_SALLE_INTROUVABLE:
		error = "Impossible de trouver cette salle"
	if errmsg == ERR_CODE_INVALIDE:
		error = "Veuillez entrer un numéro de salle valide."
	return error

def error(request, errmsg):
	error = error_message(errmsg)
	return render(request, 'Quizz/error.html', locals())

def error_json(errmsg):
	error = error_message(errmsg)
	return JsonResponse({'error':error_message(errmsg)})
