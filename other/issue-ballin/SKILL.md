---
name: issue-ballin
description: "Pick the KoFEM Linear issues that can be solved independently, side by side, and start one cloud session per issue with a self-contained brief. Use for /issue-ballin, 'start sessions for the open issues', 'fan out the backlog', or 'work several issues in parallel'."
---

# Issue ballin'

One issue, one top-level cloud session, one branch, one PR. This beats
subagents: each session reads the issue itself, starts with a clean context,
owns the whole definition of done, and the user can open it and steer. This
skill only picks and briefs; the sessions do the work.

Arguments, all optional: a number of sessions (default 5, at most 8), issue
keys to start as given, or a label, project or area to pick from. "Dry run" or
"just list" means stop after step 2 and show the picks.

The user invoking the skill is the go-ahead. Do not ask for confirmation
before starting sessions unless they asked for a dry run.

## 1. Gather

- `list_issues` with team `KOF` and state `Backlog`, then `Todo`, limit 100.
  Query by state name: the state type `unstarted` returns nothing in this
  workspace.
- `list_issues` with state `started`. Those issues are taken, and the areas
  they touch are off limits for this batch.
- Skip the Agentic Research Workflow project: it is not this repository.
- For each plausible candidate, `get_issue` with `includeRelations: true` and
  read the description and the Agent notes. Titles alone mislead.

## 2. Pick

Take an issue only if all of these hold:

- **Done is checkable.** It has acceptance criteria, or you can write a
  definition of done in a few lines without the maintainer. An empty
  description is fine if the intent is obvious (you write the brief).
- **Nothing is open.** No `blockedBy`, no `agent:blocked`,
  `agent:needs-scoping` or `decision:required`, and no undecided question in
  the notes (for example "retire the stored references?").
- **It stands alone.** Not a parent with open sub-issues, not one step of a
  chain such as the composite-shell sub-issues.
- **Its area is free.** Map each issue to the code it will touch:
  `crates/kofem-fem/src/shell`, `crates/kofem-shellize`, `engine/cpp`,
  `examples/validation`, `web/src/lib/solve` and the solver worker, a given
  panel, the viewport. At most one pick per area, and none in an area an
  In Progress issue holds.
- **It is not a broad refactor.** Changes to the mesh representation, the
  solve plumbing or cross-cutting cleanups conflict with everything. Name
  them in the report as candidates to run alone.

Prefer `agent:ready` issues, bugs with a repro, tests-only work and isolated
subsystems.

## 3. Brief

Each session starts from its prompt alone. Do not paste the issue; the session
reads it in Linear. Add what the issue does not say:

```text
Work on Linear issue KOF-nn: "<title>". Read the full issue in Linear first
(description and Agent notes). Follow AGENTS.md throughout.

<Scope: what is in, what is out, the files or modules.>

<Done when: the acceptance criteria, or your own if the issue is thin.>

<Guards: anything that must not change, and where to stop and ask.>

Context: other cloud sessions are working in parallel on KOF-aa (<area>),
KOF-bb (<area>) ... Stay out of those areas. <Known conflict risk, if any.>
Branch from develop, target develop, write `Fixes KOF-nn` in the PR
(`Refs KOF-nn` if the acceptance criteria may not be met).

Show the proof in this chat too, not only on Linear. When you post or update
the Linear evidence comment, also send it here: the before/after screenshots
as files (desktop and phone width; look at each one first), the red and
green test output, and the numbers that show the fix (measured vs reference,
before vs after). End with the PR link.
```

The last paragraph goes into every brief. Linear stays the record, but the
user follows the session in its chat and should see the proof there without
opening Linear. For a UI change, the screenshots themselves belong in the
chat, sent as files the user can open (`SendUserFile` in a cloud session),
not just a link to the Linear comment.

Guards worth stating whenever they apply:

- A change that moves solver results must not edit or loosen the stored
  references (`web/tests/fixtures/engine-solves`,
  `examples/validation/oracle-reference.json`). Stop, record the evidence on
  Linear, and ask the maintainer in the PR.
- An open product question in the issue (should the app also warn about X?)
  gets a recommendation in the evidence comment, not an implementation.
- An issue that is in progress separately (name it) is not to be
  restructured.

## 4. Start

Call `create_session` for every pick in one message:

- `source_url`: `https://github.com/mkofler96/KoFEM`, `source_revision`:
  `develop`
- `outcome_branch`: the issue's `gitBranchName`, so Linear links the PR
- `title`: `KOF-nn: <short imperative>`
- `tags`: `["batch:<YYYY-MM-DD>"]`
- leave model, effort and permission mode to inherit

Do not move the issues to In Progress yourself; each session does that
first, per AGENTS.md.

## 5. Report

A table with one row per session: issue, area it touches, why it was picked,
what done looks like. Then one line per notable issue left out and why
(overlap, open decision, chain, broad refactor). Name any remaining conflict
risk between picks. Say the sessions have only just started and give the
batch tag to find them; never describe their progress without checking with
`get_session` or `list_events`.
