---
name: mllmcelltype-consensus-annotation
description: "mllmct — a version-locked CLI that annotates scRNA-seq clusters by multi-LLM consensus over marker genes, doing both cell-TYPE and evidence-injected cell-STATE annotation. Reference-free, with per-cluster uncertainty, forced determinism, and a full prompt-to-label trace. Use with per-cluster markers for no-reference labels plus confidence."
license: MIT
---

# mllmct — Multi-LLM Consensus Cell-Type / Cell-State Annotation

**Packaged skill** — execution is outsourced to the pinned CLI below, not re-derived from this
prose. See [docs/packaged-skills.md](../../docs/packaged-skills.md).

One **version-locked, tested command-line tool**. You hand it per-cluster marker genes
(and, for cell-state, per-cluster evidence); it asks several LLMs, reconciles them by consensus
with cross-model discussion, and returns a label per cluster **plus a Python-recomputed
confidence** so you know which calls to trust. You don't need to know how it works to use it —
internals live in `references/`.

**What it gives you over a one-off LLM prompt:** multi-model consensus, **uncertainty
recomputed in Python** (not the LLM's self-reported numbers), forced determinism (`temp=0, seed=0`),
captured token **cost**, and a full **prompt→per-model-vote→label trace** on disk for every run.

**One tool, two modes — chosen by a YAML profile:**

| Mode | Profile | What the LLM sees | Use when |
|---|---|---|---|
| **cell-TYPE** | `profiles/celltype.yaml` | marker genes only | you want reference-free cell-type labels |
| **cell-STATE** | `profiles/cellstate.yaml` | markers **+ injected evidence** (programs, signatures, binned scores) + guardrails | identity is fixed and you want functional-state calls |

---

## Quick Start

```bash
SKILL=path/to/skills/mllmcelltype-consensus-annotation

# 1. Bootstrap the locked sandbox ONCE (isolated; ignores system/base site-packages).
uv sync --project "$SKILL"
uv run --project "$SKILL" python "$SKILL/checks/smoke_check_versions.py"   # pins + seams intact
uv run --project "$SKILL" mllmct selftest                                  # offline, no API

# 2. Provide an API key (see "API keys" below). Provider is derived from the model panel.
export OPENROUTER_API_KEY=sk-or-...        # or GEMINI_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY

# 3a. CELL-TYPE: markers only
"$SKILL/bin/mllmct" annotate \
  --profile "$SKILL/profiles/celltype.yaml" \
  --markers markers.csv \
  --species human --tissue "peripheral blood" \
  --models 'openai/gpt-5,anthropic/claude-sonnet-4.6,google/gemini-2.5-flash' \
  --lens leiden --out runs/pbmc

# 3b. CELL-STATE: markers + injected evidence (identity fixed)
"$SKILL/bin/mllmct" annotate \
  --profile "$SKILL/profiles/cellstate.yaml" \
  --markers clusters.csv --evidence clusters.csv --aux programs.csv \
  --species mouse --tissue "in-vitro culture" \
  --models 'openai/gpt-5,anthropic/claude-sonnet-4.6,google/gemini-2.5-flash' \
  --lens leiden_state --out runs/state
```

`bin/mllmct` runs the tool inside its locked sandbox — no venv activation needed, and it works
even when the skill is discovered through `.claude/skills` after `scio link`.

**Input — `--markers` CSV:** a `cluster` column + a `markers` column of `;`-joined **gene symbols**:

```csv
cluster,markers
0,CD3D;CD3E;IL7R;CCR7;SELL
1,MS4A1;CD79A;CD79B;HLA-DRA
```

(Build it from scanpy: `rank_genes_groups` → `{cl: names[cl][:15]}` → write CSV. Use **symbols**, not Ensembl IDs.)

---

## Decision tree

```
Need labels for scRNA-seq clusters?
├─ Have an annotated reference atlas?            → cellxgene-census-annotation
├─ Have partial ground-truth labels to spread?   → scvi-scanvi
└─ Reference-free, only marker lists?            → mllmct annotate
   ├─ Want a cell TYPE?                           → --profile celltype.yaml   (markers only)
   └─ Identity fixed, want a functional STATE?    → --profile cellstate.yaml  (+ --evidence)
      └─ Two orthogonal axes per cell to merge?   → then: mllmct reconcile
```

---

## Commands

Run `mllmct <cmd> --help` for the full argument list.

| Command | Does | Key args |
|---|---|---|
| `annotate` | Annotate clusters (type or state, per the profile). Writes labels + trace + cost. | `--profile --markers [--evidence --aux] --species --tissue --models --lens --out` |
| `preview-prompt` | Print the EXACT prompt that would be sent. **No API call.** | same inputs as `annotate`, minus `--out/--models` |
| `reconcile` | Two-axis semantic join of a per-cell axes table (pure Python, no LLM). | `--profile --axes-csv --out` |
| `backfill-metrics` | Recompute `py_*` uncertainty from saved `model_annotations`. **No API call.** | `--labels-csv` or `--labels-dir` |
| `selftest` | Offline core-logic smoke test. | (none) |
| `check-env` | Assert pins + monkeypatch seams + API-key presence. | `[--models --env-file --api-key]` |

`annotate` always: derives the provider from the model panel (a slug with `/` → OpenRouter, a bare
id → that vendor), forces `temp=0, seed=0`, captures tokens/cost, writes the trace, and **validates
before writing** (`exit 1` on a hard fail, e.g. an off-vocab label in `closed` mode or a guard leak).

---

## API keys

The tool needs a key for each provider its model panel implies. Provide them any of three ways
(precedence high→low); keys are never written to logs or the trace:

1. **Runtime arg** — `--api-key openrouter=sk-or-...` (repeatable, one per provider).
2. **Environment** — `OPENROUTER_API_KEY` / `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) / `OPENAI_API_KEY` /
   `ANTHROPIC_API_KEY`. Optionally point at a dotenv with `--env-file /path/.env`.
3. If a required key is missing the tool **fails fast** and tells you exactly which `export`
   (or `--api-key`) to add — it never half-runs.

Check readiness without spending anything: `mllmct check-env --models 'openai/gpt-5,gemini-2.5-flash'`.

---

## Outputs (the contract)

`annotate --out DIR` writes:

- **`DIR/labels.csv`** — one row per cluster:
  `cluster, consensus_label, harmonized_label, py_consensus_proportion, py_entropy,
  py_majority_label, llm_reported_proportion, llm_reported_entropy, model_annotations`.
  **The `py_*` columns are authoritative** (recomputed in Python from the per-model votes); the
  `llm_reported_*` columns are kept only for comparison — do not use them as confidence.
- **`DIR/validation.json`** — pass/fail + warnings (novel open-vocab labels are listed for review).
- **`DIR/trace/<lens>/`** — `prompt.txt`, `model_responses.json`, `discussion.json`, `tokens.json`,
  `meta.json` (with git HEAD), `llmcelltype_debug.log`. Every label is traceable back to its prompt.
- **`DIR/trace/cost_summary.json`** — token + USD totals (recoverable even on a fully-cached re-run).

Map labels back onto your AnnData:
```python
import pandas as pd
lab = pd.read_csv("runs/pbmc/labels.csv").set_index("cluster")
adata.obs["cell_type"]  = adata.obs["leiden"].astype(str).map(lab["harmonized_label"])
adata.obs["confidence"] = adata.obs["leiden"].astype(str).map(lab["py_consensus_proportion"])
```

---

## Profiles (switch modes; customize without code)

A **profile** is the one knob that turns cell-type into cell-state. It bundles: whether to inject
evidence, the prompt template, the vocabulary (open/closed + terms + synonyms), domain guards, and
an optional two-axis join. Both shipped profiles work out of the box; the cell-state one is a
**generic neutral example** — copy it and drop in YOUR vocabulary, evidence options, and guards
(keep dataset-specific biology in your analysis repo, not in this shared skill). The profile schema,
writing your own `EvidenceProvider`, and the reconcile config live in
`references/cell-state-annotation.md`.

---

## Verification checklist

- [ ] `mllmct check-env --models <your panel>` → seams PASS and the needed key(s) found.
- [ ] `mllmct preview-prompt …` → the prompt reads correctly (and, for cell-state, the evidence block
      is present and sensible) **before** spending on a real run.
- [ ] After `annotate`: `labels.csv` has one row per cluster and `py_consensus_proportion` is in [0,1];
      triage clusters with low proportion / high `py_entropy`.
- [ ] Spot-check biological plausibility against a marker dotplot; treat any `Novel:*` (open-vocab)
      label as a **hypothesis** needing orthogonal validation, not a conclusion.
- [ ] `checks/check_output_contract.py DIR --lens <lens>` → output contract OK.

---

## Common pitfalls

- **Ensembl IDs as markers** → vague labels. Pass HGNC/MGI **symbols**.
- **Cluster-id type mismatch** when mapping back → build markers keyed by `str(cluster)` and map with
  `adata.obs["leiden"].astype(str)`.
- **Trusting `llm_reported_*`** → those are the LLM's post-discussion self-report; use `py_*` instead.
- **Editing the lock loosely** → only regenerate with `uv lock` **then** `checks/smoke_check_versions.py`
  (the pins guard version-sensitive internals). See `references/monkeypatch-internals.md`.
- **Fully-cached re-run shows $0** → expected; the original cost is preserved in `tokens.json`/`cost_summary.json`.

---

## How it works / extend it (optional reading)

You don't need these to use the tool. When you want internals or to adapt it:

- `references/cell-state-annotation.md` — cell-state mode, profile knobs, writing an `EvidenceProvider`, reconcile.
- `references/monkeypatch-internals.md` — the version-sensitive patches + the lock-regeneration procedure.
- `references/packaging-template.md` — the "locked tool + CLI + logging + tests" pattern, to copy into other skills.
- `references/api-reference.md` — underlying mLLMCelltype API + the Python-recomputed-metrics override.
- `references/r-seurat-workflow.md`, `references/uncertainty-and-hierarchy.md` — upstream-library context.

---

## Resources

- Repository: https://github.com/cafferychen777/mLLMCelltype
- Preprint (Yang et al., 2025): https://doi.org/10.1101/2025.04.10.647852
- PyPI: https://pypi.org/project/mllmcelltype/ (this skill pins `2.0.7`)

---

## When not to use

- Do not use for label transfer from an annotated reference atlas. Use cellxgene-census-annotation instead.
- Do not use for semi-supervised propagation from partial ground-truth labels. Use scvi-scanvi instead.
- Do not pass Ensembl IDs (ENSG…/ENSMUSG…)

---

## See also

- `scanpy` — Prerequisite; clustering + marker genes that feed this tool
- `cellxgene-census-annotation` — Alternative; label transfer from an annotated atlas
- `scvi-scanvi` — Alternative; semi-supervised propagation from partial labels
- `single-cell-rna-qc` — Prerequisite; MAD-based QC before clustering
- `consensus-nmf-multirun` — Upstream (evidence); gene programs to inject as cell-state evidence
