from django.db import models
from django.utils.encoding import smart_str

from flickrapi import FlickrAPI
from datetime import datetime,timedelta
from threading import Thread

class Tag(models.Model):
	name	= models.CharField(max_length=31, primary_key=True)
	raw		= models.CharField(max_length=31)
	
	def __unicode__(self):
		return ', '.join([self.name, self.raw])
	
class Photo(models.Model):
	flickr_id 	= models.CharField(max_length=31, primary_key=True)
	title		= models.CharField(max_length=127)
	description = models.TextField(null = True)
	
	server 		= models.IntegerField()
	farm		= models.IntegerField()
	secret		= models.CharField(max_length=50)
	page		= models.CharField(max_length=127, null = True)
	
	added_date	= models.DateTimeField('creation date')
	posted_date = models.DateTimeField('posted date')
	updated_date= models.DateTimeField('updated date')
	
	tags		= models.ManyToManyField(Tag, verbose_name = 'list of tags')

	
	class Meta:
		ordering = ('-posted_date', 'flickr_id')
	
	def __unicode__(self):
		return ', '.join([self.flickr_id, self.title, str(self.server), str(self.farm)])

	def get_url(self, size=''):
		if size != '':
			size = '_' + size
		
		return "http://farm%d.static.flickr.com/%d/%s_%s%s.jpg" % (
			self.farm,
			self.server,
			self.flickr_id,
			self.secret,
			size)
			
	def get_url_s(self):
		return self.get_url('s')
		
	def get_url_t(self):
		return self.get_url('t')
		
	def get_url_b(self):
		return self.get_url('b')
			
	def get_flickr_url(self):
		return "http://www.flickr.com/photos/%s/%s/" % (self.set.twin.flickr_id, self.flickr_id)
					
class Update(models.Model):
	updated_date	= models.DateTimeField('updated date')
	updated			= models.BooleanField(default=False)
	
#################################################################################
# Sync Functions
#################################################################################

API_KEY = 'bb9a6a6a8458f517adc8e8d1a93112e7'
API_SECRET = '73b9ae14c02f1f6f'
UPDATE_DELTA = 1

def sync_flickr_if_needed(*args, **kwargs):
	updates = Update.objects.all().order_by('updated_date').reverse()
	worst 	= datetime.now() - timedelta(seconds=UPDATE_DELTA)
	
	if updates.count() > 0 and updates[0].updated_date > worst:
		return
	
	t = Thread(target=sync_flickr, args=['60532880@N04'])
	t.setDaemon(True)
	t.start()
	

def sync_flickr(*args, **kwargs):
	u = Update(updated_date=datetime.now())
	
	flickr = FlickrAPI(API_KEY, API_SECRET)
	
	flickr_photos = []
	
	for flickr_id in args:
		
		page = 1
		while page > 0:
			request = flickr.people_getPublicPhotos(user_id=flickr_id, per_page=100, page=page, extras='last_update')
			pages 	= int(request.find('photos').attrib['pages'])
			photos	= request.find('photos').findall('photo')
			
			#Add photos to all list
			flickr_photos.extend(photos)
		
			print "[Flickr] - Processing page: %d/%d User: [%s]" % (page,pages,flickr_id)
		
			for photo in photos:
				photo_id = photo.attrib['id']
			
				# update photo if already in db
				try:
					p = Photo.objects.get(flickr_id = photo_id)
					updated_date = datetime.fromtimestamp(float(photo.attrib['lastupdate']))
					if p.updated_date < updated_date:
						p.title 		= photo.attrib['title']
						p.updated_date 	= updated_date
						p.farm			= int(photo.attrib['farm'])
						p.server		= int(photo.attrib['server'])
						p.secret		= photo.attrib['secret']

						print '[Flickr] Updating Photo: ' + p.titl

						sync_photo(p)
				#otherwise create and save
				except:
					p = Photo(
						flickr_id 	= photo_id,
						server	 	= int(photo.attrib['server']),
						secret		= photo.attrib['secret'],
						title 		= photo.attrib['title'],
						farm		= int(photo.attrib['farm']),
						added_date	= datetime.now(),
						updated_date= datetime.fromtimestamp(float(photo.attrib['lastupdate'])),
						#set			= photoset
					)
					print '[Flickr] - Adding New Photo: %s' % (smart_str(p.title))
					sync_photo(p)

					u.updated = True
		
		
			if page == pages:
				page = 0
			else:
				page = page + 1				
	
	#Update deleted photos if needed
	sync_deleted_photos(flickr_photos)
	
	print "[Flickr] - Done Updating"		
	u.save()
	
