---
name: multi-codex-orchestration
description: Use when the user explicitly wants multiple Codex agents or a virtual team, the work can be decomposed into safe parallel roles, and tgtool should coordinate a Ruflo-backed orchestration path.
---

# Multi-Codex Orchestration

## Overview

Use this skill when a task should be executed by multiple Codex agents under a single routed session.

This skill does not replace `tgtool`. It provides the Ruflo-backed orchestration method that `tgtool` can route into.

Default backend:
- `ruflo`

## When to Use

Use when all of these are true:
- the user explicitly wants multiple Codex agents, a virtual team, or parallel agent execution
- the task can be decomposed into 2+ relatively independent roles
- safe ownership boundaries can be defined
- sequential single-agent execution would be materially worse

Prefer a token-aware role set:
- start with only `operator` as the active role
- keep `critic` dormant until a failure, stage transition, or explicit review/feedback demand appears
- do not send the same long context to multiple workers unless the output is genuinely different

Typical role set:
- `operator`
- `critic`
- optional extra specialist only when the task truly needs one

## Do Not Use

Do not use when any of these are true:
- the task is tiny or obviously faster in one session
- write ownership would overlap in unsafe ways
- the work is pure read-only diagnosis without real parallel value
- strict read-only mode leaves no meaningful orchestration path
- the task is so coupled that role splitting would be artificial

## Ruflo Backend

Helper assets included in this skill:
- `scripts/ensure_ruflo_init.py` to detect or initialize `ruflo` Codex/runtime state
- `scripts/bootstrap_ruflo_backend.py` to automatically chain init and swarm bootstrap for `ruflo`
- `scripts/probe_ruflo_execution.py` to shell-check that `ruflo` can create a swarm, spawn an agent, create a task, and assign it
- `scripts/launch_explicit_tmux.py` to launch visible `2 pane` orchestration (`operator + critic`) and auto-try foreground popup

## Supporting References

For implementation details, also see:
- `docs/ruflo-init-playbook.md`
- `docs/ruflo-runtime-bootstrap-playbook.md`
- `docs/ruflo-execution-playbook.md`
- `scripts/ensure_ruflo_init.py`
- `scripts/bootstrap_ruflo_backend.py`
- `scripts/probe_ruflo_execution.py`
- `scripts/launch_explicit_tmux.py`

## Process

### 1. Confirm orchestration eligibility

Before spawning any role, confirm:
- the task really benefits from parallel work
- the role split is meaningful
- write scopes can be kept disjoint
- the selected mode and safety boundaries still allow orchestration

If not, fall back instead of forcing orchestration.

### 2. Choose the smallest safe role set

Use the smallest role set that can safely move the task forward.

Conservative default:
- one active `operator`
- one dormant `critic`
- add an extra specialist only when discovery or review cannot be covered by that pair

### 3. Define ownership explicitly

For each role, state:
- what it owns
- what it must not edit
- what output it must return

Reject orchestration if ownership cannot be made clear enough.

### 4. Bootstrap the selected backend automatically

When the user explicitly wants a `ruflo` backend or asks to initialize orchestration runtime state:
- run `scripts/bootstrap_ruflo_backend.py` first
- let it ensure Codex integration if missing
- let it ensure runtime state if missing
- let it initialize a swarm through `ruflo swarm init --v3-mode`
- keep daemon startup optional instead of making it part of the default chain
- after bootstrap, prefer the current session's `claude_flow` orchestration tools for actual execution:
  - initialize the working swarm
  - start with only `operator` as the default active role
  - let `operator` own concrete execution
  - keep `critic` passive by default
  - wake `critic` only on failure, stage transition, or explicit review/feedback demand
  - spawn additional roles only when the task actually needs them
  - create tasks
  - assign tasks
  - monitor swarm/task/agent status
- treat raw `ruflo` CLI execution as a bootstrap and shell-side probe layer; do not rely on `ruflo swarm start` alone to mean real work is already being driven inside the current Codex session
- use `scripts/probe_ruflo_execution.py` when you need a local shell sanity check that the `ruflo` CLI path can at least create the basic swarm/agent/task primitives cleanly

### 5. Execute through the Ruflo backend when explicitly selected

If the user explicitly selects `ruflo`:
- bootstrap runtime state first
- then execute the live orchestration through the current session's `claude_flow` tools instead of stopping at CLI initialization
- prefer this minimal execution chain:
  - initialize swarm
  - spawn only `operator` by default
  - keep `critic` dormant until failure, phase change, or explicit review/feedback demand
  - let `operator` execute and let `critic` act as an on-demand planning/verification/feedback role
  - wake extra roles only if a real branch appears that cannot be covered by that policy
  - create tracked tasks
  - assign tasks to those agents
  - poll task/agent/swarm status until the main session can summarize progress
- only use the shell probe script to validate the local CLI boundary, not as the main long-running worker path

### 6. Normalize results

Collect per-role outputs into a stable result shape:
- orchestration session id
- backend used
- roles spawned
- per-role status
- blockers
- merged summary
- fallback recommendation if needed

Return the merged result back into the active `tgtool` session.

### 7. Visible tmux mode (explicit execution)

When the user asks for explicit execution:
- default to `2 pane` only:
  - `operator` pane: active execution
  - `critic` pane: dormant by default, wake on failure/stage switch/review demand
- do not create `verifier/reviewer` panes unless explicitly requested
- run:
  - `python3 scripts/launch_explicit_tmux.py --session tgtool-visible --cwd <project-dir>`
- treat explicit mode as:
  - auto-try foreground popup in a terminal emulator
  - if popup is not possible (no GUI/display), report fallback `tmux attach -t <session>`

## Fallback Order

If orchestration should not continue, fall back in this order:
1. `subagent-driven-development`
2. `dispatching-parallel-agents`
3. ordinary `using-superpowers` routing
4. single-session execution

## Common Mistakes

- Spawning too many roles before ownership is clear
- Using two writing roles on the same files
- Treating `reviewer` as a hidden second implementer
- Forcing orchestration when the task is too small
- Treating the external framework as the top-level router instead of `tgtool`

## Remember

- `tgtool` stays the entrypoint
- explicit `ruflo` backend requests may first run `scripts/bootstrap_ruflo_backend.py` to initialize Codex/runtime state and a swarm automatically
- prefer fewer roles over unsafe parallelism
