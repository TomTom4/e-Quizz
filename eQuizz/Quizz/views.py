# coding: utf8
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from Quizz.forms import *
import random
from Quizz.models import *
import sys

MAX_NUMBER_ANS = 4

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
			if 'id_student' not in request.session:
				id=0
				for index in range(0,9):
					numb=random.randint(1, 9)
					numb=numb*(10**index)
					id=id+numb

				request.session['id_student']=id #Création d'un id étudiant/session
			id_etudiant=request.session['id_student']

	except ValueError:
		addr='Quizz/error.html'
		error="Veuillez entrer un numéro de salle valide."

	return render(request, addr, locals())

def prof_refresh(request, code, question_id):
	#Constantes pour les tailles des textes
	MAX_SIZE_VALUE=50
	MIN_SIZE_VALUE=10
	nb_reponses=0
	try:
		seance=Seance.objects.filter(code=code)
	except ValueError:
		return error_json(ERR_CODE_INVALIDE)
	if not seance:
		return error_json(ERR_SALLE_INTROUVABLE)

	#On récupère les question correspondant à une séance et un id donné
	if question_id=="0":
		return JsonResponse({'qzero':'qzero'})
	else:
		question = Question.objects.filter(seance=seance, numero=question_id).get()
		compte = []

		if not question:
			return error_json(ERR_QUESTION_INTROUVABLE)
		if question.question_type=="QCM":
			#On récupère les réponses à une question donnée
			#answers=Reponse_QCM.objects.filter(question=question)
			for ans in range(0,6):
				compte.append(Reponse_QCM.objects.filter(question=question, valeur=ans).count())
			nb_reponses=Reponse_QCM.objects.filter(question=question).count()
		elif question.question_type=="Open":
			count={}
			mots=[]
			answers=Reponse_OPEN.objects.filter(question=question)
			for ans in answers:
				mots.append(ans.text)
			max=0
			min=sys.maxint
			#mots=sorted(mots)
			for mot1 in mots:
				mot = mot1.lower()
				if mot not in count:
					count[mot]=1
				else:
					count[mot]=count[mot]+1
				if count[mot]>max:
					max=count[mot]


			for index in count:
				if count[index]<min:
					min=count[index]

			#A ce moment-à on a les mots comptés dans compte[]
			#On écrit dans compte qu'on considère comme un string
			#compte=""
			Range=MAX_SIZE_VALUE - MIN_SIZE_VALUE
			temp=[]
			compte=[]
			for mot, value in count.items():


				#Convertit les poids des valeurs entre 10 et 50

				#On regarde le rapport entre max et min pour savoir quel algorithme de relation entre les réponses on prend
				if ((max/min)<Range):
					if value==max:
						value=MAX_SIZE_VALUE
					else:
						value=((min*Range)/max) + MIN_SIZE_VALUE
				else:
					if max==min:
						value=MAX_SIZE_VALUE
					else:
						value=int((((value-min)*(Range))/(max-min))+MIN_SIZE_VALUE)
				#temp.append(mot+"-"+str(value)+"-"+str(count[mot]))
				temp.append(mot)
				temp.append(value)
				compte.append(temp)
				temp=[]


			# temp.append('max'+str(max))
			# temp.append(25)
			# compte.append(temp)
			# temp=[]
			#
			# temp.append('min'+str(min))
			# temp.append(25)
			# compte.append(temp)
			# temp=[]

	#if not question:
		#return JsonResponse({})
	nb_reponses=Reponse_OPEN.objects.filter(question=question).count()
	nb_lost = Lost.objects.filter(seance = seance).count()
	return JsonResponse({
		'reponses':compte,
		'question_type':question.question_type,
		'compteur': nb_lost,
		'nb_reponses': nb_reponses,

		})





def etudiant_refresh(request, code):
	try:
		seance = Seance.objects.filter(code=code)
	except ValueError:
		return error_json(ERR_CODE_INVALIDE)
	if not seance:
		return error_json(ERR_SALLE_INTROUVABLE)

	question = Question.objects.filter(seance=seance).latest('id')
	if question.question_type=="QCM":
		deja_repondu=Reponse_QCM.objects.filter(question=question, id_etudiant=request.session['id_student'])
	elif question.question_type=="Open":
		deja_repondu=Reponse_OPEN.objects.filter(question=question, id_etudiant=request.session['id_student'])

	if not question:
		return JsonResponse({})

	if not deja_repondu:
		return JsonResponse({
			'id':question.id,
			'question_type':question.question_type,
			'numero':question.numero,
		})
	else:
		return JsonResponse({})

