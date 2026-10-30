---
name: architecture-icepanel-sync
description: >
  (Beta) Sync architecture documentation to IcePanel for C4 model visualization.
  Extracts C4 elements from architecture docs, generates IcePanel import YAML,
  checks IcePanel API for existing objects, and imports new objects or reports drift.
triggers:
  - sync to icepanel
  - sync to IcePanel
  - icepanel sync
  - icepanel
  - update icepanel
  - icepanel import
  - check icepanel
  - icepanel drift
  - IcePanel drift check
  - C4 model sync
  - icepanel status
  - generate icepanel yaml
  - export for icepanel
---

# IcePanel Sync Skill (Beta)

Syncs architecture documentation to IcePanel by extracting C4 model elements, generating import YAML, and optionally pushing via the IcePanel REST API.

> **Two modes**: Online (API key present — check, import, drift detect) or Offline (no API key — generate YAML for manual import).

> **Output directory**: `icepanel-sync/` at project root. Always produces `c4-model.yaml` and `sync-report.md`.

---

## Workflow Detection

Detect which workflow the user wants based on their request:

| User Intent | Workflow | Requires API Key |
|-------------|----------|-----------------|
| "sync to icepanel", "icepanel import", "update icepanel" | **Full Sync** (Phase 0 → 1 → 2 → 3) | Optional (offline fallback) |
| "icepanel drift", "check icepanel", "icepanel status" | **Drift Report Only** (Phase 0 → 2 only) | Yes — stop if missing |
| "generate icepanel yaml", "export for icepanel" | **YAML Export Only** (Phase 0 → 1 only) | No |

**Drift Report Only** skips YAML generation and import — it queries IcePanel's current state, compares against architecture docs, and produces `icepanel-sync/drift-report.md`. This is useful for periodic checks without modifying IcePanel.

**YAML Export Only** skips all API interaction — just extracts and generates the import file.

> **Fidelity rule**: All data in the generated YAML comes from architecture docs. Never invent names, descriptions, technologies, or connections not present in the source files.

> **Design Language Standard (conditional)**: if `[design_language_dir]/llms-rules.txt` exists, read it before generating the YAML and apply it in preference to `skills/architecture-docs/references/DIAGRAM-GENERATION-GUIDE.md` wherever the two differ — the standard's own refusal contract demotes that guide to informative as of v0.3, naming Point 5 §3.4 as the registry of record for Action Types. It governs connection labels, Diagram IDs, display names, the controlled tag vocabularies, and the `-DEP-` view rules (every Deployment connection is `No direction`, transport-form label only, no Action Type). Every registry in it is **closed** — never invent an Action Type, capability code, or tag value to make a diagram parse; an unregistered value is what nightly check `C-11` (labels) or `C-12` (tags) reports against a named author. If the file is absent, proceed unchanged. See `[design_language_dir]/README.md` for the load contract.

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

**In this skill**: nothing localizes. `icepanel-sync/c4-model.yaml` is machine-facing, and the SA Design Language Standard requires English for element names, tag groups and tag **values**, Diagram ID segments, Action Types and export profile names in every edition of the standard. `sync-report.md` prose may follow `doc_language`; every value bound for IcePanel may not.

Structural headings this skill writes carry their English anchor comment in both languages
(`## Heading <!-- SECTION: English Name -->`). The full do-not-localize registry — codes, status
enum values, table column headers, filenames, marker names, `EXPLORER_HEADER` field keys — is
`LANGUAGE_POLICY.md` §4.

---

## Phase 0 — Resolve Environment

### Step 0.1 — Resolve Plugin Directory

**Resolve `plugin_dir`** — one call, never a Glob over `~/.claude/plugins/cache/` (it keeps every version ever installed and a glob returns an arbitrary one):

```bash
plugin_dir=$(bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts --plugin sa-delivery)
sa_skills_dir=$(bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts)
```

