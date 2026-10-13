"""Base de connaissances ANIMAL : règles R1 à R15."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Regle:
    nom: str
    conditions: Tuple[Tuple[str, bool], ...]
    conclusion: str
    description: str


REGLES = [
    Regle("R1", (("a_poils", True),), "mammifere",
          "Un animal à poils est un mammifère."),
    Regle("R2", (("donne_lait", True),), "mammifere",
          "Un animal qui donne du lait est un mammifère."),
    Regle("R3", (("a_plumes", True),), "oiseau",
          "Un animal à plumes est un oiseau."),
    Regle("R4", (("vole", True), ("pond_oeufs", True)), "oiseau",
          "Un animal qui vole et pond des œufs est un oiseau."),
    Regle("R5", (("mange_viande", True),), "carnivore",
          "Un animal qui mange de la viande est carnivore."),
    Regle("R6", (("dents_pointues", True), ("griffes", True),
                  ("yeux_devant", True)), "carnivore",
          "Dents pointues, griffes et yeux dirigés vers l'avant indiquent un carnivore."),
    Regle("R7", (("mammifere", True), ("a_sabots", True)), "ongule",
          "Un mammifère à sabots est un ongulé."),
    Regle("R8", (("mammifere", True), ("rumine", True)), "ongule",
          "Un mammifère qui rumine est un ongulé."),
    Regle("R9", (("mammifere", True), ("carnivore", True),
                  ("couleur_brune", True), ("taches_sombres", True)),
          "guepard", "Mammifère carnivore brun à taches sombres : guépard."),
    Regle("R10", (("mammifere", True), ("carnivore", True),
                   ("couleur_brune", True), ("raies_noires", True)),
          "tigre", "Mammifère carnivore brun à raies noires : tigre."),
    Regle("R11", (("ongule", True), ("long_cou", True),
                   ("longues_pattes", True), ("taches_sombres", True)),
          "girafe", "Ongulé à long cou, longues pattes et taches sombres : girafe."),
    Regle("R12", (("ongule", True), ("raies_noires", True)), "zebre",
          "Un ongulé à raies noires est un zèbre."),
    Regle("R13", (("oiseau", True), ("vole", False), ("long_cou", True),
                   ("longues_pattes", True), ("noir_blanc", True)),
          "autruche", "Oiseau qui ne vole pas, à long cou, longues pattes et plumage noir et blanc : autruche."),
    Regle("R14", (("oiseau", True), ("vole", False), ("nage", True),
                   ("noir_blanc", True)),
          "pingouin", "Oiseau qui ne vole pas, nage et est noir et blanc : pingouin."),
    Regle("R15", (("oiseau", True), ("vole_bien", True)), "albatros",
          "Un oiseau qui vole bien est un albatros."),
]

NOMS_FAITS = {
    "a_poils": "a des poils",
    "donne_lait": "donne du lait",
    "a_plumes": "a des plumes",
    "vole": "vole",
    "pond_oeufs": "pond des œufs",
    "mange_viande": "mange de la viande",
    "dents_pointues": "a des dents pointues",
    "griffes": "a des griffes",
    "yeux_devant": "a les yeux dirigés vers l'avant",
    "mammifere": "est un mammifère",
    "a_sabots": "a des sabots",
    "rumine": "rumine",
    "carnivore": "est carnivore",
    "couleur_brune": "est de couleur brune",
    "taches_sombres": "a des taches sombres",
    "raies_noires": "a des raies noires",
    "ongule": "est un ongulé",
    "long_cou": "a un long cou",
    "longues_pattes": "a de longues pattes",
    "oiseau": "est un oiseau",
    "noir_blanc": "est noir et blanc",
    "nage": "nage",
    "vole_bien": "vole bien",
    "guepard": "est un guépard",
    "tigre": "est un tigre",
    "girafe": "est une girafe",
    "zebre": "est un zèbre",
    "autruche": "est une autruche",
    "pingouin": "est un pingouin",
    "albatros": "est un albatros",
}

ANIMAUX = {
    "guepard": "Guépard",
    "tigre": "Tigre",
    "girafe": "Girafe",
    "zebre": "Zèbre",
    "autruche": "Autruche",
    "pingouin": "Pingouin",
    "albatros": "Albatros",
}

# Les propriétés directement demandées à l'utilisateur.
CARACTERISTIQUES = [
    ("a_poils", "L'animal a des poils"),
    ("donne_lait", "L'animal donne du lait"),
    ("a_plumes", "L'animal a des plumes"),
    ("vole", "L'animal vole"),
    ("pond_oeufs", "L'animal pond des œufs"),
    ("mange_viande", "L'animal mange de la viande"),
    ("dents_pointues", "L'animal a des dents pointues"),
    ("griffes", "L'animal a des griffes"),
    ("yeux_devant", "L'animal a les yeux dirigés vers l'avant"),
    ("a_sabots", "L'animal a des sabots"),
    ("rumine", "L'animal rumine"),
    ("couleur_brune", "L'animal est de couleur brune"),
    ("taches_sombres", "L'animal a des taches sombres"),
    ("raies_noires", "L'animal a des raies noires"),
    ("long_cou", "L'animal a un long cou"),
    ("longues_pattes", "L'animal a de longues pattes"),
    ("noir_blanc", "L'animal est noir et blanc"),
    ("nage", "L'animal nage"),
    ("vole_bien", "L'animal vole bien"),
]
