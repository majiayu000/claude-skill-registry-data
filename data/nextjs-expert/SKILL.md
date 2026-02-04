---
name: nextjs-expert
description: Expert Next.js - App Router, Server Components, Server Actions, data fetching, rendering strategies, optimization et déploiement
version: 1.0.0
status: active
---

# Next.js Expert Skill

## Quick Start

```bash
# 1. Navigation rapide vers un agent
nextjs-expert/agents/app-router/routing      # Routes et structure
nextjs-expert/agents/data/server-actions     # Mutations avec Server Actions
nextjs-expert/agents/optimization/images     # Optimiser les images

# 2. Exécuter les tests de validation
cd .claude/skills/nextjs-expert && npm test

# 3. Questions fréquentes
"Comment créer une route dynamique ?"    → app-router/routing
"Server vs Client Component ?"            → server-components/server-vs-client
"Comment fetcher des données ?"           → data/data-fetching
"Optimiser le LCP ?"                      → optimization/images + fonts
"Déployer sur Vercel ?"                   → deployment/vercel
```

## Position dans l'Architecture

Ce skill est un skill de **NIVEAU 3 : COMMENT** (implémentation). Il fournit le code et les configurations concrètes pour le développement Next.js.

```
┌─────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : POURQUOI (direction-technique)                      │
│  → Décisions stratégiques, choix de stack, ADRs                 │
│  → Pourquoi Next.js ? Quelle stratégie de rendu ?               │
├─────────────────────────────────────────────────────────────────┤
│  COORDINATION (lead-dev)                                        │
│  → Coordination opérationnelle, qualité quotidienne             │
│  → Comment organiser le code ? Valider les PRs ?                │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : QUOI (web-dev-process)                              │
│  → Process, workflows, checklists, standards                    │
│  → Comment organiser les tests ? Quel workflow ?                │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : COMMENT (nextjs-expert) ← CE SKILL                  │
│  → Implémentation, code, configuration                          │
│  → Comment créer ce Server Component ? Configurer le cache ?    │
└─────────────────────────────────────────────────────────────────┘
```

## Philosophie

Ce skill fournit l'**implémentation concrète** pour le développement Next.js 14+. Il contient :
- ✅ Du code (React, TypeScript, Server Components...)
- ✅ Des configurations (next.config.js, middleware...)
- ✅ Des patterns d'implémentation App Router
- ✅ Des exemples concrets et prêts à l'emploi

Il ne contient PAS :
- ❌ Des décisions stratégiques → `direction-technique`
- ❌ Des processus de travail → `web-dev-process`
- ❌ Du React générique → `react-expert`
- ❌ Du CSS/styling générique → `frontend-developer`

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            frontend-developer                                │
│                         (COMMENT - 33 agents)                               │
│                     Implémentation frontend générique                        │
│                                                                              │
│  frameworks/nextjs-expert → Délégation vers CE SKILL                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            nextjs-expert                                     │
│                         (COMMENT - 35 agents)                               │
│                      Implémentation Next.js                                  │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          7 DOMAINES                                   │   │
│  │                                                                       │   │
│  │  app-router/       server-components/      data/         rendering/  │   │
│  │      (5)                  (5)              (5)              (5)      │   │
│  │                                                                       │   │
│  │  optimization/         deployment/         testing/                  │   │
│  │      (5)                  (5)               (5)                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Domaines et Agents (35 agents)

### 1. app-router/ - App Router (5 agents)

Code et patterns pour le App Router Next.js 14+.

| Agent | Responsabilité | Produit |
|-------|----------------|---------|
| `orchestrator` | Coordination | Routage |
| `routing` | Routes, segments, groupes | Code routes, layouts |
| `layouts` | Layouts, templates, loading | Code UI structure |
| `navigation` | Link, useRouter, redirects | Code navigation |
| `error-handling` | error.tsx, not-found.tsx | Code gestion erreurs |

### 2. server-components/ - React Server Components (5 agents)

Implémentation des Server Components et Client Components.

| Agent | Responsabilité | Produit |
|-------|----------------|---------|
| `orchestrator` | Coordination | Routage |
| `server-vs-client` | Choix SC vs CC, "use client" | Code composants |
| `async-components` | Composants async, await | Code async |
| `streaming` | Suspense, streaming SSR | Code streaming |
| `composition` | Patterns de composition | Code patterns |

### 3. data/ - Gestion des Données (5 agents)

Data fetching, mutations et caching.

| Agent | Responsabilité | Produit |
|-------|----------------|---------|
| `orchestrator` | Coordination | Routage |
| `data-fetching` | fetch, cache côté serveur | Code fetching |
| `server-actions` | Server Actions, mutations | Code actions |
| `revalidation` | Cache strategies, tags, ISR | Config cache |
| `client-fetching` | SWR, React Query | Code client |

