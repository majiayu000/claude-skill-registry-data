---
name: ship
description: Shipping surge mode — test, scan, PR, merge, tag. Zero manual steps between green tests and merged code.
version: 1.0.0
execution-mode: side_effecting
argument-hint: "<branch, PR number, or feature to ship>"
category: dev-tools
status: candidate
---
# Ship Mode Activation

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=ship] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

You are operating in **SHIP MODE** — maximum shipping velocity with zero skipped gates.

## Active Configuration
- **Tempo**: SURGE (the code is written; ship it)
- **Autonomy**: Maximum — run the full pipeline, report results
- **Pipeline**: Test → Scan → PR → CI Watch → Tag

## Task
$ARGUMENTS

## Shipping Pipeline

1. **Test** — `[test-run]` full suite; must be green. If red, stop and report.
2. **Security** — `[security-scan]` + `[secret-scan]`; zero HIGH/CRITICAL before proceeding
3. **PR** — `[pr-summary]` + create PR; include test count, security scan status, blast radius
4. **CI Watch** — `[ci-wait]`; report final status
5. **Tag** — if this is a release: `[tag-release]` → `[release-notes]` → `[release-announce]`

## Quick-Access Skills
- **Verify**: `[test-run]`, `[coverage]`, `[regression-check]`, `[ship-check]`
- **Security**: `[security-scan]`, `[secret-scan]`, `[dep-check]`, `[supply-chain-audit]`
- **Git**: `[commit]`, `[pr-summary]`, `[ci-wait]`, `[ci-monitor]`
- **Release**: `[tag-release]`, `[release-notes]`, `[release-announce]`, `[changelog]`
- **Rollback**: `[rollback]`, `[git-bisect]`, `[cherry-pick-safe]`

## Rules
- **CI green before PR** — never open a PR on a red local run
- **Security scan mandatory** — not optional, not skippable
- **No `--no-verify`** — ever
- **No force-push** to main or any protected branch
- **Conventional Commits** format on every commit message
- **Squash-merge to main** — per repo policy
- Stdlib-only in services/ and integrations/ — verify before PR
- No Ollama on MBP

## Output Contract
End every session with:
1. Test count (before/after)
2. Security scan result (PASS/FAIL + finding count)
3. PR URL or merge commit
4. CI final status
5. Bus STATUS posted

Begin shipping now.

## Skill Chains

### Mandatory (MUST pass before PR creation)

- **`[test-run]`** MUST be green — no PR on red local run
- **`[security-scan]`** MUST be clean — zero HIGH/CRITICAL findings
- **`[secret-scan]`** MUST be clean — no leaked secrets in diff

### Mandatory (MUST pass before merge)

- **`[ship-check]`** MUST pass all 10 checks including the bus review gate
  (step 10: `check_bus_review_gate.py`). Require an accepting, evidence-valid
  non-author REVIEW bound to the current full head SHA; verify canonical
  authorship, reviewer scope/REVIEW permission, and bus provenance. Supply
  the assigned reviewer with `--reviewer`; roster trust alone is insufficient.
  Assignment restricts qualifying approvals, while all eligible current-head
  reviewers' rejections, invalid evidence, and P0/P1 remain blocking.
  Rejecting/invalid receipts and unresolved P0/P1 block, and head changes
  require fresh review. If review is missing, search across bus lanes before
  dispatching with a nonempty actual patch and exact refs. Same-author
  `review_lane_authorized=true` does not satisfy the automated gate; operator
  waivers are separate recorded decisions. CI semantics, threads, changes
  requests, mergeability, and branch policy must also pass. See
  `cross-check-protocol.md` § "Bus as Canonical Review Record" for exit codes
  and optional structured `--receipt` validation.

### Advisory

- **Before ship**: `[ship-check]` (full pre-ship checklist)
- **After merge**: `[tag-release]` (if release), `[release-notes]`, `[release-announce]`
- **On failure**: `[rollback]`, `[git-bisect]`, `[cherry-pick-safe]`

## Authority

- **T1 (TRUSTED)**: May ship without pre-approval
- **T2 (Active/High)**: May ship with all mandatory chains passed
- **T3 (Medium)**: MUST get operator approval AND all mandatory chains passed
- **T4 (Probationary)**: BLOCKED — cannot invoke this skill
- **Operator**: Override any restriction
