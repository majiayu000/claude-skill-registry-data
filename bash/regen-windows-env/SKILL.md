---
name: regen-windows-env
description: Environment recipes for building, testing, and shipping regen-civics from Rye's Windows machine and the Cowork sandbox. Use when tests fail with React.act errors, when the sandbox mount shows phantom git changes, when long commands time out, when node_modules symlinks break tsc, or before running any pnpm/git/railway command from an agent session.
---

# ReGen Windows Environment

Mined 2026-07-17 from session memory that only Cowork could see. These quirks break builds and tests for any agent that does not know them. Deterministic recipes, no judgment calls.

## Test and typecheck

- A global `NODE_ENV=production` env var breaks vitest React component tests (`React.act is not a function`). Always run `npx cross-env NODE_ENV=test vitest run ...`.
- The typecheck script is `pnpm check`. (`pnpm typecheck` exists now only as an alias; older docs referencing it were wrong for months.)

## Cowork sandbox limits

- The sandbox cannot run the node toolchain: pnpm's Windows junction symlinks in node_modules give I/O errors through the mount. Pure-python repo scripts against the mount are fine (audit-truncation.py works).
- The FUSE mount can serve STALE state: phantom truncated files, phantom deletions in `git diff`, phantom index.lock (observed 2026-07-12). Never trust `git status/diff` or sandbox file reads for this repo; verify on the real filesystem. Host-path Read/Write/Edit tools are fine.
- Background processes do not survive between sandbox bash calls, so anything needing a live server or browser install cannot run there.

## Desktop Commander (cmd.exe) recipes

- Syntax: `cd /d "path" && ...`.
- Long jobs: output capture times out around 2 to 3 minutes and can falsely return "0 lines". Redirect to a file and poll it: `... 2>&1 | Add-Content .verify.log` then read the file. Launch with `start /b cmd /c "... > log 2>&1"` for anything long.
- PowerShell `-Command` strings get `$` stripped (`$_` arrives as `_`). Avoid variables; pipe to `Select-Object`/`Format-List`.
- Commit and push as separate process calls: multi-part `git commit -m -m` inside a cmd /c chain can swallow the following `&&` into the commit body.
- Stale 0-byte `.git/index.lock` with no git.exe running is safe to delete. Use `git pull --rebase --autostash` since the tree usually carries unrelated local edits.

## Worktree gate recipe (isolated verification)

1. `git worktree add .claude\worktrees\<name> origin/main --detach` INSIDE the connected folder.
2. `pnpm install --prefer-offline` in the worktree (~70s). A node_modules JUNCTION breaks tsc resolution (hundreds of phantom TS2307s); a real install avoids it.
3. Run `pnpm gate` DETACHED via `Start-Process powershell` writing to a file; MCP timeouts kill child processes otherwise.
4. Targeted `git add` only (parallel sessions sweep loose edits into their commits), then `git push origin HEAD:main`.
