---
name: hotfix
description: "Use when an S1 or S2 production defect requires an emergency fix with an audit trail and rollback plan."
---

<!-- codex-studio-delegation: governed -->
Resolve every role through `../../../.codex/docs/plugin-agent-delegation.md`;
do not require a repository-local `.codex/agents/` or `.codex/agent-packs/` tree.
Before default delegation, run `python3 ../../../tools/codex_studio/agent_delegation.py resolve --project-root <project-root> --role <role>` and use only its returned role contract.

## Codex Interaction Contract

- Ask one decision question per turn and wait for the answer before asking another.
- Use `request_user_input` for structured choices when it is available; otherwise ask the same concise question directly.
- Use Codex custom agents by role and profile when delegation is useful.
- Treat any approved write as one complete proposed changeset. Before writing, present every target path and material edit together; do not add unlisted files or behavior.
- A new path, expanded scope, or material change requires a revised complete proposed changeset and fresh approval.

## Release Safety Boundary

Creating or switching branches, committing, pushing, deploying, releasing, or publishing requires explicit user authorization at that step. Ask again immediately before each operation; approval for one step never authorizes another. Each destructive operation requires its own explicit authorization and rollback explanation.

## Delegation Contract

- Delegate only work that is independent and bounded.
- Name the custom-agent role and the exact artifact or evidence it must return.
- Delegated agents must not spawn additional agents (`agents.max_depth = 1`).
- The parent synthesizes every result and presents all exact paths and changes to the user.
- No subagent commits, publishes, or expands scope.
- Before an approved changeset, delegated work is read-only or draft-only.

> **Explicit invocation only**: This skill should only run when the user explicitly requests it with `$codex-game-studios:hotfix`. Do not auto-invoke based on context matching.

## Phase 1: Assess Severity

Read the bug description or ID. Assess severity using these criteria:

- **S1 (Critical)**: Game unplayable, data loss, security vulnerability
- **S2 (Major)**: Significant feature broken, workaround exists
- **S3 or lower**: Minor issue — normal bug fix workflow applies

Confirm with `request_user_input`:
- Prompt: "I've assessed this as **[assessed severity]** — [brief rationale]. Confirm severity to proceed:"
- Options:
  - `[A] S1 (Critical) — game unplayable, data loss, or security issue`
  - `[B] S2 (Major) — significant feature broken, workaround exists`
  - `[C] S3 or lower — redirect to normal bug fix workflow`

If [C]: stop. Verdict: **REDIRECTED** — use the normal bug fix workflow for S3 and below.

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
[Clear description of what is broken and the player impact]

### Root Cause
[To be filled during investigation]

### Fix
[To be filled during implementation]

### Testing
[What was tested and how]

### Approvals
- [ ] Fix reviewed by lead-programmer
- [ ] Regression test passed (qa-tester)
- [ ] Release approved (producer)

### Rollback Plan
[How to revert if the fix causes new issues]
```

Keep this record as an in-memory draft intended for `production/hotfixes/hotfix-[date]-[short-name].md` until the implementation preflight below includes that exact path in one complete proposed changeset.

---

## Phase 3: Create Hotfix Branch

Check whether this is a git repository:

Run `git rev-parse --is-inside-work-tree` and inspect the result.

If this command fails or returns empty: note "Not a git repository — create the branch manually." and skip branch creation.

If the check passes, use `request_user_input` before creating the branch:
- Prompt: "Ready to create hotfix branch 'hotfix/[short-name]' from [base-ref]?"
- Options:
  - `[A] Yes — create branch`
  - `[B] Use a different base ref — I'll specify it`
  - `[C] Skip — I'll create the branch myself`

Only run `git checkout -b hotfix/[short-name] [base-ref]` if user selects [A]. If [B]: ask the user for the base ref, then run the command with that ref. If [C]: skip branch creation and proceed to Phase 4.

---

## Phase 4: Investigate and Implement

Investigate read-only first and identify the minimum change that resolves the issue. Do NOT refactor, clean up, or add features alongside the hotfix.

Before editing, present one implementation preflight listing the hotfix record, every source/config file, every test/evidence file, the exact acceptance criteria, and rollback risk. Obtain approval for that complete proposed changeset. Delegated implementation stays inside it; any new path or material change pauses for revised approval.

Validate the fix by running targeted tests for the affected system. Check for regressions in adjacent systems.

Update the hotfix record with root cause, fix details, and test results.

---

## Phase 5: Collect Approvals

Use the Codex custom-agent delegation to request sign-off in parallel:

- `custom-agent role: lead-programmer` — Review the fix for correctness and side effects
- `custom-agent role: qa-tester` — Run targeted regression tests on the affected system
- `custom-agent role: producer` — Approve deployment timing and communication plan

All three must return APPROVE before proceeding. If any returns CONCERNS or REJECT, do not deploy — surface the issue and resolve it first.

---

## Phase 5b: QA Re-Entry Gate

After approvals, determine the QA scope required before deploying the hotfix. Delegate to `qa-lead` through Codex custom-agent delegation with:
- The hotfix description and affected system
- The regression test results from Phase 5
- A list of all systems that touch the changed files (use Search to find callers)

Ask qa-lead: **Is a full smoke check sufficient, or does this fix require a targeted team-qa pass?**

Apply the verdict:
- **Smoke check sufficient** — run `$codex-game-studios:smoke-check` against the hotfix build. If PASS, proceed to Phase 6.
- **Targeted QA pass required** — run `$codex-game-studios:team-qa [affected-system]` scoped to the changed system only. If QA returns APPROVED or APPROVED WITH CONDITIONS, proceed to Phase 6.
- **Full QA required** — S1 fixes that touch core systems may require a full `$codex-game-studios:team-qa sprint`. This delays deployment but prevents a bad patch.

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

Merge to: release branch AND development branch
Next: $codex-game-studios:bug-report verify [BUG-ID] after deploy to confirm resolution
```

### Rules
- Hotfixes must be the MINIMUM change to fix the issue — no cleanup, no refactoring
- Every hotfix must have a rollback plan documented before deployment
- Hotfix branches merge to BOTH the release branch AND the development branch
- All hotfixes require a post-incident review within 48 hours
- If the fix is complex enough to need more than 4 hours, escalate to `technical-director`

---

## Phase 7: Post-Deploy Verification

After deploying, run `$codex-game-studios:bug-report verify [BUG-ID]` to confirm the fix resolved the issue in the deployed build.

If VERIFIED FIXED: run `$codex-game-studios:bug-report close [BUG-ID]` to formally close it.
If STILL PRESENT: the hotfix failed — immediately re-open, assess rollback, and escalate.

Schedule a post-incident review within 48 hours using `$codex-game-studios:retrospective hotfix`.

Use `request_user_input`:
- Prompt: "Hotfix complete. What's the next step?"
- Options:
  - `[A] Run $codex-game-studios:smoke-check to verify the fix`
  - `[B] Run $codex-game-studios:patch-notes to document this hotfix`
  - `[C] Stop here`