def sync_deleted_photos(fetched_photos):
	db_photos		= Photo.objects.all()
	
	db_photos_ids = []
	for db_photo in db_photos:
		db_photos_ids.append(db_photo.flickr_id)
	
	if len(db_photos) > len(fetched_photos):
		print "[Flickr] - %d photos to be deleted" % (len(db_photos) - len(fetched_photos))
		
		for photo in fetched_photos:
			photo_id = photo.attrib['id']
			if photo_id in db_photos_ids:
				db_photos_ids.remove(photo_id)
				
		for photo in db_photos_ids:
			print "[Flickr] - Photo: %s will be deleted" % (photo)
			Photo.objects.get(pk=photo).delete()
				
	

def sync_set(photoset):
	flickr 		= FlickrAPI(API_KEY)
	request 	= flickr.photosets_getPhotos(photoset_id=photoset.flickr_id,extras='last_update')
	photos		= request.find('photoset').findall('photo')
	
	print "Syncing set: %s" % photoset.title
	
	updated = False
	
	for photo in reversed(photos):
		photo_id = photo.attrib['id']
		try:
			p = Photo.objects.get(flickr_id = photo_id)
			updated_date = datetime.fromtimestamp(float(photo.attrib['lastupdate']))
			if p.updated_date < updated_date:
				p.title 		= photo.attrib['title']
				p.updated_date 	= updated_date
				
				sync_photo(p)
				
				
		except:
			p = Photo(
				flickr_id 	= photo_id,
				server	 	= int(photo.attrib['server']),
				secret		= photo.attrib['secret'],
				title 		= photo.attrib['title'],
				farm		= int(photo.attrib['farm']),
				added_date	= datetime.now(),
				updated_date= datetime.fromtimestamp(float(photo.attrib['lastupdate'])),
				set			= photoset
			)
			sync_photo(p)
			
			updated = True
			
	return updated
def sync_photo(photo):
	flickr 		= FlickrAPI(API_KEY)
	infos 		= flickr.photos_getInfo(photo_id=photo.flickr_id).find('photo')
	exifs		= flickr.photos_getExif(photo_id=photo.flickr_id).find('photo').findall('exif')
	
	print "\tSyncing Photo: %s" % photo.title
	
	for exif in exifs:
		if exif.attrib['label'] == 'Aperture' and exif.attrib['tag'] == 'FNumber':
			photo.aperture = exif.find('clean').text
		if exif.attrib['label'] == 'Model' and exif.attrib['tag'] == 'Model':
			photo.camera = exif.find('raw').text
		if exif.attrib['label'] == 'Exposure' and exif.attrib['tag'] == 'ExposureTime':
			photo.exposure = exif.find('raw').text
		if exif.attrib['label'] == 'ISO Speed' and exif.attrib['tag'] == 'ISO':
			photo.iso = exif.find('raw').text
		if exif.attrib['label'] == 'Lens' and exif.attrib['tag'] == 'Lens':
			photo.lens = exif.find('raw').text
			
	photo.posted_date = datetime.fromtimestamp(float(infos.find('dates').attrib['posted']))
	photo.description = infos.find('description').text
	
	tags = infos.find('tags').findall('tag')
	
	photo.tags.clear()		# clear all previous tags if present
	
	#Save photo prior saving the many to many relationship with tags
	try:
		photo.save()
	except:
		print '\t\tFail to Save Photo: %s' % (photo.title)
		return photo
	
	for tag in tags:
		tag_id  = tag.text[0:31]
		print '\t\tFound tag: %s' % tag_id
		try:
			t = Tag.objects.get(pk=tag_id)
			photo.tags.add(t)
		except:	
			t = Tag(name=tag.text, raw=tag.attrib['raw'])
			t.save()
			photo.tags.add(t)
	
	#print '[Flickr] Exif for %s: %s, %s, %s' % (photo.title, photo.lens, photo.iso, photo.posted_date)
	
	
	
	return photo
	
