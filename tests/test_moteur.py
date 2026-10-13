import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from moteur import chainage_avant, chainage_arriere, chainage_mixte


def test_guepard_par_chainage_avant():
    faits = {
        "a_poils": True,
        "mange_viande": True,
        "couleur_brune": True,
        "taches_sombres": True,
    }
    resultat = chainage_avant(faits)
    assert resultat.faits["mammifere"] is True
    assert resultat.faits["carnivore"] is True
    assert "guepard" in resultat.animaux


def test_girafe():
    faits = {
        "a_poils": True,
        "a_sabots": True,
        "long_cou": True,
        "longues_pattes": True,
        "taches_sombres": True,
    }
    resultat = chainage_avant(faits)
    assert "girafe" in resultat.animaux


def test_autruche_necessite_negation_explicite():
    faits = {
        "a_plumes": True,
        "vole": False,
        "long_cou": True,
        "longues_pattes": True,
        "noir_blanc": True,
    }
    resultat = chainage_avant(faits)
    assert "autruche" in resultat.animaux


def test_inconnu_ne_signifie_pas_faux():
    faits = {
        "a_plumes": True,
        "long_cou": True,
        "longues_pattes": True,
        "noir_blanc": True,
    }
    resultat = chainage_avant(faits)
    assert "autruche" not in resultat.animaux


def test_chainage_arriere_guepard():
    faits = {
        "a_poils": True,
        "mange_viande": True,
        "couleur_brune": True,
        "taches_sombres": True,
    }
    resultat = chainage_arriere(faits, "guepard")
    assert resultat.objectif_demontre is True


def test_mixte():
    faits = {
        "a_poils": True,
        "mange_viande": True,
        "couleur_brune": True,
        "taches_sombres": True,
    }
    resultat = chainage_mixte(faits, "guepard")
    assert resultat.objectif_demontre is True
    assert "guepard" in resultat.animaux
