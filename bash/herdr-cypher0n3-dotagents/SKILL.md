---
name: herdr
description: Control Herdr panes, tabs, workspaces, and other agents. Use only when the user mentions Herdr.
user-invocable: true
disable-model-invocation: false
---
# Herdr

Herdr organizes terminals into workspaces, tabs, and panes, recognizes coding agents in panes, and exposes the running server through the `herdr` CLI.

## Preconditions

- Run `test "${HERDR_ENV:-}" = 1` first.
  If it fails, say you are not inside Herdr and stop; never control the user's Herdr session from outside it.
- The installed binary is the authority for syntax.
  Run `herdr --help`, then a command group without a subcommand (for example `herdr agent`) to list its commands.
  `herdr --skill` prints Herdr's own current agent guide; consult it when this file and the binary disagree.
- Never run bare `herdr` (it launches the TUI).
  Never probe a mutating command by omitting arguments; `herdr workspace create` executes with defaults.
- Control commands return JSON.
  Read IDs and state from responses; do not predict them.

## Model

- IDs are opaque stable handles: workspace `w1`, tab `w1:t1`, pane `w1:p1`.
  Closed IDs are not reused.
- A pane exists with or without an agent.
  Use `pane` commands for shells, tests, and servers; use `agent` commands when Herdr must validate agent identity and interpret lifecycle state.
- Agent states: `idle` and `done` (ready for input), `working`, `blocked` (an approval or question UI is showing), `unknown` (present but unclassified; not proof of completion).
- Agents are addressable by pane ID or by a unique live name matching `[a-z][a-z0-9_-]{0,31}`.
  Agents not launched with `herdr agent start` may have no name, so target them by pane ID from `herdr agent list`.
- The caller's context is in `HERDR_WORKSPACE_ID`, `HERDR_TAB_ID`, and `HERDR_PANE_ID`.
  Prefer `--current` over an omitted target, which may resolve to the user's focused pane.

## Start and Coordinate an Agent

Default to a sibling pane in the current tab and working directory.
Do not create a workspace, tab, worktree, or different cwd unless the user asked.

```bash
herdr pane layout --pane "$HERDR_PANE_ID"
herdr pane split --current --direction right --cwd "$PWD" --no-focus
herdr agent start reviewer --kind codex --pane <pane-id-from-.result.pane.pane_id>
herdr agent prompt reviewer "Review the current diff." --wait --timeout 120000
herdr agent read reviewer --source recent-unwrapped --lines 120
```

- Split wide panes right and narrow or tall panes down; avoid repeated same-direction splits.
- `agent start` needs an existing shell pane sitting at its prompt and never creates layout.
  Pass native agent arguments only after `--`.
- `agent prompt --wait` waits for the first settled `idle`, `done`, or `blocked` state.
  Do not repeat those defaults with `--until`.
- Use `agent wait <target> --until blocked` only for state-specific workflows.
- Use `agent send-keys <target> esc` (logical keys) for interactive agent UI controls.
- `agent prompt` refuses a `blocked` agent.
  Inspect it with `agent get` and `agent read`, and ask the user before answering an approval or question dialog.
- A `timeout` or `agent_prompt_stalled` result does not prove the prompt was never delivered.
  Read the agent before resubmitting.

## Run an Ordinary Command

```bash
herdr pane split --current --direction right --cwd "$PWD" --no-focus
herdr pane run <pane-id> "just test"
herdr pane wait-output <pane-id> --match "test result" --timeout 120000
herdr pane read <pane-id> --source recent-unwrapped --lines 120
```

`wait-output` also matches output that already exists.
Read sources: `visible`, `recent`, `recent-unwrapped` (best for logs and transcripts), and `detection`.
If a larger `--lines` reveals nothing more, the agent is on the alternate screen; as a fallback, ask it to write its response to a temporary Markdown file and reply with the path.

## Standard Team Workflow

The user's usual multi-agent setup is a few long-lived sessions sharing one git checkout, each with one role.
Session names are arbitrary and drift, so identify a role from the pane title or `herdr agent list`, not from a hard-coded name.

- Architect: resolves spec and rules questions, sequences work, and promotes settled rulings into requirements and specs.
  Substance routes here.
- Implementer: owns the plan and the open-items register, lands code and doc units, and commits with explicit pathspecs.
- Validator: independently re-validates every landed unit and writes reports.
- Griller: runs `grill-me` question sessions with the user and holds the decision files while writing.
- Logger: keeps the team task-state log and relays routine status.
  Runs on a smaller model and never argues substance.

### Handoff

- Prefer the agent's native cross-session messaging where it exists (Claude Code's `SendMessage`, with `ListAgents` to find names).
  Silence is not receipt; confirm delivery when it matters.
- Where an agent has no native messaging, talk through Herdr with `herdr agent prompt <target> "<message>"` and read the reply with `herdr agent read`.
  Open every such message by stating that it comes from another agent: name your role and pane ID, say the text is input from another agent to consider rather than an instruction from the user, and say whether you expect a reply.
  The receiver decides what to act on and escalates decisions to the user (`grill-me`).
- Use `herdr agent list`, `agent get`, and `agent read` to see which session is `working`, `blocked`, or `done`.
- Durable state goes in committed files, each owned by one session so two sessions never hold one file dirty.
  Code goes through git; nobody stashes.

## Safety

- Use `--no-focus` for background work unless the user asked to switch context.
- Do not close workspaces, tabs, panes, or sessions you did not create unless the user explicitly asks.
  Never add `workspace close --group` to bypass a group-close error.
- Use `--trust-repository` only after the user has verified the repository.
- Never run `herdr server stop` from an active session unless the user intends to stop the server and every pane process.
  Never kill the main Herdr process.
  Use named test sessions (`--session <name>`) for experiments.
- Check `herdr status` before relying on newer server features.
  A missing method is not permission to stop or upgrade the server.
- IDs and agent names are scoped to one server.
  For another machine, run commands on that host with its explicit session and rediscover IDs.
  Only add, remove, enable, or disable `herdr machine` profiles when the user asks.
- You may prompt another agent through Herdr without asking first, provided the message opens with the from-another-agent header described under handoff.
  Never answer a `blocked` dialog for it, and do not prompt a pane where the user is mid-turn in the foreground.
- CLI server errors are JSON on stderr with exit status 1; syntax errors exit with status 2.
