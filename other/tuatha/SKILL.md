---
name: tuatha
description: |
  The British Isles Formative Assessment MMO. The canonical
  capability for the new tuatha/ independent sub-project at
  ${CIANFHOGHLAIM_ROOT:-~/dev/cianfhoghlaim}/tuatha/
  (soon to be the independent GitHub repo at
  github.com/cianmacandeisigh/tuatha.git). The 8 NCCA Leaving
  Certificate subjects + the 3 educational agents + the 4
  BIEP hackathon features + the 1 media_intel pipeline.

  Use this skill when adding or modifying anything in the new
  tuatha/ sub-project: the 8 subject agents, the 40
  subject-specific tools, the 3 educational agents, the 4 BIEP
  hackathon features, the media_intel pipeline, the BAML
  contracts, the DLT sources, the Dagster asset groups, the
  CocoIndex v1 Apps, the marimo notebooks, the badges
  credential system, the web layer, the CI, the docs, the
  tests.

  The skill supersedes the deprecated tuatha-mmo +
  tuatha-platform + celtic-asset-generation skills. The
  legacy theming (Pent-Elemental Cosmology + Babylon.js 3D +
  SpacetimeDB v2 + Crypteolas + Anam Cara + Brown Ajah) is
  HARD-ARCHIVED per the 2026-08-25 consolidation change. The
  new tuatha uses the British Isles Formative Assessment MMO
  theme per openspec/specs/cianfhoghlaim-educational-mmo.
when_to_use: "tuatha British Isles Formative Assessment MMO consolidation BAML extraction DLT source Dagster asset group CocoIndex App marimo notebook"
---

# `tuatha` — The British Isles Formative Assessment MMO

> **The canonical capability for the new tuatha/ sub-project.**
> A self-contained independent sub-project at
> `${CIANFHOGHLAIM_ROOT:-~/dev/cianfhoghlaim}/tuatha/`
> (the new top-level dir; will become the independent GitHub
> repo at `github.com/cianmacandeisigh/tuatha.git`).

## Routing

Load this skill when:

- You are adding or modifying anything in the new `tuatha/`
  sub-project
- You are updating the cross-repo references in the parent
  cianfhoghlaim monorepo
- You are writing the openspec change that documents the
  consolidation (see the canonical change
  `2026-08-25-tuatha-british-isles-mmo-consolidation-v1`)

For the broader tuatha spec context, see
`openspec/specs/tuatha-british-isles-mmo/spec.md` (the new
canonical spec added by the consolidation change).

## Quick start

```bash
# The new tuatha project lives at the monorepo root
cd ${CIANFHOGHLAIM_ROOT:-~/dev/cianfhoghlaim}/tuatha/

# Read the planning + execution docs
cat CONSOLIDATION_PLAN.md     # the high-level plan
cat BUILD_PLAN.md            # the per-step execution plan

# The 8 NCCA subject agents (per subject directory)
ls subjects/

# The 40 per-subject tools (per subject + per tool)
ls tools/

# The 3 educational agents
ls agents/educational/

# The 4 BIEP hackathon features
ls agents/hackathon/

# The 1 media_intel pipeline (the 10-tool agent)
ls agents/media_intel/

# The per-spec AGENTS.md
cat openspec/specs/tuatha-british-isles-mmo/AGENTS.md
```

## Key sources

- `openspec/specs/tuatha-british-isles-mmo/spec.md` — the new
  canonical spec
- `openspec/specs/cianfhoghlaim-educational-mmo/spec.md` — the
  spec the new tuatha implements
- `tuatha/CONSOLIDATION_PLAN.md` — the high-level plan
- `tuatha/BUILD_PLAN.md` — the per-step execution plan
- `agents/agent_registry.py:AGENT_REGISTRY` — the registration
  for the 14 main agents + the 8 NCCA subject specialists
  (re-routed)
- `agents/meaisinfhoghlaim/media_intel/` — the back-compat shim
  for the media_descriptor_agent re-route

## Adjacent specs

- [`openspec/specs/cianfhoghlaim-educational-mmo/spec.md`](../../specs/cianfhoghlaim-educational-mmo/spec.md)
  — the spec the new tuatha implements
- [`openspec/specs/tuatha-platform/spec.md`](../../specs/tuatha-platform/spec.md)
  — the DEPRECATED spec (superseded by cianfhoghlaim-educational-mmo)
- [`openspec/specs/repo-hygiene-agent-routing/spec.md`](../../specs/repo-hygiene-agent-routing/spec.md)
  — the per-spec AGENTS.md convention
- [`openspec/specs/agent-platform-cluster/spec.md`](../../specs/agent-platform-cluster/spec.md)
  — the 8-stack agent cluster IaC
- [`openspec/specs/agentic-frontend-frameworks/spec.md`](../../specs/agentic-frontend-frameworks/spec.md)
  — the TanStack Start + Convex + Hono + CopilotKit + AG-UI
- [`openspec/specs/british-isles-education-pipeline-v3/spec.md`](../../specs/british-isles-education-pipeline-v3/spec.md)
  — the British Isles education pipeline (the prior pipeline the
  tuatha follows)
- [`openspec/specs/british-isles-formative-assessment/spec.md`](../../specs/british-isles-formative-assessment/spec.md)
  — the 5 curriculum frameworks + the 4 feedback channels
