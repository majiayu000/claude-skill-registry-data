---
name: harness-hiring
description: "HR hiring. Searches .harness/shared/HR-Resource candidates, installs selected worker skills into .claude and .codex, and records roster wiring."
model: opus
disable-model-invocation: false
---

# Hiring

Hire workers from `.harness/shared/HR-Resource/`.

At effective S, CTO/CQO execute directly and do not hire. COO/CDO deliverables remain worker-backed at every tier. At S/M, OPS observes directly and hires only for recovery or monitoring setup. A role whose `{cxx}.md` is `## Not Applicable` hires nobody.

## Required Inputs

- requester
- needed capability
- mission name
- blocking status
- owning CXX (`cto`, `cqo`, `coo`, `cdo`, or `ops`)
- declared model for the spawn — explicit, never the inherited CLI default

## Workflow

1. Reject any request from CEO to hire or brief a specialist worker directly. Tell CEO to route through the owning CXX.
2. Search `.harness/shared/HR-Resource/*/SKILL.md`.
3. Select the smallest fitting worker.
4. Install it to `.claude/skills/{owning-cxx}/{name}/SKILL.md` and `.codex/skills/{owning-cxx}/{name}/SKILL.md`.
5. Update `.harness/shared/hr-roster.json` without deleting existing hired entries. Record `owner` as the owning CXX, `skillPath` as `.harness/shared/HR-Resource/{name}/SKILL.md`, and `skillPaths.claude` / `skillPaths.codex` as tool-specific hierarchical installed paths.
6. The owning CXX must write worker reports under `.harness/documents/{mission}/{owning-cxx}/workers/{name}.md`. Do not write flat `.harness/documents/{mission}/workers/{name}.md` except when migrating legacy missions.
7. Ask the `harness-resource-manager` skill to update trigger wording.
8. Return worker name, owner, declared model, source skill path, installed paths, mission report path, invocation wording, related convention/gotcha links supplied by the owning CXX, and the instruction to fill the seeded report.

## Worker Rule Links

Every hired worker receives the owning CXX's relevant convention/gotcha links in the worker brief. Workers read those linked topic files only when they match the assigned task.

**Worker brief:** name the seeded report path and instruct the worker to fill its existing sections incrementally. Do not copy the report skeleton, Tally, or Notes block into the brief. Continue to pass relevant corpus links and copy behavioral requirements absent from the seed (including the browser-automation clause) verbatim. Reject briefs missing the seeded report path or applicable behavioral requirements.

## Declared Model

A hire request with no model is incomplete. Record the declared model in `hr-roster.json` alongside `owner` and the skill paths, and return it to the owning CXX for the Worker Evidence Manifest.

A worker terminated by a usage limit is indistinguishable, from the outside, from a worker that finished. When a CXX comes back asking to re-hire a worker whose round went silent, ask for the usage-limit status first: **a silent loop is a rate limit until proven otherwise**, and re-hiring on the same exhausted model family repeats the failure.

## Seeded Report

The owning CXX creates `.harness/documents/{mission}/{owning-cxx}/workers/{name}.md` **before the worker starts**, seeded from `.harness/shared/templates/worker-report.md` with every required section already present, and briefs the worker to fill it in incrementally. A worker killed mid-round must leave a valid partial report, never a stub. Do not report a hire as complete while the report file has not been seeded.

## Mandatory Worker Report Appendix

The mandatory appendix already exists in the seed template. Return its report path and require the worker to fill risks, self-corrections, chosen direction, and unresolved questions in the existing four Notes subsections (`None` when empty). Do not copy the template into the assignment.

Never mark a missing worker as available.
