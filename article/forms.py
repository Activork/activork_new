from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):

    CHOICES=[('public','Public'),
         ('friends','Friends')]

    share_with = forms.ChoiceField(choices=CHOICES, initial='public',widget=forms.RadioSelect())
    class Meta:
	model = Article
	fields = ('name','image','posted_by','content','video','interest','share_with')
