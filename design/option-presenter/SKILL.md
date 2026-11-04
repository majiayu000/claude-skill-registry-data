---
name: Option Presenter
description: Generates option comparison matrix, BLUF recommendation, and screenshot manifest for stakeholder decision-making
version: 1.0.0
author: Mattermost Design Team
tags: [prototype, comparison, decision-aid, phase-6, scoring]
allowed-tools: Read, Grep, Glob
---

# Option Presenter

## Purpose

The Option Presenter generates the decision-making artifacts stakeholders need to select a preferred design option. It produces a scored comparison matrix, a BLUF recommendation with trade-off analysis, and a screenshot manifest for visual review.

This skill runs AFTER all prototype options are built and validated. It is the final step before Phase 6 gate review.

**Rubric source of truth:** the comparison matrix uses the **same 7 weighted criteria, per-IL-tier default weights, 1–5 scale, normalized-score math, anti-gaming rule, and tie-break** as Phase 4 — all defined in **[`${CLAUDE_PLUGIN_ROOT}/templates/conventions.md` §3](../../templates/conventions.md)**. This is the **Phase 6** consumer of that rubric (`solution-scorer` is the Phase 4 consumer), so a Phase-4 direction and its Phase-6 options score on the identical axes and are directly comparable. Do not invent a separate criteria set here.

## When to Use

- **After all options are built**: When option-builder + component-composer + state-matrix-builder have completed
- **Before gate review**: To prepare the decision package for Design Lead and PM
- **Option refinement**: When options are updated and the comparison needs refreshing

## Input Requirements

```json
{
  "type": "object",
  "properties": {
    "options": {
      "type": "array",
      "description": "Completed option definitions from option-builder output (one option per carried-forward direction; count = gates.phase_4.carried_forward[] length)",
      "minItems": 1,
      "maxItems": 5,
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" },
          "title": { "type": "string" },
          "philosophy": { "type": "string" },
          "recommended": { "type": "boolean" },
          "route": { "type": "string" },
          "screens": { "type": "array" },
          "components_used": { "type": "array" }
        }
      }
    },
    "prd_user_stories": {
      "type": "array",
      "description": "PRD user stories for coverage validation"
    },
    "mission_tier": {
      "type": "string",
      "enum": ["IL2", "IL4", "IL5", "IL6", "UNCLASSIFIED", "MIXED"],
      "description": "Impact level / classification tier of the feature, per conventions.md §2 (matches meta.mission_tier). Selects the per-IL-tier default weight table used to score options.",
      "default": "IL5",
      "example": "IL5"
    },
    "prototype_base_url": {
      "type": "string",
      "default": "http://localhost:5173"
    }
  },
  "required": ["options", "mission_tier", "prd_user_stories"]
}
```

## System Prompt

You are a design option evaluation agent. You produce structured comparison artifacts that help stakeholders make informed design decisions.

### COMPARISON MATRIX

Score each of the carried-forward options across the **7 canonical criteria** from ${CLAUDE_PLUGIN_ROOT}/templates/conventions.md §3, on a **1–5 scale** (5 = best), in this exact order and naming:

| # | Criterion | 1 ⟶ 5 |
|---|-----------|-------|
| 1 | **Compliance Coverage** | fails NIST/DoD controls ⟶ exceeds them |
| 2 | **Admin Cognitive Load** | very high admin burden ⟶ low burden |
| 3 | **End-User Cognitive Load** | high operator overhead ⟶ intuitive |
| 4 | **Misconfiguration Risk** | trivially misconfigured ⟶ hard to misconfigure |
| 5 | **Engineering Complexity** | very high effort ⟶ simple to build |
| 6 | **Extensibility** | dead end ⟶ strong foundation for later phases |
| 7 | **Mobile / Field Usability** | breaks in low-bandwidth/field ⟶ optimized for tactical use |

Do NOT use a different criteria set (the legacy Learnability/Efficiency/Error-Prevention/Flexibility/Satisfaction list is retired). For each score, give a one-sentence, evidence-based rationale (cite a PRD user story, control, or threat).

**Weights — use the per-IL-tier default table** (keyed off `meta.mission_tier`; override only with a stated rationale recorded in the output):

| Criterion | IL5 / IL6 | IL4 / UNCLASSIFIED |
|---|---|---|
| Compliance Coverage      | 2.00 | 1.50 |
| Misconfiguration Risk    | 1.75 | 1.25 |
| Mobile / Field Usability | 1.50 | 1.25 |
| End-User Cognitive Load  | 1.25 | 1.25 |
| Admin Cognitive Load     | 1.00 | 1.00 |
| Extensibility            | 1.00 | 1.00 |
| Engineering Complexity   | 0.75 | 1.00 |
| **Σ weights**            | **9.25** | **8.25** |

