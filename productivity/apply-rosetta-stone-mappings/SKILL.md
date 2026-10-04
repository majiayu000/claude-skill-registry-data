---
name: apply-rosetta-stone-mappings
description: |
  Apply a set of Rosetta Stone attribute mappings to a Narrative
  dataset by wrapping them in a one-shot workflow that calls the
  `CreateRosettaStoneMappingsIfNotExist` task. Consumes the structured
  output of `/generate-rosetta-stone-mappings`, normalizes the
  generator's snake_case to the workflow task's camelCase, re-validates
  every expression against the dataset's current schema, gates on
  user approval, submits via `narrative_workflows_create`, polls the
  triggered run, and reports per-mapping created / conflict / failed.
  Use when: "apply these mappings to dataset N", "create the
  Rosetta Stone mappings I just generated", "push the mappings I
  saved earlier to <dataset>", "productionize this mapping list",
  "submit the suggested_mappings array".
  (narrative-common)
license: MIT
compatibility: >-
  Requires the narrative-mcp MCP server and local file Read. Recommends
  AskUserQuestion — a Claude Code primitive with a prose fallback in
  references/HARNESS_FALLBACK.md. Uses the harness waiting tools (job_monitor / wait_for / sleep) when
  present, and paced status checks when not. Portable to any agentskills.io-compliant
  harness via the documented fallbacks.
metadata:
  version: 0.3.8
  narrative:
    args:
      - name: "--dataset"
        value: "<id|name>"
        required: false
        description: >-
          The target dataset's numeric ID or its datasetName (alphanumerics
          + underscores). Required before submission; if omitted, the skill
          asks.
      - name: "--from"
        value: "<path>"
        required: false
        description: >-
          Path to a JSON file containing the mappings input (see
          references/INPUT_FORMAT.md). Mutually exclusive with --mappings.
      - name: "--mappings"
        value: "<json>"
        required: false
        description: >-
          Inline JSON string with the mappings input. Useful when invoked
          programmatically from /generate-rosetta-stone-mappings.
      - name: "--allow-partial / --no-allow-partial"
        required: false
        default: true
        description: >-
          Sets the task's allowPartial flag — when true, individual mapping
          failures don't abort the others.
      - name: "--data-plane"
        value: "<id>"
        required: false
        description: "UUID of the data plane to target. Skips data-plane resolution."
      - name: "--dry-run"
        required: false
        description: >-
          Render the full spec, re-validation results, and the create-call
          parameters; do NOT submit. Implies --show-spec.
      - name: "--show-spec"
        required: false
        description: >-
          Include the full rendered workflow YAML in the approval preview.
          Off by default — most users only need the plain-English summary.
      - name: "--no-trigger"
        required: false
        description: >-
          Submit the workflow but do not pass trigger_immediately: true. The
          user must trigger it manually later (rare).
      - name: "--no-revalidate"
        required: false
        description: >-
          Skip Phase 5 NQL re-validation. Intended for same-conversation
          hand-off from /generate-rosetta-stone-mappings. Do NOT pass when
          the input is from a file, a paste, or a prior conversation — the
          schema may have drifted.
    requires:
      tools:
        - Read
      mcp-servers:
        - narrative-mcp
      mcp-tools:
        - narrative_context_get
        - narrative_context_search_companies
        - narrative_context_set_company
        - narrative_datasets_describe
        - narrative_data_planes_list
        - narrative_nql_validate
        - narrative_workflows_create
        - narrative_workflow_runs_list
        - narrative_workflows_describe
    recommends:
      skills:
        - narrative-common:generate-rosetta-stone-mappings
      tools:
        - AskUserQuestion
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

# Apply Rosetta Stone Mappings

## Persona

You are a release engineer who turns a vetted mapping list into a
production change against a Narrative dataset. You optimize for:

1. Fidelity — every mapping submitted is byte-for-byte the one the
   user approved; no silent rewrites of expressions or attribute IDs.
2. Pre-flight safety — every expression is re-validated against the
   dataset's *current* schema before the workflow is rendered.
3. Transparency — the user sees a plain-English summary of what
   will be applied and approves it explicitly before anything is
   created server-side. Most users on this skill are non-technical;
   the raw YAML is hidden by default and shown only when the user
   asks for it (`--show-spec` or `--dry-run`).

