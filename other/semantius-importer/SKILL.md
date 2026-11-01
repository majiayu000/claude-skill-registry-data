---
name: semantius-importer
description: >-
  Imports a CSV into Semantius: maps its columns to field formats, diffs them
  against an existing entity, optionally creates the entity (and its module),
  and bulk-loads the rows with a Bun script. Also schema-only runs (no rows)
  and compare-only runs (no writes). Trigger on "import this CSV", "load this
  CSV into semantius", "create an entity from this CSV / spreadsheet export",
  "introspect this CSV", "bulk load these CSV rows", "does this CSV match our
  table?", "export the orders table to CSV", or asking what entity shape a CSV
  implies. Do NOT trigger for JSON transfer files (from `export_entities` /
  `export_module`), moving modules or tables between hosts, backups or
  restores (semantius-transfer), deploying blueprints or specs
  (semantius-admin / semantius-modeler), designing a multi-entity system
  (semantius-architect), or CSV work with no Semantius target.
  For xlsx, ask for a CSV export first; CSV-only.
---

# semantius-importer Skill

## Execution context (mandatory, read before anything else)

**This skill is interactive and MUST run in the conversation the user is in.**

- Do NOT start this skill, or any of its stages, in an agent that another agent started to run on its own (a background worker, subagent, executor, or Task). Those agents cannot ask the user questions, so they cannot run this skill correctly. Running in the cloud is fine when the user is talking to that agent directly.
- Do NOT write a delegation prompt that tells another agent to run this skill, "build and deploy end to end", or "make the decisions yourself".
- If you cannot call a tool that asks the user a question and waits for the answer, STOP at once. Make no writes. Report back: "This skill is interactive and must be run in the user's conversation." Muse chat is the exception: there you ask in chat text and the tap picker, so do not stop; follow the question-format step of the shared preflight. For dot, OpenAI's personal assistant, and other similarly limited tools without a supported interactive question tool, do not stop: read `../semantius-admin/references/dot-questions.md`, ask questions in chat, and wait for the user's reply before continuing.
- An agent's general habit of delegating long or multi-step work does not apply here. This rule overrides it.

**What may be delegated:** only steps that ask nothing and change nothing the user has not confirmed.

The front door for getting a **file** into Semantius. One CSV in, one entity out (created or reused), rows loaded in batches. The pipeline skills (architect → analyst → modeler) design and deploy whole systems from specs; this skill deliberately does lightweight, single-entity creation driven by what a file actually contains — no blueprint, no catalog reconciliation machinery.

Division of responsibility:

- **This skill** owns the workflow: introspect → map → detect → decide → import → verify, and the decision points along the way.
- **use-semantius** owns every low-level operation (CLI syntax, payload shapes, response contracts, Golden Rules). Loaded at Step 0; it wins on any conflict.

## Operating modes

Pick from the user's phrasing; ask once when ambiguous.

| Mode | Runs | Writes |
|---|---|---|
| **Full import** (default) | Stages 1–6 | catalog (as decided) + data |
| **Schema-only** — "just create the entity from this file" | Stages 1–4, stops after catalog writes | catalog only |
| **Compare-only** — "does this file match our entity?" | Stages 1–3, renders the classified diff report | **zero writes** |

In every mode, each decision branch that would modify an existing entity carries an explicit **"report only, do not update"** option. Comparing never forces updating.

## Writing conventions (apply to every user-facing output)

Self-contained — no other skill file needs to be read for these. They govern chat output, `AskUserQuestion` text, plans, and reports; they never apply to data payloads bound for Semantius.

1. **US English spellings, always**: optimize, behavior, customize, organization, analyze — never the British forms.
2. **No em-dashes (`—`) in chat output.** Use a comma, parentheses, a semicolon, or two sentences instead. (Skill and reference files may use them; the ban is on what the user reads in chat.)
3. **Plain language.** Say "table", "field", "row", "the file" — never internal jargon (csvschema verdict, disposition, mapping artifact) without a plain-English gloss.
4. **Narration restraint.** Never announce what you are about to do ("Let me read...", "Now let me check..."). Do the work; render only the decision points and the final report. Play-by-play between tool calls is noise. A file write is an error only when a tool call failed: a file saved cleanly through a shell heredoc or a script is not one. On success, say nothing about how the file was written; on a real failure, quote the tool's error verbatim and stop.
5. **Data is sacred.** CSV values travel into Semantius byte-for-byte except for the coercions the mapping explicitly declares; house style (spelling, dash policy) is never applied to payloads, titles, or enum values derived from the file.