def etudiant_post(request):
	if 'question_type' in request.POST:
		if request.POST['question_type']=="qcm":
			question = Question.objects.get(id=request.POST['id'])
			reponse = Reponse_QCM(question=question, id_etudiant=request.session['id_student'])
			valeur = request.POST['valeur']
			reponse.valeur = valeur
			reponse.save()
		elif request.POST['question_type']=="open":
			question = Question.objects.get(id=request.POST['id'])
			reponse = Reponse_OPEN(question=question, id_etudiant=request.session['id_student'])
			text = request.POST['texte']
			reponse.text = text
			reponse.save()
		return JsonResponse({'success':1})
	if  'lost' in request.POST:
		seance = Seance.objects.filter(code = request.session['code']).get()
		etudiant = request.session['id_student']
		lost = Lost(id_etudiant = etudiant, seance = seance)
		lost.save()
		return JsonResponse({'success':1})


def prof(request):
	#compte = {'plop':'yolo'}
	compte = {}
	pourc = {}
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
		question_number = 0
	else:
		code=request.session['code']
		seance = Seance.objects.get(code=code)
		if 'question_type' in request.POST:
			if request.POST['question_type']=="qcm":
				#creation de ask, une ligne de la table Question

				ask = Question(seance=seance, question_type="QCM")
				check = Question.objects.filter(seance=seance)
				if not check:
					ask.numero = 1
				else:
					ask.numero = Question.objects.filter(seance=seance).latest('numero').numero + 1

				question_number=ask.numero
				# if request.POST['commentaire'] !="votre commentaire ici":
					# ajout d'un commentaire à la question si il y a
				ask.commentaire = request.POST['commentaire']
				ask.save()

			elif request.POST['question_type'] == "open":
				#creation de ask, une ligne de la table Question
				#seance = Seance.objects.get(code=code)
				ask = Question(seance=seance, question_type="Open")
				check = Question.objects.filter(seance=seance)
				if not check:
					ask.numero = 1
				else:
					ask.numero = Question.objects.filter(seance=seance).latest('numero').numero + 1

				question_number=ask.numero
				# if request.POST['commentaire'] !="votre commentaire ici":
					# ajout d'un commentaire à la question si il y a
				ask.commentaire = request.POST['commentaire']
				ask.save()

			elif request.POST['question_type'] == "close":
				request.session.flush()
				return redirect('/')

			elif request.POST['question_type'] == "next":
				question_number = int(request.POST['qnumber'])
				question_number = question_number + 1
				#Attention il est possible d'avancer dans les questions!!!

			elif request.POST['question_type'] == "prec":
				question_number = int(request.POST['qnumber'])
				if question_number > 1:
					question_number = question_number - 1

			#On entre dans ce cas si jamais on a pas de requêtes (en l'occurence si jamais on perd la co par exemple
		else:
			question=Question.objects.filter(seance=seance)
			if not question:
				request.session.flush()
				return redirect('/')
			else:
				question_number = Question.objects.filter(seance=seance).latest('id').numero

		question = Question.objects.filter(seance=seance)
		if question:

			question = Question.objects.filter(seance=seance, numero=question_number).get()

			#question_number = question.numero
			total = Reponse_QCM.objects.filter(question=question).count()

			#Pour utilisation avec ID
			#question = Question.objects.filter(seance=seance, id=question_id)
			if question.question_type=="QCM":
			#On récupère les réponses à une question donnée
			#answers=Reponse_QCM.objects.filter(question=question)
				for ans in range(0,MAX_NUMBER_ANS):
					compte[ans]=Reponse_QCM.objects.filter(question=question, valeur=ans).count()
					if total>0:
						pourc[ans]=(compte[ans]*100)/total
					else:
						pourc[ans]=0
				compte_sorted=sorted(compte)
			#elif question.question_type=="Open":

	current_site = get_current_site(request)
	return render(request, addr, locals())

def qrcode(request, code):
	current_site = get_current_site(request)
	return render(request, "Quizz/qrcode.html", locals())

def logout(request):
	request.session.flush()
	return redirect('/')

ERR_SALLE_INTROUVABLE = 1
ERR_CODE_INVALIDE = 2
ERR_NO_QUESTION = 3
ERR_QUESTION_INTROUVABLE = 4

def error_message(errmsg):
	if errmsg == ERR_SALLE_INTROUVABLE:
		error = "Impossible de trouver cette salle"
	if errmsg == ERR_CODE_INVALIDE:
		error = "Veuillez entrer un numéro de salle valide."
	if errmsg == ERR_NO_QUESTION:
		error = "Une erreur inattendue s'est produite, veuillez réessayer plus tard."
	if errmsg == ERR_QUESTION_INTROUVABLE:
		error = "Impossible de trouver cette question."
	return error

def error(request, errmsg):
	error = error_message(errmsg)
	return render(request, 'Quizz/error.html', locals())

def error_json(errmsg):
	error = error_message(errmsg)
	return JsonResponse({'error':error_message(errmsg)})
