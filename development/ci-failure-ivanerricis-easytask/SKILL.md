---
name: ci-failure
description: Find and fix a red CI run of EasyTask (frontend, backend ubuntu/windows, audit, versions, e2e shards) without gh or a local Rust build. Use when a check fails on a PR, when a "check_run.completed ... failure" notification arrives, or before blaming a flaky test.
---

# CI failure (EasyTask)

Workflow `.github/workflows/ci.yml`. Jobs: `versions`, `frontend` (eslint, e2e typecheck, `npm run test:coverage`, build with tsc), `backend` (ubuntu and windows: fmt, clippy `-D warnings`, test), `audit`, `e2e` (3 Linux shards). The Windows e2e job runs only by `workflow_dispatch`.

## Tools
There is no `gh` in the cloud session: use the GitHub MCP tools (`ToolSearch` with `select:mcp__github__pull_request_read,mcp__github__actions_list,mcp__github__actions_get,mcp__github__get_job_logs`).
- Checks of a PR: `pull_request_read` with `method: get_check_runs`.
- Runs of a branch: `actions_list` (`list_workflow_runs`, `workflow_runs_filter` with `branch`).
- Log: `get_job_logs` with the `job_id` of the check and `return_content: true`, `tail_lines` 400 for an e2e shard (the failures are in the last part; the spec reporter summary lists every failing test with the file and line).
- `failed_only: true` needs the `run_id`.

## Method
1. Read the failing check and its log. Quote the real error before touching code.
2. Rule out a failure that is not the PR's: is it red on `master` too? Same error on one re-run? Only then it is not yours; say it in one comment on the PR.
3. Reproduce locally what can be reproduced (`npx eslint .`, `npx tsc -b`, `npm run e2e:typecheck`, `npx vitest run <file>`). Rust cannot be compiled in the cloud container (missing GTK libs): read the compiler error from the log and fix by reading the code.
4. Fix the cause. Never skip, disable or quarantine a test to get green; never push an empty commit to kick the CI.
5. Run the fast checks again, commit with a clear message (no signature lines if the user said so), push, then wait for the next run: the PR events wake the session, do not poll with sleep.
6. After a push from the cloud, the local ref `refs/remotes/origin/<branch>` may be missing and the stop hook complains: check with `git ls-remote origin <branch>` and run `git update-ref refs/remotes/origin/<branch> HEAD`.

## Known traps (all happened)
- **Rust `-D warnings`**: a helper used only by tests must be `#[cfg(test)]`; `Option::get` on settings needs `?` (`settings?.get(..)`). Dead code and unused imports fail clippy.
- **e2e and translations**: the specs read texts with `tr("key")`. Removing, merging or renaming a key in `src/i18n/locales/*` breaks the specs even if vitest is green. Search `e2e/` for the key (see the `i18n-keys` skill).
- **Tauri permission missing**: a plugin command without its permission in `src-tauri/capabilities/default.json` fails only in the real app, for example `store.entries()` without `store:allow-entries` made the preferences come back as defaults (see `tauri-permission`).
- **Drag on Linux**: the WebKitGTK driver does not deliver the pointer events of a drag. Drag specs must `this.skip()` when `process.platform === "linux"`.
- **Single pane has no `data-pane`**: `[data-pane]` exists only when the workspace is split. Select tabs with `[role="tab"][title=...]` when there is one pane.
- **Dialogs open after the menu closes**: wait for the dialog button (`waitUntil` on `topDialog()` plus `byText`) instead of reading the top dialog at once.
- **Debounced store save** (`src/lib/store/save-soon.ts`, 500 ms): the specs that restart the app wait until `settings.dat` contains the values.
- **Flaky multi-select color undo** passed on a re-run: re-run only once, and only for a failure that dies before the test body, otherwise treat it as real.
