---
name: pb-master
description: >-
  Run one control session over several Claude Code, Codex or OpenCode
  sessions: roster, status board, GO board, GO <session> tokens, idle
  notices and a handover file. Use for "master session", "supervise my
  sessions", "run several agents", "one control window".
category: bdb-core
kind: playbook
trigger: ["master session", "supervise my sessions", "run several agents"]
inputs: ["plan?", "workers?"]
requires:
  skills: [master-session, agenttrail, stay-within-limits, "claude (external)", "aos-acp (external)"]
  agents: []
  mcps: []
  store: []
go_points: [spawn workers, "GO <session>"]
outputs: ["docs/sessions/master-<date>.md", "production_artifacts/pb-master-<date>.md"]
verify: "handover lists every roster session with open/closed GO state; no file older than 10 min in ~/.aos/go/ unless listed as stale in the handover"
difficulty: advanced
est_time: 15 min setup, then session-long
---

# One control session over several agents
What you get: a live roster, status board and GO board for your agent sessions, GO tokens relayed per session, and a handover file.
Availability: works in any harness that can run shell: Claude workers need the `claude` CLI; Codex and OpenCode workers via aos-acp; agy is adopt-only; Cursor and Kimi sessions can be adopted but not spawned.

## Inputs
- plan (optional) — a plan file for the trail board, e.g. `production_artifacts/00_execution_plan.md`
- workers (optional) — sessions to spawn (name, cwd or worktree, model, prompt) or to adopt (already running)

## Steps
1. Preflight — `command -v aos-trail`, `command -v claude`, `command -v aos-acp` → run log header — `aos-trail` required (the aos-acp fallback below derives its path from it), else stop with an install hint; `claude` missing → log "claude not on PATH: Claude workers disabled" and continue with aos-acp workers (codex/opencode) and adoption; `aos-acp` missing → log "aos-acp not on PATH" and look for `bin/aos-acp.mjs`: `p="$(dirname "$(node -e 'console.log(require("fs").realpathSync(process.argv[1]))' "$(command -v aos-trail)")")/../../../../bin/aos-acp.mjs"; test -f "$p"`, run it as `node "$p"` in place of `aos-acp`; still missing → no spawnable workers, adopt-only (logged); read `docs/sessions/master-*.md` if one exists (the previous handover)
2. master-session (Roster) — `ListAgents` minus self when that Claude tool exists, else the aos-acp logs `ls -t ~/.aos/acp/*.jsonl` (log event `start` carries `name`, `cwd`, `adapter`; the last line carries `ts` and `event`: `done`/`error` = finished; `timeout` = finishing, cancel follows; anything else = running or parked on `permission_pending`; last `ts` older than 10 min with no terminal event = suspect stale, verify the process before treating it as running) plus any sessions the human names → roster table (name, repo@branch or cwd, adopted or spawned) in the run log — stops for approval (the human confirms scope)
3. agenttrail — plan given → `aos-trail . --plan <plan> --no-open` → board URL in the run log; no plan → `aos-trail . --no-open` (file activity only), logged — URL printed (output says "already running" → log it as "existing map", its plan is unchanged); runs before any worker is spawned, so no spawn line exists in the run log before the board URL line
4. [GO] spawn — worker list (name, cwd or worktree, model, prompt) shown in full, then one line per worker:
   - Claude (skip when claude is missing): `(cd <cwd> && claude --bg --name <n> --permission-mode auto --model <model-id> "<prompt>")` (`claude` has no cwd flag; prompt before any `--disallowedTools`)
   - Codex or OpenCode: `aos-acp <codex|opencode> --name <n> --cwd <worktree> --prompt "<task>" --go-wait 600` in the background, log `~/.aos/acp/<slug(n)>.jsonl` (slug: lowercase, runs of characters outside `a-z0-9._-` become `-`, edge dashes trimmed; a custom `--log` path is not found by the roster)
   - agy: adopt-only (an already running session, no spawn); never `aos-acp agy`, the adapter is third-party and unverified (`bin/aos-acp.mjs` lines 26+)
   - Never `aos-acp claude` (no model flag), never `--model fable`, never omit `--model`
   - The run stops here until the human types GO. The hook does not guard `claude --bg`, so GO is by contract. Check: every spawned name shows in `ListAgents` (if available) or has an ACP log
   - Adopt-only roster → step skipped
5. master-session (Status) — master-session Step 2 template verbatim, reply in at most 10 lines, one `SendMessage` per session where that tool exists; for an aos-acp worker read the tail of its log once (`tail -n 20 ~/.aos/acp/<slug(n)>.jsonl`: last `text`, `permission_pending` command = `GO needed`, `done`/`error`); for a session the master cannot reach, ask the human to read its status → replies in the run log — every in-scope session replied or is marked "no reply"
6. master-session (GO board) — replies → GO board block per session, `GO needed` commands verbatim → board in the run log — no paraphrased command
7. [GO] token relay — the human types `GO <session>` in the master (`go-token.mjs` writes `~/.aos/go/<session>.token`); the master then tells that worker only "retry the blocked command". The run stops here until the human types `GO <session>`. The master never types or forwards a GO itself, and any other human message cancels a pending token — the worker's log shows the command ran
8. Idle rules — `notify_when_idle` (Claude) only after sending a session work; without it, one read of the worker log for `done`/`error`/`timeout` at the point the human asks; no polling loops, no "are you done?" → idle events in the run log; between waves a stay-within-limits check, logged — events logged
9. Handover — roster, last GO board, open GO items, who waits on whom, next command → `docs/sessions/master-<date>.md` (outside a repo: `~/.aos/handover/`) — every roster session listed with its GO state; `ls ~/.aos/go/` has no token older than 10 min unless listed as stale in the handover (report stale ones, do not delete them)

Run log: `production_artifacts/pb-master-<date>.md` in the start directory; the run log and the handover file `docs/sessions/master-<date>.md` are never staged or committed

Rules
- Anything other than the literal GO (case-insensitive; in step 7 `GO <session>`) is not a GO; a GO covers only that one step, one time.
- GO is by contract in every harness. The go-gate hook is only a backstop on Claude Code, OpenCode and agy (Codex: unverified; Cursor, Kimi: none). A missing hook is never permission to proceed.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