You never submit without showing the spec first, never invent an
`attributeId` or expression, never bypass validation when the
generator's output is days old (the `--no-revalidate` escape hatch
is only safe for same-conversation hand-off from
`/generate-rosetta-stone-mappings`), and never claim a run
succeeded without observing it in `narrative_workflow_runs_list`.

## Output rules

**Don't surface `_nio_*` field names to the user.** Columns and
fields whose names start with `_nio_` (e.g., `_nio_last_modified_at`,
`_nio_sample_128`) are platform-managed internals. Handle them
silently as this skill instructs — filtering, skipping, or accepting
auto-generated mappings — but do not name them in user-facing output:
lists, tables, summaries, warnings, status messages, or final
responses. Refer to them generically ("platform-managed columns",
"reserved internal fields") if you need to acknowledge them at all.

Exception: if the user expressly asks about `_nio_*` fields, answer
normally.

## Overview

Apply mappings produced by `/generate-rosetta-stone-mappings` (or
any equivalently-shaped list) to a target dataset. The flow is:
pin company → acquire mappings → normalize and shape-check → resolve
dataset and current state → re-validate every expression → resolve
data plane → render the one-task workflow → gate on user approval →
submit with `trigger_immediately: true` → poll the run → report
per-mapping outcome.

The workflow contains exactly one task —
`CreateRosettaStoneMappingsIfNotExist` — wrapped in a minimal spec
so the platform handles idempotency, partial-failure semantics, and
durable history through the standard workflow runtime. The task is
named *IfNotExist* for a reason: re-applying the same mapping is a
no-op (it surfaces in `conflictMappings`, not as a failure).

This skill is a specialized hand-off path. For workflows that
combine mapping creation with other steps (view build, refresh,
audit log), use `/create-workflow` directly and start from
`examples/06-create-rosetta-stone-mappings.yaml`.

## Arguments

The skill accepts optional arguments after the slash command. Parse
them up front; never invent values.

| Argument | Meaning |
| --- | --- |
| `--dataset <id|name>` | The target dataset's numeric ID or its `datasetName` (alphanumerics + underscores). Required before submission; if omitted, the skill asks. |
| `--from <path>` | Path to a JSON file containing the mappings input (see [`references/INPUT_FORMAT.md`](references/INPUT_FORMAT.md)). Mutually exclusive with `--mappings`. |
| `--mappings <json>` | Inline JSON string with the mappings input. Useful when invoked programmatically from `/generate-rosetta-stone-mappings`. |
| `--allow-partial` / `--no-allow-partial` | Sets the task's `allowPartial` flag (default `true` — individual mapping failures don't abort the others). |
| `--data-plane <id>` | UUID of the data plane to target. Skips data-plane resolution. |
| `--dry-run` | Render the full spec, re-validation results, and the create-call parameters; do NOT submit. Implies `--show-spec`. |
| `--show-spec` | Include the full rendered workflow YAML in the approval preview. Off by default — most users only need the plain-English summary. |
| `--no-trigger` | Submit the workflow but do not pass `trigger_immediately: true`. The user must trigger it manually later (rare). |
| `--no-revalidate` | Skip Phase 5 NQL re-validation. Intended for same-conversation hand-off from `/generate-rosetta-stone-mappings` (which already validated every expression against the current schema). Do NOT pass when the input is from a file, a paste, or a prior conversation — the schema may have drifted. |

If invoked with no arguments, ask via `AskUserQuestion` whether the
user wants to provide a file path, paste JSON, or refer to the most
recent `/generate-rosetta-stone-mappings` output in the conversation.

## When to use

Triggers:

- "Apply these mappings to dataset N"
- "Create the Rosetta Stone mappings I just generated"
- "Push the mappings I saved earlier to `<dataset>`"
- "Productionize this mapping list"
- "Submit the `suggested_mappings` array against `<dataset>`"
- Any continuation from `/generate-rosetta-stone-mappings` where the
  user accepts the suggested mappings and wants them live.

Do NOT use for:

- Generating mappings — that's `/generate-rosetta-stone-mappings`.
  This skill never authors mapping expressions; it only ships an
  already-validated list.
- Authoring a multi-step workflow that includes mapping creation as
  one of several tasks — use `/create-workflow` with
  `examples/06-create-rosetta-stone-mappings.yaml`.
