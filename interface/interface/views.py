from django.http import HttpResponse
from django.template import loader, RequestContext, Context, Template
import json
from interface import settings
import unicodedata


"""
This loads the home page
"""
def home(request):
	t = loader.get_template('index.html')
	c = Context({"my_name": "Dolores"})
	return HttpResponse(t.render(c))

def sanitize(line):
	return unicodedata.normalize('NFKD', unicode(line.strip(),errors='replace')).encode('ascii','ignore').encode('string_escape')

"""
This loads a sample of data from the file
"""
def load(request):
	filename = request.GET.get('name','')
	fullpath = settings.DATA_DIR+filename

	n = 25
	f = open(fullpath,'rb+')
	line = f.readline()
	data = []
	while line != "" and n > 0:
		data.append(sanitize(line))
		line = f.readline() 
		n = n - 1

	print fullpath

	response_data = {}
	response_data['result'] = data
	return HttpResponse(json.dumps(response_data), content_type="application/json")