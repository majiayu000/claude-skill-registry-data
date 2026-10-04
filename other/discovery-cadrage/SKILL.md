---
name: discovery-cadrage
description: Utiliser pour cadrer une nouvelle discovery utilisateur. Produit cinq hypothèses concurrentes, leurs observables de validation, le profil cible, un guide d'entretien et une grille de codage des verbatims.
version: 0.1.0
author: Ludovic Lefebvre
license: MIT
language: fr
book:
  title: Le Product Manager Augmenté
  annex: A3
tags: [discovery, hypothesis, interview, coding-grid]
---

# discovery-cadrage

## Fiche éditoriale

**Objectif.** Cadrer une discovery utilisateur avec hypothèses multiples et profil cible.

**Entrées.** Sujet d'investigation, données initiales, contexte stratégique.

**Sorties.** Cinq hypothèses, observables de validation, profil cible, guide d'entretien, grille de codage.

**Cadence d'usage.** À chaque nouvelle discovery démarrée.

## Mode opératoire

### Quand m'invoquer

L'utilisateur démarre une discovery (un nouveau sujet à investiguer auprès des utilisateurs) et veut un cadrage rigoureux avant de lancer les entretiens. Il me fournit le sujet, ce qu'il sait déjà, et le contexte stratégique qui justifie l'investigation.

### Procédure

1. **Reformulation du sujet**. Reformuler en une question d'investigation claire (forme : "Comment X expérimente Y dans le contexte Z ?"). Si la formulation initiale est trop vague ou trop précise, le signaler.
2. **Cinq hypothèses concurrentes**. Générer cinq hypothèses **réellement différentes** sur ce qui se passe, pas cinq formulations de la même intuition. Les hypothèses doivent inclure au moins une qui contredit l'intuition initiale du PM.
3. **Observables**. Pour chaque hypothèse, lister 2-3 observables qui la confirmeraient et 1-2 qui l'infirmeraient. Un observable est un fait directement constatable en entretien ou en data, pas une interprétation.
4. **Profil cible**. Définir qui interroger : rôle, contexte, fréquence d'usage, ancienneté, signal d'éligibilité (ex : "a fait au moins 3 actions X dans les 30 derniers jours"). Justifier pourquoi ce profil et pas un autre.
5. **Guide d'entretien**. Produire un guide de 30-45 minutes structuré en : ouverture, contexte personnel, situation cible (récit d'un cas récent), explorations spécifiques liées aux hypothèses, clôture. Privilégier les questions ouvertes commençant par "raconte-moi", "décris", "que s'est-il passé quand".
6. **Grille de codage**. Produire une grille à 4-6 colonnes qui permettra de classer rapidement les verbatims : par hypothèse confirmée/infirmée, par catégorie thématique, par intensité du signal.
7. Produire la sortie au format ci-dessous.

### Format de sortie

```markdown
# Cadrage discovery — {sujet}

## Question d'investigation

> {formulation reformulée}

## Cinq hypothèses

### H1 — {nom court}
{énoncé}
- Observable confirmant : ...
- Observable confirmant : ...
- Observable infirmant : ...

### H2 — ... (idem)
### H3 — ... (idem)
### H4 — ... (idem)
### H5 — ... (idem)

## Profil cible

- Rôle : {rôle}
- Contexte : {contexte}
- Signal d'éligibilité : {critère vérifiable}
- Pourquoi ce profil : {justification}

## Guide d'entretien (30-45 min)

### Ouverture (5 min)
- ...

### Contexte personnel (5-10 min)
- Raconte-moi ton rôle, ce qui occupe tes journées actuellement.
- ...

### Situation cible (15-20 min)
- Raconte-moi la dernière fois que tu as {situation}.
- Que s'est-il passé exactement ? Décris-moi étape par étape.
- ...

### Explorations spécifiques (10 min)
- {questions liées aux hypothèses, à choisir selon le déroulement de l'entretien}
- ...

### Clôture (5 min)
- Y a-t-il quelque chose d'important sur ce sujet que je n'ai pas demandé ?
- Qui d'autre devrais-je interroger ?

## Grille de codage

| Verbatim | Source | H1 | H2 | H3 | H4 | H5 | Thème | Intensité (1-5) |
|----------|--------|----|----|----|----|----|-------|-----------------|
|          |        |    |    |    |    |    |       |                 |

Légende : `+` = signal confirmant, `-` = signal infirmant, `?` = ambigu, vide = non concerné.
```

### Garde-fous

- **Cinq hypothèses réellement concurrentes**, pas cinq paraphrases. Si je n'arrive pas à différencier deux hypothèses sur leurs observables, j'en supprime une.
- **Au moins une hypothèse doit contredire l'intuition initiale** du PM. Si toutes vont dans le même sens, je signale le risque de confirmation.
- **Ne pas générer de verbatims fictifs** dans la grille de codage : la grille est vide, elle se remplit au fil des entretiens.
- **Ne pas pré-conclure** : la sortie est un cadrage d'investigation, pas une recommandation. Si le PM cherche des conclusions, lui rappeler qu'il n'a pas encore parlé aux utilisateurs.
- **Pas plus de 8 questions ouvertes** dans le guide : un guide trop dense empêche d'écouter.

### Exemple

**Input** :
> "Je veux comprendre pourquoi nos free users ne convertissent pas. On a un funnel à 2,3% sur 90 jours, c'est en dessous du marché."

**Output (extrait)** :

```markdown
# Cadrage discovery — Conversion free → paid

## Question d'investigation
> Comment les utilisateurs free expérimentent-ils nos features avancées dans les 90 jours qui suivent leur inscription, et qu'est-ce qui les conduit à payer ou à abandonner ?

## Cinq hypothèses

### H1 — Friction d'onboarding
Les free users ne découvrent pas les features qui justifient le paiement.
- Confirmant : <30% des free users activent au moins 3 features clés en 30j.
- Confirmant : verbatims "je ne savais pas que c'était possible".
- Infirmant : les free users qui paient n'ont pas activé plus de features que ceux qui ne paient pas.

### H2 — Valeur perçue trop faible (différente de H1)
Les utilisateurs découvrent les features mais ne perçoivent pas la valeur qu'elles apportent vs alternatives gratuites.
- Confirmant : verbatims "c'est cool mais je peux faire pareil avec X gratuit".
...

### H3 — Cas d'usage marginal
Notre produit est utilisé pour un besoin ponctuel qui ne justifie pas un abonnement récurrent.
...

### H4 — Problème de pricing, pas de produit
Les utilisateurs voient la valeur mais le prix dépasse leur budget perçu.
...

### H5 — Le free fait trop de choses (contre-intuitif)
Le free tier est suffisant pour 95% des cas — le funnel à 2,3% est en réalité aligné avec la part de power users dans la population.
...
```

---

*Skill de l'Annexe 3 du livre [Le Product Manager Augmenté](../../README.fr.md). Voir [docs/livre.md](../../docs/livre.md) — chapitre 5.*
