from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Interne, Stage


def index(request, error_message=None):
    liste_stages = Stage.objects.all().order_by("intitule")
    context = {'liste_stages': liste_stages}
    if error_message is not None:
        context['error_message'] = error_message
    return render(request, 'choix/index.html', context=context)


def choix_interne(request, interne_uuid):
    """
    Page associée à un interne, qui peut se retrouver via son uuid.
    On y affiche seulement les stages disponibles, pour qu'il fasse son choix.
    """
    try:
        interne = get_object_or_404(Interne, uuid=interne_uuid)

    except MultipleObjectsReturned:  # si plusieurs internes ont le même uuid
        return index(request, error_message="Erreur: plusieurs internes ont le même identifiant unique")

    # pour l'affichage de l'interne
    liste_stages = Stage.objects.est_disponible().order_by("intitule")
    context = {'interne': interne,
               'liste_stages': liste_stages}
    return render(request, 'choix/interne.html', context)
