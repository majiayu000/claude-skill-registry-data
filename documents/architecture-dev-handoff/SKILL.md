---
name: architecture-dev-handoff
description: Generate the four-part Service Handoff Kit from architecture documentation — internally the Ekonte (絵コンテ) kit. Produces a shared System Runtime View (whole-system storyboard with per-hop budget decomposition and edge rationale), shared Cross-Cutting Standards (institution-wide rules synthesized from institutional ADRs), one Interface Contract per adjacent-service pair (continuity contract with mutual assumptions and failure semantics), and one Component Specification per C4 L2 component (intent + constraint only, deliberately not execution). Assets (OpenAPI, AsyncAPI, GraphQL, Avro, DDL, Protobuf, Redis key schema) are generated in parallel per component. Invoke when handing off components for implementation, when a dev team needs implementation specs, or when generating development handoff documents.
triggers:
  - generate handoff
  - create handoff
  - handoff document
  - handoff documents
  - component handoff
  - dev handoff document
  - generate dev handoff
  - create dev handoff
  - handoff for development
  - generate implementation spec
  - create implementation spec
  - implementation handoff
  - prepare component for development
  - generate handoff kit
  - system runtime view
  - interface contracts
  - cross-cutting standards
  - generate ekonte
  - generate ekonte kit
  - system ekonte
  - seam spec
  - cut sheet
---

# Architecture Dev Handoff Skill — Service Handoff Kit Orchestrator

## When This Skill is Invoked

Manually activated when users request component handoff document
generation. It is NOT automatically triggered.

**Activation triggers**:
- "Generate handoff for [component name]"
- "Create development handoff"
- "Hand off [component] to development"
- "Generate implementation spec for [component]"
- "Create dev handoff for all components"
- "Generate handoff documents"
- "Generate handoff kit" (or its internal alias, "Generate Ekonte kit")
- `/skill architecture-dev-handoff`
- `/skill architecture-dev-handoff all`
- `/skill architecture-dev-handoff [component-name]`

**NOT activated for**:
- General architecture documentation tasks (use `architecture-docs` skill)
- Compliance generation (use `architecture-compliance` skill)
- Component index maintenance (use `architecture-component-guardian` skill)

---

## Documentation Language

Resolve the project's documentation language **before writing anything**, using the protocol in
`skills/architecture-docs/references/LANGUAGE_POLICY.md` §3:

```bash
rg -m1 '<!-- DOC_LANGUAGE:' ARCHITECTURE.md || rg -m1 '<!-- LANGUAGE:' ARCHITECTURE.md
```

`DOC_LANGUAGE` → use it. Legacy `LANGUAGE` → use it and rewrite the marker as `DOC_LANGUAGE`.
Neither → infer from headings (§5.5), ask the user to confirm **once**, stamp `DOC_LANGUAGE` into
`ARCHITECTURE.md`, and never infer again. Messages this skill displays to the user stay English
in every case; only authored file content follows `doc_language`.

**In this skill**: the marker is authoritative — Step 3.3's language detection resolves `<!-- DOC_LANGUAGE: -->` first, then the legacy `<!-- LANGUAGE: -->` alias, then heading inference. All four kit documents (`SYSTEM_RUNTIME_VIEW.md`, `CROSS_CUTTING_STANDARDS.md`, interface contracts, component specifications) are authored in `doc_language`, including their `### Role Quick Index` table labels and `handoffs/README.md`. The `handoffs/.manifest.json` keys and values, the `interfaces/<upstream>→<downstream>.md` filenames and their Unicode arrow, every component canonical slug, the asset filenames, and the `TEMPLATE_VERSION` marker stay English. Asset **content** (OpenAPI, DDL, Kubernetes manifests) is code and never localizes; only the `c4-descriptor` has EN/ES scaffolds, which already select on `doc_language`.

Structural headings this skill writes carry their English anchor comment in both languages
(`## Heading <!-- SECTION: English Name -->`). The full do-not-localize registry — codes, status
enum values, table column headers, filenames, marker names, `EXPLORER_HEADER` field keys — is
`LANGUAGE_POLICY.md` §4.

**Document titles by language** — the H1 each generator writes, verbatim:

| Document | `en` | `es` |
|----------|------|------|
| `SYSTEM_RUNTIME_VIEW.md` | System Runtime View — <project> | Vista de Ejecución del Sistema — <project> |
| `CROSS_CUTTING_STANDARDS.md` | Cross-Cutting Standards — <project> | Estándares Transversales — <project> |
| `interfaces/<up>→<down>.md` | Interface Contract: <up> → <down> | Contrato de Interfaz: <up> → <down> |
| `components/NN-<slug>.md` | Component Specification — <component> | Especificación de Componente — <component> |
| `README.md` | Service Handoff Kit — <project> | Kit de Entrega a Desarrollo — <project> |

---

## Naming — the Ekonte kit, delivered under architecture names

The kit is modeled on anime storyboard practice — the *ekonte* (絵コンテ) specifies intent, framing
and timing for every cut, and the whole book goes to every animator — and the plugin keeps that
vocabulary **internally**: the agents (`ekonte-generator`, `settei-generator`, `seam-generator`,
`cutsheet-generator`), the manifest keys (`run.ekonte_hash`, `seams`, `cut_sheets`), the CLI
subcommands (`check-run ekonte`, `update-seam`, `update-cut-sheet`), the payload sections
(`## Budgets (from Runtime View)` is the one exception: payload headings follow the document they
feed) and the trigger aliases. The **documents delivered into the project** carry architecture
names — System Runtime View, Cross-Cutting Standards, Interface Contract, Component Specification —
and so does every user-facing message, report line and export filename. Never write the internal
names into a delivered document.

---

## Architecture — Orchestrator + payloads by code + 4 Generators

This skill produces the **four-part Service Handoff Kit**
(TEMPLATE_VERSION 4.3.1):

1. `handoffs/SYSTEM_RUNTIME_VIEW.md` — shared whole-system storyboard
2. `handoffs/CROSS_CUTTING_STANDARDS.md` — shared institution-wide rules
3. `handoffs/interfaces/<upstream>→<downstream>.md` — one per adjacent-service pair
4. `handoffs/components/NN-<slug>.md` — per component
5. `handoffs/assets/NN-<slug>/*`

**Payloads by code**: `scripts/handoff-prepare.js` writes the three payload shapes
into `.cache/sa-skills/handoff-payloads/` — the run payload, one per-edge payload per edge incident
on the selection, one per-component payload — computes every fingerprint and skip decision
against the manifest, and prints the `CONTEXT_RESULT` block, in under a second and without a
model token. It replaces the `handoff-context-builder` agent, which read 79 files in 134 turns
(61 M cached tokens on the reference project) to route the same text; the agent file stays one
release as the fallback for an environment without `bun`.

