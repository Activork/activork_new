from django import template

register = template.Library()


def get_tags_list(tags):
	li = []
	for i in tags.split(","):
		li.append(i.decode('ascii'))

	return li


register.filter('get_tags',get_tags_list)
