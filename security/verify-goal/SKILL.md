---
name: verify-goal
description: >
  Goal-native live verification. Drives a TRD's implementation to "all assertions pass"
  under /goal — one assertion of progress per turn against a durable verify.json contract.
  Use when running verification autonomously via `claude -p "/goal …"` or interactive
  `/goal`, or when you want a single-session, self-contained verify loop. Triggers: "verify
  until it works", "goal verify", "autonomous verification", "keep verifying until all pass".
when_to_use: >
  Reach for this for autonomous single-session live verification of a TRD under /goal — one
  assertion of progress per turn against a durable verify.json contract, looping until all
  assertions pass. For functional ship-readiness against original requirements use
  ship-workplan; for smoke tests use the smoke-test-* skills; for post-implementation
  traceability against the TRD/PRD use /audit-build.
argument-hint: "[trd-path] [--promise \"<text>\"]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Skill, Agent
---

# verify-goal — structured live verification for `/goal`

This skill is a single-session, **`/goal`-drivable** live-verification loop. `/goal` supplies
the *loop* (keep working turn-after-turn until a condition is met); this skill supplies the
*structure* and a *machine-checkable completion contract*, so the goal condition is concrete
and file-backed rather than ad-hoc prose.

> **Why this exists:** a command/skill body cannot itself activate `/goal` (slash commands
> fire only from direct user input). So instead of a command "turning on" autonomy, the
> user/orchestrator launches `/goal` with a structured condition that points at this skill.

This skill is fully self-contained — it does not depend on any other command for its
schema or templates. (An earlier version deferred to a now-deleted `/verify-trd-team`
command; that command's adversarial-verification job moved into the `implement-trd` phase
loop and `/audit-build`, per constitution.md's nesting-stance changelog. The State Schema,
Promise Decomposition method, safety rules, and PROBE/FIX templates below are the content
that command used to define, inlined here because this skill is now their only consumer.)

## How to launch

**Autonomous (headless / remote):**

```bash
claude -p "/goal Every assertion in .trd-state/<trd-name>/verify.json has verdict \"pass\" (or acceptable \"blocked\"); zero \"pending\" or \"fail\". Use the verify-goal skill against docs/TRD/<trd-name>.md."
```

**Interactive:** type the same `/goal …` line; this skill auto-activates from the mention.

## The completion contract (what `/goal` evaluates each turn)

`.trd-state/<trd-name>/verify.json` is the single source of truth (schema below). The goal
is met IFF:

- the file exists and contains at least one assertion, **and**
- every assertion's `verdict` is `pass` (or `blocked` with an acceptable justification per
  "Assertion Rollup", below), **and**
- zero assertions are `pending` or `fail`.

Because the predicate is a file, `/goal`'s per-turn check is concrete and deterministic —
not a fuzzy judgment of "is it done yet?".

## Completion Promise

The completion promise defines what "verified" means — the exit criteria for the pass.

### Default Promise

If no `--promise` is provided, use:

> Live verification — through API testing, UI testing, and (to the extent practical)
> non-destructive read-only third-party service testing — confirms the implementation
> is functional, aligned with the PRD, and delivers the intended user outcomes.

### Custom Promise

If `--promise` is provided, use it verbatim. The promise is stored in verify.json and
persists across resumed runs.

## Promise Decomposition

Before verification begins, decompose the promise into **verifiable assertions** — concrete,
testable statements that collectively satisfy the promise. Each assertion maps to one or
more TRD tasks.

```
Promise: "Users can sign up, log in, and see their dashboard with live data"

Assertions:
  V-001: POST /api/auth/register returns 201 with valid payload and creates user record
  V-002: POST /api/auth/login returns 200 with JWT for valid credentials
  V-003: POST /api/auth/login returns 401 for invalid credentials
  V-004: GET /dashboard renders without error when authenticated
  V-005: Dashboard displays data fetched from /api/dashboard endpoint
  V-006: Unauthenticated access to /dashboard redirects to login
```

Assertions should be:

- **Observable** — can be confirmed by running something and checking output
- **Specific** — exact endpoint, exact UI element, exact behavior
- **Independent** — each can be verified without the others (where possible)
- **Traceable** — maps back to TRD task IDs and PRD acceptance criteria

Each assertion gets a verdict: `pass`, `fail`, or `blocked`.

## Per-turn algorithm

Each turn, make progress toward the contract and persist it (atomic write) to verify.json:

