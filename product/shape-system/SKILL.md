---
name: shape-system
description: "The Shape System — the content_ir kind registry for structured content. Use when adding, activating, or rendering a kind/shape, writing `__kind` JSON, kind schemas or samples, XML-tag/fence detection surfaces, kind components, workflow node input_kind/output_kind, or binding agent output to a kind."
---

# Shape System — how to add to it (and never around it)

**Glossary:** "Shape" = product name; **"kind"** = the technical noun (`content_ir.kind_definition.kind`). One kind = one named, versioned structure that every platform (web, Python, workflow-studio, React Native later) validates and renders against.

**Operating doc (read it):** [`features/content-ir/docs/SHAPE_SYSTEM.md`](../../../features/content-ir/docs/SHAPE_SYSTEM.md) — rulings, posture, roadmap. FEATURE.md invariants: [`features/content-ir/FEATURE.md`](../../../features/content-ir/FEATURE.md).

## The model in three lines

- A Shape carries 7 assets: schema · skill(s) · content block · output component · input component · samples (`kind_example`) · pydantic mirror.
- Every input surface (`__kind` JSON, XML tag, fence, tool result) converges to canonical `__kind` JSON at DETECTION (`kind_surface` is the one list). Below that boundary everything is format-agnostic by construction.
- Consumers: agent outputs, **workflow node I/O (live)**, tool results (Stage 7), custom apps.

## Adding a kind (the paved road)

1. **Schema** — insert the `kind_definition` row (fields in `data[]` for ts-owned; `emitted_json_schema` always; org = system org `39c38960-d30c-4840-b0c1-c9960de95582` for platform kinds, `visibility='public'`). Python-owned kinds derive the schema from the pydantic model: `Model.model_json_schema()` — never hand-write what a model can emit. Idempotent SQL, applied via Supabase MCP, ledgered in `public._schema_migrations`.
2. **Sample** — one `kind_example` row per kind@version (`is_canonical=true`). **Never write `validation_status` yourself** — the `kind_example_recompute_validation` trigger DERIVES it on every write, so a fabricated `passed` is both impossible and a defect. Helper: `pnpm shape:sample <kind> --file|--stdin [--apply]`.
3. **Component** — register the web component. Two tiers, both satisfy the render leg: **compiled** (`kinds/<slug>.ts` → append to `SYSTEM_KIND_DEFINITIONS` → register the block type in `block-dispatch.tsx`'s `SHAPE_BLOCK_DISPATCH`; never add a switch case) or **DB-authored** (a `source='db'` `kind_component` row — no repo change, no deploy; what the creator agent writes). A **bundled** row's `component_key` MUST resolve in `block-dispatch.tsx` — `pnpm check:shapes:components` is a blocking release gate, because a dangling key changes nothing at runtime (the compiled bridge routes anyway) while the registry claims coverage. A kind without either stays inactive and renders the generic viewer (correct, not a failure).
4. **Skill + content block** — one skill per kind per syntax (`kind_<slug>` JSON / `kind_<slug>_xml`); skill bodies teach the REAL parser failure modes. Blocks pair with the skill under the **Agent Skills** category (two per skill: simple + complex), linked via `platform.associations`. Coexist-not-clobber: never overwrite a live legacy block; use a `-kind` suffix during transition.
5. **Surface** — ONLY for a non-JSON arrival form (XML tag / custom fence language). `__kind` JSON needs NO surface: the parser detects it natively in a ```json fence. A row is inert without its `parser_strategy` implemented in `surfaces/xml-finalize.ts#SURFACE_PARSER_STRATEGIES`, so registering one without the parser mints a phantom row (8 such `json_root_key` rows already exist — do not add a ninth). After inserting, run `pnpm check:shapes:surfaces:refresh` — the compiled bootstraps in BOTH repos are generated from `kind_surface`. Never hand-add a tag/fence literal to `stream-block-accumulator.ts` / `content-splitter-v2.ts` / `block_detector.py`.
6. **Activate** — `content_ir.set_kind_activation(id, true)` is the ONE write path for `is_active`; it runs the dual gate (structural leg on the sample + render leg on the component) and raises with the specific missing asset. Surfaces: the owner control on `/shapes/[kind]`, or the `kind_activate` agent tool. **This step is not optional** — an inactive kind renders through the generic viewer and, critically, `isKindBindable` refuses to bind it to an agent's structured output. The admin Gate tab (`/administration/kind-registry/<kind>?tab=gate`) shows the verdict read-only and never writes.
7. **Coverage gates** — a new kind slug or surface token that no crosswalk rule claims FAILS the run. `pnpm check:shapes:crosswalk:refresh`, then `pnpm check:content-ir:strict` (crosswalk + aidream twin + `check:shapes --strict`).

## Workflow node I/O (live)

- `NodeSpec.output_kind` is MANDATORY for non-dynamic nodes (structural kind for stable shapes; generic `json` minimum). `input_kind` gates inputs pre-execute. Per-node authored overrides: `data.input_kind` / `data.output_kind`. Read `packages/matrx-graph/docs/node-authoring.md` §kinds (aidream repo) before adding a node.
- Runtime: `matrx_graph.kinds.get_kind / validate_against_kind` (loud-fail-open). After ANY kind registry mutation call `invalidate_kind_catalog_cache()` (and remember the FE warm registry re-reads on its own cadence).
- LLM binding: `matrx_ai.kinds.response_format_for_kind(slug)` → strict portable response_format. Unknown/unportable kinds decline loudly with `None`.

## Hard rules

- **One registry.** Never a parallel kind list, detector, sample store, or component map. Extending `content_ir` IS the feature.
- **Verify live, never trust reports** — after any DB write, `execute_sql` the counts; after any render change, a runtime marker or screenshot.
- **XML is not legacy — and neither is anything else named "legacy" in this feature.** Every `*-legacy-text.ts`, every `*_legacy_text` strategy key, `legacyBlockType`, and `toLegacyServerData` is LIVE code carrying migration-narrative vocabulary that froze into identifiers. `legacyBlockType` in particular is THE render key — `kind-route.ts` sets `block.type` from it and `block-dispatch.tsx` routes on it; nothing renders without it. Never read the name as permission to delete or "modernize". Rename pending (~100 files + 23 DB rows + an aidream generated file).
- **Render-leg satisfier order is load-bearing.** The compiled-bridge check runs FIRST because it actually exercises the bridge; the resolved `kind_component` row is the last resort. Reversing them short-circuits the "No `<kind>` available" guard for every compiled kind. Pinned by tests — do not reorder.
- **Matrx Directives (MatrxEnvelope) is off-limits** except the collision guard and its `kind_surface` row. Its invariants are listed in SHAPE_SYSTEM.md.
- **`sample_data` on kind_definition is interim** — new samples go to `kind_example`; never add new readers of `sample_data`.
- **DB changes follow the db-change skill** (MCP apply → ledger → `pnpm db-types` → aidream `python db/generate.py` → live verify → both repos commit).

## Definition of done

**The doctor SHIPPED** — `pnpm check:shapes` generates `features/content-ir/docs/SHAPES_STATUS.md` (8 asset columns per kind) and `scripts/shape/shapes-status.json`. Your kind's row is green **and** a preview screenshot exists.

Read the report's `n/a` doctrine before "closing gaps": a `nested_only_child` (renders only inside its parent) and a `data_only` contract kind are STRUCTURALLY exempt from component/skill/block/surface. Those cells are derived, never declared — building assets for them is wasted work, and the doctor will keep marking them n/a.

A fabricated `validation_status='passed'` is a defect; so is an `is_active` flipped by anything other than `set_kind_activation`.
