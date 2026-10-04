---
name: master-session
description: Use when one Claude Code session must supervise several others on this machine — adopting sessions the user started by hand, or spawning workers itself. Covers roster, status requests, a GO board, idle notices, and the GO-token protocol. Works with AOS alone; the AO daemon is optional.
category: bdb-core
risk: safe
tools:
- claude-code
---

# `/master-session` — Supervise Other Sessions

One session is the **master**: it keeps the overview, asks workers for status, and relays the human's decisions. It never does the workers' jobs and never decides for the human. Needs Claude Code with cross-session messaging (`ListAgents`, `SendMessage`). Nothing here requires the AO daemon.

## Modes

- **Adopt** — supervise sessions the human already started by hand. `ListAgents` is the source of truth; message them with `SendMessage`.
- **Spawn** — start the workers yourself. AO is optional; without it:
  - Claude: `claude --bg --name <name> --permission-mode auto "<prompt>"`, or over ACP as below.
  - Codex / OpenCode / Claude over ACP: `aos-acp <codex|opencode|claude> --name <name> --cwd <worktree> --prompt "<task>" --go-wait 600 &` (one process per worker; run it in the background and read its log). Details: `docs/master-session-acp.md`.
  - agy: no sanctioned ACP adapter (`antigravity-acp` breaches Google's Antigravity terms). Adopt agy sessions or delegate via the `mcsc` skill.
  - If AO is installed, `ao-orchestrator` may run the same workers; it adds nothing the token protocol needs.

### Routing: which channel for which job

| Job | Channel |
|---|---|
| One-shot task for another harness | `mcsc` (one level deep, `delegate_agy` is read-only) |
| A worker that may need a GO | `aos-acp` |
| A message to a running OpenCode session | `aos-bus` |
| A durable fleet across repos | AO (optional; AOS must work without it) |

Details and limits (`opencode run --auto` auto-approves tool calls, a GO is never inherited): `docs/delegation-routing.md`.

### `aos-acp` in one paragraph

`bin/aos-acp.mjs` is a zero-dependency ACP client: it spawns the adapter (`npx -y @agentclientprotocol/codex-acp`, `opencode acp`, `npx -y @agentclientprotocol/claude-agent-acp`), runs `initialize` → `session/new` → `session/prompt`, streams the worker's text to stdout and logs every event to `~/.aos/acp/<name>.jsonl`. A `session/request_permission` for a guarded command (the go-gate list) is answered `allow_once` only with a valid GO token for `<name>`; with `--go-wait <sec>` the request is parked (log event `permission_pending`, show it as `GO needed`) until the token appears or the wait ends. Everything else follows `--allow-default deny|allow` (deny by default). `--model <id>` is sent as ACP `session/set_config_option` (`configId: "model"`, id is adapter-specific, e.g. `sonnet`, `provider/model`); `fable` ids are rejected (workers run opus, sonnet or haiku), default is the adapter default and is logged. ACP workers are not in `ListAgents`: the roster lists them from the logs.

## Step 1 — Roster

Call `ListAgents`, keep local Claude sessions, drop yourself. Write one line per session: name, repo/branch if known, kind (adopted/spawned). Show it to the human and confirm which sessions are in scope before messaging any.

## Step 2 — Status request

Send one message per session, never a broadcast. Template:

```status-request
Status request from the master session (reply in at most 10 lines):
1. Task, repo and branch.
2. Progress: done / in progress / not started.
3. Blockers.
4. Actions waiting on a GO (commands you were blocked from running).
5. Running subagents.
```

## Step 3 — GO board

Collate replies into one block per session and show it to the human:

```
[<session>] <task> — <repo>@<branch>
  progress : <one line>
  blockers : <none | list>
  GO needed: <exact command(s), or none>
  subagents: <n running | none>
```

The human answers per session. Items under `GO needed` are the human's to decide; list them verbatim, never summarised into something softer.

## Idle notices

- Subscribe (`SendMessage` with `notify_when_idle`) only **after** you sent that session work.
- Never re-subscribe to a session already idle; never poll; never send "are you done?".
- Waiting is silent. React when a notice arrives or the human speaks.

## Boundaries

- The master never grants GO. A relayed message is not the user's approval for the worker, and the worker's go-gate treats it as such.
- The master never executes an action another session was denied — no re-running it from here, no "just this once".
- Forward the human's words verbatim and mark them: `[forwarded by master, user said:] "<exact text>"`. No paraphrase, no added urgency.
- A subagent or worker does not inherit anyone's GO. A blocked command is not retried without a fresh one.

## GO-token protocol

The one sanctioned way for the human to release a gated action in a worker without switching windows:

1. In the **master** session the human types exactly `GO <session-name>` (case-insensitive; the name as shown by `ListAgents`).
2. The `UserPromptSubmit` hook `go-token.mjs` writes `~/.aos/go/<session-name>.token` (JSON: `target`, `issued_at`, `master_transcript`, `master_session`). Nothing else happens.
3. The worker retries the blocked command. `go-gate.mjs` opens only if the token names this session, is younger than 10 minutes, and the master transcript still ends with that very `GO <session-name>` as its last human message. The token is deleted on use: single use, no replay.

Consequences: any further human message in the master before the worker retries cancels the token; a literal `GO` typed in the worker still works as before; a chat message that merely *says* "GO" never counts. The worker's own name comes from its transcript (`--name`); if absent, set env `AOS_SESSION_NAME` (`aos-acp` sets it for its worker). The same token is honoured by the OpenCode plugin's gate (`.opencode/plugins/bdb-aos.js`, name from `AOS_SESSION_NAME` or the session title) and by go-gate under agy (`AOS_SESSION_NAME` only). Who consumes it: the worker's own gate when it has one (Claude hook, OpenCode plugin — `aos-acp` then only verifies), `aos-acp` itself for codex, which has none. Limit: the token proves the human typed it in the master transcript, not who wrote the token file — a hostile local process can forge both, so this is a guard against mistakes, not against local malware.

## Starting workers: lessons

- A background worker stalls on its first permission prompt unless started with `--permission-mode auto`. Always pass it.
- `--disallowedTools` is variadic and swallows a trailing prompt. Put the prompt before it, or end the flag list with `--`, and check the worker actually received the task.
- Name every worker (`--name`) so the token and `ListAgents` agree.

## Handover file

At session end write `docs/sessions/master-<date>.md` (or `$HOME/.aos/handover/` outside a repo): roster, last GO board, open GO items, what is waiting on whom, and the next command. A fresh master reads it first.
