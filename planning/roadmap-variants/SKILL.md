---
name: roadmap-variants
description: Utiliser à chaque révision trimestrielle de roadmap pour simuler trois variantes selon des hypothèses de capacité et de risque. Produit une variante prudente, une variante agressive, une variante équilibrée, comparées ligne à ligne.
version: 0.1.0
author: Ludovic Lefebvre
license: MIT
language: fr
book:
  title: Le Product Manager Augmenté
  annex: A3
tags: [roadmap, planning, quarterly, scenarios]
---

# roadmap-variants

## Fiche éditoriale

**Objectif.** Simuler trois variantes d'une roadmap selon des hypothèses de capacité et de risque.

**Entrées.** Roadmap actuelle, contraintes équipe, OKR cible.

**Sorties.** Variante prudente, variante agressive, variante équilibrée, comparées ligne à ligne.

**Cadence d'usage.** À chaque révision trimestrielle de roadmap.

## Mode opératoire

### Quand m'invoquer

L'utilisateur prépare une révision trimestrielle et veut tester des scénarios avant de figer la version finale. Il me fournit la roadmap actuelle (liste de sujets avec ordre et estimation rough), les contraintes équipe (capacité, congés, dépendances tech), et l'OKR cible.

### Procédure

1. **Reformuler les hypothèses** explicites de la roadmap actuelle (capacité supposée, ordre, dépendances assumées).
2. **Identifier 2-3 leviers** sur lesquels les variantes vont diverger : ordre des sujets, périmètre par sujet, parallélisation, coupe d'un sujet, ajout d'un sujet.
3. **Construire la variante prudente** : maximise les chances de tenir l'OKR à minima ; coupe le périmètre ambigu ; ne dépend de personne d'externe ; ne prend aucun risque tech non maîtrisé.
4. **Construire la variante agressive** : maximise l'impact si tout se passe bien ; assume des dépendances externes ; tente plus de sujets en parallèle ; accepte un risque de glissement si gain potentiel ≥ 2x.
5. **Construire la variante équilibrée** : posture par défaut ; arbitre entre les deux extrêmes ; couvre l'OKR avec marge réaliste.
6. **Tableau comparatif ligne à ligne** : un sujet par ligne, statut dans chaque variante (gardé / coupé / réduit / ajouté), ordre de priorité, risque associé.
7. **Recommandation argumentée** : laquelle des trois est la posture par défaut, et sous quelle condition basculer vers prudente ou agressive.

### Format de sortie

```markdown
# Roadmap — variantes pour {trimestre}

## OKR cible
{rappel de l'OKR}

## Hypothèses de capacité
- Effectif : {n} ETP
- Capacité produit-tech : ~{x} jours-homme sur le trimestre
- Risques connus : ...

## Leviers de différenciation des variantes
1. {levier 1}
2. {levier 2}
3. {levier 3}

## Tableau comparatif

| Sujet | Prudente | Équilibrée | Agressive | Risque associé |
|-------|----------|------------|-----------|----------------|
| {sujet 1} | gardé (P1) | gardé (P1) | gardé (P1) + scope étendu | ... |
| {sujet 2} | coupé | gardé (P2) | gardé (P1) en parallèle | dépendance équipe X |
| {sujet 3} | ... | ... | ... | ... |

## Variante prudente — {nom court}

**Périmètre** : ...
**Charge estimée** : {x}% de la capacité
**Probabilité de tenir l'OKR** : haute
**Probabilité de dépasser l'OKR** : faible
**Risques principaux** : ...

## Variante équilibrée — {nom court}

**Périmètre** : ...
**Charge estimée** : {x}% de la capacité
**Probabilité de tenir l'OKR** : moyenne-haute
**Probabilité de dépasser l'OKR** : moyenne
**Risques principaux** : ...

## Variante agressive — {nom court}

**Périmètre** : ...
**Charge estimée** : {x}% de la capacité (risque de saturation)
**Probabilité de tenir l'OKR** : moyenne
**Probabilité de dépasser l'OKR** : haute si tout va bien
**Risques principaux** : ...

## Recommandation

**Posture par défaut : {variante}.**

{2-3 phrases qui justifient.}

**Bascule vers prudente si** : {condition factuelle observable}
**Bascule vers agressive si** : {condition factuelle observable}
```

### Garde-fous

- **Pas plus de trois variantes** : multiplier les scénarios disperse la décision. La promesse est trois, pas cinq.
- **Pas d'invention de capacité** : si les contraintes équipe sont absentes ou floues, le signaler et utiliser des hypothèses prudentes par défaut.
- **Variante agressive ≠ wishlist** : elle reste dans les limites physiques de la capacité. Pas de "on fait tout en doublant la vélocité".
- **Variante prudente ≠ statu quo** : elle peut elle aussi couper des sujets attendus s'ils sont à risque.
- **Risque associé toujours nommé** : pas de variante sans risques signalés.
- **Pas de recommandation sans condition de bascule** : la posture par défaut s'accompagne toujours de critères qui justifieraient un revirement.

### Exemple

**Input** :
> Roadmap Q3 : refonte onboarding (P1, ~25j), feature export dashboard (P2, ~15j), multi-langue DE+ES (P3, ~20j). OKR : +20% conversion free→paid sur le trimestre. Capacité : 60 j-h. Contraintes : 1 dev en congé 3 semaines en juillet, dépendance design refonte.

**Output (extrait)** :

```markdown
# Roadmap — variantes pour Q3

## OKR cible
+20% conversion free→paid sur Q3.

## Tableau comparatif

| Sujet | Prudente | Équilibrée | Agressive | Risque |
|-------|----------|------------|-----------|--------|
| Refonte onboarding | gardé (P1) | gardé (P1) | gardé (P1) + A/B testing | dépendance design |
| Export dashboard | coupé | gardé (P2, scope réduit) | gardé (P2) | aucun |
| Multi-langue DE+ES | coupé | DE seulement (P3) | DE+ES (P3) | aucun |

## Variante prudente — "Onboarding only"
**Périmètre** : refonte onboarding seule, fenêtre confortable
**Charge estimée** : 60% de la capacité (35 j-h sur 60 j-h)
**Probabilité de tenir l'OKR** : haute si refonte onboarding livre ce qu'elle promet
**Probabilité de dépasser** : faible
**Risques** : si le levier conversion ne vient pas de l'onboarding, pas de plan B.

## Recommandation
**Posture par défaut : équilibrée.**
L'onboarding seul porte l'OKR mais sans filet ; ajouter export dashboard couvre un segment power user en parallèle ; DE seule limite le risque multi-langue.

**Bascule vers prudente si** : retard livrable design sur l'onboarding > 1 semaine.
**Bascule vers agressive si** : ajout d'un dev mi-juillet et capacité réelle > 70 j-h.
```

---

*Skill de l'Annexe 3 du livre [Le Product Manager Augmenté](../../README.fr.md). Voir [docs/livre.md](../../docs/livre.md) — chapitre 11.*
