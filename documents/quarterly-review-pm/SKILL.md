---
name: quarterly-review-pm
description: Utiliser trimestriellement pour préparer la revue d'un PM managé sur la base de données factuelles et de la grille de maturité IA. Produit une synthèse factuelle, un score de maturité IA, les zones de progression et stagnation, les questions à poser et les objectifs proposés.
version: 0.1.0
author: Ludovic Lefebvre
license: MIT
language: fr
book:
  title: Le Product Manager Augmenté
  annex: A3
tags: [management, review, quarterly, maturity-grid]
---

# quarterly-review-pm

## Fiche éditoriale

**Objectif.** Préparer la revue trimestrielle d'un PM sur la base de données factuelles et de la grille de maturité IA.

**Entrées.** Profil du PM, livraisons du trimestre, retours pairs anonymisés.

**Sorties.** Synthèse factuelle, score de maturité IA, zones de progression et stagnation, questions à poser, objectifs proposés.

**Cadence d'usage.** Trimestriellement, pour chaque PM managé.

## Mode opératoire

### Quand m'invoquer

L'utilisateur (manager) prépare la revue trimestrielle d'un PM de son équipe. Il me fournit le profil du PM, les livraisons du trimestre (objectifs initiaux, livrables réels, OKR atteints / partiels / manqués), et les retours pairs anonymisés (3-5 retours typiques).

### Procédure

1. **Synthèse factuelle** : reformuler ce que le trimestre a livré en termes neutres (sans qualificatifs comme "excellent" ou "décevant"). Lister objectifs initiaux, livrables réels, écarts, OKR atteints/partiels/manqués.
2. **Score de maturité IA** : appliquer la grille de l'Annexe 2 (5 dimensions : usage opérationnel, esprit critique, posture orchestrateur, mesure d'impact, partage). Score 1-5 par dimension. Justifier en une phrase chacun.
3. **Zones de progression** : 2-3 dimensions où le PM a clairement progressé sur le trimestre, avec preuves factuelles.
4. **Zones de stagnation** : 1-2 dimensions où la progression est absente ou faible. Tone factuel, pas accusatoire.
5. **Retours pairs** : agréger les retours pairs sans citer de noms, en distinguant points d'accord et signaux divergents.
6. **Questions à poser en revue** : 5-7 questions ouvertes qui aideront le PM à se positionner sur sa propre trajectoire (pas des questions piège).
7. **Objectifs proposés Q+1** : 3 objectifs concrets, dont au moins un de progression sur la maturité IA.
8. Produire la sortie au format ci-dessous.

### Format de sortie

```markdown
# Revue trimestrielle — {nom du PM}, {trimestre}

## Synthèse factuelle

### Objectifs initiaux
- ...

### Livrables réels
- ...

### Écarts
- ...

### OKR
- {OKR 1} : atteint / partiel / manqué — {valeur réelle vs cible}
- ...

## Score de maturité IA

| Dimension | Score (1-5) | Justification |
|-----------|-------------|---------------|
| Usage opérationnel | x | ... |
| Esprit critique | x | ... |
| Posture orchestrateur | x | ... |
| Mesure d'impact | x | ... |
| Partage | x | ... |

**Score global** : x/25

## Zones de progression (2-3)

- {dimension} — {progression observée} — {preuve factuelle}
- ...

## Zones de stagnation (1-2)

- {dimension} — {stagnation observée, sans jugement} — {ce qui pourrait débloquer}
- ...

## Retours pairs (anonymisés)

### Points d'accord (≥3 retours convergents)
- ...

### Signaux divergents (à discuter en 1:1)
- ...

## Questions à poser en revue (5-7)

1. {question ouverte}
2. ...

## Objectifs proposés Q+1

### Objectif 1 — {titre court}
**Mesurable par** : ...
**Échéance** : fin Q+1.

### Objectif 2 — {titre court}
...

### Objectif 3 — {titre court, sur la maturité IA}
...
```

### Garde-fous

