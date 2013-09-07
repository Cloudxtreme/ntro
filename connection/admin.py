from django.contrib import admin

from connection.models import Person, Connection

class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('requested_by', 'person', 'price')

admin.site.register(Person)
admin.site.register(Connection, ConnectionAdmin)