6. **`AskUserQuestion` fires alone.** Apply mapping edits, re-renders, and task updates first, in earlier steps, then call `AskUserQuestion` as the only tool call of its response; a sibling tool call in the same response cancels the pause and the run continues before the user has answered. The answers arrive as a `<user_answers>` input block keyed by question text; there is no `user_answers` tool, never call one.
   **Option count is 2 to 4 per question object, never 1 and never 5**; the tool rejects the whole call otherwise, including every other question in it. When the options come from data (one per column, candidate table, module), shape the list before firing: a single-select pick list shows at most the 3 best candidates (2 when two fixed options must stay) plus the stage's fixed alternative ("Create new", "Skip"), and the question text says another can be written in (the tool always adds its own free-text slot, so never list an "Other" option); a multiSelect with more than 4 items becomes several question objects with the same header and the text suffixed ` (<i> of <N>)`, each holding 2 to 4 items (5 → 3 + 2, never 4 + 1); exactly 1 item with no fixed alternative means no question (the one item counts as chosen). Never pad with a filler option, never merge two items into one option. The tool has no pre-checked option; "(Recommended)" on one label is the only default marker.
7. **Task tracking and the question ledger.** The harness task tools (`TaskCreate` / `TaskUpdate` / `TaskList` / `TaskGet`) track the run and the open questions. Full mechanics: [`../semantius-admin/references/task-tracking.md`](../semantius-admin/references/task-tracking.md). The importer's part, in short:
   - **Stage tasks.** At Step 0, `TaskList`, then `TaskCreate` the stage tasks from the Workflow table below (subject verbatim, `activeForm` = subject), all `pending`, then, in the same response, one `TaskUpdate` per task (`addBlockedBy: [<previous task id>]` for every task after the first; `status: in_progress` for the first; under the admin also `addBlocks: [<the in-progress unprefixed pipeline task id from TaskList>]`); a compare-only run creates only the first two, schema-only the first three. One `in_progress` at a time; `completed` when the stage's mandatory commands ran; a halted stage stays `in_progress` with `halted: <reason>` in its description. Never a task for preflight, workspace setup, or `bun add`.
   - **Ledger stages: 2, 3, 4.** Every question those stages ask is a `Q:` task first (subject = `Q: ` + the exact question text, one task per question object, description = header, options with the Recommended default, `Decides:`, `Recorded in: <mapping.json path>`), created all at once at the start of the stage (E) and gated in one call — `TaskUpdate` the stage task with `addBlockedBy: [<every Q: task id>]` — so the stage shows as blocked while any question is open, asked in batches of up to four per call (B then A), and completed only after the answer is in `mapping.json` (R). Standalone, no ledger task: the mode question (Operating modes), the previous-run-folder question (Stage 2), the single pre-write gate (Stage 4). `TaskList` clean of open `Q:` tasks is a mandatory command of Stages 2, 3, and 4 (checklist below); no plan render, dry run, or write happens while a `Q:` task is pending or in progress.
   - **`Q:` templates** (fill the placeholders, never reword): `Q: Mark <Field> as unique so re-running this import skips rows that are already there?`; `Q: <Header>: keep it as a fixed list of choices, or store it as free text?`; `Q: <Header> was read as <format>. Keep <format>, or change it?`; `Q: Empty cells in <Header>: store zero, or leave them blank?`; `Q: These columns clash with names the platform reserves: <list>. Rename them, or skip them?`; `Q: Which column should name each row?` (options: the 2 to 4 best-ranked string columns; when more than 4 qualify the text ends with ` The 4 best candidates are listed; type another header if you prefer.`); `Q: <Header> looks like a link to <Table>. Connect it?`; `Q: Create a new table <name>, or load into an existing one?` (options: `Create a new table <name>` plus at most 3 existing candidates, label `Load into <Plural Label> in <Module>`; when more than 3 were found the text ends with ` The 3 closest are listed; type another table's name if you prefer.`; with zero candidates the question does not fire and the create path is taken); `Q: <Table> is missing <N> of the file's fields. Add them, drop those columns, report only, or stop?`; `Q: <Field> in <Table> does not match the file (<live> vs <file>). Change the field, convert while loading, drop the column, or report only?` (4 options, 3 when changing the field is classified impossible; to abort the run the user types "stop" into the free-text slot, which halts exactly like a "stop" option); `Q: <Field> is required in <Table> but not in the file. Fill a constant for every row, make it optional, or stop?`; `Q: Which module should <Table> live in?` (options: at most 3 existing modules, the ones whose names are closest to the table or the file, plus `Create a new module called <name>`; when more modules exist the text ends with ` The 3 closest are listed; type another module's name if you prefer.`; with zero existing modules the question does not fire and the module is created).

