---
name: ui-pack-maintain
description: Creates, extends, repairs, validates, versions, and publishes reusable UI Packs. Use when adding or changing UI Pack Foundations, Components, Patterns, Presets, design tokens, state adapters, manifests, or registry metadata, or when extracting a reusable visual system from screenshots, existing pages, or computed styles. Creating a Pack relies only on the self-contained contract plus user intent; maintenance may additionally read existing Packs. Do not use for generating business prototypes, editing production frontend code, installing packs for end users, or ordinary page styling.
---

# UI Pack Maintain

Self-contained authoring and publication workflow for UI Packs. This skill owns the pack
contract, schema version rules, registry format, validator, and release metadata. It does not
own consumer-side discovery, download, or prototype generation.

## Quick start

Create a Pack, then validate and resolve it:

```bash
node scripts/validate-pack.mjs --pack=<pack-directory> --strict
node scripts/resolve-pack.mjs --pack=<pack-directory> --entry=<id>[,<id>...]
```

Before publishing pack changes:

```bash
node scripts/generate-registry.mjs
node scripts/generate-registry.mjs --check
```

Landing paths, create/update steps, and the consumer resolver smoke test are in
[Pack authoring](references/pack-authoring.md).

## Responsibility split

| Owns `ui-pack-maintain` | Owns `html-prototype-build` |
|---|---|
| pack contract, `schemaVersion`, `validate-pack.mjs`, registry generation | pack lookup chain, `install-pack.mjs`, `deliver[]` copy-out |
| in-pack `resolve-pack.mjs` (`--pack=<dir> --entry=`) | consumer `resolve-pack.mjs` (`--list` / `--select`) |
| pack lifecycle: create → validate → version → publish | prototype generation |

## Workflow

1. Read `references/contract.md` for structure and responsibility boundaries.
   In **creation** mode, stop here for evidence. In **maintenance** mode,
   continue to step 2.
2. Read the target Pack's `PACK.md` and `manifest.json`, plus only the resource
   entries this task touches (maintenance only).
3. Classify the change as Pack creation, Foundation, Component, Pattern, Preset,
   registry/publication, or repair.
4. Read [Pack authoring](references/pack-authoring.md) and implement the smallest
   reusable change.
5. Update `manifest.json`, then run deterministic validation.
6. For a new Pack or substantial semantic change, run the isolated review in
   [Isolated semantic review](references/semantic-review.md).
7. Regenerate `registry.json` when publishing or changing downloadable metadata.
8. Apply only verified findings, then rerun validation and the resolver smoke test.

Evidence priority is documented in [Evidence authority](references/evidence.md).

Publication references:

- [Registry format](references/registry-format.md)
- [schemaVersion contract](references/schema-version.md)

## Hard boundaries

- Keep a UI Pack inside the directory passed as `--pack=`; this skill owns only
  the workflow, contract, registry format, resolver, and validator. It does not
  hard-code a consumer's pack install location.
- Keep the Foundation DOM-free; include only shared tokens and a document-level
  CSS baseline.
- Keep each Component as one leaf implementation with a local contract.
- Compose Components through Patterns without copying their implementations.
- Keep Presets business-fact-free.
- Keep state adapters to projecting passed local state only; never access
  `PrototypeViewers`, persist state, parse URLs, or register global event handlers.
- Treat `manifest.json` as the only machine-readable index and dependency source.
- Declare only required dependencies in `requires`; keep conditional capabilities
  in `optional`.
- Patterns and Presets must not select internal components directly.
- Do not implement consumer download flows here; point users to
  `html-prototype-build` [Pack install](../html-prototype-build/references/pack-install.md).

## Deterministic validation

```bash
node scripts/validate-pack.mjs --pack=<pack-directory> --strict
```

The validator enforces [the pack contract](references/contract.md), including pack-local
`vendor` / `runtime` / `assets` and `manifest.delivery`. Fix every error before semantic
review. Warnings must be resolved or explicitly reported as evidence gaps.

It cannot judge whether a component boundary is useful or whether visual evidence
is sufficient; delegate those questions to the semantic reviewer.

## Resolver smoke test

```bash
node scripts/resolve-pack.mjs --pack=<pack-directory> --entry=<id>[,<id>...] [--optional=<id>[,<id>...]]
```

This covers in-pack `requires`/`uses` closures only. After validation, also run the
consumer resolver check in [Pack authoring](references/pack-authoring.md#resolver-smoke-tests).
Cross-pack references are out of scope and must be reported as a `ponytail:` evidence gap.

## Completion report

Report:

- changed Pack entries
- evidence used
- provisional decisions and missing evidence
- validator and resolver test results
- registry regeneration status
- unresolved independent-review findings
