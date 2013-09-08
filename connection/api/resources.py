from django.contrib.auth.models import User
from django.conf.urls import url

from tastypie.resources import ModelResource

from tastypie import fields

from connection.models import Connection, Person

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

class PersonResource(ModelResource):
    """ Displaying all the Persons """        
    class Meta:
        queryset = Person.objects.all()
        allowed_methods = ['get']
        detail_uri_name = 'twitter_handle'
        excludes = ['id',]

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<twitter_handle>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
        
class ConnectionResource(ModelResource):
    """ Displaying all the connections """
    person = fields.ToOneField(PersonResource, 'person', full=True)
    requested_by = fields.ToOneField(UserResource, 'requested_by', full=True)
    responded_by = fields.ToOneField(UserResource, 'responded_by', null=True, full=True)

    class Meta:
        queryset = Connection.objects.all()
        allowed_methods = ['get']