- **Tone factuel obligatoire** : pas de qualificatifs comme "excellent", "décevant", "remarquable". Les faits parlent.
- **Anonymisation stricte des retours pairs** : pas de "X a dit", seulement "n retours mentionnent...".
- **Distinguer accord et divergence** : si les retours pairs sont contradictoires, le signaler — c'est un signal en soi.
- **Pas plus de 7 questions** en revue : un entretien doit pouvoir respirer.
- **Questions ouvertes, jamais piège** : "Comment vois-tu ta posture orchestrateur sur ce trimestre ?" et pas "Pourquoi n'as-tu pas plus utilisé X ?"
- **Objectifs Q+1 calibrés** : 3, dont 1 sur la maturité IA. Au-delà, le PM se disperse.
- **Pas de comparaison entre PMs** : la revue est individuelle. Pas de "vs Sarah" ou "comme Thomas".
- **Pas de score sans justification** : chaque score 1-5 est argumenté.

### Exemple

**Input (résumé)** :
> PM : Thomas, 2 ans d'expérience, périmètre onboarding & activation. Trimestre Q1 : OKR activation J7 atteint à 102%, OKR rétention M1 manqué (87% de la cible). 4 retours pairs : "très précis sur la spec", "lent à arbitrer en comité", "partage peu ses workflows IA", "écoute bien les utilisateurs".

**Output (extrait)** :

```markdown
# Revue trimestrielle — Thomas, Q1 2026

## Synthèse factuelle

### OKR
- Activation J7 : atteint (102% de la cible)
- Rétention M1 : manqué (87% de la cible — 39% vs 45%)

### Livrables vs initial
- Refonte onboarding livrée à temps ✓
- Test pricing déclenché en avance ✓
- Rétention M1 : pas d'expé lancée sur le trimestre

## Score de maturité IA

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Usage opérationnel | 4 | usage régulier sur spec et discovery |
| Esprit critique | 4 | rejets argumentés des outputs IA observés en revue |
| Posture orchestrateur | 2 | aucun agent en routine sur le trimestre |
| Mesure d'impact | 3 | journal de décision tenu, pas d'indicateurs calculés |
| Partage | 2 | aucun workflow partagé en équipe |

**Score global** : 15/25

## Zones de progression

- Esprit critique — observé : 3 cas de rejets argumentés d'outputs IA en revue de spec.
- Usage opérationnel — observé : routinisation sur les pré-revues de tickets.

## Zones de stagnation

- Posture orchestrateur — aucun agent persistant lancé sur le trimestre. Hypothèse : sentiment d'opacité, à discuter.
- Partage — workflows tenus en local, pas diffusés. Pourrait débloquer un effet de levier sur l'équipe.

## Retours pairs (anonymisés)

### Points d'accord (≥3 retours convergents)
- Précision sur la spec saluée par 3 retours.
- Écoute utilisateur citée par 2 retours.

### Signaux divergents (à discuter en 1:1)
- 1 retour mentionne "lent à arbitrer en comité" — à explorer.

## Questions à poser en revue

1. Comment lis-tu ton trimestre toi-même, par rapport aux OKR ?
2. La rétention M1 manquée — quelle est ta lecture des causes ?
3. Sur la posture orchestrateur, qu'est-ce qui te freine pour lancer un agent en routine ?
4. Le partage de workflows IA en équipe — est-ce un blocage de temps ou de confiance ?
5. Sur quel sujet aimerais-tu progresser en Q2, indépendamment des objectifs business ?

## Objectifs proposés Q2

### Objectif 1 — Lancer une expérimentation rétention M1
Mesurable par : un test livré, mesuré, conclu (positif ou négatif). Échéance : fin Q2.

### Objectif 2 — Documenter et partager 2 workflows IA en équipe
Mesurable par : 2 docs courts dans la base partagée, 1 démo en équipe. Échéance : fin Q2.

### Objectif 3 — Activer un premier agent persistant
Mesurable par : un agent en routine ≥ 4 semaines avec audit. Échéance : fin Q2.
```

---

*Skill de l'Annexe 3 du livre [Le Product Manager Augmenté](../../README.fr.md). Voir [docs/livre.md](../../docs/livre.md) — chapitre 13 et Annexe 2 pour la grille.*