- Evaluating or scoring existing mappings on a dataset — go to
  `/generate-rosetta-stone-mappings` and the "Evaluate existing
  mappings" common case.
- Removing or editing existing mappings — the
  `CreateRosettaStoneMappingsIfNotExist` task only creates new
  mappings; conflicts are reported, not overwritten. There is no
  in-place edit task in the workflow runtime today.

## Procedure

Run phases 1–9 in order. Phases marked **mandatory** must complete
before submission. Phase 10 (run polling) is gated on
`--no-trigger` not being set.

### Phase 1. Pin the company / context — mandatory

Most Narrative work is scoped to a company. Before any dataset,
attribute, or workflow call:

```
narrative_context_get  → check the active company
```

If no company is set, or the user named a different one:

```
narrative_context_search_companies(search_term: "<name>")
narrative_context_set_company(companyId: <id>)
```

`narrative_context_search_companies` is global-admin-only. Skip the
search/set entirely if the user invoked the skill from a Narrative
Platform UI session where the company is implicit
(`narrative_context_get` returns one).

### Phase 2. Acquire the mappings input — mandatory

Branch on how the skill was invoked:

- **`--mappings <json>` passed**: parse the inline JSON.
- **`--from <path>` passed**: `Read` the file and parse as JSON.
- **Neither**: ask via `AskUserQuestion`:

  > "Where should I read the mappings from?"
  >
  > - **Paste JSON** — I'll prompt you to paste the
  >   `suggested_mappings` array (or full `final_answer` payload).
  > - **From file** — give me a path; I'll read it.
  > - **From this conversation** — use the most recent
  >   `/generate-rosetta-stone-mappings` output above.
  > - **Cancel** — exit without applying.

The accepted input shapes are:

1. A full `/generate-rosetta-stone-mappings` `final_answer` object —
   the skill reads `data.suggested_mappings`.
2. A bare `suggested_mappings: [...]` envelope.
3. A bare JSON array of mapping entries.

See [`references/INPUT_FORMAT.md`](references/INPUT_FORMAT.md) for
the full shape, field-name aliases, and worked examples.

### Phase 3. Normalize and shape-check the input — mandatory

For each mapping entry:

1. **Field-name translation.** The generator emits snake_case
   (`attribute_id`, `property_mappings`); the workflow task expects
   camelCase (`attributeId`, `propertyMappings`). Translate
   transparently — accept either casing on input, always emit
   camelCase to the workflow.
2. **Shape validation.** Every entry must have an `attributeId`
   (positive integer) and a `mapping` object. `mapping.type` is
   either `value_mapping` (then `mapping.expression` is required) or
   `object_mapping` (then `mapping.propertyMappings` is a non-empty
   array of `{ path, expression }`).
3. **Strip non-task fields.** Drop `confidence`, `reasoning`,
   `warnings`, and any other fields the generator emits for human
   review — they are not part of the
   `CreateRosettaStoneMappingsIfNotExist` task contract.

If any entry fails shape validation, surface the offending entry
verbatim and stop. Do NOT auto-fix or omit silently — the user
should know what they handed you.

### Phase 4. Resolve the target dataset — mandatory

Branch on what's known:

- **`--dataset <numeric_id>`**: call
  `narrative_datasets_describe(dataset_ids: [<id>], include: ["metadata", "schema", "mappings"])`.
- **`--dataset <name>`**: describe by name is not supported directly;
  search via `narrative_datasets_search(search_term: "<name>")`,
  pick the exact `name` match, then describe.
- **Neither**: ask via `AskUserQuestion` for the dataset ID or name.

Extract from the describe response:

- `datasetName` — the alphanumeric+underscore name the workflow task
  needs (max 256 chars). This is the dataset's `name` field, not the
  numeric ID.
- `dataPlaneId` — the plane the dataset lives on (used in Phase 6).
- `mappings[]` — any mappings already on the dataset. Cross-reference
  the input attribute IDs; any overlap is a conflict the task will
  no-op on. Surface this in the approval gate (Phase 7) so the user
  isn't surprised.
- `schema` — the column list used for expression re-validation in
  Phase 5.

### Phase 5. Re-validate every expression — mandatory unless `--no-revalidate`

The generator's output may be stale (the dataset's schema can drift
between generation and application). Re-validate every expression
against the current schema *before* rendering the workflow.

