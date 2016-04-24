from django import forms

class AccessQuizz(forms.Form):
    code = forms.CharField(max_length=10)

