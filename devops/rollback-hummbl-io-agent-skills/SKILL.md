---
name: rollback
description: CD recovery skill for reverting a bad release or deployment with health verification, rollback evidence, and bus notification. Use when a deployment, release, main-branch merge, or production health check requires reversal or rollback planning.
version: 0.1.0
execution-mode: side_effecting
argument-hint: "<commit-or-pr> [--dry-run]"
category: backend-infra
status: candidate
---
# [rollback] | Structured Rollback

## Purpose

Answer: "How do we safely reverse a bad release and verify recovery?"

## When to Use
- Production incident requiring immediate revert
- Failed deployment or broken CI on main
- After `[incident]` identifies a bad commit
- Health probes reporting failures after a merge
- Release promotion must be reversed before broader rollout

## Workflow

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=rollback] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

1. **Identify scope** -- parse `$ARGUMENTS` for commit SHA, PR number, or "last N commits"
2. **Find last known good** -- check CI status, health probes, and test results
   ```bash
   git log --oneline -10
   python -m hummbl_governance.services.health --check 2>/dev/null || echo "HEALTH: DEGRADED"
   ```
3. **Dry run** (if `--dry-run` or by default on >3 commits):
   - Show files affected: `git diff --stat <good>..<bad>`
   - List services touched
   - Flag contract schema changes (requires SemVer bump)
4. **Execute revert**:
   ```bash
   git revert --no-edit <bad-commit>..HEAD  # or single commit
   ```
5. **Verify health**:
   ```bash
   python -m pytest $PROJECT_ROOT/tests/test_acceptance.py -v
   python -m hummbl_governance.services.health --check
   ```
6. **Notify bus**:
   Post STATUS to the bus with the rollback result.
   ```
   Type: STATUS
   To: all
   Message: ROLLBACK: reverted <sha> -- health restored
   ```
   (The skill invocation runtime injects the caller's canonical identity as `from_id`.)
7. **If contract baseline affected**, warn: contract rollbacks may require downstream coordination.

## Output Format

```
[rollback] | <commit-or-range>
------------------------------
Target:       <commit SHA or range>
Reason:       <from incident or argument>
Files:        <N files changed>
Services:     <list of affected services>
Contracts:    <SAFE | AFFECTED (requires coordination)>
Health before: <PASS | FAIL (N probes)>
Revert:       <commit SHA of revert>
Health after:  <PASS | FAIL (N probes)>
Tests:        <PASS | N failures>
Bus:          <posted | skipped>
------------------------------
Status: ROLLED BACK | DRY RUN ONLY | FAILED (reason)
```

## Skill Chains

### Mandatory (MUST pass before rollback execution)

- **`[deploy-health]`** MUST confirm degradation — no rollback without evidence of failure
  Exception: operator explicit override for emergency rollback

### Advisory

- `[incident]` -> `[rollback]` (incident identifies, rollback executes)
- `[rollback]` -> `[health]` (verify recovery)
- `[rollback]` -> `[sitrep]` (communicate status to team)
- `[rollback]` -> `[retrospective]` (after stabilization)
- `[release-manager]` -> `[rollback]` (release plan includes recovery path)

## Authority

- **T1 (TRUSTED)**: May rollback with `[deploy-health]` confirming degradation
- **T2 (Active/High)**: MUST get operator approval AND `[deploy-health]` confirming degradation
- **T3 (Medium)**: MUST get operator approval AND `[deploy-health]` confirming degradation
- **T4 (Probationary)**: BLOCKED — cannot invoke this skill
- **Operator**: Override any restriction — emergency rollback allowed without pre-chain
