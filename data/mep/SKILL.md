---
name: mep
description: Mise en Production pour Motivia. Utilise ce skill quand l'utilisateur dit "MEP", "mise en prod", "release", "prepare version", "changelog", ou demande de préparer une nouvelle version. Gère le CHANGELOG, le bump de version, et la liaison avec Linear.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, mcp__linear__list_issues, mcp__linear__get_issue, mcp__linear__list_projects
---

# Mise en Production (MEP) Motivia

## Workflow complet

Quand l'utilisateur demande une MEP (ex: "Config MEP v1.12.0"):

### 1. Identifier la dernière version

```bash
git tag --sort=-version:refname | head -5
```

### 2. Récupérer l'historique des commits depuis le dernier tag

```bash
git log <dernier_tag>..develop --format="%H|%s|%b"
```

### 3. Analyser les tickets Linear

- Utiliser `mcp__linear__list_issues` avec le projet "Motivia"
- Filtrer par milestone si spécifié
- Chercher les références `Ref : PERSO-XX` dans les corps de commits

### 4. Générer le CHANGELOG

Format strict:

```markdown
---
### vX.X.X
---

## Features

- MIA-XX : Description de la fonctionnalité

## Miscellaneous

- MIA-XX : Description de l'amélioration

## Fixes

- MIA-XX : Description du fix
```

### 5. Règles de catégorisation

| Type commit | Catégorie CHANGELOG |
|-------------|---------------------|
| feat        | Features            |
| fix         | Fixes               |
| config, misc, docs | Miscellaneous |

### 6. Conversions

- `PERSO-XX` → `MIA-XX` dans le CHANGELOG
- Si pas de référence Linear → `MIA-X`

### 7. Exclusions

NE PAS inclure:
- Fix d'un autre ticket (ex: "fix du PERSO-XX")
- Commits purement techniques: `fix(build): lockfile`
- Commits de MEP précédents: `config(version): version and changelog`

### 8. Mise à jour package.json

Modifier le champ `version` avec la nouvelle version.

### 9. Créer le commit de MEP

```bash
git add CHANGELOG.md package.json
git commit -m "misc(config):vX.X.X"
```

## Exemple de sortie

```markdown
---
### v1.12.0
---

## Features

- MIA-25 : Ajout de l'export PDF des lettres
- MIA-27 : Nouveau dashboard avec statistiques

## Miscellaneous

- MIA-26 : Amélioration des performances de génération
- MIA-X : Mise à jour des dépendances

## Fixes

- MIA-24 : Correction de l'upload CV sur mobile
```

## Points importants

- Descriptions en français, orientées utilisateur
- Une ligne par entrée
- Features en premier, Miscellaneous après, Fixes en dernier
- Toujours vérifier Linear pour remplacer MIA-X si possible
