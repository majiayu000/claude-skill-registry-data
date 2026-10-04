---
name: healer
description: Run moflo's Healer (`flo healer`, alias for `flo doctor`) from inside the Claude session. Audit-only by default; pass `--fix` to apply auto-repairs, `-c <component>` for a single check. Use when something feels off (missing moflo.yaml, daemon dead, statusline empty, hooks not firing) or as a periodic health check. Distinct from Claude Code's built-in `/doctor`, which diagnoses Claude Code itself, not moflo.
arguments: "[options]"
---

# /healer — moflo Installation Healer

Thin wrapper around the `flo healer` CLI. All check + fix logic lives in the CLI; this skill just shells out, surfaces results in-thread, and gives one-line follow-up nudges.

**Arguments:** $ARGUMENTS

## Procedure

1. **Memory first** (gate requirement):
   ```
   mcp__moflo__memory_search { query: "doctor healer fix moflo.yaml gate hook wiring", namespace: "guidance" }
   ```

2. **Run the CLI** with the user's arguments passed through:
   ```bash
   npx moflo healer --json $ARGUMENTS
   ```
   - No args → audit-only.
   - `--fix` → CLI runs auto-repairs after the audit.
   - `-c <component>` → restricts to one check.
   - Always include `--json` so output is machine-parseable.

3. **Surface the JSON in-thread**. Group by status:
   - `✓ N passing` (count only)
   - `⚠ warnings` — list `name: message`; flag with `[auto-fixable]` when the result has a `fix` field
   - `✗ failures` — same
   - If `--fix` mode, read `fixesApplied[]` from the JSON payload and list `{name, applied}` per entry — applied=true → "fixed", applied=false → "needs manual action". The `results[]` array is post-fix state (re-evaluated), so report the final status.
   - If `--install` was passed, surface `claudeCodeInstall.installed` from the payload.
   - If `--kill-zombies` was passed, surface `zombieScan.killed` / `zombieScan.found` from the payload.

4. **Nudge based on what changed.** Only mention next steps for state that *actually* changed:
   - Daemon restarted → `Statusline should refresh within ~5s.`
   - `moflo.yaml` created → `Review the new defaults at the project root before your next deep run.`
   - Hook wiring repaired → `Restart Claude Code so the new SessionStart hook fires next launch.`
   - In audit-only mode with auto-fixable issues → `Run /healer --fix to repair.`

## Rules

- **Don't** re-document checks or fixes here. The CLI's `--help` and `src/cli/commands/doctor-*` are the source of truth.
- **Don't** call `flo doctor` directly — use the `healer` alias for thematic consistency. They're equivalent CLI-side.
- **Don't** swallow non-zero exit codes silently — surface them in the summary.
- **Note for users:** Claude Code has its own built-in `/doctor` command that diagnoses Claude Code itself. This skill (`/healer`) diagnoses **moflo**, not Claude Code. The two are complementary, not duplicates. The healer rolls in the user-actionable parts of `claude doctor` (Claude Code version freshness vs npm latest) into its own `Claude Code CLI` check; the rest of `claude doctor` is a TUI on current releases and must be run interactively if you need its full report.

## See Also

- `flo doctor --help` — full flag/component list
- `/eldar` — broader project-setup audit; consults the Healer as one input
