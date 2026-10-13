"""Moteur d'inférence avec chaînage avant, arrière et mixte."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from regles import REGLES, NOMS_FAITS, ANIMAUX, Regle


@dataclass
class Resultat:
    faits: Dict[str, bool]
    trace: List[str] = field(default_factory=list)
    animaux: List[str] = field(default_factory=list)
    objectif_demontre: Optional[bool] = None


def nom_fait(fait: str, valeur: bool = True) -> str:
    texte = NOMS_FAITS.get(fait, fait.replace("_", " "))
    return texte if valeur else f"ne {texte}"


def conditions_satisfaites(regle: Regle, faits: Dict[str, bool]) -> bool:
    """Une règle s'active seulement si toutes ses conditions sont connues et vraies/fausses comme attendu."""
    return all(fait in faits and faits[fait] is valeur
               for fait, valeur in regle.conditions)


def conditions_contradictoires(regle: Regle, faits: Dict[str, bool]) -> bool:
    """Vrai si au moins une condition connue contredit la règle."""
    return any(fait in faits and faits[fait] is not valeur
               for fait, valeur in regle.conditions)


def chainage_avant(faits_initiaux: Dict[str, bool]) -> Resultat:
    faits = dict(faits_initiaux)
    trace = [f"Faits initiaux : {', '.join(nom_fait(k, v) for k, v in faits.items()) or 'aucun fait renseigné'}."]

    changement = True
    while changement:
        changement = False
        for regle in REGLES:
            if regle.conclusion in faits:
                continue
            if conditions_satisfaites(regle, faits):
                faits[regle.conclusion] = True
                details = " ET ".join(nom_fait(k, v) for k, v in regle.conditions)
                trace.append(
                    f"{regle.nom} déclenchée : SI {details}, ALORS "
                    f"{nom_fait(regle.conclusion)}. {regle.description}"
                )
                changement = True

    animaux = [cle for cle in ANIMAUX if faits.get(cle) is True]
    trace.append("Arrêt : aucun nouveau fait ne peut être déduit.")
    return Resultat(faits=faits, trace=trace, animaux=animaux)


def chainage_arriere(faits_initiaux: Dict[str, bool], objectif: str) -> Resultat:
    """Vérifie un objectif en recherchant récursivement les règles qui le concluent."""
    faits = dict(faits_initiaux)
    trace: List[str] = []
    pile: Set[str] = set()

    def prouver(but: str, profondeur: int = 0) -> bool:
        prefixe = "  " * profondeur
        if but in faits:
            valeur = faits[but]
            trace.append(f"{prefixe}Fait connu : {nom_fait(but)} = {'vrai' if valeur else 'faux'}.")
            return valeur
        if but in pile:
            trace.append(f"{prefixe}Cycle détecté pendant la recherche de {nom_fait(but)}.")
            return False

        regles_cibles = [r for r in REGLES if r.conclusion == but]
        if not regles_cibles:
            trace.append(f"{prefixe}Aucune règle ne permet de démontrer {nom_fait(but)}.")
            return False

        pile.add(but)
        trace.append(f"{prefixe}Objectif : démontrer « {nom_fait(but)} ». "
                      f"{len(regles_cibles)} règle(s) candidate(s).")

        for regle in regles_cibles:
            trace.append(f"{prefixe}Essai de {regle.nom} : {regle.description}")
            valide = True
            for premisse, valeur_attendue in regle.conditions:
                if premisse in faits and faits[premisse] is not valeur_attendue:
                    trace.append(f"{prefixe}  Échec : {nom_fait(premisse)} contredit la condition.")
                    valide = False
                    break
                if premisse not in faits:
                    if valeur_attendue is False:
                        # La négation n'est prouvée que si la propriété est explicitement fausse.
                        trace.append(f"{prefixe}  Condition négative inconnue : "
                                     f"il faut savoir que {nom_fait(premisse)} est faux.")
                        valide = False
                        break
                    if not prouver(premisse, profondeur + 1):
                        valide = False
                        break
            if valide:
                faits[but] = True
                trace.append(f"{prefixe}{regle.nom} réussie : {nom_fait(but)} est démontré.")
                pile.remove(but)
                return True

        pile.remove(but)
        trace.append(f"{prefixe}Échec : objectif « {nom_fait(but)} » non démontré.")
        return False

    demontre = prouver(objectif)
    animaux = [cle for cle in ANIMAUX if faits.get(cle) is True]
    trace.insert(0, f"Chaînage arrière : objectif demandé = {ANIMAUX.get(objectif, objectif)}.")
    return Resultat(faits=faits, trace=trace, animaux=animaux,
                    objectif_demontre=demontre)


def chainage_mixte(faits_initiaux: Dict[str, bool], objectif: Optional[str] = None) -> Resultat:
    """Déduit d'abord les faits accessibles, puis vérifie éventuellement un objectif par arrière."""
    avant = chainage_avant(faits_initiaux)
    trace = ["=== Phase 1 : chaînage avant ==="] + avant.trace
    faits = dict(avant.faits)
    demontre = None

    if objectif:
        trace.append("")
        trace.append("=== Phase 2 : vérification ciblée par chaînage arrière ===")
        arriere = chainage_arriere(faits, objectif)
        trace.extend(arriere.trace)
        faits.update(arriere.faits)
        demontre = arriere.objectif_demontre

    animaux = [cle for cle in ANIMAUX if faits.get(cle) is True]
    return Resultat(faits=faits, trace=trace, animaux=animaux,
                    objectif_demontre=demontre)


def resoudre(faits_initiaux: Dict[str, bool], methode: str,
             objectif: Optional[str] = None) -> Resultat:
    if methode == "avant":
        return chainage_avant(faits_initiaux)
    if methode == "arriere":
        if not objectif:
            raise ValueError("Le chaînage arrière nécessite un objectif.")
        return chainage_arriere(faits_initiaux, objectif)
    if methode == "mixte":
        return chainage_mixte(faits_initiaux, objectif)
    raise ValueError(f"Méthode inconnue : {methode}")
