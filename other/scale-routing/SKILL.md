---
name: mk:scale-routing
description: Domain-aware complexity routing. Scans task description for domain keywords, matches against domain-complexity.csv, returns complexity level, workflow intensity, and execution tier. Extends Phase 0 orchestration.
triggers:
  - task classification
  - complexity routing
  - phase 0 orient
phase: 0
user-invocable: false
source: local
keywords:
  - scale-routing
  - domain-classification
  - complexity-routing
  - csv-routing
  - execution-tier
when_to_use: Auto-invoked at Phase 0 — scans task description for domain keywords, returns complexity tier and execution tier. Not user-callable directly.
owner: portability
criticality: medium
status: active
runtime: claude-code
---

# Scale-Adaptive Routing

Automatically classifies task complexity based on domain keywords.

> Internal sub-skill of Phase 0 (Orient). Not user-invocable directly — invoked by the orchestrator during task classification.

## Purpose

Replace subjective orchestrator judgment with deterministic, auditable domain-based routing. A fintech auth change should auto-classify as COMPLEX without human intervention.

## How It Works

1. **Input:** User task description (string)
2. **Layer 0:** Match keywords from `data/domain-complexity.csv`
3. **Layer 1:** Analyze task content — classify type and extract mentioned files/modules (load `references/multi-layer-detection.md`)
4. **Layer 2:** Check project context — files present, directory structure, recent git changes
5. **Layer 3:** Score confidence per domain (HIGH ≥70, MEDIUM 40–69, LOW <40)
6. **Classify task type** — map signals to one of: `bug_fix`, `feature`, `refactor`, `security`, `devops`, `docs`, `review`, `intake` (load `references/task-type-classification.md`)
7. **Optional:** Check `.claude/product-areas.yaml` if exists — merge area keywords and paths (see `references/product-area-config.md`)
8. **Output:** `{domain, level, workflow, execution_tier, task_type, suggested_skill, confidence, product_area?}`
9. **Fallback:** No match → return `unknown`, defer to manual classification

## CSV Schema

| Column | Values | Purpose |
|--------|--------|---------|
| domain | snake_case identifier | Domain name |
| signals | comma-separated keywords | Match against task description |
| level | low, medium, high | Complexity classification |
| workflow | one-shot, standard, enhanced, advanced | Workflow intensity |
| web_searches | comma-separated topics | Suggested research queries |

## Routing Logic

| Level | Execution Tier | Gate 1 | Workflow |
|-------|-----------|--------|---------|
| low | minimal | Bypass eligible (one-shot) | Minimal |
| medium | standard | Required | Standard phases |
| high | high-assurance | Required | Full phases + security |

## Provider Boundary

This skill emits only task complexity, risk, workflow intensity, and scaffolding density. It does not select a model or name a provider. The active harness resolves any provider-specific model policy after this routing result is produced.

## Usage

Called automatically by orchestrator at Phase 0. Not invoked directly by users.

```
Orchestrator Phase 0:
  1. Run mk:scale-routing on task description
  2. If match found → use returned level/workflow/execution_tier
  3. If no match → fall back to manual classification
```

## Extending

Users can add custom domains by editing `data/domain-complexity.csv`. Add a new row with domain keywords relevant to your project.

## Gotchas

- **Runtime dependency on `mk:autobuild/scripts/density-select.sh`** — if the autobuild workflow skill is removed or renamed, density selection breaks. The script is shared intentionally (single source of truth for density policy); treat it as load-bearing infrastructure, not a private harness internal.
- Multiple domains can match a single task (e.g., "fintech dashboard" matches both fintech and internal_tools) — use the HIGHEST complexity match
- CSV keyword matching is case-insensitive but signal order matters — first match wins for domain name
- Adding too many low-signal keywords (e.g., "data", "app") creates false positives — keep signals specific to the domain
- One-shot workflow bypass requires BOTH CSV match AND orchestrator zero-blast-radius confirmation — CSV alone is not sufficient

## Output Schema (v2.0)

Base fields (v1.0):

| Field | Values | Description |
|---|---|---|
| `domain` | snake_case string | Matched domain or `unknown` |
| `level` | low, medium, high | Complexity classification |
| `workflow` | one-shot, standard, enhanced, advanced | Workflow intensity |
| `execution_tier` | minimal, standard, high-assurance | Provider-neutral execution intensity |

New fields (v2.0):

| Field | Values | Description |
|---|---|---|
| `task_type` | bug_fix, feature, refactor, security, devops, docs, review, intake | Classified task type |
| `suggested_skill` | mk:fix, mk:cook, mk:cso, mk:review, mk:intake | Recommended skill for this task |
| `confidence` | HIGH, MEDIUM, LOW | Routing confidence from Layer 3 scoring |
| `product_area` | string | Area name from `.claude/product-areas.yaml` (omitted if no YAML) |

New fields (v2.1 — Phase 5 of harness plan, 260408):

| Field | Values | Description |
|---|---|---|
| `autobuild_density` | `MINIMAL`, `FULL`, `LEAN` | Recommended scaffolding density for `mk:autobuild` runs (see Adaptive Density Policy below) |

### Harness Density Selection (v2.1)

Used by `mk:autobuild` to choose how much scaffolding to apply per run. The decision rules:

| `level` | neutral baseline | `autobuild_density` |
|---|---|---|
| low | none | `MINIMAL` |
| medium | none | `FULL` |
| high | none | `FULL` |

**Override:** `MEOWKIT_AUTOBUILD_MODE=MINIMAL\|FULL\|LEAN` env var, when set, overrides the auto-detected value. The override is logged in the autobuild run report for audit.

For scriptable density selection, callers may invoke `.claude/skills/autobuild/scripts/density-select.sh` which echoes only the density token to stdout.

## Data File

- `data/domain-complexity.csv` — Domain → complexity → workflow mapping

## Reference Files

- `references/multi-layer-detection.md` — 4-layer detection logic and confidence scoring
- `references/task-type-classification.md` — 8 task types, signals, and suggested skills
- `references/product-area-config.md` — Optional `.claude/product-areas.yaml` schema and loading rules

## Cross-Skill Dependencies

- `.claude/skills/autobuild/scripts/density-select.sh` — Echoes `autobuild_density` token to stdout; used by autobuild when scriptable density selection is needed
