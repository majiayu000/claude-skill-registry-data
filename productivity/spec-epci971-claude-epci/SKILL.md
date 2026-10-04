---
name: epci:spec
description: >-
  Create comprehensive technical specifications from CDC (Cahier des Charges) or brief output.
  Decomposes features into 1-2h atomic tasks with 15-30min steps. Generates Markdown specs
  (index.md + task-XXX.md), machine-readable PRD.json, and Ralph execution artifacts.
  Uses project-memory for calibration and @decompose-validator for DAG validation.
  Use when: transforming brainstorm output, writing technical specs, preparing Ralph batch.
  Triggers: write spec, create specification, spec from brief, decompose feature, technical breakdown.
  Not for: ideation (use /brainstorm), direct implementation (use /implement).
user-invocable: true
argument-hint: "<feature-slug> [@brief-path | @text-description]"
allowed-tools: Read, Write, Glob, Grep, Task, AskUserQuestion
---

# Spec — Technical Specification Generator

Transform CDC/brief documents into executable technical specifications with Ralph-ready artifacts.

## Quick Start

```
/spec auth-oauth                                    # From description
/spec auth-oauth @docs/briefs/auth/brief.md         # From brief file
/spec auth-oauth @"OAuth integration for users"    # From inline description
```

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER generate specs without understanding the source
- 🔴 NEVER skip @decompose-validator before generation
- 🔴 NEVER create circular dependencies in task DAG
- 🔴 NEVER exceed granularity limits (tasks 1-2h, steps 15-30min)
- 🔴 NEVER call EnterPlanMode during skill execution
- ✅ ALWAYS start with step-00-init.md
- ✅ ALWAYS follow next_step from each step
- ✅ ALWAYS present breakpoints at phase transitions
- ✅ ALWAYS validate with @decompose-validator before generation
- ⛔ FORBIDDEN generating PRD.json with missing acceptance criteria
- 🔵 YOU ARE A METHODICAL SPECIFICATION WRITER following EPCI discipline
- 💭 FOCUS on one phase at a time, complete before proceeding

## EXECUTION PROTOCOLS:

1. **Load** step-00-init.md
2. **Execute** current step protocols completely
3. **Present** breakpoint if specified in step
4. **Evaluate** next step trigger conditions
5. **Proceed** to next_step or conditional_next

## CONTEXT BOUNDARIES:

- IN scope: Transforming CDC/briefs into specs, task decomposition, Ralph artifacts
- OUT scope: Ideation (use /brainstorm), implementation (use /implement or /quick)

## Input Detection

```
INPUT
├── @docs/briefs/*.md → BRIEF-FIRST workflow
│   └─ Parse CDC sections, extract requirements
├── @"text description" → TEXT workflow
│   └─ Clarify with clarification-engine, then proceed
└── feature-slug only → DISCOVERY workflow
    └─ Search for existing brief, else ask for input
```

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SPEC WORKFLOW (3 Phases)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Step 00: INIT                                                       │
│  └─ Parse input, detect source type                                  │
│  └─ Load project context via project-memory                          │
│     └─ If no source → ask for brief/description                      │
│                                                                      │
│  Step 01: ANALYZE & DECOMPOSE                                        │
│  └─ Parse CDC/brief structure                                        │
│  └─ Calculate complexity via complexity-calculator                   │
│  └─ Decompose into tasks (1-2h) with steps (15-30min)                │
│  └─ Build DAG (dependency graph)                                     │
│  └─ Validate with @decompose-validator                               │
│     └─ BREAKPOINT: Decomposition review                              │
│                                                                      │
│  Step 02: GENERATE SPECS                                             │
│  └─ Create docs/specs/{slug}/ directory                              │
│  └─ Generate index.md (orchestrator)                                 │
│  └─ Generate task-XXX.md for each task                               │
│  └─ Generate {slug}.prd.json (machine-readable)                      │
│     └─ BREAKPOINT: Specs review                                      │
│                                                                      │
│  Step 03: GENERATE RALPH                                             │
│  └─ Detect project stack                                             │
│  └─ Create .ralph/{slug}/ directory                                  │
│  └─ Generate PROMPT.md (stack-aware)                                 │
│  └─ Generate MEMORY.md (template)                                    │
│  └─ Generate ralph.sh (runner)                                       │
│  └─ Update .ralph/index.json                                         │
│     └─ BREAKPOINT: Completion summary with routing                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Steps

| Step | Name | Description |
|------|------|-------------|
| 00 | init | Parse input, detect source, load context |
| 01 | analyze | Decompose into tasks, build DAG, validate |
| 02 | generate-specs | Create index.md, task-XXX.md, PRD.json |
| 03 | generate-ralph | Create Ralph artifacts |

## Granularity Rules

| Level | Duration | Purpose |
|-------|----------|---------|
| **Task** | 1-2 hours | Human-readable units, complete deliverables |
| **Step** | 15-30 minutes | Atomic execution units for Ralph |

### Task Structure

