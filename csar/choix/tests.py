from django.test import TestCase

from .models import Interne, Stage, Choix


class StageModelsTests(TestCase):
    stage_trimestre = Stage(intitule="stage 3 mois", duree="trimestre")
    stage_semestre = Stage(intitule="stage 6 mois", duree="semestre")

    def test_duree_en_mois(self):
        self.assertEqual(self.stage_trimestre.duree_en_mois(), 3)
        self.assertEqual(self.stage_semestre.duree_en_mois(), 6)

    def test_compte_nombre_postes_disponibles(self):
        stage = Stage.objects.create(intitule="stage", nombre_postes_ouverts=3)
        interne1 = Interne.objects.create(prenom="Interne", nom="1")
        interne2 = Interne.objects.create(prenom="Interne", nom="2")

        # interne 1 et 2 choisissent tous les deux le stage
        Choix.objects.create(interne=interne1, stage=stage)
        Choix.objects.create(interne=interne2, stage=stage)
        self.assertEqual(stage.nombre_postes_disponibles(), 1)


class ChoixModelsTests(TestCase):
    def test_relation_plusieurs_a_plusieurs(self):
        """
        On vérifie dans ce jeu de tests qu'on peut bel et avoir plusieurs internes
        dans un même stage, et qu'un interne peut choisir plusieurs stages.
        """
        stage1 = Stage.objects.create(intitule="stage 1")
        stage2 = Stage.objects.create(intitule="stage 2")
        interne1 = Interne.objects.create(prenom="Interne", nom="1")
        interne2 = Interne.objects.create(prenom="Interne", nom="2")

        # l'interne 1 choix le stage 1 et le stage 2
        interne1.stages.add(stage1)
        interne1.stages.add(stage2)
        # on vérifie qu'il y a bien 2 stages associés à l'interne 1
        self.assertEqual(interne1.stages.all().count(), 2)

        # l'interne 2 choisit aussi le stage 1
        interne2.stages.add(stage1)

        # on vérifie que les deux internes sont dans le stage 1
        self.assertIn(interne1, stage1.interne_set.all())
        self.assertIn(interne2, stage1.interne_set.all())
