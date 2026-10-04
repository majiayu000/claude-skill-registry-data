---
name: feature-ethics-audit
description: Utiliser pour auditer une feature envisagée sur ses risques éthiques (manipulation, biais, exploitation de vulnérabilité, données). Produit un diagnostic d'exploitation potentielle, des alternatives moins exposées, et une recommandation explicite.
version: 0.1.0
author: Ludovic Lefebvre
license: MIT
language: fr
book:
  title: Le Product Manager Augmenté
  annex: A3
tags: [ethics, audit, decision, dark-patterns]
---

# feature-ethics-audit

## Fiche éditoriale

**Objectif.** Auditer une feature envisagée sur ses risques éthiques (manipulation, biais, données).

**Entrées.** Description fonctionnelle, profil utilisateur cible, mécanisme de la feature.

**Sorties.** Diagnostic d'exploitation de vulnérabilité, alternatives moins exposées, recommandation explicite.

**Cadence d'usage.** À toute proposition de feature à fort potentiel d'engagement.

## Mode opératoire

### Quand m'invoquer

L'utilisateur me soumet une feature à auditer, particulièrement si elle vise l'engagement, la rétention, la conversion, ou si elle traite des données utilisateurs sensibles. Il me fournit la description fonctionnelle, le profil cible, et le mécanisme (ce qui s'active, quand, comment).

### Procédure

1. **Reformuler la feature** sans interpréter, en isolant le mécanisme central.
2. **Identifier la vulnérabilité activée** : quel biais cognitif, quel besoin émotionnel, quelle asymétrie d'information la feature mobilise pour fonctionner ? Toute feature à fort engagement en active au moins un.
3. **Évaluer l'intensité** : la feature est-elle conçue pour rendre l'arrêt difficile (sunk cost, FOMO, intermittence variable), ou laisse-t-elle l'utilisateur libre de partir sans coût psychologique ?
4. **Identifier les segments à risque** : quels utilisateurs sont disproportionnellement exposés (mineurs, personnes vulnérables, utilisateurs en situation de stress, biais socio-économiques) ?
5. **Vérifier les données** : la feature collecte/utilise-t-elle des données nouvelles ? Sont-elles strictement nécessaires ? Sont-elles cohérentes avec la finalité initialement consentie ?
6. **Générer 2-3 alternatives** qui atteignent ~80% du bénéfice business sans le mécanisme problématique.
7. **Recommandation explicite** : continuer / continuer avec garde-fous / ne pas continuer. Justifier en 2-3 phrases.

### Format de sortie

```markdown
# Audit éthique — {nom de la feature}

## Description reformulée

> {description en 2-3 phrases, neutre}

## Vulnérabilité activée

- **Biais ou besoin mobilisé** : {nom du biais ou besoin}
- **Intensité d'activation** : faible / moyenne / forte
- **Mécanisme** : {comment la feature exploite ce biais}

## Segments à risque

- {segment 1} — {raison de l'exposition disproportionnée}
- {segment 2} — ...

## Données

- Données collectées : {liste}
- Données strictement nécessaires : {liste}
- Cohérence avec la finalité consentie : oui / partielle / non

## Drapeaux levés

- {drapeau 1}
- {drapeau 2}

## Alternatives moins exposées

### A1 — {nom de l'alternative}
{description courte}
Bénéfice business attendu vs original : ~{x}%
Risque éthique vs original : {réduit / similaire / aggravé}

### A2 — ...

## Recommandation

**{continuer | continuer avec garde-fous | ne pas continuer}.**

{2-3 phrases qui justifient. Si "continuer avec garde-fous", lister les garde-fous obligatoires.}
```

### Garde-fous

- **Pas de jugement moral abstrait** : l'audit pointe des mécanismes concrets (sunk cost, FOMO, intermittence variable, dark patterns RGPD, etc.), pas une condamnation générale.
- **Reconnaître la légitimité business** : l'objectif n'est pas d'interdire toute feature à fort engagement, mais d'éclairer le coût caché.
- **Trois recommandations possibles seulement** : continuer / continuer avec garde-fous / ne pas continuer. Pas de "ça dépend" sans tranchage.
- **Si la feature concerne des mineurs ou personnes vulnérables** : drapeau levé d'office, recommandation minimum "continuer avec garde-fous".
- **Si données collectées hors de la finalité initiale** : drapeau levé d'office, vérification RGPD requise.
- **Pas d'interprétation des intentions du PM** : on audite la feature, pas la motivation.

### Exemple

**Input** :
> Feature : notification push "X de tes contacts viennent de s'inscrire — rejoins-les" envoyée 24h après l'inscription si l'onboarding n'est pas complété. Profil cible : nouveaux utilisateurs particuliers. Mécanisme : si l'inscription via OAuth a permis de récupérer une liste de contacts, on cross-référence avec notre base d'utilisateurs.

**Output (extrait)** :

```markdown
# Audit éthique — Push "tes contacts sont là"

## Description reformulée
> Une notification push affirmant que des contacts de l'utilisateur sont présents sur la plateforme, déclenchée 24h après l'inscription si l'onboarding n'est pas complet, et utilisant une liste de contacts collectée via OAuth.

## Vulnérabilité activée
- **Biais mobilisé** : besoin d'appartenance + FOMO social
- **Intensité d'activation** : forte
- **Mécanisme** : pression sociale fabriquée — la formulation suggère une simultanéité (« viennent de s'inscrire ») qui peut ne pas exister.

## Segments à risque
- Utilisateurs jeunes / adolescents : sensibilité aux dynamiques de groupe.
- Utilisateurs en situation d'isolement : impact émotionnel disproportionné.

## Données
- Données collectées : liste de contacts via OAuth.
- Données strictement nécessaires : non — la fonctionnalité d'onboarding ne nécessite pas la liste de contacts.
- Cohérence avec finalité consentie : partielle — l'OAuth est consenti pour authentification, pas pour cross-référencement.

## Drapeaux levés
- Affirmation potentiellement fausse ("viennent de s'inscrire") si les contacts sont anciens utilisateurs.
- Données d'OAuth utilisées hors de la finalité d'authentification.
- Mécanisme dark-pattern de pression sociale.

## Alternatives
### A1 — Push neutre
"X de tes contacts utilisent {produit}" sans timing fabriqué. Bénéfice business : ~80%. Risque éthique : réduit.

### A2 — Pas de cross-référencement automatique
Proposer en onboarding "veux-tu voir si certains de tes contacts utilisent {produit} ?". Bénéfice business : ~50% (consentement requis). Risque éthique : minimal.

## Recommandation
**Ne pas continuer en l'état.** La combinaison "donnée hors finalité + affirmation potentiellement fausse + segment jeune" cumule trois drapeaux. Si la feature est tenue, basculer sur A2 (consentement explicite).
```

---

*Skill de l'Annexe 3 du livre [Le Product Manager Augmenté](../../README.fr.md). Voir [docs/livre.md](../../docs/livre.md) — chapitres 6 et 16.*
