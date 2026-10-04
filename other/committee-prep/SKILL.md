---
name: committee-prep
description: Utiliser pour préparer un comité d'arbitrage ou un comité de pilotage. Produit une synthèse de fond, des contre-arguments classés, les objections anticipées par participant, une formulation médiane et les critères de décision attendus.
version: 0.1.0
author: Ludovic Lefebvre
license: MIT
language: fr
book:
  title: Le Product Manager Augmenté
  annex: A3
tags: [decision, arbitrage, comite, communication]
---

# committee-prep

## Fiche éditoriale

**Objectif.** Préparer un comité d'arbitrage avec dossier de fond et anticipation des objections.

**Entrées.** Sujet, recommandation provisoire, données disponibles, liste des participants.

**Sorties.** Synthèse des données, contre-arguments classés, objections anticipées par participant, formulation médiane, critères de décision.

**Cadence d'usage.** Avant chaque comité d'arbitrage majeur.

## Mode opératoire

### Quand m'invoquer

L'utilisateur prépare un comité d'arbitrage (steerco, comité produit, instance de décision) et me fournit le sujet, sa recommandation provisoire, les données qu'il a en main, et la liste des participants attendus. Il veut un dossier qui anticipe la dynamique de la réunion.

### Procédure

1. **Synthèse des données** : reformuler ce qui est documenté en 5 à 8 puces factuelles. Distinguer faits observés et hypothèses.
2. **Contre-arguments** : générer les trois meilleurs contre-arguments à la recommandation, classés par force décroissante. Pour chacun, donner ce qui le réfute si possible.
3. **Cartographie des participants** : pour chaque participant, identifier sa position probable (favorable / neutre / opposé) et son angle de préoccupation principal (technique, commercial, financier, RH, juridique, etc.). Si les positions ne sont pas connues, le dire.
4. **Objections anticipées** : pour chaque participant identifié comme neutre ou opposé, formuler 1 à 2 objections probables et la réponse préparée.
5. **Formulation médiane** : proposer une version intermédiaire de la recommandation, qui pourrait émerger comme compromis si la position initiale n'est pas validée. Préciser ce qu'on perd et ce qu'on gagne.
6. **Critères de décision** : expliciter les critères sur lesquels la décision devrait se prendre, et signaler s'ils sont implicites ou divergents entre participants.
7. Produire la sortie au format ci-dessous.

### Format de sortie

```markdown
# Dossier comité — {sujet}
*{date du comité} — préparé le {date du jour}*

## Recommandation soumise

> {1-3 phrases — recommandation à arbitrer}

## Synthèse des données (5-8 puces)

- {fait factuel} *(source : {référence})*
- ...

## Contre-arguments (par force décroissante)

### 1. {contre-argument principal}
{explication courte}
**Réfutation possible** : {élément qui désamorce}

### 2. ...
### 3. ...

## Cartographie des participants

| Participant | Position probable | Angle de préoccupation |
|-------------|-------------------|------------------------|
| {nom} | favorable / neutre / opposé / inconnu | technique / commercial / financier / juridique / RH / autre |

## Objections anticipées et réponses

### {participant 1}
- **Objection** : {formulation probable}
- **Réponse préparée** : {1-2 phrases}

### {participant 2}
...

## Formulation médiane

> {version compromis de la recommandation}

**Ce qu'on gagne** : {bénéfice de la médiane}
**Ce qu'on perd** : {compromis assumé}

## Critères de décision

- {critère 1} — {explicite / implicite ; consensus / divergent}
- ...
```

### Garde-fous

- Pas de jugement de valeur sur les participants. Les positions sont des hypothèses de travail, pas un procès d'intention. Si une position est inconnue, l'écrire "inconnue" plutôt que la deviner.
- Pas d'invention de données. Si la recommandation manque de support factuel, le signaler explicitement dans la synthèse.
- Pas de stratégie de manipulation. Anticiper des objections sert à clarifier la pensée, pas à neutraliser une opposition légitime.
- Si la recommandation soumise est faible (peu de support, contre-arguments majeurs sans réfutation), le dire. Ne pas dorer la pilule.

### Exemple

**Input** :
> Sujet : généralisation du multi-langue dans l'app, démarrage par allemand et espagnol. Ma reco : oui, démarrer Q3. Données : 18% de signups venant de DE/ES en H1, churn 2x supérieur sur ces marchés. Participants : CFO, CTO, Head of Growth, Head of Support.

**Output (extrait)** :

```markdown
# Dossier comité — Multi-langue DE+ES

## Recommandation soumise
> Démarrer la généralisation multi-langue en Q3, avec un MVP allemand + espagnol.

## Contre-arguments (par force décroissante)
### 1. Charge tech non chiffrée
La reco repose sur "démarrer Q3" sans estimation tech. Risque que l'effort réel dépasse Q3.
**Réfutation possible** : produire une estimation rough avec le CTO avant comité.

### 2. ROI non démontré
Le churn 2x supérieur peut venir d'autres facteurs que la langue (méthodes de paiement, pricing local).
**Réfutation possible** : citer les verbatims support qui mentionnent explicitement la langue.

### 3. Priorité concurrente
H2 est déjà chargé (refonte onboarding annoncée).
**Réfutation possible** : proposer un découpage permettant le déploiement progressif sans bloquer l'onboarding.

## Cartographie des participants

| Participant | Position probable | Angle |
|-------------|-------------------|-------|
| CFO | neutre | financier (coût de l'effort) |
| CTO | inconnu | technique (estimation, dette) |
| Head of Growth | favorable | commercial (TAM débloqué) |
| Head of Support | favorable | qualité service |
```

---

*Skill de l'Annexe 3 du livre [Le Product Manager Augmenté](../../README.fr.md). Voir [docs/livre.md](../../docs/livre.md) — chapitre 6.*