---

## Preflight (before Step 0, every invocation)

The shared environment checks live in **[`../semantius-admin/references/preflight.md`](../semantius-admin/references/preflight.md)**; do not duplicate them. Standalone summary: install the toolchain if missing, probe `getCurrentUser` to confirm the CLI is authenticated. This skill runs from wherever the user's CSV work happens; it needs no repository and makes no assumptions about one. This skill critically needs **Bun** (the import script runs with `bun run`); `jq` is convenient but optional; `yq` and the customizations file are not used.

**Nothing about preflight reaches chat:** not the checks, not whether a `Run context:` block is present (under the admin or on your own), not the org, not the customizations path. The user sees only the setup and halt lines the shared preflight's Output discipline names.

Preflight check 1 (**never `cd`**) binds this skill's helper scripts too, not only bare `semantius` commands: `create-fields.ts` and `import.ts` spawn `semantius call crud …`, a child process inherits the shell's cwd, and the CLI reads `.env` from that cwd. So every helper is run **from `<cwd>` by path** — `bun run <run-folder>/<helper>` with `<run-folder>` = `.tmp_import/run-<ts>` — never from inside the run folder; the one step that needs the run folder as its working directory is the dependency install, done as `bun add --cwd <run-folder> csv-parse`. Run from inside the run folder, the CLI never reads the session's `.env`: every field create and batch insert either fails with an auth error (exit 5) that reads like a CLI bug, or, worse, lands with whatever the global `.env` or the current host supplies. Mechanics and rationale: import-script-template.md → Workspace layout.

Also confirm the CLI ships the introspection util: `semantius info utils` must list `get_csvschema`. If it is missing, re-run the installer first.

## Step 0 (hard gate): load the essentials

**Blocking prerequisite, not a suggestion.** Do not issue a single `create_*` / `update_*` and do not start the import until you have read:

```
Read: references/importer-essentials.md
```

Also at Step 0, once the operating mode is known: `TaskList`, then create the stage tasks for that mode (writing convention 7; subjects from the Workflow table) and set the first one `in_progress`.

That file is the distilled subset of `use-semantius` this workflow needs: CLI forms, exit codes, response shapes, the three catalog writes, `postgrestRequest`, deep links. It is a distillation, not the authority — **use-semantius wins on any conflict** — and the full references are consulted **on demand**, not up front: `../use-semantius/references/data-modeling.md` for FK modeling depth, RBAC beyond the module's two standard permissions, or schema-evolution risk; `../use-semantius/references/crud-tools.md` for PostgREST syntax beyond the essentials; `../use-semantius/references/cli-usage.md` for exotic CLI forms and chaining.

### Safety-net cheat table (a backstop, never a substitute; use-semantius wins)

