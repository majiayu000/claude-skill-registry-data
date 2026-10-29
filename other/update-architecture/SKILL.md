---
name: update-architecture
description: Keep the canonical, LAYERED Open Lakehouse architecture model (LikeC4, in architecture/) in sync with the estate. Logical layer = abstract capabilities, concerns, asset kinds, and the technology catalog (no repo names in the reference); deployment layer = our services realizing them. Traverses sibling repos' docs/ADRs, proposes minimal .likec4 patches for human approval, then regenerates artifacts. Use when a service/deployment changes, a new capability or asset kind appears, an instanceOf mapping changes, or designed work becomes built.
user-invocable: true
version: 0.2.0
---

You maintain the canonical architecture model at `docs-factory/architecture/`.
Your job: fold a structural change into the LikeC4 model as a **minimal** patch,
show it for human approval, then regenerate the committed artifacts. You never
invent facts — you read them from the estate.

**Scope:** `architecture/` holds *only* fact about the lakehouse we document (the
model, its design docs, its ADRs, `estate.yml`, `glossary.md`).
Decisions about the **docs factory itself** (site, emitters, review server, authoring
pipeline) live in `docs/` and are **out of scope for this skill** — do not touch them.
See `architecture/adr/ADR-0002` for the dividing line.

## Invocation

```
/update-architecture [--repo <name>] [--summary "what changed"]
```

- `--repo <name>` — the sibling repo whose architecture changed (e.g. `mangrove`).
- `--summary "..."` — freeform description of the change, if known in-session.

With no args, do a full reconciliation pass across all modeled repos.

## Ground rules

1. **Structural facts only.** This model owns *what the systems/repos are and how
   they relate*. Narrative (positioning, naming canon, framing) belongs to
   `architecture/estate.yml` — never fold narrative in here.
2. **One-way from estate facts.** You MAY read `architecture/estate.yml` and
   `storyline.md` for framing, but writing never feeds facts back and this model is
   the source of truth, not `estate.yml`.
3. **Ref-free.** Names, roles, dependency edges only — never a commit SHA or
   release tag.
4. **Minimal patches.** Change the fewest lines. Preserve `metadata.designDoc`
   and an implementation's `sourceRepo` / `license` / `language` metadata and
   GitHub `link`. Tags come first in an element body. `#public` is a publication
   decision, not a structural fact: never add or drop it while reconciling a
   repo; leave it to the PR that adds or removes the page citing the element.
5. **Respect the layering.** The model is layered:
   - **Logical (abstract):** technology-agnostic capabilities, concerns
     (governance, lineage, observability), and asset kinds. **NO
     repo/service/infra names** ever appear here. The technology catalog is
     logical too but names specs and software, including our own first-party
     software (`headwaters`).
   - **Deployment (concrete):** configured occurrences. Our repos/services are
     nodes that `instanceOf` their implementation, never a capability (ADR-0008),
     in the authored `trustedCompute` reference scenario; a node whose
     implementation isn't recorded is an instance of nothing. Generated docs environments (`deployment/generated/`,
     `#generated`) come from a pinned Trestle plan: never hand-edit them; change
     `envs/<name>/env.toml` and run `just env-render <name>`.
   Implementation and specification edges are architectural relationships,
   not release-specific proof of support (that is a compat claim).
   A repo change almost always edits the **deployment** layer, not the logical one.
   Only touch logical files if a genuinely new *capability* or *asset kind*
   (not a new service) appears. The zero-trust points (PAP/PDP/PEP/PIP/PA) are
   prose in `design/governance.md`, not elements.
6. **Maturity honesty.** Tag designed-but-not-built elements/edges `#designed`
   (or `#prototype`) when the source repo shows they are unbuilt. Never present
   designed work as built. Do **not** bulk-tag the estate. Incomplete
   realization of something that is built gets `#partial` on the `realizes`
   edge; designed-only topology also lives in `design/governance.md`.

## Phase 1 — Load current truth

- Read the `architecture/model/**/*.likec4` files — the current model (grouped
  under `logical/`, `deployment/`, `views/`, with shared `specification.likec4` +
  `globals.likec4` at the root).
- Optionally read `architecture/dist/model.json` for a resolved view of elements
  and relationships.

## Phase 2 — Gather the change

For the affected repo(s) (from `--repo`, `--summary`, or all in a full pass):

- Read that sibling repo's `README`, `docs/`, and `docs/adr/` (its repo is the
  element's `sourceRepo` metadata).
- Cross-check against `architecture/estate.yml` for coarse facts — but prefer
  the repo's own docs where they're more specific.
