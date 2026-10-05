---
slug: openclaw-automation-architecture
version: 1.0.1
displayName: OpenClaw 自动化架构（Openclaw Automation Architecture）
summary: 设计基于 OpenClaw 的自动化系统，使用定时任务、会话代理等工具实现工作流自动化。
tags: clawhub
---

# OpenClaw Automation Architecture

## Overview

Design automations around OpenClaw's native primitives first. Reach for external workflow tools only when the job truly depends on third-party app glue, webhooks, or auth patterns that OpenClaw cannot cover cleanly.

Read `references/decision-matrix.md` when choosing the execution plane. Read `references/patterns.md` when the user needs a ready-made workflow pattern.

## Core Doctrine

- Prefer **OpenClaw-native** building blocks before Zapier, Make, or n8n.
- Prefer **small reliable systems** over giant brittle flows.
- Separate **trigger**, **execution**, **state**, **delivery**, and **recovery**.
- Pick the cheapest primitive that can do the job well.
- Do not ask the user to choose among primitives unless the trade-off materially affects behavior, cost, or reliability.

## Quick Selection

Use this order:

1. **Direct tool call now** — when the user wants an immediate result, not automation.
2. **`cron`** — when timing matters or the task must run independently.
3. **`HEARTBEAT.md`** — when the task is periodic housekeeping, context-aware maintenance, or a drift-tolerant batch check.
4. **Spawned session / specialist agent** — when the run is heavy, multi-step, or belongs to a dedicated role.
5. **Local script / MCP** — when the same deterministic operation will repeat.
6. **External workflow platforms** — only if native OpenClaw building blocks are not enough.

## Execution Plane Rules

### Use `cron` when time is the product

Reach for `cron` when the user wants:
- one-shot reminders
- daily or weekly reports
- scheduled monitoring
- isolated runs that should survive chat silence
- model-isolated or context-isolated jobs

Rules:
- Use `payload.kind="systemEvent"` only for `sessionTarget="main"`.
- Use `payload.kind="agentTurn"` for isolated jobs.
- If the run should notify a specific chat or recipient, prefer `delivery.mode="announce"` with `channel` / `to` instead of sending messages manually inside the run.
- Write reminder text so it reads naturally when fired, including enough context to make sense later.

### Use `HEARTBEAT.md` when drift is fine and context helps

Reach for heartbeat when the task is:
- maintenance
- periodic review
- memory consolidation
- cheap-gate checks followed by optional deeper work
- work that benefits from current conversation context

Do not use heartbeat for:
- precise alarms
- externally visible SLAs
- high-frequency fan-out jobs
- anything that must run exactly on time

### Use spawned sessions when the work is a real job, not a callback

Spawn a session when the task is:
- long-running research
- coding or refactoring
- multi-file content production
- specialist work for research, writing, trading, planning, or similar roles
- better handled by ACP harnesses such as Codex or Claude Code

Rules:
- If the user explicitly asks for Codex / Claude Code / Gemini in that style, use ACP harness intent.
- Do not wrap ACP intent in local shell hacks.
- Do not poll spawned workers in loops; let completion be push-based.

### Use a script or MCP when determinism matters

Create or reuse a local script / MCP when:
- the same transformation repeats
- the work is fragile and should not rely on free-form reasoning every time
- the workflow needs stable parsing, normalization, or batching
- the task already maps to an external API or local tool cleanly

Examples:
- feed normalization
- CSV enrichment
- content post-processing
- quote/fundamental data pulls
- knowledge-base ingest

### Use Zapier / Make / n8n only as the edge adapter

Escalate to external workflow tools only when you need:
- third-party app auth not covered by tools or MCPs
- webhook-first integrations across SaaS products
- drag-and-drop ops handoff for nontechnical collaborators
- app connectors that would be slower to recreate locally than to consume externally

Treat them as adapters, not the brain.

## Design Workflow

For every automation, define these five pieces in order.

### 1. Outcome

State the business result in one sentence.

Example:
- "Alert me when a paper release maps to a stock or theme I track."
- "Every morning, produce a shortlist and draft one article."

### 2. Trigger

Pick one:
- user request now
- schedule
- heartbeat poll
- new file / new data arrival
- external event / webhook

If the trigger is weak or noisy, add a cheap gate before expensive work.

### 3. Execution plane

Choose one primary plane:
- direct tool call
- cron main-session reminder/event
- cron isolated agent run
- heartbeat task
- spawned specialist agent
- deterministic script / MCP

Do not mix planes unless there is a clear handoff.

### 4. State and dedup

Always decide:
- where state lives
- how duplicates are prevented
- what counts as success
- what can be retried safely

Typical state locations:
- JSON state file in workspace
- curated memory file
- append-only log
- project artifact such as `today-briefing.md`

### 5. Delivery and recovery

Define:
- where the result goes
- how failures surface
- when to stay silent vs notify
- what the fallback is

Prefer a single notification path. Split success and failure channels only when necessary.

## Architecture Patterns

### Pattern A: Monitor → Filter → Notify

Use for news, prices, releases, topic monitoring, and alerts.

Structure:
1. scheduled trigger
2. fetch candidates
3. deduplicate
4. score importance
5. announce only if threshold met
6. save medium-priority items for digest

### Pattern B: Collect → Distill → Produce

Use for content factories and report generation.

Structure:
1. collector gathers raw material
2. artifact file stores shortlist or briefing
3. producer turns artifact into final output
4. optional review or delivery step

### Pattern C: Ingest → Normalize → Index

Use for RAG and knowledge pipelines.

Structure:
1. detect source
2. extract text/content
3. normalize metadata
4. chunk/index
5. optionally summarize or tag

### Pattern D: Scan → Decide → Act

Use for operations checks and maintenance.

Structure:
1. cheap gate
2. deeper scan only if needed
3. deterministic decision rule where possible
4. action or alert

### Pattern E: Fan-out specialist work

Use when the user asks for one outcome that naturally decomposes.

Structure:
1. orchestrator defines subtasks
2. delegate by specialty
3. collect outputs into one artifact
4. synthesize once at the top

## Guardrails

- Do not automate a bad process. Simplify first.
- Do not add an external platform if `cron` + tools + scripts already solve it.
- Do not build giant all-in-one jobs when two small jobs with a file handoff are clearer.
- Do not rely on repeated polling if eventing or longer waits work.
- Do not send external messages without approval when approval is required.
- Do not put business logic only in your head; store it in files, prompts, scripts, or config.
- Do not make every failure page the user. Some failures should log quietly and retry later.

## Output Expectations

When helping with an automation request, produce a concrete recommendation in this shape:

1. **Best execution plane**
2. **Why this plane wins**
3. **State + dedup plan**
4. **Failure handling**
5. **Whether native OpenClaw is enough or an external workflow tool is justified**

If the user asks to actually build it, implement the smallest end-to-end version first.

## Example Requests

- "Set up a daily report in OpenClaw."
- "Should this be a cron job or a heartbeat task?"
- "Help me replace this Zapier flow with native OpenClaw automation."
- "Design an alerting pipeline for topic monitoring."
- "How should I split this across agents, scripts, and scheduled jobs?"

## References

- Use `references/decision-matrix.md` for primitive selection and anti-patterns.
- Use `references/patterns.md` for ready-made workflow templates in OpenClaw terms.
