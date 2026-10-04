---
name: onboarding-pm
description: Utiliser à chaque arrivée d'un nouveau Product Manager dans l'équipe pour produire un parcours d'onboarding sur mesure. Produit les questions clés à poser à la base, les décisions structurantes récentes, les zones de tension, les rencontres prioritaires et un projet introductif.
version: 0.1.0
author: Ludovic Lefebvre
license: MIT
language: fr
book:
  title: Le Product Manager Augmenté
  annex: A3
tags: [management, onboarding, ramp-up]
---

# onboarding-pm

## Fiche éditoriale

**Objectif.** Produire un parcours d'onboarding pour un nouveau PM rejoignant l'équipe.

**Entrées.** Profil du nouveau PM, périmètre, base documentaire accessible.

**Sorties.** Questions clés à poser à la base, décisions structurantes récentes, zones de tension, rencontres prioritaires, projet introductif.

**Cadence d'usage.** À chaque nouvelle arrivée.

## Mode opératoire

### Quand m'invoquer

Un nouveau PM arrive et l'utilisateur (manager ou pair) prépare son parcours d'onboarding. Il me fournit le profil du nouveau PM (séniorité, contexte précédent, forces, lacunes connues), le périmètre qu'il va prendre, et l'accès à la base documentaire produit.

### Procédure

1. **Lire la base documentaire** dans la limite de ce qui est accessible : roadmap actuelle, décisions récentes, journal de décision si disponible, notes de discovery, OKR.
2. **Adapter le parcours au profil** : un PM senior n'a pas besoin du même onboarding qu'un PM junior. Calibrer les rencontres prioritaires, le projet introductif, et le niveau de détail.
3. **Produire les 8-12 questions-clés** que le nouveau PM devrait poser à la base documentaire dans sa première semaine. Une bonne question est ouverte, factualisable, et révèle des zones d'ombre du périmètre.
4. **Lister les 5-8 décisions structurantes récentes** (3-6 derniers mois) que le nouveau PM doit connaître pour comprendre le contexte. Pour chacune : la décision, son contexte, son statut actuel.
5. **Identifier les zones de tension** : sujets en débat, dépendances tendues, équipes en désaccord, dette tech ou produit qui bloque. À traiter en lecture orale (au cours d'une 1:1), pas dans un doc public.
6. **Recommander 5-8 rencontres prioritaires** : qui voir, dans quel ordre, sur quoi. Inclure systématiquement : un dev senior, un user / customer success, un stakeholder business.
7. **Définir un projet introductif** : un sujet limité, livrable en 4-6 semaines, qui force le nouveau PM à toucher tous les segments du périmètre sans porter d'enjeu critique.
8. Produire la sortie au format ci-dessous.

### Format de sortie

```markdown
# Onboarding PM — {prénom du nouveau PM}

## Profil et calibrage
- Séniorité : ...
- Contexte précédent : ...
- Périmètre confié : ...
- Calibrage retenu : {détaillé / accéléré / mixte}

## Questions-clés à poser à la base documentaire (semaine 1)

1. ...
2. ...
3. ...
... (8-12)

## Décisions structurantes récentes (3-6 derniers mois)

### {date} — {décision}
- Contexte : ...
- Statut actuel : ...
- Ce qu'il faut savoir : ...

### {date} — {décision}
... (5-8 entrées)

## Zones de tension (à traiter en 1:1, pas en doc partagé)

- ...
- ...

## Rencontres prioritaires (semaines 1-3)

| Personne | Rôle | Sujet | Quand |
|----------|------|-------|-------|
| ... | ... | ... | semaine X |

## Projet introductif

**Sujet** : ...
**Périmètre limité** : ...
**Livrable attendu** : ...
**Échéance** : 4-6 semaines
**Pourquoi ce sujet** : touche {zones du périmètre} sans enjeu critique sur la roadmap principale.

## Calendrier des trois premières semaines

### Semaine 1
- ...

### Semaine 2
- ...

### Semaine 3
- ...
```

### Garde-fous

- **Calibrage du niveau de détail selon la séniorité** : un parcours pour PM senior est plus court (2-3 semaines), un parcours junior est plus encadré (4-6 semaines).
- **Zones de tension confidentielles** : ces sujets ne sont jamais dans un doc partagé, seulement transmis à l'oral.
- **Questions-clés ouvertes** : ce ne sont pas des QCM. Elles forcent une exploration.
- **Projet introductif sans pression** : pas de livrable critique, pas de dépendance bloquante. Le but est l'apprentissage.
- **Pas de jugement sur les anciennes décisions** : les décisions passées sont présentées factuellement, pas critiquement. Le nouveau PM se fera son avis.
- **Anonymisation des zones de tension** dans tout export public. Pas de "X a un problème avec Y".

### Exemple

**Input** :
> Nouveau PM : Sarah, 4 ans d'expérience PM B2B SaaS, vient d'une scale-up data. Périmètre : pricing & monétisation. Base doc : Notion + journal de décision.

**Output (extrait)** :

```markdown
# Onboarding PM — Sarah

## Profil et calibrage
- Séniorité : confirmé (4 ans, B2B SaaS)
- Contexte précédent : pricing existant chez précédent employeur ✓
- Périmètre confié : pricing & monétisation
- Calibrage retenu : accéléré (3 semaines)

## Questions-clés à poser à la base documentaire

1. Quelle a été l'évolution du pricing depuis la création du produit ? Quelles décisions structurantes ?
2. Existe-t-il un test pricing en cours ou récent (≤ 12 mois) et quels enseignements ?
3. Quels sont les 3 segments de clientèle qui contribuent le plus au revenu ? Quelle est leur élasticité prix observée ?
4. Quelle est la marge brute actuelle par tier et par segment ?
5. Quelles features sont actuellement upsells et lesquelles ont été testées sans succès ?
6. Quelle est la position vs concurrence sur le pricing (benchmark récent disponible) ?
7. Existe-t-il un pricing géographique et sur quelles bases ?
8. Quels sont les commentaires les plus fréquents sur le pricing en NPS et support ?
9. Quelles sont les contraintes commerciales / contractuelles (clauses MFN, accords cadres) ?
10. Quel est l'état du modèle d'attribution revenu par feature ?

## Décisions structurantes récentes

### 2026-01-15 — Bascule annual-first
- Contexte : friction observée sur l'engagement long terme
- Statut : déployé, métriques positives sur 60 j
- Ce qu'il faut savoir : la décision a été contestée par sales — voir compte rendu

### 2025-11-08 — Suppression du tier "Starter"
- Contexte : <3% du revenu, support disproportionné
- Statut : effectif depuis le 1er janvier
- Ce qu'il faut savoir : 30 clients legacy migrés à la main, point d'attention historique
...
```

---

*Skill de l'Annexe 3 du livre [Le Product Manager Augmenté](../../README.fr.md). Voir [docs/livre.md](../../docs/livre.md) — chapitre 13.*
