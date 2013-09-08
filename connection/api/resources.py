from django.contrib.auth.models import User
from django.conf.urls import url
from django.conf import settings

from tastypie.resources import ModelResource
from tastypie.validation import Validation
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.http import HttpSeeOther
from tastypie.exceptions import ImmediateHttpResponse

from connection.models import Connection, Person

import twitter

class PersonValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'At least supply us with the twitter handle.'}

        if 'twitter_handle' not in bundle.data:
            return {'__all__': 'At least supply us with the twitter handle.'}

        twitter_handle = bundle.data['twitter_handle']
        api = twitter.Api(consumer_key=settings.API_TWITTER_KEY,
                          consumer_secret=settings.API_TWITTER_SECRET,
                          access_token_key=settings.API_TWITTER_TOKEN_KEY,
                          access_token_secret=settings.API_TWITTER_TOKEN_SECRET)

        try:
            api.GetUser(screen_name=twitter_handle)
        except:
            return {'__all__': 'User with this Twitter user does not exist.'}

        return {}

class PersonResource(ModelResource):
    """ Displaying all the Persons """        
    class Meta:
        queryset = Person.objects.all()
        allowed_methods = ['get', 'post']
        detail_uri_name = 'twitter_handle'
        excludes = ['id']
        validation = PersonValidation()
        authorization = Authorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<twitter_handle>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def obj_create(self, bundle, **kwargs):
        twitter_handle = bundle.data['twitter_handle']
        try:
            Person.objects.get(twitter_handle=twitter_handle)
        except Person.DoesNotExist:
            pass
        else:
            raise ImmediateHttpResponse(HttpSeeOther("Person already exists"))
        return super(PersonResource, self).obj_create(bundle,
                                                      **kwargs)

class UserResource(ModelResource):
    """ Displaying all the connections """
    class Meta:
        queryset = User.objects.all()
        excludes = ['email', 'password', 'is_superuser']
        allowed_methods = ['get']
        detail_uri_name = 'username'
        excludes = ['id',]

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
        
class ConnectionResource(ModelResource):
    """ Displaying all the connections """
    person = fields.ToOneField(PersonResource, 'person', full=True)
    requested_by = fields.ToOneField(UserResource, 'requested_by', full=True)
    responded_by = fields.ToOneField(UserResource, 'responded_by', null=True, full=True)

    class Meta:
        queryset = Connection.objects.all()
        allowed_methods = ['get']

