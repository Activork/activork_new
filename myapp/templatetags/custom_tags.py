from django import template
register = template.Library()
from myapp.models import UserProfile
import os

def decode_choices(intent):
    """
    Decode intent choices
    """
    decoder = dict(UserProfile.MY_CHOICES)
    decoded = [decoder[i] for i in intent]
    decoded.sort()
    return ', '.join(decoded)

def improve_quality(path):
	cmd = "pwd"
	new_path = os.path.realpath("profile_photos")
	print path
	location = path.split("/")
	print "location",location
	actual_path = new_path + "/" + location[-1]
	print actual_path
	cmd = "convert -contrast -enhance -density 500 -normalize -quality 100 "+actual_path+" "+actual_path+""
	os.system(cmd)
	return path


register.filter('decode_choices', decode_choices)
register.filter('improve_quality',improve_quality)
