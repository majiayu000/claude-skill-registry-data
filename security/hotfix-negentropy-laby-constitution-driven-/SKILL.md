---
name: hotfix
description: "Emergency fix workflow that bypasses normal sprint processes with a full audit trail. Creates hotfix branch, tracks approvals, and ensures the fix is backported correctly."
argument-hint: "[bug-id or description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task
---

## User Guide

- When to use: Emergency fix workflow that bypasses normal sprint processes with a full audit trail. Creates hotfix branch, tracks approvals, and ensures the fix is backported correctly.
- Inputs: Command arguments: `/hotfix [bug-id or description]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: `memory_bank/t0_core/release_state.md`, `memory_bank/t3_archive/release_evidence/hotfix-[short-name]-[YYYY-MM-DD].md`.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before running the hotfix workflow:
- `design/cdd/game-concept.md` -> **[Game]** handle shipped-build hotfixes: crash, save corruption, progression blocker, multiplayer exploit, platform certification issue, or severe player-facing regression.
- `design/cdd/product-concept.md` -> **[Product]** handle product hotfixes: outage, API regression, CLI packaging break, migration failure, auth/security issue, data corruption, config rollback, or deployment incident.
- If unclear, ask whether this is a game build hotfix or a product/service hotfix.

Do not remove game hotfix guidance. Product incident/hotfix guidance is added beside it.

## Dual-Domain Parity Contract

| Area | Game branch | Product branch |
|------|-------------|----------------|
| Context reads | Game Concept, bug report, release tag/build, affected CDD/ADR, tests, crash/playtest/session evidence | Product Concept, incident/bug report, release tag/deploy, affected CDD/ADR, logs/alerts, API/CLI/workflow/migration/config/deployment/package evidence |
| Steps | Assess severity, create hotfix record/branch, implement minimal fix, run targeted tests/regression, collect approvals, deploy/backport | Assess severity, create incident/hotfix record/branch, implement minimal fix, validate contract/workflow/migration/config/deploy/package recovery, collect approvals, deploy/backport |
| Outputs | `production/hotfixes/hotfix-[date]-[short-name].md`, branch, test evidence, rollback plan, backport notes | Same hotfix record plus product incident context, monitoring signal, compatibility risk, deployment/rollback evidence |
| Next steps | Verify via `/bug-report verify`, monitor player reports, backport to main, add regression coverage | Verify monitoring/customer recovery, run `/test-evidence-review`, update release notes/docs, backport, add regression/contract coverage |

> **Explicit invocation only**: This skill should only run when the user explicitly requests it with `/hotfix`. Do not auto-invoke based on context matching.

## Phase 1: Assess Severity

Read the bug description or ID. Determine severity:

- **S1 (Critical)**: Game unplayable, data loss, security vulnerability — hotfix immediately
- **S2 (Major)**: Significant feature broken, workaround exists — hotfix within 24 hours
- **Product S1 (Critical)**: production outage, security/auth bypass, data loss,
  migration failure, API/CLI regression blocking core workflow, broken package
  release, or config/deployment issue with no safe workaround — hotfix immediately
- **Product S2 (Major)**: degraded workflow, partial outage, broken docs/package
  artifact, compatibility regression, or operational issue with a documented
  workaround — hotfix within 24 hours
- If severity is S3 or lower, recommend using the normal bug fix workflow instead and stop.

---

## Phase 2: Create Hotfix Record

Draft the hotfix record:

```markdown
## Hotfix: [Short Description]
Date: [Date]
Severity: [S1/S2]
Reporter: [Who found it]
Status: IN PROGRESS

### Problem
[Clear description of what is broken and the player/user/customer/API/CLI impact]

### Root Cause
[To be filled during investigation]

### Fix
[To be filled during implementation]

### Testing
[What was tested and how. Product hotfixes must include affected contract,
workflow, migration/config, deployment, docs/help, or monitoring evidence.]

### Approvals
- [ ] Fix reviewed by lead-programmer
- [ ] Regression test passed (qa-tester)
- [ ] Release approved (producer)

### Rollback Plan
[How to revert if the fix causes new issues]