- [`openspec/specs/centralized-model-registry/spec.md`](../../specs/centralized-model-registry/spec.md)
  — the 24-entry VISION_MODELS + the 7-family MODEL_REGISTRY

## DO NOT

- **Never** add back the Pent-Elemental Cosmology + Babylon.js +
  SpacetimeDB + Crypteolas + Anam Cara + Brown Ajah theming —
  these are HARD-ARCHIVED per the consolidation change
- **Never** create a per-app `apps/<app>/apps/api/src/` for
  CopilotKit actions — they live at `tuatha/web/hono-api/src/routes/copilotkit/`
- **Never** hardcode a model string in any extractor — route
  through `MODEL_REGISTRY.resolve(family, role)`
- **Never** use a Plan B or Plan C Firecrawl tool when the
  keyless tier is active (Plan A is the default)
- **Never** commit a copyrighted comic panel image, animation
  frame still, or game screenshot to the repo (the
  `shippable: false` invariant — the descriptor is
  description-only)
- **Never** declare `shippable_default: true` without explicit
  operator override
- **Never** add a new source without a `source.yaml` manifest
- **Never** skip the `legal_notes` field in any `source.yaml`
- **Never** use "Wikipedia Foundation" as `rights_holder` — use
  the original publisher of the official document (e.g.,
  "An Garda Síochána", "Metropolitan Police Service", "Crown
  copyright")

## Skill pointers

| Skill | When to load |
|:--|:--|
| [`ccc`](../ccc/SKILL.md) | for semantic code search across the new tuatha/ project |
| [`centralized-registry`](../centralized-registry/SKILL.md) | MODEL_REGISTRY + schema + codegen patterns |
| [`british-isles-formative-assessment`](../british-isles-formative-assessment/SKILL.md) | the 5 curriculum frameworks + the 4 feedback channels |
| [`baml`](../baml/SKILL.md) | BAML extraction patterns + the 8-stage BAML lifecycle |
| [`dlt`](../dlt/SKILL.md) | DLT source patterns + the `source.yaml` manifest |
| [`dagster`](../dagster/SKILL.md) | the 5-layer Cianfhoghlaim Component Architecture |
| [`agent-fleet-orchestration`](../agent-fleet-orchestration/SKILL.md) | the 12-agent fleet wiring + the 5-framework runtime + the LiteLLM routing keyword map |
| [`dignified-python`](../dignified-python/SKILL.md) | production Python standards |
| [`motherduck`](../motherduck/SKILL.md) | the lakehouse / DuckDB / MotherDuck query surface |

## Cross-references

- [`tuatha/CONSOLIDATION_PLAN.md`](../../../tuatha/CONSOLIDATION_PLAN.md)
  — the high-level consolidation plan
- [`tuatha/BUILD_PLAN.md`](../../../tuatha/BUILD_PLAN.md)
  — the per-step execution plan
- [`../../specs/cianfhoghlaim-educational-mmo/spec.md`](../../specs/cianfhoghlaim-educational-mmo/spec.md)
  — the canonical British Isles MMO spec
- [`../agents-sync/SKILL.md`](../agents-sync/SKILL.md) — the
  Layer 10 of the knowledge-sync-loop

## Thematic guidelines

The new tuatha/ project ADOPTS the British Isles Formative
Assessment MMO theme. The 8 NCCA Leaving Certificate subjects
are the canonical content surface.

**KEEPS** (the technological choices):
- The 8 NCCA subject agents (mathematics / applied_mathematics
  / chemistry / geography / history / english / gaeilge /
  computer_science)
- The 5 per-subject tools (syllabus_lookup / past_paper_lookup
  / marking_scheme_lookup / formative_item_generate /
  response_score)
- The 12-agent fleet pattern (root_agent + curriculum_agent +
  ...)
- The 3 educational agents (academic_history_agent +
  celtic_grammar_agent + celtic_morphology_agent)
- The 4 BIEP hackathon features (marking_grader +
  adaptive_tutor + equivalency_generator +
  curriculum_change_sensor)
- The 1 media_intel pipeline (the 10-tool ADK agent)
- The BAML extraction + DLT + Dagster + CocoIndex + marimo
  pipeline stack
- The Hono + Convex + TanStack Start + CopilotKit web stack
- The LiteLLM + Cognee + Graphiti + LanceDB + Letta memory stack
- The educational-credential badge system (the
  `badges/` subdir; the previous `crypteolas/` financial-token
  system is archived)

**DROPS** (the legacy theming):
- ~~Pent-Elemental Cosmology~~ (5 realms: Spirit / Water /
  Fire / Earth / Air) — hard-archived
- ~~Babylon.js 3D~~ game front-end — replaced with the
  TanStack Start 2D client
- ~~SpacetimeDB v2~~ game engine backend — replaced with
  Convex + Hono + Dagster + DuckLake
- ~~Crypteolas financial token~~ — replaced with the
  educational-credential badge system
- ~~Anam Cara soul friend mechanic~~ — replaced with the 4 BIEP
  hackathon features
- ~~Brown Ajah theming~~ (the 8 NCCA subject ↔ Tuatha Dé deity
  mapping is preserved as `tuatha/subjects/character.py` but the
  "Brown Ajah" name is dropped)

The Celtic MMO design itself — which elements, what boons, the
4+1 element binding, the sub-nation mapping, the 2D particle
renderer choice, the iOS delivery vehicle — is the downstream
theming change gated on the corpus being populated. **NOT in
this change.**
