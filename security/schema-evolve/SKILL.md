---
name: schema-evolve
description: "This skill should be used when the user asks about 'schema drift', 'schema evolution', 'evolve schema', 'schema sync', 'sync schemas', 'update schema fields', 'schema field frequency', 'missing schema fields', 'unused schema fields', 'schema proposal', 'schema cardinality', 'check schema', 'schema audit', 'schema changes', 'declare a relation verb', 'add a field to the schema', 'force-add schema field', 'prescribed schema vocabulary'. Detects drift between Basic Memory schema definitions and actual note usage, proposes field additions/removals based on frequency analysis, and dual-syncs BM notes + local schema files after approval."
user-invocable: true
argument-hint: "<note_type> [--prescribed verb1,verb2,...]"
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - mcp__basic-memory__schema_diff
  - mcp__basic-memory__schema_infer
  - mcp__basic-memory__schema_validate
  - mcp__basic-memory__read_note
  - mcp__basic-memory__edit_note
---

# Schema Evolution

Detect drift between a Basic Memory schema definition and actual note usage,
propose changes, and synchronize both the BM schema note and the local
`schemas/` file after user approval.

## Arguments

**Required:** the note type in snake_case.

| Example | Schema file |
|---------|-------------|
| `npm_package` | `schemas/npm_package.md` |
| `brew_formula` | `schemas/brew_formula.md` |
| `github_action` | `schemas/github_action.md` |
| `engineering` | `schemas/engineering.md` |
| `standard` | `schemas/standard.md` |

The argument must match a `type` value used in Basic Memory note frontmatter
and a corresponding file in `schemas/`. If the type is unknown, list available
schema files and ask the user to pick one.

**Optional:** `--prescribed verb1,verb2,...` — force-add specified relation
verbs (or observation field names) to the schema regardless of usage
frequency. See "Modes" below.

## Modes

The skill operates in two complementary modes:

### Drift-driven mode (default)

Invocation: `/schema-evolve <note_type>`

Frequency-based: `schema_diff` and `schema_infer` decide what to add or
remove. Fields are added only when their actual per-type usage crosses
the 25% threshold. This is the right mode for organic schema evolution
where the notes lead and the schema catches up.

Limitation: prescribed cross-schema vocabulary (e.g., a Tier-0 verb set
that should be declared identically across many schemas) cannot be
absorbed this way until each schema independently crosses 25% — which
may never happen for narrow types.

### Prescribed mode

Invocation: `/schema-evolve <note_type> --prescribed verb1,verb2,...`

Frequency-bypass: the listed names are force-added to the target schema
regardless of usage. Intended for absorbing cross-schema vocabulary
(Tier-0 verbs the operator wants declared uniformly across schemas) or
for adding fields ahead of authoring practice.

The two modes compose: in a single invocation, prescribed additions are
applied alongside drift-driven proposals. Removal and cardinality
proposals continue to come from `schema_diff` / `schema_infer` and are
unaffected by `--prescribed`.

## Edge Cases

- **No schema found** — with `output_format="json"` the tool short-circuits and
  returns `{"error": "No schema found for type '<note_type>'"}`; there is no
  `schema_found: false` payload to inspect, so key on the `error` field. Report
  "No schema registered in Basic Memory for type `<note_type>`." Direct the
  user to run `/intel` first (it auto-seeds the schema
  on first use), or to use `/memory-schema` to create the schema manually. Stop.
- **No drift detected** — rare in practice, and do not expect it: because
  `dropped_fields` lists every declared field under 10%, a schema with many
  declared fields will essentially always report drift (a 37-field schema
  cannot have all fields at ≥10% unless usage is near-uniform, which
  observation categories never are). Report "Schema is in sync — no changes
  needed" and stop only when `new_fields`, `dropped_fields` and
  `cardinality_changes` are all genuinely empty AND `--prescribed` was not
  supplied. Otherwise continue and let the proposal show empty Add/Remove
  sections.
- **Prescribed verb already present** — if a `--prescribed` entry already
  appears in the schema's `schema:` block, treat it as a no-op for that
  entry. List it in the proposal under "Already present (skipping)" so the
  operator can confirm the verb name matched what they expected. Continue
  with the remaining prescribed entries.
- **Invalid prescribed verb name** — reject any prescribed entry that is
  not a valid picoschema identifier (must match `[a-z][a-z0-9_]*` —
  lowercase, snake_case, no spaces, no leading digits). Report the
  invalid entries and ask the user to re-issue with corrected names. Do
  not silently drop them.
