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
		
	return render(request, 'Quizz/proto.html', locals())
	
def name(request):
	
	code = request.POST['code']
	querySet=Seance.objects.filter(code=code)
	if (querySet==[]):
		return render(request, 'Quizz/proto.html', locals())
	else:
		return render(request, 'Quizz/name.html', locals())

	
def ppl(request):
	
	nom = request.POST['name']
	request.session['name'] = nom
	name=request.session['name']
	code = request.code
	
	return render(request, 'Quizz/main.html', locals())
	
def prof(request):

	code=0
	for index in range(0,9):
		numb=random.randint(1, 9)
		numb=numb*(10**index)
		code=code+numb
	
	session = Seance(code=code)
	session.save()
	
	return render(request, 'Quizz/prof.html')