### Product Incident Context (if Product)
- Affected surface: [API endpoint / CLI command / web flow / package / migration / config / deployment]
- Affected users or integrations: [who is blocked or degraded]
- Compatibility risk: [schema, exit code, package version, migration, config]
- Monitoring signal: [dashboard/log/alert proving recovery]
```

Ask: "May I write this to `production/hotfixes/hotfix-[date]-[short-name].md`?"

If yes, write the file, creating the directory if needed.

---

## Phase 3: Create Hotfix Branch

If git is initialized, create the hotfix branch:

```
git checkout -b hotfix/[short-name] [release-tag-or-main]
```

---

## Phase 4: Investigate and Implement

Focus on the minimal change that resolves the issue. Do NOT refactor, clean up, or add features alongside the hotfix.

Validate the fix by running targeted tests for the affected system. Check for regressions in adjacent systems.
For Product hotfixes, targeted validation must include the affected public
contract or workflow: API contract/integration test, CLI exit-code/stdout test,
E2E flow, migration apply/rollback or dry-run, config smoke, package install,
or deployment/monitoring check as relevant.

Update the hotfix record with root cause, fix details, and test results.

---

## Phase 5: Collect Approvals

Use the Task tool to request sign-off in parallel:

- `subagent_type: lead-programmer` — Review the fix for correctness and side effects
- `subagent_type: qa-tester` — Run targeted regression tests on the affected system
- `subagent_type: producer` — Approve deployment timing and communication plan
- Product hotfixes may also require `security-engineer` for auth/secrets/data
  issues, `devops-engineer` for deployment/migration/config rollback, or the
  relevant language specialist for API/CLI/package compatibility.

All three must return APPROVE before proceeding. If any returns CONCERNS or REJECT, do not deploy — surface the issue and resolve it first.

---

## Phase 5b: QA Re-Entry Gate

After approvals, determine the QA scope required before deploying the hotfix. Spawn `qa-lead` via Task with:
- The hotfix description and affected system
- The regression test results from Phase 5
- A list of all systems that touch the changed files (use Grep to find callers)

Ask qa-lead: **Is a full smoke check sufficient, or does this fix require a targeted team-qa pass?**

Apply the verdict:
- **Smoke check sufficient** — run `/smoke-check` against the hotfix build. If PASS, proceed to Phase 6.
- **Targeted QA pass required** — run `/team-qa [affected-system]` scoped to the changed system only. If QA returns APPROVED or APPROVED WITH CONDITIONS, proceed to Phase 6.
- **Full QA required** — S1 fixes that touch core systems may require a full `/team-qa sprint`. This delays deployment but prevents a bad patch.
- **Product contract/release validation required** — run the affected contract,
  CLI, E2E, migration, package, deployment, or monitoring smoke checks before
  proceeding. Product hotfixes that affect public compatibility cannot deploy
  on unit tests alone.

Do not skip this gate. A hotfix that breaks something else is worse than the original bug.

---

## Phase 6: Update Bug Status and Deploy

Update the original bug file if one exists:

```markdown
## Fix Record
**Fixed in**: hotfix/[branch-name] — [commit hash or description]
**Fixed date**: [date]
**Status**: Fixed — Pending Verification
```

Set `**Status**: Fixed — Pending Verification` in the bug file header.

Output a deployment summary:

```
## Hotfix Ready to Deploy: [short-name]

**Severity**: [S1/S2]
**Root cause**: [one line]
**Fix**: [one line]
**QA gate**: [Smoke check PASS / Team-QA APPROVED]
**Approvals**: lead-programmer ✓ / qa-tester ✓ / producer ✓
**Rollback plan**: [from Phase 2 record]
**Product surface**: [API / CLI / web / package / migration / config / deployment, if applicable]
**Product validation**: [contract / CLI / E2E / migration / package / monitoring evidence, if applicable]
**Compatibility note**: [schema, exit code, package, migration, config, or docs impact, if applicable]

Merge to: release branch AND development branch
Next: /bug-report verify [BUG-ID] after deploy to confirm resolution
```

When `memory_bank/` exists, present the actual hotfix evidence draft and proposed
`memory_bank/t0_core/release_state.md` update as distinct path/effects. Reuse existing
scoped authority; ask only for uncovered effects, naming the actual
`memory_bank/t3_archive/release_evidence/hotfix-[short-name]-[YYYY-MM-DD].md`
report path and any state update in the concrete changeset.

Write each effect only when it is covered by that authority. Approval for the report
alone does not authorize the state update; preserve a pending state projection while
saving an authorized report. If the evidence filename exists, append `-[NN]` and
include the resolved new path in scope; do not overwrite history.

Hotfix evidence must include severity, branch/commit, QA gate, rollback plan,
deployment status, monitoring result, and post-incident review link. Do not
create `memory_bank/` from `/hotfix`; if it does not exist, keep the normal
hotfix record and tell the user to run `/constitute` to establish the
memory_bank governance control plane.

### Rules
- Hotfixes must be the MINIMUM change to fix the issue — no cleanup, no refactoring
- Every hotfix must have a rollback plan documented before deployment
- Hotfix branches merge to BOTH the release branch AND the development branch
- All hotfixes require a post-incident review within 48 hours
- If the fix is complex enough to need more than 4 hours, escalate to `technical-director`
- Product hotfixes that change public API schemas, CLI output/exit codes,
  package artifacts, migrations, config defaults, auth behavior, or deployment
  topology require an explicit compatibility note and release communication.
- Product hotfix rollback must identify whether rollback means code revert,
  feature flag disablement, config rollback, migration rollback/forward-fix, or
  package version yank/deprecation.

---

## Phase 7: Post-Deploy Verification

After deploying, run `/bug-report verify [BUG-ID]` to confirm the fix resolved the issue in the deployed build.
For Product hotfixes, verification must include the live or staged product
surface that failed: API endpoint, CLI install/command, web workflow, data
pipeline, migration state, package artifact, config, alert, log, or dashboard.

If VERIFIED FIXED: run `/bug-report close [BUG-ID]` to formally close it.
If STILL PRESENT: the hotfix failed — immediately re-open, assess rollback, and escalate.

Schedule a post-incident review within 48 hours using `/retrospective hotfix`.
