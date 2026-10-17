---
name: integrable-lattice-generate
description: Project-specific unresolved statement generation for integrable-lattice. Use when Codex needs to turn unknown gap-map cells into concrete candidate theorems, conjectures, or paper-sized finite-symbol statements in integrable lattice models.
---

# Integrable Lattice Generate

## Goal

Convert gap-map cells into concrete unresolved statement candidates that could become paper results.

## Required Context

Read:

- **`CLAUDE.md` / `AGENTS.md` (mandatory before starting)** — the repository's top-priority conventions: proof form (structured text under `structured-latex/`; **never author new Typst**), naming rules, verification commands, the definition of "done", and **"文書・定理を番号や記号で管理しない"** (never manage documents, theorems, or classifications by number or symbol — call them by name).
- `integrable-lattice/README.md` and `integrable-lattice/docs/tasks/auto-loop-runbook.md` — project goal and the auto-loop procedure.
- `docs/discussion/対数順序群上の統計力学/` and `docs/discussion/可算性の効用/` — primary sources for the countable core (ℕ⊂ℚ⊂Λ⊂ℚ̄) and for treating ℝ/ℂ as a convenience for applications; the countable/ℝ boundary is the decidability boundary.
- `docs/research/R-Lambda-duality/` — the ℝ-side / Λ-side duality and what counts as a closed form on the countable side.
- `docs/research/場の量子論の数学的定式化/` — which layers of existing physics close algebraically and which escape to ℝ.
- `integrable-lattice/docs/schemas.md`
- relevant gap-map entries from `integrable-lattice/outputs/maps/`
- nearest known anchors from the classified literature

## Workflow

1. Start from unknown or needs-review gap cells with a nearby known anchor.
2. Write the candidate as a mathematical statement, not just a topic.
3. State the finite-symbol process expected to prove it: local relation, transfer-matrix algebra, determinant/Pfaffian reduction, T-system recurrence, q-series identity, or small-size extrapolation.
4. Identify the exact shift from known work: boundary, rank, representation, root of unity, elliptic/trigonometric/rational regime, finite-size truncation, defect, or model family.
5. Add a small-case experiment plan when possible.
6. Save candidates under `integrable-lattice/outputs/candidates/`.

## Output Shape

Use `StatementCandidate` from `integrable-lattice/docs/schemas.md`.

Minimum required fields:

```yaml
id:
title:
model_family:
model:
operation_type:
statement_type:
known_result_anchor:
missing_generalization:
candidate_statement:
finite_symbol_process:
expected_proof_strategy:
small_case_experiment:
resolved_risk: unchecked
novelty_risk: unchecked
paper_potential: unknown
references:
```

## Guardrails

- Do not generate candidates from unsupported gaps; every candidate needs a known anchor.
- Avoid vague statements like "study X". Use theorem-shaped statements.
- Mark speculative candidates as speculative rather than laundering them into open problems.
- State, for every symbol in the candidate statement, which set it lives in (ℕ / ℤ / ℚ / Λ / ℚ̄ / ℝ / ℂ).
  Where ℝ/ℂ appears, classify the escape by name and record the reason:
  見かけだけの ℝ 脱出 / 実対数による ℝ 脱出 / 指数評価による ℝ 脱出 / 極限・積分による ℝ 脱出 /
  完備性・可分性を要する構造. A 見かけだけの ℝ 脱出 must be rewritten away, not carried forward.
- Prefer formulations that stay in the countable core: finite sums over integrals, difference
  quotients over derivatives, integer comparison over real ordering
  (`docs/discussion/対数順序群上の統計力学/`, `docs/research/R-Lambda-duality/`).
- Keep finite-size claims and post-limit claims as separate candidates; do not merge them into one statement.
- Name candidates by content, never by a bare number or letter code; the repository convention
  "文書・定理を番号や記号で管理しない" (CLAUDE.md) applies to candidate ids and titles too.
- Candidate files under `outputs/candidates/` are exploration-phase artifacts. **Promoting a candidate to
  a proposition means writing it as structured text under `integrable-lattice/structured-latex/`,
  following the `math-prover` skill and `CLAUDE.md`. Never write it in Typst — Typst
  authoring is abolished in this repository.**