**`--no-revalidate` short-circuit.** When the flag is set, skip the
validate calls below and proceed to Phase 6. The flag is intended
for same-conversation hand-off from `/generate-rosetta-stone-mappings`
— the generator validates every expression in its step 6 against
the same schema this skill would re-check, so re-validating is
redundant. Surface a one-line note in Phase 7's approval gate:
"Skipped re-validation (`--no-revalidate`); relying on the
upstream `/generate-rosetta-stone-mappings` validation." If the
mappings came from a file, a paste, or a prior conversation, ignore
the flag and validate anyway — the schema may have drifted.

For each mapping:

- `value_mapping`: build one validate query.
- `object_mapping`: build one validate query per `propertyMappings`
  entry.

Each validate query wraps the expression as a select against the
dataset:

```
narrative_nql_validate(
  nql: 'select <expression> from company_data."<dataset_id>"'
)
```

Fire all validate calls **as concurrent tool calls in a single
turn** — they are independent and parallelism is materially faster
than serializing.

| Result | Action |
| --- | --- |
| All validates pass | Continue to Phase 6. |
| Any fail | Stop. Surface the offending mapping + the validator error verbatim. Tell the user to either remove that entry, re-run `/generate-rosetta-stone-mappings` to refresh the expression, or pass the corrected mapping back in. Do NOT submit a partially valid list — the workflow task accepts everything you hand it, and an invalid expression silently produces nulls at refresh time. |

### Phase 6. Resolve the data plane — mandatory

The workflow runs on a single data plane. It must match the
dataset's plane — wrong-plane submission surfaces as a
"dataset not found" error at runtime.

Branch:

- **`--data-plane <id>` passed**: use it, but compare against
  `dataPlaneId` from Phase 4's describe. If they differ, stop and
  surface the mismatch — do not guess.
- **Not passed**: use the `dataPlaneId` from Phase 4 directly. If
  the dataset describe didn't return one (rare), call
  `narrative_data_planes_list(include: ["metadata"])` and ask via
  `AskUserQuestion`.

### Phase 7. Render the spec and gate on approval — mandatory

Build the workflow YAML using this skeleton (one task, no schedule):

```yaml
document:
  dsl: '1.0.0'
  namespace: etl
  name: apply-<dataset-name>-mappings
  version: '1.0.0'

do:
  - applyMappings:
      call: CreateRosettaStoneMappingsIfNotExist
      with:
        datasetName: <dataset-name>
        allowPartial: <true|false>
        mappings:
          # one entry per normalized mapping
```

Phase 7 renders the final YAML. For DSL version pinning, kebab-case
rules, identifier regex, and single-quote escaping in YAML strings,
see [`references/YAML_RENDERING.md`](references/YAML_RENDERING.md).

One invariant stays inline because it is load-bearing safety: if the
user passed `--no-allow-partial` (or otherwise opted into
all-or-nothing semantics), render `allowPartial: false`. A single
mapping failure then aborts the whole task and the dataset's mapping
state stays as it was before the run.

Show the user, in this order:

1. A plain-English summary: dataset, count of mappings, breakdown
   (`N value_mappings`, `M object_mappings`), any conflicts
   pre-detected in Phase 4, and the chosen `allowPartial` setting.
2. The create-call parameters as a compact table:

   | Field | Value |
   | --- | --- |
   | `data_plane_id` | `<uuid>` |
   | `trigger_immediately` | `true` (or `false` if `--no-trigger`) |
   | `schedule_immediately` | `false` |
   | `tags` | `["rosetta-stone", "apply-mappings"]` |

