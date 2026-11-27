---
name: playbook
description: Model-discipline playbook - use when setting up a repo for Claude Code agents, choosing which model to dispatch a subagent on, working a long session on an expensive model, doing browser or UI verification, or running tool-heavy loops (serial test runs, migration batches, CI polling).
---

# Model discipline playbook

The goal is simple: expensive models do judgment, cheap models do everything else, and nothing expensive runs by accident.

## Dispatch ladder

Every `Agent` dispatch passes an explicit `model`, unless the agent definition pins one.

| Work | Model | Examples |
|---|---|---|
| Mechanical | `sonnet` | renames, import fixes, test repairs, doc edits, batch find-and-replace, running a suite and reporting failures |
| Real thinking | `opus` | feature implementation, codebase exploration, planning, verification, code review, debugging |
| Orchestration and judgment | the top session model | deciding what to build, triaging findings, reviewing what the subagents returned |

The main loop is the expensive seat. Keep it thinking and delegating; push the doing down the ladder.

## Top-model subagent amendment

Dispatching a subagent on the top model is allowed for genuine judgment calls: security triage, adversarial verification, an architecture review where a cheaper model would miss the point. Budget is the constraint, not a ban. What is not allowed is reaching the top model by leaving `model` off and inheriting it silently.

## Pins: upgrading is safe, downgrading is not

An agent definition that pins a model in its frontmatter is authoritative. Omit `model` when dispatching it - an explicit argument overrides the pin.

- Upgrading a pinned agent for one dispatch (sonnet pin, `model: "opus"` for a hard case) is safe.
- Downgrading is not. A pin exists because the author decided the agent needs that tier; dropping it below the pin quietly degrades the agent's output.

## Fork caveat

`subagent_type: "fork"` always runs on the parent model and ignores any `model` you pass. Do not pass one; it would teach a rule that is not real.

## Session rules, and why

Every main-loop turn re-reads the whole cached context and emits output at the session model's rate. Anything that bloats the main loop costs more on every turn after it, not just once.

- **Tool-heavy loops run in subagents.** Serial test runs, migration batches, CI polling: dispatch a background sonnet agent so the tool output never lands in the main context.
- **Browser and UI verification runs in a subagent or a skill**, never the main loop. Page snapshots and console dumps are large and rarely needed twice.
- **Prefer `/clear` plus a written handoff over repeated `/compact`.** Compaction keeps a lossy summary of everything; a handoff you wrote keeps the part that matters.
- **Truncate or redirect large command output** (`| tail -50`, `> /tmp/out.txt`) and read back only the part you need.
- **Start mostly-mechanical sessions on a cheaper model.** PR babysitting, polling loops, doc passes: `claude --model opus` or `/model` before you begin.

An audit of a month of sessions found roughly 60% of dispatches omitted `model` before the hook was in place, and none after.

## Project setup pattern

When you set up a repo for Claude Code agents:

1. **Pin a model in every project agent's frontmatter.** A `test-writer` agent pins `model: sonnet`; a `security-auditor` agent pins `model: opus`. With a pin in place, callers omit `model` and the guard stays quiet.
2. **Skills that dispatch subagents name the model inline** in the skill body, so the instruction travels with the skill.
3. **Browser walks live in a skill**, so the heavy output happens inside a subagent by construction.
4. **Agents that edit files get their own worktree** (`isolation: "worktree"`), or run one at a time. Parallel agents sharing a checkout will clobber each other. Read-only agents are fine in the shared tree, and pushing a branch by ref does not touch it.
5. **Write the dispatch rule into the repo's `CLAUDE.md`.** Subagents never see SessionStart-injected context, so prose in `CLAUDE.md` is the primary carrier; the hook is a backstop.

## What the hook does and does not police

The guard runs on `PreToolUse` for the `Agent` tool and denies a dispatch only when all of these are true: no `model` argument, the session model matches the expensive prefix, the subagent type is not `fork`, the type is not namespaced, and no agent definition pins a model.

It fails open - exits 0 and allows - on every other path:

- `jq` is not installed
- stdin cannot be read, or a `jq` field extraction fails
- `transcript_path` is missing or the transcript is not readable
- no assistant entry appears in the last 200 lines of the transcript (a very long tool run can still push it out of view)
- the session model does not start with the expensive prefix
- the subagent type is namespaced (contains `:`, i.e. supplied by a plugin) and cannot be resolved by path
- an agent definition at `<project>/.claude/agents/<type>.md` or `~/.claude/agents/<type>.md` has a `model:` line

Set `CLAUDE_EXPENSIVE_MODEL_PREFIX` if your top tier is not the default (`claude-fable`) - for example `claude-opus` on a machine where opus is the top model.

The hook cannot set the session model. That is a user-settings value, not something a plugin can control.