Sub-agents:

- `agents/generators/ekonte-generator.md` (sonnet, once per run) —
  writes `SYSTEM_RUNTIME_VIEW.md`.
- `agents/generators/settei-generator.md` (sonnet, once per run) —
  writes `CROSS_CUTTING_STANDARDS.md`.
- `agents/generators/seam-generator.md` (sonnet, once per edge) —
  writes one seam file.
- `agents/generators/cutsheet-generator.md` (sonnet, once per C4 L2
  component) — writes one Component Specification.
- `agents/generators/handoff-asset-generator.md` (sonnet) — writes one
  asset file per invocation. The C4 descriptor is not an agent task: `scripts/c4-descriptor.js` renders it (Phase 4).

**Run the kit in a fresh session.** The orchestrator cannot measure its own context, and every
turn re-reads all of it: on the reference project a handoff started at 500 K tokens of earlier
work cost 37 M cached tokens in the main session alone. `/clear` (or a new session) first.

**Main-context budget**: ~80–120 KB per invocation, flat regardless of
how many components / edges are selected. **Sub-agent budget**:
~25–40 KB per generator spawn (payload + template + extraction guide
slice).

**Concurrency in Phase 5**: one cohort message spawns, in parallel, up
to `1 + 1 + seam_parallelism + parallelism + asset_parallelism` Tasks
(default `1 + 1 + 4 + 4 + 4 = 14`); after it, each lane refills itself as its Tasks return (rolling lanes). See Phase 5 below.

---

## Template Format Preservation Policy

Applies identically to every generator sub-agent. See each generator's
own `PHASE 2 — Fill the template` section for the specific extraction
rules.

**What is preserved is the structure; what is written is the text.** The five rules below are written
not to collide. A template literal that would make them collide is a **template defect** (kit-check
`vocabulary` / `row-label-language`), never something a generator works around.

1. ✅ **PRESERVE the structure exactly** — every heading with its `<!-- SECTION: … -->` anchor, every table's
   shape and its **column headers** (English, on the do-not-localize registry), every `[PLACEHOLDER]`'s
   position, every HTML-comment marker, the fixed sections (§ 8 Deliberately unspecified — non-negotiable;
   § Return Path pointers). No restructuring, no reformatting, no section added or dropped.
2. ✅ **REPLACE every `[PLACEHOLDER]` token** with the payload's value, and never leave one in the output.
3. ✅ **WRITE the visible text in `doc_language`** — headings' visible part, prose, bullets, **row labels**
   (first-column cells of a label/value table are cells, not headers) and table cell contents. The
   templates are English; under `es` every one of those localizes, per `LANGUAGE_POLICY.md`. The machine
   layer never does: codes, ids, status values, column headers, filenames, anchors, marker names.
4. ✅ **NEVER write the internal vocabulary** — *Ekonte, Settei, seam, cut sheet* — into a delivered
   document, in any language (§ Naming). The delivered names are System Runtime View, Cross-Cutting
   Standards, Interface Contract, Component Specification, *interface* for the pair. The templates carry
   none of the internal words on their delivered surface; if one appears in a payload
   sentence you would carry, use the delivered name.
5. ✅ **GAP DETECTION** — write the specific gap marker documented in each template (e.g. `[NOT
   DOCUMENTED — run /sa-analysis:architecture-analysis latency-budget]`) or the generic `[NOT DOCUMENTED —
   add to <file>]` marker, in `doc_language` for its prose part. Never leave a raw `[PLACEHOLDER]`.
6. ❌ **NEVER invent** rules, edges, budgets, ADRs, or invariants absent from the payload.

---

## Strict Source Traceability

Everything in every part of the kit traces to a source. Rules cite
an institutional ADR (`ADR-018`); the kit reads nothing compliance writes. Edges cite an ADR. Budgets cite the Latency Budget
analysis flow / hop. Invariants cite the component responsibility or
ADR that seeded them.

If a source cannot be cited, the value is either dropped (Cross-Cutting Standards rules
without citations) or marked `[NOT DOCUMENTED]` with a concrete
recommendation for how to source it.

---

## Orchestration Workflow

### Step 0 — Resolve plugin directory

Before any workflow, resolve the absolute path to the plugin
installation so sub-agents and the orchestrator can invoke
`bun [plugin_dir]/skills/architecture-dev-handoff/utils/*.ts` helpers.

**Resolve `plugin_dir`** — one call, never a Glob over `~/.claude/plugins/cache/` (it keeps every version ever installed and a glob returns an arbitrary one):

```bash
plugin_dir=$(bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts --plugin sa-delivery)
sa_skills_dir=$(bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts)
```

This skill ships in the **sa-delivery** plugin (`sa-skills` depends on it and installs it). `[plugin_dir]` is sa-delivery's install (this skill's scripts, templates and agents); `[sa_skills_dir]` is sa-skills' — the architecture is read through its facts ledger, explorer, judge and shared scripts, documents render through its `tools/docgen`, and the scripts find it on their own (`scripts/sa-skills.js`: `--sa-skills`, `SA_SKILLS_DIR`, the repo layout, the install registry) and stop with the install command when sa-skills is absent. The script answers from Claude Code's install registry — the project-scope install for this directory, else the user-scope one, else the copy it runs from — and warns on stderr when a newer version is on the machine (`claude plugin update … --scope <scope>`, then `/reload-plugins`); show that warning to the user. Without the marketplace clone (a dev clone alone): Glob `**/{sa-skills,solutions-architect-skills}/.claude-plugin/plugin.json` **outside** `~/.claude/plugins/cache/`, strip `/.claude-plugin/plugin.json` for `sa_skills_dir` and append `/plugins/sa-delivery` for `plugin_dir`.

### Phase 1: Initialization

**Step 1.0 — Parse orchestrator flags**:

| Flag | Default | Validation | Purpose |
|------|--------:|------------|---------|
| `--parallelism N` | 4 | 1–8, clamp | Cut-sheet-generator batch size |
| `--seam-parallelism N` | 4 | 1–8, clamp | Seam-generator batch size |
| `--asset-parallelism N` | 4 | 1–8, clamp | Asset-generator batch size |
| `--force` | false | boolean | Bypass all skip-if-unchanged checks |

Store as `parallelism`, `seam_parallelism`, `asset_parallelism`, `force`.

**Step 1.1 — Locate ARCHITECTURE.md**: current directory → parent → `/docs` subdirectory → ask user. Extract project name (first H1), architect metadata, and `<!-- ARCHITECTURE_VERSION: X.Y.Z -->`.

