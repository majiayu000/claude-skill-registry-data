---
name: brainstormer
description: >-
  Feature discovery et brainstorming guide pour EPCI v5.3. Workflow avec
  personas adaptatifs, phases Divergent/Convergent, scoring EMS v2 via @ems-evaluator,
  auto-techniques via @technique-advisor (63 techniques CSV), Party Mode (5 personas),
  Expert Panel (5 dev leaders). Breakpoints via @skill:breakpoint-display (ems-status,
  plan-review, analysis, validation). Modes: standard | party | panel.
  Use when: /brainstorm invoked, feature discovery needed.
  Not for: implementation tasks, code generation, simple questions.
allowed-tools: [Read, Write, Glob, Grep, Task, AskUserQuestion]
---

# Brainstormer v5.3

## Overview

Skill de brainstorming specialise pour la decouverte de features.
Transforme des idees vagues en briefs fonctionnels complets via
un processus iteratif guide avec personas adaptatifs.

**Nouveautes v5.3:**
- **Breakpoints via skill** — Utilise `@skill:breakpoint-display` pour tous les breakpoints
- **Nouveau type ems-status** — Affichage EMS 5 axes avec barres de progression
- **~57% économie tokens** — Via skill centralisé au lieu de ASCII boxes manuelles
- **Cohérence UI** — Format unifié avec /brief et /epci

**Nouveautes v5.1:**
- **AskUserQuestion natif** — Questions via outil Claude Code (UI QCM interactive)
- **3 questions max** par iteration (au lieu de 5)
- **Headers priorité** — `🛑 Critical`, `⚠️ Important`, `ℹ️ Info` (max 12 chars)
- **Suggestions visuelles** — `(Recommended)` dans le label de l'option suggérée
- **Technique-advisor adapté** — Retourne JSON, main thread pose la question

**Nouveautes v5.0:**
- **68 techniques** en CSV (11 categories) remplacent les fichiers .md
- **Party Mode** — Discussion multi-persona collaborative (5 personas EPCI)
- **Expert Panel** — Panel 5 dev leaders (Martin, Fowler, Newman, Gamma, Beck)
- **Modes mutuellement exclusifs** — standard | party | panel
- **Random/Progressive modes** — Selection aleatoire ou par phase EMS

**Reference Documents:**
- [Personas](references/personas.md) — 3 modes de facilitation
- [EMS System](references/ems-system.md) — Scoring v2 avec 5 axes
- [Frameworks](references/frameworks.md) — 5 frameworks d'analyse
- [Techniques CSV](references/techniques.csv) — 68 techniques (11 categories)
- [Technique Mapping](references/technique-mapping.md) — EMS → categories
- [Party Personas](references/party-personas.md) — 5 personas collaboratifs (v5.0)
- [Expert Panel](references/experts/) — 5 experts dev (v5.0)
- [Brief Format](references/brief-format.md) — Template de sortie
- [Session Format](references/session-format.md) — Format YAML v1.2

**Session Storage:** `.project-memory/brainstorm-sessions/[slug].yaml`

## Personas

| Persona | Role |
|---------|------|
| **Architecte** | Structure, frameworks, synthese (DEFAUT) |
| **Sparring** | Challenge, stress-test |
| **Pragmatique** | Action, deblocage |

> Voir [personas.md](references/personas.md) pour regles de bascule

## Phases

| Phase | Focus |
|-------|-------|
| **Divergent** | Generer, explorer, quantite |
| **Convergent** | Evaluer, decider, qualite |

**Transition auto**: Couverture >= 60% ET iter >= 3

## Agents

### Core Agents

| Agent | Model | Role |
|-------|-------|------|
| `@Explore` | - | Analyse codebase initiale |
| `@clarifier` | haiku | Questions turbo mode |
| `@planner` | sonnet | Plan en phase Convergent |
| `@security-auditor` | opus | Audit securite conditionnel |
| `@ems-evaluator` | haiku | Calcul EMS 5 axes + weak_axes |
| `@technique-advisor` | haiku | Auto-selection techniques (63 en CSV) |

### v5.0 Agents

| Agent | Model | Role |
|-------|-------|------|
| `@party-orchestrator` | sonnet | Orchestration multi-persona (5 personas) |
| `@expert-panel` | sonnet | Panel 5 experts dev (3 phases) |

## EMS Calculation (via @ems-evaluator)

