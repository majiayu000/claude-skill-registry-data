---
name: swarm
description: Atomic multi-agent batch execution engine. Executes a single concurrent batch of M Interns via subagent_batch and aggregates outputs.
---

# swarm: atomic multi-agent batch engine

This skill is the low-level execution engine for parallel multi-agent sweeps.
A single Swarm is an atomic execution unit: **1 Swarm = 1 concurrent batch of M read-only Interns (`subagent_batch`)**.
Swarm does not define multi-round state machines. Caller skills (`audit`, `init`, `ssot`, `auto`) orchestrate N rounds of Swarms with custom M counts.

## Specifications and constraints

- **Worker role**: Intern. The infra2 SDK `LlmSettings` role `small` gives its model and reasoning effort. `subagent-worker --check-models` prints them.
- **Batch size (M)**: Default 10 tasks per swarm batch. `PROVIDER_CONCURRENCY` in `subagent-worker` sets how many requests run at once; the rest run in waves. Custom M specified by caller skill (e.g. M=4 in `init`/`ssot`, M=3 in `auto`).
- **Tool profile**: Strictly read-only tools or prompt-injected source code via `subagent_batch`.
- **Output contract**:
  - Dense, structured ASD-STE100 technical findings.
  - Length: 500 to 1200 tokens per Intern.
  - Anchors required: Every finding must cite exact file anchors (`file#Lxx-Lyy`) and reproducible counterexamples.
  - Zero conversational filler. Start line 1 with the single line-1 JSON verdict contract defined in `workspace-iac/bin/subagent-worker` (`{"subject": "claim" | "code", "verdict": "holds" | "breaks" | "unknown", "anchors": [...], "unverified": [...]}`). Do not restate or invent a secondary format.

## Atomic invocation protocol

To execute 1 Swarm, the orchestrator invokes `subagent_batch` with M tasks:

1. Prepare task array with M distinct task objects: `[{"id": "...", "prompt": "..."}]`.
2. Pass target files via `context_files: [{"path": "...", "start_line": 1, "end_line": 120}]` (and optional `cwd`) so the worker reads disk once without duplicating code in tool-call JSON.
3. Call `subagent_batch`.
4. Reduce outputs: Full output persists to `~/.local/state/subagent-worker/runs/<call_id>.md`; inline return folds evidence-free `holds` tasks (`unverified: []`) and expands `breaks`, `unknown`, non-empty `unverified`, `unparsed`, `PARTIAL`, or `FAILED` tasks into `SwarmResult`.
5. Return `SwarmResult` to the calling skill for the next state transition.

## Execution discipline

- **Physical exit codes required**: Cite actual commands and exit codes. A score or claim without a physical command is invalid.
- **Call deadline**: A call ends within 110 s. A batch with more tasks than the concurrency limit gets that time once per wave, up to 600 s. A task may use the time left in its batch, less one wave per wave of queued tasks; 50 s of silence still ends it. A task cut by the deadline is FAILED (no text) or PARTIAL (text so far). A provider filter or a provider fault inside the answer is PARTIAL too. The first output line gives the counts. Worker log: `~/.local/state/subagent-worker/worker.log`.
