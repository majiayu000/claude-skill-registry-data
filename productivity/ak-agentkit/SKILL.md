---
name: ak-agentkit
description: "Route AgentKit work by classifying the task, chaining installed skills and spawning subagents at trigger points; also operate the ak CLI."
when_to_use: "Invoke at the start of multi-step work, when the right skill is unclear, or when the next action is an ak subcommand."
category: meta
keywords: [routing, dispatch, skills, chaining, subagents, workflow, ak, cli, lifecycle, install, doctor, recover]
argument-hint: "[task to route | ak goal or subcommand]"
metadata:
  author: agentkit
  version: "1.1.0"
---

# AgentKit router

Return one concrete route to an installed owner, then let that owner execute. Reuse the
accepted outcome, constraints, non-goals, acceptance criteria and current evidence.

## Proportionality gate

A named skill goes directly to that skill. A single obvious domain goes directly to its
owner. Pure conversation needs no workflow. For ambiguous or multi-domain work, match the
live installed catalog; never infer a skill or agent from a different kit or remembered roster.

Use `references/task-taxonomy.md` only for unclear classification and
`references/chaining-patterns.md` when more than one owner is actually needed. Select one
primary owner per intent, pass existing artifacts and stop routing. Do not repeat outcome,
inspection, planning or verification gates that the owner already completed on current state.

Risk determines verification: bounded reversible work uses relevant checks and direct review;
cross-module/public-contract/security work needs broader affected checks and independent
review where required. Reuse exact-revision evidence, never scores as proof. Delegate only
when available, authorized, useful and scoped; `references/subagent-timing.md` supplies the
contract. Missing optional agents permits inline work with honest limitations.

Headless cross-runtime work belongs to an installed orchestration capability. Missing owners
fall back to native capabilities; report the gap instead of inventing an invocation. On a
failed route, change approach from evidence and resume useful work. Ask only for a material
missing decision or authorization beyond the current scope. Report outcome and verification.

## Operating the ak CLI

When the next action is an `ak` subcommand, or reading its `--json` output, follow
`references/ak-cli-operation.md`: classify the effect (read-only, mutating, diagnostic),
confirm project versus global scope before any mutation, and prefer `--json --no-interactive`
for scripted reads. `references/command-reference.md` is a generated starting index;
`ak <cmd> --help` and the `--json` envelope stay authoritative.
