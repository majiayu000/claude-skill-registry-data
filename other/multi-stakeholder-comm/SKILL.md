---
name: multi-stakeholder-comm
description: Utiliser avant chaque communication transverse importante pour décliner un même sujet en versions calibrées par stakeholder. Produit un encart d'une page par stakeholder, dans le format de prédilection identifié dans la matrice.
version: 0.1.0
author: Ludovic Lefebvre
license: MIT
language: fr
book:
  title: Le Product Manager Augmenté
  annex: A3
tags: [communication, stakeholders, alignment, one-pager]
---

# multi-stakeholder-comm

## Fiche éditoriale

**Objectif.** Décliner un même sujet en versions calibrées par stakeholder.

**Entrées.** Contenu de fond, matrice stakeholders.

**Sorties.** Un encart d'une page par stakeholder, dans son format préféré.

**Cadence d'usage.** Avant chaque communication transverse importante.

## Mode opératoire

### Quand m'invoquer

L'utilisateur a un sujet à communiquer transversalement (changement de roadmap, lancement majeur, décision structurante, alerte) et veut éviter le mail unique générique. Il me fournit le contenu de fond et sa matrice stakeholders (nom, rôle, angle de préoccupation, format préféré).

### Procédure

1. **Comprendre le contenu de fond** : reformuler en mes mots les 3-5 points-clés. Si la reformulation ne tient pas, demander des précisions.
2. **Lire la matrice stakeholders** : pour chaque destinataire, identifier rôle, angle (financier, technique, commercial, RH, etc.) et format préféré (mail synthétique, slide, dashboard, slack).
3. **Pour chaque stakeholder**, générer un encart en respectant trois règles :
   - Une page maximum (densité adaptée au format).
   - L'angle de préoccupation est traité en premier.
   - Le format respecte la préférence (slide → bullets et titre fort ; mail → paragraphes courts ; slack → ton informel + emojis sobres).
4. **Cohérence factuelle** : tous les encarts disent la même chose sur les faits. Ce qui varie, c'est l'ordre, l'angle, le niveau de détail technique, et la formulation.
5. **Indicateur de divergence** : signaler si un même fait risquerait d'être interprété différemment selon le format choisi (ex : "M&A en discussion" peut sonner alarmant pour le CFO et opportuniste pour le CMO).
6. Produire la sortie au format ci-dessous.

### Format de sortie

```markdown
# Communication transverse — {sujet}

## Points-clés (factuels, identiques pour tous)

1. ...
2. ...
3. ...

## Indicateurs de divergence à surveiller

- {fait susceptible d'être lu différemment} — vigilance pour {stakeholders A vs B}

---

## Encart pour {Stakeholder 1} — {rôle}, {angle de préoccupation}

*Format : {préférence}*

{Contenu calibré, ≤ 1 page.}

---

## Encart pour {Stakeholder 2} — {rôle}, {angle}

*Format : {préférence}*

{Contenu calibré.}

---

## Encart pour {Stakeholder 3} — ...
...
```

### Garde-fous

- **Cohérence factuelle stricte** : tous les encarts disent la même chose sur les faits. La déclinaison joue sur l'ordre, l'angle, le niveau de détail — jamais sur le fond.
- **Pas de version "édulcorée"** pour qui que ce soit : si un fait est désagréable pour un destinataire, il est dit, juste positionné de la manière la plus utile à la décision.
- **Une page maximum** : la promesse est l'encart, pas le dossier. Si le sujet en demande plus, le signaler et proposer un dossier de fond séparé en complément.
- **Format respecté** : un destinataire qui consomme du slack ne reçoit pas un mail de 3 paragraphes, et inversement.
- **Anonymisation absente** : ces communications nomment les stakeholders. Pas d'enjeu d'anonymisation contrairement aux skills discovery.
- **Indicateurs de divergence systématiques** : si je vois qu'un fait peut être lu de deux façons selon les destinataires, je le signale au PM avant de produire les encarts.

### Exemple

**Input** :
> Sujet : on décale le lancement DE+ES de Q3 à Q4 pour cause de retard tech sur l'infra multi-langue.
> Matrice : CEO (commercial, slide), CTO (tech, mail), Head of Sales DACH (commercial, slack), CFO (financier, mail).

**Output (extrait)** :

```markdown
# Communication transverse — Décalage lancement DE+ES

## Points-clés
1. Le lancement DE+ES bascule de Q3 à Q4.
2. Cause : retard tech sur la refonte infra multi-langue, complexité sous-estimée de 30%.
3. Impact business : -€{x}k de revenu attendu sur Q3, rattrapé en Q4 si pas d'autre incident.
4. Plan B : démarrer DE seul début Q4 si ES nécessite encore deux semaines.

---

## Encart pour CEO — commercial, slide

*Format : slide*

# Lancement DE+ES → Q4

- **Décalage** : Q3 → Q4 (3 mois)
- **Cause** : refonte infra multi-langue plus complexe que prévu
- **Manque à gagner Q3** : ~€{x}k
- **Rattrapage** : Q4 visé sans dégradation périmètre
- **Action attendue** : aligner com externe / report annonce presse

---

## Encart pour CTO — tech, mail

*Format : mail*

Objet : Décalage lancement DE+ES Q3 → Q4

Bonjour,

Comme discuté lundi, on bascule le lancement DE+ES en Q4. La cause est connue : la refonte infra multi-langue (cf. ticket TECH-2104) a sous-estimé d'environ 30% la complexité de gestion des fallbacks de traduction et des tests d'intégration multi-locale.

Décisions prises de mon côté :
- arbitrage business : on assume le décalage plutôt que de livrer un MVP fragile.
- plan B : DE seul possible début Q4 si ES nécessite encore 2 semaines.

Ce dont j'ai besoin de toi cette semaine :
- confirmation de l'estimation tech révisée (Q4 atteignable avec capacité actuelle ?).
- signal si une coupe de scope éviterait le décalage complet.

Merci.

---

## Encart pour Head of Sales DACH — commercial, slack

*Format : slack*

@head-of-sales-dach Heads-up rapide : on décale DE+ES de Q3 à Q4 (retard infra). Pour ton équipe DACH ça veut dire : on tient le pipeline en français/anglais sur Q3 mais le push DE arrive en Q4. Je te transmets un brief Q4 d'ici fin de semaine pour ajuster ton plan d'engagement. 🙏

---

## Encart pour CFO — financier, mail

*Format : mail*

Objet : Décalage DE+ES — impact financier Q3

Bonjour,

Décalage du lancement DE+ES de Q3 à Q4. Impact à anticiper côté forecast :

- Q3 : -€{x}k vs prévision (correspondant à la part DACH+ES du forecast)
- Q4 : rattrapage prévu, sans surcoût additionnel (l'effort tech est dans le run, pas en surcoût externe)
- Risque résiduel : nouveau retard si dépendance externe identifiée — j'ai demandé une revue tech avant fin de semaine

Je te ferai un point écrit avec la version révisée du forecast lundi.
```

---

*Skill de l'Annexe 3 du livre [Le Product Manager Augmenté](../../README.fr.md). Voir [docs/livre.md](../../docs/livre.md) — chapitre 8.*
