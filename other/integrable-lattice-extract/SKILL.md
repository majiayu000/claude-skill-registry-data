---
name: integrable-lattice-extract
description: Project-specific extraction of statement fragments from integrable-lattice papers. Use when Codex needs to extract model names, boundary conditions, theorem/conjecture/open-problem text, formula labels, and finite-symbol operation hints from harvested lattice-model literature.
---

# Integrable Lattice Extract

## Goal

Turn harvested papers into statement fragments. A fragment is evidence for a possible known result, open problem, or operation type.

## Required Context

Before extraction, read:

- **`CLAUDE.md` / `AGENTS.md` (mandatory before starting)** — the repository's top-priority conventions: proof form (structured text under `structured-latex/`; **never author new Typst**), naming rules, verification commands, the definition of "done", and **"文書・定理を番号や記号で管理しない"** (never manage documents, theorems, or classifications by number or symbol — call them by name).
- `integrable-lattice/README.md` and `integrable-lattice/docs/tasks/auto-loop-runbook.md` — project goal and the auto-loop procedure.
- `docs/discussion/対数順序群上の統計力学/` and `docs/discussion/可算性の効用/` — primary sources for the countable core (ℕ⊂ℚ⊂Λ⊂ℚ̄) and for treating ℝ/ℂ as a convenience for applications; the countable/ℝ boundary is the decidability boundary.
- `docs/research/R-Lambda-duality/` — the ℝ-side / Λ-side duality and what counts as a closed form on the countable side.
- `docs/research/場の量子論の数学的定式化/` — which layers of existing physics close algebraically and which escape to ℝ.
- `integrable-lattice/docs/schemas.md`
- `integrable-lattice/inputs/seeds/models.md`
- `integrable-lattice/inputs/seeds/operations.md`
- the relevant harvested records in `integrable-lattice/inputs/corpus/`

## Workflow

1. Prefer arXiv LaTeX source over PDF text. Use abstract text only for coarse extraction.
2. Search for section headers and environments: theorem, proposition, lemma, corollary, conjecture, problem, open problem, future work.
3. Extract model names, boundary conditions, parameter regimes, algebraic objects, and operation names.
4. Extract formula labels and nearby prose for finite-symbol relations: Yang-Baxter, star-triangle, reflection equation, fusion, T-system, Y-system, determinant, Pfaffian, character identity.
5. Capture enough local context to support classification without copying long passages.
6. Preserve uncertainty. Use `unknown` rather than forcing a classification.

## Output Shape

```yaml
fragment_id:
paper_id:
location:
text_summary:
raw_short_quote:
model_hints:
boundary_hints:
parameter_hints:
operation_hints:
statement_hints:
status_hints:
equation_labels:
notes:
```

## Guardrails

- Do not infer an open problem from absence alone; extract explicit evidence or mark as unknown.
- Do not collapse different boundary conditions or parameter regimes.
- Keep formulas tied to their source location, because later novelty checks depend on traceability.

