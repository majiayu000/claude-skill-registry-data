---
name: codex-agent
description: Run Codex CLI as an independent coding worker for implementation, investigation, planning, or review, then monitor and verify its result. Use when asked to delegate work through `codex exec`, capture a Codex session ID for follow-up work, or resume, continue, consult, or "adopt" a prior Codex session or thread ID.
---

# Codex Agent

Run `codex exec` from the intended workspace, give it a bounded outcome, monitor
it at the task's time scale, and preserve its session ID when follow-up work is
likely.

Read `/cross-provider-agent` first and apply its doctrine to the whole
dispatch; this skill is only the Codex transport.

Treat installed help as authoritative because Codex CLI evolves:

```bash
codex --version
codex exec --help
codex exec resume --help
codex login status
```

If authentication is missing, ask the user to run `codex login`. Never display,
copy, or embed authentication files or tokens.

## agent permissions

Use the least authority that completes the task. Never add
`--dangerously-bypass-approvals-and-sandbox`, `danger-full-access`,
`--ignore-rules`, or `--dangerously-bypass-hook-trust` merely to make a run
unattended.

## Start a worker

Resolve the intended working directory and whether the task may edit files.
Default analysis, planning, and review to a read-only sandbox:

```bash
codex exec --json --sandbox read-only -C /absolute/path/to/repo \
  "[message]"
```

Use `--sandbox workspace-write`  when the user's task authorizes implementation.

Use `--output-last-message` when a separate final-result file is useful;
keep result files and JSONL logs in a temporary location unless the user asks to
retain them because they may contain prompts, paths, or file content.

## Capture the session ID

Use `--json` whenever later continuation or structured monitoring matters. The
initial event has this form:

```json
{"type":"thread.started","thread_id":"SESSION_ID"}
```

Record that exact `thread_id` as soon as it appears so an interrupted run can
still be resumed.

## Resume or adopt a worker

Resume a specific session sequentially from the intended checkout:

```bash
codex exec --json --sandbox read-only -C /absolute/path/to/repo \
  resume SESSION_ID \
  "[message]"
```
Put global `codex exec` options before `resume`.

## Monitor and collect

With `--json`, require a successful process exit and a terminal
`turn.completed` event. Treat `turn.failed`, `error`, a nonzero exit, or a
mismatched thread ID as failure. The final `item.completed` whose item type is
`agent_message` contains the worker's result.

## Profiled dispatch
`codex exec` hardcodes never-ask approvals: a sandboxed command that needs
network fails (on Linux, a bubblewrap loopback error) with no runtime
escalation path. Pre-authorize the specific commands with execpolicy rules 
 instead of widening the sandbox

Use the transactional runner with scoped profiles : `/absolute/path/to/codex-agent/scripts/run-profiled.sh`

The transactional runner assembles a throwaway home from the profile installed
skills symlinked so the child can invoke cited skills — runs one session as
the profiled agent, and deletes the home afterwards:

```bash
/absolute/path/to/codex-agent/scripts/run-profiled.sh \
  --workspace /absolute/path/to/workspace \
  [--effort [effort level]] \
  --profile github-pr-reviewer \
  -- --json "REVIEW_TASK"
```

The root session is the profiled agent — no bootstrap relay — and native
children it spawns inherit the same sandbox and rules. Nothing touches the
workspace, so parallel Codex dispatches need no lock.

Known gap (0.146.0, live-verified): native file tools bypass the read-only
sandbox, so file-write denial is detect-and-reject — verify the pinned head
and a clean tree after dispatch and discard the child's output otherwise
The runner refuses a workspace containing `.codex/`: its rules load into the child's policy with
no trust gate.

Verify a rule offline before relying on it:

```bash
codex execpolicy check \
  --rules /absolute/path/to/codex-agent/profiles/github-pr-reviewer/rules/github-pr-reviewer.rules \
  -- gh pr comment 1 --body test
```

Rules are experimental. Keep only narrow `allow` prefixes and never add a
fallback rule: most-restrictive-wins would turn a broad `prompt` decision
into a blocker under exec's never-ask approvals. A failed rule match fails
closed — the command stays sandboxed with no network escape.

### available profiles
**github-pr-reviewer** : `profiles/github-pr-reviewer/` encodes the profile from
`/cross-provider-agent` as a complete `CODEX_HOME` layer: `config.toml`
(read-only sandbox + role instructions) plus a `rules/` directory whose
execpolicy allows exactly the profile's `gh` surface to run outside the
sandbox; local reads need no rules because they run inside it.
