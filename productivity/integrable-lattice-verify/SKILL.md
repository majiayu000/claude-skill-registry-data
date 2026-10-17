---
name: integrable-lattice-verify
description: Project-specific verification for integrable-lattice candidates. Use when Codex needs to check whether a generated unresolved statement candidate is already solved, follows from a known theorem, is ill-defined, has small-case counterexamples, or remains plausible as a paper target.
---

# Integrable Lattice Verify

## Goal

Reduce false candidates. Verification does not prove the candidate; it tests whether it is still a credible unresolved target.

## Required Context

Read:

- **`CLAUDE.md` / `AGENTS.md` (mandatory before starting)** — the repository's top-priority conventions: proof form (structured text under `structured-latex/`; **never author new Typst**), naming rules, verification commands, the definition of "done", and **"文書・定理を番号や記号で管理しない"** (never manage documents, theorems, or classifications by number or symbol — call them by name).
- `integrable-lattice/README.md` and `integrable-lattice/docs/tasks/auto-loop-runbook.md` — project goal and the auto-loop procedure.
- `docs/discussion/対数順序群上の統計力学/` and `docs/discussion/可算性の効用/` — primary sources for the countable core (ℕ⊂ℚ⊂Λ⊂ℚ̄) and for treating ℝ/ℂ as a convenience for applications; the countable/ℝ boundary is the decidability boundary.
- `docs/research/R-Lambda-duality/` — the ℝ-side / Λ-side duality and what counts as a closed form on the countable side.
- `docs/research/場の量子論の数学的定式化/` — which layers of existing physics close algebraically and which escape to ℝ.
- the candidate record from `integrable-lattice/outputs/candidates/`
- its known anchors and references
- relevant seed queries and aliases for the model/operation

## Workflow

1. Search exact title-like phrases from the candidate statement.
2. Search by aliases: model name variants, boundary condition variants, operation variants.
3. Check whether a more general theorem implies the candidate.
4. Check whether the candidate is ill-defined or incompatible with the model.
5. If feasible, run or outline small-size symbolic/numeric checks.
6. Update risk fields:
   - `resolved_risk`
   - `novelty_risk`
   - `definition_risk`
   - `counterexample_risk`
7. Preserve links and evidence for every risk decision.

## Output Shape

```yaml
candidate_id:
verification_status: plausible | solved | probably_solved | ill_defined | counterexample | needs_more_search
resolved_risk:
novelty_risk:
definition_risk:
counterexample_risk:
evidence:
queries_used:
followup:
```

## Guardrails

- Do not call a candidate open merely because no match appears in one search.
- Do not discard a candidate because a neighboring result exists; identify the exact implication if claiming solved.
- Separate mathematical counterexamples from failed implementation experiments.

