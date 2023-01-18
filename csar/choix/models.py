from django.core.exceptions import ValidationError
from django.db import models
import uuid


class StageManager(models.Manager):
    """
    Manager personnalisé pour pouvoir filtrer les stages suivant leur disponibilité
    Sources :
    - question StackOverFlow : https://stackoverflow.com/questions/2276768/django-query-filtering-from-model-method
    - documentation Django : https://docs.djangoproject.com/en/4.0/topics/db/managers/
    """

    def est_disponible(self):
        """
        Retourne un QuerySet permettant de filtrer sur la disponibilité du stage.
        Ainsi, Stages.objects.est_disponible() renverra la liste de tous les stages
        disponibles.
        """
        stages = super().get_queryset().all()
        id_disponibles = [stage.id for stage in stages if stage.est_disponible()]
        return stages.filter(id__in=id_disponibles)


class Stage(models.Model):
    """
    Classe faisant référence à un stage. À noter qu'il peut exister plusieurs
    stages ayant le même nom (par exemple, "Anesthésie pédiatrique premier trimestre").

    Attributs:
        - intitule : l'intitulé du stage, exemple "Bloc des urgences deuxième trimestre"
        - duree : la durée du stage (peut être égale seulement à "3 mois" ou "6 mois")
        - nombre_postes_ouverts : le nombre de postes ouverts, c'est-à-dire au total (différent
        du nombre de postes disponibles, qui sera dans les méthodes)
    Méthodes :
        - duree_en_mois : la durée du stage, exprimée en mois (peut être égale seulement à 3 ou 6)
        - nombre_postes_disponibles : le nombre de poste qu'il reste après choix des internes
    """

    # Manager personnalisé, pour filtrer sur les stages disponibles via la méthode StageManager.est_disponible()
    objects = StageManager()

    # Fields
    intitule = models.CharField(max_length=200)
    DUREES_STAGES_EN_MOIS = [
        ('trimestre', '3 mois'),
        ('semestre', '6 mois'),
    ]
    duree = models.CharField(
        max_length=9,
        choices=DUREES_STAGES_EN_MOIS
    )
    nombre_postes_ouverts = models.IntegerField(default=0)

    def duree_en_mois(self):
        """
        Retourne la durée, exprimée en mois, sous forme d'entier
        """
        if self.duree == 'trimestre':
            return 3
        if self.duree == 'semestre':
            return 6
        raise Exception("l'attribut 'duree' de 'Stage' ne peut être que 'trimestre' ou 'semestre'")

    def nombre_postes_disponibles(self):
        """
        Le nombre de postes qu'il reste après choix des internes
        """
        return self.nombre_postes_ouverts - self.interne_set.all().count()

    def est_disponible(self):
        return self.nombre_postes_disponibles() > 0

    def __str__(self):
        return self.intitule


class Interne(models.Model):
    """
    Classe faisant référence à un interne. Contient les informations basiques
    d'identité mais également de contact (pour la messagerie).
    L'attribut "stage" est en relation "many-to-many" : un stage peut avoir plusieurs internes,
    et un interne peut choisir plusieurs stages (dans le cas des trimestres)

    Attributs :
        - nom, prenom, mail, et telephone : sont stockés sous forme de strings
        - stage : le stage choisi par l'interne
        - uuid: un identifiant unique (UUID = "universally unique identifier") qui permettra
            d'accéder à la page de l'interne sans mettre en clair dans l'URL la clé primaire
    """
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    stages = models.ManyToManyField(
        Stage,
        blank=True,
        through="Choix",
    )
    uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.prenom + ' ' + self.nom


class Choix(models.Model):
    """
    La classe intermédiaire permettant de définir la relation plusieurs-à-plusieurs
    entre la classe Interne et la classe Stage.
    https://docs.djangoproject.com/fr/4.1/topics/db/models/#extra-fields-on-many-to-many-relationships

    On définit une classe intermédiaire pour pouvoir mieux la visualiser dans le panneau
    d'administrateur, et ce grâce à la méthode __str__
    """
    interne = models.ForeignKey(Interne, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.interne} a choisi {self.stage}"

    class Meta:
        verbose_name_plural = "Choix"  # permet de ne pas afficher automatiquement "Choixs"
        # dans le panneau d'administration

    def clean(self):
        """
        La ré-écriture de cette méthode de base permet de valider qu'il reste des postes
        disponibles dans le stage au moment du choix.

        Cf. documentation de Django :
        https://docs.djangoproject.com/en/4.1/ref/models/instances/#django.db.models.Model.clean
        """
        if self.stage.nombre_postes_disponibles() == 0:
            raise ValidationError(f"Le stage {self.stage.intitule} n'a plus de poste disponible")
