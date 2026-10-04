---
name: academic-paper-writer
description: "Use when writing or revising CS/AI/ML papers from research notes, code repositories, local literature libraries, target venue requirements, or section-level drafting requests. Triggers include 写论文, 初稿, paper draft, write introduction, write method, full paper outline, section-by-section drafting, 证据闭环, 论文起草, 从零写论文, 逐节写作."
---

# Academic Paper Writer (Core Orchestrator)

证据闭环型、分节推进的论文编排代理。协调六个子技能：Step 0→1→2→3→4→5→6→7→8→9→10→11→12。

## Router Protocol

1. Read `manifest.yaml`. It declares `always_load` files, `axes`, and `references.on_demand`.
2. Read every file listed under `always_load`. These are the skill's binding rules — not reference material.
3. Apply the loaded material as constraints:
   - `stance.md` defines core rules, sub-skill boundary, and scope.
   - `red-lines.md` defines absolute prohibitions. Do not negotiate these.
   - `output-contract.md` defines file outputs, deliverables, and completion criteria.
   - `anti-patterns.md` defines known failure modes and their correct alternatives.
   - `workflow.md` defines the Step 0-12 sequence summary.
   - `../shared/core/` policies define evidence, non-invention, and output boundaries.
4. Detect `mode`, `paper_type`, `section`, and `language` using manifest axes.
5. Echo the detected mode to the user before executing.
6. Reach for `references/` only when the manifest's `references.on_demand` condition is satisfied.

## Modes

| Mode | Purpose |
|---|---|
| `full-paper-planning` | From-scratch full paper (balanced spectrum) |
| `section-drafting` | Single section, narrowed evidence scope (balanced) |
| `section-revision` | Local evidence audit + rewrite (fidelity spectrum) |
| `related-work-or-citation-pass` | Delegate to academic-citation (fidelity spectrum) |
| `experiment-evidence-pass` | Delegate to academic-experiments (fidelity spectrum) |

## Sub-Skill Dispatch

| Task | Sub-Skill | Step |
|---|---|---|
| Venue research | academic-venue-research | Step 4 |
| Evidence audit | Probe agent | Step 5 |
| Citation search | academic-citation | Step 6 |
| Experiment audit | academic-experiments | Step 7 |
| Figure generation | academic-figure | Step 9.4 |
| Prose polishing | academic-polishing | Step 9.6 (internal) |
| Draft review | academic-reviser | Step 9.5 / 9.8 |

## Push Modes

| Mode | Behavior |
|---|---|
| `auto` (default) | Auto-advance after Verification; brief progress summary only |
| `step-by-step` | Pause after each section for user confirmation |

Switch anytime via user request.

## Hard Gates (A-E)

| Gate | Trigger | Condition | Failure |
|---|---|---|---|
| E: Venue | Step 1→5 | 若用户提供本地 PDF 文献库，Step 2 已验证 MD 目录；venue-brief.md exists | Blocked |
| A: Evidence | Step 5→9 | >= 1 usable evidence | Degradation or blocked |
| B: Section Citation Readiness | Step 6→9 | Current section has VERIFIED citations, Citation-to-Claim Map, or explicit `[REF_NEEDED]` debt for key claims | Section-dependent: Intro/RW blocked, Method/Results may proceed with tracked debt |
| C: Verification | Step 9.8→10 | All hard debts closed + thin_draft=no | passed/failed/blocked |
| D: Full-Paper Citation Count | Step 11→output | Total >= min_citations | Warn, allow retry |

## 9.1 Pre-Draft Probe Rules

| Section | Probes to Dispatch | Strategy |
|---|---|---|
| Introduction | `existing_material` + local lit deep search + external lit search | **Must parallel** (3 Tasks) |
| Related Work | `existing_material` + local lit deep search + external lit search | **Must parallel** (3 Tasks) |
| Method | `code_structure` (Module Cards + tensor shapes + forward) + `preprocessing` | **Must parallel** |
| Experimental Setup | `experiment_setup` (hyperparams, dataset split, demographics) | Single probe |
| Results / Ablation | `experiment_results` (main results, baselines, ablation) | Single probe |
| Discussion | `interpretability` (interpretability results, network analysis) | Single probe |

## Default Section Queue

Abstract is post-posed, not in initial queue. Default: Introduction → Related Work → Method → Experimental Setup → Results → Discussion → Conclusion → Abstract.
