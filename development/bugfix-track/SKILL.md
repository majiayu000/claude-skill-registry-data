---
name: bugfix-track
description: Takes a bug from report to reproduction, root cause, regression test, minimal fix and a verified pull request, stopping for approval between steps. Use for any bug worth fixing properly.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: workflow
  category: debugging
  source: https://hermes-ide.com/prompts/bugfix-track
  catalog: 2026.1014.1
---

# Bugfix track

## Inputs

- [BUG_REPORT] (required): The bug as reported, verbatim if possible - what happened, what was expected, steps, error messages, screenshots described in words, and a link or id if there is one.
- [ENVIRONMENT] (optional): Where it happens - app version or commit, OS, browser or runtime, configuration, data or account involved, and whether it is production, staging or local.
- [SEVERITY] (optional; one of: low, medium, high, critical; default: medium): How bad the bug is for users. Critical and high get a mitigation check before the full fix.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

Fixes this bug properly, one approved step at a time:

<bug_report>
[BUG_REPORT]
</bug_report>
Only if [ENVIRONMENT] was provided: 

<environment>
[ENVIRONMENT]
</environment>

Severity: [SEVERITY].

The order is fixed: reproduce it, find the root cause, write a test that fails because of the bug, make the smallest fix that turns the test green, then verify everything and prepare the pull request. Each step ends with a short report and stops for the developer's approval; later steps build on the approved findings instead of re-asking. Nothing is called fixed until a test that failed before the change passes after it and the rest of the suite still passes. If the severity is high or critical, the first step also says whether users need a mitigation now (rollback, feature flag, config change) while the proper fix is made, and leaves that decision to the developer.

Throughout: read the code before making a claim about it, run real commands and quote their real output, change only what the bug requires, and never push, merge or open a pull request without explicit approval.

## Steps

Work through these steps in order. Do not skip a gate.

1. reproduce (discover)
2. root-cause (discover)
3. regression-test (verify)
4. fix (build)
5. pull-request (ship)

### Step 1: Reproduce

Turn the report into a reproduction you can run on demand.

1. Restate the bug as observed versus expected behaviour. If a missing fact (version, input data, account state, configuration) blocks reproduction and the code, logs and history cannot supply it, ask for it in one message and stop.
2. Find the code path involved, from the entry point (route, command, handler, job) to the functions the symptoms point to. Cite file paths.
3. Reproduce it in the smallest form you can: a failing test or command is best, numbered manual steps are the fallback. Remove every condition that is not needed and list the ones that are.
4. Run it at least twice. If it fails only sometimes, say how often.
5. If you cannot reproduce it, do not guess a fix: report what you tried, the setup differences that could matter, and what information or instrumentation would most likely make it reproducible.
6. For high or critical severity, say who is affected now and whether a mitigation (rollback, flag, config change) would stop the harm meanwhile. Recommend it; do not apply it.

Report: the bug in one sentence, the exact reproduction with its quoted output, the required conditions, reproduced (yes, intermittent with rate, or no), and the mitigation if relevant.

Stop and wait for approval.

**Gate:** stop here and wait for the user's approval before step 2 (root-cause).

### Step 2: Root cause

Find why it happens, not just where it shows up.

1. List at most three hypotheses, ranked by how well each explains every symptom, including which conditions are required and which are not.
2. Test them one at a time with the cheapest experiment that tells them apart: a log line or breakpoint, a changed input, `git bisect` against a known-good version, a smaller reproduction. Change one thing per experiment and record the result.
3. Follow the chain to the decision in the code, data or configuration that is wrong, and explain the path from it to the symptom.
4. Ask once more why it was possible (a missing validation, a wrong assumption about an API, an unhandled state), because that decides whether the fix is local or belongs at a boundary.
5. Search for the same pattern elsewhere and list the places. Do not fix them yet.

Report: the root cause with `path:line` references, each experiment and its result, the hypotheses ruled out, why it was possible, the same pattern elsewhere, and one to three fix options with scope and risk, recommending one.

Stop and wait for approval of the cause and the fix option.

**Gate:** stop here and wait for the user's approval before step 3 (regression-test).

### Step 3: Regression test

Write the test that proves the bug, before changing the code under test.

1. Pick the cheapest level that reaches the root cause: unit if the faulty decision is in one function, integration if it lives between components or in the database, end-to-end only if nothing smaller can reach it.
2. Follow the project's test conventions; read a neighbouring test first.
3. Name the test after the behaviour, not the ticket, and assert on the outcome the user cares about with a message that explains the failure.
4. Make it deterministic: fixed clocks, seeds and data, no sleeps. For an intermittent bug, force the bad timing instead of hoping to hit it.
5. Run it against the unfixed code and confirm it fails on the bug's assertion, not on setup.

Report: the test's path, name and code, and the quoted failure with why it is the bug.

Stop and wait for approval before changing the code under test.

**Gate:** stop here and wait for the user's approval before step 4 (fix).

### Step 4: Fix

Make the smallest change that fixes the root cause.

1. Implement the approved option at the root cause. No special-casing the test's inputs, no catch-and-ignore, no retries that hide the failure, no unrelated refactors or formatting.
2. Run the regression test and confirm it passes. Then run the module's tests (the full suite if it is reasonably fast), the type check and the linter. If something unrelated was already failing, show that it fails on the original code too.
3. If callers may rely on changed behaviour (an error type, a return value, a default), list them and say whether they need updating.
4. Remove any temporary instrumentation from step 2.

Report: the diff with a line per hunk, every check with its real result, behaviour changes for callers, and anything noticed but not changed.

Stop and wait for approval before preparing the pull request.

**Gate:** stop here and wait for the user's approval before step 5 (pull-request).

### Step 5: Verify and prepare the pull request

1. Run the original reproduction from step 1 again and confirm the bug is gone. Quote the output. If the app can be run locally, check the behaviour once as the reporter would.
2. On a branch named after the behaviour (for example `fix/expired-discount-accepted`), commit the test and the fix with a message that says what was wrong and why, following the project's commit conventions.
3. Write the pull request description: the problem as the user saw it with the report's link or id; the root cause in two or three sentences; the fix and why it belongs there; the regression test and proof it failed before; risk and rollout notes (caller changes, what to watch, any mitigation to remove); and follow-ups (the same pattern elsewhere, things noticed but not changed).
4. Show the branch, commit and description. Push and open the pull request only if the developer says so; otherwise give them the commands.