- Determine the delta **and which layer it touches**: a new/changed *service or
  deployment* (concrete)? a new *capability or asset kind* (abstract)? a new
  `instanceOf` mapping (which role does a service now play)? a maturity change
  (something moved from designed → built)?

## Phase 3 — Propose the patch

Decide the layer first, then map to the owning file and draft a **minimal** diff:

Files are grouped by layer under `model/`: `logical/`, `deployment/`, `views/`,
with `specification.likec4` + `globals.likec4` shared at the root. (LikeC4
discovers `**/*.likec4` recursively, so location is organization only.)

| Change | Owning file |
|---|---|
| New/changed abstract **capability** | `model/logical/capabilities.likec4` |
| New/changed **concern** | `model/logical/concerns.likec4` |
| What a concern spans (`appliesTo` edge) | `model/logical/concerns.likec4` |
| New/changed **specification** (and its specifies / governs edges) | `model/logical/specifications.likec4` |
| New/changed **implementation** (OSS tech) | `model/logical/implementations/<area>.likec4` (engines and their integrations, table-formats, catalogs, clients, governance-lineage-observability, platform, infrastructure) |
| New/changed **asset kind** (securable), its registeredIn / locatedAt / derivedFrom edges | `model/logical/assets.likec4` |
| Capability-chain edge, or a person's `uses` | `model/logical/relationships.likec4` |
| New/changed **service, datastore, environment**, or `instanceOf` | `model/deployment/deployments.likec4` |
| New element / deploymentNode / relationship kind, or tag | `model/specification.likec4` |
| New logical / deployment / dynamic **view** | `model/views/logical-views.likec4` / `deployment-views.likec4` / `docs-views.likec4` |

- A new **service** goes in `deployments.likec4` as a `service` (or
  `datastore`) node inside the right environment, with `metadata` + `link`
  **then** `instanceOf <implementation>`. Its implementation realizes existing
  logical capabilities — do **not** invent a new logical element for it unless
  it introduces a genuinely new capability.
- A new **capability** goes in the logical layer (tech-agnostic name, and a
  `metadata.designDoc` when a design doc is about it), and is then realized by
  one or more implementations.
- Edges follow ADR-0008: one meaning per kind, no title that restates the
  kind, and a plugin or library that adds a spec's support to an engine is
  `host -[integrates]-> X` with the spec edge on X.

A component that meets a capability or concern only together with another
gets `#partial` on its `realizes` edge (`{ #partial }` in the edge body); never
draw a `realizes` edge an implementation's own release doesn't back (UC OSS has
no fine-grained access). Governance changes go on a facet
(`governance.authentication` / `authorization` / `fineGrainedAccess`), not the
parent.

A Trestle module's `model:` ref always names an **implementation** in the
technology catalog, never a capability or concern; what a Trestle *role*
contributes lives in `architecture/integrations/trestle.yaml`. When the Trestle
pin (`envs/trestle.toml`) moves or a module gains a ref the model lacks, add the
implementation, run `just trestle-catalog`, and fix what `uv run docsnip
trestle` reports: a dangling ref fails `docsnip check`, and a role whose
implementation has no `realizes` / `implements` path to its target is a gap.

If a design doc's scope changed, also propose the `design/*.md` edit and the
`designDoc` metadata that points at it.

**Present the proposed diff and stop for human approval before writing.**

## Phase 4 — Apply + regenerate

After approval:

1. Apply the `.likec4` (and any `design/*.md`) edits.
2. Run `just arch-refresh` (validate → export `dist/model.json` → build). Fix any
   validation errors. Common gotchas:
   - Tags come **first** in an element body; metadata keys are plain identifiers
     (no dots/quotes) — use `designDoc`, `sourceRepo`.
   - Inside a **deployment node**, `metadata`/`link` come **before** `instanceOf`.
   - `view of <el>` and `instanceOf <el>` need the **fully-qualified** logical path
     (e.g. `lakehouse.governance`).
   - Deployment relationships connect deployment nodes/instances — you can't use a
     logical actor (a `person`) as an endpoint there.
3. Run `uv run docsnip check`: it fails on any ADR-0008 rule the edit breaks
   (wrong endpoint kinds, a missing `realizes`, a title that restates its kind,
   an implementation or spec in no `tech*` area view). Add a new
   implementation or spec to the right `tech*` view in
   `views/logical-views.likec4`.
4. Surface the final diff (sources **and** regenerated `dist/`). Remind the human
   to commit them together.

## Validation quick-reference

- `just arch-check` — validate only.
- `just arch-dev` — interactive preview at http://localhost:5173.
- Element identifiers: letters/digits/`-`/`_`, no leading digit, no periods.
- Relationship kinds use `-[kind]->`; plain edges use `->`.
