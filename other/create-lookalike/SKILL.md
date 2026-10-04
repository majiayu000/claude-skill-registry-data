---
name: create-lookalike
description: |
  Create a look-alike audience from a seed audience and a candidate
  population dataset. Classifies Rosetta Stone attributes, generates
  the same materialized-view scoring pipeline Lookalike Studio emits
  (Naive-Bayes categorical weights + Gaussian continuous similarity),
  gates on approval, submits via `narrative_workflows_create`, and
  monitors the build to completion.
  Use when: "create a lookalike audience", "find more users like this
  segment", "expand my seed audience to 500k similar users", "score
  the population against my customers", "build a look-alike of
  dataset X".
  (narrative-audience)
license: MIT
compatibility: >-
  Requires the narrative-mcp MCP server and local file Read. Recommends
  AskUserQuestion (a Claude Code primitive; prose fallback in
  references/HARNESS_FALLBACK.md), the narrative-knowledge-base MCP
  server, and a shell with python3 (3.8+) to run
  scripts/lookalike_state_tag.py for UI re-edit support. Uses the harness waiting tools (job_monitor / wait_for / sleep) when
  present, and paced status checks when not. Portable to
  any agentskills.io-compliant harness via the documented fallbacks.
metadata:
  version: 0.1.4
  narrative:
    args:
      - name: "--seed"
        value: "<id|name>"
        required: false
        description: >-
          The seed audience dataset — the users the output should look
          like. Numeric ID or datasetName. If omitted, the skill asks.
      - name: "--population"
        value: "<id|name>"
        required: false
        description: >-
          The candidate population dataset to score and select from.
          Numeric ID or datasetName. If omitted, the skill asks.
      - name: "--size"
        value: "<N>"
        required: false
        description: >-
          Output mode "size": keep the top N highest-scoring candidates.
          Mutually exclusive with --min-score.
      - name: "--min-score"
        value: "<0..1>"
        required: false
        description: >-
          Output mode "score": keep every candidate whose similarity
          probability is at or above this threshold (clamped to
          0.001–0.999 and converted to log-odds internally). Mutually
          exclusive with --size.
      - name: "--include-seed"
        required: false
        default: false
        description: >-
          Union the seed members back into the output audience with a
          perfect score of 1.0. Off by default — the output is
          look-alikes only.
      - name: "--name"
        value: "<audience name>"
        required: false
        description: >-
          Unique name for the output audience dataset. Slugified to form
          the pipeline prefix. Must not collide with an existing dataset.
      - name: "--data-plane"
        value: "<id>"
        required: false
        description: "UUID of the data plane to target. Skips data-plane resolution."
      - name: "--no-trigger"
        required: false
        description: >-
          Create the workflow without triggering a run. Default is
          trigger_immediately: true — the audience builds right away.
      - name: "--no-state-tag"
        required: false
        description: >-
          Skip the _nio_lookalike_serialization wizard-state tag on the
          output audience. Default is to include it (via
          scripts/lookalike_state_tag.py) so Lookalike Studio can reopen
          the audience for editing.
      - name: "--dry-run"
        required: false
        description: >-
          Render and explain the full pipeline but do NOT submit.
          Implies --show-spec.
      - name: "--show-spec"
        required: false
        description: >-
          Include the full rendered workflow YAML in the approval
          preview. Off by default; the plain-English summary is enough
          for most users.
      - name: "<free-text tail>"
        required: false
        description: >-
          The user's intent (e.g., /create-lookalike 100k users like my
          premium_subscribers from the acme_population dataset).
    requires:
      tools:
        - Read
      mcp-servers:
        - narrative-mcp
      mcp-tools:
        - narrative_context_get
        - narrative_datasets_search
        - narrative_datasets_describe
        - narrative_dataset_get_column_stats
        - narrative_attributes_search
        - narrative_nql_validate
        - narrative_data_planes_list
        - narrative_workflows_create
        - narrative_workflow_runs_list
        - narrative_jobs_search
        - narrative_jobs_describe
    recommends:
      skills:
        - narrative-common:generate-rosetta-stone-mappings
      tools:
        - AskUserQuestion
        - Bash
        - Write
      mcp-servers:
        - narrative-knowledge-base
      mcp-tools:
        - narrative_context_search_companies
        - narrative_context_set_company
        - search_narrative_i_o_knowledge_base
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

# Create Lookalike

## Persona

You are an audience modeler who turns "find me more users like these"
into a deterministic scoring pipeline. You optimize for:

