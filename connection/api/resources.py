from django.contrib.auth.models import User
from django.conf.urls import url
from django.http import HttpResponseRedirect

from tastypie.resources import ModelResource
from tastypie.validation import Validation
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import ALL

from connection.models import Connection, Person
from ntro.utils import get_twitter_user

class PersonValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'At least supply us with the twitter handle.'}

        if 'twitter_handle' not in bundle.data:
            return {'__all__': 'At least supply us with the twitter handle.'}

        twitter_handle = bundle.data['twitter_handle']

        try:
            get_twitter_user(twitter_handle)
        except:
            return {'__all__': 'User with this Twitter user does not exist.'}

        return {}

class PersonResource(ModelResource):
    """ Displaying all the Persons """        
    class Meta:
        queryset = Person.objects.all()
        allowed_methods = ['get', 'post']
        detail_uri_name = 'twitter_handle'
        validation = PersonValidation()
        authorization = Authorization()
        authentictation = Authentication()
        excludes = ['id', 'klout_score', 'tweet_score']

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<twitter_handle>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def obj_create(self, bundle, **kwargs):
        twitter_handle = bundle.data['twitter_handle']
        try:
            person = Person.objects.get(twitter_handle=twitter_handle)
        except Person.DoesNotExist:
            pass
        else:
            raise ImmediateHttpResponse(HttpResponseRedirect("/api/v1/person/%s/" % person.twitter_handle))

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
        authentication = Authentication()
        authorization = Authorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
        
    def dehydrate(self, bundle):
        twitter_user = get_twitter_user(bundle.data['username'])
        if twitter_user is not None:
            bundle.data['mugshot'] = twitter_user.profile_image_url.replace('_normal', '')
        else:
            bundle.data['mugshot'] = None
        return bundle

#
# Connection
#
class ConnectionValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'At least supply us with the person.'}
        if 'person' not in bundle.data:
            return {'__all__': 'At least supply us with the person.'}

        if request.method == "POST":
            person = bundle.data['person'].split('/')[-2]

            try:
                Person.objects.get(twitter_handle=person)
            except Person.DoesNotExist:
                return {'__all__': 'Person does not exist in our database.'}
        return {}

class AuthenticatedPostAuthentication(ApiKeyAuthentication):
    def is_authenticated(self, request, **kwargs):
        """ If POST, don't check auth, otherwise fall back to parent """
        if request.method == "GET":
            return True
        else:
            return super(ApiKeyAuthentication, self).is_authenticated(request, **kwargs)
            
class ConnectionResource(ModelResource):
    """ Displaying all the connections """
    person = fields.ForeignKey(PersonResource, 'person', full=True, blank=True)
    requested_by = fields.ForeignKey(UserResource, 'requested_by', blank=True, full=True)
    responded_by = fields.ForeignKey(UserResource, 'responded_by', blank=True, null=True)
    
    class Meta:
        queryset = Connection.objects.all()
        allowed_methods = ['get', 'post', 'patch', 'put']
        authentication = Authentication()
        authorization = Authorization()
        validation = ConnectionValidation()
        filtering = {
            'status': ALL,
        }
    
    def obj_create(self, bundle, **kwargs):
        bundle.data['requested_by'] = u'/api/v1/user/%s/' % bundle.request.user
        person = bundle.data['person'].split('/')[-2]

        try:
            con = Connection.objects.get(requested_by=bundle.request.user,
                                         person__twitter_handle=person)
        except Connection.DoesNotExist: pass
        else:
            raise ImmediateHttpResponse(HttpResponseRedirect("/api/v1/connection/%s/" % con.id))
        
        return super(ConnectionResource, self).obj_create(bundle,
                                                          **kwargs)

class YourConnectionResource(ModelResource):
    """ Displaying all the connections """
    person = fields.ForeignKey(PersonResource, 'person', full=True, blank=True)
    requested_by = fields.ForeignKey(UserResource, 'requested_by', blank=True, full=True)
    responded_by = fields.ForeignKey(UserResource, 'responded_by', blank=True, null=True)
    
    class Meta:
        queryset = Connection.objects.all()
        allowed_methods = ['get', 'post']
        authentication = Authentication()
        authorization = Authorization()
        