1. **Bootstrap (first turn only):** load the TRD + linked PRD (from TRD Section 10 or
   `.trd-state/current.json`'s `prd` field). Decompose the completion promise into
   assertions per "Promise Decomposition", above. Write verify.json with every assertion
   `pending`.
2. **Select** the next unsatisfied assertion (priority: `fail` before `pending`). If none
   remain unsatisfied, the contract is met — print the satisfied report and stop.
3. **PROBE** it live using the V.1 template below. Record `verdict` + `evidence`.
4. **FIX (if FAIL)** using the V.2 template below — minimal change; never weaken assertions
   to pass. Delegate deep debugging to the `app-debugger` subagent via the **Agent** tool.
   Cap at 3 fix attempts per assertion; then mark `fail` and move on (the goal stays unmet,
   surfacing the blocker for a human).
5. **RE-PROBE**, and re-check previously-`pass` assertions touching the same files
   (regression guard).
6. For each `pass`, ensure a durable test exists (write one if missing) so CI catches
   regressions.
7. **Persist verify.json.** The turn ends; `/goal` re-evaluates the contract and re-invokes
   if unmet.

Durable across `/compact` and session end — verify.json is the state; resuming the `/goal`
run picks up exactly where it left off. No run-counter / max-runs cap; `/goal` stops when
the contract is met or the user interrupts.

## Assertion Rollup

```
All PASS (including BLOCKED with acceptable justification) -> PROMISE SATISFIED
Any FAIL -> PROMISE NOT SATISFIED
```

**BLOCKED handling:** an assertion is acceptably blocked if:
- It requires destructive third-party operations (by design)
- The service/dependency is unavailable and cannot be started locally
- It requires infrastructure not present in development environment

Unacceptable blocks (count as FAIL):
- Code errors preventing the test from running
- Missing implementation
- Configuration issues that should be fixable

## Safety — third-party service rules

Read-only / sandbox third-party operations only:

- **NEVER** send real emails, SMS, or push notifications
- **NEVER** charge real payment methods or modify billing
- **NEVER** write to production external databases
- **NEVER** delete or modify external resources
- READ-ONLY operations and mock/sandbox endpoints are acceptable
- If a sandbox/test mode is available, use it
- Document any third-party tests as "sandbox-verified" or "connection-verified"

If verifying an assertion would require a destructive external action, mark it `blocked`
with the reason (acceptable block).

## State Schema

Stored at `.trd-state/<trd-name>/verify.json`:

```json
{
  "version": "1.0.0",
  "mode": "verify",
  "trd_file": "docs/TRD/<feature>.md",
  "prd_file": "docs/PRD/<feature>.md",
  "trd_hash": "<sha256>",
  "branch": "<branch-name>",
  "completion_promise": "<promise text>",
  "phase_cursor": 1,
  "assertions": {
    "V-001": {
      "text": "Assertion description",
      "task_ids": ["AUTH-B001", "AUTH-B002"],
      "verdict": "pass|fail|blocked|pending",
      "evidence": "Description of evidence or null",
      "fix_attempts": 0,
      "max_fix_attempts": 3,
      "tests_created": ["path/to/test.spec.ts"],
      "history": [
        {
          "verdict": "fail",
          "evidence": "...",
          "fix_applied": "description or null"
        }
      ]
    }
  },
  "recovery": {
    "last_healthy_checkpoint": null,
    "last_checkpoint_timestamp": null,
    "interrupted": false,
    "interrupt_reason": null
  },
  "metrics": {
    "total_assertions": 0,
    "total_fixes": 0,
    "total_tests_written": 0,
    "total_regressions": 0
  }
}
```

## Appendix V.1 — Template: PROBE

```xml
<probe_request>
  <assertion id="{assertion_id}" task_ids="{TRD task IDs}">
    {assertion text}
  </assertion>
  <prior_verdict>{PASS|FAIL|BLOCKED|NEW}</prior_verdict>
  <prior_evidence>{evidence from last turn, if any}</prior_evidence>
</probe_request>

<skills>
  <matched>{test framework skills: jest, pytest, writing-playwright-tests, etc.}</matched>
  <instruction>
    Invoke matched skills for test framework patterns when writing durable tests.
  </instruction>
</skills>

<instructions>
Verify this assertion through live testing.

1. Determine the verification method:
   - API endpoint -> make HTTP requests, check responses
   - UI behavior -> use Playwright to navigate and interact
   - Data flow -> trace from input to storage to output
   - Service integration -> read-only probe of external service

2. Execute the probe:
   - Start services if needed (check first, don't duplicate)
   - Perform the verification action
   - Capture evidence (response bodies, screenshots, logs)

3. Record verdict:
   - PASS: assertion holds, evidence confirms it
   - FAIL: assertion does not hold, evidence shows why
   - BLOCKED: cannot verify due to external constraint (explain)

4. If PASS: ensure a durable test exists that will catch regression.
   If no test covers this assertion, write one now.

Deliverables:
- verdict: PASS | FAIL | BLOCKED
- evidence: concrete output (response body, screenshot path, log excerpt)
- test_file: path to durable test (existing or newly created)
- services_started: list of services you started (for cleanup)
</instructions>
```

## Appendix V.2 — Template: FIX

```xml
<fix_request>
  <assertion id="{assertion_id}">
    {assertion text}
  </assertion>
  <failure_evidence>{evidence from PROBE}</failure_evidence>
  <fix_attempt>{N} of 3</fix_attempt>
  <prior_fixes>{descriptions of prior fix attempts, if any}</prior_fixes>
</fix_request>

<skills>
  <matched>{implementation skills matching the code area}</matched>
  <instruction>
    Invoke matched skills for framework-specific fix patterns.
  </instruction>
</skills>

<instructions>
The live verification probe failed. Fix the underlying issue.

1. Diagnose: Read the failing code, check logs, trace the execution path.
   The evidence from the probe should point you to the area.

2. Fix: Make the minimal change to make the assertion pass.
   - Do NOT refactor unrelated code
   - Do NOT change test expectations to match broken behavior
   - If the fix requires changing multiple files, that's fine — but
     each change must be justified by the assertion failure

3. Test: Write or update a test that covers this specific fix.

4. Verify: Confirm the fix addresses the failure. Also check that
   no other assertions in this session regressed.

If this is attempt 2+, review prior fix attempts to avoid repeating
the same approach. If the root cause is unclear, delegate to
@app-debugger (subagent_type: "app-debugger") for deep analysis.

Deliverables:
- files_changed: list of modified files
- root_cause: one-line description of what was wrong
- fix_description: what you changed and why
- regression_check: list of other assertions re-verified
- SKILLS_USED: exact skill names invoked
</instructions>
```