**Step 1.2 — Validate prerequisites**:
- `ARCHITECTURE.md` exists.
- `docs/components/` exists with at least one `NN-*.md`.
- `docs/components/README.md` exists (required for multi-system; recommended for single-system — if absent, suggest running architecture-component-guardian).
- The contract validator is installed: `bun [plugin_dir]/skills/architecture-dev-handoff/scripts/contract-check.js --probe`. Exit 1 means `@redocly/openapi-core`, `graphql`, `avsc`, `libpg-query`, `node-sql-parser` or `protobufjs` is missing — stop and print its message (`bun install` in `[plugin_dir]`); every OpenAPI, AsyncAPI, GraphQL, Avro, DDL and Protobuf asset would otherwise fail the Step 5.2b gate after the run had spent its tokens.

- The identifiers the assets will copy are English: `bun [sa_skills_dir]/scripts/shared/identifier-check.js <project_root> --file docs/05-integration-points.md --file <each selected component's file>`. Every path, field, schema, enum value, topic, table and key prefix goes into the assets verbatim, so a Spanish one there becomes a Spanish contract. On `PENDING` the session is the judge: answer the worksheet the note names (one `1` / `0` per item — is this identifier Spanish?) into the answers file it names, then re-run with `--answers`; under `SA_JUDGE=typesafe` Jev answers and nothing is pending. A finding is a WARNING: print it in the Phase 7 report under *Identifiers not in English* and continue — the fix is an edit of the docs (architecture-docs Workflow 2), never a translation in the asset.

**Step 1.3 — Load component facts**: run

```bash
bun [sa_skills_dir]/scripts/shared/component-facts.ts list <project_root>
```

Keep the entries with `level: L2` — the CLI already applies the filename heuristic and the
`**C4 Level:**` metadata, and reports a `level-conflict` warning when the two disagree. Use `name`
as the canonical component name and `index` for ordering. Present the component list. If the
command is unavailable, fall back to reading `docs/components/README.md` and filtering by hand.

### Phase 2: Component Selection

**Step 2.1 — Ask user which components** (unless the user pre-named them). Selection modes: `all`, number by index, component name, comma-separated list. Apply the C4 Level Validation Gate to reject non-L2 selections.

**By delivery increment** ("handoff for increment 2", or a project whose `docs/01` declares `Delivery Increments`): the selection is code's — `bun [sa_skills_dir]/scripts/shared/increments.js <project_root> --increment <id> --slugs` prints the increment's containers (`--new` only the ones it adds to the increment before). Offer both and pass the answer as `--components`; never pick the containers by reading the flows.

**Step 2.2 — Order selected components** by `component_index_position` ascending.

### Phase 3: Build the payloads by code

**Step 3.1 — Detect architecture-doc language** (marker first):
`<!-- DOC_LANGUAGE: es -->` / `<!-- DOC_LANGUAGE: en -->` in `ARCHITECTURE.md` (authoritative), else the legacy `<!-- LANGUAGE: xx -->` alias — adopt it and rewrite the marker as `DOC_LANGUAGE` — else Spanish section-heading inference on `docs/01-system-overview.md` confirmed once by the user and then stamped, else default `en`. Full protocol: `skills/architecture-docs/references/LANGUAGE_POLICY.md` §3.

**Step 3.2 — Pre-cache context7 spec docs (optional, orchestrator-side)**: if context7 MCP tool is available and any selected component produces asset types, call `resolve-library-id` once per unique asset spec and cache the resolved library IDs. Pass the cache path hint to asset-generator Tasks in Phase 5. Skip silently if context7 unavailable.

**Step 3.3 — Capture `generation_date` and prepare payload dir**:

```bash
generation_date=$(bun [plugin_dir]/skills/architecture-dev-handoff/utils/prepare-payload-dir.ts .cache/sa-skills/handoff-payloads)
```

**Step 3.4 — Run the payload builder** (one Bash call, no sub-agent):

```bash
bun [plugin_dir]/skills/architecture-dev-handoff/scripts/handoff-prepare.js <project_root> \
    --components <slug,slug,…|all> --date <generation_date> [--force]
```

It reads the facts ledger, docs/04, docs/05, the descriptors of the selected components and of
every edge endpoint, the latest `analysis/LATENCY_BUDGET-*`, `BLAST_RADIUS-*` (or `BLAST-RADIUS-*`)
and `COUPLING-*`, and every institutional ADR — never a compliance contract — and writes `.cache/sa-skills/handoff-payloads/_run.md`, `seams/<up>→<down>.md` for every
docs/05 edge incident on the selection whose two endpoints are documented components,
`<slug>.md` per selected component, and `context-result.json`. Every payload section is verbatim
or a rule (PAYLOAD_SCHEMA.md); absent sources render as `[NOT DOCUMENTED — …]` with the command
that produces them. It hashes every payload and decides SKIP / REGEN against
`handoffs/.manifest.json` with the same module `manifest-cli.ts` runs; `--force` is honoured. The hash leaves out the
payload's stamps — architecture version, generation date, checkout path — so a release that did not touch a part keeps
it: the script moves its Architecture Version row and its manifest entry by code (`Kept, … restamped` on stderr). Never
`--force` a release: the model would rewrite every part in other words, and the kit's diff would hide the release's.

**Edit mode** (10.9.0, `scripts/kit-edit.js`): a REGEN part that exists and whose payload hash moved is not rewritten.
The script cuts its payload again from the tree of the release the part was written at (`architecture-v<version>` from
the manifest, same plugin, same judge answers) and compares the two without their stamps. Equal, the part is kept
(`Kept — the payload re-cut from their release is the same`): a manifest hashed in an older form costs no
regeneration. Different, the part carries `edit_path` — the delta and a copy of the previous text under
`.cache/sa-skills/handoff-payloads/edit/` — and its generator edits only what the delta reaches. No tag, no previous
file, a template change or a delta over half the payload: written whole, no `edit_path`.
Template version `4.3.1` and schema version `4` are its defaults — pass `--template-version` /
`--schema-version` only to override.

**stdout** is the `CONTEXT_RESULT:` block (YAML; `--json` for the object). **stderr** is the
review: the sizes and counts, the active edges and the endpoints that are not documented
components (the edge stays in the run payload, no seam is written), the Compliant rule counts per
domain, the decisions, the prerequisite warnings, and the edge cross-check — a docs/05 edge the
endpoint's Outbound / Inbound table does not name, a fan-out row the blast-radius analysis does
not list. Read both; never open the payloads.

Handle statuses:
- `FAILED` (exit 1) — abort orchestration (`docs/05-integration-points.md` missing or without `I-nn` rows).
- `OK` — every part has a SKIP or REGEN decision; a component that is not a C4 L2 descriptor is
  dropped with a warning (`component skipped — <slug>: …`), never failed.

Store the `run`, `seams`, `cut_sheets` blocks as `context_result`, and `warnings[]`,
`edge_cross_check_warnings[]`, `unresolved_endpoints[]`, `undecided_endpoints[]`, `endpoint_review[]` for Phase 7.

