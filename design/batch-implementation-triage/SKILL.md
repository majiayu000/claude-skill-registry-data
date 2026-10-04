---
name: batch-implementation-triage
description: Use when a list of open GitHub issues has to be filtered before automated or batch implementation — separating issues already landed on main, issues an open pull request already claims, issues whose scope is UI/UX and needs a design gate, and issues that are destructive or change live repository settings and need a runbook plus explicit human approval.
---

# Batch Implementation Triage

## Profile keys consumed

- `project.repo`
- `capabilities.figma`

## Overview

Before implementing a queue of issues, classify each one exactly once. Three filters exclude work
that must not be automated (already done, already claimed, design-gated), and a fourth flag marks
qualifying work that still needs human approval because it destroys data or changes live settings.

## When to use

- A batch implementation run is about to be launched over many open issues.
- Deciding which issues an agent may implement unattended and which must be deferred.
- Reviewing a triage output for consistent filtering before work starts.
- An issue in the queue would delete tags or branches, or change repository/org settings.
- Not for: implementing a single, already-scoped issue — triage is only worth its cost on a batch.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — `gh` against `project.repo` for issue and pull-request state; UI-scoped issues
  route to the [figma-design-check skill](../figma-design-check/SKILL.md) before any code is
  written.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — same `gh` flow and the
  same design-check skill.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial — same
  triage, but no tracked design-check skill, so the design gate is a manual reference review rather
  than a skill invocation.

## Classification

Apply the tests in order; the first one that matches decides the category.

1. **An open pull request already claims it** → excluded. Link the pull request on the issue and
   wait for the merge; do not duplicate the work.

   ```bash # profile-example
   gh issue view <n> --json title,url
   gh pr list --search "<n> in:body" --state open --json number,title,headRefName
   ```

2. **Already implemented on `main`** → excluded. Close as superseded. Prove it against the branch,
   not from memory: search the merged history and the file the issue asks for.

   ```bash # profile-example
   git log origin/main --oneline --grep '<n>'
   git show origin/main:.github/workflows/<gate>.yml
   ```

3. **Scope includes UI or UX change** → excluded from the unattended queue. Component redesign,
   palette or contrast changes, layout, interaction patterns, form labels, and ARIA all belong
   behind the design check. Route them there instead of guessing at the design.
4. **Otherwise** → qualifying. It goes into the batch.

## Design-check gating

The UI/UX filter routes to the design check driven by `capabilities.figma`. When that flag is
`false` the routed issue is not silently returned to the queue: skip the tooling step with a
recorded capability-absent note and hold the issue behind a manual design review instead.

## Manual approval gates

Two kinds of qualifying issue still need a written runbook and explicit human sign-off before
anything executes. Produce the script and the rollback steps, then stop and ask.

- **Destructive**: deleting release tags, orphaned branches, deprecated schemas, or stale cloud
  resources. Outward-facing and not undoable by a revert.
- **Live settings**: branch rulesets, required status checks, org settings, IAM trust policies,
  workflow permissions. Run the tool's dry-run mode first, diff it against the current state, and
  name the cascade risks (a new required check blocks every open pull request the moment it lands).

## Triage summary

Report the batch as counts plus the qualifying list, so the excluded categories are auditable.

| Category            | Action                                             |
| ------------------- | -------------------------------------------------- |
| Qualifying          | Implement; flag any needing a manual gate          |
| Already implemented | Close as superseded, citing the commit or workflow |
| Needs UI/UX         | Defer to the design gate                           |
| Open pull request   | Link the pull request; await merge                 |

## Common mistakes

- Trusting the issue's own state — an issue stays open long after its gate landed; check `main`.
- Reading "adds a check" as non-UI — a contrast or label fix is a UI change however it is worded.
- Treating a dry-run as approval — the dry-run is evidence for the human, not a substitute.
- Implementing an issue a stale pull request claims, producing two conflicting branches.
- Counting an issue in two categories, which makes the totals unreconcilable at review time.