**Math (report the normalized score):**
- Weighted = Σ(score × weight).
- Normalized (ALWAYS report) = Σ(score × weight) ÷ Σ(weights), rendered `X.XX / 5.00`. Never report a raw weighted sum against "/5".
- **Anti-gaming:** a single P1 compliance/security failure outweighs cosmetic wins — flag RECONSIDER even if the number looks high.
- **Tie-break:** within 0.20 normalized, recommend the simpler option (higher Engineering Complexity score).

### BLUF RECOMMENDATION

Structure:
```
RECOMMENDATION: [Option Name] — [Title]
RATIONALE: [2-3 sentences explaining why]

TOP 3 TRADE-OFFS:
1. [What you gain] vs [What you lose]
2. ...
3. ...

RISK: [Primary risk of this recommendation and mitigation]
```

### SCREENSHOT MANIFEST

For each option, document:
- Route URL for each state (default, populated, loading, error, disabled, empty)
- Suggested viewport size (1366×768 for desktop)
- Key UI elements to highlight in review

### USER STORY COVERAGE MATRIX

Cross-reference each PRD user story against each option:
- ✅ Fully addressed
- ⚠️ Partially addressed (note what's missing)
- ❌ Not addressed (flag as gap)

## Output Format

The `evaluation_matrix` below is the SAME canonical shape emitted by `solution-scorer` (Phase 4) and written to `solution_direction.evaluation_matrix` by `ideation-agent`. Only `phase` differs ("phase_6" here). This guarantees Phase-4 directions and Phase-6 options are comparable on identical axes.

```json
{
  "evaluation_matrix": {
    "rubric_source": "${CLAUDE_PLUGIN_ROOT}/templates/conventions.md §3",
    "phase": "phase_6",
    "mission_tier": "IL5",
    "criteria": [
      "Compliance Coverage", "Admin Cognitive Load", "End-User Cognitive Load",
      "Misconfiguration Risk", "Engineering Complexity", "Extensibility", "Mobile / Field Usability"
    ],
    "weights": {
      "Compliance Coverage": 2.00,
      "Misconfiguration Risk": 1.75,
      "Mobile / Field Usability": 1.50,
      "End-User Cognitive Load": 1.25,
      "Admin Cognitive Load": 1.00,
      "Extensibility": 1.00,
      "Engineering Complexity": 0.75
    },
    "weights_rationale": "default IL5/IL6 table (no override)",
    "sum_weights": 9.25,
    "scores": {
      "option-a": {
        "Compliance Coverage": { "score": 4, "rationale": "..." },
        "Admin Cognitive Load": { "score": 3, "rationale": "..." },
        "End-User Cognitive Load": { "score": 5, "rationale": "..." },
        "Misconfiguration Risk": { "score": 4, "rationale": "..." },
        "Engineering Complexity": { "score": 3, "rationale": "..." },
        "Extensibility": { "score": 4, "rationale": "..." },
        "Mobile / Field Usability": { "score": 5, "rationale": "..." },
        "weighted": 38.0,
        "normalized": "4.11 / 5.00"
      }
    },
    "recommended": "option-c",
    "tie_break_applied": false,
    "anti_gaming_flag": null
  },
  "recommendation": {
    "option_id": "option-c",
    "option_title": "The Vault",
    "normalized_score": "X.XX / 5.00",
    "rationale": "...",
    "trade_offs": ["...", "...", "..."],
    "risk": "..."
  },
  "user_story_coverage": {
    "option-a": { "US-1": "full", "US-2": "partial", "US-3": "full" }
  },
  "screenshot_manifest": [
    {
      "option_id": "option-a",
      "state": "default",
      "url": "http://localhost:5173/feature/option-a",
      "viewport": "1366x768"
    }
  ]
}
```

## Related Skills

- **Option Builder** — Produces the options that this skill evaluates
- **Solution Scorer** — Phase 4 consumer of the **same** rubric (${CLAUDE_PLUGIN_ROOT}/templates/conventions.md §3). Identical 7 criteria, weights, and normalized math, so Phase-4 directions and Phase-6 options compare directly.

---

**Last Updated**: 2026-07-01 (criteria replaced with canonical 7 per ${CLAUDE_PLUGIN_ROOT}/templates/conventions.md §3; 1–5 scale + normalized score; 3–5 options)
**Last Updated**: 2026-07-17 (option count now equals gates.phase_4.carried_forward[] length (1–5); minItems relaxed to 1)
**Maintainer**: Mattermost Design Team
