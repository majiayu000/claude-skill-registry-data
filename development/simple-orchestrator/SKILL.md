---
name: simple-orchestrator
description: Multi-agent workflow for planned development. Explores, plans, dispatches workers, reviews, and reports. Use only when the user explicitly asks to run it.
disable-model-invocation: true
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple Orchestrator

You are the main orchestrator. You coordinate subagents and do not implement product code yourself.

Use this for features that span several files or scopes. For a single small change, skip it: implement directly, then run `simple-check`.

## Agents

Spawn these by name. Do not use built-in `explorer`, `worker`, or `default` agents.

| Agent | Role | Access |
|-------|------|--------|
| `simple-explorer` | Map current behavior, constraints, risks, candidate scope | Read-only |
| `simple-worker` | Implement one assigned scope, run its test plan, hand off with evidence | Write |
| `simple-reviewer` | Check test evidence, diff, and scope against the plan, using `simple-check` | Read-only |

The agent files ship in the `agents/` folder next to this skill, and the user must install them. Copy them to `.cursor/agents/` or `.claude/agents/`, or the `.toml` versions in `agents/codex/` to `.codex/agents/`. If they are not installed, tell the user before continuing.

## Workflow

1. Read the docs and code the request needs. Plan only the requested outcome and the files it directly needs. Do not expand to unrelated work.
2. Spawn `simple-explorer` before writing the plan.
3. Present the plan:
   - Outcome and scope
   - Files and steps
   - Test plan, including browser checks on the local dev URL for UI changes
   - Risks and doc updates
   - A worker dispatch table for multiple scopes, one row per worker with files and test-plan slice

   Approval depends on size. A single small scope proceeds without waiting. Multiple workers, cross-module, large, or risky changes wait for user approval, with no code changes before it. If scope grows during work, stop and get approval again.
4. Spawn one `simple-worker` per dispatch row. Do not merge scopes into one worker.
5. When all handoffs are in (diff and test results), spawn one `simple-reviewer` with every handoff and the approved plan. It marks each row done, partial, or missing and flags scope creep.
6. Update progress and affected docs, then report what changed, what remains, and verification status.

## Parallel work

- Workers with disjoint files run in parallel. Workers with overlapping files run one after another.
- Respect the tool's limit on concurrent subagents, assume 4 if unknown. If there are more workers than the limit, run them in batches and collect each batch first.
- Order is explorer, workers, reviewer. Never run the reviewer alongside workers.

## Interrupt and resume

An interrupted subagent is not a finished one. Never skip its work unless the user approves a reduced scope.

- Track each row as not started, in progress, or handed off. Mark handed off only with diff and test evidence.
- On resume, re-read the repo state and do not trust memory. Resume the same subagent if the tool allows it. Otherwise spawn a new `simple-worker` with the finished items (with evidence) and only the remaining items.
- Never mark the plan complete while any row lacks a handoff.

## Review loop

- Valid in-scope finding: the owning `simple-worker` fixes it and re-runs the affected tests, then `simple-reviewer` checks again.
- Suspected behavior bug: run `simple-debug` before changing code.
- Scope expansion: stop and get approval.
- Unresolved blocker: report the evidence and do not loop forever.
- After multi-module work, optionally run `simple-refactor`.

## Verification report

Report these separately: repository checks (build, type check, lint, tests), local runtime, browser checks when UI behavior matters, real user data, and production evidence. Do not claim runtime or data validation from build or type check alone.
