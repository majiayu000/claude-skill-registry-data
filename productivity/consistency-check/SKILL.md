---
name: consistency-check
description: "Scan all CDDs against the entity registry to detect cross-document inconsistencies. Works for both game and product CDDs. Grep-first approach — reads registry then targets only conflicting CDD sections rather than full document reads."
argument-hint: "[full | since-last-review | entity:<name> | item:<name> | schema:<name> | api:<name> | permission:<name> | config:<name>]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

## Scope, evidence and effects

Read `standards/evidence-lifecycle.md` and `standards/notes-adr-sync.md` from the
project root. Reuse explicit existing authorization for its named paths, effects
and limits across roles and retries. Present unresolved material choices or new
effects for approval; a document/batch/synchronization authorization does not
require another question for each covered section or file. Content agreement,
write authority, independent review, ADR acceptance and workflow completion
remain separate.

Analysis defaults to read-only: no write entrypoint, input edits, status/index/
session/Memory Bank updates. Report-only may write one new assigned report with
authority; report approval does not authorize indexes or rolling logs. Other
writes need the named path/effect in existing authority or a concrete draft and
changeset approval. Unknown paths are findings, not permission to create them.
No Memory Bank means use the established report/conversation fallback. Next
steps are recommendations; execute only effects already authorized or explicitly
selected by the user. Tool availability determines the question interface.

Bind claims to a declared scope and minimum direct/indirect evidence closure:
record original paths, full SHA-256, byte sizes, source commit plus exact diff
and uncommitted/ignored/external identities, exclusions and recoverable originals.
Do not read sensitive local settings or secrets merely to complete discovery.
Read required inputs back from their actual paths, verify closure and report
missing inputs as incomplete affected checks. Keywords, timestamps, counts,
equal hashes at two collections and static checks do not certify semantic review,
continuous unchanged history, runtime behavior or independent approval.

Classify meaningful choices with the shared disposition record (`cdd-layer`,
`no-adr`, `covered`, `documentation-update`, `adr-required`, `conflict`). Significant
trust, public contract, durable format or state ownership changes require an
Accepted ADR/valid scoped exception before affected implementation continues.
Keep As-Is observations and their evidence separate from Target promises and
gaps; implemented behavior cannot lower a governing Target. Continue independent
work while blocking only affected dependants.

## User Guide