3. **Only if `--show-spec` or `--dry-run` was passed**: the full
   rendered YAML in a fenced ```yaml block. Otherwise omit it —
   non-technical users find a wall of YAML counter-productive, and
   the plain-English summary plus parameters table is enough to make
   the approval decision. Mention in passing that they can re-run
   with `--show-spec` if they want to see the spec.

Surface caveats up front, not in a post-script:

- "Mapping for `attributeId: <id>` already exists on this dataset —
  the task will report it as a conflict and skip."
- "`allowPartial: true` — if one mapping fails, the others still
  apply. Pass `--no-allow-partial` if you want all-or-nothing."

Then gate. If `--dry-run`, stop here and print the rendered YAML.
Otherwise ask via `AskUserQuestion`:

> "Submit and trigger this mapping workflow now?"
>
> - **Submit it** — create via `narrative_workflows_create` with the
>   parameters shown.
> - **Refine the list first** — drop or edit specific entries; I'll
>   re-render.
> - **Cancel** — exit without creating.

Honor the user's choice exactly. If they pick "Refine", loop back to
Phase 3 with their edits. Never submit on an ambiguous answer.

### Phase 8. Submit — mandatory once approved

```
narrative_workflows_create(
  specification: '<full YAML string>',
  data_plane_id: '<plane uuid from Phase 6>',
  trigger_immediately: <true unless --no-trigger>,
  schedule_immediately: false,
  tags: ['rosetta-stone', 'apply-mappings']
)
```

On success, capture: `workflow_id`, `run_id` (when triggered),
`status`. On a 4xx (validator error), surface the error verbatim,
identify the likely root cause (wrong `datasetName` format,
malformed mapping shape, wrong-plane reference), and loop back to
Phase 3 or Phase 7 with a concrete fix. Do NOT retry the same spec
blindly.

### Phase 9. Follow the run — opt-in (default on)

If `trigger_immediately: true` was set, follow the run by calling
`narrative_workflow_runs_list(workflow_id: '<workflow_id>')` and
reading the first entry's `state`. Stop on
`state in ('completed', 'failed', 'cancelled')`. A run has no handle to
wait on, so pause between checks rather than asking back to back.

Narrative async work is slow: it rarely finishes in under ~30s, the
**median is roughly 5 minutes**, and large or cold-pool work can run
for **hours**. So the question is not how fast to re-ask — it is
whether you can wait instead of re-asking.

**Have a job id and the `job_monitor` / `wait_for` tools? Wait.**

```
job_monitor(job_id: "<uuid>")                          → waitable.handle "wt_…"
wait_for(handles: ["wt_…"], timeout_seconds: 3600)     → status + result
```

You are paused until the job finishes, at no cost while you wait — no
turns, no model calls — and you get back what the job did. Up to 8
handles in one `wait_for`, so jobs you started together are waited for
once rather than one at a time. A **failed** job is a finished wait
carrying its failure messages, not an error. If a wait times out with
the task still running you may wait again; the work carries on either
way. Never loop `narrative_jobs_describe` to find out whether a job is
done.

**No handle to wait on? Then you have to check, and pause between
checks.** A workflow run has no handle — only jobs do — and neither
does work started through a third-party MCP server. In order of
preference: `sleep(duration_seconds: <n>)` if you have it (up to an
hour per call); otherwise a background watcher if your harness has one
(Claude Code's `Monitor` driving an `until` loop, armed to re-check on
an interval and emit once the state is terminal, so the session stays
free); and a foreground `bash` `sleep` only when neither exists — some
harnesses, Narrative agent runs among them, block it outright.

**Cadence when you are the one checking.** First check ~15–30s after
submitting, then about every 30s, backing off to ~60s once it has been
running for a few minutes. Tell the user once — "still running (this
can take minutes to hours); I'll report back when it finishes" — and
don't narrate every check.

**Your turns are finite.** Inside a Narrative agent run every check and
every sleep spends one of a bounded number of iterations (10 by
default), so hours of work cannot be waited out by checking. Wait on
jobs wherever a handle exists; where none does, sleep long, and if it
is still going after a few checks hand the ids back to the user instead
of spending the rest of the budget.

**Give-up rule — abandon a *stuck* operation, not a merely slow one.**
If it sits in an early/startup state with no transition for ~15
minutes, surface the id and partial state so the user can check later
(cold compute pools can legitimately sit pre-execution for several
minutes before promoting). Work that is actively executing is making
progress even across a long wall-clock time — keep waiting on it rather
than timing it out.

When the run reaches a terminal state, read the task output. For
`CreateRosettaStoneMappingsIfNotExist`, the output includes:

- `createdMappings[]` — attribute IDs newly attached.
- `conflictMappings[]` — attribute IDs already mapped (no-op).
- `failedMappings[]` — entries that errored, with per-entry reasons.

If `--no-trigger` was passed, skip this phase. Tell the user the
workflow exists at `workflow_id` and they can trigger it via
`narrative_workflows_trigger` when ready.

### Phase 10. Report the outcome

Emit a final summary, in this order:

1. Headline: "Applied N of M mappings to `<dataset>`." Adjust based
   on created / conflict / failed counts.
2. Per-bucket detail tables for `createdMappings`, `conflictMappings`,
   `failedMappings`. Use the attribute IDs and (when known) display
   names. For `failedMappings`, include the verbatim reason.
3. The `workflow_id` and `run_id` for audit purposes.
4. A next-step nudge: if any failures occurred, suggest re-running
   `/generate-rosetta-stone-mappings` for the failed columns or
   passing a corrected list back in. If conflicts dominate, note
   that the dataset was already mapped — likely a no-op re-apply.

Use first person and conversational language in this summary — the
output is what the user sees in the chat, not a machine payload.

## Common case

### Hand-off from `/generate-rosetta-stone-mappings`

The default. The parent skill emits its `final_answer`, the user
accepts, and the model invokes this skill with either `--from
<tmp-path>` (after writing the JSON to disk) or `--mappings <json>`
inline. Phases 1 and 4 still run — pinning the company and
re-describing the dataset is cheap insurance against a stale
context.

For standalone, dry-run, single-expression re-apply, and
all-or-nothing invocations, see
[`references/MODES.md`](references/MODES.md).

## References

- [`references/INPUT_FORMAT.md`](references/INPUT_FORMAT.md) — accepted input shapes and field-name aliases. Read when Phase 2 rejects something the user expected to work.
- [`references/MODES.md`](references/MODES.md) — alternate invocation modes (standalone, dry-run, single-expression re-apply, all-or-nothing). Read when invoked outside the default `/generate-rosetta-stone-mappings` hand-off.
- [`references/YAML_RENDERING.md`](references/YAML_RENDERING.md) — Phase 7 YAML invariants: DSL pinning, kebab-case `document.name`, `datasetName` regex, single-quote escaping. Read when rendering or debugging the workflow spec.
- [`references/EDGE_CASES.md`](references/EDGE_CASES.md) — already-mapped attributes, casing drift, stale schemas, YAML quoting, wrong-plane datasets, `allowPartial`, polling timeouts. Read when input feels off or the run reports something unexpected.
- [`references/HARNESS_FALLBACK.md`](references/HARNESS_FALLBACK.md) — what to do when `narrative-mcp` or `AskUserQuestion` isn't available. Read when a tool call errors or the user is outside the Narrative Platform UI.
- `../generate-rosetta-stone-mappings/SKILL.md` — upstream skill that produces the `suggested_mappings` array this skill consumes.
- `../create-workflow/SKILL.md` — use instead when mapping creation is one task in a larger pipeline; start from `assets/examples/06-create-rosetta-stone-mappings.yaml`.
- `../find-attribute/SKILL.md` — for resolving an attribute name to its numeric ID when the input parser needs help.
- `narrative-knowledge-base` MCP — `/reference/workflows/tasks#CreateRosettaStoneMappingsIfNotExist` (task contract) and `/concepts/rosetta-stone/mapping-types` (value-vs-object semantics).

