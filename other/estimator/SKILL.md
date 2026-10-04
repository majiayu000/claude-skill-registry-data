---
name: estimator
description: >-
  Project estimation tool with interactive workflow. Breaks down projects into
  functional components, calculates cost ranges (optimistic/realistic/pessimistic)
  with auto-detected risk coefficients. Generates structured Markdown ready for
  propositor. Supports dev, refonte, TMA, and audit projects with 3 granularity
  levels. Use when user needs to estimate costs, calculate workload, prepare
  project budgets, or says "estime", "chiffrage", "JH", "combien coûterait".
  Not for invoicing, accounting, contract review, or projects without technical scope.
---

# Estimator — Project Estimation Tool

## Overview

Estimator transforms functional requirements into structured, argumented cost estimates through an interactive 4-phase workflow with mandatory checkpoints. Outputs client-ready Markdown documents consumable by Propositor.

## Quick Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                    What type of estimation?                      │
└─────────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  NEW PROJECT  │   │  EVOLUTION    │   │  AUDIT/TMA    │
│  (dev/refonte)│   │  (features)   │   │  (review)     │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        ▼                   ▼                   ▼
   Full workflow       Partial lots        Specific template
   (all 12 lots)       (impacted only)     (no recette for audit)
```

## Main Workflow (4 Phases)

### Phase 1: Qualification
**Goal**: Understand context and calibrate estimation

1. Analyze input (brief, brainstorm output, specs)
2. Ask clarification questions (≤3 if brief is clear)
3. Auto-detect: project type, granularity, coefficients

**📍 Checkpoint 1**: Present understanding + detected parameters for validation

→ See [workflow-details.md](references/workflow-details.md) for checkpoint format

### Phase 2: Functional Breakdown
**Goal**: Identify ALL features (explicit AND implicit)

1. Extract features from brief
2. Identify implicit features (auth, logs, admin...)
3. Assign unique IDs (FCT-001, FCT-002...)
4. Prioritize: MVP / Should / Could
5. Provide AI suggestions

**📍 Checkpoint 2**: Present feature table + suggestions for validation

### Phase 3: Task Evaluation
**Goal**: Estimate each task with ranges

1. Generate task tables per lot
2. Calculate: JH_Low × 0.8 | JH_Mid × coeff | JH_High × 1.3
3. Apply automatic recette (15% for dev, varies by type)

**📍 Checkpoint 3**: Present detailed estimation for validation

→ See [lots-templates.md](references/lots-templates.md) for lot structures

### Phase 4: Valorization & Synthesis
**Goal**: Convert JH to budget, document assumptions

1. Apply TJM (default 450€)
2. Generate budget scenarios (Light/Low/Mid/High)
3. Document technical registry (assumptions, risks, stack choices)

**📍 Final Checkpoint**: Complete document ready for export or Propositor

## Granularity Auto-Detection

| Project Size | Granularity | Lots Structure |
|--------------|-------------|----------------|
| < 30 JH | Macro (±30%) | 4 merged lots |
| 30-200 JH | Standard (±20%) | 12 standard lots |
| > 200 JH | Detailed (±10%) | 12 lots + Back/Front sub-modules |

## Coefficient Auto-Detection

| Client Type | Specs Clarity | coeff_effort | coeff_risk |
|-------------|---------------|--------------|------------|
| Known | Clear | 0.85 | 1.05 |
| Known | Partial | 0.90 | 1.10 |
| New | Clear | 0.90 | 1.10 |
| New | Unclear | 0.95 | 1.20 |

→ See [coefficients.md](references/coefficients.md) for detailed formulas

## Tech Stack Preferences

| Domain | Priority 1 | Priority 2 | Fallback |
|--------|------------|------------|----------|
| Backend | **Symfony 7** | Django | Spring Boot |
| Frontend | **React 18** | Vue 3 | Angular |
| Database | **PostgreSQL** | MySQL | MongoDB |
| Infra | **Docker** | PaaS | VM |
| Mobile | **React Native** | Flutter | Native |

## Commands Reference

### During Session

| Command | Action |
|---------|--------|
| `valider` | Confirm checkpoint, proceed to next phase |
| `ajouter [item]` | Add feature or task |
| `modifier [ID]` | Edit existing element |
| `supprimer [ID]` | Remove element |
| `question [topic]` | Ask clarification before validating |
| `ajuster-jh [ID] [value]` | Manually adjust JH |
| `recalculer` | Recalculate after modifications |
| `détailler [lot]` | Show lot details |
| `exporter` | Generate final document |
| `propositor` | Chain to Propositor skill |

### Launch Flags

| Flag | Effect | Default |
|------|--------|---------|
| `--macro` | Force macro granularity (±30%) | Auto |
| `--standard` | Force standard granularity (±20%) | ✅ |
| `--detailed` | Force detailed granularity (±10%) | Auto if >200 JH |
| `--tjm [amount]` | Set specific TJM | 450€ |
| `--type [dev/refonte/tma/audit]` | Force project type | Auto-detected |
| `--coeff [0.6-1.0]` | Override effort coefficient | Auto |
| `--no-suggestions` | Disable AI suggestions | Enabled |

## Output Format

Estimator produces structured Markdown with parseable tags:

```markdown
<!-- ESTIMATOR_DATA_START -->
| Lot | JH Low | JH Mid | JH High |
|-----|--------|--------|---------|
...
<!-- ESTIMATOR_DATA_END -->

<!-- ESTIMATOR_BUDGET_START -->
| Scenario | JH | Amount HT |
|----------|-----|-----------|
...
<!-- ESTIMATOR_BUDGET_END -->
```

→ See [output-format.md](references/output-format.md) for complete template

## Critical Rules

1. **Mandatory checkpoints** — No one-shot generation
2. **Proactive AI suggestions** — Implicit features, risks, alternatives
3. **Ask when uncertain** — Never guess, request clarification
4. **FCT-xxx traceability** — Each task references a feature
5. **Complete technical registry** — Document all assumptions
6. **User's language** — Output in input language
7. **Parseable tags** — For Propositor integration

## Synergies

### Inputs From
- `brainstormer` → Synthesis report, decisions
- `code-promptor` → Technical brief, constraints
- `resumator` → Meeting notes, requirements

### Outputs To
- `propositor` → **Primary** — Full estimation for commercial proposal
- `planificator` (future) → JH per lot for detailed planning
- `tracker` (future) → Initial estimate as tracking reference

## Limitations

This skill does NOT handle:
- Invoicing or accounting
- Contracts or legal aspects
- Estimates without technical scope
- Negotiation (see `negociator`)
- Detailed planning (see `planificator`)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-15 | Initial release |

## Current: v1.0.0

## Owner

- **Author**: Édouard
- **Contact**: Via Claude.ai
