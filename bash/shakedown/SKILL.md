---
name: shakedown
description: Multi-surface product validation against live Dataverse - exercise the Extension, TUI, MCP server and CLI, compare behaviour across surfaces, audit the architecture, and write a findings report. Use before a release, after a large cross-surface feature or refactor, or when asked to kick the tires. Refuses to start without a configured safe-environment allowlist.
---

# Shakedown

A shakedown asks "does the product work" by using it on every surface, not by reading code. A passing test suite is not a shakedown. It differs from `/verify`, which checks one change on one surface.

Use it before releases, after large multi-surface features or refactors, or when asked to "test everything".

## Phase 0: Safety Pre-checks

Before any other work, validate the safety guardrails are configured and
active. The `shakedown-safety` hook (`.claude/hooks/shakedown-safety.py`) and
the C# `IShakedownGuard` consume what this phase sets up; see
`docs/SAFE-SHAKEDOWN.md` for the full model.

1. **Verify env allowlist is configured** — read
   `.claude/settings.json` → `safety.shakedown_safe_envs`, or
   `$PPDS_SAFE_ENVS`. If neither lists at least one safe env, STOP and ask
   the user to configure (`docs/SAFE-SHAKEDOWN.md` for details). Do not
   continue without one: the hook's environment gating is opt-in, so with no
   allowlist nothing stops `ppds` commands from reaching an unsafe environment.
2. **Verify active env is in the allowlist** — run `ppds env who`. It
   passes only when the active env is listed (it sends WhoAmI there), so a
   pass with the displayed env matching an allowlist entry confirms it. If
   the active env is not listed, the `shakedown-safety` hook refuses it, and
   the refusal names the active env, the allowlist and the remedy: switch
   with `ppds env select <listed env>` and run `ppds env who` again. The hook
   blocks downstream `ppds *` calls until the active env is listed.
3. **Arm the shakedown write-block (sentinel file).** Before any
   mutating Bash work (steps 1-2 are read-only checks and run first
   by design), write `.claude/state/shakedown-active.json` containing at
   least `started_at` (ISO-8601 UTC timestamp string, consumed by both
   the Python `shakedown-safety` hook and the C# `IShakedownGuard`) and,
   when available, `session_id`:

   ```bash
   python -c "import json, os; from datetime import datetime, timezone; \
     os.makedirs('.claude/state', exist_ok=True); \
     json.dump({'started_at': datetime.now(timezone.utc).isoformat(), \
                'session_id': os.environ.get('CLAUDE_SESSION_ID', '')}, \
               open('.claude/state/shakedown-active.json', 'w'))"
   ```

   The hook reads this sentinel on every Bash call and refuses mutation
   verbs (`plugins deploy` without `--dry-run`, `<surface> create/update/delete`,
   `solutions import`, etc.) for the duration of the shakedown. The sentinel
   auto-expires after 24h so a crashed session cannot wedge the write-block
   for future sessions.

   **Why the sentinel and not just `export PPDS_SHAKEDOWN=1`?** Claude
   Code's Bash tool spawns a fresh shell per invocation, so neither an inline
   `PPDS_SHAKEDOWN=1 ppds ...` prefix nor an `export` from a prior call
   reaches the hook subprocess. The sentinel file is the reliable activation
   source inside a Claude Code session. The env var is still honored for
   shell scripts and CI (its name is configurable via
   `safety.readonly_env_var` in settings.json; default `PPDS_SHAKEDOWN`).
4. **Acknowledge the model:** plugin deploys MUST be invoked with
   `--dry-run` during shakedown. To run a real deploy, delete the
   sentinel file (`rm .claude/state/shakedown-active.json`) and unset
   `PPDS_SHAKEDOWN` if it's also in the environment — deliberate action,
   there is no softer bypass.

## What to exercise

Ask which surfaces are in scope, then use each one interactively through the `/verify` skill (its sections cover launching and driving the TUI, the extension, the MCP server and the CLI). Reading code does not count as verifying an interactive feature; mark it "not tested" instead.

- **Extension:** open each panel, run a query, sort and filter results, switch profile and environment, check the error states.
- **TUI:** launch, switch profile and environment, open every screen from the menus, send keystrokes, read the rendered text.
- **MCP:** invoke each tool against the safe environment (server launched with `--read-only`) and check the responses.
- **CLI:** run the command groups with `--output-format json` and without; check data on stdout, status on stderr, and exit codes.

Build a feature-by-surface matrix from `specs/` and `src/` first, confirm it with the user, and record pass or fail with evidence (screenshots, output) for each cell.

Then:

- **Parity:** for features on more than one surface, note differences and say which is a bug and which is acceptable.
- **Architecture audit:** direct `ServiceClient` use outside the pool, empty or non-logging catch blocks, commands or handlers that are not wired up, TUI screens unreachable from menus, business logic outside Application Services (see `specs/CONSTITUTION.md`).

## Findings

Write `docs/qa/{date}-{scope}.md`: surfaces tested, bugs found and fixed, bugs found and not fixed (with severity), the matrix, the parity table, audit findings, and untested areas with reasons. Present findings and let the user decide what to defer; do not recommend deferral. Investigate failed background tasks rather than dismissing them.

## Finish

Before declaring complete, list the untested features and get the user's explicit sign-off on skipping them. Then **disarm the shakedown write-block** — delete the sentinel file as
the very last act:

```bash
rm .claude/state/shakedown-active.json
```

A leftover sentinel keeps the write-block armed for any subsequent
session in this worktree until it expires 24h later. Delete the
sentinel explicitly; do not rely on the staleness expiry.