- **Empty `--prescribed` list** — if `--prescribed` is supplied with no
  verbs (or only whitespace/commas), warn and fall back to drift-driven
  mode.
- **Local schema file missing** — if `schemas/<note_type>.md` does not exist,
  warn and offer to create it from the current BM schema note. Do not skip.
- **Small sample** — if `schema_infer` reports fewer than 5 notes, warn that
  frequency data may be unreliable. Still present the proposal but flag it.
  Separately, below ~15 notes a **single** note crosses the 10%
  `dropped_fields` boundary on its own (1/13 = 7.7%), so on a small type expect
  most `dropped_fields` entries to be genuinely-used "used once" fields rather
  than dead ones. Weight this into the Step 5 removal decision well above the
  5-note floor.
- **Stale index right after note edits** — `edit_note` transiently inflates a
  note's parsed observation counts while the index re-syncs, and `schema_diff`
  reads that same index. Observed: immediately after a 7-note edit batch,
  `cardinality_changes` shrank from 15 entries to 12 (fields stopped looking
  single-valued) while the files on disk were unchanged. Do not run this skill
  directly after a note-editing pass — let the index settle, or verify any
  cardinality finding against the note files before acting on it.
- **User rejects proposal** — do not write anything. Report "No changes made."
- **Pre-existing divergence** — if the BM schema note and local `schemas/`
  file differ before evolution begins (detected in Step 4), present the
  divergence first and ask the user to reconcile before proceeding.

## Workflow

### Step 1: Validate inputs

Confirm the note type argument is provided. Verify the local schema file
exists:

```
Glob(pattern="schemas/<note_type>.md")
```

If the file does not exist, list available schemas:

```
Glob(pattern="schemas/*.md")
```

Report available types and ask the user to choose.

If `--prescribed` was supplied, parse the comma-separated list, trim
whitespace, drop empties, and validate each entry against the picoschema
identifier pattern `[a-z][a-z0-9_]*`. Report invalid entries and stop;
do not proceed with a partial list. Keep the validated list in memory
for Steps 4, 5, 6, and 7.

### Step 2: Detect drift

Run `schema_diff` to compare the registered schema against actual note usage:

```
schema_diff(note_type="<note_type>", output_format="json")
```

This returns:
- `new_fields` — categories or relations used in notes but not in the schema,
  at or above 25% usage (candidates for addition)
- `dropped_fields` — declared fields whose usage is **below 10%**, including
  fields at 0%. A field listed here is **rare, not unused**. The 10% cut-off
  is hard-wired in Basic Memory (`dropped_field_threshold=0.10` in
  `schema/diff.py`) and the MCP tool exposes **no** parameter to change it;
  BM's own text formatter titles the section "in schema but rare in notes".
  Never read membership in this list as evidence a field is dead — check each
  entry's own `count`. (Measured: on a 132-note type, 18 entries of which only
  2 were at 0%; on a 13-note type, 12 entries of which only 4 were at 0%.)
- `cardinality_changes` — a list of prose **strings**, not structured fields
  (e.g. `"convention: schema declares array but usage is typically
  single-value"`)

**Every `percentage` in the JSON payload is a fraction in 0–1** — `0.0985`
means 9.85%. All thresholds in this skill are written as percents; convert
before comparing, or every field will read as below threshold.

If all three are empty **and `--prescribed` was not supplied**, report "Schema
is in sync — no drift detected." Stop. If `--prescribed` was supplied,
continue to Step 4 regardless — whether any prescribed entries remain can only
be decided after the schema block has been read, which is Step 4's job.

### Step 3: Gather frequency data

This step feeds the **Watch List only** — every add/remove decision comes from
Step 2. Skip it when Step 2 already answered the question.

`threshold` does **not** filter `field_frequencies`: every field is returned at
any threshold, and lowering it only enlarges `suggested_schema`. Use the
default:

```
schema_infer(note_type="<note_type>", output_format="json")
```

Extract for each field: `name`, `source` (observation/relation), `count`,
`total`, `percentage`, `is_array`.

**Expect a large response on high-volume types.** Each field carries up to five
*full observation bodies* as `sample_values`, so the payload scales with note
count — on a 132-note type this exceeded the max tool-result size (95,249
characters) and the harness spilled it to a file. If that happens, do NOT retry
at a lower threshold (it returns more, not less): query the spilled file with
targeted `jq` for `name`/`source`/`count`/`total`/`percentage` only, and never
load `sample_values` into context. A skill cannot raise the limit itself —
`MAX_MCP_OUTPUT_TOKENS` (default 25,000) is fixed at session launch.

