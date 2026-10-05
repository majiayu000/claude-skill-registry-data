---
name: author-brief
description: Use this skill when the user has unstructured external input (an email thread, a prose description, a Linear Issue, a stakeholder message) and needs to produce a DoR-compliant product brief and queue it in workspace.toml. Triggers on "author a brief", "write a brief from this email", "create a brief from this Linear issue", "intake this brief", "turn this into a brief". Do NOT use to decompose an existing brief into specs (use receive-brief) or to author a single feature from scratch (use new-spec).
---

# Skill: author-brief

Turn any unstructured external input into a DoR-compliant product brief,
then queue it so `workspace-status` can surface it immediately.

`author-brief` stops at **draft** — it does not decompose the brief into specs
and does not set `Status: Ready`. Those are `receive-brief`'s job. The two
skills have distinct entry points and must stay distinct.

## Output rendering

Key–value / one record — For a single record's fields, use an aligned key: value list, not a two-row table.

## When to invoke

- The user has an email thread, a prose description, a Linear Issue body, or
  a stakeholder message they want to turn into a brief.
- The unit of work is larger than one feature (otherwise use `new-spec`).
- The brief does not yet exist as a file in `docs/product/briefs/`.

If the input is already a well-formed brief file, go directly to `receive-brief`.
If the user wants to record a decision already made, use `new-adr`.

## Procedure

### 1. Ingest

Accept whatever the user provides: a pasted email, a prose block, issue
text, a verbally-described idea. Do **not** reject partial or messy input —
the brief template is a guide, not a form. The goal is to extract enough
signal to elicit what is missing.

### 2. Identify

Scan the input for DoR fields already present:

- **Outcome** — a user-facing or system change the input is trying to
  achieve; often in the subject or opening sentence.
- **Appetite** — a time or effort constraint ("this needs to ship before
  the conference", "a sprint, not a quarter").
- **Rabbit holes** — named design traps, constraints, or things to avoid
  ("don't touch the billing system", "not the API redesign").

Name what you found and what is missing. Be specific: "I found an Outcome
('reduce checkout abandonment by surfacing error messages inline') but no
Appetite and no Rabbit holes."

### 3. Elicit

Ask for each missing DoR field conversationally. Rules:

- **Insist on Outcome.** If the input contains no clear outcome, ask for it
  before proceeding. Do not fabricate an outcome.
- **Offer defaults for the rest.** If no Appetite is stated, offer a default
  ("no Appetite stated — shall I default to 'a few weeks, not a quarter'?")
  rather than blocking.
- **Surface the Rabbit holes gap.** ≥1 Rabbit hole is required for the DoR
  gate. If the input contains none, ask the user to name at least one design
  trap or out-of-bound exploration before proceeding.
- **Do not invent.** Never fabricate missing fields. Do not silently derive
  a Rabbit hole from the problem description without confirmation.

### 4. Create

1. **Confirm the slug** with the user (kebab-case, matches the filename).
2. **Check for a slug collision:** if `docs/product/briefs/<slug>.md` already
   exists, stop and prompt the user before proceeding — do not silently
   overwrite an existing brief.
3. Write the brief file at `docs/product/briefs/<slug>.md` using the
   updated template (`_template.md` in that directory). Populate all fields
   gathered in steps 1–3. Set `Status: Draft`. Leave a Spec map placeholder
   row (do not run decomposition — that is `receive-brief`'s job).
4. Stage the file.

### 5. Queue

Check `workspace.toml` in the working directory:

- **Absent or unparseable:** create the brief file only. Emit the named
  diagnostic below — do not throw an error.
- **Present and parseable:**
  - If **multiple sections** have `status = "active"`, prompt the user to
    select which initiative's `brief_queue.draft` list the new brief joins.
    Do not guess.
  - If **no active initiative** exists, or the active initiative has no
    `brief_queue` sub-table: emit the named diagnostic below and continue
    with file-only operation.
  - Otherwise: append the brief's path as a string element to
    `["<initiative-slug>".brief_queue].draft` using a **comment-preserving
    edit** (targeted text insertion or `tomlkit`; never a full
    `tomllib` + `tomli_w` round-trip). Stage the file.

**Named diagnostic (all no-write cases):**
`"workspace.toml not available — brief created at docs/product/briefs/<slug>.md; add the path manually as a string element in [\"<initiative-slug>\".brief_queue].draft (e.g. append \"docs/product/briefs/<slug>.md\" to the list)."`

### 6. Hand off

Tell the user:

> "Brief is queued as draft at `docs/product/briefs/<slug>.md`.
> Run `receive-brief` to decompose it into specs and mark it ready."

## DoR gate

A brief is **eligible for `Ready`** when it carries:
- **Outcome** — non-empty outcome statement.
- **Appetite** — a time/effort constraint.
- **≥1 Rabbit hole** — at least one named design trap or uncertainty.
- **Spec map skeleton** — at least one placeholder row.

`author-brief` elicits these fields but does **not** set `Status: Ready`,
even when all four are populated. The brief exits this skill as `Status: Draft`.
Only `receive-brief`'s write-back step (after decomposition is confirmed) sets
`Status: Ready`.

## Anti-patterns to refuse

- **Running decomposition.** That is `receive-brief`'s job. Stop at draft.
- **Setting `Status: Ready`.** That is `receive-brief`'s write-back step.
- **Inventing a slug the user did not confirm.** Confirm it in step 4.
- **Fabricating missing DoR fields.** If Outcome is absent, ask. Do not derive
  it silently from the problem description.
- **Silently overwriting an existing brief file.** Prompt before proceeding if
  `docs/product/briefs/<slug>.md` already exists.
- **Guessing the target initiative** when multiple active ones exist in
  `workspace.toml`. Prompt for selection in step 5.
- **Making `workspace.toml` writes blocking.** A missing, unparseable, or
  no-brief_queue file degrades to file-only operation with the named diagnostic.
  Never stop skill execution for a TOML write failure.
