from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from Quizz.forms import *

# Create your views here.

def home(request):

	#if request.method == 'POST':
		#form = AccessQuizz(request.POST['code'])
		#if form.is_valid():
		
			#room=form.cleaned_data['code'];
		
	return render(request, 'Quizz/proto.html', locals())
	
def name(request):
	
	code = request.POST['code']
	

	return render(request, 'Quizz/name.html', locals())
	
def ppl(request):
	
	nom = request.POST['name']
	request.session['name'] = nom
	name=request.session['name']
	
	return render(request, 'Quizz/main.html', locals())