**Endpoint resolution is a judgement, not a substring test.** Which documented component a
docs/05 From / To cell names goes through `scripts/resolve-name.js` on the plugin's one judge
(`scripts/judge.js`): containment only finds the candidates. The default engine, `agent`, writes a
worksheet (`--judge-answers` / `--judge-also-answers`, or answers written beside it, close the loop
on a re-run); `--judge typesafe` asks Jev. A cell that is exactly one component's name is answered
by code and never judged. A cell no judge has answered is **undecided**: never resolved by
containment, no seam for its edge, listed in `undecided_endpoints[]` with the worksheet — dispatch the `sa-skills:reviewers:worksheet-judge` subagent (Haiku) once per worksheet
and re-run before Phase 4 (`unresolved_endpoints[]` is a cell the judge read as no documented component). What the
judge adds is visible, never silent: `endpoint_review[]` names every second component a cell also
names ("Aplicación Tienda Móvil y Base Local de Pedidos" — the contract is written for the
first, the second is reported) and every pick below the confident band; a cell with no documented
name in it resolves only at high confidence. `--verify <fixtures.json>` measures the resolutions
against `[{ "id": "I-06:to", "label": "<canonical name>" | "none", "also": [...] }]` before any
engine is trusted. Never offer the `typesafe` engine unprompted: the cells leave the machine.

### Phase 3.6: legacy layout detection (silent auto-regen + cleanup)

After Step 3.4, sweep `handoffs/` for the two older layouts. Every queued entry is a pair `{ legacy: <path>, counterpart: <path the 4.0.0 kit writes instead> }`:

1. **v2 per-component handoffs**: `Glob <project>/handoffs/*-handoff.md`. For each match, `Read` the first ~10 lines. If any `<!-- TEMPLATE_VERSION: 2.` marker is present:
   - Derive the slug from the filename (`NN-<slug>-handoff.md` → `<slug>`).
   - Force the matching `context_result.cut_sheets[<slug>].decision` to `REGEN`. If no matching Component Specification entry exists (e.g. component was removed from the index but the legacy handoff was never cleaned up), skip the flip but queue the file for deletion.
   - Queue it with counterpart `handoffs/components/NN-<slug>.md`.

2. **v3 kit (3.x, the Ekonte-named layout)**: `Glob` `handoffs/SYSTEM_EKONTE.md`, `handoffs/SETTEI.md`, `handoffs/seams/*.md`, `handoffs/cut-sheets/*.md`. Queue each match with its counterpart — `SYSTEM_RUNTIME_VIEW.md`, `CROSS_CUTTING_STANDARDS.md`, `interfaces/<same filename>`, `components/<same filename>`. No decision flip is needed: `manifest-cli.ts` migrates a v3 manifest on load by rewriting its file paths to the 4.0.0 layout and marking every entry stale, so the context-builder already returned `REGEN` for every part.

3. **Emit one summary line per layout found** (only if the queue is non-empty):
   ```
   Detected N v2 handoff(s) → migrating to the 4.0.0 kit (legacy files are removed once their Component Specification is written)
   Detected a 3.x kit (Ekonte-named files) → migrating to the 4.0.0 layout (SYSTEM_RUNTIME_VIEW.md, CROSS_CUTTING_STANDARDS.md, interfaces/, components/); legacy files are removed once their counterpart is written
   ```

Deletion happens in Phase 6 after the counterpart is written. Legacy files whose counterpart fails to generate stay on disk and are surfaced in Phase 7.

### Phase 4: Pre-create output directories

Ensure the 4.0.0 directory layout exists:

```bash
bun [sa_skills_dir]/scripts/ensure-dir.ts <project>/handoffs/interfaces
bun [sa_skills_dir]/scripts/ensure-dir.ts <project>/handoffs/components
```

For each REGEN Component Specification, pre-create its asset directory:

```bash
bun [sa_skills_dir]/scripts/ensure-dir.ts <project>/handoffs/assets/NN-<slug>
```

SKIP'd components keep their existing asset directories untouched. FAILED entries are excluded.

**Render the C4 descriptors by code**, one Bash call for every REGEN Component Specification:

```bash
bun [plugin_dir]/skills/architecture-dev-handoff/scripts/c4-descriptor.js <project_root> --components <slug,slug,…> --write
```

It writes `handoffs/assets/NN-<slug>/c4-descriptor.md` — one table of operational facts and a link to the
Component Specification — and `.cache/sa-skills/handoff-payloads/asset-gaps/<slug>.c4-descriptor.json` with its
gaps, merged at Step 5.3. Every value comes from the facts ledger or a metadata row of the component file; a value
with no structured source is `[NOT DOCUMENTED — …]` naming the row to add. `c4-descriptor` is therefore never part
of the Phase 5 asset fan-out.

**Render the security obligations by code**, one Bash call for **every** component of the kit — REGEN and SKIP alike,
since they read the STRIDE and Data Sensitivity reports and `docs/07`, which change without the specification:

```bash
bun [plugin_dir]/skills/architecture-dev-handoff/scripts/security-obligations.js <project_root> --components <slug,slug,…> --write
```

It writes `handoffs/assets/NN-<slug>/security.md` — who may call the component (every docs/05 row into it; any
other caller is rejected), how each interface authenticates (the STRIDE trust-boundary inventory, per `I-nn`), the
Security by Design principle verbatim, the institutional ADRs the security section cites, the STRIDE findings of
its boundaries with their mitigations, the Data Sensitivity flows it sends or receives, and the security tests the
build must pass — and `asset-gaps/<slug>.security.json`. **An inbound interface whose authentication is not
documented fails closed**: the file says so, and the build pack's instructions forbid shipping it open. A missing
STRIDE or Data Sensitivity report is a gap naming the lens to run. `kit-check.js` fails a Component Specification
without its `security.md` (`security-missing`), so no build pack is cut from a kit that lacks one.

### Phase 5: Parallel fan-out — 4 generator lanes + assets, rolling

One cohort message spawns, in parallel:

- **1 × ekonte-generator** if `context_result.run.ekonte_decision == REGEN`
- **1 × settei-generator** if `context_result.run.settei_decision == REGEN`
- **Up to `seam_parallelism` seam-generator Tasks** — one per `context_result.seams[]` entry with `decision == REGEN`, ordered by `edge_key`
- **Up to `parallelism` cutsheet-generator Tasks** — one per `context_result.cut_sheets[]` entry with `decision == REGEN`, ordered by `component_index_position`
- **Up to `asset_parallelism` handoff-asset-generator Tasks** — one per `(cut_sheet, asset_type)` tuple derived from the REGEN Component Specifications' `asset_types[]`, **`c4-descriptor` excluded** (rendered in Phase 4)

