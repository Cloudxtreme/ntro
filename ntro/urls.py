from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse

from tastypie.api import Api

from connection.api.resources import ConnectionResource, PersonResource, UserResource, YourConnectionResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ConnectionResource())
v1_api.register(YourConnectionResource())
v1_api.register(PersonResource())

def ping(request):
    return HttpResponse("pong", content_type="text/plain")

urlpatterns = patterns('',
    url(r'', include('social_auth.urls')),
    url(r'^ping$', ping),
    url('^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^$',
        TemplateView.as_view(template_name="index.html"),
        name="index"),
)

# Add media and static files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
