from django.db import models
from django.contrib.auth.models import User

from tastypie.models import create_api_key

from connection.tasks import calculate_price, get_twitter_info

import hashlib
import os

CONNECTION_STATUS_CHOICES = (
    ('calculating', 'Calculating'),
    ('public', 'Public'),
    ('in-progress', 'In Progress'),
    ('closed', 'Closed'),
)

def upload_to_mugshot(instance, filename):
    """
    Uploads a mugshot.
    
    """
    hasher = hashlib.md5()
    for chunk in instance.mugshot.chunks():
        hasher.update(chunk)
    hash = hasher.hexdigest()
    base, ext = os.path.splitext(filename)

    return 'mugshots/{hash}{ext}'.format(hash=hash,
                                         ext=ext)

class Person(models.Model):
    """ Person which is requested """
    # Social connections
    twitter_handle = models.CharField(blank=True,
                                      max_length=255)

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    
    klout_score = models.PositiveIntegerField(blank=True, null=True)
    tweet_score = models.PositiveIntegerField(blank=True, null=True)
    score = models.PositiveIntegerField(blank=True, null=True)
    mugshot = models.URLField(blank=True)
    
    # meta fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.twitter_handle

    def set_score(self):
        """ Set's the price for this person """
        self.score = 100

    def full_name(self):
        """ Returns the full name of this person """
        full_name = '%s %s' % (self.first_name,
                               self.last_name)
        return full_name.trim()

    class Meta:
        db_table = 'persons'    

class Connection(models.Model):
    """ Connection model """
    title = models.CharField(max_length=255,
                             blank=True)
    url = models.URLField(blank=True)
    person = models.ForeignKey(Person)
    requested_by = models.ForeignKey(User,
                                     related_name='requested_by')
    
    responded_by = models.ForeignKey(User,
                                     blank=True,
                                     null=True,
                                     related_name='responded_by')

    price = models.DecimalField(blank=True,
                                null=True,
                                max_digits=5,
                                decimal_places=2)

    pitch = models.TextField(blank=True)

    is_connected = models.BooleanField()
    is_payed = models.BooleanField()
    status = models.CharField(max_length=255,
                              choices=CONNECTION_STATUS_CHOICES,
                              default=CONNECTION_STATUS_CHOICES[0][0])

    # meta fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s wants to meet %s' % (self.requested_by,
                                         self.person)

    class Meta:
        db_table = 'connections'    

# Create an API key
models.signals.post_save.connect(create_api_key, sender=User)

def calculate_price_handler(sender, instance, created, *args, **kwargs):
    if created:
        calculate_price(instance)

def get_twitter_info_handler(sender, instance, created, *args, **kwargs):
    if created:
        get_twitter_info(instance)

models.signals.post_save.connect(get_twitter_info_handler, sender=Person)
models.signals.post_save.connect(calculate_price_handler, sender=Connection)
