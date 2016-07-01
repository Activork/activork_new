from django import forms
from collections import OrderedDict
from django.contrib.auth import get_user_model



class SignupForm(forms.Form):
    phone_no = forms.CharField(max_length=10, label='Phone No.',widget=forms.TextInput(attrs={'placeholder':
                                                             ('Phone No.')}))

    class Meta:
	model = get_user_model()
	
	fields = ['username','email','phone_no','password1']

    def __init__(self,*args, **kwargs):
	#self.request = request
    	super(SignupForm, self).__init__(*args, **kwargs)
    	fields_key_order = ['username', 'email', 'phone_no','password1', 'password2']
	if (self.fields.has_key('keyOrder')):
    		self.fields.keyOrder = fields_key_order
	else:
    		self.fields = OrderedDict((k, self.fields[k]) for k in fields_key_order)
	
    def save(self, user):
        user.phone_no = self.cleaned_data['phone_no']
	user.first_name = self.cleaned_data['username']
        user.save()
	#print user.phone_no