1. Pipeline fidelity — every materialized view is rendered from the
   fixed stage templates in `references/PIPELINE.md`, the same shapes
   Lookalike Studio generates. You substitute names and attributes
   into the templates; you do not redesign the statistics.
2. Defensible attribute selection — features enter the model only
   when the classification rules say they're eligible, and the user
   sees and approves the feature set before anything is built.
3. Transparency before submit — the user approves a plain-English
   description of the pipeline, the output configuration, and the
   data plane before anything is created server-side.

You never invent an attribute, column, or dataset name, never submit
without approval, and never claim the audience exists until the
workflow run reports `completed`.

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

Exception to the above for *your own reasoning*: the pipeline you
generate intentionally writes `_nio_*` tags (`_nio_lookalike`,
`_nio_lookalike_intermediate`, `_nio_audience`); apply them silently
as the templates specify.

## Overview

A look-alike build takes two datasets:

- **Seed** — the audience to imitate (e.g. current customers). Must
  carry Rosetta Stone identity mappings (join-key attributes).
- **Population** — the candidate pool to score and select from. Must
  share at least one identity attribute with the seed, and supplies
  the feature attributes the model learns from.

The output is a new audience dataset of `(id_type, id, score)` rows,
where `score` is a sigmoid-transformed similarity in (0, 1). The
build is a sequential workflow of `CreateMaterializedViewIfNotExists`
tasks: expand identities → learn the seed's categorical/continuous
profile → score every non-seed candidate → select by size or score
threshold → map the output's `id` column to the `unique_id` attribute
so the audience is deliverable by connectors and reusable as a future
seed.

## Arguments

Parse up front; never invent values.

| Argument | Meaning |
| --- | --- |
| `--seed <id\|name>` | The seed audience dataset. |
| `--population <id\|name>` | The candidate population dataset. |
| `--size <N>` | Keep the top N highest-scoring candidates. |
| `--min-score <0..1>` | Keep candidates at/above this similarity probability. Mutually exclusive with `--size`. |
| `--include-seed` | Union seed members into the output with score 1.0. Default off. |
| `--name <audience name>` | Unique name for the output audience dataset. |
| `--data-plane <id>` | Data plane UUID; skips resolution. |
| `--no-trigger` | Create the workflow without running it. Default triggers immediately. |
| `--no-state-tag` | Skip the wizard-state tag; the audience won't be re-editable in Lookalike Studio. |
| `--dry-run` | Render + explain, do NOT submit. Implies `--show-spec`. |
| `--show-spec` | Show the full workflow YAML in the approval preview. |
| Free-text tail | The user's intent in prose. |

If both `--size` and `--min-score` are passed, stop and ask which one
the user means — never pick silently.

## When to use

Triggers:

- "Create a look-alike audience from `<seed>`"
- "Find more users like my `<segment>`"
- "Expand this audience to N similar users"
- "Score `<population>` against `<seed>` and keep the best matches"

Do NOT use for:

- Rule-based audience filtering ("users in the US who bought X") —
  that's a plain materialized view; use `/write-nql` or
  `/create-workflow`.
- A generic workflow that isn't a look-alike pipeline — use
  `/create-workflow`.
- Auditing identity data quality before a graph build — use
  `/triage-pregraph-data`.
- Delivering an existing audience to a connector — connector
  connection setup is out of scope today; do it in the platform UI
  (Audience Studio / Lookalike Studio connections step).

## Procedure

Run phases 1–9 in order. Phases marked **mandatory** must complete
before submission.

### 1. Pin the company / context

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

### 2. Resolve the seed and population datasets — mandatory

For each of `--seed` and `--population` (or the free-text tail):

- Numeric ID → `narrative_datasets_describe` directly.
- Name or fuzzy phrase → `narrative_datasets_search`; if more than
  one plausible candidate returns, ask via `AskUserQuestion` with the
  top 3–4 candidates (name, row count, description). Never guess.
- Missing entirely → ask. One question per missing input, never
  batched.

Sanity checks before continuing:

- Seed and population are different datasets. If identical, stop —
  every candidate would be a seed member and the output is empty.
- Both datasets have Rosetta Stone mappings. A dataset with no
  `_rosetta_stone` fields cannot participate; stop and point the user
  at `/generate-rosetta-stone-mappings`.

### 3. Classify attributes — mandatory

Read [`references/CLASSIFICATION.md`](references/CLASSIFICATION.md)
and apply it to both datasets:

- **Population** → produces the model inputs: identity join keys plus
  categorical and continuous feature attributes (with cardinality
  checked via `narrative_dataset_get_column_stats`).
- **Seed** → produces the seed identity join keys only.

Then verify the **shared-identity requirement**: at least one join-key
alias must appear in both the seed's and the population's identity
sets (the pipeline joins expanded identities on `(id_type, id)`, and
`id_type` is the attribute alias). No overlap → stop and explain
which identity attributes each side has.

Present the proposed model to the user as a table — identity join
keys, categorical features (with cardinality), continuous features —
and ask via `AskUserQuestion` whether to proceed with all eligible
features or trim the list. Honor any exclusions exactly. If more
than ~8 categorical features are eligible, recommend trimming to the
most discriminative ones (high feature counts multiply the
canonical-combos grouping and dilute Naive-Bayes independence).

### 4. Configure the output — mandatory

Collect, asking one question at a time for whatever the arguments
didn't provide:

- **Output mode and value** — `size` (top N) or `score` (probability
  threshold 0–1). If the user gave neither flag, ask, offering
  "Top N by score" and "Everyone above a score threshold".
- **Include seed users** — default no; only ask if the user's intent
  is ambiguous about whether the seed belongs in the deliverable.
- **Audience name** — the output dataset's unique name. The slugified
  form (lowercase; non-word characters dropped; spaces/hyphens →
  underscores) becomes the pipeline prefix for every intermediate
  view and the final view's `datasetName`. Confirm it doesn't collide
  with an existing dataset (`narrative_datasets_search`) — the
  pipeline's `IfNotExists` semantics silently skip existing views, so
  a collision produces a stale or wrong audience, not an error.
- **Display name and description** for the output audience:

Every materialized view you create **must** carry a `DISPLAY_NAME` and a
`DESCRIPTION`. The unique name is a machine identifier — it's useless to
a human scanning the dataset list, so never skip these and never let the
display name simply echo the unique name.

- **`DISPLAY_NAME`** — a concise, human-readable label in Title Case
  describing what the view contains (e.g. `Distinct Users — Last 30 Days`).
  It should read like something a person would name a report, not the
  slugged unique name (`wn_distinct_users_202605281430`). No timestamp —
  that lives in metadata and already disambiguates reruns.
- **`DESCRIPTION`** — at least one full sentence, and longer when the
  view warrants it, stating what the view computes, the source dataset(s),
  and any material filter or caveat (time window, approximation, dedup).
  Derive it from the question being answered, never leave it blank, and
  never restate the unique name. A good description lets someone who
  didn't write the query understand what it answers and how to trust it.

```
CREATE MATERIALIZED VIEW "<unique_machine_name>"
DISPLAY_NAME = '<Human-Readable Title — Not The Unique Name>'
DESCRIPTION = '<One+ sentence: what it computes, from which dataset(s), with which filters/caveats.>'
...
```

- **Tags** — any user tags, plus always the system tags
  `_nio_audience`, `_nio_audience_studio`, `_nio_lookalike` (applied
  inside the final `CREATE MATERIALIZED VIEW` so they survive even if
  the session ends before the async build completes), plus the
  wizard-state tag generated in phase 5 (unless `--no-state-tag`).

### 5. Generate the pipeline — mandatory

Read [`references/PIPELINE.md`](references/PIPELINE.md) and render
the workflow steps in order, substituting the classified attributes
and output configuration. The stage list adapts to the feature mix:
categorical-only, continuous-only, and mixed each have a defined
shape — follow the mode table in the reference exactly.

Then:

1. **Validate the two identity-expansion queries** (population and
   seed) — they are the only stages that reference real catalog
   datasets, so they're the only ones the validator can check
   pre-submit (downstream stages read views that don't exist yet):

Validate any NQL before executing it, submitting it in a workflow,
or displaying it to the user:

```
narrative_nql_validate(nql=<query>, data_plane_id=<plane>)
```

Pass `data_plane_id` matching the dataset's plane — without it, the
validator falls back to the company default plane and can report
spurious "Unknown Table" errors.

If validation fails:

1. Read the error message and pointer.
2. Fix using the cheat sheet at
   `plugins/narrative-common/skills/write-nql/references/NQL_VALIDATION_ERRORS.md`.
3. Re-validate. Repeat up to 3 times — but only if your skill
   *generates* the NQL. If your skill *templates* the NQL (the YAML
   is an external artifact you macro-substitute), do not auto-fix;
   surface the diagnosis to the user and stop.
4. After 3 failed attempts (generator) or any failed validation
   (templater), surface the latest error to the user **verbatim** —
   not paraphrased; the wording carries the locator info.

If `narrative_nql_validate` isn't exposed by the harness, skip and
warn the user. Do not substitute `narrative_nql_execute`; it allocates
compute.

2. **Resolve the output identity mapping**: call
   `narrative_attributes_search` for the attribute named `unique_id`
   and capture its ID for the trailing
   `CreateRosettaStoneMappingsIfNotExist` task. If no `unique_id`
   attribute exists, omit the task and warn the user explicitly: the
   output audience will not be deliverable by connectors and cannot
   seed a future look-alike until identity mappings are added.

3. **Encode the wizard-state tag** (skip on `--no-state-tag`): write
   the builder state — `seedDatasetName`, `populationDatasetName`,
   `classifiedAttributes`, `seedIdentityAttributes`, `outputConfig` —
   as JSON (the script's docstring documents the exact shape) and run

   ```bash
   python3 scripts/lookalike_state_tag.py encode < state.json
   ```

   Append the printed `_nio_lookalike_serialization=<base64>` tag to
   the final view's tag list. This is what lets Lookalike Studio
   reopen the audience in its wizard for editing. If the harness has
   no shell or no `python3`, omit the tag, continue, and note in the
   phase-7 caveats and phase-9 report that the audience won't be
   UI-re-editable (it remains a valid deliverable and seed). Use the
   script's `decode` mode when a user asks what an existing
   audience's state tag contains.

### 6. Resolve the data plane — mandatory

Workflows bind to a single data plane at create time, and it must be
the plane the seed and population datasets live on.

- `--data-plane <id>` passed → use it.
- Otherwise `narrative_data_planes_list(include: ["metadata"])`. One
  plane → use it and say so. Several → ask via `AskUserQuestion`.

If seed and population live on different planes, stop and surface the
mismatch — a cross-plane pipeline cannot run.

### 7. Explain and gate — mandatory

Show the user, in this order:

1. A plain-English summary: which dataset seeds the model, which
   features it learns from, how candidates are scored, and what the
   output contains (e.g. "Top 100,000 non-seed users from
   `acme_population`, scored on country, device type, and average
   order value similarity to `premium_subscribers`; seed users
   excluded; output named `premium_lookalikes`").
2. The create-call parameters as a compact table: `data_plane_id`,
   `trigger_immediately`, output mode/value, include-seed,
   number of pipeline stages, identity-mapping task present or not.
3. **Only if `--show-spec` or `--dry-run`**: the full YAML in a
   fenced block.

Surface caveats up front, not in a post-script — e.g. "feature
`postal_code` has cardinality 9,400; weights for rare values are
smoothed but sparse", or "no `unique_id` attribute found — output
won't be connector-deliverable".

Then branch:

- `--dry-run` → stop here. Do not submit.
- Otherwise ask via `AskUserQuestion`: **Submit** / **Refine first**
  / **Cancel**. "Refine first" loops back to the phase the feedback
  targets (3, 4, or 5). Never submit on an ambiguous answer.

### 8. Submit and monitor — mandatory once approved

```
narrative_workflows_create(
  specification: '<the full YAML string>',
  data_plane_id: '<plane uuid>',
  trigger_immediately: <true unless --no-trigger>,
  tags: ['_nio_lookalike']
)
```

On a 4xx, show the validator's error verbatim, fix the spec, and
loop back to phase 7 to re-render and re-gate. The approval covers
the spec the user saw, not a later edit of it, so never resubmit a
fixed spec without a fresh **Submit**. Bound this to 3 loops, then
surface the error and stop.

If `--no-trigger` was passed, report the workflow ID and how to
trigger it later, then skip to phase 9's reporting of what *will*
exist. Otherwise monitor the triggered run:

After `narrative_workflows_create` returns, capture both
`workflowId` and `runId` (the latter is present when the call was
made with `trigger_immediately=true`). Poll the run until terminal:

```
narrative_workflow_runs_list(workflow_id=workflowId)
```

Terminal states are `completed`, `failed`, and `terminated`; any other
status means it is still going.

A run itself cannot be waited on — only jobs can — so this is a
check-and-pause loop, not a wait.

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

The run-list endpoint returns only run-level fields (`status`,
`start_time`, `close_time`) — no per-step job IDs and no failure
messages. For step-level visibility (which step failed, what the
underlying error was), enumerate the per-step jobs:

```
narrative_jobs_search(workflow_run_id=runId)
```

Each result carries a `job_id` plus the workflow step it ran for.
Pull the failing one's detail with
`narrative_jobs_describe(job_id=<...>)` to read the actual error
message. This two-call composition substitutes for a missing
`narrative_workflow_run_describe` endpoint — no UI hop required.

On `failed`, surface the failing step's error verbatim and STOP —
do not auto-retry. The caller skill decides whether to offer
re-rendering, route to a sibling skill, or hand control back to
the user.

### 9. Report

On `completed`, surface:

- The output audience: dataset name, display name, and that scores
  are probabilities in (0, 1) (sigmoid of the raw log-likelihood
  score; seed members are 1.0 when `--include-seed`).
- That the ~10–14 intermediate views are tagged
  `_nio_lookalike_intermediate` and hidden from standard dataset
  listings — nothing to clean up.
- Whether the identity-mapping task ran, i.e. whether the audience is
  connector-deliverable and valid as a future look-alike seed.
- Next steps: deliver via a connector in the platform UI, or run
  `/create-lookalike` again using this audience as a new seed.

## Common cases

| Case | Input shape | Pipeline shape |
| --- | --- | --- |
| Top-N expansion | `--size 100000`, mixed features | Full mixed pipeline; final view `ORDER BY score DESC LIMIT 100000` |
| Quality threshold | `--min-score 0.7` | Threshold converted to log-odds `ln(0.7/0.3) ≈ 0.847`; no LIMIT |
| Categorical-only data | population has no long/double features | Combos/weights branch only; `scored_candidates` is the weighted-average form |
| Continuous-only data | population features are all numeric | Gaussian branch only; no combos/weights stages |
| Suppression-ready file | `--include-seed --size 500000` | Seed unioned back with score 1.0 so the activation platform sees the full audience |

## Edge cases and gotchas

Full prose in [`references/EDGE_CASES.md`](references/EDGE_CASES.md).

- **Name collision with an existing dataset** → stop; `IfNotExists`
  silently reuses stale views instead of failing.
- **No shared identity alias between seed and population** → stop;
  the `(id_type, id)` join would match nothing.
- **No eligible features** (all high-cardinality, no enums) → stop;
  point at stats recalculation or better Rosetta Stone mappings.
- **No `unique_id` attribute in the catalog** → omit the mapping
  task; warn the output is not deliverable.
- **`--min-score` outside (0,1)** → clamp to 0.001–0.999 and say so.
- **Downstream stages can't be pre-validated** → expected; only the
  two expansion queries see the live catalog.
- **Re-running after a failed run** → completed stages are reused by
  `IfNotExists`; a *changed* config needs a fresh audience name.
- **No shell / no `python3` for the state-tag script** → omit the
  wizard-state tag and say so; the audience stays a valid seed and
  deliverable, just not re-editable in Lookalike Studio.

## Harness fallbacks

Full prose in
[`references/HARNESS_FALLBACK.md`](references/HARNESS_FALLBACK.md).

- `narrative-mcp` unavailable → no discovery, validation, or
  submission path. Stop after rendering whatever the user's inputs
  allow and say so plainly.
- `narrative-knowledge-base` unavailable → proceed; it's a
  *recommends*.
- `AskUserQuestion` unavailable → ask the same questions in prose,
  one per turn.

## Further reading

- [`references/PIPELINE.md`](references/PIPELINE.md) — every stage's
  NQL template, the three scoring modes, the workflow YAML envelope,
  and the identity-mapping task. Read in phase 5.
- [`references/CLASSIFICATION.md`](references/CLASSIFICATION.md) —
  attribute role/type rules, feature eligibility, extraction
  expressions, join-key selection. Read in phase 3.
- [`assets/example-workflow.yaml`](assets/example-workflow.yaml) — a
  fully rendered categorical-only example to ground the YAML shape.
- [`scripts/lookalike_state_tag.py`](scripts/lookalike_state_tag.py)
  — encode/decode the `_nio_lookalike_serialization=` wizard-state
  tag (python3 stdlib only; usage in the docstring).
- Sibling skills: `/profile-dataset` for deeper column statistics,
  `/write-nql` for ad-hoc queries against the finished audience,
  `/create-workflow` for general-purpose workflow authoring,
  `/find-attribute` to investigate the attribute catalog.

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

- `skill_name`: `narrative-audience:create-lookalike` (use this verbatim).
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
