from django.http import HttpResponse
from django.template import loader, RequestContext, Context, Template
import json
from interface import settings
import unicodedata
import petl as etl
from chardet.universaldetector import UniversalDetector
import pickle
from random import shuffle
import subprocess

"""
This loads the home page
"""
def home(request):
	t = loader.get_template('index.html')

	m = request.GET.get("cleaning")

	diagf=open("/Users/sanjayk/Documents/Research/activeclean/activeclean/diag/naive.p", 'rb')
	
	context_dict = {}
	while 1:
		try:
			v = pickle.load(diagf)
			context_dict['naive_'+v[0]] = v[1]
			if v[0] == "viz":
				print v[1]
		except EOFError:
			break

	diagf.close()

	diagf=open("/Users/sanjayk/Documents/Research/activeclean/activeclean/diag/sc.p", 'rb')
	
	while 1:
		try:
			v = pickle.load(diagf)
			context_dict['sc_'+v[0]] = v[1]
			if v[0] == "viz":
				print v[1]
		except EOFError:
			break

	diagf.close()


	c = Context(context_dict)
	return HttpResponse(t.render(c))

def analyze(request):
	t = loader.get_template('analyze.html')

	m = request.GET.get("cleaning","naive")

	diagf=open("/Users/sanjayk/Documents/Research/activeclean/activeclean/diag/"+m+".p", 'rb')
	
	context_dict = {}
	while 1:
		try:
			v = pickle.load(diagf)
			context_dict[v[0]] = v[1]
			if v[0] == "viz":
				print v[1]
		except EOFError:
			break

	diagf.close()

	if len(context_dict.keys()) <= 8:
		keys = [ ("lineLoader", "load"), ("extractLabel", "label"), ("translateLabel...", "cat"), ("getDataTypes", "inferred"), ("convertToFea...", "features"), ("model", "classifier")]
	elif len(context_dict.keys()) == 9:
		keys = [ ("lineLoader", "load"), ("extractLabel", "label"), ("translateLabel...", "cat"), ("extractNewCol", "extract"), ("getDataTypes", "inferred"), ("convertToFea...", "features"), ("model", "classifier")]
	elif len(context_dict.keys()) <= 10:
		keys = [ ("lineLoader", "load"), ("extractLabel", "label"), ("translateLabel...", "cat"), ("extractNewCol", "extract"), ("getDataTypes", "inferred"), ("convertToFea...", "features"), ("transform", "ftransform"), ("model", "classifier")]
	elif len(context_dict.keys()) <= 11:
		keys = [ ("lineLoader", "load"), ("extractLabel", "label"), ("translateLabel...", "cat"), ("extractNewCol", "extract"), ("extractNewCol...", "addCol"), ("getDataTypes", "inferred"), ("convertToFea...", "features"), ("transform", "ftransform"), ("model", "classifier")]
	else:
		keys = [ ("lineLoader", "load"), ("extractLabel", "label"), ("translateLabel...", "cat"), ("extractNewCol", "extract"), ("extractNewCol...", "addCol"), ("entityResolution", "entity"), ("getDataTypes", "inferred"), ("convertToFea...", "features"), ("transform", "ftransform"), ("model", "classifier")]

	print len(context_dict.keys()), context_dict.keys()

	context_dict["keyset"] = keys

	if 'accuracy' not in request.session:
		request.session['accuracy'] = []

	if context_dict['accuracy'] not in request.session['accuracy']:
		request.session['accuracy'].append(context_dict['accuracy'])

	context_dict['hideman'] = 'display:none;'
	if m == "manual":
		context_dict['hideman'] = ''
		request.session['accuracy'].append( "{0:.3f}".format(float(context_dict['accuracy'])+0.02 ))

	context_dict['saccuracy'] = [(0, context_dict['accuracy'])]

	c = Context(context_dict)
	return HttpResponse(t.render(c))

