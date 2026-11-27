---
name: daily-auth
description: Use at the start of a working day to check and fix every login and credential the day needs - when the user says "new day", "good morning", "start of day", "run my logins" or "check auth", when board rollover calls it, or when the new-day hook says daily-auth has not run yet today.
---

# Daily auth

Checks every login and credential on this machine once a day and fixes what it can, so nothing stalls on a login later while the user is away. The user approves permission prompts and finishes browser steps; they never have to remember which logins exist.

## Config

The per-machine list lives in `~/.claude/auth-checks.json`. Start from `auth-checks.example.json` next to this file. Each entry:

| Field | Meaning |
|---|---|
| `name` | Short label shown in the results |
| `kind` | `shell` (a command), `mcp` (one cheap read call on that MCP server) or `browser` (a page check in Chrome) |
| `check` | The command, or the instruction for `mcp` and `browser` checks |
| `pass` | `exit0` (passes on exit code 0) or `regex:<pattern>` (passes when the output matches) |
| `fix` | The command or instruction that fixes a failure |
| `fix_kind` | `auto` (run it), `interactive` (run it while the user finishes a browser or app step) or `manual` (only the user can do it) |
| `covers` | Optional: other entries or profiles that one run of this fix also fixes |

If `~/.claude/auth-checks.json` is missing, say so, point at `auth-checks.example.json` in this skill's folder, and stop.

## Steps

1. Read `~/.claude/auth-checks.json`. If `~/.claude/daily-auth-last-run.json` already has today's date (`date +%F`) and the caller only needs status (the board's access check), reuse it: report its results and re-run only the checks not marked `pass` or `fixed`.
2. Run every check:
   - `shell`: one Bash call each, read-only, 30 s timeout. Judge it with `pass`.
   - `mcp`: one cheap read call on that server (a search or a "who am I" call). Any auth error fails it.
   - `browser`: dispatch a sonnet agent with the Chrome tools to do what the entry says and report pass or fail.
3. Fix each failure right away, without asking first:
   - `auto`: run the fix, then re-run the check.
   - `interactive`: run the fix with a long timeout (up to 10 minutes) while the user approves the prompt and finishes the browser or app step, then re-run the check.
   - When one fix `covers` several entries, run it once and re-check all of them.
   - `manual` fixes, and any fix that failed twice, go on a short TODO list for the user: `! <fix>` plus what it blocks.
4. Write `~/.claude/daily-auth-last-run.json` when finished, even with leftovers. This is what quiets the new-day hook:

   ```json
   {"date":"<date +%F>","at":"<date -u +%H:%MZ>","results":[{"name":"...","status":"pass|fixed|needs_user","todo":"! <fix> (blocks: ...)"}]}
   ```

   `todo` only on `needs_user` rows.
5. Output one line per check: `pass`, `fixed`, or `needs you: ! <fix> (blocks: ...)`. Nothing else.

## Unattended runs

When the turn was started by a task notification, a `/loop` tick, a scheduled task or another session's message, the user is probably not watching. Run the checks and the `auto` fixes, but do not start `interactive` fixes: record them as `needs_user` with their `! <fix>` line, and still write the results file.

## Common mistakes

| Mistake | Fix |
|---|---|
| Asking before running a fix | The user asked for fixes to run on their own. Run it; they approve the permission prompt |
| Running the same SSO login once per profile | One login covers every profile in its `covers` list |
| Printing a token or secret while checking it | Check by exit code or HTTP status only, never echo the value |
| Skipping the results file when something still needs the user | Always write it; the new-day hook keeps nudging until today's file exists |
