---
name: mozglo-orchestrator
description: Coordinate authorized Codex work with native Astra, Sol, and Luna agent roles, compact checkpoints, and recovery. Use when a task needs bounded parallel work or durable orchestration.
---

# MOZGLO Orchestrator

First decide whether current native agents can complete the task. Use them directly when sufficient. Start the packaged runner once only when orchestration, recovery, or capacity is needed. Never recursively launch a runner or Codex CLI from an executing root. The runner requires Linux, Python 3.10+, and the existing authenticated Codex CLI; it is independently installable with this skill.

## Roles and authorization

Astra owns scope, planning, authorization continuity, allocation, integration, and final reporting. Sol coordinates, investigates, makes technical decisions, and reviews. Luna implements every product change and does not delegate. Preserve user authorization through handoffs and recovery; delegation never expands it. Assign bounded tasks with owner, baseline, acceptance evidence, dependencies, and checkpoint. Path assignments guide coordination and do not create locks. Avoid duplicate or overlapping edits by coordinating baselines.

Defaults request one Astra, one Sol, and five Lunas; tiny work can use Astra and one Luna. Default requested models are `gpt-6-astra`, `gpt-6.1-sol`, and `gpt-6-luna`. Configure role models, reasoning effort, counts, sandbox, and an existing Codex profile in settings; counts and models are requests, not capacity or identity guarantees. For native delegation, use configured model and effort, `fork_turns: none`, and a compact brief. Provider compatibility is not universal. Keep within available capacity and the hard cap of 15 total agents.

## Memory and recovery

Use native agent messages for live coordination and keep the roster and task status in `.mozglo/context.md`. Astra maintains accepted scope and authorization, roster and ownership, baselines, current decisions (mark superseded decisions), verified progress, evidence, blockers, and next actions. Replace outdated notes instead of appending an endless history. Keep credentials, tokens, private messages, and production payloads out of prompts, memory, logs, and reports.

Before retrying interrupted work, inspect the checkpoint, runner status, and existing worker/process state. Do not assign unfinished work to a second writer until the earlier one is finished. Preserve completed changes and evidence, then continue from the checkpoint. Stop only the owned verified process group; a local stop signal does not prove remote or delegated work has stopped.

## Reports

Give workers compact text handoffs with scope, authorization, owner, baseline, acceptance evidence, dependencies, and checkpoint location. Worker status messages and internal handoffs are three to six lines and contain no images. For the final user report, lead with the result and include one to three technical images plus two to four concise lines or links; use fewer or no images when requested or when rendering is unavailable, and state that limitation plainly. Distinguish completed, verified, prepared, installed, and activated work.

See the [runtime reference](references/runtime.md) for commands and settings and the [report reference](references/report.md) for checkpoint and reporting details.
