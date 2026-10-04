---
name: delegate-to-deepseek-harness
description: Delegate bounded, implementation-heavy, repetitive, read-heavy, or independently verifiable coding work from Codex to DeepSeek Harness, preferably through a local Harness MCP worker and otherwise through the official headless CLI. Keep Codex responsible for scope, risky judgment, review, integration, and final verification. Do not use for trivial edits, secrets, deployments, destructive operations, or work that cannot be independently checked.
---

# Delegate to DeepSeek Harness

Use DeepSeek Harness as a worker. Keep Codex as orchestrator, reviewer, and final authority.

## Core rule

Delegate execution, not responsibility. A worker report is a claim, not proof. Review the workspace and independently verify relevant acceptance criteria before reporting success.

Verify the contract, not the whole implementation again. **Delegate the work. Verify the evidence. Don't redo the work.**

## Decide whether to delegate

Delegate when the task is self-contained and at least one of these is true:

- implementation is mechanical, repetitive, or context-heavy;
- the task has clear acceptance criteria and a practical verification path;
- repository exploration can be framed as a concrete question;
- an isolated second implementation or diagnosis would be useful;
- independent tasks can run in separate worktrees.

Keep the task in Codex when it is trivial, primarily architecture/product judgment, dependent on rich unsummarized conversation context, privileged or irreversible, or not independently verifiable.

## Choose the worker path

Use this order:

1. **Harness MCP** if a configured server exposes `agent_run` and, when needed, `task_inbox` / `task_result`.
2. **Headless fallback** with `scripts/dsh_headless.sh` when MCP is unavailable and `dsh` exists.
3. If neither path is available, stop delegation and state the missing prerequisite.

Read `references/setup.md` only when setup or connectivity matters.

## Write the worker brief

Give the worker a self-contained contract:

```text
Objective:
<one concrete outcome>

Scope:
<allowed files/modules and explicit non-goals>

Constraints:
<compatibility, API, style, dependency, or user constraints>

Acceptance criteria:
- <observable condition>
- <observable condition>

Verification contract:
- allowed_paths: <glob list, e.g. src/parser/**>
- checks: <test/lint/typecheck/build commands to run>
- invariants: <no_new_dependencies | no_public_api_change | no_untracked_files | ...>
- limits: <max_changed_files | max_diff_lines>
- review_mode: receipt | targeted | full

Verification:
- <focused command/check if known>

Rules:
- Work only inside the supplied cwd.
- Inspect before editing.
- Preserve unrelated changes.
- Do not commit, push, publish, deploy, rotate credentials, or perform destructive external actions.
- If blocked, report the blocker instead of guessing.
```

Put durable context in MCP `context`; put the actionable assignment in `task`. Do not dump the entire host conversation into the worker prompt.

## Run the worker

For one bounded task, prefer synchronous `agent_run` with `task`, relevant `context`, and an absolute `cwd`.

Use queued tools only when multiple independent tasks benefit from overlap. Never run concurrent mutating workers against the same checkout. Use separate worktrees/cwds, then review and integrate in Codex.

For headless fallback, resolve this Skill directory and run:

```bash
scripts/dsh_headless.sh "<worker brief>" "<absolute cwd>"
```

## Review the result

If the MCP returns structured fields, inspect `changes`, `verification`, `leftovers`, and the final assistant text. Inspect tool traces when the summary is unclear.

First run the machine verifier with the contract from the brief:

```bash
scripts/verify_workspace.sh --allowed-paths '<glob>' --checks '<command>' [--invariants no-new-deps,no-public-api-change,no-untracked] [--max-changed-files N] [--max-diff-lines N]
```

It returns a small JSON receipt (status, changed files, diff lines, scope check, test results, risk flags). Then review by the contract's review mode:

- **receipt** (test fixes, mechanical edits, small bugs): contract PASS → report done. Do not read the diff. Do not edit.
- **targeted** (ordinary features): contract PASS → skim the changed-file summary or named high-risk hunks only. No concrete defect seen → done.
- **full** (auth, payment, DB migrations, concurrency, security, public API, broad architecture): read the full diff and review risky logic yourself.

**Stop rule — the contract is the finish line.** If the verification contract passes:

- do not make additional edits;
- do not broaden scope;
- do not refactor for cleanliness;
- do not add defensive handling;
- do not improve unrelated edge cases;
- do not rerun broader tests unless the contract requires them;
- report completion.

Reopen implementation only on a concrete contract failure or a predefined high-risk trigger. Never say tests passed unless Codex observed a reliable test result.

If the worker is blocked or wrong, either fix the issue directly or send one focused follow-up. Avoid open-ended retry loops; after two failed delegated attempts on the same failure mode, take over or report the blocker.

## Final response

Keep the user-facing answer about the task, not the plumbing. Distinguish what the worker attempted from what Codex independently verified, and mention any remaining uncertainty.

Read `references/delegation-policy.md` when routing boundaries are unclear.
