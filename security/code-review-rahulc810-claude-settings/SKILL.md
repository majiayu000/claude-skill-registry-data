---
name: code-review
description: Review a diff or a plan's implementation for correctness, quality and plan adherence, bucketing findings by severity into specs/NNN-<slug>/review.md. Trigger on:- review this, check my code, does this match the plan, audit, running-review.
argument-hint: "project (path or name), scope: full | plan <plan-name...> | running-review [report]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
disable-model-invocation: true
model: claude-opus-5
---

# Code Review

Reviews on two axes together: **does it do what the plan said**, and **is it good code**
(bugs, security, tests, style). Findings are bucketed by severity, not dumped as a flat
list. This skill reports and re-verifies only — it never fixes anything and never creates
mcp-erp tasks.

## When to use this

- Before landing or merging, or to check an implementation against its plan doc.
- Not for architecture questions with no diff in hand — that's `/improve`.
- To *fix* what this finds, run `/resolve-review`. To apply routine quality cleanups
  directly without a report, use `/simplify`.

## Assumptions (flag if any are wrong)

- `project` resolves to a path on disk. Accept a path directly, or a name — if a name,
  look under the common project roots and ask once rather than guessing.
- Plans live at `specs/NNN-<slug>/plan.md` (the output of `/designit` → `/plan-doc`).
  If that path doesn't exist, search the project before asking.

Read `.specify/memory/constitution.md` first — it holds the pipeline map and the review
status vocabulary (`open` → `worked-on` → `closed`).

## Arguments

- `project` — path or name of the project to review.
- `scope` — if omitted, ask. Don't default silently between "everything", "one plan" and
  "re-check fixes".
  - `full` — the whole codebase, cross-checked against every `specs/*/plan.md`.
  - `plan <name...>` — only the code the named plan(s) describe.
  - `running-review [report]` — re-check fixes against an existing report. If `report` is
    omitted, take the most recent one with `Status: worked-on`; if none exists, say so and
    stop rather than guessing which report or scope was meant.

## Status lifecycle

A review thread lives in **one file for its whole life** (`specs/NNN-<slug>/review.md`),
reused across rounds rather than recreated. The `status:` header drives the handoff with
`resolve-review`; the vocabulary and who-writes-what is in the constitution. In short:
this skill writes `open` and (terminal) `closed`; `resolve-review` writes `worked-on`;
`closed` forwards to `finalize`.

## Steps

1. **Resolve the project.** Confirm it's a git repo (`git rev-parse
   --is-inside-work-tree`). If not, say diff-based scoping is unavailable and review
   files directly.

2. **Load context for the scope.**
   - `full` — `Glob` every `specs/*/plan.md`, read each, then survey the codebase
     (structure via `Glob`/`Grep`, key files via `Read`).
   - `plan <name...>` — read the plan doc(s) in full *first*: decisions, architecture,
     locked-in details. Then find the code, preferring `git log`/`git diff` against the
     base branch; fall back to `Grep`/`Glob` for the files the plan names.
   - `running-review` — read the existing report in full, including `resolve-review`'s
     `## Resolution` section. Re-check each item marked Fixed against the current code
     rather than trusting the note, and re-examine anything Skipped or Deferred to
     confirm that's still the right call.

3. **Review both axes together**, per file for `full`/`plan`, per finding for
   `running-review`:
   - **Plan adherence** (only with a plan doc in hand) — flag both *deviations* and *plan
     gaps*. Don't assume a deviation is wrong or that it's fine; let severity reflect
     your confidence.
   - **Quality** — correctness, security (injection, secrets, auth gaps, unsafe
     deserialization), test coverage for the changed logic, and consistency with the
     codebase's conventions, not your own preferences.

4. **Bucket every finding.** **Blocking** (bugs, security, plan deviations that must be
   fixed before landing) / **Should-fix** (real but not launch-blocking) / **Nit**
   (style, naming, preference). Don't inflate severity to look thorough, and don't bury
   real issues under nits.

5. **Write or update the report** at `specs/NNN-<slug>/review.md` (from
   `.specify/templates/review-template.md`) — created once per thread; `running-review`
   edits it in place.
   - `status:` + `updated:` header, scope at the top, then a summary of counts by severity.
   - Findings grouped by severity, each with file:line, what's wrong, why it matters, and
     a suggested fix.
   - `running-review` appends a `## Re-review — <date>` section listing which prior
     findings are confirmed resolved and which remain — it doesn't rewrite history.
   - Set `status: closed` if no Blocking or Should-fix remain and forward to `/finalize`;
     otherwise `open`.
   - Give a concise inline summary in chat too: the counts, then the Blocking items in
     full. Don't just say "see the report."

## What not to do

- Don't fix anything, and don't create mcp-erp tasks from findings.
- Don't write `worked-on` — that status belongs to `resolve-review`.
- No plan doc found for scope `plan <name>`: say so and stop; don't guess at what the
  plan said. (For `full` with no plans anywhere, proceed as a pure quality review and say
  so.)
- Nothing changed since the plan started: say so plainly rather than manufacturing
  findings.
