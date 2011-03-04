from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from lib.utils import add_request, get_referer_view
import inspect

def default(request):
	## Start by adding a request object ##
	add_request(request, inspect.currentframe())
	
	r = set_default_local(request)
	if r is not None:
		return r
	
	return render_to_response('web/index.html', {})
	
def biography(request):
	
	r = set_default_local(request)
	if r is not None:
		return r

	return render_to_response('web/bio.html', {})
	
def therapy(request):
	
	r = set_default_local(request)
	if r is not None:
		return r

	return render_to_response('web/therapy.html', {})

def center(request):
	
	r = set_default_local(request)
	if r is not None:
		return r

	return render_to_response('web/center.html', {})

def testimonies(request, name):
	
	r = set_default_local(request)
	if r is not None:
		return r
		
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
		
		#Redirect to previous caller page if no default language was set
		return  HttpResponseRedirect(referer)
	return None