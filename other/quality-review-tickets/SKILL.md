---
name: quality-review-tickets
description: Utiliser la veille de chaque cérémonie de refinement pour pré-réviser un ou plusieurs tickets de backlog. Produit un tableau des critères manquants par dimension, un test INVEST argumenté, des scénarios edge cases en Given/When/Then, et la liste des dépendances détectées.
version: 0.1.0
author: Ludovic Lefebvre
license: MIT
language: fr
book:
  title: Le Product Manager Augmenté
  annex: A3
tags: [refinement, quality, invest, ticket-review]
---

# quality-review-tickets

## Fiche éditoriale

**Objectif.** Produire la pré-revue qualité d'un ou plusieurs tickets de backlog avant cérémonie de refinement.

**Entrées.** URL ou contenu du ticket, base documentaire produit, glossaire métier.

**Sorties.** Tableau des critères manquants par dimension, test INVEST argumenté, scénarios edge cases en Given/When/Then, dépendances détectées.

**Cadence d'usage.** Veille de chaque refinement, sur l'ensemble des tickets prévus.

## Mode opératoire

### Quand m'invoquer

L'utilisateur prépare un refinement et veut pré-réviser les tickets pour identifier les manques avant la cérémonie. Il me passe le contenu (texte, URL, ou liste de tickets) et la base documentaire à laquelle se référer si besoin.

### Procédure

1. **Pour chaque ticket**, examiner sa qualité sur cinq dimensions :
   - **User story** présente et bien formée (En tant que / je veux / afin de).
   - **Critères d'acceptation** explicites et testables.
   - **Scénarios** au moins un nominal et idéalement un ou deux edge cases.
   - **Dépendances** identifiées (tickets liés, services tiers, données requises).
   - **Cas hors-scope** explicités.
2. **Tableau des manques** : sur chaque dimension, marquer présent / partiel / absent et préciser ce qui manque.
3. **Test INVEST** : pour chaque lettre, dire si elle est tenue (oui/non/partiel) et expliquer.
4. **Génération d'edge cases** : 2-3 scénarios edge en Given/When/Then que le ticket ne couvre pas explicitement.
5. **Dépendances détectées** : tickets potentiellement bloquants/bloqués, données nécessaires en amont, services tiers.
6. **Niveau de préparation** : prêt pour refinement / besoin de clarification / à découper.
7. Produire la sortie au format ci-dessous.

### Format de sortie

```markdown
# Pré-revue refinement — {date du refinement}

## Ticket {ID} — {titre}

### Tableau des manques par dimension

| Dimension | État | Manque |
|-----------|------|--------|
| User story | présent / partiel / absent | ... |
| Critères d'acceptation | ... | ... |
| Scénarios | ... | ... |
| Dépendances | ... | ... |
| Cas hors-scope | ... | ... |

### Test INVEST

- Independent : oui / non / partiel — {explication}
- Negotiable : ...
- Valuable : ...
- Estimable : ...
- Small : ...
- Testable : ...

### Edge cases manquants

```
Given {prérequis}
When {action}
Then {résultat}
```
```
Given {prérequis}
When {action}
Then {résultat}
```

### Dépendances détectées

- {ticket lié ou service tiers} — {nature de la dépendance}
- ...

### Niveau de préparation

**{prêt pour refinement | besoin de clarification | à découper}**

{1-2 phrases qui justifient.}

---

## Ticket {ID suivant} — {titre}
... (idem)

## Synthèse pour la cérémonie

- {n} tickets prêts
- {n} tickets nécessitant clarification : ID1, ID2
- {n} tickets à découper : ID3
```

### Garde-fous

- **Ne pas inventer de critère d'acceptation** absent du ticket. Pointer le manque, c'est différent de combler.
- **Edge cases plausibles** : ne pas générer des scénarios artificiels juste pour remplir. 2-3 edge cases pertinents valent mieux que 8 cas farfelus.
- **Pas d'estimation d'effort**. C'est le rôle de l'équipe en refinement.
- **Distinguer "manque" et "défaut"** : un ticket peut être minimaliste mais valide (story claire + 1 critère + 1 scénario) ; ce n'est pas la même chose qu'un ticket flou.
- **Si le ticket est trop volumineux pour être Small** : suggérer un découpage en 2-3 sous-tickets, avec leurs périmètres respectifs.
- **Référencer le glossaire métier** si un terme ambigu apparaît, pour suggérer une normalisation.

### Exemple

**Input** :
> Ticket #1842 : "Permettre l'export des dashboards. CdA : on doit pouvoir exporter les dashboards. Cas testés : un dashboard simple."

**Output (extrait)** :

```markdown
# Pré-revue refinement — 2026-04-30

## Ticket #1842 — Permettre l'export des dashboards

### Tableau des manques par dimension

| Dimension | État | Manque |
|-----------|------|--------|
| User story | absent | aucune story formulée — on a une fonctionnalité brute |
| Critères d'acceptation | partiel | "on doit pouvoir exporter" est tautologique, pas testable |
| Scénarios | partiel | un seul scénario nominal très vague |
| Dépendances | absent | rien sur le format, le storage, l'authent |
| Cas hors-scope | absent | export en masse ? export récurrent ? |

### Test INVEST
- Independent : non — dépend du choix de format pas tranché
- Negotiable : oui
- Valuable : partiel — bénéfice non explicité
- Estimable : non
- Small : non — sous "exporter" se cachent plusieurs sous-fonctionnalités
- Testable : non — pas de critère vérifiable

### Edge cases manquants
```
Given un dashboard contenant 50k lignes
When l'utilisateur lance l'export
Then ... (timeout ? batch ? message ?)
```
```
Given un dashboard contenant des données sensibles RGPD
When l'utilisateur l'exporte
Then ... (logging ? anonymisation ? blocage ?)
```

### Dépendances détectées
- Décision business sur les formats supportés (PDF, PNG, CSV, JSON)
- Service de génération PDF (existant ?)
- Audit logs (à créer ?)

### Niveau de préparation
**à découper**

Le ticket cumule trop de questions ouvertes pour un refinement productif. Suggéré : un ticket parent "exporter dashboard" et 3 sous-tickets (PDF, CSV, audit).
```

---

*Skill de l'Annexe 3 du livre [Le Product Manager Augmenté](../../README.fr.md). Voir [docs/livre.md](../../docs/livre.md) — chapitre 7.*
