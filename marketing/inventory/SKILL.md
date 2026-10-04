---
name: inventory
description: Tient l'inventaire central des livrables de {{COMPANY_NAME}} dans _templates/inventory.md — tout post, carrousel, email, deck, page ou image produit y est indexé (date, canal, sujet, chemin, statut). Deux modes — reconstruction (scan complet des dossiers de production) et incrément (ajout après chaque livrable). À consulter avant toute création de contenu pour éviter les doublons.
---

# inventory — index central des livrables

Tu maintiens **`_templates/inventory.md`**, l'index unique de TOUS les livrables produits par le cockpit : posts, carrousels, emails, slides, pages, images. C'est la mémoire de production du repo — la première chose qu'une skill de production consulte avant de créer.

## Format du fichier

`_templates/inventory.md` est un tableau Markdown trié **du plus récent au plus ancien** :

```markdown
# Inventaire des livrables — {{COMPANY_NAME}}

> Fichier maintenu par la skill `inventory`. Ne pas éditer à la main ; lancer une reconstruction en cas de doute.
> Dernière mise à jour : YYYY-MM-DD (mode : reconstruction | incrément)

| Date | Canal | Type | Sujet | Chemin | Statut |
|---|---|---|---|---|---|
| 2026-07-01 | linkedin | carrousel | Lancement offre X | 06-graphic-design/carousels/offre-x/ | publié |
| 2026-06-28 | newsletter | email | Édition juin | 04-email/newsletter/editions/2026-06.md | publié |
```

Conventions de valeurs :
- **Date** : date de création du livrable (`YYYY-MM-DD`), pas la date d'indexation.
- **Canal** : `linkedin`, `discord`, `whatsapp`, `newsletter`, `email-promo`, `web`, `blog`, `event`, `slides`, `visuel`.
- **Type** : `post`, `carrousel`, `email`, `article`, `landing`, `deck`, `image`, `plan-comm`.
- **Sujet** : 5-10 mots, assez précis pour détecter un doublon à la lecture.
- **Chemin** : relatif à la racine du repo.
- **Statut** : `brouillon`, `validé`, `publié`, `archivé`.

## Mode 1 — Reconstruction (scan complet)

À utiliser à l'initialisation, après un doute sur la fraîcheur de l'index, ou périodiquement (ex. mensuel).

1. Scanner les dossiers de production `03-` à `09-` :
   - `03-social-media/` — posts par canal, y compris `*/examples/` (contenus publiés archivés)
   - `04-email/` — `newsletter/{drafts,editions}/`, promos, séquences
   - `05-web-content/` — landing pages, artefacts HTML
   - `06-graphic-design/` — visuels, carrousels, `presentations/decks/`
   - `07-events/` — plans de comm, scripts
   - `09-seo/` — articles, briefs
2. **Exclure** : `CLAUDE.md`, `README.md`, `templates/`, `briefs/`, scripts (`.py`, `.js`, `.sh`), fichiers marqués `[WIP]`.
3. Pour chaque fichier retenu, déduire date (frontmatter ou nom de fichier, sinon date de modification), canal, type, sujet (titre ou première ligne), statut (dossier `drafts/` → `brouillon` ; `editions/`, `examples/`, `decks/` → `publié` ; `archives/` → `archivé` ; sinon `validé`).
4. Réécrire `_templates/inventory.md` en entier (créer le fichier s'il n'existe pas), trié par date décroissante.
5. Annoncer le bilan : N livrables indexés, répartition par canal, anomalies (fichiers sans date identifiable).

## Mode 2 — Incrément (après chaque livrable)

À utiliser à chaque fin de production d'un livrable (juste après le brand-check).

1. Lire `_templates/inventory.md`. S'il n'existe pas → basculer en mode reconstruction d'abord.
2. Vérifier que le chemin n'est pas déjà indexé ; si oui, mettre à jour la ligne (statut, sujet) au lieu d'en ajouter une.
3. Insérer la ligne en tête de tableau et mettre à jour la ligne « Dernière mise à jour ».

Quand un livrable change de statut (brouillon → publié, publié → archivé), mettre à jour la ligne existante — ne jamais dupliquer.

## Règle de consultation (pour les skills de production)

Les skills de production (`social-content`, `email`, `copywriting`, `seo`, `event-marketing`, `slides`, `image-generation`) **consultent l'inventaire avant de créer** :

1. Lire `_templates/inventory.md` et chercher les lignes proches du sujet demandé (même sujet, même canal, < 8 semaines).
2. Si un livrable similaire existe → le signaler à l'utilisateur avec son chemin, et proposer : réutiliser, décliner sous un autre angle, ou créer quand même.
3. Ce contrôle est le mécanisme d'anti-répétition de référence : l'inventaire est exhaustif, purement fichiers, et sans dépendance externe.

## Ce que cette skill ne fait PAS

- ❌ Juger la qualité ou la conformité d'un livrable (→ `brand-check`)
- ❌ Planifier le contenu (→ `content-strategy`)
- ❌ Indexer `_sources/` (matière première, pas des livrables)
