from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    """ Person which is requested """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    score = models.PositiveIntegerField()

    # Social connections
    twitter_handle = models.CharField(blank=True,
                                      max_length=255)

    # meta fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

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
    person = models.ForeignKey(Person)
    requested_by = models.ForeignKey(User,
                                     related_name='requested_by')
    
    responded_by = models.ForeignKey(User,
                                     blank=True,
                                     null=True,
                                     related_name='connected_by')

    price = models.DecimalField(max_digits=5,
                                decimal_places=2)

    pitch = models.TextField(blank=True)

    is_connected = models.BooleanField()
    is_payed = models.BooleanField()

    # meta fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s wants to meet %s' % (self.requested_by,
                                         self.person)

    class Meta:
        db_table = 'connections'    