`[design_language_dir]` is the Design Language Standard in force — `bun [sa_skills_dir]/scripts/shared/packs.js --path design-language` prints it (an institution pack's — the base carries none) or prints nothing and exits 1: **fallback mode**.

This skill ships in the **sa-delivery** plugin (`sa-skills` depends on it and installs it). `[plugin_dir]` is sa-delivery's install (this skill's scripts, templates and agents); `[sa_skills_dir]` is sa-skills' — the architecture is read through its facts ledger, explorer, judge and shared scripts, documents render through its `tools/docgen`, and the scripts find it on their own (`scripts/sa-skills.js`: `--sa-skills`, `SA_SKILLS_DIR`, the repo layout, the install registry) and stop with the install command when sa-skills is absent. The script answers from Claude Code's install registry — the project-scope install for this directory, else the user-scope one, else the copy it runs from — and warns on stderr when a newer version is on the machine (`claude plugin update … --scope <scope>`, then `/reload-plugins`); show that warning to the user. Without the marketplace clone (a dev clone alone): Glob `**/{sa-skills,solutions-architect-skills}/.claude-plugin/plugin.json` **outside** `~/.claude/plugins/cache/`, strip `/.claude-plugin/plugin.json` for `sa_skills_dir` and append `/plugins/sa-delivery` for `plugin_dir`.

If both steps fail, stop and report:
```
Cannot locate plugin directory. Ensure the plugin is installed correctly.
```

### Step 0.2 — Load Reference

Read `$plugin_dir/skills/architecture-icepanel-sync/ICEPANEL_IMPORT_REFERENCE.md` — this contains the YAML schema, type mapping, ID rules, and tag conventions. Keep these rules in context for the entire workflow.

### Step 0.3 — Check Prerequisites

Read these files (stop if any required file is missing):

| File | Required | Purpose |
|------|----------|---------|
| `docs/03-architecture-layers.md` | Yes | C4 diagrams (L1 Context + L2 Container) |
| `docs/components/README.md` | Yes | Component index — the derived fallback when `component-cli.ts` is unavailable |
| `docs/01-system-overview.md` | No | System name and description enrichment |
| `docs/05-integration-points.md` | No | Connection protocol enrichment |

If `docs/03-architecture-layers.md` is missing:
```
docs/03-architecture-layers.md not found.
Generate architecture documentation first with /skill architecture-docs.
```

If `docs/components/README.md` is missing:
```
docs/components/README.md not found.
Create component index first with /skill architecture-component-guardian sync.
```

### Step 0.4 — Detect Sync Mode

Check for IcePanel configuration:

1. Check environment variables: `ICEPANEL_API_KEY` and `ICEPANEL_LANDSCAPE_ID`
2. If not in env, check for `.env` file at project root — look for these two variables

**If both variables found** → Online mode. Confirm with user:
```
IcePanel API credentials detected. Running in online mode — will check existing objects and import/report drift.
Landscape ID: {ICEPANEL_LANDSCAPE_ID}
```

**If either variable is missing** → Offline mode. Inform user:
```
No IcePanel API credentials found. Running in offline mode — will generate import YAML only.
To enable online sync, set ICEPANEL_API_KEY and ICEPANEL_LANDSCAPE_ID in your environment or .env file.
```

### Step 0.5 — Create Output Directory

Cross-platform Bun helper (replaces `mkdir -p icepanel-sync` — works identically on Linux, macOS, Windows native, WSL, and Git Bash):

```bash
bun [sa_skills_dir]/scripts/ensure-dir.ts icepanel-sync
```

---

## Phase 1 — Extract C4 Model & Generate Import YAML

### Step 1.1 — Parse C4 Diagrams

Read `docs/03-architecture-layers.md` and extract all Mermaid C4 diagram blocks.

**Extract from `C4Context` blocks:**

Find code fences containing `C4Context`. For each element:

- `Person(id, "name", "description")` → Record as person (used for report only — not imported as model object)
- `Person_Ext(id, "name", "description")` → Record as external person
- `System(id, "name", "description")` → Record as internal system
- `System_Ext(id, "name", "description")` → Record as external system
- `Rel(from, to, "description", "protocol")` → Record as connection. The 3rd parameter (description) carries the verb plus any via-hop / topic / queue / async context; the 4th parameter (protocol) follows the canonical `<PROTOCOL>/<STYLE> [Action Type]` normal form — governed by `[design_language_dir]/llms-rules.txt` §5 when that file is present, otherwise by the Connection Naming Rule in `skills/architecture-docs/references/DIAGRAM-GENERATION-GUIDE.md`. The IcePanel `modelConnections.name` field stores the 4th-parameter value verbatim.

**Extract from `C4Container` blocks:**

Find code fences containing `C4Container`. For each element:

- `Container_Boundary(id, "name")` → Record the system boundary ID and name
- `Container(id, "name", "technology", "description")` → Record as app container
- `ContainerDb(id, "name", "technology", "description")` → Record as store container
- `ContainerQueue(id, "name", "technology", "description")` → Record as store container (subtype: message-broker). Exceptional use only — per the Infrastructure-as-via Rule, transit brokers collapse into edge encoding (description + protocol on `Rel()`), not a `ContainerQueue` node
- `Rel(from, to, "description", "protocol")` → Record as connection (merge with L1 connections, deduplicate). Same Connection Naming Rule applies — 4th parameter MUST be the canonical normal form

**Skip**: `%%{init: ...}%%` theme directives, `title` lines, comment lines starting with `%%`.

**Governed-notation branch — when no `C4Context` / `C4Container` fence exists**: an architecture generated under the Design Language governed mode (see `skills/architecture-docs/references/DIAGRAM-GENERATION-GUIDE.md` § Design Language Governance) carries Diagrams 2 and 3 as `flowchart TB` blocks instead. Do not fail with "zero systems extracted" — extract from the governed sources:

- **Systems and containers** — from the component facts (Step 1.2's `component-facts.ts list` becomes the primary element source, not an enrichment): C4 L1 descriptors → systems, C4 L2 components → containers, with canonical name, type and technology from the tuple. External systems and persons → the `ext`-classed nodes of the Diagram 2 block.
- **Boundary** — the `subgraph` (classed `zone`) of the Diagram 3 block → the system boundary ID and name.
- **Connections** — the directed edges of the Diagram 3 block: `A -->|"<label>"| B` → a connection from `A` to `B`; the quoted label carries the same `<PROTOCOL>/<STYLE> [Action Type]` normal form the `Rel()` 4th parameter carries in C4 notation, and `modelConnections.name` stores it verbatim. Merge with Diagram 2 edges and deduplicate, exactly as the C4 branch merges L1 and L2 `Rel()` lines.

Store-shaped nodes (`[( )]`, classed `store`) map to store containers; the Infrastructure-as-via Rule applies unchanged — a broker that appears only in edge labels is edge encoding, not an element.

### Step 1.2 — Enrich from Component Facts

Load the component facts — never hand-parse `docs/components/README.md`:

```bash
bun [sa_skills_dir]/scripts/shared/component-facts.ts list <project_root>
```

For each entry with `level: L2`:
- Match `name` to a container extracted in Step 1.1 (fuzzy match on name)
- Enrich the container with:
  - **`type`** → map to C4 type tag (one of 8 canonical types)
  - **`technology[]`** → one technology tag per entry, already bracket-stripped
  - **`system`** → the system grouping, used to validate parentId assignments

The component file is the source of truth and the README is derived from it, so the CLI reads the
files rather than the index. If the command is unavailable, fall back to parsing the 5-column
table(s) in `docs/components/README.md` and note the degradation.

### Step 1.3 — Enrich from Integration Points (optional)

If `docs/05-integration-points.md` exists, read the integration tables.

For each integration entry, find the matching connection from Step 1.1 and enrich:
- Protocol details → more specific connection name
- Direction (Sync/Async) → connection direction hint
- Auth method → add as tag if relevant

### Step 1.4 — Validate Extracted Model

Run these checks before generating YAML. Collect all findings.

**FAIL checks (block generation):**
- No C4 diagrams found in `docs/03-architecture-layers.md`
- Zero systems extracted
- Zero containers extracted

**WARN checks (generate but report):**
- `Rel()` references an element ID not found in any `Person()`, `System()`, or `Container()` declaration
- A component returned by `component-facts.ts list` (`level: L2`) has no matching container in C4 diagrams
- A container has empty technology field
- Duplicate element IDs detected

If any FAIL check triggers, stop and report:
```
Validation failed — cannot generate import YAML:
- {list of FAIL findings}

Fix the architecture documentation and retry.
```

If only WARN checks trigger, continue but include warnings in the sync report.

### Step 1.5 — Generate Import YAML

Build the `LandscapeImportData` YAML following the reference document rules.

**ID generation**: Use the Mermaid element ID as-is if it's already kebab-case. Otherwise convert: lowercase, replace spaces/underscores with hyphens, strip special characters.

**Build order:**

1. **tagGroups** — always create `technology` and `c4-type` groups
2. **tags** — one tag per unique technology + one tag per unique C4 type found
3. **modelObjects** — systems first (parentId: null), then containers (parentId: system-id)
   - Internal systems: `type: system`
   - External systems: `type: system`, tagged with `external`
   - App containers: `type: app`
   - Store containers (DB + Queue): `type: store`
4. **modelConnections** — one per unique `Rel()`, deduplicated

**Assign tagIds**: Each modelObject gets tagIds referencing its technology tags + its C4 type tag.

**Write** the YAML to `icepanel-sync/c4-model.yaml` with the schema comment at the top:
```yaml
# yaml-language-server: $schema=https://api.icepanel.io/v1/schemas/LandscapeImportData
namespace: architecture-docs
```

Report to user:
```
Generated icepanel-sync/c4-model.yaml
- {N} systems ({M} external)
- {N} containers ({M} apps, {M} stores)
- {N} connections
- {N} tags ({M} technology, {M} type)
```

**If offline mode** → skip to Phase 3 (Report).

---

## Phase 2 — Check IcePanel (Online Mode Only)

### Step 2.1 — Fetch Existing Objects

Query the IcePanel API. The cache directory is created by the cross-platform Bun helper (works identically on Linux, macOS, Windows native, WSL, and Git Bash):

```bash
# Ensure project-local cache dir exists (cross-platform; no POSIX `mkdir -p` dependency)
bun [sa_skills_dir]/scripts/ensure-dir.ts .cache/sa-skills/icepanel

# Fetch model objects
curl -s "https://api.icepanel.io/v1/model/objects" \
  -H "Authorization: ApiKey ${ICEPANEL_API_KEY}" \
  > .cache/sa-skills/icepanel/objects.json

# Fetch model connections
curl -s "https://api.icepanel.io/v1/model/connections" \
  -H "Authorization: ApiKey ${ICEPANEL_API_KEY}" \
  > .cache/sa-skills/icepanel/connections.json
```

If either request fails (non-200 status), report the error and fall back to offline mode:
```
IcePanel API request failed (HTTP {status}). Falling back to offline mode.
The import YAML has been generated at icepanel-sync/c4-model.yaml — import it manually.
```

### Step 2.2 — Compare Models

Compare the extracted model (Phase 1) against the IcePanel state:

**For each extracted system/container:**
- Search IcePanel objects by name (case-insensitive match)
- If found → mark as `SYNCED` (check for attribute drift: name, type, tags)
- If not found → mark as `NEW` (needs import)

**For each IcePanel object (in the `architecture-docs` namespace):**
- If no matching element in extracted model → mark as `STALE` (exists in IcePanel but not in docs)

**For each extracted connection:**
- Search IcePanel connections by originId + targetId
- If found → mark as `SYNCED` (check name/protocol drift)
- If not found → mark as `NEW`

**For each IcePanel connection (in namespace):**
- If no match in extracted model → mark as `STALE`

### Step 2.3 — Present Diff Summary

Show the user a summary:

```
IcePanel Sync Status:
  Objects:  {N} synced, {N} new, {N} stale, {N} drifted
  Connections: {N} synced, {N} new, {N} stale, {N} drifted

New (will be imported):
  - {object name} ({type})
  ...

Stale (in IcePanel but not in docs):
  - {object name} ({type})
  ...

Drifted (attribute mismatch):
  - {object name}: {field} differs (docs: "{value}" vs IcePanel: "{value}")
  ...
```

**If there are NEW objects**, ask user:
```
Import {N} new objects and {N} new connections to IcePanel?
```

**If everything is synced** with no drift:
```
IcePanel is in sync with architecture documentation. No changes needed.
```

---

## Phase 3 — Sync or Report

### Step 3.1 — Import New Objects (Online Mode, if user approves)

If user approves the import:

```bash
# Import the YAML
IMPORT_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST "https://api.icepanel.io/v1/landscapes/${ICEPANEL_LANDSCAPE_ID}/import" \
  -H "Authorization: ApiKey ${ICEPANEL_API_KEY}" \
  -H "Content-Type: application/x-yaml" \
  --data-binary @icepanel-sync/c4-model.yaml)
```

Parse the response. If the import returns an `importId`, check status:

```bash
curl -s "https://api.icepanel.io/v1/landscapes/${ICEPANEL_LANDSCAPE_ID}/import/${IMPORT_ID}" \
  -H "Authorization: ApiKey ${ICEPANEL_API_KEY}"
```

Report result:
```
Import successful. {N} objects and {N} connections added to IcePanel.
Note: Diagrams are not auto-created. Create C4 L1 and L2 diagram views manually in IcePanel.
```

If import fails, report the error and note the YAML file is available for manual import.

### Step 3.2 — Generate Sync Report

Write `icepanel-sync/sync-report.md`:

```markdown
# IcePanel Sync Report

**Generated**: {YYYY-MM-DD HH:MM}
**Mode**: Online | Offline
**Landscape ID**: {id} (or "N/A — offline mode")

## Model Summary

| Element | Count |
|---------|-------|
| Internal Systems | {N} |
| External Systems | {N} |
| App Containers | {N} |
| Store Containers | {N} |
| Connections | {N} |
| Technology Tags | {N} |
| C4 Type Tags | {N} |

## Validation Results

| Check | Status | Details |
|-------|--------|---------|
| C4 diagrams present | PASS/FAIL | ... |
| All Rel() endpoints declared | PASS/WARN | ... |
| Components match containers | PASS/WARN | ... |
| No empty technology fields | PASS/WARN | ... |
| No duplicate IDs | PASS/WARN | ... |

## Sync Status (online mode only)

| Category | Synced | New | Stale | Drifted |
|----------|--------|-----|-------|---------|
| Objects | {N} | {N} | {N} | {N} |
| Connections | {N} | {N} | {N} | {N} |

### New Objects (imported)
- ...

### Stale Objects (in IcePanel, not in docs)
- ...

### Attribute Drift
- ...

## Import File

The generated YAML import file is at: `icepanel-sync/c4-model.yaml`

To import manually:
1. Open your IcePanel landscape
2. Go to workspace settings → Import Model
3. Upload `c4-model.yaml`
4. Review and confirm

> Diagrams are not auto-created by import. After importing, create C4 L1 (System Context) and C4 L2 (Container) diagram views in IcePanel manually.
```

### Step 3.3 — Final Summary

Report to user:

**Offline mode:**
```
IcePanel sync complete (offline mode).
  - icepanel-sync/c4-model.yaml — import this file into IcePanel
  - icepanel-sync/sync-report.md — validation results and model summary

To enable online sync, set ICEPANEL_API_KEY and ICEPANEL_LANDSCAPE_ID.
```

**Online mode:**
```
IcePanel sync complete.
  - {N} objects imported / {N} already synced / {N} stale / {N} drifted
  - icepanel-sync/c4-model.yaml — generated import file
  - icepanel-sync/sync-report.md — full sync report

Remember: create diagram views manually in IcePanel after import.
```

---

## Workflow: Drift Report Only

> Triggered by: "icepanel drift", "check icepanel", "icepanel status"
>
> This workflow queries IcePanel and compares against architecture docs **without generating import YAML or modifying IcePanel**. Use it for periodic health checks.

### Step D.0 — Resolve Environment

Run Phase 0 (Steps 0.1–0.5). **API key is required** — if missing, stop:

```
Drift report requires IcePanel API access.
Set ICEPANEL_API_KEY and ICEPANEL_LANDSCAPE_ID in your environment or .env file.
```

### Step D.1 — Extract Model from Docs

Run Phase 1 Steps 1.1–1.4 (parse C4 diagrams, enrich from component index and integration points, validate). **Skip Step 1.5** — do not generate YAML.

### Step D.2 — Fetch IcePanel State

Run Phase 2 Step 2.1 — fetch objects and connections from IcePanel API.

### Step D.3 — Compare and Generate Drift Report

Run Phase 2 Step 2.2 (compare models). Then write `icepanel-sync/drift-report.md`:

```markdown
# IcePanel Drift Report

**Generated**: {YYYY-MM-DD HH:MM}
**Landscape ID**: {ICEPANEL_LANDSCAPE_ID}

## Summary

| Category | Synced | Docs Only | IcePanel Only | Drifted |
|----------|--------|-----------|---------------|---------|
| Objects | {N} | {N} | {N} | {N} |
| Connections | {N} | {N} | {N} | {N} |

**Status**: {IN SYNC | DRIFT DETECTED}

## Docs Only (in architecture docs, missing from IcePanel)

| Element | Type | Source |
|---------|------|--------|
| {name} | {system/app/store} | docs/03-architecture-layers.md |
| ... | ... | ... |

**Action**: Run `/skill architecture-icepanel-sync` to import these into IcePanel.

## IcePanel Only (in IcePanel, missing from architecture docs)

| Element | Type | IcePanel ID |
|---------|------|-------------|
| {name} | {system/app/store} | {id} |
| ... | ... | ... |

**Action**: Either add these to architecture docs or remove from IcePanel if stale.

## Attribute Drift (present in both, values differ)

| Element | Field | Docs Value | IcePanel Value |
|---------|-------|-----------|----------------|
| {name} | {name/type/technology} | {docs value} | {icepanel value} |
| ... | ... | ... | ... |

**Action**: Decide which source is authoritative and update the other.

## Connections Drift

### New (in docs, not in IcePanel)
| From | To | Protocol |
|------|-----|----------|
| {origin} | {target} | {protocol} |

### Stale (in IcePanel, not in docs)
| From | To | Protocol | IcePanel ID |
|------|-----|----------|-------------|
| {origin} | {target} | {protocol} | {id} |

### Drifted (protocol/label mismatch)
| From | To | Docs Protocol | IcePanel Protocol |
|------|-----|--------------|-------------------|
| {origin} | {target} | {docs} | {icepanel} |
```

### Step D.4 — Report

```
Drift report generated: icepanel-sync/drift-report.md
  Objects:  {N} synced, {N} docs-only, {N} icepanel-only, {N} drifted
  Connections: {N} synced, {N} docs-only, {N} icepanel-only, {N} drifted

Status: {IN SYNC | DRIFT DETECTED — review drift-report.md for details}
```

Do NOT offer to import or modify IcePanel — this workflow is read-only.

---

## Workflow: YAML Export Only

> Triggered by: "generate icepanel yaml", "export for icepanel"
>
> Generates the import YAML without any API interaction. Useful when you just need the file.

Run Phase 0 (Steps 0.1–0.3, skip 0.4 API detection) → Phase 1 (all steps). Write `c4-model.yaml` and a minimal `sync-report.md` with validation results only (no sync status section).