- When to use: Scan all CDDs against the entity registry to detect cross-document inconsistencies. Works for both game and product CDDs. Grep-first approach — reads registry then targets only conflicting CDD sections rather than full document reads.
- Inputs: Command arguments: `/consistency-check [full | since-last-review | entity:<name> | item:<name> | schema:<name> | api:<name> | permission:<name> | config:<name>]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

# Consistency Check

Detects cross-document inconsistencies by comparing all CDDs against the
entity registry (`design/registry/entities.yaml`). Uses a grep-first approach:
reads the registry once, then targets only the CDD sections that mention
registered names — no full document reads unless a conflict needs investigation.

**This skill is the write-time safety net.** It catches what `/design-system`'s
per-section checks may have missed and what `/review-all-gdds`'s holistic review
catches too late.

**When to run:**
- After writing each new CDD (before moving to the next system)
- Before `/review-all-gdds` (so that skill starts with a clean baseline)
- Before `/create-architecture` (inconsistencies poison downstream ADRs)
- On demand: `/consistency-check entity:[name]` to check one entity specifically

**Output:** Conflict report + optional registry corrections

---

## Phase 1: Parse Arguments and Load Registry

Validate before spawn/write/verdict: accept absent/full, `since-last-review`
or one documented `entity:`/`item:`/`schema:`/`api:`/`permission:`/`config:`
selector with a nonempty name. Reject unknown modes/selectors, empty or whitespace
names (`entity:`, `schema:`), extra selectors and unknown explicit flags. Give the
legal usage `/consistency-check [full|since-last-review|entity:<name>|item:<name>|schema:<name>|api:<name>|permission:<name>|config:<name>]`
and a correction; stop rather than default, spawn, write or issue a verdict.

**Modes:**
- No argument / `full` — check all registered entries against all CDDs
- `since-last-review` — check only CDDs modified since the last review report

**[游戏专用] Game registry modes:**
- `entity:<name>` — check one specific game entity across all CDDs
- `item:<name>` — check one specific game item across all CDDs

**[通用产品] Product registry modes:**
- `schema:<name>` — check one specific data schema across all CDDs
- `api:<name>` — check one specific API contract across all CDDs
- `permission:<name>` — check one specific permission across all CDDs
- `config:<name>` — check one specific configuration parameter across all CDDs

**Load the registry:**

```
Read path="design/registry/entities.yaml"
```

If the registry is absent/empty, disclose that the registry check cannot verify
coverage; issue no PASS. Recommend the owning /design-system registry proposal
workflow without invoking it or creating entries. Governing required registry
inputs are incomplete affected checks; optional absence uses conversation/report
fallback. No CDDs likewise produces guidance without a verdict.

Build lookup tables from the registry. Game and product CDDs register different
types of cross-document facts:

**[游戏专用]** Game registry maps:
- **entity_map**: `{ name → { source, attributes, referenced_by } }`
- **item_map**: `{ name → { source, value_gold, weight, ... } }`
- **formula_map**: `{ name → { source, variables, output_range } }`
- **constant_map**: `{ name → { source, value, unit } }`

**[通用产品]** Product registry maps:
- **schema_map**: `{ name → { source, fields, constraints, referenced_by } }`
- **api_map**: `{ name → { source, endpoint, method, params, response, referenced_by } }`
- **permission_map**: `{ name → { source, roles, scope, referenced_by } }`
- **config_map**: `{ name → { source, key, default_value, range, referenced_by } }`

Count total registered entries. Report:
```
Registry loaded: [game maps if any] / [product maps if any]
Scope: [full | since-last-review | entity:name | schema:name | api:name]
```

---

## Phase 2: Locate In-Scope CDDs

```
Glob pattern="design/cdd/*.md"
```

Exclude: `game-concept.md`, `product-concept.md`, `module-index.md`, and `principles.md` — these are not
system CDDs.

For `since-last-review`, compare a prior exact registry/input manifest and
recoverable bytes to current commit+diff and uncommitted/ignored/external
identities. Include changed registry entries, referenced sources and indirect
contract dependencies. Missing baseline permits only a disclosed current-scope
scan/new full registry scan, never a timestamp-based incremental PASS.

Report the registry entries, source/reference paths, exclusions and exact
baseline before scanning. Here `full` means the full registry-derived comparison
closure, not a Full-body CDD design review; recommend /review-all-gdds for that.

---

## Phase 3: Grep-First Conflict Scan

Searches and deep interpretation must use the same bound input bytes. Use already
retained exact bytes for both, or verify each path's full digest before/after its
search/read against the manifest. If bytes change mid-run, stop affected PASS
qualification, preserve valid earlier scoped findings and rebind a fresh baseline
before rechecking the affected comparisons/closure. Never combine old grep
results with a new file body into one verified comparison.


For each registered entry, grep every in-scope CDD for the entry's name.
Use matching lines as discovery. Read complete relevant definitions, source and
reference sections and required indirect evidence before deciding equivalence;
-C 3 lines alone cannot qualify a semantic comparison. Record actual coverage.

This is the core optimization: instead of reading 10 CDDs × 400 lines each
(4,000 lines), you grep 50 entity names × 10 CDDs (50 targeted searches,
each returning ~10 lines on a hit).

### 3a: Game Entity Scan

**[游戏专用]** For each entity in entity_map:

```
Grep pattern="[entity_name]" glob="design/cdd/*.md" output_mode="content" -C 3
```

For each CDD hit, extract the values mentioned near the entity name:
- any numeric attributes (counts, costs, durations, ranges, rates)
- any categorical attributes (types, tiers, categories)
- any derived values (totals, outputs, results)
- any other attributes registered in entity_map

Compare extracted values against the registry entry.

**Conflict detection:**
- Registry says `[entity_name].[attribute] = [value_A]`. CDD says `[entity_name] has [value_B]`. → **CONFLICT**
- Registry says `[item_name].[attribute] = [value_A]`. CDD says `[item_name] is [value_B]`. → **CONFLICT**
- CDD mentions `[entity_name]` but doesn't specify the attribute. → **NOTE** (no conflict, just unverifiable)

### 3b: Item Scan

For each item in item_map, grep all CDDs for the item name. Extract:
- sell price / value / gold value
- weight
- stack rules (stackable / non-stackable)
- category

Compare against registry entry values.

### 3c: Formula Scan

For each formula in formula_map, grep all CDDs for the formula name. Extract:
- variable names mentioned near the formula
- output range or cap values mentioned

Compare against registry entry:
- Different variable names → **CONFLICT**
- Output range stated differently → **CONFLICT**

### 3d: Constant Scan

For each constant in constant_map, grep all CDDs for the constant name. Extract:
- Any numeric value mentioned near the constant name

Compare against registry value:
- Different number → **CONFLICT**

---

**[通用产品]** Product scans:

### 3e: Schema Scan

For each schema in schema_map, grep all CDDs for the schema name. Extract:
- field names and types
- constraints (required, unique, max length)
- relationships (foreign keys, references)

Compare against registry. Flag: field type mismatch, missing constraint, relationship drift.

### 3f: API Contract Scan

For each API in api_map, grep all CDDs for the endpoint name. Extract:
- HTTP method and path
- request/response shapes
- error codes

Compare against registry. Flag: method mismatch, path drift, response shape conflict.

### 3g: Permission Scan

For each permission in permission_map, grep all CDDs for the permission name. Extract:
- assigned roles
- scope boundaries
- resource targets

Compare against registry. Flag: role drift, scope expansion without documentation.

### 3h: Configuration Scan

For each config in config_map, grep all CDDs for the config key. Extract:
- default values
- valid ranges
- environment overrides

Compare against registry. Flag: default mismatch, range conflict, missing environment override.

## Phase 4: Deep Investigation (Conflicts Only)

For each conflict found in Phase 3, do a targeted full-section read of the
conflicting CDD to get precise context:

```
Read path="design/cdd/[conflicting_cdd].md"
```
Read the complete affected definition/contract and its required dependencies;
grep excerpts alone may miss qualifiers, aliases or exception rules.

Confirm the conflict with full context. Determine:
1. **Owner and authority:** The registry `source:` identifies a candidate owner;
   verify the governing CDD/Accepted decision and exact approved scope. It does
   not prove that a contradictory downstream or implemented value is wrong.
2. **Freshness:** Compare exact retained baselines/current bytes and choices.
   Git log or mtime alone cannot prove the registry stale.
3. **Resolution:** Separate As-Is from Target and classify the decision under
   `standards/notes-adr-sync.md`. Propose authorized source/registry/dependant
   edits; required acceptance precedes affected implementation.

For each conflict, classify:
- **🔴 CONFLICT** — same named entity/item/formula/constant/schema/API/permission/config
  with different values or contracts in different CDDs. Must resolve before
   affected architecture proceeds; name dependants and continue independent work.
- **⚠️ STALE REGISTRY** — source CDD value changed but registry not updated.
  Registry needs updating; other CDDs may be correct already.
- **ℹ️ UNVERIFIABLE** — entity mentioned but no comparable attribute stated.
  Not a conflict; just noting the reference.

---

## Phase 5: Output Report

```
## Consistency Check Report
Date: [date]
Registry entries checked: [N entities, N items, N formulas, N constants, N schemas, N APIs, N permissions, N configs]
CDDs scanned: [N] ([list names])