If the response is `{"error": "No schema pattern found ..."}`, treat it as an
empty Watch List and continue.

### Step 4: Read current schema

Read both the BM schema note and the local file:

```
read_note(identifier="main/schema/<note_type>", output_format="json")
Read(file_path="<plugin-root>/schemas/<note_type>.md")
```

Note: do NOT assume an identifier form. A schema note's permalink is whatever
its own frontmatter declares; only when frontmatter omits `permalink:` does
Basic Memory derive one from the file path, lowercasing and turning `_` into
`-`. Both forms exist in practice — `main/schema/npm_package` and
`main/schema/brew-formula` are both real permalinks in this vault, so any
hardcoded rule is wrong for some types. Read the note, take the exact
`permalink` value from the response, and use it verbatim in Steps 6 and 9.

Compare the `schema:` blocks of both sources. If they differ (pre-existing
divergence), present the differences and ask the user to reconcile before
proceeding with evolution. Do not compound existing drift.

If `--prescribed` was supplied, scan the (now-reconciled) `schema:` block
for each prescribed verb name. Partition the list into:

- **To add** — names not yet declared in the schema block
- **Already present** — names already declared (no-op for these entries)

Carry both partitions forward to Step 5.

### Step 5: Present proposal

Build and display a change proposal with four sections:

```markdown
## Schema Evolution Proposal: `<note_type>`

Based on **N** notes analyzed.

### Fields to Add (>25% usage, not in schema)

| Field | Source | Usage | Proposed Picoschema |
|-------|--------|-------|---------------------|
| `security` | observation | 25% (34/135) | `security?(array): string, CVE status and advisories` |

### Prescribed Additions (frequency-bypass)

Shown only when `--prescribed` is supplied. Source defaults to `relation`
unless `schema_infer` data clearly indicates the verb is being used as an
observation field — in that case, prompt the user to confirm intent.

| Field | Source | Current Usage | Proposed Picoschema |
|-------|--------|---------------|---------------------|
| `relates_to` | relation | 8% (3/35) | `relates_to?(array): Note, generic cross-reference` |

### Prescribed: Already Present (no-op)

| Field | Source | Note |
|-------|--------|------|
| `depends_on` | relation | Already declared — skipping |

### Fields to Remove (candidates only — exactly 0 uses)

| Field | Source | Usage | Current Picoschema |
|-------|--------|-------|--------------------|
| `benefit` | observation | 0% (0/135) | `benefit?(array): string, advantages` |

### Rare — keep, do not remove (in `dropped_fields` but still used)

| Field | Source | Usage |
|-------|--------|-------|
| `used_by` | relation | 9.85% (13/132) |

### Cardinality Fixes

| Field | Declared | Actual | Suggestion |
|-------|----------|--------|------------|
| `convention` | array | single | Keep array (forward-compatible) |

### Watch List (below 25%, observed at least once — not yet proposing)

| Field | Source | Usage |
|-------|--------|-------|
| `workaround` | observation | 18% (24/135) |
```

**Decision rules:**
- **Add** if in `new_fields` AND >= 25% usage. Always optional (`?`).
- **Prescribed Add** — present every `--prescribed` "to add" entry,
  regardless of frequency. Always optional (`?`). For a relation the default
  Picoschema is `<name>?(array): Note, <one-line description>` — the literal
  **capitalized** type `Note` is what marks a field as an entity reference.
  Never write `[[entity]]`, a bracketed form, or a lowercase type: Basic
  Memory treats any non-capitalized type as a scalar
  (`_is_entity_ref_type` requires `type_str[0].isupper()`), so the relation
  you meant to declare is silently registered as an **observation category**,
  `schema_validate` then hunts for a `- [<name>] ...` observation line that
  will never exist, and every later run sees the field at 0% and offers to
  remove it. For observations use `<name>?(array): string, <description>`.
  Suggest a description but prompt the user to refine it before applying.
  Always declare prescribed entries as `(array)` for forward compatibility.
