---
name: scrna-pipeline-conventions
description: >-
  Assay-specific conventions for restartable scRNA-seq objects and milestone
  packaging. Use when choosing AnnData checkpoints and deliverables, packaging
  gene identifiers or dual embeddings, cleaning obs metadata, or preserving
  uncertain annotation states. Structural analysis-code decisions route to
  analysis-code-conventions.
license: MIT
---

# scRNA-seq Pipeline Conventions

Use this skill for the scRNA-specific objects and deliverables shared by
`cellranger-multi-to-anndata`, `scrna-cxg-host`, and
`consensus-nmf-multirun`. Apply the CRAFT block and
`analysis-code-conventions` for stage naming, layout, helper boundaries,
configuration placement, and generic restartability.

## Routing decision tree

```text
What scRNA deliverable decision is being made?
│
├─ Is this an intermediate checkpoint or a finalized object?
│     → checkpoints-and-objects.md
│
├─ Which gene identifier should be active at delivery?
│     → gene-identifier-packaging.md
│
├─ Which embeddings must the packaged object carry?
│     → embedding-deliverables.md
│
└─ How should obs metadata and uncertain labels be packaged?
      → metadata-packaging.md
```

## Routing contract

1. Apply the repository's rendered CRAFT block for standing stage and result
   mechanics; load `analysis-code-conventions` for structural judgment.
2. Select the scRNA deliverable question and read its reference completely.
3. Load every relevant reference when finalizing an object because identifier,
   embedding, metadata, and derivation guarantees interact.
4. Read numeric thresholds and project choices from the project's current
   configuration and decision records. Preserve their provenance.
5. Use the adjacent conversion or hosting skill for tool-specific execution.

## References (load on demand)

| Intent | Load |
|---|---|
| Plan recovery objects and the canonical milestone | [`references/checkpoints-and-objects.md`](references/checkpoints-and-objects.md) |
| Package symbols while preserving stable identifiers | [`references/gene-identifier-packaging.md`](references/gene-identifier-packaging.md) |
| Carry discovery and integrated embeddings | [`references/embedding-deliverables.md`](references/embedding-deliverables.md) |
| Clean `obs` and preserve annotation uncertainty | [`references/metadata-packaging.md`](references/metadata-packaging.md) |

## Adjacent skills

- `analysis-code-conventions` — structural stages, helpers, configuration, and
  restartable data flow.
- `cellranger-multi-to-anndata` — build the initial pooled AnnData object.
- `single-cell-rna-qc` — perform assay QC before milestone packaging.
- `anndatar-seurat-scanpy-conversion` — derive a Seurat object from AnnData.
- `louper-seurat-conversion` — derive a Loupe object from the packaged data.
- `scrna-cxg-host` — validate and host the CellxGene derivative.

## When not to use

- Generic stage sequencing, helper extraction, or project layout decisions.
- Assay methodology such as QC models, integration choice, or differential tests.
- Throwaway exploration with no durable scRNA object or collaborator handoff.
