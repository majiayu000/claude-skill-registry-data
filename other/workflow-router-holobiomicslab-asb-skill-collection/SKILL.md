---
name: metabolomics-workflow-router
description: Use when a user has a whole metabolomics analysis GOAL (e.g. "annotate my untargeted LC-MS/MS data", "find biomarkers", "where else has this molecule been seen") rather than a single step — select the right end-to-end composite workflow super-skill, then run its stages, grounding each against its source papers.
license: CC-BY-4.0
metadata:
  kind: workflow-router
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  indexes:
  - workflows_index.json
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# ASB Metabolomics — composite workflow router

This is the **goal-level** entry point for the ASB Metabolomics collection. Where the
leaf router (`metabolomics-collection-router`) finds ONE atomic skill, this router selects
an **end-to-end composite workflow super-skill** — an ordered pipeline of stages, each
delegating to vetted leaf skills, with grounding and a declarative `workflow.yaml`.

Use it in three steps: **select → run → ground**.

## 1. Select — match the goal to a workflow

**Prefer semantic retrieval (P2):** run

```bash
python bin/semantic_search.py --query "<the user's goal>" \
  --collection . --target workflows [--technique LC-MS] --k 3
```

It uses meaning-based ranking (text-embedding-3-large — the same model Perspicacité uses)
when an embedding backend is available, and **falls back to a keyword index search
automatically** when it is not, so it always works offline. The result's `mode` field tells
you which ran. The same tool works at the leaf level with `--target skills` (Step 2).

If you prefer manual lookup, load `workflows_index.json` (one row per composite workflow:
`slug`, `name`, `description`, `techniques`, `stages`, `member_tools`) and match the goal,
in order of precision:

1. **Technique** — what platform is the data? `LC-MS`, `GC-MS`, `MS-imaging`,
   `ion-mobility-MS`, `NMR`. Filter `techniques` first.
2. **Goal phrasing** — match the user's intent against each row's `description`.

Available workflows (published as outlines):

| workflow | technique | what it does |
|---|---|---|
| `untargeted-lcmsms-annotation` | LC-MS | raw mzML → preprocess → network → library-match → SIRIUS → fuse → master table |
| `lipidomics-lcms-annotation` | LC-MS | class/species-level lipid annotation + stats |
| `gcms-deconvolution-and-identification` | GC-MS | EI deconvolution → library match → retention index → stats |
| `ms-imaging-spatial-metabolomics` | MS-imaging | imzML → spatial annotation (FDR) → segmentation → region stats |
| `statistics-and-biomarker-discovery` | LC-MS | normalize → multivariate → differential → pathway → biomarkers |
| `sirius-denovo-structure-elucidation` | LC-MS | formula → structure → class → confidence filter (no library needed) |
| `masst-repository-scale-search` | LC-MS | reverse metabolomics: where else does this molecule occur in public data |
| `ion-mobility-4d-annotation` | ion-mobility-MS | 4D feature extraction → CCS calibration → CCS-aware annotation |
| `nmr-metabolomics-profiling` | NMR | spectra → preprocess → identify (chemical shift) → quantify → stats |
| `pathway-functional-analysis` | LC-MS | m/z feature list → mummichog → pathway/enrichment → interpretation |

If no workflow fits the goal, fall back to the **leaf router**
(`metabolomics-collection-router`) and assemble steps from atomic skills.

## 2. Run — execute the workflow's stages

Read the chosen `workflows/<slug>/SKILL.md` and follow its **Stages** in order. Each stage
carries: a goal, candidate leaf skills (primary first), the tools to install/invoke, and
its typed inputs/outputs. The machine-readable `workflows/<slug>/workflow.yaml` is the DAG
(`after`, `inputs_from`). Automatic grading of that DAG (`asb solve-workflow`) is **not part
of this release**: no released ASB version loads these files, so run the stages yourself.
Honor the I/O contract: each stage consumes the prior stage's declared outputs. Optional
stages are marked.

For a stage's leaf skills, read each `skills/<leaf-slug>/SKILL.md` for the procedure, or
use the leaf router to pick among the candidates for your exact data.

## 3. Ground — verify each stage against its source papers

Before trusting a parameter or default, ground the stage's leaves against the papers they
were distilled from. Each stage's `grounding.kb_slugs`/`dois` (in `workflow.yaml`) point at
the `asb-paper-<doi>` KBs. Use the collection's `/ground` command or
`bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

> These workflows are published as **outlines**: the stage structure is validated, the
> execution is not. Bindings were chosen by semantic retrieval (`text-embedding-3-large`) +
> deterministic selection. `derived_from_workflows` in each frontmatter is a provenance
> record; no ablation experiment consuming it is released.