**MANDATORY: Invoke @ems-evaluator at each iteration.**

Axes (weights):
- Clarte (25%) — Precision du besoin
- Profondeur (20%) — Niveau de detail
- Couverture (20%) — Exhaustivite
- Decisions (20%) — Choix actes
- Actionnabilite (15%) — Pret pour action

**Invocation:**
```
Task tool -> @ems-evaluator (haiku)
Input: current brief state, previous EMS, open questions
Output: 5-axis scores, composite, delta, weak_axes, recommendations
```

**Output includes (v4.8+):**
- `weak_axes[]` — Liste des axes avec score < 50
- Trigger auto-technique si `weak_axes` non vide

**Thresholds:**

| EMS Range | Recommendation | Technique Trigger | Checkpoint |
|-----------|----------------|-------------------|------------|
| 0-49 | CONTINUE | Si axe < 50 → SUGGEST_TECHNIQUE | - |
| 50-69 | SUGGEST_CONVERGE | Si axe < 50 → SUGGEST_TECHNIQUE | Transition (EMS=50) |
| 70-84 | FINALIZATION_CHECKPOINT | Non (proche finish) | **Finalization** |
| 85-100 | FINALIZATION_CHECKPOINT | Non | **Finalization** |

**IMPORTANT**: À EMS >= 85, NE JAMAIS finaliser automatiquement.
Toujours afficher le Finalization Checkpoint et attendre le choix explicite.

## Technique Selection (via @technique-advisor)

### Technique Library (v5.0)

**MANDATORY: Load techniques from CSV, not deprecated .md files.**

```
Read src/skills/core/brainstormer/references/techniques.csv
Read src/skills/core/brainstormer/references/technique-mapping.md
```

**11 Categories (68 Techniques):**

| Category | Count | Primary Phase |
|----------|-------|---------------|
| collaborative | 5 | Divergent |
| creative | 11 | Divergent |
| deep | 8 | Convergent |
| introspective | 6 | Divergent |
| structured | 11 | Convergent |
| theatrical | 6 | Divergent |
| wild | 8 | Divergent |
| biomimetic | 3 | Divergent |
| quantum | 3 | Convergent |
| cultural | 4 | Divergent |
| prioritization | 3 | Convergent |

### Auto-Invocation

**Declenchement automatique** a chaque iteration si:
1. Au moins un axe EMS < 50 (retourne par `@ems-evaluator` dans `weak_axes`)
2. Technique correspondante pas utilisee dans les 2 dernieres iterations
3. Pas en mode `--no-technique`

**Invocation manuelle:**
- `technique [name]` — Applique technique specifique
- `--random` flag — Selection aleatoire avec equilibrage categories
- `--progressive` flag — Selection basee sur phase EMS

### Mapping EMS → Categories

| Axe Faible | Categories Primaires | Categories Secondaires |
|------------|---------------------|------------------------|
| Clarte < 50 | deep, structured | creative |
| Profondeur < 50 | deep, introspective | creative, theatrical |
| Couverture < 50 | creative, collaborative, wild | theatrical, biomimetic |
| Decisions < 50 | structured, deep | collaborative |
| Actionnabilite < 50 | structured | collaborative, wild |

### Mix de Techniques

Quand 2+ axes sont faibles:
- Combiner 1 technique par axe faible (max 2)
- Privilegier techniques complementaires (Divergent + Convergent)
- Eviter 2 techniques de meme categorie
- Ordre: Divergent d'abord, puis Convergent

### Format Proposition

**Technique unique:**
```
💡 Technique suggérée: [NOM] ([CATEGORIE])
   Raison: Axe [X] à [Y]% — [effet attendu]

→ Appliquer? [Y/n/autre]
```

**Mix (2+ axes faibles):**
```
💡 TECHNIQUES SUGGÉRÉES | Iteration [N]

Axes faibles: [Axis1] ([X]%), [Axis2] ([Y]%)

[1] [Technique1] → [Axis1]
[2] [Technique2] → [Axis2]

→ [1] / [2] / [b]oth / [n]one
```

### Session Tracking

Ajouter dans session YAML (`techniques_history`):
```yaml
techniques_history:
  - iteration: 3
    suggested: ["six-hats", "moscow"]
    applied: ["six-hats"]
    reason: "Couverture 35%, Decisions 42%"
```

### Invocation Agent