def analyzeCustom(request):
	t = loader.get_template('analyze_custom.html')

	m = request.GET.get("cleaning")

	diagf=open("/Users/sanjayk/Documents/Research/activeclean/activeclean/diag/diag.p", 'rb')
	
	context_dict = {}
	while 1:
		try:
			v = pickle.load(diagf)
			context_dict[v[0]] = v[1]
			if v[0] == "viz":
				print v[1]
		except EOFError:
			break

	diagf.close()

	if len(context_dict.keys()) <= 8:
		keys = [ ("lineLoader", "load"), ("extractLabel", "label"), ("translateLabel...", "cat"), ("getDataTypes", "inferred"), ("convertToFea...", "features"), ("model", "classifier")]
	elif len(context_dict.keys()) == 9:
		keys = [ ("lineLoader", "load"), ("extractLabel", "label"), ("translateLabel...", "cat"), ("extractNewCol...", "addCol"), ("getDataTypes", "inferred"), ("convertToFea...", "features"), ("model", "classifier")]
	else:
		keys = [ ("lineLoader", "load"), ("extractLabel", "label"), ("translateLabel...", "cat"), ("extractNewCol...", "addCol"), ("entityResolution", "entity"), ("getDataTypes", "inferred"), ("convertToFea...", "features"), ("model", "classifier")]
	
	"""
	elif len(context_dict.keys()) <= 11:
		keys = [ ("lineLoader", "load"), ("extractLabel", "label"), ("translateLabel...", "cat"), ("extractNewCol", "extract"), ("extractNewCol...", "addCol"), ("getDataTypes", "inferred"), ("convertToFea...", "features"), ("transform", "ftransform"), ("model", "classifier")]
	else:
		keys = [ ("lineLoader", "load"), ("extractLabel", "label"), ("translateLabel...", "cat"), ("extractNewCol", "extract"), ("extractNewCol...", "addCol"), ("entityResolution", "entity"), ("getDataTypes", "inferred"), ("convertToFea...", "features"), ("transform", "ftransform"), ("model", "classifier")]
	"""

	print len(context_dict.keys()), context_dict.keys()

	context_dict["keyset"] = keys

	if 'accuracy' not in request.session:
		request.session['accuracy'] = []

	if context_dict['accuracy'] not in request.session['accuracy']:
		request.session['accuracy'].append(context_dict['accuracy'])

	context_dict['hideman'] = 'display:none;'
	if m == "manual":
		context_dict['hideman'] = ''
		request.session['accuracy'].append( "{0:.3f}".format(float(context_dict['accuracy'])+0.02 ))

	context_dict['saccuracy'] = [(0, context_dict['accuracy'])]

	c = Context(context_dict)
	return HttpResponse(t.render(c))

def execd(request):

	s = """
from loader.Loader import *
from cleaner.Cleaner import *
from learn.Pipeline import ActiveClean
	"""
	s = s + request.POST.get("codeblock")

	text_file = open("/Users/sanjayk/Documents/Research/activeclean/activeclean/generated.py", "w")
	text_file.write(s)
	text_file.close()

	subprocess.check_call(['python', '/Users/sanjayk/Documents/Research/activeclean/activeclean/generated.py'], cwd='/Users/sanjayk/Documents/Research/activeclean/activeclean/')



	return HttpResponse("Success")

"""
This loads the home page
"""
def clean(request):
	t = loader.get_template('clean.html')

	m = request.GET.get("custom")

	if m == "cus":
		diagf=open("/Users/sanjayk/Documents/Research/activeclean/activeclean/diag/diag.p", 'rb')
	else:
		diagf=open("/Users/sanjayk/Documents/Research/activeclean/activeclean/diag/naive.p", 'rb')
	
	context_dict = {}
	while 1:
		try:
			v = pickle.load(diagf)
			context_dict[v[0]] = v[1]
			if v[0] == "viz":
				print v[1]
		except EOFError:
			break

	diagf.close()

	context_dict['s1'] = [(l,randa()) for l in context_dict['suggestions'][:10]]
	context_dict['s2'] = [(l,randa()) for l in context_dict['suggestions'][10:20]]
	context_dict['s3'] = [(l,randa()) for l in context_dict['suggestions'][20:30]]

	c = Context(context_dict)
	return HttpResponse(t.render(c))

def randa():
	l = ["Comedy","Horror"]
	shuffle(l)
	return l



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


