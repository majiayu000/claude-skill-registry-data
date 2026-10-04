---
name: repoprompt-agent-run-sandbox-approval
description: |
  Fix for `mcp__RepoPrompt__agent_run` subagents (Codex CLI) silently pausing with
  "Waiting For Input" when asked to write files outside the loaded RepoPrompt
  workspace roots. Use when: (1) you spawned an agent_run session and `op=poll`
  reports it as `Waiting For Input` with an `Approval` interaction, (2) the prompt
  asked the subagent to write to a path under `~/.claude/`, `~/.codex/`, `/tmp/`,
  or any other path not inside the loaded RepoPrompt roots, (3) the subagent's
  preview text mentions "outside the workspace sandbox" or "outside loaded roots".
  Covers the agent_run respond protocol (interaction_id, decisions) that isn't
  surfaced in the tool description, and the choice between `accept` (one-shot)
  vs `accept_for_session` (batch — preferred when the agent needs multiple writes).
author: Claude Code
version: 1.0.0
date: 2026-05-02
---

# RepoPrompt agent_run sandbox approval

## Problem

When you spawn a sub-agent with `mcp__RepoPrompt__agent_run op=start`, the
subagent (Codex CLI) runs in a sandbox bound to RepoPrompt's loaded workspace
roots. If your prompt instructs the subagent to write files to paths outside
those roots, the subagent will not refuse — it will pause and ask the *parent*
(you) for explicit approval.

The pause shows up as a `Waiting For Input` state when you `op=poll` the
session. The agent_run tool description doesn't document the response protocol,
so it's easy to think the agent has hung or crashed and reach for `op=cancel`.
It hasn't crashed — it's blocked on you.

## Trigger conditions

All of the following together:

1. You're using `mcp__RepoPrompt__agent_run op=start` (or `wait`/`poll`).
2. The agent is a Codex CLI agent (the default for `engineer`/`pair`/`design` role labels).
3. Your prompt asked the subagent to write/create/modify a file at a path that
   is NOT under any of RepoPrompt's currently loaded workspace roots. Common
   examples: `~/.claude/skills/...`, `~/.codex/...`, `/tmp/...`, any absolute
   path outside the project the user has open.
4. `op=poll` returns `Status: Waiting For Input` with `Interaction: Approval`
   and an `Interaction ID`.

You can confirm by reading the `Prompt` field in the poll response — it
typically reads something like *"Do you want to allow writing the requested
answer.md file to the .claude skills workspace path outside the project
sandbox?"*

## Solution

Respond to the interaction with `op=respond`, passing the `session_id`,
`interaction_id`, and one of the `accept*` decisions:

```
mcp__RepoPrompt__agent_run
  op=respond
  session_id=<from start/poll>
  interaction_id=<from poll output>
  response="accept_for_session"
```

Decision choices:

| Response | When to use |
|---|---|
| `accept` | One-shot approval. The agent will pause again on the next out-of-sandbox write. Use when you only expect one write. |
| `accept_for_session` | Batch approval for the rest of this session. **Prefer this** when the agent needs to write multiple files (e.g. a skill that does `read input → write output → write log`). Saves round-trips. |
| `decline` | Reject the write. The agent will adapt or fail. |
| `cancel` | Kill the session entirely. Only use if you actually want to abort. |

If you have multiple paused sessions in a batch (common when you spawn N
parallel agents and they all hit the sandbox), respond to each one in turn —
they each have their own `interaction_id`. You can do this efficiently by
making the `op=poll` calls in parallel, then the `op=respond` calls in parallel.

## Verification

After `op=respond`, the session status flips back to `Running`. Confirm with
another `op=poll` — you should see the agent's `Preview` text move past the
write and start producing output. Subsequent `op=wait` will then return
`Completed` once the agent finishes.

## Why this happens (and why not all sessions pause)

The Codex CLI sandbox is conservative by default about writes outside the
workspace it was given. RepoPrompt passes its loaded roots as the allowed
write surface. Anything outside that surface triggers an interaction request.

Empirically, not every parallel session in a batch will pause even with
identical prompts — some find an unsandboxed code path (e.g. running `cat >
file` via shell) and others go through the sandboxed file-write tool. Don't
treat the absence of a pause as a sign that the prompt is wrong; just be
ready to respond to whichever ones do pause.

## Example

You launch 8 sub-agents in parallel via `agent_run op=start`, each writing to
`~/.claude/skills/foo-workspace/iteration-1/eval-N/.../answer.md`. After
`op=wait` returns the first completion, you `op=poll` all 8 and see:

```
- Sessions polled: 8
- Interesting: 4
- Running: 4
- Terminal: 1
- session-A — Completed
- session-B — Waiting For Input
- session-C — Waiting For Input
- session-D — Waiting For Input
- session-E — Running
- session-F — Running
- session-G — Running
- session-H — Running
```

For each `Waiting For Input` session, `op=poll session_id=...` returns the
`Interaction ID`. Respond with `accept_for_session` to all three (in
parallel), then `op=wait` on the remaining sessions until they all complete.

## Notes

- This is specific to RepoPrompt's `agent_run` calling Codex CLI. Other agent
  backends may have different sandbox behavior.
- The `Preview` text the paused agent shows is human-readable and useful for
  debugging — read it before responding so you understand what the agent is
  about to do.
- If you anticipate the writes ahead of time, you can sometimes avoid the
  pause entirely by having the parent (you) create directories/files before
  spawning the agent, and only ask the subagent to populate content that
  already has a writable home. But for ad-hoc workflows like skill-creator
  evals, just plan to handle the approval round-trip.

## See also

- `repoprompt-agent-run-mcp-not-inherited` — sibling gotcha about a
  different `agent_run` failure mode: non-RepoPrompt MCPs (seo-utils,
  open-brain, etc.) are NOT inherited by spawned sub-agent sessions.
- `skill-creator-aggregate-benchmark-layout` — sibling gotcha about the
  workspace layout `aggregate_benchmark.py` expects (`run-N/grading.json`,
  not `grading.json` at the config dir root).

