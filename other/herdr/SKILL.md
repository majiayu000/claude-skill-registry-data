---
name: herdr
description: "Control Herdr, a terminal multiplexer for coding agents. Use only when the user explicitly mentions Herdr or asks to use Herdr to inspect or control panes, tabs, workspaces, commands, or another agent. Do not use merely because a task could benefit from a background terminal, delegation, or parallel work. Requires HERDR_ENV=1."
---

# Herdr

<!-- Modified for kirin-pi. -->

Before control, verify `test "${HERDR_ENV:-}" = 1`. If it fails, stop: do
not inspect or control the focused session from outside Herdr. Inside a managed
pane, the CLI addresses its current session; that is not authority over other work.

## Pi integration

Prefer Pi's typed `herdr` tool for actions in its schema. It preserves aliases and
caller context; it is not a complete client. Use the installed CLI for agent
start/prompt/get, worktrees, integrations, notifications, sessions and other missing
features. The installed CLI is the syntax and behavior authority: start with
`herdr --help`, then the relevant group alone (`herdr agent`, `herdr pane`, etc.).
Never run bare `herdr` for discovery—it launches/attaches the TUI—or probe a
mutating nested command by omitting arguments; creation commands have defaults.

## Targets and ownership

- Topology (workspace/tab/pane), raw terminals and recognized agents are distinct.
  Use pane commands for shells/tests/servers; raw terminals are not agents. Agent
  commands validate identity and interpret lifecycle state.
- Use caller context (`HERDR_WORKSPACE_ID`, `HERDR_TAB_ID`, `HERDR_PANE_ID`),
  `--current`, or explicit returned IDs, not another client's UI-focused pane.
  Discover with workspace/tab/pane lists, `pane current --current` and `agent list`.
- IDs are opaque, not sidebar positions. Parse creation JSON: workspace/tab
  creation returns `root_pane`; a split returns `pane`. Closed IDs are not reused.
  A moved pane receives a new workspace-qualified pane ID: use
  `.result.move_result.pane.pane_id` or its live agent name. Only the moved
  process's inherited caller context resolves the old `previous_pane_id`; it is
  not a general target.
- Agent targets are unique live names or their current pane IDs, not terminal IDs
  or bare kind labels. Names match `[a-z][a-z0-9_-]{0,31}` and clear on exit,
  release or replacement; they identify the current occupant, not a durable job.
- Default to a sibling pane in the current tab and current working directory.
  New workspaces, tabs, worktrees or cwd changes need the user's request. Honor
  requested split direction; otherwise inspect `pane layout` and choose right for
  a wide pane, down for a narrow/tall one. Avoid unusable repeated splits. Preserve
  cwd and focus explicitly: `herdr pane split --current --direction right --cwd "$PWD"
  --no-focus` (adjust direction). Keep `--no-focus` unless a focus change is wanted.
- Do not close topology you did not create without explicit authorization. Never
  run `herdr server stop` unless the user explicitly intends to stop that server
  and its pane processes. Never kill the main Herdr process; use named test
  sessions for isolated server experiments.

## Submit and observe

`agent start` needs an existing available shell pane: interactive prompt, shell
in the foreground, no command/editor/agent occupying it. It never creates or
moves layout. Use the requested kind, a valid unique name and returned pane ID;
native agent arguments follow `--`. Start waits for detected identity/readiness
(default 30 seconds), not task completion.

Use `herdr agent prompt <name-or-pane> "…" --wait --timeout <ms>` for normal agent work.
It submits text and Enter atomically using live bracketed-paste mode, then waits
for settled `idle`, `done` or `blocked`. Standalone `agent wait` has the same state
defaults; use `--until` only for a state-specific need. From a non-working state,
no observed lifecycle change within five seconds yields `agent_prompt_stalled`.
If already working, the active turn may satisfy the wait: it is not per-prompt
completion proof. On failure or `blocked`, inspect `agent get` and `agent read`
before sending more input. Use `agent send-keys` for UI keys (such as `esc` or
`ctrl+c`); all keys are validated before any bytes are written.

For ordinary commands, `pane run <pane> "…"` atomically submits text and Enter.
Submission is not completion. Use `pane wait-output <pane> --match <text>` or
`--regex <Rust-pattern>` with an explicit timeout, then read the result. An existing
snapshot can match immediately; use fresh task-specific evidence, not a stale
success marker. Omitting the timeout allows an indefinite wait.

- `idle`: ready and seen in the focused UI. `done`: the same idle state after unseen
  background work. Focusing marks it seen; CLI reads do not. `blocked`: recognized
  approval/question UI. `unknown`: an agent is present but unclassified, not done.
- Typed-tool aliases and explicit IDs work across workspaces without focus changes.
  A transport error is not proof an alias is stale; inspect/retry that target,
  never substitute the focused pane. `wait_agent` requires recognized agents in
  every target and retains aggregate `all` / `any` semantics. Immediate idle/done
  proves neither new work's start nor completion; use native prompt/wait or fresh
  output. Canceling or timing out a wait does not stop the underlying work.

## Evidence and limits

Prefer `recent-unwrapped` for logs/transcripts; `recent` retains soft wraps,
`visible` is the viewport, and CLI `detection` is the bottom-buffer agent-detection
snapshot. Use `--format ansi` for styling evidence, or `--raw` on pane reads/output
waits; otherwise use text. CLI server errors are JSON on stderr with exit 1;
syntax errors exit 2. A failed request is not proof a target disappeared.

More `--lines` can reveal only available screen/host scrollback. Rows lost from the
alternate screen cannot be recovered that way. For complete output, request an
artifact only within write authority (including its path), then read it directly;
otherwise report the evidence gap or ask permission. Reading, waiting or reviewing
does not grant probe-file or cleanup authority.
