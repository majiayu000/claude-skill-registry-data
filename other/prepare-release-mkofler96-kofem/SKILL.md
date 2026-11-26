---
name: prepare-release
description: Analyze KoFEM changes and readiness, recommend a version, and create or refresh a Linear release parent with actionable sub-issues and a release label. Use for prepare release, release planning, or a release checklist; this does not bump versions or open the release PR.
---

# Prepare release

Turn a release request into one reviewable Linear plan. Follow
[the shared assessment](../release/references/assessment.md) first. Run only
when requested by the maintainer. This invocation authorizes writing the plan
and its tasks; no second confirmation is needed for those writes.

## 1. Find or reuse the plan

Discover the KoFEM team/project and existing issue labels through Linear.
Search for the target version, release parent, and existing open release plans,
including archived results when checking for an already published version.
Read matching descriptions and relations before creating anything.

Use a parent named **Prepare vX.Y.Z release**, with the marker
`<!-- kofem-release-plan -->` in its description. Use one team-scoped label
**release/vX.Y.Z** on the parent, its subtasks, included feature/fix issues,
and release blockers. This is a Linear label, never a Git tag.

Reuse the matching parent and label on subsequent runs. If the proposed version
changes for the same open candidate, update that plan in place and migrate its
release label memberships; do not create a second plan or rename a label used
by another release. If several plans could match, ask which one before writing.
Do not reopen a completed or canceled plan without the maintainer's instruction.

## 2. Record the assessment

Create or update the parent's assessment section using the template below.
Preserve maintainer notes, decisions, completed-task evidence, and unrelated
content. Use targeted edits when refreshing a section. Keep the full commit SHA
and CI links, so the next invocation can detect stale evidence.

```markdown
<!-- kofem-release-plan -->

## Candidate

- Target: vX.Y.Z; why this version
- Base: last product tag and release date
- Assessed develop: full SHA and assessment date
- Readiness: GO / WAIT / NO-GO, with reason and exact-head CI link
- Release label: release/vX.Y.Z

## Scope

- Included: user-facing changes with merged PR and Linear links
- Required before release: unmerged fixes and manual checks
- Deferred: related work excluded from this candidate, with reasons

## Numerical and compatibility notes

- What moved, why, validation evidence, and required user action
- Draft Changed / Breaking notes, including known limitations

## Release prerequisites

- Existing blockers: linked issues, expected evidence, and current status
- New checks: linked sub-issues and their acceptance criteria

## Handoff

When prerequisites are complete, invoke create-release with this issue.
It must recheck current develop, CI, scope, version, and task evidence.
Keep this parent open until CI publishes the product release after promotion.
```

## 3. Connect actionable tasks

Reuse existing issues for defects and work already tracked. Add the release
label without replacing other labels. Add them to the parent's `blockedBy`
relations when they block this release; preserve its existing dependencies.
Keep their current parents, projects, assignees, priorities, and statuses.
Do not reparent them or create duplicate "fix KOF-nn" subtasks.

Create a sub-issue only for missing release-specific work. Each needs a concrete
result, context/source links, and acceptance criteria describing evidence that
will establish completion. Set `parentId` to the release parent, use the same
project and release label, and make it block the parent. Do not invent owners
or deadlines. Examples, only when the assessment makes them relevant:

- Reproduce a reported regression and resolve it with a merged fix or evidence
  that the candidate is unaffected.
- Verify GA4's key event, dimensions, and funnel configuration; record evidence
  without credentials or user/model data. Mark manual work explicitly.
- Verify numerical/compatibility changes against their production regression
  results and draft the user action for the release notes.

Search the parent's children and the release label before adding each task.
Refresh an existing task instead of creating a new one on every run. A canceled
or duplicate task is not automatically completed: follow its replacement or
record the maintainer's explicit scope decision. Checkboxes without evidence
do not establish readiness. Never mark engineering work Done on its behalf.

Do not add "create release PR" or "publish release" as prerequisites for
`create-release`: that would make its readiness gate circular. They belong in
the parent's Handoff section.

## 4. Finish

Read back the parent, label memberships, children, and blocking relations.
Report its link, proposed version, readiness, and the next outstanding tasks.
If part of a write fails, report what succeeded and retry by ID after readback;
do not recreate the plan. If Linear is unavailable, return the concrete plan
inline and identify the unsaved work; do not claim it was created.

Preparation does not change versions, `CHANGELOG.md`, code, tags, releases,
external service configuration, or PRs. A later explicit `create-release`
invocation authorizes the release PR; finishing tasks does not trigger it
automatically.
