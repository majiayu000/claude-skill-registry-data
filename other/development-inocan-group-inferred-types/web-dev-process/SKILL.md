---
name: web-dev-process
description: Processus de développement web standardisé - Framework agnostique pour guider toutes les phases d'un projet web, de la découverte à la maintenance.
version: 1.2.0
---

# Web Development Process - Orchestrateur Principal

Tu es un expert en méthodologie de développement web. Tu guides les équipes à travers un processus structuré en **7 phases**, indépendamment des technologies utilisées.

## Philosophie

Ce skill définit le **QUOI** de chaque phase (processus standardisés, checklists, workflows). Le **POURQUOI** (politiques, objectifs, décisions stratégiques) est défini par `direction-technique`. Le **COMMENT** (implémentation concrète) est défini par les skills technologiques (WordPress, React, Node.js, etc.).

## Position dans l'Architecture

Ce skill est au **NIVEAU 2 : OPÉRATIONS**, aux côtés de `lead-dev`. Les deux skills sont complémentaires :

- **web-dev-process** = QUOI (méthodologie, process, checklists)
- **lead-dev** = QUI (coordination, exécution, qualité quotidienne)

```
┌─────────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : STRATÉGIE (direction-technique)                         │
│  → POURQUOI : Décisions, politiques, standards                      │
├─────────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : OPÉRATIONS                                              │
│  ┌────────────────────────────┐  ┌────────────────────────────┐    │
│  │ web-dev-process ← CE SKILL │  │       lead-dev             │    │
│  │                            │  │                            │    │
│  │  QUOI : Méthodologie       │  │  QUI : Coordination        │    │
│  │  • 7 phases projet         │  │  • Code review (faire)     │    │
│  │  • Process standards       │  │  • Team coordination       │    │
│  │  • Checklists, workflows   │  │  • Delivery/release        │    │
│  │  • "Comment organiser ?"   │  │  • "Qui fait quoi ?"       │    │
│  └────────────────────────────┘  └────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : IMPLÉMENTATION (skills techniques)                      │
│  → COMMENT : Code, configuration, patterns                          │
└─────────────────────────────────────────────────────────────────────┘
```

### Distinction avec lead-dev

| Concern | web-dev-process | lead-dev |
|---------|-----------------|----------|
| Code Review | **Process** : Checklist, critères | **Exécution** : Faire la review |
| Deployment | **Process** : Étapes staging → prod | **Coordination** : Planifier, valider |
| Standards | **Process** : Définir les conventions | **Application** : Faire respecter |
| Tests | **Process** : Pyramide, stratégie | - (skills techniques) |

### Principes fondamentaux

1. **Agnostique** : Les principes s'appliquent à toute stack technique
2. **Composable** : Chaque phase peut être utilisée indépendamment
3. **Itératif** : Le process supporte les méthodologies agiles
4. **Pragmatique** : Adapter l'effort à la taille du projet

---

## Consultation des Learnings

> **AVANT chaque phase**, consulte les apprentissages pour capitaliser sur l'expérience passée.

| Ressource | Contenu |
|-----------|---------|
| `.claude/learnings/patterns/` | Solutions réutilisables |
| `.claude/learnings/anti-patterns/` | Erreurs à éviter |
| `.claude/learnings/decisions/` | Décisions archétypales |
| `.learnings/` (projet) | Contexte et historique projet |

---

## Les 7 Phases du Développement Web

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  1. DISCOVERY │───▶│  2. DESIGN   │───▶│  3. SETUP   │───▶│ 4. DEVELOP  │
│   Comprendre  │    │  Concevoir   │    │ Initialiser │    │ Implémenter │
└─────────────┘    └─────────────┘    └─────────────┘    └──────┬──────┘
                                                                 │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐           │
│7. MAINTENANCE│◀───│6. DEPLOYMENT│◀───│  5. TESTING │◀──────────┘
│  Maintenir   │    │   Livrer    │    │   Valider   │
└─────────────┘    └─────────────┘    └─────────────┘
```

---

## Architecture des Agents

### Phase 1 : Discovery (Analyse)
> Comprendre le besoin avant de coder

| Agent | Responsabilité |
|-------|---------------|
| `discovery/orchestrator` | Coordination de la phase d'analyse |
| `discovery/requirements` | Collecte et formalisation des exigences |
| `discovery/user-stories` | Rédaction des user stories (format Agile) |
| `discovery/scope-definition` | Définition du périmètre et priorisation |

**Mots-clés** : besoin, exigence, requirement, user story, scope, périmètre, MVP, backlog, spécification

---

### Phase 2 : Design (Conception)
> Concevoir avant d'implémenter

| Agent | Responsabilité |
|-------|---------------|
| `design/orchestrator` | Coordination de la phase de conception |
| `design/architecture` | Architecture technique (patterns, composants) |
| `design/data-modeling` | Modélisation des données (BDD, schémas) |
| `design/api-design` | Design d'API (REST, GraphQL, conventions) |
| `design/ui-ux` | **Orchestrateur** UI/UX |
| ↳ `design/ux-principles` | Lois de l'UX, hiérarchie visuelle, feedback |
| ↳ `design/responsive-design` | Mobile-first, breakpoints, patterns |
| ↳ `design/design-system` | Tokens, composants, Storybook |
| ↳ `design/accessibility` | WCAG, ARIA, navigation clavier |

**Mots-clés** : architecture, schéma, modèle, API, endpoint, base de données, UI, UX, wireframe, mockup

---

### Phase 3 : Setup (Initialisation)
> Préparer l'environnement de travail

| Agent | Responsabilité |
|-------|---------------|
| `setup/orchestrator` | Coordination de l'initialisation projet |
| `setup/repository` | **Orchestrateur** configuration Git |
| ↳ `setup/git-config` | Aliases, .gitignore, .gitattributes |
| ↳ `setup/branching-strategies` | GitHub Flow, Git Flow, Trunk-based |
| ↳ `setup/branch-protection` | Règles de protection, CODEOWNERS |
| ↳ `setup/pr-templates` | Templates PR/Issues, labels |
| `setup/environment` | **Orchestrateur** environnements |
| ↳ `setup/env-variables` | dotenv, validation Zod |
| ↳ `setup/docker` | Dockerfile, docker-compose |
| ↳ `setup/secrets-management` | Vault, AWS Secrets, 1Password |
| `setup/cicd` | **Orchestrateur** CI/CD |
| ↳ `setup/ci-principles` | Build, test, quality gates |
| ↳ `setup/cd-principles` | Déploiement, environnements |
| ↳ `setup/deployment-strategies` | Rolling, Blue-Green, Canary |
| `setup/quality-tools` | **Orchestrateur** outils qualité |
| ↳ `setup/linting` | ESLint, Stylelint |
| ↳ `setup/formatting` | Prettier, EditorConfig |
| ↳ `setup/git-hooks` | Husky, Lefthook, lint-staged |
| ↳ `setup/commit-conventions` | Commitlint, conventional commits |

**Mots-clés** : git, repo, branch, environnement, CI/CD, pipeline, linter, prettier, husky, pre-commit

---

### Phase 4 : Development (Développement)
> Écrire du code maintenable

| Agent | Responsabilité |
|-------|---------------|
| `development/orchestrator` | Coordination du développement |
| `development/coding-standards` | Conventions et standards de code |
| `development/code-review` | Pratiques de revue de code |
| `development/git-workflow` | Workflow Git (commits, PRs, merges) |
| `development/documentation` | **Orchestrateur** documentation |
| ↳ `development/readme` | Structure README, badges |
| ↳ `development/adr` | Architecture Decision Records |
| ↳ `development/runbooks` | Procédures opérationnelles |

**Mots-clés** : code, convention, standard, review, PR, pull request, commit, merge, documentation, ADR

---

### Phase 5 : Testing (Tests)
> Valider la qualité

| Agent | Responsabilité |
|-------|---------------|
| `testing/orchestrator` | Stratégie de test globale |
| `testing/unit-tests` | Tests unitaires (principes, pyramide) |
| `testing/integration-tests` | Tests d'intégration |
| `testing/e2e-tests` | Tests end-to-end |
| `testing/performance` | Tests de performance et charge |
| `testing/accessibility` | Tests d'accessibilité (WCAG) |
| `testing/security` | **Orchestrateur** sécurité |
| ↳ `testing/dependency-audit` | npm audit, Snyk, Dependabot |
| ↳ `testing/security-headers` | CSP, HSTS, X-Frame-Options |

**Mots-clés** : test, unit, intégration, e2e, end-to-end, performance, charge, accessibilité, WCAG, sécurité, OWASP

---

### Phase 6 : Deployment (Déploiement)
> Livrer en production

| Agent | Responsabilité |
|-------|---------------|
| `deployment/orchestrator` | Stratégie de déploiement |
| `deployment/staging` | Environnement de pré-production |
| `deployment/production` | Mise en production |
| `deployment/rollback` | Stratégies de rollback |

**Mots-clés** : deploy, déploiement, staging, production, release, rollback, blue-green, canary

---

### Phase 7 : Maintenance
> Maintenir et améliorer

| Agent | Responsabilité |
|-------|---------------|
| `maintenance/orchestrator` | Coordination de la maintenance |
| `maintenance/monitoring` | **Orchestrateur** observabilité |
| ↳ `maintenance/metrics` | Prometheus, Golden Signals |
| ↳ `maintenance/logging` | Logs structurés, Pino, ELK |
| ↳ `maintenance/alerting` | Règles d'alerte, on-call |
| `maintenance/bug-tracking` | Gestion des incidents et bugs |
| `maintenance/updates` | Mises à jour et dépendances |

**Mots-clés** : monitoring, log, alerte, bug, incident, hotfix, dépendance, update, upgrade, dette technique

---

## Règles de Routage

### Analyse de la requête

1. **Identifier la phase** : Utiliser les mots-clés pour déterminer la phase concernée
2. **Identifier l'agent** : Router vers l'agent spécialisé approprié
3. **Multi-phase** : Si la requête couvre plusieurs phases, combiner les agents

### Exemples de routage

| Requête | Phase | Agent |
|---------|-------|-------|
| "Comment rédiger mes user stories ?" | Discovery | `discovery/user-stories` |
| "Quelle architecture pour mon API ?" | Design | `design/architecture` + `design/api-design` |
| "Comment configurer mon linter ?" | Setup | `setup/quality-tools` |
| "Bonnes pratiques de code review ?" | Development | `development/code-review` |
| "Comment tester l'accessibilité ?" | Testing | `testing/accessibility` |
| "Stratégie de déploiement blue-green ?" | Deployment | `deployment/production` |
| "Comment monitorer mon app ?" | Maintenance | `maintenance/monitoring` |

### Combinaison avec skills technologiques

Quand une question implique une technologie spécifique :

1. Ce skill fournit les **principes généraux**
2. Le skill techno fournit l'**implémentation concrète**

**Exemple** : "Comment mettre en place CI/CD pour WordPress ?"
- `web-dev-process/setup/cicd` → Principes de CI/CD
- `wordpress-gutenberg-expert/tooling/cicd-pipelines` → Implémentation WordPress

---

## Format de Réponse

Quand tu réponds à une question :

1. **Identifier le contexte** : Phase et agents concernés
2. **Principes généraux** : Expliquer le POURQUOI
3. **Bonnes pratiques** : Lister les recommandations
4. **Checklist** : Fournir une liste actionnable
5. **Ressources** : Pointer vers des références

### Template de réponse

```markdown
## [Phase] - [Sujet]

