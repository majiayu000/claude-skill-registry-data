---
name: tiny-spec-create
description: Start or update a spec — capture intent and requirements into .spec/<slug>/SPEC.md, optionally bound to a ticket (or ad-hoc). On first run, scaffolds .spec/ and seeds the shared constitution (constitution.md). If a BREAKDOWN.md (from tiny-spec-scope) is present, seeds the spec from a chosen feature instead of a full interview. Re-run to update an existing spec in place.
---

# tiny-spec-create

Captures **what** the user wants and **why**, as testable `REQ-N` requirements.
This is the front door of the per-ticket flow. A spec can be bound to a ticket or worked
**ad-hoc** — both are first-class.

The suite works **one spec at a time**, namespaced per spec. Artifacts live under
`.spec/` in the **project root** (the user's cwd) — never in this skill's directory. Two
are **project-wide** and shared at the `.spec/` root (`constitution.md`, `memory.md`);
the per-spec ones (`SPEC.md`, `PLAN.md`, `decisions.md`) live under
`.spec/<slug>/`. The `SPEC.md` and `constitution.md` skeletons are inline below — write
them from there, no files to read.

## Pick your mode first — before doing anything else

**Decide which mode you are in before you ask a single question, create a directory, or
touch git** — each mode forbids side effects the others require, so getting here late
means the damage is already done.

Check in this order; the first match wins:

| # | If | Mode | Go to |
|---|----|------|-------|
| 1 | `.spec/` exists but `.spec/constitution.md` does **not** | **reseed** | [Reseed a missing constitution](#reseed-a-missing-constitution) — repair only, then stop |
| 2 | `.spec/` does not exist | **fresh** (first run) | Seeded mode if `BREAKDOWN.md` exists, else Pick the slug → First run — scaffold → Write `SPEC.md` |
| 3 | the active spec's `SPEC.md` already exists | **update** | [Update mode](#update-mode-re-run-on-an-existing-spec) — edit in place, never overwrite |
| 4 | otherwise (new spec in an existing `.spec/`) | **fresh** (new spec) | Seeded mode if `BREAKDOWN.md` exists, else Pick the slug → Write `SPEC.md` |

Rule 1 outranks everything, including **Seeded mode** — a missing constitution is a
repair, and repairs don't create work items. Rule 3 outranks rule 4 so that a re-run on
existing work can never overwrite it.

To evaluate rules 3 and 4 you need the **active spec dir**. Resolve it **read-only**
first (see *Pick the slug* for the shared resolution order). Only *create* a dir once
you know you're in a fresh mode.

**If the user (or `tiny-spec-run`) says this is new work, skip the sole-dir fallback**
and go to rule 4. That fallback exists to find the ticket you're already on; letting it
match when someone asked for a *new* spec quietly retargets the run onto an old ticket
and marks its downstream artifacts stale for no reason.

## Reseed a missing constitution

Check this **before** anything else. The constitution is project-wide, so it can go
missing — deleted, or never committed — while a perfectly good `.spec/<slug>/` sits next
to it. Then it is unrecoverable: the scaffold below never fires, `tiny-spec-plan` only
*hardens* an existing one, and `tiny-spec-build` would inject nothing.

**If this repo already contains real source code, hand off to `tiny-spec-adopt`** — it
derives the constitution from the code itself, which beats anything reconstructible from
here. Say so and stop; that skill also handles the staleness propagation below.

Otherwise (little or no code yet), do **only** this:

1. Resolve the active spec dir **read-only** — you may need its `SPEC.md`. There may be
   none; that's fine.
2. Write `.spec/constitution.md` using the skeleton in **First run — scaffold** below,
   filled in from whatever already exists, in this order of preference: a `BREAKDOWN.md`
   `## Decisions` block at the project root if there is one (Stack + Code-lives →
   **Style** and **Layout**; verification hints → **Verification commands**;
   cross-cutting → **Guiding invariants**), then the active `SPEC.md`, then the codebase
   itself. A *declared* source beats inference. Ask the user only what you genuinely
   cannot infer.
3. **Flag downstream work as unverified — across every spec, not just the active one.**
   The constitution is project-wide, so *any* `[x]` task in *any* `.spec/*/` was built
   and reviewed against a document that did not exist. For each spec dir whose
   `PLAN.md` has checked tasks, set it `status: stale` and log a `decisions.md` entry
   in that spec (`type: change`) saying the constitution was reseeded and the completed
   tasks were never checked against it.
4. Report what you seeded, say plainly that it was **inferred and needs review** (it
   gets injected whole into every executor and reviewer, so a wrong Verification
   commands block silently corrupts every future gate), note that `SPEC.md`/`PLAN.md`
   and the branch were left untouched, and point the user at `tiny-spec-plan` to harden
   it. Then stop.

Do **not** run the interview, create a spec dir, switch branches, or touch `SPEC.md`.
This is a repair, not a new spec.

## Seeded mode (`BREAKDOWN.md` present)

**Fresh modes only** — reseed (rule 1) and update (rule 3) both outrank this.

Before interviewing, check for **`BREAKDOWN.md`** at the project root (written by
`tiny-spec-scope`). If it exists and the user is creating one of its features, **seed from
it instead of running the full interview** — confirm, don't re-ask:

1. **Pick the feature.** Ask which feature (or infer from the user's request); match it
   to its `## Feature:` entry by slug or title.
2. **Slug + binding.** Use the feature's **slug** for `.spec/<slug>/`. Take the ticket
   provider from the Decisions **Platform** and the **id** from the feature's
   `(tracker: …)` or the user (ask for the id if the placeholder is still blank; omit the
   `ticket:` block entirely if the platform is ad-hoc).
3. **Requirements.** Promote the feature's **`AC:` lines into `REQ-N`** — verbatim where
   already atomic; split any that hide two capabilities behind an "and".
4. **Constitution (first run only).** Seed `constitution.md` from the **`## Decisions`**
   block instead of interviewing stack/layout: Stack + Code-lives → **Style** and
   **Layout**; any verification hints → **Verification commands**; cross-cutting
   concerns → **Guiding invariants**. If `constitution.md` already exists, reuse it.
5. **Designs.** If the feature carries `design:` paths, note them and point the user at
   **`tiny-spec-design`** — that skill reads the files and writes this spec's `D<n>`
   entries against a token system. Don't describe the screens here.
6. Confirm the captured `REQ-N` with the user, then write `SPEC.md` as below.

Only the **project-wide** questions collapse — still confirm this feature's binding and
requirements. If there is **no `BREAKDOWN.md`**, or no entry matches, run the **full
interview** below unchanged.

**Exception — a feature run.** If the caller says this is a **feature run** and names the
feature's slug (`tiny-spec-run` does, in build-through mode), skip step 6's confirmation
and write `SPEC.md` straight out. The `AC:` lines *are* the approval: the user reviewed
them when they wrote or accepted `BREAKDOWN.md`, and re-confirming them once per feature
is asking the same question twice — across a seven-feature run it is the difference between
walking away and being interrupted seven times. Report the captured `REQ-N` instead of
asking about them.

This waives **only** that confirmation. Everything that is a genuine question still stops
the run: a feature whose `AC:` lines contradict each other or the Decisions block, an `AC:`
you cannot turn into a testable `REQ-N`, a missing ticket id the platform needs, a design
export the feature names that isn't on disk. Those are not ceremony — they are the human
input the run is supposed to stop for. Never guess past one because a run is in progress.

## Pick the slug (resolve the active dir)

**Fresh modes only** — in reseed or update mode the active dir already exists and you
resolve it read-only, as above. Do not run this section.

**If a spec dir already resolves for the current branch, reuse it — don't invent a new
slug.** Asking for a slug when `.spec/PROJ-123/` already matches the branch is how you
end up with both `PROJ-123/` and `dark-mode/` matching `feature/PROJ-123-dark-mode`,
which makes the ticket permanently ambiguous for every downstream skill.

Each spec lives in its own directory `.spec/<slug>/`. At the start of the interview,
establish the slug. There are two paths — both are first-class:

- **Bound to a ticket.** Ask for the **provider** (`jira | github | ado | monday`),
  **id**, **url**, and optionally the current **status**. Derive the slug from the
  platform key: verbatim when filesystem-safe (`PROJ-123`); otherwise normalize —
  GitHub `#42`→`gh-42`, Monday item→`monday-<id>`, ADO `AB#77`→`ado-77`.
- **Ad-hoc (no ticket).** Perfectly supported — just confirm there's no ticket and use a
  short kebab-case slug of the feature name (e.g. `dark-mode`, `perf-pass`). The SPEC
  omits the `ticket:` frontmatter block, and commits drop the `Refs:` footer (everything
  else — namespacing, the constitution, the build loop — is identical). You can bind a
  ticket later by adding the block to `SPEC.md`.

Create `.spec/<slug>/`.

**One branch per spec — how the active spec is resolved.** Work lives on a branch named
after the slug (e.g. `PROJ-123` or `feature/PROJ-123-dark-mode`); downstream skills
resolve the active spec from the branch name, so several can be in flight on separate
branches at once. If the user isn't already on such a branch, create one (e.g.
`git switch -c <slug>`) so the new spec resolves by branch match.

## First run — scaffold

If `.spec/` does not exist:

**If this repo already contains real source code, run `tiny-spec-adopt` first.** It
derives the constitution from the actual lint/test/build commands, layout, and
conventions — an interviewed constitution on an existing codebase is how you get a gate
that names commands the project doesn't have. Come back here for the spec itself.

Otherwise:

1. Create `.spec/` and the active spec dir `.spec/<slug>/` (on the spec's branch — see
   above).
2. **Short interview** (keep it short — earned ceremony):
   - the ticket binding (above);
   - the intent in one paragraph;
   - the language/stack and where code lives;
   - the must-have requirements (the capabilities, not the design).
3. Seed the **shared constitution** at `.spec/constitution.md` (the **root**, not the
   spec dir — it is project-wide), filling in what the interview or a `BREAKDOWN.md`
   `## Decisions` block already told you (Style, Layout, Verification commands at
   minimum). Leave the rest for `tiny-spec-plan` to harden — but never leave a section
   empty of intent. If `constitution.md` already exists (a prior spec created it),
   **reuse it** — do not overwrite the project's constitution. Write it with this
   structure (drop the indentation when you write the file):

   ```markdown
   # Constitution

   > This is the strongest, most persistent document in the project. It is
   > **project-wide** — it lives at the `.spec/` root and anchors *every* spec, not
   > any one of them. Every task is implemented and reviewed against it. Keep it true;
   > keep it lean. Project-specific richness belongs here — not scattered across tasks.

   ## Style
   <Formatting, naming, language idioms. The defaults a reader should assume.>

   ## Engineering standards
   <Error handling, logging, testing approach, dependency policy, what "tested" means here.>

   ## Guiding invariants
   <The non-negotiables. "Never X." "Always Y." The rules a reviewer can fail a task on.>

   ## Glossary
   <Domain term — one-line definition. Keep the team speaking one language.>

   ## Layout
   <Where things live. Directory map. Where new code of each kind goes.>

   ## Definition of Done
   <The bar a task must clear to be checked off: e.g. code + tests + docs updated,
   gate green, no TODOs left, matches the invariants above.>

   ## Verification commands
   <The exact gate. The reviewer runs these. Omit any stage this project doesn't have.
   - install: `...`
   - lint:    `...`
   - test:    `...`
   - build:   `...`
   - run:     `...`
   >
   ```

   **A `## Design system` section is `tiny-spec-design`'s** — leave it absent here. A
   dead design heading on a CLI or library is worse than none: it gets injected into
   every executor and reviewer prompt for the life of the project.

## Write `SPEC.md`

Write `.spec/<slug>/SPEC.md` with the structure below, filling it in:

```markdown
---
status: current
updated: <ISO date>
# Ticket binding (reference-only). Omit this whole block if there is no ticket.
ticket:
  provider: jira | github | ado | monday
  id: <PROJ-123 | #42 | AB#77 | item id>
  url: <link to the ticket>
  status: <optional manual mirror of the platform status, e.g. In Progress>
---

# <Project / feature name>

<!-- optional: omit if N/A -->
## Context

<Why now — the background, the problem, what prompted this. No solution detail.>

## Intent

<One paragraph: what this is and why it exists. The "what" and "why", never the "how".>

## Requirements

<Each REQ is one user-observable, testable capability. No implementation detail.
If a line hides two capabilities behind an "and", split it.>

- REQ-1 — <capability>
- REQ-2 — <capability>
- REQ-3 — <capability>

<!-- optional: omit if N/A -->
## Non-goals

<What this explicitly does NOT cover — scope boundaries that prevent creep.>

<!-- optional: omit if N/A -->
## Success criteria

<How we'll know the whole spec succeeded, beyond the per-requirement acceptance —
e.g. a metric, an end-to-end scenario, a stakeholder sign-off.>

<!-- optional: omit if N/A -->
## Open questions

<Unresolved questions that may change requirements. Resolve before/while planning.>

<!-- optional: omit if N/A -->
## Links

<Ticket, related specs, design docs, prior art.>
```

- the **ticket binding** frontmatter block (or omit it if there's no ticket);
- a one-paragraph **intent**;
- a `## Requirements` list — each `REQ-N` a single **user-observable, testable**
  capability with **no implementation detail** ("the CLI accepts a `--json` flag and
  prints valid JSON", not "add a json module");
- the optional sections (`Context`, `Non-goals`, `Success criteria`, `Open questions`,
  `Links`) where they add value — omit any that don't apply.

Number requirements `REQ-1, REQ-2, …`. Keep each atomic — if a line has an "and" that
hides two capabilities, split it.

**If this spec has a visual surface**, run **`tiny-spec-design`** afterwards. It adds a
`## Design` section — one `D<n>` per screen, written against a project-wide token system
— and arms the visual gate. Don't write screen descriptions here; a description not
anchored to tokens is how per-screen drift starts.

## Update mode (re-run on an existing spec)

When the active spec's `SPEC.md` already exists and the user wants a change to
requirements (resolve the active dir by branch match):

1. Edit `.spec/<active>/SPEC.md` in place — add/alter/remove `REQ-N`, preserving existing
   ids where the requirement still exists.
2. Flip downstream **stale**: set `PLAN.md` frontmatter to `status: stale` (if it
   exists).
3. Log it: append a `decisions.md` entry to `.spec/<active>/decisions.md`, using the
   fixed skeleton (`type: change`, the affected `REQ-N`). Create the file if absent:

   ```
   ## D-NNN — <short title>
   - type: change
   - date: <ISO date>
   - affects: REQ-N
   - note: <what changed + why>
   ```

4. **Completed-work guardrail.** If a changed `REQ-N` is delivered by a task already
   `[x]` in `PLAN.md`'s `## Tasks` (follow its `req:` field), **uncheck it** and name the unchecked
   ids in the same `decisions.md` entry. `tiny-spec-build` resumes from the checkbox
   state, so a task left `[x]` is a task it will never revisit — never assume built work
   survived a requirement change.
5. Set `SPEC.md` `status: current` and bump `updated`. **Do this even if it was already
   `current`.** `SPEC.md` is the root of the chain and no other skill in the suite writes
   that flag, so a hand-edited `stale` SPEC is otherwise unclearable and the chain jams
   at the root.

If the spec has a `## Design` section and the change touches a screen, hand off to
**`tiny-spec-design`** — it owns those entries and their staleness hashes.

Tell the user which downstream docs went stale and to re-run `tiny-spec-plan` to
reconcile.

> **New spec?** To start a different piece of work, re-run this skill on a new branch —
> it creates a new `.spec/<slug>/` that resolves by branch match. The shared
> `constitution.md` and `memory.md` carry over; the previous spec's artifacts stay
> untouched on disk.

## When done

Report the requirements captured and point the user at `tiny-spec-plan` (or
`tiny-spec-design` first, if this spec has screens to anchor).
