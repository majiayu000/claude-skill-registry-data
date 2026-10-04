---
name: verify-before-done
category: quality
description: Evidence rules for completion claims. Use before ticking an acceptance criterion, ending an implementation run, or writing anything that says something works, passes or is fixed.
source: obra/superpowers (MIT), adapted
---
# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in THIS run, you cannot claim it passes. A previous run, "should pass", or "looks correct" is not evidence.

## The Gate Function

Before claiming any status or moving any task forward:

1. IDENTIFY — what command proves this claim?
2. RUN — execute the full command, fresh and complete.
3. READ — the full output: exit code, failure count, warnings.
4. VERIFY — does the output actually confirm the claim? If no: state the real status with evidence.
5. ONLY THEN — make the claim, with the evidence.

Skipping any step is lying, not verifying.

## What Each Claim Requires

| Claim | Requires | Not sufficient |
|-------|----------|----------------|
| Checks pass | The component's `list_component_checks` commands, run in this run, exit 0 — the hand-off gate runs exactly these | A different command you picked yourself |
| Build succeeds | Build command: exit 0 | Linter passing, logs look fine |
| Bug fixed | Re-run the original symptom: passes | Code changed, assumed fixed |
| Regression test guards the fix | Revert the fix, run the test (MUST FAIL), restore, run again (passes) | The test passing once, with the fix already in place |
| Endpoint works (backend) | `curl` against the running service: status code and body | Code review of the handler |
| Screen works (frontend) | `browser_read_dom` with `contains:` for the element, plus screenshots at the four widths | A build that compiled |
| Screen works (mobile) | `mobile_screenshot` / `mobile_read_ui`, or the Flutter web-render fallback when no device is attached | "The widget should render" |
| AC met | Line-by-line check of every acceptance criterion against what you just verified | Tests passing |

Tests passing is NOT the same as requirements met — re-read every acceptance criterion and confirm each one is actually satisfied.

## Handoff

Then close as your prompt says: final message, no comment, no move.

If you cannot show fresh passing output, the task is not done — say what actually failed instead. And do not re-run a check you already have fresh output for: once a build has passed on the code as it stands, running it again proves nothing and costs the run.

## Red Flags — STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Done!", "Perfect!")
- Finishing a run without having run the checks in it
- Relying on partial verification ("the linter passed")
- Running the same check twice over unchanged code — that is not rigor, it is a loop

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification. |
| "I'm confident" | Confidence is not evidence. |
| "Just this once" | No exceptions. |
| "Partial check is enough" | Partial proves nothing. |
| "I'm tired / it's late in the task" | Exhaustion is not an excuse. |
