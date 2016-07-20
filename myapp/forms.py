from django import forms
from .models import Upload_Image,Event_Staff
from django import forms
from image_cropping import ImageCropWidget

class Upload_ImageForm(forms.ModelForm):
    class Meta:
	
    
	model = Upload_Image
	fields = ('image', 'cropping')



"""class Hangout_StaffForm(forms.ModelForm):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
        )

    days = forms.MultipleChoiceField(choices=DAYS_OF_WEEK, required=True, widget=forms.CheckboxSelectMultiple(), label='Select Days', initial=("1", "2"))
    class Meta:
        model = Hangout_Staff"""


class Event_StaffForm(forms.ModelForm):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
        )

    days = forms.MultipleChoiceField(choices=DAYS_OF_WEEK, required=True, widget=forms.CheckboxSelectMultiple(), label='Select Days', initial=("1", "2"))
    class Meta:
        model = Event_Staff



