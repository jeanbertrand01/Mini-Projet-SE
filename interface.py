"""Interface graphique PyQt6 du système expert ANIMAL."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QGroupBox, QLabel, QComboBox, QPushButton, QCheckBox,
    QTextEdit, QMessageBox, QScrollArea, QSplitter
)
from regles import CARACTERISTIQUES, ANIMAUX, NOMS_FAITS
from moteur import resoudre


class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Système expert ANIMAL")
        self.resize(1050, 760)
        self.checkboxes = {}
        self._construire_interface()

    def _construire_interface(self):
        central = QWidget()
        principal = QVBoxLayout(central)

        titre = QLabel("Système expert ANIMAL")
        titre.setStyleSheet("font-size: 24px; font-weight: bold;")
        sous_titre = QLabel(
            "Sélectionnez les caractéristiques connues, puis choisissez une méthode de raisonnement."
        )
        sous_titre.setWordWrap(True)
        principal.addWidget(titre)
        principal.addWidget(sous_titre)

        commandes = QHBoxLayout()
        commandes.addWidget(QLabel("Méthode :"))
        self.methode = QComboBox()
        self.methode.addItem("Chaînage avant", "avant")
        self.methode.addItem("Chaînage arrière", "arriere")
        self.methode.addItem("Chaînage mixte", "mixte")
        self.methode.currentIndexChanged.connect(self._maj_objectif)
        commandes.addWidget(self.methode, 1)

        commandes.addWidget(QLabel("Objectif :"))
        self.objectif = QComboBox()
        for cle, nom in ANIMAUX.items():
            self.objectif.addItem(nom, cle)
        commandes.addWidget(self.objectif, 1)
        principal.addLayout(commandes)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        groupe_faits = QGroupBox("Caractéristiques observées")
        faits_layout = QVBoxLayout(groupe_faits)
        aide = QLabel(
            "Cochez uniquement les propriétés vraies. Pour indiquer explicitement qu'un animal ne vole pas, "
            "cochez la case « Ne vole pas » ci-dessous. Une case non cochée reste inconnue."
        )
        aide.setWordWrap(True)
        faits_layout.addWidget(aide)

        zone_defilante = QScrollArea()
        zone_defilante.setWidgetResizable(True)
        contenu = QWidget()
        grille = QGridLayout(contenu)

        for index, (cle, libelle) in enumerate(CARACTERISTIQUES):
            cb = QCheckBox(libelle)
            self.checkboxes[cle] = cb
            grille.addWidget(cb, index, 0)

        self.ne_vole_pas = QCheckBox("L'animal ne vole pas (négation explicite)")
        self.ne_vole_pas.toggled.connect(self._negation_vol)
        grille.addWidget(self.ne_vole_pas, len(CARACTERISTIQUES), 0)

        zone_defilante.setWidget(contenu)
        faits_layout.addWidget(zone_defilante)
        splitter.addWidget(groupe_faits)

        groupe_resultats = QGroupBox("Résultats et explication")
        resultat_layout = QVBoxLayout(groupe_resultats)
        self.resume = QLabel("Les résultats apparaîtront ici.")
        self.resume.setWordWrap(True)
        self.resume.setStyleSheet("font-size: 15px; font-weight: bold;")
        resultat_layout.addWidget(self.resume)
        self.sortie = QTextEdit()
        self.sortie.setReadOnly(True)
        resultat_layout.addWidget(self.sortie)
        splitter.addWidget(groupe_resultats)
        splitter.setSizes([430, 570])
        principal.addWidget(splitter, 1)

        boutons = QHBoxLayout()
        analyser = QPushButton("Lancer le raisonnement")
        analyser.clicked.connect(self._analyser)
        effacer = QPushButton("Effacer")
        effacer.clicked.connect(self._effacer)
        exemple = QPushButton("Charger l'exemple guépard")
        exemple.clicked.connect(self._exemple_guepard)
        boutons.addWidget(analyser)
        boutons.addWidget(exemple)
        boutons.addWidget(effacer)
        principal.addLayout(boutons)

        self.setCentralWidget(central)
        self._maj_objectif()

    def _negation_vol(self, coche):
        if coche:
            self.checkboxes["vole"].blockSignals(True)
            self.checkboxes["vole"].setChecked(False)
            self.checkboxes["vole"].blockSignals(False)

    def _maj_objectif(self):
        arriere = self.methode.currentData() == "arriere"
        self.objectif.setEnabled(arriere or self.methode.currentData() == "mixte")

    def _collecter_faits(self):
        faits = {}
        for cle, cb in self.checkboxes.items():
            if cb.isChecked():
                faits[cle] = True
        if self.ne_vole_pas.isChecked():
            faits["vole"] = False
        return faits

    def _analyser(self):
        faits = self._collecter_faits()
        methode = self.methode.currentData()
        objectif = self.objectif.currentData() if methode in ("arriere", "mixte") else None

        if methode == "arriere" and not faits:
            QMessageBox.information(
                self, "Aucun fait", "Renseignez au moins une caractéristique avant de vérifier un objectif."
            )
            return

        try:
            resultat = resoudre(faits, methode, objectif)
        except Exception as exc:
            QMessageBox.critical(self, "Erreur", str(exc))
            return

        if methode == "arriere":
            nom = ANIMAUX[objectif]
            etat = "DÉMONTRÉ" if resultat.objectif_demontre else "NON DÉMONTRÉ"
            self.resume.setText(f"Objectif : {nom} — {etat}")
        elif resultat.animaux:
            noms = ", ".join(ANIMAUX[a] for a in resultat.animaux)
            self.resume.setText(f"Animal(s) identifié(s) : {noms}")
        else:
            self.resume.setText("Aucun animal précis n'a pu être identifié avec les faits fournis.")

        lignes = ["FAITS SAISIS"]
        if faits:
            lignes.extend(f"• {NOMS_FAITS.get(k, k)} : {'vrai' if v else 'faux'}"
                          for k, v in faits.items())
        else:
            lignes.append("• Aucun fait saisi")
        lignes += ["", "TRACE DU RAISONNEMENT", "-" * 45]
        lignes.extend(resultat.trace)
        lignes += ["", "FAITS DÉDUITS / CONNUS", "-" * 45]
        for cle, valeur in resultat.faits.items():
            lignes.append(f"• {NOMS_FAITS.get(cle, cle)} : {'vrai' if valeur else 'faux'}")
        self.sortie.setPlainText("\n".join(lignes))

    def _effacer(self):
        for cb in self.checkboxes.values():
            cb.setChecked(False)
        self.ne_vole_pas.setChecked(False)
        self.sortie.clear()
        self.resume.setText("Les résultats apparaîtront ici.")

    def _exemple_guepard(self):
        self._effacer()
        for cle in ("a_poils", "mange_viande", "couleur_brune", "taches_sombres"):
            self.checkboxes[cle].setChecked(True)
        self.methode.setCurrentIndex(0)
        self._analyser()


def lancer():
    app = QApplication([])
    fenetre = FenetrePrincipale()
    fenetre.show()
    app.exec()