- **Remove** ONLY when the entry's own `count` is exactly 0 **and** at least
  10 notes were analysed. Every other `dropped_fields` entry is rare-but-live
  — route it to the "Rare — keep" table, never to removal. Confirm with the
  user first. Even at a genuine 0%, do not propose removing a field this
  plugin's own conventions mandate (e.g. a relation verb an `intel` note
  template requires such as `built_with`, or a declared feature category such
  as `agent-leverage`) or one a sibling schema declares — a field can be
  load-bearing at 0% because it was just declared, or applies to a subset of
  notes. Flag those as "declared but unused this sample — not proposed for
  removal". **Removing a field used by even one note silently converts that
  note's observations into unmatched categories; every schema here is
  `validation: warn`, so `schema_validate` still reports the note as passing
  and the loss never surfaces.**
- **Cardinality**: default to keeping `array` unless > 90% single-value.
  `schema_diff` reports only prose strings and `schema_infer` exposes only a
  boolean `is_array` — neither yields a single-value percentage, so treat the
  90% bar as unmeasurable in practice and keep `array` unless the user
  directs otherwise.
- **Watch list**: below 25% usage but observed at least once — covers both
  the 10-24% band and any nonzero `dropped_fields` entry. Informational only.

Ask: "Apply these changes? (You can modify individual items before applying.)"

### Step 6: Apply to BM schema note

After approval, update the Basic Memory schema note using `edit_note` with
`find_replace`. Use `main/schema/<note_type>` as the identifier.

For adding fields, insert new Picoschema lines into the `schema:` frontmatter
block. Place observation fields among existing observations, relation fields
among existing relations. Treat prescribed additions identically to
drift-driven additions at this step — the only difference is provenance,
not the edit shape.

For removing fields, delete the Picoschema line from frontmatter.

Use one `edit_note` call per change for atomic, reviewable diffs.

**Before the first edit, keep the full pre-edit note text from Step 4.** It is
the only rollback available: `git checkout` restores the local mirror, nothing
restores the BM note.

Keep `find_text` inside the YAML `schema:` block (between `schema:` and the
next top-level key such as `settings:`) and never include the `---` markers.
Be precise about why: `UPSTREAM-basic-memory.md` records the trigger as
`edit_note(find_replace)` **on a schema note's frontmatter at all** — not
specifically as crossing the `---` boundary — with status Open and
`write_note(overwrite=True)` as the recorded reliable workaround. Staying
inside the block is a mitigation, not a proven fix.

**After each `edit_note`, re-read the note and confirm the frontmatter still
opens with a single `---`, still carries the `schema:` key, and still contains
every field you did not touch.** If it does not, stop immediately, restore the
note with `write_note(..., overwrite=True)` from the pre-edit text, and do not
proceed to Step 7.

### Step 7: Apply to local schema file

Update `schemas/<note_type>.md` with the same changes using the `Edit` tool.
The local file mirrors the BM note — changes to the `schema:` block must
match exactly.

### Step 8: Validate

Run `schema_validate` against the updated schema:

```
schema_validate(note_type="<note_type>", output_format="json")
```

Capture `warning_count` from a `schema_validate` run **before** Step 6, then
re-run here and compare. `passed` is true whenever `error_count` is 0 — it
ignores warnings entirely — so a removal that orphans real observations cannot
fail this check on its own.

- **`{"error": "No schema found ..."}`** — the schema note was corrupted by the
  edit. Restore it from the Step 6 pre-edit text via
  `write_note(..., overwrite=True)`, then re-run. Do NOT report this as a
  pre-existing issue
- **`warning_count` rose** — a removal orphaned observation categories or
  relation verbs in real notes. Report the delta explicitly and offer to
  restore the removed fields
- **`error_count` rose** — list the failures
- **Unchanged** — report success with counts
- **Schema invalid** — report the validation error. Do not auto-revert
  silently; the local file can be undone via `git checkout schemas/<type>.md`,
  but that does NOT restore the BM note — use the pre-edit text for that

### Step 9: Report results

```markdown
## Schema Evolution Complete: `<note_type>`

### Changes Applied
- Added N fields (drift-driven): `field1`, `field2`
- Added P fields (prescribed): `verb_a`, `verb_b`
- Skipped Q prescribed entries (already present): `verb_c`
- Removed M fields: `field3`

### Files Modified
- BM schema note: `main/schema/<note_type>`
- Local schema: `schemas/<note_type>.md`

### Validation
- N notes validated, M passed

### Watch List for Next Evolution
- `field_x` at 18% — revisit when it crosses 25%
```

Remind the user to commit the local schema file change.
