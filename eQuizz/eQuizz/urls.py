"""eQuizz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Quizz import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^$', views.home),
	url(r'^etudiant/(?P<code>.*)', views.etudiant),
    url(r'^etudiant_refresh/(.*)', views.etudiant_refresh),
    #url(r'^prof_refresh/(?P<code>.*)/(?P<question_id>.*)', views.prof_refresh),
    url(r'^prof_refresh/(?P<code>[0-9]*)/(?P<question_id>[0-9]*)', views.prof_refresh),
    url(r'^etudiant_post', views.etudiant_post),
	url(r'^prof', views.prof),
    url(r'^download', views.download),
	url(r'^error/(?P<id>\d+)', views.error),
    url(r'^qrcode/(?P<code>[0-9]*)', views.qrcode),
	url(r'^logout/', views.logout),

]
