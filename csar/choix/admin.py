from django.contrib import admin
from django.apps import apps

# ajout de tous les 'models' de l'app 'choix' dans le panneau d'administration
app = apps.get_app_config('choix')
for model_name, model in app.models.items():
    admin.site.register(model)

admin.site.site_url = "/choix"