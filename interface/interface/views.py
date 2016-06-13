from django.http import HttpResponse
from django.template import loader, RequestContext, Context, Template
import json
from interface import settings
import unicodedata
import petl as etl
from chardet.universaldetector import UniversalDetector

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
This loads a sample of data from the file, 

!!fix header 
"""
def load(request):
	filename = request.GET.get('name','')
	fullpath = settings.DATA_DIR+filename
	"""
	detector = UniversalDetector()
	file_open = open(fullpath)
	for line in file_open.readlines():
		detector.feed(line)
		if detector.done: break
		detector.close()
	file_open.close()
	"""
	encoding = 'ascii'#detector.result['encoding']

	response_data = {}
	a = tryExtractors(fullpath, encoding)
	response_data['result'] = [row for row in etl.head(a)]
	response_data['headers'] = etl.header(a)
	typeInference(a)
	return HttpResponse(json.dumps(response_data), content_type="application/json")


def loadCSV(filname, encoding, delimiter=','):
	print encoding
	table2 = etl.fromcsv(filname,delimiter=delimiter, encoding=encoding)
	return table2

#first row header fix

def tryExtractors(filename, encoding, delimiter_list=[',','\t', ';', '|'], quality_metric= lambda x: len(x)):
	result = []
	for d in delimiter_list:
		csvView = loadCSV(filename, encoding, delimiter=d)
		result.append((quality_metric(etl.header(csvView)), csvView))
	result.sort()
	return cleanFormatTable(result[-1][1])

def cleanFormatTable(table):
	newtable = table
	for h in etl.header(table):
		newtable = etl.convert(table, h, sanitize)
	return newtable

def typeInference(table):
	for h in etl.header(table):
		col =  etl.cut(table, h)
		print etl.nrows(col)


