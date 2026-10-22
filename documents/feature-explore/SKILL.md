---
name: feature-explore
description: >-
  Interviews for the problem behind a new Umbraco feature or package: what, for whom, why,
  and what's out of scope, written to BRIEF.md. Use when starting a feature, package or
  add-on, or when a request is too vague to design yet.
user-invocable: true
argument-hint: [one-line idea, optional]
---

# feature-explore

Think through an idea before touching the solution space. By the end, the feature's `BRIEF.md`
says what's being built and for whom, honestly including what isn't known yet.

## Where this writes

The project's per-feature plan folder — see the root `CLAUDE.md` for the path convention
(default `docs/plans/<feature-slug>/`; a monorepo or worktree-based project may scope it
differently). If no convention is written down anywhere, ask once, then propose one and add it
to `CLAUDE.md` so the next phase doesn't have to ask again.

Owns exactly one file: `BRIEF.md`. Never edit `ARCHITECTURE.md`, `SPEC.md`, `STORIES.md`,
`PLAN.md`, or `BUILD-LOG.md` — those belong to later phases.

**Also creates `README.md`, the folder's read-order index — the one time any phase creates
it.** Every later phase updates its own line in this file when it finishes (same append-only
discipline as `DECISION-LOG.md`): never recreate it if it already exists, and never edit a line
that isn't `BRIEF.md`'s own.

**Stays uncommitted, stays on trunk.** `feature-explore` never runs `git commit`, never creates a
branch. The plan folder is just plain files on disk until `feature-build` decides the feature
is actually being built — see "Branch/worktree per feature" in `git-workflow` for why. If the
feature never gets built, nothing ever touched git history.

**Why one file per phase, not one shared doc:** re-running a phase must never silently
overwrite another phase's decisions, and two files can't collide the way two sections in one
shared file can — a phase editing its own file is safe to run concurrently with another phase
(or another session) touching a different one. If a project already has its own plan-folder
convention, match it for consistency, but keep the same discipline (one owner per file) rather
than going fully freeform.

## Scope

- IN: the problem, the user (an editor? a developer integrating the package? an end site
  visitor?), the why-now, in/out scope, what success looks like, unknowns, light research
  where a fact is needed to proceed.
- OUT: architecture, CMS extension points to use, data model, package structure — all
  `feature-design`. If a solution idea comes up mid-interview, park it under a `> ASSUMPTION:`
  or note in the non-goals section rather than deciding it here.

## Preflight

1. Resolve which feature this run is for. If more than one plan folder exists, prefer a match
   between the current branch/worktree name and a folder name (see `CLAUDE.md`'s "Finding the
   current feature's plan folder" rule) — this is the normal case for a refinement run once
   `feature-build` has started. If nothing matches and only one plan folder exists, or the
   argument names a brand-new idea, use that instead; ask only if it's still ambiguous. If
   the argument is a tracker issue (title, body, triage findings, repro, notes), treat it as
   a brand-new feature and use it to answer interview questions up front. A bug's repro goes
   in `BRIEF.md`'s `Repro` section. If the argument is an idea file (see `CLAUDE.md`'s
   "Ideas"), treat it the same way: it's a brand-new feature, and the idea answers questions
   up front. An idea can cover more than one feature, so ask which part this one builds.
   Refer to the idea by its name alone, never its path (see "Ideas").
   If
   `BRIEF.md` already exists in the resolved folder, read it. Summarize current state in 1–2
   lines ("problem defined, no success metric yet"). Re-entrant: refine, don't restart. **Skip
   step 2 below** when refining an existing `BRIEF.md`.
2. **Only for a brand-new feature (no `BRIEF.md` yet):** confirm the current branch is the
   project's trunk branch (see `CLAUDE.md`'s Feature workflow section; default the repo's
   default branch). If it isn't, stop and tell the user — starting a new plan folder from an
   unrelated branch is how plan folders end up scattered across branches they don't belong to.
   Let them override if they confirm it's intentional (e.g. planning a sub-feature inside a
   monorepo product's own long-lived line). Also check the archive (see `CLAUDE.md`'s
   "Feature workflow" section) for a closed plan with the same slug. If one exists, pick a
   different slug: the slug is also the branch name, and an archived plan's links and PR
   still use it.
3. Read the project's `CLAUDE.md` and any existing architecture docs for prior context —
   don't re-litigate a decision already on record.
4. If this is a package/add-on (not a feature inside an existing product), check whether it's
   extending an existing Umbraco extension point (property editor, dashboard, content app,
   notification handler) or introducing a new one — that framing shapes several of the
   interview questions below.

