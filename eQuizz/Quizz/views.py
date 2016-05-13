# coding: utf8
import csv
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from Quizz.forms import *
import random
from Quizz.models import *
from django.db.models import Max, Min
import sys
import re
import unicodedata
import datetime
from django.utils import timezone

MAX_NUMBER_ANS = 4

# Create your views here.
#	myfield = models.CharField(validators=[RegexValidator(regex='^.{4}$', message='Length has to be 4', code='nomatch')])

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
			#request.session['code']=code
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

	data = {}

	#On récupère les question correspondant à une séance et un id donné
	if question_id=="0":
		data['qzero'] = 'qzero'
	else:
		question = Question.objects.filter(seance=seance, numero=question_id).get()
		data['question_type'] = question.question_type
		compte = []

		if not question:
			return error_json(ERR_QUESTION_INTROUVABLE)
		if question.question_type=="QCM":
			#On récupère les réponses à une question donnée
			#answers=Reponse_QCM.objects.filter(question=question)
			for ans in range(0,6):
				compte.append(Reponse_QCM.objects.filter(question=question, valeur=ans).count())
			data['nb_reponses'] = Reponse_QCM.objects.filter(question=question).count()
			data['reponses'] = compte

			reponses = Reponse_QCM.objects.filter(question=question)
			tempsreponse = [0 for i in range(10)]
			tempsreponsex = [i for i in range(10)]
			if reponses:
				max = reponses.aggregate(Max('date'))['date__max']
				min = question.date
				tt = (max - min).total_seconds()
				dt = int(tt/10)
				tempsreponsex = [i*dt for i in range(10)]
				for r in reponses:
					t = int(round(((r.date - min).total_seconds()/tt) * 9))
					tempsreponse[t] = tempsreponse[t] + 1
			data['tempsreponse'] = tempsreponse
			data['tempsreponsex'] = tempsreponsex

		elif question.question_type=="Open":
			##########################
			#	Temps de réponse	#
			##########################
			reponses = Reponse_OPEN.objects.filter(question=question)
			tempsreponse = [0 for i in range(10)]
			tempsreponsex = [i for i in range(10)]
			if reponses:
				max = reponses.aggregate(Max('date'))['date__max']
				min = question.date
				tt = (max - min).total_seconds()
				dt = int(tt/10)
				tempsreponsex = [i*dt for i in range(10)]
				for r in reponses:
					t = int(round(((r.date - min).total_seconds()/tt) * 9))
					tempsreponse[t] = tempsreponse[t] + 1
			data['tempsreponse'] = tempsreponse
			data['tempsreponsex'] = tempsreponsex

			data['nb_reponses'] = Reponse_OPEN.objects.filter(question=question).count()
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
				mot = ''.join((c for c in unicodedata.normalize('NFD', mot) if unicodedata.category(c) != 'Mn'))
				mot = re.sub('[^a-z0-9]', '', mot)
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

			data['reponses'] = compte


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

	data['nb_lost'] = Lost.objects.filter(seance = seance).count()

	##########################
	#	 graphe de losts	#
	##########################
	reponses = Lost.objects.filter(seance = seance)
	NOMBRE = 20
	tempsreponse = [0 for i in range(NOMBRE)]
	tempsreponsex = [i for i in range(NOMBRE)]
	if reponses:
		max = timezone.now()
		min = max - datetime.timedelta(0,60*5,0)
		min = min - datetime.timedelta(minutes=0, seconds=min.second%15, microseconds=min.microsecond)
		tt = datetime.timedelta(0,60*5,0).total_seconds()
		dt = int(tt/NOMBRE)
		tempsreponsex = [i*dt for i in range(NOMBRE)]
		for r in reponses:
			t = int(round(((r.date - min).total_seconds()/tt) * (NOMBRE-1)))
			if t > 0 and t <= NOMBRE-1:
				tempsreponse[t] = tempsreponse[t] + 1
	data['lost_data'] = tempsreponse
	data['lost_datax'] = tempsreponsex

	return JsonResponse(data)





def etudiant_refresh(request, code):
	try:
		seance = Seance.objects.filter(code=code)
	except ValueError:
		return error_json(ERR_CODE_INVALIDE)
	if not seance:
		return error_json(ERR_SALLE_INTROUVABLE)

	questions = Question.objects.filter(seance=seance)
	if not questions:
		return JsonResponse({})
	question = questions.latest('id')
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
		etudiant = request.session['id_student']
		seance = Seance.objects.filter(code = request.POST['code']).get()
		t = timezone.now() - datetime.timedelta(0,60*5,0)
		if Lost.objects.filter(seance = seance, id_etudiant = etudiant, date__gte = t):
			return JsonResponse({'error':1})
		lost = Lost(id_etudiant = etudiant, seance = seance)
		lost.save()
		return JsonResponse({'success':1})


def download(request):
	# Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="export.csv"'

	if 'code' not in request.session:
		return error_message(ERR_SALLE_INTROUVABLE)

	writer = csv.writer(response)

	code=request.session['code']
	seance = Seance.objects.get(code=code)
	questions = Question.objects.filter(seance=seance)
	for q in questions:
		writer.writerow(['Question n°'+str(q.numero), q.date, q.commentaire])
		if q.question_type == "QCM":
			writer.writerow([i+1 for i in range(6)])
			compte = []
			for ans in range(0,6):
				compte.append(Reponse_QCM.objects.filter(question=q, valeur=ans).count())
			writer.writerow(compte)

	return response


def prof(request):
	#compte = {'plop':'yolo'}
	compte = {}
	pourc = {}
	addr = 'Quizz/prof.html'
	if 'code' not in request.session: # On crée une nouvelle séance
		code=0
		for index in range(0,5):
			numb=random.randint(1, 9)
			numb=numb*(10**index)
			code=code+numb

		session = Seance(code=code)
		session.save()
		request.session['code']=code #Sauvegarde dans la session pour un usage ultérieur
		question_number = 0
	else: # On utilise la séance dans la session
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

		if "commentaire" in request.POST:
			question=Question.objects.filter(seance=seance, id=request.POST['id']).get()
			question.commentaire = request.POST['commentaire']
			question.save()

		question=Question.objects.filter(seance=seance)
		question_number = 0
		question_id = 0
			#request.session.flush()
			#return redirect('/')
		if question:
			q = Question.objects.filter(seance=seance).latest('id')
			question_id = q.id
			question_commentaire = q.commentaire
			question_number = q.numero

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