| Trap | Right behavior | Authoritative source |
|---|---|---|
| Read response shape | `crud` reads return a JSON **array**; exit `0` + `[]` means "found nothing". Pass `--single` on unique-key reads: bare object, exit `1` = none, `2` = ambiguous | use-semantius SKILL.md → Response handling |
| Mandatory fields | There is **no `required` column**: mandatory = `input_type: "required"`, unique = `unique_value: true`. Never send `is_nullable` | data-modeling.md → All Field Properties |
| Nullability | Computed from `format`: only `reference`, `date`, `date-time` accept NULL; everything else is NOT NULL with an auto-default. Drives the empty-cell policy | data-modeling.md |
| `postgrestRequest` payload | The record field is **`body`**, not `data`. Bulk insert = array body where **every object has the same keys** (else `PGRST102`; raw PostgREST, no `missing=default`). The typed `create_*` tools have no such constraint | crud-tools.md → Bulk insert / Bulk operations |
| Several records of one kind | **One call, never a loop**: every typed `create_*` takes `data` as an array (items may differ in keys; one transaction, all-or-nothing; the response is always an array), `update_*` / `delete_*` take an `id` array. Both baseline permissions in one `create_permission`, every new field in one `create_field` (the copied runner does this). `--single` is rejected with an array | use-semantius SKILL.md → Golden Rules (batching); crud-tools.md → Bulk operations |
| Create response ids | Never read the new row's id off the create response; re-read by the identifying field (`table_name`, `field_name`, ...) | use-semantius SKILL.md |
| `update_field` identifier | Composite id string: `{"id": "<table>.<field>", "data": {...}}`; payload carries only the changing keys | data-modeling.md → Updating and Deleting |
| `update_entity` identifier | Keyed by `table_name` at top level, not numeric id | data-modeling.md |
| Big payloads | Pipe JSON via stdin (`... | semantius call crud postgrestRequest`); the CLI reads stdin when no JSON argument is given. The "always pass inline JSON" warning is about interactive shells with an empty stdin, not scripts that pipe | cli-usage.md → Passing Arguments |
| Format vocabulary | `enum` (with `enum_values`), never `select`; monetary values are `number` + `precision`; a 0–5 judgment is `rating` | data-modeling.md |

---

## Workflow

```
1. Introspect → 2. Map & review → 3. Detect & diff → 4. Decide & create → 5. Run import → 6. Verify & report
```

Read **[`references/schema-mapping.md`](references/schema-mapping.md)** and **[`references/import-script-template.md`](references/import-script-template.md)** (workspace and helper mechanics) before Stage 2.

