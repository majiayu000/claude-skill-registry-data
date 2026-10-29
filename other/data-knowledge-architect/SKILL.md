---
name: data-knowledge-architect
description: >-
  Builds semantic models from API, CLI, and database contracts with an HTML review and OKF/YAML export. Use when modeling enterprise knowledge, semantic layers, dimensional models, or ontology.
metadata:
  language: en
  translation_of: data-knowledge-architect-cn
  version: "1.1.0"
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills/tree/main/skills/en/data-knowledge-architect
---

# Data Knowledge Architect — Model the Meaning Behind Your Data

Turn an interface contract—REST/OpenAPI, CLI, or table/DDL—into a governed semantic layer in four
strictly sequential phases. Advance only when the current phase meets its exit condition.

```text
Phase 1 Ingest → Phase 2 Review → Phase 3 Emit → Phase 4 Verify
   ingest.md       review.md      emit-okf.md      verify.md
                                  emit-yaml.md
```

The interface is the sole source of truth. Never invent fields, grain, enums, or values. Stop on
missing evidence and ask one question at a time.

## Workflow

1. **Ingest** (`references/ingest.md`) — Normalize interfaces into a complete operation inventory
   and classify each operation as fact or dimension lookup with read/write status. Exit when every
   operation is classified.
2. **Review** (`references/review.md`) — Decompose the model into atomic decisions. Show objective,
   options, evidence, risks, dependencies, and tradeoffs, with fixed YAGNI guidance for facts,
   dimensions, measures, and routing. Inject model JSON into `assets/review-template.html`; record
   feedback in `amendments.md` and regenerate. Stop after the report. Exit only on `approved:true`
   with no open or blocked decisions.
3. **Emit** — Default to a Google OKF v0.1 bundle using `references/emit-okf.md`; use repository
   YAML only when explicitly requested, following `references/emit-yaml.md`. Both targets share
   field semantics. Generate a thin root index for two or more bundles. Exit when every artifact
   exists.
4. **Verify** (`references/verify.md`) — Run structural checks, semantic lint, and OKF hard
   constraints when applicable. Report every pass and failure. Return non-mechanical failures to
   Phase 2 with one blocking question.

## Critical Rules

1. **Evidence only** — Unsupported fields, grain, enums, or values become `TODO(verify)` and an open
   decision.
2. **Grain first** — Attach no dimensions or measures before grain is fixed.
3. **One blocking ask** — Stop only when an answer changes the model; ask one question with options.
   Use the HTML review for bulk decisions.
4. **Layer split** — Shape, routing, and grain belong to the semantic layer. Values typed into
   commands or read from responses—enums, codes, paths, and commands—belong to the contract layer;
   the semantic layer only points to them.
5. **Stable names** — Do not rename confirmed fact or dimension names; OKF concept IDs derive from
   paths.
6. **Decision gate** — Every decision starts pending. Phase 2 must stop after producing the report;
   Phase 3 requires `approved:true` and no open or blocked item.

Load by phase: `ingest.md`, `review.md`, `emit-okf.md` or `emit-yaml.md`, then `verify.md`. Read
`references/examples.md` for an end-to-end example.