## Assume, then show

Not every topic below needs a spoken question. Before asking:

1. **Check whether it's a checkable fact** — does Umbraco core already expose this, how does
   a sibling package handle it — and go find it instead of asking.
2. **If it's a judgment call and a wrong guess is cheap to correct once it's written down**
   (a scope boundary, a success metric, the smallest shippable slice), write it as
   `> ASSUMPTION: ...` under the relevant section of `BRIEF.md` instead of asking, and let the
   human correct it when they read the brief. Correcting a written-down guess costs them a
   sentence; answering a live question costs them a context switch.
3. **Ask directly only when a wrong guess is expensive to undo here** — which CMS version(s)
   to support (locks in a compatibility promise you'd have to walk back), or anything only the
   human can actually know (why this, now; what would kill it).

This doesn't relax "stop, don't guess" — that rule is about a phase's *required input* being
missing (no prior phase's file to read). This is about which of *this* phase's own questions
you put to the human versus answer yourself and show your work.

## Interview

Up to ~10 questions, adaptive — only ask what's missing **and fails the filter above**. Batch
what's left (4 at a time, 2–3 rounds, not an interrogation):

1. What problem, concretely? What does an editor/developer do today without it?
2. Who is it for? Backoffice editors, developers consuming the package, front-end site
   visitors, or some mix? Who is explicitly *not* the audience?
3. Why now?
4. What's explicitly **out** of scope?
5. What does success look like — observable, ideally measurable?
6. Hard constraints: which Umbraco CMS version(s) must this support? Any locked
   dependencies?
7. What's the riskiest unknown — a CMS API that might not do what's assumed, a UUI
   component that might not exist yet, a performance ceiling?
8. What's the smallest version that's still worth shipping?
9. Is this replacing or extending something that already exists in Umbraco core or another
   package?
10. What would make you kill this?

Do targeted research only when an answer hinges on a checkable fact (e.g. does Umbraco core
already expose the extension point this needs). Check Umbraco's docs with `umbraco-docs`
and the CMS itself with `umbraco-cms-source`.

## Produce

Write every file this phase produces following `plain-writing`: a person reads it before the
next phase runs, so it should be quick to read without leaving anything out.

**First run only (`README.md` doesn't exist yet):** create it as the folder's index:

```md
# <Feature name>

Read these in order:

1. [ ] [BRIEF.md](./BRIEF.md) — <pending>
2. [ ] [ARCHITECTURE.md](./ARCHITECTURE.md) — <pending>
3. [ ] [SPEC.md](./SPEC.md) — <pending>
4. [ ] [STORIES.md](./STORIES.md) — <pending>
5. [ ] [PLAN.md](./PLAN.md) — <pending>
6. [ ] [BUILD-LOG.md](./BUILD-LOG.md) — <pending>

See [DECISION-LOG.md](./DECISION-LOG.md) for why things changed along the way.
```

Every run (first run or a refinement), update only the `BRIEF.md` line: check its box and
replace `<pending>` with one plain-English line summarizing the current problem. Never touch
any other phase's line.

When revising an existing `BRIEF.md`, rewrite the affected sections to reflect the current
understanding only — don't leave the old answer in place alongside a note about what
changed. This file is a snapshot of the current problem definition, not a changelog. Past
answers and why they changed belong in `DECISION-LOG.md`.

Write/update `BRIEF.md`:

```md
# Brief

Source idea: `<idea-name>`, <which part of it this feature builds>
<only when the feature started from an idea. Leave the line out otherwise.>

## Problem
<what, who, why-now, success criteria, constraints, riskiest unknowns. A guess you're showing
the human is `> ASSUMPTION: ...`. Something genuinely unresolved that needs a real decision,
not just a correction, is `TODO`.>

## Non-goals
<explicitly out of scope, and why>

## Repro
<only for a reported bug: the steps or test that show it. The finished work must make it
pass. Leave the section out otherwise.>
```

Append a dated entry to `DECISION-LOG.md` for anything decided here worth remembering later
(a scope cut, a killed alternative), one line each with the why. If a decision is project-wide
rather than scoped to this feature (a constraint that will bind every future feature too, not
just this one), write it to `.claude/memory/` instead (type: `decision`) — see
`.claude/memory/README.md` for the format.

## Hand off

State what's still `TODO`, then: `Suggested next: feature-design — or re-run feature-explore
to close open questions first.`