**Stage tasks and per-stage command checklist.** The prose below governs the details; this table is the completeness gate. A stage counts as run only when its listed commands actually ran — substituting a variant call (e.g. a bare `read_entity '{}'` in place of Stage 3's `--single` read plus the overlap sweep) is skipping the stage, not running it. The Task subject column is the exact `TaskCreate` subject (writing convention 7). Every `bun run` below is issued from `<cwd>` with the helper's path (`<run-folder>` = `.tmp_import/run-<ts>`), never after a `cd` into the run folder (Preflight).

| Stage | Task subject | Mandatory commands |
|---|---|---|
| 1 Introspect + 2 Map & review | `Import › Read the file and review the field mapping with you` | `semantius call utils/get_csvschema '{"path": "<csv>"}'`; the canonical setup block (import-script-template.md → Workspace layout): mkdir + all four copies under **final names** (`import.template.ts` → `import.ts`) + `bun add --cwd <run-folder> csv-parse`; the ledger: `TaskCreate` every open mapping question (E), then batches of `bun run <run-folder>/render-plan.ts` + `AskUserQuestion` (B / A / R) after every mapping-edit round; finally `TaskList` with no `Q:` task pending or in progress |
| 3 Detect & diff | `Import › Check for a matching table` | `read_entity --single '{"filters":"table_name=eq.<table>"}'` + `read_field '{"filters":"table_name=eq.<table>"}'`; on absent entity additionally `read_entity '{}'` (name sweep) **and** `read_field '{"filters":"field_name=in.(<mapped field names>)"}'` (overlap sweep), then the create-vs-reuse question as a `Q:` task; `TaskList` clean before the diff report |
| 4 Decide & create | `Import › Decide and create what is missing` | the decision-table questions as `Q:` tasks; `TaskList` clean; catalog writes per decision; `bun run <run-folder>/create-fields.ts --dry-run` (pre-write gate), then `bun run <run-folder>/create-fields.ts` (one bulk `create_field` call) |
| 5 Run import | `Import › Load the rows` | `bun run <run-folder>/import.ts <absolute-csv-path>` (`import.ts` exists since the Stage 2 setup block) |
| 6 Verify & report | `Import › Verify and report` | spot-read `postgrestRequest` GET with `select=<id_column>,<label_column>,<sample fields>` — never `select=label`; every probe result, including errors, goes into the report |

### Stage 1 — Introspect

```bash
semantius call utils/get_csvschema '{"path": "<csv-path>"}'
```

Default `maxRecords: -1` scans the whole file (streaming; large files are fine). **Do not cap the scan** unless the user insists: a capped scan degrades format verdicts (low-cardinality columns collapse to `enum`) *and* silently suppresses id detection. The result returns the schema inline and writes `<file>.csvschema.json` next to the CSV — keep it, the import workspace copies it. On an error envelope (`FILE_NOT_FOUND`, `EMPTY_FILE`, `NO_HEADER_ROW`, `PARSE_ERROR`, ...), surface the message and stop.

The schema is a wrapper: `{id_mode, id_move_column?, record_count, fields}`. Record three things: `record_count` (the import's expected parsed-row count on a full scan), `id_mode` (drives the id decision in Stage 2), and each column's verdict from `fields`. The full output contract and its detection quirks are in schema-mapping.md section 1.

### Stage 2 — Map and review

First create the run workspace with the **canonical setup block** (import-script-template.md → Workspace layout): `<cwd>/.tmp_import/run-<timestamp>/` (a scratch folder under the current working directory — never `$TMPDIR` / `/tmp/` / `$env:TEMP`, which a sandbox restart can wipe mid-run), then all four copies under their **final names** — the `.csvschema.json`, `render-plan.ts`, `create-fields.ts`, and `references/import.template.ts` copied **as `import.ts`** (the rename happens here at setup, never in Stage 5) — and `bun add --cwd <run-folder> csv-parse`. The shell stays in `<cwd>` throughout; the run folder is only ever addressed by path (Preflight, check 1). If a previous run folder for the same table exists, offer to reuse and reconfigure it instead. The mapping lives in that folder as `mapping.json` from the first proposal on.

Apply schema-mapping.md sections 2–7 to produce the proposed mapping:

- format passthrough (the CLI vocabulary is aligned; unlisted formats flow through verbatim per the fallback rule) plus the `multiline` naming heuristic;
- **enum review** for every `enum` verdict (low-cardinality columns masquerade as enums; a 1–5 rating column is offered as `rating`);
- **the id line** (schema-mapping.md section 4): `id_mode` applies to the **new-entity path only** — report the detection ("this file carries a usable primary key" / "the first column is an id candidate"), then apply the **classic policy**: id-named column renamed to `external_id` (offered as the unique key, below), an `id_move_column` kept as its own integer field. Importing source ids into a newly created entity's primary key is **deferred** (design and roadmap in the README; the `fix_id_sequence` RPC it needs now ships with the platform, but re-enabling preservation still needs its own plan). For an **existing target entity**, `id_mode` is ignored; the live `id_column` drives the collision policy and the payload guard;
- **the unique-key question** (schema-mapping.md section 4): when the file carries a column that identifies each row (a source system id, a code, an external reference), ask **once**, in plain words, whether to **mark that field unique** so re-imports cannot create duplicates: *"`<Header>` looks like a unique id from the source. Mark `<field>` as unique so re-running this import skips rows that are already there?"* with two options — **Unique** (Recommended: `unique_value: true` on the field; the import skips rows whose value already exists) / **Not unique** (plain insert; re-running the file inserts every row again). Never say "natural key" to the user; that is only the internal `mapping.json` name (`natural_key`) for the field the script dedupes on. Never offer an "update existing rows" option: **updating existing records is postponed** (README → Postponed), the import is insert-only;
- field-name verification, digit-leading renames, and **reserved-column resolutions** (`created_at`, `updated_at`, `label`);
- **FK candidates** (only with a live target and user confirmation);
- **label column** proposal (new entities);
- empty-cell policy per column; the util's `input_type` proposals (downgradeable).

Write the proposal as `mapping.json` (schema-mapping.md section 8) and render it with the helper: `bun run <run-folder>/render-plan.ts` prints the mapping table (raw header → field → format → extras → empty-cell rule → disposition → notes) and a facts block with every count. **Paste the helper's output; never restate a number in prose that the helper did not print** — the artifact is the single source of truth for the table, the plan, and what executes, so counts can never drift between what was said and what was done. Add the id-handling line beside it.

Then run the **review loop through the question ledger** (writing convention 7; sequence in `task-tracking.md`):

1. **Enumerate (E).** Walk the proposal once and `TaskCreate` a `Q:` task for every open decision (then one `TaskUpdate` on this stage's task with `addBlockedBy: [<every Q: id just created>]`), using the templates in convention 7: the unique-key question; one per `enum` verdict that needs review; one per proposed format deviation from the csvschema verdict (introspected format as the default; there should be none unless the user asked); the zero-for-empty question per affected column or one for all when the rule is the same; ONE task listing every reserved-column collision; the label-column question (new entities); one per FK candidate (only with a live target). One question per **open decision**: a column with nothing to decide gets no question, the reserved-column collisions are always grouped into one, and there is never a blanket "confirm this column" pass over every column. Nothing else in that response. Self-check: the number of `Q:` tasks equals the number of open decisions you enumerated.
2. **Batch (B).** `TaskList`; take up to four pending `Q:` tasks; `TaskUpdate` them `in_progress`; when a previous round changed `mapping.json`, run `bun run <run-folder>/render-plan.ts` in this same response and paste its output.
3. **Ask (A).** `AskUserQuestion` alone in its own response (never in the same response as an `edit`, `bash`, or `TaskUpdate` call).
4. **Record (R).** For each answer: apply it to `mapping.json` first, then `TaskList` and `TaskUpdate` the task `completed` with `Answer: <value>`. A free-form request in the reply (rename a field, drop a column, change the id decision, pick a different label column) is applied to `mapping.json` directly; if it opens a new decision, it becomes a new `Q:` task. Then `TaskList`: any `Q:` task pending or in progress → this response is also the next B; none → run `bun run <run-folder>/render-plan.ts` one last time, paste it, and Stage 2 is complete when that render draws no further edit request.

Format is **not** free to change silently: every deviation from the introspected csvschema verdict (schema-mapping.md section 2) is a `Q:` task with the introspected format as the default, never folded into the mapping on the skill's own judgment. If the approved mapping ends up differing from the csvschema verdict on any `format`, that decision must trace to a completed `Q:` task's answer, not skill inference.

The approved `mapping.json` is final: every later stage (pre-write plan, field creation, import) executes exactly what it says, nothing more.

### Stage 3 — Detect and diff

Derive the candidate `table_name` (plural snake_case) from the user's phrasing or the file name; when ambiguous, confirm it as a `Q:` task (this stage is a ledger stage). Then:

```bash
semantius call crud read_entity --single '{"filters": "table_name=eq.<table>"}'
semantius call crud read_field '{"filters": "table_name=eq.<table>"}'
```

- **Entity absent** (exit 1): do **not** silently take the create path. Sweep for plausible existing targets two ways: name similarity from `read_entity '{}'` (table names containing the derived name or its singular/plural variants, similar labels), and **field overlap** in one query — `read_field '{"filters":"field_name=in.(<mapped field names>)"}'` grouped by `table_name` and ranked by overlap count. Then the create-vs-reuse `Q:` task (`Q: Create a new table <name>, or load into an existing one?`; `multiSelect: false`; options: **`Create a new table <derived table>`** plus **at most 3 existing candidates** (label `Load into <Plural Label> in <Module>`, description = the overlap count and the matching field names), so 2 to 4 options; when more than 3 candidates were found the question text ends with ` The 3 closest are listed; type another table's name if you prefer.`; mark "(Recommended)" on the top-ranked candidate when its overlap covers more than half of the mapped columns, otherwise on the create option; the user types any other table's name into the tool's free-text slot, never list an "Other" option), asked and recorded per the ledger sequence. When the sweep finds **zero** candidates the question does not fire (a 1-option question is rejected by the tool): take the create path; the Stage 4 pre-write gate still shows the new table before anything is written. Choosing an existing entity continues below as "entity exists"; choosing create marks the Stage 4 create path.
- **Entity exists** (or an existing target was chosen): capture the entity's **`id_column`** from the `read_entity` result (default `id`, but customizable — it drives the reserved-name rules and the script's payload guard; never assume the literal `id`), then diff the approved mapping against the live fields into the four buckets of schema-mapping.md section 9 (matched / missing live / mismatched / extra live), classify every needed change as **possible** or **impossible**, and render the classified change report. Never target the `id_column` field, live fields with `input_type` `readonly` / `disabled`, nor `_label` / `<fk>_label`.

**Compare-only mode ends here**: the classified report is the deliverable, zero writes (`TaskList` clean of `Q:` tasks before the report, then the stage task `completed`).

### Stage 4 — Decide and create

The "Decision" column below is the ledger for this stage: at the start of Stage 4, enumerate every row that applies into `Q:` tasks (convention 7 templates: missing fields, mismatched fields, required-but-absent fields, module pick), ask them in batches of up to four, record each answer in `mapping.json` (dispositions, coercions, constants) before completing its task, and only when `TaskList` shows no open `Q:` task move on to the writes and the pre-write gate. Rows marked "confirmation gate only" ask nothing here.

| Live state | Default plan | Decision |
|---|---|---|
| Entity exists, everything matched | reuse as-is, import only | confirmation gate only |
| Entity exists, missing fields | add them via `create_field` | ask: add fields / drop those columns / report only / abort |
| Entity exists, mismatched fields | per the possible-vs-impossible classification | ask per report: `update_field` (only when classified possible) / coerce-in-script into the live format / drop / report only (4 options at most; "stop" is written into the free-text slot and aborts) |
| Entity exists, extra live **required** fields not in the CSV | blocker | ask: constant value for all rows / make the field optional / abort |
| Entity absent, target module known | create the entity there | confirmation gate only |
| Entity absent, no module | create the module first | ask: at most 3 existing modules from `read_module '{}'` (closest names to the table or file) / create a new one (2 to 4 options; another module is written into the free-text slot; zero existing modules: no question, create it) |

Creation order (mechanics in data-modeling.md, `read_*` before every `create_*` so a re-run never double-creates):

1. Module (when needed): `create_module`, then `<slug>:read` + `<slug>:manage` permissions in **one** `create_permission` call (`data` is an array of the two rows), then `update_module` to wire `view_permission` / `manage_permission` (both take the permission name).
2. Entity: `create_entity` with `table_name`, symmetric `singular_label` / `plural_label`, description, **`label_column`** (the platform auto-creates that field and the computed `label` field), `module_id`, `view_permission`, `edit_permission`.
3. Fields: run `bun run <run-folder>/create-fields.ts` from `<cwd>` (by path, never after a `cd`; the runner spawns `semantius call` and the CLI must keep reading the session's `.env`) — it creates every `disposition: "create"` column from `mapping.json` in **one bulk `create_field` call** (`data` is an array of all the field objects; up to 100 per call, so a wide file is at most a few calls; items may differ in keys — `enum_values` here, `precision` there — the typed tool handles that) in the mapping's column order and without `field_order` (the platform appends new fields in array order, so the CSV order is the display order; `field_order` goes on a column only when the user asks for a specific position, never as a default, since a hand-picked value can tie with the label field at 20), skips field names that already exist live (read-before-create, so a re-run never double-creates), **retries transient failures** (exit 3: up to 3 retries per call with 1s/3s/9s backoff, re-reading the live fields before each retry so rows that landed are never resent), and **fails fast and loud on real errors** (exit 4 validation / exit 5 auth, never retried): a bulk call is one transaction, so a failed call landed nothing — every field of it is reported `failed` with the platform's first stderr line, later calls are `not-run`, non-zero exit; on success it re-reads the live fields and asserts every requested name is present. Never hand-roll a shell loop for field creation — ad-hoc loops swallow errors, and one call per field is against the platform's batching rule anyway. The label column (`disposition: "label"`) and skipped columns are never created. When the label field deserves a more specific title than `singular_label`, follow up with `update_field` on that field's `title` (importer-essentials.md).

**Insert-only.** The import never modifies existing rows; updating existing records from a re-import is **postponed** (README → Postponed) and must not be offered, planned, or reported. With a unique key set (`natural_key` in `mapping.json`, `unique_value: true` on that field), rows whose key value already exists are skipped; without one, every run inserts every row. On an existing target entity whose chosen key field is not unique live, say so plainly and offer making it unique via the possible-change classification (`update_field` with `unique_value: true`, which fails loudly when live duplicates exist) or import without a unique key.

**One pre-write confirmation gate** (`AskUserQuestion`, never a y/n asked in chat text; a standalone question, not a ledger task): render the complete numbered plan — module ops, entity, each field, planned alterations, then the import (rows and batches) — and get one approval before the first write. Precondition: `TaskList` shows no `Q:` task pending or in progress (every Stage 2-4 decision recorded); an open one means back to the ledger, not to the gate. Run the helpers in an earlier step; the gate's `AskUserQuestion` is the only tool call of its response. Every number and field line in the plan comes from the helpers, not from prose arithmetic: `bun run <run-folder>/render-plan.ts` for the mapping table and counts, `bun run <run-folder>/create-fields.ts --dry-run` for the exact `create_field` payloads. The per-topic decisions above happen during analysis; the gate is a single yes.

**Schema-only mode ends here** after the catalog writes, reporting what was created plus the deep link.

Payload hygiene: any payload carrying free text from the CSV or the user (descriptions, titles, enum values) goes through a Bun script or stdin pipe, never inline shell-quoted JSON (see the modeler's data-fidelity rules; same reasoning).

### Stage 5 — Run the import

The workspace, mapping, and dependencies already exist from Stage 2. Per **[`references/import-script-template.md`](references/import-script-template.md)**:

1. `import.ts` already sits in the run folder — the Stage 2 setup block copied `references/import.template.ts` to that final name, **byte-for-byte, never retyped or edited per run** (no placeholders; it reads all run configuration from `./mapping.json` at startup). If it is missing, re-run that one copy line; never re-author the file.
2. `bun run <run-folder>/import.ts <absolute-csv-path>`, issued from `<cwd>` (the script spawns `semantius call` per batch; run from inside the run folder, it misses the session's `.env`, see Preflight): streaming parse, coercion per mapping, uniform-key batches via stdin-piped `postgrestRequest`, exit-code-aware retries, `failed-batches.json` capture, unique-key dedupe (rows already present are skipped; existing rows are never modified), built-in count verify.

### Stage 6 — Verify and report

The script already count-verifies and emits `import-summary.json`. The skill then:

1. Checks `parsed` against the introspection's `record_count` (full-scan runs): a mismatch is a parsing defect to surface (delimiter trouble, embedded newlines), not noise.
2. Spot-reads 2–3 imported rows (`postgrestRequest` GET with `select=<id_column>,<label_column>,<a few mapped fields>`) and eyeballs the coercions: booleans are `true`/`false`, dates are dates, enums carry expected values, the **label column field** carries the expected values. **Never `select=label`**: the computed `label` field is a read-time projection, not a PostgREST column — that probe fails with `42703` (verified live).
3. Renders the final report: parsed / inserted / skipped / failed, the count-verify verdict, the path to `failed-batches.json` when failures exist (with the first error quoted verbatim), and what was created in the catalog.
4. Closes with a clickable deep link to the entity list: `[Open <Plural Label> in Semantius →](<ui_baseurl>/<module_slug>)` — read `ui_baseurl` as a discrete field from `getCurrentUser`, never derive it from `api_baseurl`.

**Probe errors are findings.** A verification probe that returns an error — any non-zero exit or error body — goes into the final report verbatim, with that check marked **failed** or **not verified**. It is never reasoned away, and no prose may claim a check passed whose probe errored: a check either ran and passed, or its error is quoted. ("The probe failed but it's probably fine" is exactly the failure this rule exists to prevent.)

A failed batch is loud: the run is reported as incomplete with the re-run instruction (fix the cause and re-run; with a unique key set, rows that already landed are skipped, otherwise a re-run duplicates them). Never render a success-shaped summary over a partial import.

---

## Download as CSV

For a spreadsheet copy of a table; a CSV is not re-importable with its ids, references and schema. Anything that must be restored or moved to another host is a JSON transfer file from `utils/export_entities` (the `semantius-transfer` skill). PostgREST serves CSV directly. `postgrestRequest` has no header override, so for a CSV download use the raw endpoint with the CLI's token, or simply deliver JSON-to-CSV via a few lines of Bun:

```bash
semantius call crud postgrestRequest '{"method":"GET","path":"/products?select=product_code,list_price&order=product_code"}' \
  | bun -e 'const r=await new Response(Bun.stdin.stream()).json();const k=Object.keys(r[0]??{});console.log([k.join(","),...r.map(o=>k.map(c=>JSON.stringify(o[c]??"")).join(","))].join("\n"))' > products.csv
```

Filters, column selection, and pagination follow the normal PostgREST syntax from crud-tools.md.

## This skill never

- deletes anything in the catalog (`delete_entity`, `delete_field`, `delete_module`, ...) — cleanup of test or mistaken imports is the user's explicit call;
- models multi-entity systems, junction tables, or RBAC beyond the module's two standard permissions — route to `semantius-architect`;
- writes sample or probe records outside the import itself;
- edits files it did not create this run (the CSV stays untouched);
- imports into `users` or other platform built-ins.
