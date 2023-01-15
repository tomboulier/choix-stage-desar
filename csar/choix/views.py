from django.shortcuts import render

from .models import Stage


def index(request):
    liste_stages = Stage.objects.all()
    context = {'liste_stages': liste_stages}
    return render(request, 'choix/index.html', context=context)
