from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from photos.models import Photo,Tag,sync_flickr_if_needed

import inspect

def default(request, tag_=None):
	
	sync_flickr_if_needed()
	
	tags  	= Tag.objects.all()
	tag	 	= None
	 
	photos = None
	
	if tag_ is not None:
		tag 	= Tag.objects.get(pk=tag_)
		photos 	= Photo.objects.filter(tags__name__exact=tag_)	
	else:
		photos = {}
		for tag in tags:
			p = Photo.objects.filter(tags__name__exact=tag.name)
			photos[tag.name] = p
		tag = None
		
	context = {'tags' : tags, 'photos' : photos, 'tag' : tag, 'notree' : True }
	
	return render_to_response('web/photos.html', context)
	
def photo(request, tag_, pid_):

	tags  	= Tag.objects.all()
	tag  	= Tag.objects.get(pk=tag_)
	
	photos 	= Photo.objects.filter(tags__name__exact=tag_)
	photo	= Photo.objects.get(pk=pid_)

	context = {'tags' : tags, 'photos' : photos, 'tag' : tag, 'photo' : photo, 'notree' : True  }

	return render_to_response('web/photos.html', context)