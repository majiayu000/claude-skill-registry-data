---
name: verify
description: "Use before saying done, fixed or passing, before a commit or PR, or when asked 'have I missed something?'"
license: MIT
metadata:
  reviewed: "2026-11-01"
  sources: "obra/superpowers 7.0.0 skills/verification-before-completion; cursor/plugins pstack 0.15.25 skills/principle-prove-it-works, skills/principle-sequence-verifiable-units; garrytan/gstack 1.60.1.0 review/checklist.md (enum completeness), ship/SKILL.md.tmpl (verification gate); MCT (local) ~/.claude/MCT.md (Check Selection, Post-Task Verification, Completion Receipt), skills/have-i-missed-something, skills/testing-strategy, agents/test-runner.md"
---

# Verify

This is the gate between "I changed it" and "it's done". Prove the claim itself, not a proxy for it.

For app, CLI or service behavior, first look for the repository's project-local verification skill and feature map. Reuse its launch, doctor, drive and cleanup instructions and select the changed journeys. Missing or stale harness: use `project-verify` when creation/maintenance is requested; a focused verification can still use the repo's existing checks and state the coverage gap. Do not turn every small change into harness creation.

## Task evidence

For non-trivial execution, inspect `honey task status --json`. Codex uses `CODEX_THREAD_ID`; on other hosts pass `--agent claude --session <session-id>` to every command. Replace `<session-id>` and `<call-id>` with the real host identifiers. When the task's project differs from the session directory, pass `--cwd /actual/project` to `task set` before running checks.

- Code: `honey task set --mode execute --operation code`. The default `verification` check accepts a recognized successful test/lint command in this task's workspace after its latest observed mutation. For separate test and lint requirements, add `--check tests --check lint` and map each result explicitly.
- If the host hides commands inside opaque tool wrappers, run `honey task run --check verification -- python3 tests/run.py`. Honey launches the check itself and records its real exit status against the task's Git source snapshot. It never accepts printed success text. The proof survives opaque wrapper bookkeeping only while the source, Git HEAD and index still match; failed reruns and known edits invalidate it. The project must be a Git root with at most 20,000 non-ignored files and 64 MiB of source, without source symlinks.
- Uninstall: `honey task set --mode execute --operation uninstall --target /Applications/Example.app`. Required checks are `application`, `helpers`, `startup`, and `preserved-data`. Name the real app path. Check registrations as well as files; record anything deliberately retained.
- Startup change: `honey task set --mode execute --operation startup`; the `startup` check must inspect the resulting registration, not just the command that changed it.
- Link a completed assertion/check using `honey task verify --check startup --tool-call <call-id>`. Only a successful observed call in the current task/workspace after the latest mutation is accepted. Choose a command whose assertion actually proves the named check; exit zero alone does not establish semantics.
- For a declared file target, `honey task verify --check application --absent /Applications/Example.app` measures absence directly. `--present` measures existence. Neither executes a shell command.

The task record is an evidence aid, not a permission grant or a complete sandbox. Opaque wrappers and unobserved external changes cannot be verified. State that limit; do not relabel unknown status as a pass. Recheck after changes. A failed or incomplete recognized check must be rerun successfully or explicitly reported as unresolved. Read-only answers need no execution contract or receipt.

## 1. Match each claim to its evidence

| Claim | Evidence that proves it | Not enough |
|---|---|---|
| Tests pass | Test command output: 0 failures, exit 0 | An earlier run, "should pass" |
| Types or lint clean | `tsc` / linter output: 0 errors | One passing (lint doesn't compile) |
| Build succeeds | Build command exits 0 | Lint passing, logs look fine |
| Bug fixed | The original symptom, reproduced, now gone | Code changed, assumed fixed |
| Regression test guards it | Revert fix: fails. Restore: passes | Passes once |
| Subagent finished | The diff shows the change and you ran its check | "Success" in its report |
| Requirements met | Each requirement line checked against the change | Tests passing |
| UI works | Browser run with tool, URL, viewport or flow, result | Screenshot from before the last edit |

Read the actual value and run the actual feature. File mtimes, cached output and "it compiles" are proxies. When a check fails strangely, suspect the way you observed it before the system. Where you can, script the comparison so it re-runs, and keep its output visible.

Re-run after any edit. Evidence describes the tree it ran on, so a fix made after the test run needs a fresh run.

Done when: every claim you are about to make has fresh evidence from this turn.

## 2. Pick checks by changed surface

Match the weight of the checks to the risk. Use the repo's own scripts (package.json, Makefile, justfile, CI config) rather than inventing commands.

| Changed surface | Minimum checks |
|---|---|
| Copy or style only | Inspect the diff. Add a browser check if layout could shift. |
| React component or hook | `npx -y react-doctor@latest . --verbose --diff`, plus a targeted test if behavior changed |
| Shared logic, routing, data fetching | Typecheck and targeted tests |
| Auth, payments, permissions, user data | Typecheck, targeted tests including negative and permission cases, and a security read of the diff |
| Broad refactor | Typecheck, relevant tests, the `review` skill, and React Doctor if React changed |
| PR-ready | The lint, typecheck and test commands the repo defines |

Run a full build only for a broad or risky change, or when asked. For multi-step work such as sweeps, migrations or runs of similar edits, check each unit before starting the next. A break caught at the unit that caused it is cheap to find.

For browser verification, follow [WebMCP verification](references/webmcp.md) and the `qa` skill. Reuse verified tools to replace eligible setup, then exercise the affected UI and assert independent outcomes. Reuse existing tests and preflight; add separate tool-contract tests only when that contract is in scope or required coverage is missing. WebMCP does not replace lint, types, backend tests, native mobile checks or visual proof. If unavailable, report the fallback; if required, record a failed or blocked requirement.

Done when: each applicable row has run and you have read its output, or it is listed as skipped with the concrete blocker.

## 3. Finish audit ("have I missed something?")

Go line by line:

- **Reach.** Every caller, test, fixture, mock, type, config and doc that references a changed symbol was updated. Grep for it, including string and dynamic references.
- **Completeness.** A new enum value, status or flag is handled by every consumer that switches on its siblings (allowlists, `switch`/`case` chains, UI dropdowns, persistence).
- **Clean-up.** Debug logs, temporary tags, `.only`/`.skip`, commented-out code and scratch files are gone. `git diff` shows only intended changes.
- **UI proof.** A visible UI change was exercised in a browser through the `qa` skill, with the tool, URL, viewport or flow, and result.
- **TODO.md.** An item is ticked only after its proof exists. Blocked items stay unchecked with the blocker written under them.
- **Docs.** README, help text, examples and comments match the new behavior, setup, commands or API.
- **Scope.** Re-read the request. Everything asked for is present and nothing unasked was added.
- **Shortcuts.** Every `shortcut:` you added names its limit and its upgrade trigger.

Fix what you can before replying. Anything you can't fix goes into Skipped or Risk with its reason.

Done when: every line is true or recorded.

## 4. Report

Answer the user's question first: for a coverage or yes/no question, state the answer and its limits before the evidence. Close an execution report with the receipt line; a read-only lookup does not need an execution receipt:

```
Checks run: <cmd> pass, <cmd> fail (<n>). Skipped: <check> (<concrete reason>). Risk: <thing>.
```

Name failures as failures, including pre-existing ones you saw. Leave out empty parts.
