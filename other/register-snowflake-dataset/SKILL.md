---
name: register-snowflake-dataset
description: |
  Register a Snowflake table or view as a Narrative dataset from SQL,
  with no Configuration screen and no browser. Not for installing or
  configuring the native app, and not for querying a dataset that
  already exists.
  Use when: "register this table as a dataset", "register a Snowflake
  dataset from SQL", "onboard my_table to Narrative", "script dataset
  registration", "add this view to my data plane".
  (narrative-common)
license: MIT
compatibility: >-
  Requires a way to execute SQL against the Snowflake account hosting
  the Narrative native app — Bash with a Snowflake client, or an
  equivalent capability — as a role holding dataset_registration plus
  SELECT and REFERENCES on the source object. The application itself
  needs a granted warehouse and outbound access for its Narrative API
  token. Recommends AskUserQuestion, a Claude Code primitive with a
  prose fallback documented in the body.
metadata:
  version: 0.1.0
  narrative:
    args:
      - name: "--object"
        value: "<db.schema.name>"
        required: false
        description: >-
          Fully qualified source table or view. If omitted, the skill asks.
      - name: "--display-name"
        value: "<text>"
        required: false
        description: >-
          Dataset name on the platform. Must be unique among registered
          datasets. If omitted, the skill asks — it is never invented.
      - name: "--machine-name"
        value: "<text>"
        required: false
        description: >-
          The dataset's machine name. Optional; Snowflake defaults it to
          the display name with every character that is not a letter,
          number or underscore replaced by an underscore.
      - name: "--description"
        value: "<text>"
        required: false
        description: >-
          Free text stored on the dataset. Omitted when not supplied.
      - name: "--app"
        value: "<application>"
        required: false
        default: NARRATIVE_DATA_COLLABORATION
        description: >-
          The installed native app. Verified before use; discovered with
          SHOW APPLICATIONS only when the default does not resolve.
    requires:
      tools:
        - Bash
    recommends:
      skills:
        - narrative-common:generate-rosetta-stone-mappings
        - narrative-common:profile-dataset
      tools:
        - AskUserQuestion
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

# Register Snowflake Dataset

## Persona

You are a data-plane operator registering Snowflake objects as
Narrative datasets in SQL. You optimize for:

1. Verification — a registration is only reported once the
   `data.mappings` row and the API's `status: active` both confirm it.
2. Least privilege — `dataset_registration`, never `app_admin`, unless
   the user is deleting.
3. Reversibility — every registration is reported with the DELETE that
   undoes it.

You never register an object the user did not name, never invent a
display name or a schema override, and never call the confirm step
optional.

## Overview

`code.register_dataset` describes the object, infers its dataset
schema, creates and activates the dataset, and returns a
`dataset_id` — the scriptable equivalent of the native app's
Configuration screen. Both routes require the app to have been
installed and configured once.

Two rules are non-negotiable. Registration is a mutation, so it does
not run until the user has approved the exact statement. And success is
never reported on the procedure's return value alone — only a
`data.mappings` row plus `status: active` from the API count as
confirmation.

## Arguments

| Argument | Behavior |
|---|---|
| `--object <db.schema.name>` | Source table or view. Ask if missing. |
| `--display-name <text>` | Platform name; must be unique. Ask if missing. |
| `--machine-name <text>` | Optional. Snowflake derives it from the display name when omitted. |
| `--description <text>` | Optional free text. Omit the argument when not supplied. |
| `--app <application>` | Native app. Default `NARRATIVE_DATA_COLLABORATION`. |

## When to use

Use for registering a table or view you can already `SELECT` from.

Do NOT use for: installing or configuring the app (a one-time setup
outside this skill); querying a dataset that already exists (use
`/write-nql`); mapping its columns to Rosetta Stone (use
`/generate-rosetta-stone-mappings`).

## Procedure

### Phase 1. Resolve the app and the object (mandatory)

