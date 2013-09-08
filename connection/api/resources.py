from tastypie.resources import ModelResource
from connection.models import Connection, Person

from django.contrib.auth.models import User

class UserResource(ModelResource):
    """ Displaying all the connections """
    class Meta:
        queryset = User.objects.all()
        excludes = ['email', 'password', 'is_superuser']
        allowed_methods = ['get']

class ConnectionResource(ModelResource):
    """ Displaying all the connections """
    class Meta:
        queryset = Connection.objects.all()
        allowed_methods = ['get']

class PersonResource(ModelResource):
    """ Displaying all the Persons """        
    class Meta:
        queryset = Person.objects.all()
        allowed_methods = ['get']
