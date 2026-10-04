---
name: four-indicators-measure
description: Utiliser une fois par trimestre pour calculer les quatre indicateurs du PM augmenté (densité de décision, justesse rétrospective, délai de bascule, indice de réinvestissement) à partir du journal de décision, des indicateurs d'usage, des audits agents et des agendas comparés.
version: 0.1.0
author: Ludovic Lefebvre
license: MIT
language: fr
book:
  title: Le Product Manager Augmenté
  annex: A3
tags: [mesure, indicateurs, trimestriel, bilan]
---

# four-indicators-measure

## Fiche éditoriale

**Objectif.** Calculer les quatre indicateurs du PM augmenté (densité de décision, justesse rétrospective, délai de bascule, indice de réinvestissement).

**Entrées.** Journal de décision, indicateurs d'usage, audits agents, agendas comparés.

**Sorties.** Tableau des quatre indicateurs avec valeur actuelle, comparaison trimestre précédent, lecture qualitative.

**Cadence d'usage.** Trimestriellement.

## Mode opératoire

### Quand m'invoquer

L'utilisateur clôture un trimestre et veut faire le bilan factuel de sa transformation augmentée. Il fournit son journal de décision, ses logs d'usage IA, les rapports d'audit de ses agents, et l'extraction de son agenda sur le trimestre.

### Procédure

Pour chaque indicateur, suivre la définition du chapitre 14.

1. **Densité de décision**. Compter le nombre de décisions explicitement consignées dans le journal sur le trimestre. Diviser par le nombre de jours ouvrés. Comparer au trimestre précédent.

2. **Justesse rétrospective**. Pour les décisions du trimestre N-2 (assez de recul pour observer le résultat), classer en : confirmée par les faits, infirmée, non concluante. Calculer le ratio confirmées / total.

3. **Délai de bascule**. Mesurer le temps moyen entre la première mention d'un sujet (en réunion, en ticket, en verbatim) et la première décision documentée à son sujet. Comparer N et N-1.

4. **Indice de réinvestissement**. Sur la base des agendas comparés, calculer la part du temps gagné par l'IA qui a été réinvestie en discovery / arbitrage / décision (vs. consommée par d'autres réunions ou lissée dans la journée). Le livre suggère 60% comme cible saine.

5. Produire le tableau au format ci-dessous, suivi d'une lecture qualitative en 3-5 phrases.

### Format de sortie

```markdown
# Bilan trimestriel — Q{n} {année}

## Tableau des quatre indicateurs

| Indicateur | Valeur Q{n} | Valeur Q{n-1} | Évolution | Cible |
|------------|-------------|----------------|-----------|-------|
| Densité de décision | {x} décisions/jour | {y} décisions/jour | {↗ ↘ →} | — |
| Justesse rétrospective | {x}% (sur {n} décisions Q{n-2}) | {y}% | {↗ ↘ →} | ≥ 60% |
| Délai de bascule | {x} jours | {y} jours | {↗ ↘ →} | en baisse |
| Indice de réinvestissement | {x}% | {y}% | {↗ ↘ →} | ≥ 60% |

## Lecture qualitative

{3-5 phrases : ce que les chiffres disent au-delà de la valeur brute. Ce qui est en progrès, ce qui régresse, ce qu'il faut creuser.}

## Sources des données

- Journal de décision : {nombre d'entrées analysées sur la période}
- Audits agents : {nombre d'audits intégrés}
- Agenda : {nombre de semaines couvertes}
- Indicateurs d'usage : {référence}

## Limites de cette mesure

{1-3 phrases : ce qu'il faut savoir des biais ou des manques de cette mesure ce trimestre.}
```

### Garde-fous

- **Pas d'invention de chiffres**. Si une donnée d'entrée manque (ex : journal incomplet sur octobre), l'écrire dans la section "Limites" et baisser la confiance de l'indicateur correspondant.
- **Justesse rétrospective sur Q{n-2} seulement** : il faut au minimum un trimestre complet de recul pour évaluer la confirmation. Ne jamais évaluer la justesse de décisions trop récentes.
- **Pas de jugement personnel sur le PM**. Les indicateurs s'interprètent dans le contexte (un trimestre avec un comex stratégique aura mécaniquement plus de décisions). La lecture qualitative reste factuelle.
- **Aucune pondération arbitraire**. Si les quatre indicateurs sont en tension, ne pas les agréger en un score unique ; les présenter tels quels.

### Exemple

**Input (résumé)** :
> Journal Q1 : 47 décisions sur 60 jours ouvrés. Trimestre N-2 (Q3 année dernière) : 38 décisions, 22 confirmées, 9 infirmées, 7 non concluantes. Délai de bascule moyen Q1 : 12 jours (vs 19 en Q4). Agenda : 6h gagnées par semaine sur la rédaction d'artefacts ; sur ces 6h, 3.5h passées en discovery/arbitrage en moyenne.

**Output (extrait)** :

```markdown
# Bilan trimestriel — Q1 2026

## Tableau

| Indicateur | Valeur Q1 | Valeur Q4 | Évolution | Cible |
|------------|-----------|-----------|-----------|-------|
| Densité de décision | 0,78 décisions/jour | 0,62 | ↗ | — |
| Justesse rétrospective | 71% (22/31 sur Q3) | 64% | ↗ | ≥ 60% |
| Délai de bascule | 12 jours | 19 jours | ↘ (favorable) | en baisse |
| Indice de réinvestissement | 58% | 47% | ↗ | ≥ 60% |

## Lecture qualitative

Les quatre indicateurs vont dans le bon sens. La densité de décision augmente sans dégrader la justesse rétrospective (qui s'améliore aussi), ce qui est l'indice principal d'une transformation saine. Le délai de bascule diminue significativement, signe que les routines de veille sont effectivement utilisées. L'indice de réinvestissement reste sous la cible des 60% — à creuser : où vont les 42% restants ?
```

---

*Skill de l'Annexe 3 du livre [Le Product Manager Augmenté](../../README.fr.md). Voir [docs/livre.md](../../docs/livre.md) — chapitre 14.*
