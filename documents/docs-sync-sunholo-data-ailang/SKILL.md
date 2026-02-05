---
name: docs-sync
description: Synchronise la documentation avec le code. Utilise ce skill quand l'utilisateur dit "sync docs", "met à jour la doc", "vérifie la doc", "avant de merge", ou termine une branche. Analyse les changements et met à jour les specs (.claude/specs/).
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Documentation Sync Agent

## Objectif

Analyser les changements de la branche courante et mettre à jour les fichiers de spécifications dans `.claude/specs/` pour qu'ils restent synchronisés avec le code.

## Fichiers de specs à maintenir

| Fichier | Surveille | Met à jour si... |
|---------|-----------|------------------|
| `ARCHITECTURE.md` | prisma/schema.prisma, auth.ts, utils/ai-model.tsx, structure dossiers | Nouveaux modèles, providers, patterns |
| `PRD.md` | README.md, nouvelles features, CHANGELOG.md | Nouvelles fonctionnalités |
| `API.md` | app/actions/*.ts, app/api/*, utils/schemas.ts | Nouvelles actions, routes, schémas |
| `SECURITY.md` | utils/encryption.ts, auth.ts, .env changes | Changements auth, chiffrement |

## Workflow

### 1. Identifier la branche et les changements

```bash
# Branche courante
git branch --show-current

# Fichiers modifiés vs develop
git diff develop --name-only

# Diff détaillé
git diff develop --stat
```

### 2. Catégoriser les changements

Analyser les fichiers modifiés et les mapper aux specs:

| Pattern de fichier | Spec impactée |
|--------------------|---------------|
| `prisma/schema.prisma` | ARCHITECTURE.md (schéma DB) |
| `auth.ts` | ARCHITECTURE.md + SECURITY.md |
| `utils/ai-model.tsx` | ARCHITECTURE.md (providers) |
| `app/actions/*.ts` | API.md (server actions) |
| `app/api/**/*.ts` | API.md (routes) |
| `utils/schemas.ts` | API.md (schémas Zod) |
| `utils/encryption.ts` | SECURITY.md |
| `components/**` | Potentiellement ARCHITECTURE.md |
| `locales/*.ts` | PRD.md si nouvelles features |

### 3. Lire les fichiers modifiés

Pour chaque fichier modifié pertinent:
1. Lire le contenu actuel
2. Comprendre les changements (git diff)
3. Identifier les sections de specs à mettre à jour

### 4. Mettre à jour les specs

Pour chaque spec impactée:
1. Lire le fichier spec actuel
2. Identifier la section à modifier
3. Mettre à jour avec les nouvelles informations
4. Garder le format et le style existants

### 5. Résumer les changements

Afficher un récapitulatif:
- Fichiers analysés
- Specs mises à jour
- Sections modifiées

## Règles de mise à jour

### ARCHITECTURE.md

**Schéma DB** - Si `prisma/schema.prisma` modifié:
- Ajouter/modifier les modèles dans le diagramme ASCII
- Mettre à jour les relations
- Ajouter les nouveaux enums

**Providers IA** - Si `utils/ai-model.tsx` modifié:
- Mettre à jour la table des modèles
- Ajouter les nouveaux providers

**Auth** - Si `auth.ts` modifié:
- Mettre à jour la section "Flow d'Authentification"

### API.md

**Server Actions** - Si `app/actions/*.ts` modifié:
- Ajouter les nouvelles actions dans la table correspondante
- Documenter input/output
- Ajouter les nouveaux codes d'erreur

**Routes API** - Si `app/api/**` modifié:
- Documenter la nouvelle route
- Ajouter le schéma de validation
- Lister les codes d'erreur

**Schémas** - Si `utils/schemas.ts` modifié:
- Mettre à jour la section "Schémas Zod"

### SECURITY.md

**Chiffrement** - Si `utils/encryption.ts` modifié:
- Documenter les changements d'algorithme
- Mettre à jour les flux

**Auth** - Si `auth.ts` ou config auth modifié:
- Mettre à jour la section authentification
- Documenter les nouveaux providers OAuth

**Variables env** - Si nouvelles variables sensibles:
- Ajouter à la table des variables

### PRD.md

**Features** - Si nouvelle fonctionnalité majeure:
- Ajouter dans la table des features
- Créer les user stories si pertinent

**Roadmap** - Si feature de la roadmap implémentée:
- Mettre à jour le statut

## Exemple d'exécution

```
User: "sync docs" ou "vérifie la doc avant merge"

Agent:
1. git diff develop --name-only
   → prisma/schema.prisma (modifié)
   → app/actions/user-projects.ts (nouveau)
   → utils/ai-model.tsx (modifié)

2. Analyse:
   - Nouveau modèle Project dans Prisma
   - Nouvelles actions CRUD pour projets
   - Nouveau provider IA ajouté

3. Mises à jour:
   - ARCHITECTURE.md: ajout modèle Project dans schéma DB
   - ARCHITECTURE.md: nouveau provider dans la table
   - API.md: nouvelles actions user-projects documentées

4. Résumé affiché à l'utilisateur
```

## Format de sortie

```markdown
## 📝 Documentation Sync Report

### Fichiers analysés
- `prisma/schema.prisma` → changements détectés
- `app/actions/user-projects.ts` → nouveau fichier
- `utils/ai-model.tsx` → changements détectés

### Specs mises à jour

#### ARCHITECTURE.md
- ✅ Ajout du modèle `Project` dans le schéma DB
- ✅ Ajout du provider `NewProvider` dans la table

#### API.md
- ✅ Documentation des actions `user-projects.ts`
  - `getAllUserProjects`
  - `createProject`
  - `updateProject`
  - `deleteProject`

### Aucune mise à jour nécessaire
- PRD.md
- SECURITY.md
```

## Commandes déclencheurs

- "sync docs"
- "met à jour la doc"
- "vérifie la documentation"
- "avant de merge"
- "finalise la branche"
- "prépare la PR"
