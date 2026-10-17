---
name: integrable-lattice-classify
description: Project-specific classification for integrable-lattice statement fragments. Use when Codex needs to map extracted fragments onto the project taxonomy, including model family, model, operation type, statement type, boundary condition, parameter regime, and solved/open/unknown status.
---

# Integrable Lattice Classify

## Goal

Map extracted fragments onto the project taxonomy without overstating certainty.

## Required Context

Read:

- **`CLAUDE.md` / `AGENTS.md` (mandatory before starting)** — the repository's top-priority conventions: proof form (structured text under `structured-latex/`; **never author new Typst**), naming rules, verification commands, the definition of "done", and **"文書・定理を番号や記号で管理しない"** (never manage documents, theorems, or classifications by number or symbol — call them by name).
- `integrable-lattice/README.md` and `integrable-lattice/docs/tasks/auto-loop-runbook.md` — project goal and the auto-loop procedure.
- `docs/discussion/対数順序群上の統計力学/` and `docs/discussion/可算性の効用/` — primary sources for the countable core (ℕ⊂ℚ⊂Λ⊂ℚ̄) and for treating ℝ/ℂ as a convenience for applications; the countable/ℝ boundary is the decidability boundary.
- `docs/research/R-Lambda-duality/` — the ℝ-side / Λ-side duality and what counts as a closed form on the countable side.
- `docs/research/場の量子論の数学的定式化/` — which layers of existing physics close algebraically and which escape to ℝ.
- `integrable-lattice/docs/schemas.md`
- `integrable-lattice/inputs/seeds/models.md`
- `integrable-lattice/inputs/seeds/operations.md`
- `integrable-lattice/inputs/seeds/axes.md`
- extracted fragments from the current task

## Workflow

1. Normalize model names to the closest seed model, while preserving source terminology.
2. Classify operation type using `OperationType` in `docs/schemas.md`.
3. Classify statement type using `StatementType` in `docs/schemas.md`.
4. Separate status from content:
   - `known`: the paper proves or cites the statement as established.
   - `conjectured`: the paper states it as conjecture.
   - `open`: the paper explicitly presents it as open.
   - `unknown`: evidence is insufficient.
5. Record boundary and parameter conditions explicitly.
6. Add ambiguous cases to `integrable-lattice/inputs/labels/` for human review.

## Output Shape

```yaml
fragment_id:
paper_id:
canonical_model_family:
canonical_model:
source_model_name:
operation_type:
statement_type:
boundary_condition:
parameter_regime:
status:
confidence:
evidence:
review_needed:
notes:
```

## Guardrails

- Do not mark a gap as open during classification; gap detection happens in `integrable-lattice-gap-map`.
- Do not merge "determinant formula exists" with "this determinant formula is evaluated" unless the evidence supports both.
- Prefer `review_needed: true` for terminology mismatches.
