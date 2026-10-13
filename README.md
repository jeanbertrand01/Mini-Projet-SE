# Système expert ANIMAL

Mini-projet de système expert en Python avec PyQt6. La base de connaissances contient les 15 règles R1 à R15 de classification animale. Le moteur implémente le chaînage avant, arrière et mixte.

## Prérequis

- Python 3.10 ou supérieur
- pip

## Installation

Dans un terminal, placez-vous dans le dossier du projet puis créez un environnement virtuel.

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si PowerShell bloque l'activation, vous pouvez lancer directement :
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Lancer l'application

```bash
python main.py
```

## Lancer les tests

```bash
pytest -q
```

## Utilisation

1. Cochez les caractéristiques dont vous savez qu'elles sont vraies.
2. Pour affirmer que l'animal ne vole pas, cochez « L'animal ne vole pas ». Une case non cochée signifie « inconnu », pas « faux ».
3. Choisissez une méthode :
   - **Chaînage avant** : déduit tous les faits atteignables.
   - **Chaînage arrière** : vérifie l'objectif sélectionné en remontant les règles.
   - **Chaînage mixte** : effectue le chaînage avant puis vérifie l'objectif par chaînage arrière.
4. Cliquez sur « Lancer le raisonnement ».
5. Consultez le résumé et la trace pour comprendre quelles règles ont été utilisées.

Le bouton « Charger l'exemple guépard » préremplit les caractéristiques d'un exemple et lance le chaînage avant.

## Structure

- `regles.py` : les 15 règles et les libellés affichés.
- `moteur.py` : les algorithmes d'inférence et la trace d'explication.
- `interface.py` : l'interface PyQt6.
- `main.py` : point d'entrée.
- `tests/test_moteur.py` : tests unitaires.

## Limites du modèle

- Le système raisonne uniquement à partir des règles fournies ; il ne remplace pas un diagnostic zoologique.
- Une conclusion non démontrée n'est pas nécessairement fausse : il peut manquer des informations.
- Le moteur traite les conditions négatives uniquement quand la propriété est explicitement connue comme fausse.
- Les règles R9 à R15 sont appliquées telles qu'elles sont fournies dans l'énoncé, même si elles simplifient la classification réelle des animaux.
