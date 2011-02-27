from django.conf.urls.defaults import *
from django.conf import settings

import os
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^karma/', include('karma.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

	(r'^/?$', 'karma.healing.views.default'),
	(r'^biography/?$', 'karma.healing.views.biography'),
	(r'^therapy/?$', 'karma.healing.views.therapy'),
	(r'^center/?$', 'karma.healing.views.center'),
	(r'^testimonies/?(?P<name>\w+)?/?$', 'karma.healing.views.testimonies'),
	(r'^locale/(?P<language>\w+)/?$', 'karma.healing.views.locale'),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(
			r'^/?css/(?P<path>.*)$', 
			'django.views.static.serve', 
			{'document_root': (os.path.dirname(os.path.abspath(__file__)) + '/../data/css/')}
		),
		(
			r'^/?js/(?P<path>.*)$', 
			'django.views.static.serve', 
			{'document_root': (os.path.dirname(os.path.abspath(__file__)) + '/../data/js/')}
		),
		(
			r'^/?img/(?P<path>.*)$', 
			'django.views.static.serve', 
			{'document_root': (os.path.dirname(os.path.abspath(__file__)) + '/../data/img/')}
		),
		
	)
