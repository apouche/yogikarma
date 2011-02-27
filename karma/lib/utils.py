from healing.models import Request
import inspect
import re

def add_request(request, frame):
	f = re.sub(r'^.*karma/', '', frame.f_code.co_filename)
	
	request.session.set_test_cookie()
	
	#m = re.search(r'^(?P<base>[^\s]+)\s+\(\w+;\s\)')
	try:
		r = Request(
			agent 			= request.META['HTTP_USER_AGENT'],
			view			= f + ': ' + frame.f_code.co_name,
			session_id		= request.session.session_key,
			request_date 	= datetime.now()
		)
		r.save()
	except:
		return

def get_referer_view(request, default=None):
    ''' 
    Return the referer view of the current request

    Example:

        def some_view(request):
            ...
            referer_view = get_referer_view(request)
            return HttpResponseRedirect(referer_view, '/accounts/login/')
    '''

    # if the user typed the url directly in the browser's address bar
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return default

    # remove the protocol and split the url at the slashes
    referer = re.sub('^https?:\/\/', '', referer).split('/')
    
    if re.match(request.META.get('SERVER_NAME'), referer[0], re.IGNORECASE) is None:
        return default

    # add the slash at the relative path's view and finished
    referer = u'/' + u'/'.join(referer[1:])
    return referer