```
Task tool -> @technique-advisor (haiku)
Input: phase, weak_axes, techniques_used
Output: selected technique(s), adapted questions
```

## Question Format (AskUserQuestion Native v5.1)

**Contraintes AskUserQuestion:**
- Maximum **3 questions** par invocation
- Timeout: 60 secondes par question
- Header: max 12 caractères
- Options: 2-4 par question
- `(Recommended)` suffix pour la suggestion visuelle
- Option "Other..." automatiquement disponible

**Format standard:**
```typescript
AskUserQuestion({
  questions: [
    {
      question: "[Question complète avec contexte ?]",
      header: "[🛑|⚠️|ℹ️] [Label]",  // Max 12 chars
      multiSelect: false,
      options: [
        { label: "[Option concise]", description: "[Contexte, raison]" },
        { label: "[Option (Recommended)]", description: "[Pourquoi recommandé]" },
        { label: "[Autre option]", description: "[Description]" }
      ]
    }
  ]
})
```

**Mapping Priorité → Header:**
| Priorité | Header | Comportement |
|----------|--------|--------------|
| 🛑 Critique | `🛑 Critical` | Question posée en premier, obligatoire |
| ⚠️ Important | `⚠️ Important` | Recommandation appliquée si ignorée |
| ℹ️ Info | `ℹ️ Info` | Purement informatif, default silencieux |
| Checkpoint | `🎯 Checkpoint` | Finalization ou transition |
| Technique | `💡 Technique` | Suggestion de technique |
| Transition | `🔄 Transition` | Changement de phase |

**IMPORTANT:** L'option "Other..." est automatiquement disponible dans AskUserQuestion.
Ne pas l'ajouter manuellement aux options.

### PRD Industry Standards Questions (v3.0)

Sections PRD avec exemples de questions :
- **Problem Statement** — `🛑 Critical` — données quantitatives, evidence
- **Goals** — `⚠️ Important` — objectifs business/user/tech
- **Non-Goals** — `⚠️ Important` — exclusions explicites v1
- **Background** — `ℹ️ Info` — timing, stratégie
- **Assumptions** — `ℹ️ Info` — hypothèses techniques

> Voir `brainstorm.md` pour exemples TypeScript détaillés.

## Breakpoint Format (v5.3 — via @skill:breakpoint-display)

**IMPORTANT:** Tous les breakpoints utilisent maintenant le skill centralisé `breakpoint-display`.

**Status Breakpoint (display-only):**
```yaml
@skill:breakpoint-display
  type: ems-status
  title: "BRAINSTORM STATUS"
  data:
    phase: "{DIVERGENT|CONVERGENT}"
    persona: "{Architecte|Sparring|Pragmatique}"
    iteration: {N}
    ems:
      score: {EMS}
      delta: "{+N}"
      axes: {clarity: X, depth: X, coverage: X, decisions: X, actionability: X}
      weak_axes: ["{axes < 50}"]
      progression: ["Init(22)", "Iter1(38)", ..., "Current({EMS})"]
    done: ["{éléments validés}"]
    open: ["{points restants}"]
    commands: ["continue", "dive", "back", "save", "energy", "finish"]
```

**Questions Breakpoint (interactive):**
```yaml
@skill:breakpoint-display
  type: analysis
  title: "QUESTIONS ITÉRATION"
  data:
    context:
      phase: "{PHASE}"
      iteration: {N}
      ems: {EMS}
    questions:
      - {tag: "🛑", text: "{question}", suggestion: "{suggestion}"}
      - {tag: "⚠️", text: "{question}", suggestion: "{suggestion}"}
      - {tag: "ℹ️", text: "{question}", suggestion: "{suggestion}"}
  ask:
    question: "Répondez aux questions"
    header: "📋 Questions"
    options:
      - {label: "Répondre (Recommended)", description: "Répondre une par une"}
      - {label: "Valider suggestions", description: "Accepter suggestions IA"}
      - {label: "Finish", description: "Finaliser maintenant"}
```

**Avantages v5.3:**
- ~57% économie tokens via skill centralisé
- Format cohérent avec /brief et /epci
- UI native Claude Code avec boutons

Voir `src/skills/core/breakpoint-display/templates/ems-status.md` pour détails du rendu.

## Finalization Checkpoint (v5.3 — via @skill:breakpoint-display)

**Trigger:** EMS >= 70 (première fois atteint dans la session)