---

### Conflicts Found (must resolve before architecture)

🔴 [Entity / Item / Formula / Constant / Schema / API / Permission / Config Name]
   Registry (source: [cdd]): [attribute] = [value]
   Conflict in [other_cdd].md: [attribute] = [different_value]
   → Resolution needed: [which doc to change and to what]

---

### Stale Registry Entries (registry behind the CDD)

⚠️ [Entry Name]
   Registry says: [value] (written [date])
   Source CDD now says: [new value]
   → Update registry entry to match source CDD, then check referenced_by docs.

---

### Unverifiable References (no conflict, informational)

ℹ️ [cdd].md mentions [entity_name] but states no comparable attributes.
   No conflict detected. No action required.

---

### Clean Entries (no issues found)

✅ [N] registry entries verified across all CDDs with no conflicts.

---

Verdict: PASS | CONFLICTS FOUND
```

**Verdict:**
- **PASS** — all declared registry comparisons verified, no conflicts or missing
  required inputs. This is scoped registry agreement, not full CDD review approval.
- **INCOMPLETE** — required input/definition/dependency cannot be verified.
- **CONFLICTS FOUND** — one or more conflicts detected. List resolution steps.

---

A requested report-only run may save one new assigned report with scoped
authority; registry corrections and reflexion logs remain untouched.

## Phase 6: Registry Corrections

If stale registry entries were found, ask:
> "May I update `design/registry/entities.yaml` to fix the [N] stale entries?"

For each stale entry:
- Update the `value` / attribute field
- Set `revised:` to today's date
- Add a YAML comment with the old value: `# was: [old_value] before [date]`

If new entries were found in CDDs that are not in the registry, ask:
> "Found [N] entities/items mentioned in CDDs that aren't in the registry yet.
> May I add them to `design/registry/entities.yaml`?"

Only add entries that appear in more than one CDD (true cross-system facts).

**Never delete registry entries.** Set `status: deprecated` if an entry is removed
from all CDDs.

After authorized repair, reread changed inputs/closure and collect a fresh
baseline. Completion of execution is separate from PASS, CONFLICTS FOUND or
INCOMPLETE; unresolved choices block only named affected dependants.

### 6b: Append to Reflexion Log

If conflicts were found, propose the following reflexion entry. Append to
`docs/consistency-failures.md` only with authority for that exact log effect,
never as a read-only/report-only side effect:

```markdown
### [YYYY-MM-DD] — /consistency-check — 🔴 CONFLICT
**Domain**: [system domain(s) involved]
**Documents involved**: [source CDD] vs [conflicting CDD]
**What happened**: [specific conflict — entity name, attribute, differing values]
**Resolution**: [how it was fixed, or "Unresolved — manual action needed"]
**Pattern**: [generalised lesson, e.g. "Item values defined in combat CDD were not
referenced in economy CDD before authoring — always check entities.yaml first"]
```

Only append if `docs/consistency-failures.md` exists. If the file is missing,
disclose the omitted optional log; do not create it from this skill.

---

## Next Steps

- **If PASS**: Run `/review-all-gdds` for holistic design-theory review, or
  `/create-architecture` if all MVP CDDs are complete.
- **If CONFLICTS FOUND**: Fix the flagged CDDs, then re-run
  `/consistency-check` to confirm resolution.
- **If STALE REGISTRY**: Update the registry (Phase 6), then re-run to verify.
- Run `/consistency-check` after writing each new CDD to catch issues early,
  not at architecture time.