Each task-XXX.md contains:
- YAML frontmatter (id, title, deps, complexity, effort)
- Objective section
- Acceptance Criteria (Given-When-Then or checklist)
- Steps section (numbered 15-30min steps)
- Files to modify/create
- Test approach

### Step Structure

Each step within a task:
- Action verb title
- Expected duration
- Input requirements
- Output deliverable
- Validation criteria

## Decision Tree

```
IF source is brief (@*.md):
  → Parse sections, extract requirements
  → Calculate complexity
  → Proceed to decomposition
ELSE IF source is text (@"..."):
  → Clarify with clarification-engine if needed
  → Convert to structured requirements
  → Proceed to decomposition
ELSE IF no source:
  → Search for existing brief in docs/briefs/{slug}/
  → If found → use it
  → If not found → ask user for input
```

## Step Files

- [steps/step-00-init.md](steps/step-00-init.md) — Initialization
- [steps/step-01-analyze.md](steps/step-01-analyze.md) — Analysis & Decomposition
- [steps/step-02-generate-specs.md](steps/step-02-generate-specs.md) — Specs Generation
- [steps/step-03-generate-ralph.md](steps/step-03-generate-ralph.md) — Ralph Generation

## Reference Files

- [references/task-format.md](references/task-format.md) — Task file format
- [references/prd-schema.md](references/prd-schema.md) — PRD.json schema
- [references/ralph-generation.md](references/ralph-generation.md) — Ralph artifacts guide

## Templates

- [templates/index.md.template](templates/index.md.template) — Index template
- [templates/task.md.template](templates/task.md.template) — Task template
- [templates/prompt.md.template](templates/prompt.md.template) — Ralph PROMPT template

## Output Structure

```
docs/specs/{feature-slug}/
├── index.md                    # Orchestrator (table + Mermaid DAG + context)
├── task-001-{slug}.md          # Task 1 (1-2h, with Steps)
├── task-002-{slug}.md          # Task 2
├── ...
└── {feature-slug}.prd.json     # Machine version (Ralph-ready)

.ralph/{feature-slug}/
├── PROMPT.md                   # Claude Code instructions (stack-aware)
├── MEMORY.md                   # Persistent context (template)
└── ralph.sh                    # Runner script
```

## Shared Components Used

- `epci:complexity-calculator` — Scope estimation for routing
- `epci:project-memory` — Velocity calibration, conventions
- `epci:clarification-engine` — Input clarification if needed
- `epci:breakpoint-system` — Phase checkpoints
- `@decompose-validator` — DAG validation

## Subagents

| Agent | Model | Usage |
|-------|-------|-------|
| @decompose-validator | Opus | Validate DAG before generation |
| @Explore | - | Codebase analysis for context |

## Breakpoints

This skill uses these breakpoint types:
- **decomposition**: Task table + DAG review (Step 01)
- **plan-review**: Specs preview (Step 02)
- **validation**: Completion summary with routing (Step 03)

## Complexity Routing (at completion)

| Complexity | Workflow |
|------------|----------|
| TINY/SMALL | Recommend `/quick` |
| STANDARD/LARGE | Recommend `/implement` |

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| @decompose-validator NEEDS_REVISION | Circular deps, missing coverage | Fix issues, re-decompose |
| Brief parsing failure | Malformed brief | Ask for clarification |
| Stack detection failure | No project markers | Use generic templates |
| Granularity violation | Task too large/small | Split or merge tasks |

## Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max tasks | 20 | Avoid overwhelming complexity |
| Min tasks | 2 | At least 2 for meaningful spec |
| Task duration | 1-2h | Goldilocks zone |
| Step duration | 15-30min | Atomic execution |
| AC per task | >= 2 | Quality gate |

## INVOCATION PROTOCOL (CRITICAL)

Les syntaxes `@skill:epci:xxx` et `@agent:xxx` dans les step files sont **DOCUMENTAIRES SEULEMENT**.
Claude interprète les blocs de code comme des exemples, pas comme des instructions d'exécution.

**Pour invoquer réellement:**

| Type | Syntaxe documentaire | Invocation réelle |
|------|---------------------|-------------------|
| Breakpoints | `@skill:epci:breakpoint-system` | Section impérative + AskUserQuestion explicite |
| Agents | `@agent:decompose-validator` | `Task({ subagent_type: "decompose-validator", ... })` |
| Core skills | `@skill:epci:project-memory` | `Read(".claude/state/...")` pour fichiers d'état |

**Règle pour auteurs de step files:**
- Utiliser le format impératif direct (pas dans bloc de code)
- Afficher les boîtes ASCII hors bloc exécutable
- Appeler AskUserQuestion explicitement
- Ajouter `⏸️ ATTENDS la réponse` après chaque breakpoint

## Limitations

This skill does NOT:
- Ideate or explore (use /brainstorm)
- Implement code (use /implement or /quick)
- Debug existing code (use /debug)
- Create new skills (use /factory)
- Execute Ralph batches (use ralph.sh directly)
