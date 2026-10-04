---
name: pr-fix-ci
description: "Activate when a pull request has failing CI checks that require code fixes."
---

## Required `<project-root>/docs` reads

Read these project-root spec files before fixing failing CI checks (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/git-hosts.md`

Fix failing CI checks on a PR by reading check logs, fixing the code, pushing, and verifying green. Tools: git host tool (see `<project-root>/docs/git-hosts.md` in the project root). Check source: `gh pr checks` / `gh pr view --json statusCheckRollup` (CLI fallback per `<project-root>/docs/git-hosts.md`).

Modes: `review` (default; approval required before commit/push) or `auto` (commits/pushes without approval). `<pr-ref>` is the only authoritative source for the target PR — never assume current branch determines it.

> CRITICAL: in `review` mode, get explicit approval (Step 10) before committing or pushing. Never infer approval.

### 1. Interpret Arguments
`auto` → `<execution-mode>` = `auto`; PR number/URL → `<pr-ref>`; extra guidance → `<additional-context>`; otherwise → `review`.

### 2. Load PR Context
Verify git host auth (see `<project-root>/docs/git-hosts.md`). Resolve project root via `git rev-parse --show-toplevel` → `<repo-path>` (use as `cwd`). View PR via git host view PR (includes checks) or CLI fallback:
```bash
gh pr view <pr-number> --json number,title,headRefName,baseRefName,url,state,statusCheckRollup
```
Extract `<pr-branch>`, `<base-branch>`, `<pr-number>`, `<pr-url>`. Run `git branch --show-current` → `<current-branch>`.

### 3. Align Local Branch
If `<pr-branch>` unavailable → STOP. Check out via git host checkout PR or `gh pr checkout <pr-number>`. Store as `<active-branch>`. Checkout fails → STOP. Don't modify code until `<active-branch>` == `<pr-branch>`.

### 4. Identify Failing Checks
From `statusCheckRollup` (or `gh pr checks <pr-number>`), collect checks where state is `FAILURE`, `ERROR`, `CANCELLED`, or `TIMED_OUT`. Store each as `<check>` with `<name>`, `<state>`, `<run-id>` (Actions runs only), `<url>`. Pending/in-progress checks → wait and re-poll once before deciding (transient). No failing checks → output "No failing checks" and stop.

### 5. Read Failure Logs
For each `<check>`: Actions run → `gh run view <run-id> --log-failed` (failed steps only); fall back to `gh run view <run-id> --log` if empty. Non-Actions check → no CLI logs; open `<url>` and read the rendered failure output via `webfetch` if reachable, else record `<url>` for the user. Extract `<error-lines>` (first error/stack/assertion), `<failing-file>`, `<failing-test>`, `<failing-command>`.

### 6. Triage Failures
Classify each `<check>`:
- `code` — failure caused by the PR's code (compile error, test failure, lint violation). Fix in Step 8.
- `flaky` — transient (network timeout, race, known-flaky test). Re-run, don't fix code.
- `infra` — environment/runner issue (missing secret, service down, quota). Report; don't fix code. Re-run only if user confirms.
- `required-status` — required status check missing or pending (e.g., no recent review). Out of scope; report.

Record `<classification>` per check. Move `flaky`/`infra`/`required-status` to `<not-fixing>` with reason. If every failure is non-`code` → output summary and stop (suggest re-runs where applicable).

### 7. Plan Fix
Fast path: every `code` failure is a straightforward fix with no cross-check dependencies → `<implementation-plan>` = `trivial`, skip to Step 8. Otherwise: build ordered fix list (compile/build → test → lint; then shared file, then check). Merge failures sharing one root cause into one fix. Map dependencies → `<dependencies>`.

### 8. Implement Fix
Fix on `<active-branch>`, focused minimal changes, follow existing patterns. Address root cause, not the symptom (don't disable a failing test; fix what it asserts unless the assertion is wrong — then fix the assertion with justification). Store `<changes-count>`.

### 9. Validate Locally
Reproduce each fixed `<check>`'s `<failing-command>` locally (lint/build/test on changed files). Confirm green. If a check can't run locally (e.g., platform-specific), state so and rely on Step 12. Store `<validation-results>`, `<validation-passing>` (`yes`/`no`).

### 10. Approval Gate (mandatory in `review` mode)
Never skip. Only `decision: approved` counts. If `<validation-passing>` = `no` → STOP. If `auto` mode → skip to Step 11.

Present gate: failing checks fixed, changed file count, local validation results, any `<not-fixing>` items (flaky/infra with suggested re-runs). Ask (header `Approval`): "Ready to commit and push?" Options: `Go Ahead` (→ `approved`) or `Needs Review` (requires feedback → `concerns`).

- `approved` → Step 11. `concerns` → store `<review-feedback>` → refine (8) → re-validate (9) → re-present gate. Repeat until `approved`.
- When `<changes-count>` = 0 (all non-`code`), surface no-change state so user picks `Go Ahead` (no-op) or `Needs Review`.

### 11. Commit and Push (after `approved` or in `auto` mode)
`git add -A`, `git commit -m "<message>"` (lowercase, `<prefix>: <summary>`, under 50 chars), `git push origin <active-branch>`. Never use generic messages like "fix ci". Do not poll CI, wait for results, or loop back to earlier steps. Session ends after push.

## Output
Summary of fixed checks, local validation, and pushed state. At the approval gate: one line per fix, not full diffs. Example: "Fixed N failing checks across M files" + local validation + "pushed to `<active-branch>`". Do not claim CI is green — it has not been verified.
