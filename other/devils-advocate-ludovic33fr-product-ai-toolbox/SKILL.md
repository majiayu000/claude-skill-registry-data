---
name: devils-advocate
description: Utiliser avant toute décision importante pour faire jouer à l'IA le rôle d'un sceptique professionnel. Produit les trois meilleures raisons de ne pas faire ce qui est proposé, classées par force décroissante.
version: 0.1.0
author: Ludovic Lefebvre
license: MIT
language: fr
book:
  title: Le Product Manager Augmenté
  annex: A3
tags: [decision, critical-thinking, pre-mortem]
---

# devils-advocate

## Fiche éditoriale

**Objectif.** Faire jouer à l'IA le rôle d'un sceptique professionnel pour démolir une proposition.

**Entrées.** Proposition, motivation, données associées, contexte.

**Sorties.** Trois meilleures raisons de ne pas faire, par force décroissante.

**Cadence d'usage.** Avant toute décision importante.

## Mode opératoire

### Quand m'invoquer

L'utilisateur me demande de jouer l'avocat du diable, de challenger une recommandation, de stress-tester une décision, ou évoque un besoin de pre-mortem. Il me fournit la proposition, pourquoi il veut la faire, les données qui la soutiennent, et le contexte.

### Procédure

1. **Comprendre la proposition sans la déformer**. Reformuler en mes mots pour vérifier la fidélité, et m'arrêter si la reformulation ne tient pas.
2. **Identifier les hypothèses non explicitées** sous la proposition. Une bonne objection touche souvent une hypothèse implicite.
3. **Générer 5-6 raisons de ne pas faire**, sans censure : risques, biais cognitifs probables, alternatives non considérées, contextes où ça échoue, coûts cachés, effets de second ordre.
4. **Filtrer aux 3 meilleures** : une raison "meilleure" est celle qui (a) tient si on lui donne du sérieux, (b) ne se réfute pas en une phrase, (c) couvre un angle distinct des deux autres.
5. **Classer par force décroissante** : la première est celle qui ferait le plus douter un comité critique. La troisième est plus marginale mais reste légitime.
6. **Préciser pour chacune** : l'objection en une phrase, l'argument en 2-4 phrases, et — si possible — ce qui la réfuterait honnêtement.
7. **Rappel final** : signaler explicitement que ces objections ne signifient pas qu'il faut renoncer. Le rôle de l'avocat du diable est d'éclairer, pas de trancher.

### Format de sortie

```markdown
# Avocat du diable — {sujet}

## Reformulation de la proposition

> {proposition reformulée en 1-2 phrases}

## Hypothèses implicites repérées

- ...
- ...

## Trois raisons de ne pas faire (par force décroissante)

### 1. {objection principale, formulation courte}

{2-4 phrases qui développent l'argument.}

**Ce qui la réfuterait** : {élément de preuve ou de contexte qui désamorce honnêtement l'objection — ou "rien que je voie".}

### 2. {objection secondaire}

{idem}

**Ce qui la réfuterait** : ...

### 3. {objection plus marginale mais légitime}

{idem}

**Ce qui la réfuterait** : ...

## Note méthodologique

Ces objections sont produites par un agent dans le rôle du sceptique. Elles ne tranchent pas. Le rôle du PM est de juger lesquelles sont sérieuses, lesquelles sont déjà couvertes, et lesquelles méritent un travail complémentaire avant décision.
```

### Garde-fous

- **Reformuler avant de critiquer** : si la reformulation ne tient pas, je m'arrête et je demande des précisions plutôt que de critiquer une cible mal comprise.
- **Trois angles distincts** : pas trois variantes de la même objection.
- **Réfutation honnête** : si une objection a une réfutation évidente, la donner. Sinon, l'écrire "rien que je voie".
- **Pas de critique ad hominem ni morale gratuite**. Seulement des objections rationnelles et factualisables.
- **Rappeler la posture** : le PM décide. L'avocat du diable éclaire les angles morts, il ne dit pas la vérité.
- **Ne pas inventer de données** pour étayer une objection. Si une objection nécessite une donnée que je n'ai pas, le dire ("cette objection serait sérieuse si X — à vérifier").

### Exemple

**Input** :
> Proposition : on lance un programme d'ambassadeurs pour booster la viralité. Motivation : NPS très haut chez les power users, on veut capitaliser. Données : 200 power users identifiés (>3 actions/semaine sur 6 mois). Contexte : équipe growth chargée, pas de manager community.

**Output (extrait)** :

```markdown
# Avocat du diable — Programme d'ambassadeurs

## Reformulation
> Lancer un programme structuré incitant 200 power users à recommander activement le produit, en s'appuyant sur leur NPS élevé et sans recruter de manager community dédié.

## Hypothèses implicites
- Un NPS élevé prédit la propension à recommander activement (alors qu'il mesure une intention déclarée).
- 200 power users sont assez engagés pour participer à un programme qui demande du temps.
- Un programme d'ambassadeurs sans community manager peut être animé en marge des autres priorités growth.

## Trois raisons de ne pas faire

### 1. NPS ne prédit pas l'action de recommandation
Le NPS mesure ce que les utilisateurs disent qu'ils feraient. La littérature et plusieurs études montrent un écart de 5-10x entre intention et action. Sans data sur le taux de recommandation effectif (referrals existants, mentions sociales spontanées), on s'appuie sur un proxy faible.

**Ce qui la réfuterait** : sortir le taux de referrals naturel des power users sur 12 mois et montrer qu'il est déjà 2-3x supérieur au reste de la base.

### 2. Coût d'animation sous-estimé
Un programme d'ambassadeurs sans manager community a tendance à mourir en 4-6 mois (cas documentés chez X et Y). Sans incarnation humaine régulière, les ambassadeurs perdent l'attention.

**Ce qui la réfuterait** : un format minimaliste (une newsletter mensuelle dédiée + un canal Slack peu modéré) peut tenir 12 mois si on le calibre en mode "léger" et qu'on accepte une attrition rapide.

### 3. Risque de braconnage par les concurrents
Concentrer 200 ambassadeurs identifiés en une seule audience visible, c'est faciliter le travail des recruteurs concurrents qui auront une liste pré-qualifiée des power users d'un produit.

**Ce qui la réfuterait** : programme privé, communications individuelles, pas de page publique liste-ambassadeurs.

## Note méthodologique
Ces objections sont produites par un agent dans le rôle du sceptique. Elles ne tranchent pas.
```

---

*Skill de l'Annexe 3 du livre [Le Product Manager Augmenté](../../README.fr.md). Voir [docs/livre.md](../../docs/livre.md) — chapitre 6.*
