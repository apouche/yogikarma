from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from lib.utils import add_request, get_referer_view
import inspect

def default(request):
	## Start by adding a request object ##
	add_request(request, inspect.currentframe())
	
	set_default_local(request)
	
	#show tree in first window only
	return render_to_response('web/index.html', {'tree' : True})
	
def biography(request):

	return render_to_response('web/bio.html', {})
	
def therapy(request):

	return render_to_response('web/therapy.html', {})

def center(request):

	return render_to_response('web/center.html', {})
	
def seminars(request):

	return render_to_response('web/seminars.html', {})
	
def private(request):

	return render_to_response('web/private.html', {})

def testimonies(request, name):
	
	set_default_local(request)
	
	t = None
	if name is not None:
		t = "testimonies/%s/%s_%s.html" % (name, name, request.session["django_language"])
		print t
		
	return render_to_response('web/testimonies.html', {'testimony': t, 'name' : name })
	
def locale(request, language):
	referer = get_referer_view(request, 'default')
	
	request.session["django_language"] = language
	
	return HttpResponseRedirect(referer)
	
def set_default_local(request):
	referer = get_referer_view(request, '/')
	
	#French by default but potientally base this on the IP it's coming from
	if 'django_language' not in request.session:
		request.session["django_language"] = 'fr'
	