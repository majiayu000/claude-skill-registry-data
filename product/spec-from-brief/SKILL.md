---
name: spec-from-brief
description: Utiliser quand l'utilisateur fournit un brief flou de fonctionnalité et veut une spec testable et exhaustive. Produit une user story INVEST, un scénario nominal Given/When/Then, des scénarios annexes et la liste des questions business non tranchées.
version: 0.1.0
author: Ludovic Lefebvre
license: MIT
language: fr
book:
  title: Le Product Manager Augmenté
  annex: A3
tags: [spec, refinement, invest, given-when-then]
---

# spec-from-brief

## Fiche éditoriale

**Objectif.** Transformer un brief flou en spec testable et exhaustive.

**Entrées.** Brief initial, base documentaire produit.

**Sorties.** User story INVEST, scénario nominal Given/When/Then, scénarios annexes, questions business non tranchées.

**Cadence d'usage.** À chaque nouvelle fonctionnalité spécifiée.

## Mode opératoire

### Quand m'invoquer

L'utilisateur me fournit un brief texte (mail, slack, paragraphe de roadmap) et demande de le transformer en spec, ou évoque un besoin de "passer du brief à la story", ou demande une spec INVEST.

### Procédure

1. Lire le brief en entier sans interpréter.
2. Identifier l'**utilisateur cible** (rôle, contexte d'usage) ; si absent, l'inscrire en question business non tranchée.
3. Identifier le **bénéfice attendu** ; si absent, idem.
4. Reformuler en user story au format `En tant que <rôle>, je veux <action> afin de <bénéfice>`.
5. Tester la story contre INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable). Pour chaque lettre, dire si elle est tenue ; sinon dire pourquoi.
6. Construire le scénario nominal au format Given/When/Then.
7. Lister les scénarios annexes : cas limites, états système particuliers, erreurs prévisibles. Chacun en Given/When/Then.
8. Lister les **questions business non tranchées** : ambiguïtés du brief, choix de produit qui doivent être arbitrés avant la mise en chantier.
9. Produire la sortie au format ci-dessous.

### Format de sortie

```markdown
# Spec — {titre court de la fonctionnalité}

## User story (INVEST)

> En tant que {rôle}, je veux {action} afin de {bénéfice}.

**Test INVEST**
- Independent : {oui / non — explication}
- Negotiable : {oui / non — explication}
- Valuable : {oui / non — explication}
- Estimable : {oui / non — explication}
- Small : {oui / non — explication}
- Testable : {oui / non — explication}

## Scénario nominal

```
Given {prérequis}
When {action utilisateur}
Then {résultat observable}
```

## Scénarios annexes

### {nom du scénario annexe 1}
```
Given ...
When ...
Then ...
```

### {nom du scénario annexe 2}
...

## Questions business non tranchées

1. {question}
2. {question}
```

### Garde-fous

- Si une information manque dans le brief, **ne pas l'inventer**. Inscrire la question dans la section "Questions business non tranchées".
- Si la user story échoue clairement à un test INVEST (par ex. trop grosse pour être Small), dire explicitement laquelle découper plutôt que produire une fausse spec.
- Ne jamais produire de spec définitive en un coup quand le brief mentionne plusieurs fonctionnalités : proposer un découpage en plusieurs stories et demander quelle traiter en priorité.
- Pas d'estimation d'effort (jours, points). C'est le rôle de l'équipe en refinement.

### Exemple

**Input** :
> "On a besoin que les power users puissent exporter leurs dashboards. C'est urgent, on a perdu deux deals la semaine dernière."

**Output (résumé)** :

```markdown
# Spec — Export de dashboard pour power users

## User story (INVEST)
> En tant qu'utilisateur power, je veux exporter un dashboard afin de le partager hors de la plateforme.

**Test INVEST**
- Independent : oui
- Negotiable : oui
- Valuable : oui (perte de deals confirmée)
- Estimable : non — format d'export pas tranché
- Small : à confirmer selon les formats retenus
- Testable : oui une fois les formats tranchés

## Scénario nominal
```
Given un utilisateur power authentifié sur un dashboard qu'il possède
When il clique sur "Exporter"
Then un fichier est téléchargé localement dans le format choisi
```

## Questions business non tranchées
1. Quels formats d'export ? PDF, PNG, CSV, JSON ?
2. "Power user" est-il un rôle existant ou à créer ?
3. Faut-il auditer les exports (qui a exporté quoi quand) ?
4. Périmètre : un seul dashboard, plusieurs, tous ?
```

---

*Skill de l'Annexe 3 du livre [Le Product Manager Augmenté](../../README.fr.md). Voir [docs/livre.md](../../docs/livre.md) — chapitre 7.*
