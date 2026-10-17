---
name: integrable-lattice-harvest
description: Project-specific literature harvesting for integrable-lattice. Use when Codex needs to collect candidate papers, metadata, abstracts, identifiers, and source availability for unresolved finite-symbol statement mining in integrable lattice models.
---

# Integrable Lattice Harvest

## Goal

Collect a broad but traceable paper set for the `integrable-lattice` project. The output is not a bibliography; it is raw material for statement extraction.

## Required Context

Before deciding queries or scope, read:

- **`CLAUDE.md` / `AGENTS.md` (mandatory before starting)** — the repository's top-priority conventions: proof form (structured text under `structured-latex/`; **never author new Typst**), naming rules, verification commands, the definition of "done", and **"文書・定理を番号や記号で管理しない"** (never manage documents, theorems, or classifications by number or symbol — call them by name).
- `integrable-lattice/README.md` and `integrable-lattice/docs/tasks/auto-loop-runbook.md` — project goal and the auto-loop procedure.
- `docs/discussion/対数順序群上の統計力学/` and `docs/discussion/可算性の効用/` — primary sources for the countable core (ℕ⊂ℚ⊂Λ⊂ℚ̄) and for treating ℝ/ℂ as a convenience for applications; the countable/ℝ boundary is the decidability boundary.
- `docs/research/R-Lambda-duality/` — the ℝ-side / Λ-side duality and what counts as a closed form on the countable side.
- `docs/research/場の量子論の数学的定式化/` — which layers of existing physics close algebraically and which escape to ℝ.
- `integrable-lattice/README.md`
- `integrable-lattice/inputs/seeds/models.md`
- `integrable-lattice/inputs/seeds/operations.md`
- `integrable-lattice/inputs/seeds/axes.md`
- `integrable-lattice/inputs/queries/seed-queries.md`

## Workflow

1. Identify the target slice: model family, operation type, boundary condition, parameter regime, or seed paper.
2. Expand search phrases from the seed files. Preserve exact phrases for reproducibility.
3. Collect metadata from stable sources first: arXiv, DOI pages, OpenAlex, Semantic Scholar, publisher pages.
4. Prefer arXiv records when available because later extraction can use LaTeX source.
5. Record enough metadata to deduplicate papers: title, authors, year, arXiv id, DOI, URL, abstract, source availability.
6. Save curated query strings under `integrable-lattice/inputs/queries/`.
7. Save harvested metadata under `integrable-lattice/inputs/corpus/` when it is small and curated. For large corpora, save only manifest/query instructions.

## Output Shape

Use this minimal record shape in markdown, YAML, JSON, or JSONL:

```yaml
id:
title:
authors:
year:
source:
arxiv_id:
doi:
url:
abstract:
model_hints:
operation_hints:
source_available:
notes:
```

## Guardrails

- Do not call a paper relevant only because it contains generic terms like "integrable" or "lattice"; connect it to at least one seed model or operation.
- Do not judge novelty here. Mark only retrieval facts and coarse relevance.
- Keep failed or noisy queries when they explain search coverage.

