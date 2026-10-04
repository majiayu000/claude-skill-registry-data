---
name: sdd-archive
description: >
  Close the SDD cycle: sync delta specs to main specs, merge changes,
  update CHANGELOG, and persist final state. Consolidate, don't discard.
  Trigger: After successful sdd-verify. Never archive with open CRITICAL issues.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  delegate_only: true
---

> **ORCHESTRATOR GATE**: If you loaded this skill via the `skill()` tool, you are
> the ORCHESTRATOR — STOP. Delegate to the dedicated `sdd-archive` sub-agent.
> This skill is for EXECUTORS only.

# Skill: sdd-archive

Archive SDD change. Consolidate and close the cycle.

## Purpose

You are a sub-agent responsible for CLOSING a completed SDD change. You sync delta specs to main specs, merge the change, update documentation, and persist final state.

## What You Receive

From the orchestrator:
- Change name
- Artifact store mode (`engram | openspec | hybrid | none`)
- Verify report status (must be PASS or PASS WITH WARNINGS — never FAIL)

## Execution and Persistence Contract

> Follow **Section B** (retrieval) and **Section C** (persistence) from `skills/_shared/sdd-phase-common.md`.

- **engram**: Read all artifacts for the change. Consolidate into archive report. Save as `sdd/{change-name}/archive-report`.
- **openspec**: Move `openspec/changes/{change-name}/` to `openspec/archive/{change-name}/`. Update main specs with deltas.
- **hybrid**: Do BOTH — persist archive-report to Engram AND move/update filesystem artifacts.
- **none**: Return archive summary only.

## Pre-flight Check

Before archiving, verify:
1. Verify report exists and status is PASS or PASS WITH WARNINGS
2. No CRITICAL issues remain open
3. All artifacts for the change exist (proposal, spec/design, tasks, verify-report)

If any check fails → return `blocked` with reason.

## Step 1: Load Skills

Follow **Section A** from `skills/_shared/sdd-phase-common.md`.

## Step 2: Read All Artifacts

Read every artifact for the change in parallel:

```
mem_search → mem_get_observation for each:
├── sdd/{change-name}/proposal
├── sdd/{change-name}/spec
├── sdd/{change-name}/design
├── sdd/{change-name}/tasks
├── sdd/{change-name}/apply-progress
└── sdd/{change-name}/verify-report
```

## Step 3: Consolidate and Archive

1. **Sync delta specs** → merge spec scenarios from the change into main project specs
2. **Merge changes** → confirm PR/merge to main branch is complete
3. **Update CHANGELOG** → add entry under appropriate version with what changed
4. **Close related issues** → reference the merged PR
5. **Save archive report** → summary of: what changed, why, decisions made, lessons learned

## Step 4: Archive Report Content

```markdown
# Archive: {change-name}

## Summary
{1-2 sentences}

## What Changed
- {change 1}
- {change 2}

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| ... | ... |

## Specs Updated
- {spec file}: added scenario {X}

## Issues Closed
- Closes #{N}

## Lessons Learned
- {non-obvious learning}
```

## Step 5: Return Envelope

```markdown
**Status**: success | partial | blocked
**Summary**: change archived and cycle closed
**Artifacts**: Engram sdd/{change-name}/archive-report | openspec/archive/{change-name}/
**Specs Synced**: yes | no (reason)
**CHANGELOG Updated**: yes | no
**Next**: none (cycle complete)
**Risks**: None | ...
**Skill Resolution**: injected | fallback-registry | fallback-path | none
```

## Anti-patterns

- ❌ Archiving with CRITICAL issues still open
- ❌ Skipping spec sync (deltas lost)
- ❌ Not updating CHANGELOG for user-visible changes
- ❌ Archiving without reading all artifacts first
