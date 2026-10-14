---
name: cursor-agent
description: Run Cursor Agent CLI as an independent coding agent for implementation, investigation, planning, or review in a local workspace. Use when asked to delegate work to Cursor, automate cursor-agent in headless mode, capture a Cursor session ID, or resume and continue an earlier Cursor chat.
---

# Cursor Agent

Run `cursor-agent` from the intended workspace, give it a concrete outcome, monitor it at the task's time scale, and preserve its session ID whenever follow-up work is likely.

Read `/cross-provider-agent` first and apply its doctrine to the whole dispatch; this skill is only the Cursor transport.

## Check the CLI and authentication

Treat the installed CLI help as authoritative because Cursor Agent is evolving:

```bash
cursor-agent --version
cursor-agent --help
cursor-agent status --format json
```

If authentication is missing, ask the user to run `cursor-agent login`, or use `CURSOR_API_KEY` when the user has already arranged it. Never print or embed an API key in a command.

## agent permissions

Use the least authority suitable for the task:

- Add `--mode plan` for read-only analysis and planning.
- Add `--mode ask` for read-only questions.
- Prefer `--auto-review` for ordinary agent work.
- Add `--force` only when the user authorized changes and unattended command execution is necessary.
- Use `--sandbox enabled` when the task can run within Cursor's sandbox.

## Start a worker

Run from the repository checkout or pass `--workspace /absolute/path`. For a headless task with structured progress:

```bash
cursor-agent -p --output-format stream-json --auto-review --trust \
  "[message]"
```

Drop `-p --output-format stream-json` for an interactive task.

Every `-p` run requires `--trust`, including `--mode plan` and `--mode ask`; without it the run aborts immediately with `Workspace Trust Required`.

`--auto-review` prompts for tool calls its classifier does not deem safe, and in `-p` mode no one can answer, so the run can stall. For genuinely unattended work that must run any command, add `--force` instead.

## Capture the session ID

When the ID must be known even if the first turn is interrupted, allocate it up front with `cursor-agent create-chat` and pass `--resume="$cursor_chat_id"` from the first run onward. 
Otherwise capture `session_id` from the stream's `system`/`init` event or the terminal result object.

## Resume a session

Resume with `--resume="$cursor_chat_id"` from the same workspace used to create the chat — chat discovery is workspace-scoped. Recover an unrecorded ID interactively with `cursor-agent ls` or `cursor-agent resume`.

## Monitor and verify

Poll the NDJSON log often enough to surface approval prompts promptly. On completion require
a clean exit and a successful terminal result event.

A `cursor-agent` or `gh` failure with transport errors naming the URL is the sandbox denying network, not bad credentials; rerun with the environment's required network escalation.

## Profiled dispatch

Cursor takes permission and sandbox policy only from configuration files, so 
profiled dispatch runs through the skill's transactional runner:
`/absolute/path/to/cursor-agent/scripts/run-profiled.sh`

The runner stages the profile for exactly one invocation, supervises the child, and restores the workspace byte-for-byte:

```bash
/absolute/path/to/cursor-agent/scripts/run-profiled.sh \
  --workspace /absolute/path/to/workspace \
  --profile github-pr-reviewer \
  -- -p --output-format stream-json --trust "REVIEW_TASK"
```

Use `stream-json` for unattended runs. A long review with plain `json` prints nothing until the terminal result, so the caller can't tell progress, a tool denial, or a stall apart.

While the child runs, the workspace holds the staged `.cursor/` files and the runner's `.cursor-profile-txn/` lock and journal. That has two separate effects:

- A second Cursor runner on the same workspace hits the lock and exits 75. Give each Cursor dispatch its own workspace.
- Other providers are not locked out, but their clean-tree or diff checks in that workspace see the staged state: `git status --porcelain` lists `.cursor-profile-txn/` and any staged `.cursor/` file the repo doesn't track, such as `.cursor/sandbox.json`, and shows a tracked `.cursor/cli.json` as an edit. Run them in a separate checkout, or before or after the Cursor run.

The staging has to stay in the workspace. Cursor reads the user `sandbox.json` from `~/.cursor/` regardless of `CURSOR_CONFIG_DIR`, and the workspace's own `.cursor/sandbox.json` takes priority over it, so overwriting the workspace copy is the only per-run way to stop a reviewed branch's Cursor config from widening the profile.

Run profiled dispatches with plain `-p --trust` (deny-unless-allowed), so the profile's allowlist is the whole command surface; the runner allowlists child arguments and rejects everything else.

### available profiles
**github-pr-reviewer** : `profiles/github-pr-reviewer/` encodes the profile from
`/cross-provider-agent` with `cli.json` as the canonical permissions object:
multi-word `Shell(...)` allows — live-verified but undocumented — for exactly
the profile's `gh` surface, paired with a `sandbox.json` GitHub-only network
allowlist as defense in depth.
The allowlist covers git only as `git diff`, `git log`, `git show`, and `git status`. `git rev-parse` has no allow entry, so the profile denies it.
