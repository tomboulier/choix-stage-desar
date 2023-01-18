# CSAR: Choix des Stages en Anesthésie-Réanimation

[![Django CI](https://github.com/tomboulier/csar/actions/workflows/django.yml/badge.svg)](https://github.com/tomboulier/csar/actions/workflows/django.yml)

Une webapp permettant de choisir les stages en anesthésie-réanimation.

## Installation
Il est fortement recommandé d'utiliser un environnement virtuel :

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

La base de données se crée avec la commande suivante :

```
cd csar
python manage.py migrate
```

## Utilisation

### Lancer le serveur

Dans le dossier `csar/`, lancer simplement la commande suivante :

```
python manage.py runserver
```

L'app est alors disponible à l'adresse [http://127.0.0.1:8000/csar](http://127.0.0.1:8000/choix).

### Panneau d'administration

Le panneau d'administration est accessible depuis l'accueil, mais aussi directement à l'adresse [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).
Mais avant cela, il faut créer un compte administrateur avec la commande suivante :

```
python manage.py createsuperuser
```
