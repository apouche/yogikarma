from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from lib.utils import add_request, get_referer_view
import inspect

def default(request):
	
	## Start by adding a request object ##
	add_request(request, inspect.currentframe())
	
	return render_to_response('web/index.html', {})
	
def biography(request):

	return render_to_response('web/bio.html', {})
	
def therapy(request):

	return render_to_response('web/therapy.html', {})

def center(request):

	return render_to_response('web/center.html', {})

def testimonies(request, name):

	t = None
	if name is not None:
		t = "testimonies/%s/%s_%s.html" % (name, name, request.session["django_language"])
		print t
		
	return render_to_response('web/testimonies.html', {'testimony': t})
	
	
	
def locale(request, language):
	referer = get_referer_view(request, 'default')
	
	request.session["django_language"] = language
	
	return HttpResponseRedirect(referer)
	
	