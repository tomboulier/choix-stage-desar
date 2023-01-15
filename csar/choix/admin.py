from django.contrib import admin

from .models import Interne, Stage

admin.site.register(Interne)
admin.site.register(Stage)

admin.site.site_url = "/choix"