**Breakpoint:**
```yaml
@skill:breakpoint-display
  type: plan-review
  title: "FINALIZATION CHECKPOINT"
  data:
    metrics:
      ems_score: {EMS}
      ems_delta: "{delta}"
      axes: {clarity: X, depth: X, coverage: X, decisions: X, actionability: X}
      weak_axes: []
    progression: "Init(22) → Iter1(38) → ... → Final({EMS})"
    preview_next_phase:
      phase_name: "Phase 3: Generation"
      tasks:
        - {title: "Générer brief PRD v3.0", time: "auto"}
        - {title: "Créer journal exploration", time: "auto"}
      message: "Le brief est suffisamment mature pour être finalisé."
  ask:
    question: "Brief EMS {EMS}/100 prêt. Quelle action ?"
    header: "🎯 Checkpoint"
    options:
      - {label: "Continuer", description: "Plus d'itérations pour affiner"}
      - {label: "Preview (Recommended)", description: "@planner sans finaliser"}
      - {label: "Finaliser", description: "Générer brief + journal maintenant"}
```

**Note:** La ligne "progression" utilise `ems_history` stocké pendant les itérations.

**Comportement selon réponse:**
- "Continuer" → génère 3 nouvelles questions via breakpoint `type:analysis`, reprend Phase 2
- "Preview" → invoque @planner, affiche plan, puis redemande [Continuer/Finaliser]
- "Finaliser" → passe en Phase 3 Generation

**CRITICAL:** Ce checkpoint est BLOQUANT. Attendre réponse explicite.

## @planner Integration

**Invocation:** Uniquement sur choix explicite [2] au Finalization Checkpoint
ou commande `plan-preview`

**Confirmation préalable:** `Lancer @planner? [Y/n]`

Invoke via Task tool (model: sonnet).
Output integre dans brief section "Preliminary Plan".

## @security-auditor Integration

**Auto-detection:** Patterns auth/security/payment/api

**Confirmation:** `Lancer @security-auditor? [Y/n]`

Invoke via Task tool (model: opus).
Output integre dans brief section "Security Considerations".

## Phase 3 — Generation

**MANDATORY: Use Write tool for BOTH files using official templates.**

**CRITICAL: Before generating, ALWAYS read the template:**
```
Read src/skills/core/brainstormer/references/brief-format.md
```

1. Create directory: `mkdir -p ./docs/briefs/[slug]`
2. **Read template** `references/brief-format.md` (MANDATORY)
3. Section-by-section validation (si pas --quick/--turbo)
4. Write `brief-[slug]-[date].md` — **Must include (v3.0 PRD Standard)**:
   - **Document Header** — PRD-YYYY-XXX, Version, Status, Change History
   - **Executive Summary** — TL;DR, Problem, Solution, Impact
   - **Background & Strategic Fit** — Why Now?, Alignment
   - **Problem Statement** — Current Situation, Evidence & Data, Impact
   - **Goals** — Business/User/Technical goals with metrics
   - **Non-Goals** — Explicit exclusions with reasons (replaces Hors Scope)
   - **Personas** section (min 1 primary persona)
   - **User Stories** format (En tant que... je veux... afin de)
   - **Acceptance Criteria** (Given/When/Then)
   - **Success Metrics** (KPIs or "TBD")
   - **User Flow** — As-Is vs To-Be with Key Improvements
   - **Assumptions** — Technical/Business/User/Resources hypotheses
   - **FAQ** — Internal + External questions
   - **Timeline & Milestones** — Key milestones with Phasing Strategy
   - **Appendix** (optional) — Research, Glossary
5. Write `journal-[slug]-[date].md` — Using Journal template
6. Display completion summary

**Optional sections (if flag or context relevant):**
- **Competitive Analysis** — With `--competitive` flag

**Anti-pattern**: Generating brief without reading template first = INVALID

**Completion format:**
```
-------------------------------------------------------
BRAINSTORM COMPLETE
-------------------------------------------------------
EMS Final: XX/100
Agents: [@planner | @security-auditor | Aucun]

Fichiers generes:
   - Brief: ./docs/briefs/[slug]/brief-[slug]-[date].md
   - Journal: ./docs/briefs/[slug]/journal-[slug]-[date].md

Prochaine etape: Lancer /brief avec le contenu du brief.
-------------------------------------------------------
```