### 4. rendering/ - Stratégies de Rendu (5 agents)

SSR, SSG, ISR et rendu dynamique.

| Agent | Responsabilité | Produit |
|-------|----------------|---------|
| `orchestrator` | Coordination | Routage |
| `ssr-ssg` | SSR vs SSG, generateStaticParams | Code rendu |
| `isr` | ISR, revalidation périodique | Config ISR |
| `middleware` | Middleware, redirections | Code middleware |
| `edge-runtime` | Edge Functions, config | Code Edge |

### 5. optimization/ - Optimisation (5 agents)

Performance et Core Web Vitals.

| Agent | Responsabilité | Produit |
|-------|----------------|---------|
| `orchestrator` | Coordination | Routage |
| `images` | next/image, formats, placeholder | Code images |
| `fonts` | next/font, loading, subsets | Code fonts |
| `bundle` | @next/bundle-analyzer, code split | Config analyse |
| `caching` | Cache strategies, headers | Config cache |

### 6. deployment/ - Déploiement (5 agents)

Déploiement et configuration production **spécifique Next.js**.

> **Note : Différence avec lead-dev/delivery/**
> - `nextjs-expert/agents/deployment/` = **Implémentation technique** : Vercel, Docker, CI/CD *pour Next.js*
> - `lead-dev/delivery/` = **Processus de release** : planification, vérifications, hotfixes, release notes
>
> Exemple : `lead-dev/delivery/deployment-check` vérifie qu'on est prêt à déployer,
> puis `nextjs-expert/agents/deployment/vercel` effectue le déploiement technique.

| Agent | Responsabilité | Produit |
|-------|----------------|---------|
| `orchestrator` | Coordination | Routage |
| `vercel` | Déploiement Vercel | Config Vercel |
| `docker` | Containerisation, self-hosted | Dockerfile, compose |
| `environment` | Variables d'env, secrets | Config env |
| `ci-cd` | Pipelines GitHub/GitLab | Workflows CI |

### 7. testing/ - Tests (5 agents)

Tests unitaires, intégration et E2E.

| Agent | Responsabilité | Produit |
|-------|----------------|---------|
| `orchestrator` | Coordination | Routage |
| `unit-testing` | Jest, Vitest pour Next.js | Code tests |
| `integration-testing` | Testing Library + Next | Code tests composants |
| `e2e-testing` | Playwright pour Next.js | Code tests E2E |
| `mocking` | MSW, mocks API | Code mocks |

**Total : 35 agents spécialisés**

## Règles de Routage

### Par Type de Question

| Question | Domaine |
|----------|---------|
| Routes, layouts, navigation, URL | `app-router/` |
| Server/Client Components, streaming | `server-components/` |
| Fetch data, mutations, cache, DB | `data/` |
| SSR, SSG, ISR, middleware | `rendering/` |
| Performance, images, fonts, bundle | `optimization/` |
| Deploy, Vercel, Docker, env | `deployment/` |
| Tests Next.js | `testing/` |

### Par Mots-Clés

```
SI question contient [route, page.tsx, layout.tsx, segment, group]
   → app-router/routing

SI question contient [loading.tsx, error.tsx, not-found.tsx]
   → app-router/error-handling

SI question contient [Server Component, Client Component, "use client"]
   → server-components/server-vs-client

SI question contient [async component, await, Suspense, streaming]
   → server-components/streaming

SI question contient [Server Action, "use server", mutation, form]
   → data/server-actions

SI question contient [fetch, cache, revalidate, revalidatePath, revalidateTag]
   → data/caching

SI question contient [generateStaticParams, static, build time]
   → rendering/static-generation

SI question contient [dynamic, force-dynamic, no-store]
   → rendering/dynamic-rendering

SI question contient [ISR, revalidate: 60, on-demand]
   → rendering/incremental-static

SI question contient [middleware, Edge, NextResponse]
   → rendering/middleware

SI question contient [next/image, Image, placeholder, blur]
   → optimization/image-optimization

SI question contient [next/font, Google Fonts, local fonts]
   → optimization/font-optimization

SI question contient [Vercel, deploy, production]
   → deployment/vercel

SI question contient [Docker, container, standalone]
   → deployment/docker

SI question contient [test, Jest, Playwright, Next.js]
   → testing/
```

## Composition avec Autres Skills

### Exemple 1 : Nouvelle page avec data fetching

```
1. direction-technique/architecture
   → Décide : "Page avec ISR, revalidation 1h"

2. nextjs-expert/agents/rendering/incremental-static
   → Implémente : Config ISR

3. nextjs-expert/agents/data/data-fetching
   → Implémente : Fetch avec cache

4. nextjs-expert/agents/server-components/async-components
   → Implémente : Composant async
```

### Exemple 2 : Optimisation performance

```
1. direction-technique/performance
   → Décide : "Optimiser LCP < 2.5s"

2. nextjs-expert/agents/optimization/image-optimization
   → Implémente : next/image optimisé

3. nextjs-expert/agents/optimization/font-optimization
   → Implémente : next/font

4. nextjs-expert/agents/optimization/core-web-vitals
   → Implémente : Autres optimisations
```

## Points d'Escalade

### Vers direction-technique

- Choix de stratégie de rendu globale (full SSR vs hybrid)
- Architecture micro-frontend avec Next.js
- Choix entre Pages Router et App Router (migration)
- Décisions de caching stratégiques

### Vers react-expert

- Patterns React avancés (non spécifiques Next.js)
- State management global
- Hooks personnalisés complexes

### Vers frontend-developer

- Styling et CSS (Tailwind, CSS Modules génériques)
- Accessibilité générale
- JavaScript/TypeScript générique

### Vers l'humain

- Problèmes de configuration complexes
- Bugs Next.js non documentés
- Décisions d'architecture avec trade-offs importants

## Skills Associés

| Skill | Niveau | Relation |
|-------|--------|----------|
| `direction-technique` | POURQUOI | Définit les décisions stratégiques |
| `lead-dev` | COORDINATION | Valide les PRs, coordonne |
| `frontend-developer` | COMMENT | Délègue vers ce skill pour Next.js |
| `react-expert` | COMMENT | Patterns React génériques |
| `web-dev-process` | QUOI | Définit les processus |

## Versions Next.js Supportées

Ce skill est optimisé pour **Next.js 14+** avec App Router.

| Feature | Version Min | Notes |
|---------|-------------|-------|
| App Router | 13.4+ | Stable depuis 13.4 |
| Server Actions | 14.0+ | Stable depuis 14.0 |
| Partial Prerendering | 14.0+ | Expérimental |
| Turbopack | 14.0+ | Stable en dev |

## Tests de Validation

Le skill inclut des tests automatisés pour valider sa structure.

```bash
# Exécuter les tests (depuis le dossier du skill)
cd .claude/skills/nextjs-expert
npm test

# Mode verbose
npm run test:verbose

# Tests individuels
npm run test:domains
npm run test:agents
npm run test:skill
```

Les tests vérifient :
- ✅ Existence de tous les domaines
- ✅ Présence de tous les agents attendus
- ✅ Frontmatter YAML valide (name, description)
- ✅ Structure des agents (sections requises)
- ✅ Références croisées (escalades)

## Intégration CI

Les tests sont automatiquement exécutés via GitHub Actions :

- **Workflow** : `.github/workflows/nextjs-expert-tests.yml`
- **Déclenchement** : Push sur `main` ou PR modifiant `.claude/skills/nextjs-expert/**`
- **Rapport** : Commentaire automatique sur la PR avec les résultats

| Badge | Description |
|-------|-------------|
| ✅ Pass | Tous les tests passent |
| ❌ Fail | Au moins un test échoue |

```yaml
# Vérifier le status localement avant de push
npm test
```

## Exemples de Workflows End-to-End

### Workflow 1 : Développeur crée une nouvelle page avec data

```
1. 🧑‍💻 Développeur demande : "Créer une page produits avec SSG"

2. → nextjs-expert/agents/rendering/ssr-ssg
   Répond : Code generateStaticParams + page.tsx

3. → nextjs-expert/agents/data/data-fetching
   Répond : Code fetch avec cache

4. → nextjs-expert/agents/server-components/async-components
   Répond : Pattern composant async

5. 🧑‍💻 PR créée → lead-dev/code-review/pr-review
   Valide : Structure, patterns, performance
```

### Workflow 2 : Optimisation performance après audit

```
1. 🧑‍💻 Demande : "LCP trop lent, optimiser"

2. → nextjs-expert/agents/optimization/images
   Répond : Config next/image, priority, sizes

3. → nextjs-expert/agents/optimization/fonts
   Répond : next/font avec display: swap

4. → nextjs-expert/agents/optimization/bundle
   Répond : Dynamic imports, analyze bundle

5. → lead-dev/code-review/performance-review
   Valide : Impact Core Web Vitals
```

### Workflow 3 : Implémentation Server Actions

```
1. 🧑‍💻 Demande : "Formulaire de contact avec Server Action"

2. → nextjs-expert/agents/data/server-actions
   Répond : Code "use server", form action

3. → nextjs-expert/agents/data/revalidation
   Répond : revalidatePath après mutation

4. → nextjs-expert/agents/app-router/error-handling
   Répond : Gestion erreurs useFormState

5. → nextjs-expert/agents/testing/integration-testing
   Répond : Tests avec Testing Library
```

## Changelog

### v1.0.0
- Création initiale avec 7 domaines et 35 agents
- Focus sur App Router et Server Components
- Positionnement COMMENT dans la hiérarchie
- Intégration avec frontend-developer
- Tests de validation inclus