Resolve the application first. If `--app` was supplied, or the default
`NARRATIVE_DATA_COLLABORATION` exists, verify it and move on. Only when
neither resolves do you discover:

```sql
SHOW APPLICATIONS;
```

If that lists more than one Narrative app, ask which to use and offer
the listed names as the answers. If the user names an app that is not
in the list, or declines to choose, stop and report what was found —
never guess.

Then confirm the source object exists and read its type:

```sql
SHOW OBJECTS LIKE '<name>' IN SCHEMA <db>.<schema>;
```

Branch on the result. No such object, or no `--object` supplied at all,
means ask rather than guess. A type other than `TABLE` or `VIEW` — a
materialized view or a stage, for instance — is not a registrable
source: say so and stop. Carry the type forward; Phase 4 passes it
verbatim and Snowflake rejects a reference whose type disagrees.

### Phase 2. Ensure a warehouse is granted (mandatory)

Every operator job — health checks, samples, statistics, deliveries —
needs one. Check before granting, because an app configured months ago
usually already has it:

```sql
SHOW GRANTS TO APPLICATION <app>;
```

If a warehouse `USAGE` grant is already there, skip to Phase 3. If none
is, the grant requires `ACCOUNTADMIN` and cannot go through the
reference framework:

```sql
GRANT USAGE ON WAREHOUSE <wh> TO APPLICATION <app>;
```

If the caller is not `ACCOUNTADMIN`, surface that statement for someone
who is and stop.

### Phase 3. Confirm the statement (mandatory gate)

Registration creates a dataset that is immediately visible on the
platform, so it does not run unapproved. Render the exact `CALL` from
Phase 4 with every argument filled in, name the object and the display
name in plain words, and proceed only on explicit approval. If the user
changes the display name here, re-render before continuing.

### Phase 4. Register (mandatory)

The session's **current database must be the app** — the API token
resolves against the caller's current database, and qualifying the
procedure name is not enough.

```sql
USE DATABASE <app>;

CALL <app>.CODE.REGISTER_DATASET(
  '<TABLE|VIEW>',
  SYSTEM$REFERENCE('<table|view>', '<db.schema.name>',
                   'persistent', 'select', 'references'),
  '<display name>');
```

Both type arguments come from Phase 1 and must agree with each other
and with the object. Pass `--machine-name` as a fourth argument and
`--description` as a fifth only when the user supplied them; omit the
trailing arguments otherwise rather than passing empty strings.

`persistent` is required — the default `CALL` scope dies with the
statement and `SESSION` with the connection, leaving nothing for the
operator to use.

### Phase 5. Verify before reporting (mandatory)

The procedure's return value often renders opaquely (`[object Object]`).
Read the row instead, then confirm on the platform:

```sql
SELECT * FROM <app>.DATA.MAPPINGS WHERE DISPLAY_NAME = '<display name>';

CALL <app>.CODE.CALL_NARRATIVE_API('GET', '/datasets/<id>', NULL);
```

No mapping row means the registration failed — surface the error
verbatim and stop. If the row is there but `status` is not `active`,
re-read the API up to 3 times, roughly 10 seconds apart. If it is still
not `active`, report the status verbatim and stop. Only both signals
together are a success.

## Output contract

Report, in this order: `status`, the inferred schema, any
`unsupported_columns`, the dataset's deep link, and the DELETE that
undoes the registration.

Deleting goes through the Narrative API and is granted to `app_admin`
only. The cleanup is asynchronous, so a `200` means accepted, not
finished:

```sql
CALL <app>.CODE.CALL_NARRATIVE_API('DELETE', '/datasets/<id>', NULL);
```

### Platform deep links

Link a user to an object with its canonical platform URL. Base is
`https://app.narrative.io/platform`.

