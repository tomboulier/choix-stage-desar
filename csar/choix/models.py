from django.db import models


class Interne(models.Model):
    """
    Classe faisant référence à un interne. Contient les informations basiques
    d'identité mais également de contact (pour la messagerie).

    Attributs :
        - nom
        - prenom
        - mail
        - telephone
    """
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)

    def __str__(self):
        return self.prenom + ' ' + self.nom


class Stage(models.Model):
    """
    Classe faisant référence à un stage. À noter qu'il peut exister plusieurs
    stages ayant le même nom (par exemple, "Anesthésie pédiatrique premier trimestre").

    Attributs:
        - interne : l'interne ayant choisi le stage (est égal à NULL tant que pas de choix)
        - intitule : l'intitulé du stage, exemple "Bloc des urgences deuxième trimestre"
        - duree : la durée du stage (peut être égale seulement à "3 mois" ou "6 mois")
    Méthodes :
        - duree_en_mois : la durée du stage, exprimée en mois (peut être égale seulement à 3 ou 6)
    """
    interne = models.ForeignKey(
        to=Interne,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    intitule = models.CharField(max_length=200)

    DUREES_STAGES_EN_MOIS = [
        ('trimestre', '3 mois'),
        ('semestre', '6 mois'),
    ]

    duree = models.CharField(
        max_length=9,
        choices=DUREES_STAGES_EN_MOIS
    )

    def duree_en_mois(self):
        """
        Retourne la durée, exprimée en mois, sous forme d'entier
        """
        if self.duree == 'trimestre':
            return 3
        if self.duree == 'semestre':
            return 6
        raise Exception("l'attribut 'duree' de 'Stage' ne peut être que 'trimestre' ou 'semestre'")

    def __str__(self):
        return self.intitule
