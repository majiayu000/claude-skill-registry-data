---
name: investigate
description: Investigates a bug or unexpected behavior from reproduction to root cause with a panel of independent hypothesis agents, then fixes it only when the request asks for a fix. Use when invoked explicitly to debug, diagnose, or fix a reported failure.
---

## Running in Codex

This is the Codex copy of this skill. Read the rest of it with these translations:

- Agents launched in parallel: spawn each one with `spawn_agent` before waiting on any, then collect the
  results with `wait_agent`. Tell every agent you spawn not to spawn agents of its own. If subagents are
  unavailable, run each lane yourself, one after another.
- "Your default model" and "your strongest model": spawn the agent with an `agent_type` whose role file in
  `~/.codex/agents/` sets `model` and `model_reasoning_effort`. An agent without a role runs on the
  session's model.
- A slash command such as `/name`: mention the skill as `$name`.
- This repository's hooks and `.claude/` paths are for Claude Code only, and nothing here installs a Codex
  hook. A loop runs one pass per invocation, saves its state and reports how to resume.
- `CLAUDE.md`: also read `AGENTS.md`, which is the file Codex loads.

# investigate

Investigate the reported behavior from reproduction to root cause. Fix it only when the request authorizes a change.

The task is the text given with this invocation.

---

## Authorization

Infer the terminal condition from the request:

- diagnose, explain, audit, or identify cause: investigate and report; do not edit;
- investigate and fix, debug this, resolve, or equivalent change intent: diagnose first, then implement and verify the smallest root-cause fix;
- ambiguity that would materially change behavior: finish the diagnosis, recommend a fix, and ask one focused question before editing.

Read applicable repository instructions and preserve staged, unstaged, untracked, and concurrent user work.

## Reproduce before fixing

1. State the observed behavior, expected behavior, environment, and trigger.
2. Reproduce with the smallest reliable case. Capture exact logs, state transitions, inputs, outputs, and relevant versions without exposing secrets or sensitive data.
3. If reproduction is impossible, identify the missing condition and use the strongest available trace or static evidence. Do not present speculation as a root cause.

## Adaptive hypothesis panel

Scale by uncertainty and blast radius:

- trivial: investigate directly or use 1 specialist;
- modest: 2-3 agents;
- normal: 4-7 agents;
- broad, cross-system, intermittent, security-sensitive, or high-risk: 8-12+ agents.

Choose independent lenses such as execution tracing, debugger/reproduction, data/state, recent history, concurrency, environment/operations, security, architecture, and test gaps. Orthogonality and independence matter more than reaching a count. Launch independent agents concurrently in one dispatch. Never use nested agents.

Tiers: hypothesis investigators run on your default model; the agents that try to falsify the leading hypothesis, and the root-cause synthesis, run on your strongest model. Pin the model on every agent; an unpinned agent inherits whatever the session runs on.

Require competing hypotheses. Each hypothesis must include:

- a causal mechanism and predicted observation;
- evidence for and against;
- a falsifying probe;
- confidence and affected scope.

Run the cheapest discriminating probes first. Update the ranking from observed evidence, not votes.

## Root-cause gate

Call a cause established only when it explains the reproduction, the causal path is evidenced, plausible alternatives have been falsified or bounded, and changing the cause predicts removal of the failure.

Before any authorized fix, add or identify a root-cause test that fails for the demonstrated mechanism, not merely the visible symptom. When a deterministic automated test is impractical, record a repeatable validation procedure and why.

## Fix and verify

For authorized changes:

1. Apply the smallest fix at the causal boundary.
2. Run the root-cause test and focused regression tests.
3. Check adjacent invariants suggested by the blast radius.
4. Use an independent reviewer or verifier for consequential changes; the author does not self-approve.

If evidence disproves the leading hypothesis, return to hypothesis ranking rather than patching symptoms. Do not broaden into unrelated cleanup.

Report reproduction, evidence, hypotheses considered, established root cause and confidence, fix authorization, changed files if any, and fresh verification results.
