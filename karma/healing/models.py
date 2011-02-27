from django.db import models

#################################################################################
# Utils
#################################################################################

class Request(models.Model):
	agent		= models.CharField(max_length=512)
	view		= models.CharField(max_length=128)
	session_id	= models.CharField(max_length=64)
	request_date= models.DateTimeField('Date Of Request')
	
	def __unicode__(self):
		return ', '.join([
			self.request_date.strftime("%b %d %Y"),
			self.name,
			self.view
		])