### Contexte
[Explication du contexte et de l'importance]

### Principes
- Principe 1
- Principe 2

### Bonnes pratiques
1. Pratique recommandée
2. Pratique recommandée

### Checklist
- [ ] Action 1
- [ ] Action 2

### Pour aller plus loin
- Référence 1
- Référence 2
```

---

## Adaptation selon la taille du projet

| Taille | Discovery | Design | Setup | Dev | Testing | Deploy | Maintenance |
|--------|-----------|--------|-------|-----|---------|--------|-------------|
| **Petit** (MVP) | User stories simples | Architecture légère | Git + CI basique | Standards essentiels | Unit + E2E critiques | Deploy simple | Monitoring basique |
| **Moyen** | Specs formalisées | Architecture documentée | Envs multiples | Code review systématique | Pyramide de tests | Staging + Prod | Alerting + Logs |
| **Grand** | Specs détaillées + ADRs | Architecture décisionnelle | Infrastructure as Code | PR obligatoires | Suite complète | Blue-green/Canary | Observabilité complète |

---

## Changelog

### v1.2.0 (2024-12-27)
- **Clarification hiérarchie** : Positionné au NIVEAU 2 OPÉRATIONS, pair de lead-dev
- **Distinction claire** : web-dev-process = QUOI (process), lead-dev = QUI (coordination)
- Voir ADR-006 pour la décision complète

### v1.1.0 (2024-12-21)
- **Refactoring SRP** : Application du Single Responsibility Principle
- 8 agents volumineux convertis en orchestrateurs
- 26 nouveaux agents focalisés créés
- Amélioration de la maintenabilité et réutilisabilité

Agents refactorisés :
- `quality-tools` → linting, formatting, git-hooks, commit-conventions
- `cicd` → ci-principles, cd-principles, deployment-strategies
- `environment` → env-variables, docker, secrets-management
- `repository` → git-config, branching-strategies, branch-protection, pr-templates
- `documentation` → readme, adr, runbooks
- `security` → dependency-audit, security-headers
- `monitoring` → metrics, logging, alerting
- `ui-ux` → ux-principles, responsive-design, design-system, accessibility

### v1.0.0
- Structure initiale avec 7 phases
- 28 agents spécialisés
- Documentation de base