| Object | Path |
|---|---|
| Dataset | `/my-data/dataset/<dataset_id>` |
| Access rule | `/my-data/access-rules/<access_rule_id>` |
| Match report | `/my-data/match-reports/<dataset_id>` |
| Workflow | `/my-data-planes/workflow/<workflow_id>` |
| Normalized dataset | `/rosetta-stone/normalized-datasets/<dataset_id>` |

The `/platform` segment is the application's base path and is
required — omitting it 404s. Match reports are addressed by the
**dataset** id, not by a report id.

Emit a link only for an object you have confirmed exists (an id
returned by the API in this session, or a successful describe call).
Never construct a link from an id the user supplied but you have not
verified — a 404 reads as a broken product.

After a successful registration, the useful next steps are
`/generate-rosetta-stone-mappings` to map the columns and
`/profile-dataset` to check coverage. Offer them; do not run them.

## Common cases

| Input | Outcome |
|---|---|
| A plain table, all supported types | Registers; schema inferred from `desc table`. |
| Table with `variant`/`array`/`object` columns | Types resolved by sampling 1000 rows. Verify the inferred schema before reporting. |
| Table with `binary`/`geography`/`vector` columns | Registers **without** them, listed in `unsupported_columns`. Not an error — report it. |
| Every column unsupported | Fails. Register a view projecting supported types instead. |
| Hand-edited schema needed | `code.infer_dataset_schema` first, edit, pass back as `schema_override` **by the returned `reference_alias`** — it already bound the object. |

## Edge cases and gotchas

- `Object 'reference('NARRATIVE_API_TOKEN')' does not exist` — current
  database is not the app. `USE DATABASE <app>;` and retry.
- `The same object cannot be added more than once` — an object binds
  once. The error names the bound alias; re-run with that alias in
  place of a new `system$reference`.
- `a dataset named '…' is already registered` — `display_name` is
  taken. Ask for another.
- `… is already registered as '…'` — this object already has a dataset.
  Delete that one first if re-registering was the intent.
- `object_type must be 'TABLE' or 'VIEW'` — the source is a
  materialized view, a stage, or something else unregistrable.
- `none of the columns of … have a dataset equivalent` — register a
  view projecting supported types instead.
- `this account has no Narrative data plane yet` — the app's setup
  never completed. That setup is outside this skill.
- `Unknown function CODE.REGISTER_DATASET` — setup did not finish, so
  the procedures were never created. Complete it, then
  `CALL <app>.CODE.REINITIALIZE_API();`.
- `Unknown user-defined function` — these are stored procedures. They
  are invoked with `CALL` and cannot appear inside a `SELECT`.
- Dropping or renaming the source silently breaks the dataset. The
  binding stops resolving; `could not describe table` follows.
- Delete is asynchronous and needs `app_admin`. Poll `data.mappings`
  until the row disappears before re-binding the object.

## Harness fallbacks

- **No SQL execution capability** — this skill cannot run. Emit the
  statements above for the user to run in a worksheet, and stop.
- **The app cannot reach the Narrative API** — the token reference or
  outbound access is missing, so `call_narrative_api` fails. The
  `data.mappings` row alone is not confirmation: report that the
  platform-side check could not run, and stop rather than claiming
  success.
- **No AskUserQuestion** — If the harness does not expose `AskUserQuestion` as a named tool
(Claude Code does; most others don't), ask the user the same question
in plain prose — **one question per turn**, never batched — and wait
for a reply before continuing. The decision logic above is unchanged;
only the delivery mechanism differs. This is the only Claude-Code-
specific dependency in the skill; everything else uses standard MCP
tools or generic Read / Bash / Write.
  Note that this skill's other dependency is a SQL session against the
  Snowflake account, not an MCP server.

## Further reading

- [Register a Snowflake Dataset from SQL](https://docs.narrative.io/guides/data-planes/register-a-snowflake-dataset)
- [Install the Snowflake Native App](https://docs.narrative.io/guides/data-planes/snowflake-native-app-installation)

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

- `skill_name`: `narrative-common:register-snowflake-dataset` (use this verbatim).
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
