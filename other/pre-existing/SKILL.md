---
name: pre-existing
description: Fix any test/lint/type/build/CI failure instead of dismissing it as pre-existing, flaky, or unrelated. Triggers on red checks or `/pre-existing`.
argument-hint: "[optional: name of the failing check, file, or error]"
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Pre-Existing

**Don't investigate whether it's pre-existing. Just fix it.**

We don't care who broke it, when, or whether your changes caused it. The only acceptable end state is **all checks green**. Skip the forensics.

## When to invoke

Whenever you are about to:

- Call a failure "pre-existing", "already broken", "already failing", "was already there", or "not introduced by my changes"
- Call a test "flaky", "unrelated", "intermittent", or "environmental"
- Suggest the user "skip", "ignore", or "move on past" a test, lint, type, build, or CI failure
- Use `git diff` / `git blame` / `git stash` to argue a failure isn't your fault
- Stop a turn while any check is red

Also when the **user** types `/pre-existing`.

## Common rationalizations

If you catch yourself thinking any of these, the answer is in the right column.

| Rationalization | Reality |
|---|---|
| "It was failing before my changes" | CI was green at the branch point. If it's red now, something changed — a dep update, a generated file, a type-narrowing edit elsewhere. Bisect. |
| "`git diff` doesn't touch this file" | Indirect deps, generated files, transitive type changes, and snapshot drift can break distant checks. The diff is not the blast radius. |
| "It's a flaky test" | Known by whom? Link the issue. If you can't, it's not flaky — it's a race or shared-state bug you haven't found yet. |
| "Out of scope for this PR" | Green CI is in scope for every PR. There is no PR for which red CI is acceptable. |
| "The test must be wrong" | Maybe. Verify — don't assume. If it really is wrong, fix the test; don't delete or skip it. |
| "Works on my machine / differs from CI" | Match the environment. That's what lockfiles, containers, and CI configs are for. |
| "I'll fix it in a follow-up" | Follow-ups don't happen. Fix it now, in this change, before the next bug lands on top. |

## What to do

1. **Reproduce.** Re-run the failing command. Capture the full output — exact error, file, line, stack trace.
2. **Read.** Open the failing file and the production code it exercises. Read every line of the error before diagnosing.
3. **Fix the root cause.** Edit the offending code. If the production code is correct and the check is stale (renamed symbol, outdated snapshot, old type), fix the test/lint/type expectation instead. If the failure is a tooling regression, update the dependency or config.
4. **Re-run the full suite.** Not just the one test — the whole failing command. Confirm green before stopping.

Do **not**:
- Run `git stash`, `git switch`, or any "is this my fault?" verification
- Add a skip / xfail / `// eslint-disable` / `# type: ignore` without explicit user OK
- Comment out the failing test or assertion
- Lower the strictness of the check
- Rebase/squash/force-push to make the failure disappear from the diff

## If you genuinely cannot fix it

Some failures are outside the current scope (e.g. an integration test that needs a network resource you don't have, or a fix that would require changes the user hasn't authorized).

1. State the root cause and what you tried.
2. Propose a concrete fix.
3. Ask the user whether to defer, suppress (with their approval of the exact suppression), or keep investigating.

The user — not you — makes that call.

## Escalation

After 2 failed fix attempts, invoke `/second-opinion`. After 4, invoke `/hard-fix`. Don't keep retrying the same approach.

## Examples

**typecheck error in a file you didn't touch.**
Wrong: "Pre-existing — my changes only touched `src/api/`." Stop.
Right: Read the error. Fix it. Re-run `tsc`. Green.

**A flaky-looking test.**
Wrong: "Flaky — unrelated to this PR."
Right: Read the test. Find the race / shared state / missing await. Fix it. If you can't, escalate to the user with what you checked.

**Lint warning in legacy code.**
Wrong: "Pre-existing in legacy code, ignoring."
Right: Read the warning. Fix it (usually three lines). If it's a stylistic rule that genuinely doesn't apply, ask the user before adding a scoped override.

## User-approved exceptions

If the user has explicitly told you in this session that a specific failure is OK to leave alone ("yeah, skip the e2e suite, staging is down"), honor it — and quote their words when you do. Do not infer permission from silence.