## Framework Detection

| Signal | Framework |
|--------|-----------|
| Priorisation | MoSCoW |
| "Pourquoi" repete | 5 Whys |
| Plusieurs options | SWOT |
| Criteres multiples | Scoring |
| Risques | Pre-mortem |

## Anti-patterns

**Ne pas faire:**
- Plus de 5 questions par iteration
- Breakpoint > 15 lignes
- Ignorer contexte codebase
- `finish` avant EMS 60
- Finaliser automatiquement à EMS >= 85 (CRITIQUE)
- Invoquer @planner sans choix explicite utilisateur
- Generer brief SANS lire `references/brief-format.md` d'abord (CRITIQUE)
- Omettre section Personas dans le brief
- Utiliser format SF au lieu de User Stories
- Omettre Acceptance Criteria Given/When/Then

**Toujours faire:**
- Invoquer @ems-evaluator a chaque iteration
- Proposer suggestions avec questions
- Respecter format compact CLI
- Afficher Finalization Checkpoint à EMS >= 85
- Attendre réponse explicite [1]/[2]/[3] avant action
- Lire `brief-format.md` AVANT de generer le brief
- Inclure Personas, User Stories, Success Metrics dans le brief

## Party Mode (v5.0)

Discussion collaborative multi-persona pour explorer sous plusieurs angles.

### 5 Personas EPCI

| Persona | Icon | Focus |
|---------|------|-------|
| **Architect** | 🏗️ | System design, patterns, scalabilite |
| **Security** | 🔒 | OWASP, auth, protection donnees |
| **Frontend** | 🎨 | UI/UX, accessibilite, perf |
| **Backend** | ⚙️ | APIs, data integrity, infra |
| **QA** | 🧪 | Testing, edge cases, coverage |

### Commandes

| Commande | Action |
|----------|--------|
| `party` | Demarrer discussion party mode |
| `party add [persona]` | Ajouter persona au round |
| `party focus [persona]` | Deep dive d'un persona |
| `party exit` | Retour mode standard |

### Invocation

```
Task tool -> @party-orchestrator (sonnet)
Input: current topic, selected personas, previous rounds
Output: persona contributions, cross-talk, synthesis, question
```

**Regles MANDATORY:**
- EMS continue d'etre calcule pendant party mode
- Finalization Checkpoint se declenche normalement a EMS >= 85
- `party exit` retourne au mode standard immediatement

Voir [party-personas.md](references/party-personas.md) pour details.

## Expert Panel (v5.0)

Panel 5 dev thought leaders pour decisions techniques strategiques.

### 5 Experts Dev

| Expert | Icon | Framework | Focus |
|--------|------|-----------|-------|
| **Martin** | 📖 | SOLID, Clean Architecture | Code design, maintenabilite |
| **Fowler** | 🔄 | Enterprise Patterns | Architecture, refactoring |
| **Newman** | 🌐 | Distributed Systems | Scalabilite, decouplage |
| **Gamma** | 📐 | Design Patterns (GoF) | Design OO |
| **Beck** | ✅ | XP, TDD | Testing, agilite |

### 3 Phases

| Phase | Description |
|-------|-------------|
| **Discussion** | 3 experts analysent via leurs frameworks |
| **Debate** | Stress-test des idees par desaccord structure |
| **Socratic** | Questions guidees pour approfondir |

### Commandes

| Commande | Action |
|----------|--------|
| `panel` | Demarrer panel (phase discussion) |
| `panel debate` | Passer en phase debate |
| `panel socratic` | Passer en phase socratic |
| `panel exit` | Retour mode standard |

### Invocation

```
Task tool -> @expert-panel (sonnet)
Input: topic, phase, selected experts, previous rounds
Output: expert contributions, synthesis (convergent + tensions)
```

Voir [experts/](references/experts/) pour details par expert.

## Session Modes (v5.0)

Les modes sont **mutuellement exclusifs**:

| Mode | Description | Commande |
|------|-------------|----------|
| `standard` | Workflow brainstorm classique | (defaut) |
| `party` | Multi-persona collaboratif | `party` ou `--party` |
| `panel` | Expert panel technique | `panel` ou `--panel` |

**Changement de mode:**
- `party` ou `panel` → active le mode correspondant
- `party exit` ou `panel exit` → retourne en `standard`
- On ne peut pas etre en `party` ET `panel` simultanement