**Rolling lanes**: each lane keeps up to its own cap in flight — seams `seam_parallelism`, Component
Specifications `parallelism`, assets `asset_parallelism` — and **the moment one of its Tasks returns, the next queued
item of that lane is spawned** (one Agent call, in the same message as whatever else that result triggers), without
waiting for the other lanes or the rest of the cohort. A lane with nothing queued spawns nothing. At any instant, total
in-flight sub-agents ≤ `1 + 1 + parallelism + seam_parallelism + asset_parallelism`.

#### Step 5.1 — Spawn the cohort

Each Task carries its own prompt body (see each generator's SKILL for the exact fields):

- **ekonte** / **settei**: `run_payload_path` (from `context_result.run.ekonte_payload_path`), `output_ekonte_path` / `output_settei_path`, `ekonte_version` / `settei_version` (both `4.3.1` on this rollout).
- **seam**: `seam_payload_path`, `output_seam_path`, `edge_key`, `ekonte_version`, `settei_version`.
- **cut-sheet**: `cut_sheet_payload_path`, `output_cut_sheet_path`, `component_slug`, `component_index_position`, `asset_types`, `ekonte_version`, `settei_version`.
- **asset**: `payload_path` (the per-component cut-sheet payload), `asset_type`, `output_asset_path`, `component_slug`, `doc_language`, optional `context7_cache_hint`. Set `model: sonnet`.
- **Edit mode**: a part with `edit_path` (`run.ekonte_edit_path`, `run.settei_edit_path`, a seam's or a component's `edit_path`) passes it in its prompt; each asset of a component in edit mode passes the component's `edit_path`.

#### Step 5.2 — Collect results from all lanes

Each generator returns one of the following blocks:

- `EKONTE_RESULT: { status, ekonte_file, flows_count, edges_count, gaps_count, validation_notes }`
- `SETTEI_RESULT: { status, settei_file, rules_count, citations_count, gaps[], validation_notes }`
- `SEAM_RESULT: { status, edge_key, seam_file, related_adrs[], gaps_count, validation_notes }`
- `CUT_SHEET_RESULT: { component_slug, status, cut_sheet_file, not_documented_count, sections_with_gaps, invariants_count, validation_notes }`
- `ASSET_RESULT: { component_slug, asset_type, status, asset_path, gaps[], validation_notes }`

Aggregate everything for Phase 6 (manifest updates) and Phase 7 (report). Do NOT abort on any single failure — continue collecting.

**Orphaned assets**: asset Tasks spawn eagerly, so a component whose Component Specification fails to generate may still have asset files on disk. Phase 6 excludes them from the manifest; Phase 7 lists them so the next run regenerates.

#### Step 5.2a — Edit mode: only the sections the delta reached (by code)

For each part written in edit mode, one Bash call each, before the gate:

```bash
bun [plugin_dir]/skills/architecture-dev-handoff/scripts/kit-edit.js check <part.md> \
    --previous <edit_path without .md>.previous.md --sections "<edited_sections>" --restore
```

It compares the part with its previous text section by section (`<!-- SECTION: … -->`; dates and the Architecture
Version row masked) and puts back the previous text of every section that changed without being declared, printing
`not declared: … (restored: …)`. Exit 1 is a section added or removed without being declared: treat the part as
`VALIDATION_FAILED` and re-spawn it once with the line quoted. List what it restored in the Phase 7 report.

#### Step 5.2b — The diagram gate over the written kit

Run, in one Bash call, over the kit written this run:

```bash
bun [plugin_dir]/skills/architecture-dev-handoff/scripts/kit-check.js handoffs --fix
```

`--fix` rewrites a row label left in English, or the registered one up to case / accents / spacing, to its
`ROW_LABELS.json` value before the check, and an Interface Contract's H1 and every endpoint slug in its visible
text to the canonical names its payload carries (`title-names`, `component-slug`; code spans, links and file
names keep the slug), and prints `fixed N row label(s), M name(s)` per file — never translate a
row label by hand and never re-dispatch a part for one. A free translation (`tiempo de espera agotado` for `timeout`)
stays a `row-label-unregistered` finding: edit that cell to the label the finding names.

Per file it checks the H1 and the managed / `TEMPLATE_VERSION` markers, a template placeholder
left outside an HTML comment (`[UPSTREAM_COMPONENT]`, `[N]ms`, `[FLOW_PANELS …]` — `[NOT
DOCUMENTED — …]` is the gap marker, never a placeholder), an authoring-rule comment carried into
a deliverable, a `<!-- SECTION: … -->` anchor on every H2 and on the `Role Quick Index`, **no internal
name on the delivered surface** (`vocabulary` — seam / ekonte / settei / cut sheet, comments and fences
exempt), **every row label the registered one** (`row-label-language` / `row-label-unregistered` — each label table
of the four templates, read at run time, against `ROW_LABELS.json`, the closed EN↔ES list every payload carries as
`## Row Labels`; technical terms such as `timeout`, `poison message`, `upstream` and `Error budget` stay English and
are registered as themselves; `--lang` overrides the `DOC_LANGUAGE` marker), **an
Interface Contract's Interaction label row held to its seam payload** (`interaction-label-missing` / `-drift` /
`-ungoverned` — under `design_language: governed` the row carries `interaction_label` verbatim, under `fallback` it is
absent; the mode is the payload's, never the orchestrator's: the standard ships in the plugin, not the project), a
phase drawn once, and every ```mermaid fence through
`mermaid-check.js` (the phase panels and each flow's main image are cut by `handoff-prepare.js` and carried verbatim — a fence that
fails was edited by a generator), **every Architecture Version row the architecture's** (`version-stale` — the
`ARCHITECTURE_VERSION` marker of the project's `ARCHITECTURE.md`: payloads cut before a release write the old version,
so cut them after it), and **every interface of a component in § 2 of its specification** (`interface-missing` — each
`I-nn` its `security.md` lists is named in § 2 Position, or by an Interface Contract § 2 links; an `I-nn` whose other end
is no component has no contract and is listed under *Interfaces without an Interface Contract*, from the payload). A file that fails names the line and the rule: treat that part as
`VALIDATION_FAILED` (it is not written to the manifest) and re-spawn it once with the finding
quoted; the payload is the reference.

**Every `assets/*/openapi.yaml`, `asyncapi.yaml`, `schema.graphql`, `*.avsc`, `ddl.sql`, `schema.proto` and `redis-key-schema.md` passes `scripts/contract-check.js` in the same call**:
the YAML parses; the structure holds (every map a mapping — a key holding only comments is YAML null —, no
scaffold placeholder in a value; OpenAPI: responses with descriptions, every `{param}` declared `in: path`,
unique `operationId`s; AsyncAPI: `action` `send` / `receive`, `channel` a `$ref`); the contract is the
documented one — an operation whose method and path, or a channel whose address, the component's cut-sheet
payload never states is `operation-undocumented` / `channel-undocumented` (the no-invention rule); and
Redocly validates it against the OpenAPI 3.1 / AsyncAPI 3.0 schema in-process (`@redocly/openapi-core`, a
dependency of the plugin; the project's `redocly.yaml` if present, else `recommended`). Spec conformance
blocks — `struct` (3.0's `nullable` in an OpenAPI 3.1 file, an AsyncAPI 2.x security requirement in a 3.0
file), unresolved refs, path parameters — and every other rule warns, since a missing auth or server URL
is a gap to record, not a value to invent. A `schema.graphql` is built and validated by graphql-js (also a
dependency); every root field must be named in the payload, a comments-only schema warns, and breaking or
dangerous changes against the previous version (the file at git HEAD) are reported as warnings — a
regenerated contract that breaks its consumers says so here. An Avro schema (`<RecordName>.avsc`, one record per
file) must be plain JSON, build in `avsc` (also a dependency), give every `decimal` a `precision`, and name only
fields the architecture docs name — the producer's descriptor, docs/05 and docs/04 count, since a consumer
repeats the producer's message. A `ddl.sql` is written for a relational store only (the payload's `sql_engine`) in
that engine's dialect and checked by its grammar — PostgreSQL by `libpg-query`, MySQL / MariaDB / SQL Server / DB2 /
SQLite / Snowflake / Redshift / BigQuery by `node-sql-parser`, Oracle by none (the receipt says so) — and every table and
column must be named in the architecture docs. A `schema.proto` (one per component; a gRPC service's `service` and
`rpc`s in it, since it gets no `openapi.yaml`) is parsed and resolved by `protobufjs` (also a dependency), its enums
start at 0, its field numbers avoid 0 and 19000–19999, every service, rpc, message and field is named in the docs,
and a field number changed or reused against the version at git HEAD is reported as a breaking change — the
generator keeps the numbers of the file it regenerates. A `redis-key-schema.md` is three tables with fixed headers
(Keys, Settings, On Redis failure) and nothing else; its vocabularies are closed and every key prefix, TTL, size and
writer is stated in the docs, a quantity matching in any unit (`300s` = "5 minutes"). A failing asset is
`VALIDATION_FAILED` like any other part.

**The kit inherits what `docs/04` disagrees about.** Before a run, `bun [sa_skills_dir]/scripts/shared/flow-check.js <project_root>` says whether each flow's phase list and its complete sequence agree. They are the two things the Runtime View puts side by side — the phase panels under each flow, the sequence linked from it — so a `phase-absent` finding becomes a kit that draws a phase the flow's own sequence never runs. Report the findings with the kit; fixing them is `/sa-skills:architecture-docs` — generate my architecture diagrams, not this skill.

**The anchor rule is what makes the language contract checkable.** Each generator localizes visible
headings and emits the template's English anchor beside each one. The checks match the anchor, not the
visible text, so a heading without its anchor is a defect in either language.

**The panel rule is one heading per phase.** A flow's block ends with its **main image** — the end-to-end sequence `flow-compose.js` derived in `docs/04` from the phases the flow declares, every step labelled `N.M` (phase N, step M of that phase's panel) — and every phase is drawn **once**, in `§ Phase Catalog`, with a `Used by:` line naming the flows that declare it. A second `### Phase N` is a finding, identical or not. A reader follows `4.2` in any main image to step 2 of Phase 4 in the catalog, and reads `Used by` to know what a change to that phase reaches.

#### Step 5.2c — The kit against itself and against the kit before it (judge)

Once Step 5.2b passes, run both in one Bash call, **before the regenerated kit is committed** (the drift base is git HEAD):

```bash
bun [plugin_dir]/skills/architecture-dev-handoff/scripts/kit-coherence.js <project_root>
bun [plugin_dir]/skills/architecture-dev-handoff/scripts/kit-drift.js <project_root>
```

- **`kit-coherence.js`** — who owns what, said three times: each Interface Contract's Ownership table against its Exit
  state and the § 6 Data ownership of both Component Specifications, one judge question per contract.
  `ownership-mismatch` at p ≥ 0.85 blocks; 0.5–0.85 warns.
- **`kit-drift.js`** — what this run dropped or re-decided against the committed kit:
  - **Blocking `regression`:** an OpenAPI / AsyncAPI operation or `operationId` the docs still name is gone or renamed, or
    `info.version` moved to a value the docs do not state.
  - **Warning:** a rename or removal of a name the docs never stated (pin it there; `contract-check.js` warns
    `operation-id-undocumented` / `version-undocumented` on the same names), or a § 4 invariant the judge says the new
    list no longer states (`invariant-dropped`).
  - No git or no committed kit: `SKIPPED`.

**A pending worksheet**: dispatch `sa-skills:reviewers:worksheet-judge` on each worksheet the scripts name (one per worksheet, in
one message), then re-run the same commands — the answers beside the worksheet are applied.

**Settling the findings:**
- A blocking finding is settled at its source, never by editing the part:
  - **Ownership:** the narrower source (usually a docs/05 block) is fixed in the architecture and the part re-spawned with
    the finding quoted.
  - **Regression:** the part is re-spawned with the documented name or version quoted, or the architecture states the
    new one.
- **`invariant-dropped`** is either restored (the specification re-spawned with the rule quoted) or confirmed against the
  docs as removed by the architecture, and listed in the Phase 7 report.

#### Step 5.3 — Asset-gap merge into Component Specification § 11 (by code)

The C4 descriptor's and the security obligations' gaps are already on disk (`asset-gaps/<slug>.c4-descriptor.json`,
`asset-gaps/<slug>.security.json`, Phase 4): run the merge below with each file — the descriptor's for every REGEN
component, the security file's for every component of the kit. For each Component Specification with an asset regenerated this
run, write its gaps once to `.cache/sa-skills/handoff-payloads/asset-gaps/<slug>.json` as
`{ "assets": ["<every asset filename regenerated this run>"], "gaps": [{ "asset": "<asset filename>", "field": "<what is missing>", "where": "<recommended location>", "impact": "<what it blocks>" }] }`
(one `Write`, the fields mapped from `ASSET_RESULT.gaps[]`; `assets` lists an asset that came back with no gap too, so
its old rows clear), then run:

```bash
bun [plugin_dir]/skills/architecture-dev-handoff/scripts/kit-gaps-merge.js handoffs/components/NN-<slug>.md \
    .cache/sa-skills/handoff-payloads/asset-gaps/<slug>.json
```

It finds `## … <!-- SECTION: Open Questions -->`, appends one row per gap to the four-column register
(`Section` = `Assets — <filename>`, then field · where · impact), creates the table in place of the
"No gaps detected" line when § 11 had none, never adds a row already present, **removes the rows of a
regenerated asset that its new gaps no longer carry** (a regenerated asset's register is replaced, never
accumulated; other assets' rows and the specification's own stay), and prints how many rows it added and removed.
Never edit § 11 by hand to drop a stale row. It refuses a file with no § 11 anchor (the Component Specification failed validation — log for
Phase 7). Column headers stay English; the cells are in `doc_language` as the asset generator wrote them.

Component Specifications whose `CUT_SHEET_RESULT.status != OK` are skipped here — their orphaned assets
are surfaced separately in Phase 7.

#### Step 5.3b — Technical debt into § 7 (by code)

One Bash call, for **every** component of the kit, REGEN and SKIP alike:

```bash
bun [plugin_dir]/skills/architecture-dev-handoff/scripts/kit-debt.js <project_root>
```

It writes `### Technical debt <!-- LABEL: Technical Debt -->` at the end of each specification's § 7 Constraints. The
table has one row per TDR the descriptor's `**Technical Debt:**` line names (the facts ledger's `tdrs`): the id linked to
its record, the title and the status. It replaces the table on every run and removes it when the descriptor names
none. The line stays out of the payload (`handoff-prepare.js`), so a release that only records debt keeps the
specification and moves only this table. Never write debt into a specification by hand.

### Phase 6: Update manifest, index, and legacy cleanup

**Step 6.0 — Update the v4 manifest**

For each successful part, call the appropriate `manifest-cli.ts update-*` subcommand. Cache `template_version` once (`4.3.1`) and `generator_version` once (`.claude-plugin/plugin.json` version).

- **Run parts** (Runtime View + Cross-Cutting Standards, both status OK):
  ```bash
  bun [plugin_dir]/skills/architecture-dev-handoff/utils/manifest-cli.ts \
      update-run <manifest_path> ekonte <ekonte_payload_hash> 4.3.1 4 <arch_version> <generator_version>
  bun [plugin_dir]/skills/architecture-dev-handoff/utils/manifest-cli.ts \
      update-run <manifest_path> settei <settei_payload_hash> 4.3.1 4 <arch_version> <generator_version>
  ```

- **Seams** (each with SEAM_RESULT.status == OK):
  ```bash
  bun [...]/manifest-cli.ts update-seam <manifest_path> <edge_key> <payload_hash> 4.3.1 4 interfaces/<edge_key>.md <generator_version> "<ADR-018,ADR-023>"
  ```

- **Cut sheets** (each with CUT_SHEET_RESULT.status == OK):
  ```bash
  bun [...]/manifest-cli.ts update-cut-sheet <manifest_path> <slug> <payload_hash> 4.3.1 4 <arch_version> components/NN-<slug>.md <doc_language> <generator_version> "<asset1,asset2,...>"
  ```
  Filter `<asset1,asset2,...>` to assets whose `ASSET_RESULT.status == OK`, plus `c4-descriptor.md` and `security.md`, which code renders (Phase 4). Orphaned assets are excluded — the next run regenerates them.

Failed parts (`VALIDATION_FAILED` / `PAYLOAD_FAILED` / `FAILED`) are NOT written to the manifest, so the next run treats them as needing regen.

**Step 6.1 — Legacy cleanup (v2 handoffs and the 3.x layout)**

For each `{ legacy, counterpart }` in `legacy_cleanup_queue` from Phase 3.6:
- If `counterpart` exists on disk: delete `legacy` via `rm`.
- Else: leave the legacy file, log for Phase 7 as `Legacy retained: <file> — counterpart regen failed`.

When `handoffs/seams/` or `handoffs/cut-sheets/` is left empty, remove the directory (`rmdir`). `rm` is used (not moved to a trash dir) because the migration is silent and reversible via git.

**Step 6.2 — Regenerate `handoffs/README.md`** (by code):

```bash
bun [plugin_dir]/skills/architecture-dev-handoff/scripts/kit-readme.js <project_root>
```

It reads the manifest just updated, the facts ledger and the payload builder's
`context-result.json`, and writes the managed index in the document language — never compose
it by hand. Format, for reference:

```
Line 1: <!-- managed by sa-skills:architecture-dev-handoff — do not edit manually -->
Line 2: [Architecture](../ARCHITECTURE.md) > Development Handoffs
Line 3: (blank)
Line 4: # Service Handoff Kit — <project>
Line 5: (blank)
Line 6: Four-part handoff kit. Read the shared documents alongside your Component Specification.
Line 7: (blank)
Line 8: ## Shared documents
Line 9: (blank)
Line 10: | Document | Generated |
Line 11: |----------|-----------|
Line 12: | [SYSTEM_RUNTIME_VIEW.md](SYSTEM_RUNTIME_VIEW.md) | YYYY-MM-DD |
Line 13: | [CROSS_CUTTING_STANDARDS.md](CROSS_CUTTING_STANDARDS.md) | YYYY-MM-DD |
Line 14: (blank)
Line 15: ## Quick reference — reading order by role
Line 16: (blank)
Line 17: | If you're... | Read in this order |
Line 18: |--------------|--------------------|
Line 19: | **Dev** (building `<component>`) | 1) your Component Specification §§ 1–4, 7, 8 · 2) each Interface Contract listed in Component Specification § 2 · 3) Cross-Cutting Standards § Error semantics, Idempotency, Resilience defaults · 4) System Runtime View § Flows for the flows in Component Specification § 2 |
Line 20: | **QA** (testing `<component>`) | 1) your Component Specification §§ 3, 4, 5, 9 · 2) each Interface Contract § Failure semantics + Entry/Exit state · 3) Cross-Cutting Standards § Idempotency, Observability · 4) `assets/NN-<slug>/openapi.yaml` (or the equivalent contract asset) |
Line 21: | **Ops / SRE** (deploying + running `<component>`) | 1) System Runtime View § Budget Decomposition + § Failure Posture · 2) each Interface Contract § Failure semantics + § Observability · 3) Cross-Cutting Standards § Observability conventions, Resilience defaults, Data · 4) your Component Specification §§ 5, 7, 10 (Assets) |
Line 22: | **Architect** (validating the kit) | 1) System Runtime View (whole) · 2) Cross-Cutting Standards (rule inventory + Deviations table) · 3) every Interface Contract (continuity check) · 4) `handoffs/.manifest.json` for what regenerated this run |
Line 23: (blank)
Line 24: ## Interface contracts
Line 16: (blank)
Line 17: | # | Edge | Interface Contract | Related ADRs | Generated |
Line 18: |--:|------|-----------|--------------|-----------|
...
Line M: ## Component Specifications
Line M+1: (blank)
Line M+2: | # | Component | Component Specification | Status | Assets | Generated |
Line M+3: |---|-----------|-----------|--------|--------|-----------|
...
Line N: ## Related Documentation
```

Statuses (`Ready` / `Outdated`) match v2 semantics: `Outdated` when the source component file's mtime is newer than the Component Specification's mtime. Interface contracts do not carry a `Status` column because they are always regenerated from the shared corpus.

**Step 6.3 — Update ARCHITECTURE.md navigation**

If `ARCHITECTURE.md` does not already link to `handoffs/README.md`, add one under the Component Details section or at the end of the navigation table.

### Phase 7: Report

Print the aggregated report:

```
handoff kit — generation complete

Location: handoffs/

Shared documents:
  ✓ SYSTEM_RUNTIME_VIEW.md — [flows_count] flows, [edges_count] edges, [gaps_count] gaps
  ✓ CROSS_CUTTING_STANDARDS.md — [rules_count] rules, [citations_count] citations
  or ✎ edited: [edited_sections][ · restored: …]
  or ⏭ skipped (unchanged since last generation)

Interface contracts: [N] regenerated, [E] edited, [M] skipped, [K] failed
  ✓ [edge_key] — related ADRs: ADR-018
  ✎ [edge_key] — edited: [edited_sections][ · restored: …]
  ⏭ [edge_key] — skipped
  ✗ [edge_key] — VALIDATION_FAILED: [notes]

Component Specifications: [N] regenerated, [E] edited ([K] failed, [S] skipped)
  ✓ [component-slug] — components/NN-<slug>.md
  ✎ [component-slug] — edited: [edited_sections][ · restored: …] · assets edited: [names or none]
      Assets: openapi.yaml, ddl.sql
      Gaps recorded: [M] open questions in § 11
      Technical debt: [TDR ids, or none] (§ 7, by code)
  ⏭ [component-slug] — skipped (unchanged since last generation)
  ✗ [component-slug] — VALIDATION_FAILED: [notes]

Legacy v2 handoffs removed: [N]
Legacy v2 handoffs retained (Component Specification failed): [N]
  - handoffs/03-legacy-comp-handoff.md — Component Specification regen failed

Orphaned assets: [O]
  - <asset_path> — will be regenerated next run

Warnings (prerequisites):
  ⚠ [warning line]

Warnings (edge cross-check):
  ⚠ [warning line]

Identifiers not in English (identifier-check.js — fix in the docs, then regenerate):
  ⚠ `[token]` — [file:line, …]

Main-context reads (shared docs): 1 (ARCHITECTURE.md only — handoff-prepare.js owns docs/04–09 + adr/ + analysis/)
Payloads (handoff-prepare.js, no model tokens):
  shared docs: [N] · analyses: [N] · institutional ADRs: [N]
  edges: [N] active, [U] endpoint(s) not a documented component
  panels: [P] phases in the catalog, once · [F] flows with a main image · [C] cuts of <docs/03 diagram> · kit-check over the kit: PASS
Phase 5: first cohort [N] Task(s) · [R] spawned as lanes freed (rolling)
  ekonte / settei: 1 sonnet each (if REGEN)
  seams: {seam_parallelism}-parallel sonnet
  component specifications: {parallelism}-parallel sonnet
  assets: {asset_parallelism}-parallel sonnet ([X]) · C4 descriptors rendered by code ([Y])
Step 5.3 gap-merge edits: [E] Component Specification(s) had asset gaps merged into § 11

💡 Generated the handoff kit. Run `/compact` to trim main context now if continuing.
```

If any of `Interface contracts: skipped`, `Component Specifications: skipped`, or `Legacy removed/retained` counters are 0, omit their bullets. Skipped entries are listed under their bucket so users can decide whether to `--force` a targeted re-run.

---

## Files in This Skill

- **SKILL.md** — this file (orchestrator)
- **SYSTEM_EKONTE_TEMPLATE.md** — bundled by ekonte-generator
- **SETTEI_TEMPLATE.md** — bundled by settei-generator
- **SEAM_SPEC_TEMPLATE.md** — bundled by seam-generator
- **CUT_SHEET_TEMPLATE.md** — bundled by cutsheet-generator
- **SECTION_EXTRACTION_GUIDE.md** — extraction rules for all four templates
- **PAYLOAD_SCHEMA.md** — three-payload contract between `scripts/handoff-prepare.js` and the generators
- **assets/_index.md** — asset-type → output-filename map (bundled into handoff-asset-generator)
- **ASSET_GENERATION_GUIDE.md** — per-asset scaffold templates (unchanged; consumed by handoff-asset-generator)
- **utils/manifest.ts / manifest-cli.ts** — v4 manifest (run / seams / cut_sheets sections; v3 and v1/v2 shapes migrate on load)
- **utils/prepare-payload-dir.ts** — cross-platform payload dir creation + date capture
- **scripts/handoff-prepare.js** — the three payload shapes, fingerprints and skip decisions by code; tests in `tests/handoff-prepare.test.ts`
- **scripts/kit-check.js** — the gate over the written kit: markers, leftover placeholders, authoring-rule comments, every Mermaid fence; tests in `tests/kit-check.test.ts`
- **scripts/kit-coherence.js** and **scripts/kit-drift.js** — Step 5.2c: ownership across parts, and what a regeneration dropped or re-decided against the committed kit (judge); tests in `tests/kit-coherence.test.ts`
- **scripts/kit-readme.js** — `handoffs/README.md` rendered from the manifest, the ledger and `context-result.json`; tests in `tests/kit-readme.test.ts`

---

## Permissions required

Add to project `.claude/settings.json`:

```json
"Edit(handoffs/**)",
"Read(handoffs/**)",
"Edit(handoffs/.manifest.json)",
"Read(handoffs/.manifest.json)",
"Edit(.cache/sa-skills/handoff-payloads/**)",
"Read(.cache/sa-skills/handoff-payloads/**)",
"Read(~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/**)",
"Read(~/.claude/plugins/cache/shadowx4fox-solution-architect-marketplace/**)",
"Bash(bun *)",
"Bash(rg *)",
"Bash(rm handoffs/*-handoff.md)",
"Agent(sa-delivery:generators:ekonte-generator)",
"Agent(sa-delivery:generators:settei-generator)",
"Agent(sa-delivery:generators:seam-generator)",
"Agent(sa-delivery:generators:cutsheet-generator)",
"Agent(sa-delivery:generators:handoff-asset-generator)"
```

The payloads are built by `scripts/handoff-prepare.js` under `Bash(bun *)`; no builder agent is
spawned (`/setup` removes the retired `Agent(sa-skills:builders:handoff-context-builder)` grant).

The `Bash(rm handoffs/*-handoff.md)` grant is used ONLY for the v2 → v3
migration in Phase 6 to delete legacy files after their replacements
succeed. If your project prefers to migrate manually, omit this grant —
the skill will log `Legacy retained` in Phase 7 for every legacy file
and leave them on disk.
