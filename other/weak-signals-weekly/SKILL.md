---
name: weak-signals-weekly
description: Utiliser chaque lundi matin pour produire la synthèse hebdomadaire de signaux faibles à partir de sources multiples (verbatims, tickets support, mentions externes, logs). Produit une note markdown lisible en cinq minutes structurée en quatre blocs.
version: 0.1.0
author: Ludovic Lefebvre
license: MIT
language: fr
book:
  title: Le Product Manager Augmenté
  annex: A3
tags: [discovery, weak-signals, weekly, synthesis]
---

# weak-signals-weekly

## Fiche éditoriale

**Objectif.** Produire la synthèse hebdomadaire de signaux faibles à partir de sources multiples (verbatims, logs, mentions, support).

**Entrées.** Connecteurs vers les sources brutes, période d'observation, contexte stratégique du périmètre.

**Sorties.** Synthèse markdown structurée en quatre blocs (thèmes émergents, signaux faibles, anomalies, questions ouvertes), lisible en cinq minutes.

**Cadence d'usage.** Chaque lundi matin, en automatique.

## Mode opératoire

### Quand m'invoquer

L'utilisateur me demande la synthèse hebdo de signaux faibles, ou évoque un besoin d'observation utilisateur sur la semaine. Sources typiques : exports de verbatims (CSV ou markdown), tickets support, mentions externes (forums, social), logs d'usage agrégés.

### Procédure

1. **Identifier la fenêtre d'observation** (par défaut : 7 derniers jours ; ajustable).
2. **Charger les sources** fournies. Si une source est inaccessible ou vide, le signaler dans la note.
3. **Catégoriser chaque entrée** dans l'un des 4 blocs : thème émergent (récurrent et nouveau), signal faible (rare mais inattendu), anomalie (écart entre data et verbatims), question ouverte (chose à creuser).
4. **Anonymiser** systématiquement : pas de nom, pas d'identifiant utilisateur, pas d'email.
5. **Sourcer chaque entrée** : lien ou référence à la source d'origine, date, et indice de confiance (faible / moyenne / forte selon le nombre d'occurrences).
6. **Distinguer fait et hypothèse** : un fait observé est repérable dans les sources ; une hypothèse interprétative est une lecture du PM, à signaler comme telle.
7. Produire la note au format ci-dessous.

### Format de sortie

```markdown
# Signaux faibles — semaine du {date_debut} au {date_fin}

## Thèmes émergents
- {thème} — observé dans {n} verbatims / {m} tickets — confiance {faible|moyenne|forte}
  Sources : [{ref}], [{ref}]
- ...

## Signaux faibles
- {signal} — apparu pour la première fois cette semaine — confiance faible
  Source : [{ref}]
- ...

## Anomalies
- {description du gap} — confiance {niveau}
  Indicateur d'usage : {chiffre}
  Verbatim contradictoire : "{citation anonymisée}" — [{ref}]
- ...

## Questions ouvertes
- ?
- ?

## Sources consultées
{nombre} sources sur {total}, {nombre_indispo} indisponibles ou vides.
```

### Garde-fous

- **Ne pas inventer de signal en l'absence de source** : si une catégorie est vide, écrire "—".
- **Anonymisation systématique** : tout verbatim qui contient un nom, un identifiant ou un email est reformulé avant inclusion. Si l'anonymisation est impossible sans dénaturer, exclure le verbatim.
- **Distinguer fait observé et hypothèse interprétative** : ne pas mélanger ce qui est dans les données et ce qui est ma lecture.
- **Calibrer la confiance** : une seule mention = confiance faible, jamais "forte".
- **Pas de hiérarchisation par "gravité business"** : la note est descriptive, pas prescriptive. Les arbitrages se font ailleurs.
- **Lisible en cinq minutes** : si la note dépasse 60 lignes, condenser ou découper en deux semaines distinctes.

### Exemple

**Input** :
> Verbatims support semaine 17 (32 entrées), tickets app store (5 nouvelles reviews), logs d'usage feature export (47 utilisations vs 32 la semaine précédente).

**Output (extrait)** :

```markdown
# Signaux faibles — semaine du 2026-04-22 au 2026-04-28

## Thèmes émergents
- Lenteur du dashboard sur datasets >10k lignes — observé dans 7 tickets support — confiance moyenne
  Sources : [#4521, #4534, #4538, #4541, #4546, #4552, #4559]

## Signaux faibles
- Demande d'export en JSON (vs CSV/PDF actuellement supportés) — apparu 3 fois cette semaine — confiance faible
  Sources : [#4528, #4539, app-store-review-2026-04-25]

## Anomalies
- Hausse 47% de l'usage feature export sans pic correspondant côté trafic ou signups — confiance moyenne
  Verbatim potentiellement lié : "je dois exporter pour faire des recoupements ailleurs" — [#4528]
  Hypothèse interprétative : friction non résolue dans le dashboard, contournée par export.

## Questions ouvertes
- ? La hausse export persiste-t-elle si la lenteur dashboard est résolue ?
- ? Le besoin JSON émerge-t-il chez un segment précis (devs, analystes) ?

## Sources consultées
3 sources sur 3, 0 indisponibles.
```

---

*Skill de l'Annexe 3 du livre [Le Product Manager Augmenté](../../README.fr.md). Voir [docs/livre.md](../../docs/livre.md) — chapitre 5.*
