---
name: preflight-checks
description: "Reference document describing six pre-flight checks (clean git state, not detached HEAD, gh auth, issue exists and OPEN, remote reachable, duplicate-branch warning) as pure bash exit codes with no LLM calls. Reference only (policy document; consumed by `/flow:start` Phase 0)."
allowed-tools: Read
agent: general-purpose
disable-model-invocation: true
---

# Pre-flight Checks

## Contract

Iron law: no LLM calls in pre-flight — every check is a bash command with a pass/fail exit code, and a failed pre-flight stops the workflow before any token is spent on planning. Consumed by `/flow:start` Phase 0 (PRE-FLIGHT); the runnable bash lives in `plugins/flow/commands/start.md` and is never invoked as `Skill(preflight-checks)`. That bash returns a `### Pre-Flight` section with `ISSUE_NUM=`, `PREFLIGHT_ERRORS=`, `PREFLIGHT_WARNINGS=`, `PREFLIGHT_STATE=PASSED|BLOCKED`, then one `PREFLIGHT_FAIL=<reason>` line per error and one `PREFLIGHT_WARN=<reason>` per warning. `PREFLIGHT_STATE=BLOCKED` halts before EXPLORE. Permitted skips: none — warnings surface and proceed; errors always halt.

## What Pre-flight Protects

Pre-flight is the cheapest filter: it runs before EXPLORE, before any agent dispatch, before any reasoning, and fails fast on conditions that would invalidate everything downstream. Because it is honest about what it proves, downstream phases trust their preconditions and stop re-checking them.

## The Checks

| # | Check | Failure mode it prevents |
|---|-------|--------------------------|
| 0 | Issue number present and all-digit | Non-numeric argument reaching the prompt context or a shell (`git checkout -b "feature/issue-${ISSUE_NUM}-..."`). |
| 1 | Clean git state (`git status --porcelain` empty) | Starting a feature branch on unrelated dirty state and shipping it in the PR. |
| 2 | Not on detached HEAD (`git symbolic-ref HEAD`) | Commits with no branch reference that vanish on the next checkout. |
| 3 | `gh auth status` succeeds | Spending tokens on planning, then failing at the first `gh issue view`. |
| 4 | Issue exists and state is `OPEN` | Working a closed, deleted, or mistyped issue — a PR with nothing to close. |
| 5 | `git ls-remote --exit-code origin` succeeds | Reaching the push step and discovering the remote is unreachable or misconfigured. |
| 6 | Current branch already matches `issue-$ISSUE_NUM` (warning only) | Re-starting an issue already in progress on this branch — recoverable, so warn not fail. |

Checks 0–5 are **errors**: any one fails, the workflow halts. Check 6 is a **warning**: noted in output, workflow proceeds.

## Behavior Contract

- **ERRORS > 0**: halt. Do not proceed to EXPLORE. Do not spend tokens on planning.
- **WARNINGS only**: surface in output, proceed normally.
- **No LLM calls, no Agent dispatches, no Skill invocations** during pre-flight.
- **Total execution**: one Bash call, sub-second. If pre-flight is slow, it has scope creep.
- Output follows `references/command-output-format.md` (section heading + `KEY=value` records + state sentinel).

## Where the Bash Lives

The single runnable copy is the bash block under "Phase 0: PRE-FLIGHT" in `plugins/flow/commands/start.md`; `$ARGUMENTS` supplies the issue number. This skill intentionally does not duplicate it — two copies drift silently. Policy and rationale live here; shell lives in the command.

## Extending Pre-flight

A new check must satisfy all four, or it belongs in EXPLORE or a domain skill:

1. Representable as a single bash exit code — no LLM judgment, no multi-step reasoning.
2. Cheap — sub-second, no network beyond the `gh` and `git` calls pre-flight already makes.
3. Protects against a concrete failure mode — add a row to the table above.
4. Classifies cleanly as ERROR (halts) or WARNING (surfaces).

Add the check to the start.md bash block and its row here in the same change.
