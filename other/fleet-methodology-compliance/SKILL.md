---
name: fleet-methodology-compliance
description: How fleet-ops detects methodology violations during review — code during analysis, skipped stages, readiness jumps, missing contributions. The quality enforcement backbone.
---

# Methodology Compliance — Fleet-Ops Quality Backbone

Your review is the last gate before "done." The methodology exists to ensure agents think before they build. Your job is to verify they followed it — not just that the code works, but that the PROCESS was sound.

## What You're Checking (5 Compliance Dimensions)

### 1. Stage Traversal

Every task should progress through stages in order. A task that jumps from conversation (readiness 10) to work (readiness 99) without analysis or reasoning skipped the thinking.

**How to check:** Use `acct_trail_reconstruction(task_id)` or read board memory trail events:
- Trail should show: stage transitions (conversation → analysis → ... → work)
- Trail should show: artifacts at each stage (analysis_document, investigation_document, plan)
- Red flag: only `plan_accepted` and `task_completed` events — no analysis, no investigation

**Acceptable exceptions:**
- Subtasks and fix tasks may start at work stage (PM triaged them correctly)
- Spikes and concerns may only go through analysis/investigation (no work stage)

### 2. Tool Usage at Correct Stages

The methodology blocks certain tools at certain stages (methodology.yaml). The MCP layer enforces this at call time. But defense-in-depth means you should verify the trail doesn't show violations:

| Stage | Blocked | Allowed |
|-------|---------|---------|
| conversation | fleet_commit, fleet_task_complete, fleet_task_accept | fleet_chat, fleet_artifact_create (drafts) |
| analysis | fleet_task_complete | fleet_commit (analysis docs OK), fleet_artifact_create/update |
| investigation | fleet_task_complete | fleet_commit (research docs OK), fleet_artifact_create/update |
| reasoning | fleet_task_complete | fleet_task_accept, fleet_task_create, fleet_commit (plans OK) |
| work | (nothing blocked) | ALL tools available |

**Red flag:** Trail shows `fleet_commit` events during conversation stage. The MCP layer should have blocked this, but if it somehow got through, flag it.

### 3. Contribution Consumption

For stories and epics, the synergy matrix requires contributions. Check that:
- Required contributions were received (typed comments on the task)
- The implementation actually FOLLOWS the contributions (design_input pattern used, TC-XXX criteria satisfied)
- Security requirements were followed, not ignored

**How to check:** Read the task's typed comments. Look for `**Contribution (design_input)**`, `**Contribution (qa_test_definition)**`, etc. Then compare the implementation/PR against what was contributed.

**Red flag:** design_input says "adapter pattern" but implementation uses direct API calls. QA defined TC-003 testing timeout handling but no timeout test exists.

### 4. Phase Standards

Each delivery phase (poc/mvp/staging/production) has quality bars from `config/phases.yaml`. The phase_advance tool checks these, but you should verify during review:

| Phase | Tests | Docs | Security |
|-------|-------|------|----------|
| poc | Happy path only | README | Basic scan |
| mvp | Main flows + edges | Setup + usage | Auth + validation |
| staging | Comprehensive + integration | Full docs | Dep audit |
| production | Complete + performance | Everything + runbook | Certified |

**Red flag:** Production-phase task with only happy-path tests. MVP task with zero documentation.

### 5. Trail Completeness

A complete trail tells the story of the task. Minimum trail events for a standard task:

1. `plan_accepted` — agent committed to an approach
2. Stage transition events (if applicable)
3. `fleet_commit` events — the work itself
4. `task_completed` — agent submitted for review
5. Contribution events (if story/epic)

**Red flag:** Only `task_completed` in the trail. No plan, no commits, no stage transitions — the agent may have done everything in one untracked burst.

## The Review Decision

After checking all 5 dimensions:

- **ALL PASS** → `fleet_approve(decision="approved", comment="[specifics of what passed]")`
- **MINOR GAPS** → Approve with feedback: `comment="Approved. Note: trail could be richer — consider recording stage transitions."`
- **SIGNIFICANT GAPS** → `fleet_approve(decision="rejected", comment="[specific gap]: design_input says X but implementation does Y. Reground in verbatim and fix.")`

Never rubber-stamp. Never approve without reading the work. The PO trusts your review — make it real.
