---
name: project-reconciliation
description: |
  Reconcile a processkit project’s migrations, health findings, and
  repository collaboration queue. Use when resolving all migrations,
  pk-doctor findings, GitHub issues, pull requests, or release blockers.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-project-reconciliation
    version: "1.0.0"
    created: 2026-07-21T19:30:00Z
    category: processkit
    layer: 4
    uses:
      - skill: migration-management
        purpose: "Query and resolve pending or in-progress migrations through their state-machine tools."
      - skill: pk-doctor
        purpose: "Build and remediate the repository-health queue from errors, warnings, and actionable findings."
      - skill: repo-management
        purpose: "Plan and apply guarded issue, pull-request, local-commit, and push reconciliation."
    provides:
      processes: [project-reconciliation]
    commands:
      - name: pk-reconcile
        args: "scope (optional: all, session-start, migrations, doctor, repo, report-only)"
        description: "Reconcile a project's migration, health, and repository queues with guarded remediation."
---

# Project Reconciliation

## Intro

Use `/pk-reconcile` to turn the recurring cleanup request into one guarded
workflow. It owns the combined migration, pk-doctor, issue, and pull-request
queues; the specialist skills continue to own their individual remediations.

## Overview

### Select a scope

| Scope | Behaviour |
| --- | --- |
| `all` (default) | Reconcile migrations, doctor findings, and repository queues. |
| `session-start` | Resolve safe migrations and health work; inventory GitHub state without closing issues or merging pull requests. |
| `migrations` | Resolve only pending and in-progress migrations. |
| `doctor` | Resolve the pk-doctor remediation queue. |
| `repo` | Run guarded repository reconciliation for issues, pull requests, local commits, and push readiness. |
| `report-only` | Inspect every selected queue and make no changes. |

### Reconcile in order

1. **Migrations.** Apply or continue unambiguous migrations; reject clearly
   malformed no-op migrations. Ask before policy-changing, destructive,
   ambiguous, conflicting, or externally blocked changes.
2. **Health.** Run `pk-doctor`; build a queue from every ERROR, WARN, and
   actionable INFO. Use the owning tool to fix safe, unambiguous findings,
   then rerun the doctor.
3. **Repository.** Run `pk-repo-reconcile` in plan mode. Resolve issues only
   with evidence and merge only non-draft pull requests that satisfy branch
   protection and checks. Obtain the existing confirmation tokens before
   external close or merge actions.
4. **Report.** Rerun the selected checks. State what was fixed, what remains,
   the owner or blocker for each remaining item, and the next exact action.

`/pk-resume` invokes `pk-reconcile session-start` before generating its
briefing. It does not repeat the reconciliation logic or silently close an
issue or merge a pull request at session start.

## Gotchas

- **Treating every finding as safe to auto-fix.** Errors, warnings, and
  actionable INFO are a queue, not blanket permission. Preserve the owning
  skill's confirmation and state-machine rules.
- **Closing GitHub issues because a related change exists.** Link concrete
  evidence and use the repository tool's required confirmation; otherwise
  leave a proposed resolution in the report.
- **Merging a pull request merely because it is open.** Draft state, missing
  checks, unresolved comments, and branch protection remain hard blockers.
- **Running full repository mutation during pk-resume.** Session start may
  inspect GitHub state, but external close and merge actions require the
  explicit full reconciliation scope and its confirmations.
- **Reporting doctor totals without action totals.** A zero-WARN result is
  not clean if actionable INFO remains. Always account for both queues.
- **Moving migration files by hand.** Use migration-management tools so
  validation, state transitions, and audit events remain consistent.

## Full reference

### Completion contract

Report each selected queue using this shape:

```text
Scope:
Resolved:
Remaining:
Blocked or confirmation-required:
Recheck evidence:
Next action:
```

`all` is complete only when every selected item is fixed, explicitly
deferred with a reason, linked to evidence or a tracking item, or reported as
blocked by missing authority or external state.

### Anti-patterns

- **Replacing specialist remediation with a generic script.** Delegate to
  the migration, doctor, and repository owners; this skill coordinates order
  and reporting only.
- **Treating a plan as execution.** A dry run is valuable but does not resolve
  work. Say clearly which mutations were applied and which require approval.
- **Hiding an external blocker.** Missing authentication, branch protection,
  or a required reviewer is an actionable result, not a clean outcome.

### Cross-references

- `migration-management` — migration state transitions
- `pk-doctor` — health finding remediation
- `repo-management` — guarded issues, pull requests, commits, and pushes