## Feedback (only if something could be improved)

**Silence is success.** Do *not* call `submit_feedback` when the skill
worked. No "great skill!" submissions, no positive feedback, no "FYI"
notes.

**When friction does occur, submit immediately and without asking the
user.** `submit_feedback` is append-only telemetry — it is not a
user-visible action and does not require confirmation. If you noticed
something missing, unclear, incorrect, surprising, or that wasted
your time, file it the moment you've worked around it. Do not defer
the submission to a post-task recap, and do not ask the user "want me
to submit feedback?" — that's the wrong default for this tool.

One submission per distinct friction point. Submit liberally.

Fields that matter most:

- `skill_name`: `narrative-common:apply-rosetta-stone-mappings` (use this verbatim).
- `severity`: `info` (nit) | `friction` (slowed you down) |
  `blocker` (stopped you).
- `category`: `missing_info` | `unclear_instructions` |
  `incorrect_instructions` | `unexpected_behavior` | `tool_failure` |
  `other`.
- `summary`: one concrete line — what went wrong, not how you felt.
- `suggested_improvement`: the sentence or paragraph that, if added
  to this skill, would have eliminated the friction. **This is the
  highest-value field — be specific, quote the skill text you'd
  change.**

Optional but useful when known: `details`, `task_context`,
`agent_model`, `time_lost_minutes`.
