---
name: fable-5
description: Claude Fable 5 (claude-fable-5) protocol — selection, prompting, effort tuning, token discipline. Trigger when working with, routing to, or writing code that calls Fable 5.
---

# Fable 5 — Maximum-Capability Protocol

Model ID: `claude-fable-5` · 1M context (default and max) · 128K max output · $10 in / $50 out per MTok — the most expensive tier. Every rule below exists to convert that cost into results a cheaper model can't produce.

## Staleness guard
Model facts here (ID, pricing, limits, API rules) were verified 2026-07. If a newer Claude model generation exists, pricing looks off, or the API contradicts this file: verify against current docs (Models API / platform.claude.com or the claude-api skill) before relying on them, follow the live source, and log the correction in `learnings.md`.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply every relevant lesson.
2. **At end of every use:** append one dated bullet to `learnings.md` — what worked, what wasted tokens, what you'd prompt differently. One lesson per bullet, concrete, project-agnostic. Merge into an existing bullet instead of duplicating; delete bullets proven wrong.

## When to route work here
Use Fable 5 only for work at the top of the difficulty range: long-horizon autonomous runs, hard architecture/debugging that other models failed, first-shot builds of well-specified systems, end-to-end deliverables. Routine work belongs on Opus 4.8 or below — Fable at low effort still beats prior models' max, but you're paying 2× Opus rates for it.

## Hard API rules (violations are 400 errors)
- **Omit the `thinking` parameter entirely** (or `{type: "adaptive"}`). Thinking is always on; `disabled` and `budget_tokens` are rejected.
- No `temperature` / `top_p` / `top_k`. No assistant prefill.
- Raw chain of thought is never returned. `thinking: {type: "adaptive", display: "summarized"}` for readable summaries; default is omitted (empty thinking text).
- Handle `stop_reason: "refusal"` before reading content, and ship the server-side fallback by default: `betas: ["server-side-fallback-2026-06-01"]`, `fallbacks: [{"model": "claude-opus-4-8"}]`.
- Requires 30-day data retention (ZDR orgs get 400 on every request).

## Getting the most out of it
- **Full spec up front, one turn.** State the goal, constraints, and what "done" looks like in the first message. Progressive drip-feeding reduces quality and burns tokens.
- **Give the reason, not just the request:** "I'm working on X for Y; they need Z. With that in mind: [request]."
- **Effort is the lever:** `output_config.effort` — `high` default, `xhigh` for the hardest coding/agentic work, `max` only when correctness outweighs cost, `low`/`medium` for routine passes. Lower effort = fewer, more consolidated tool calls.
- **De-prescribe.** Prompts written for older models (step-by-step scaffolding, "CRITICAL: YOU MUST") reduce Fable output quality. State goal + constraints, not steps.
- **Delegate.** Parallel sub-agents are dependable — fan independent subtasks out and keep working; asynchronous beats spawn-and-block.
- **Give it a memory surface.** Even a plain `.md` file it can write learnings to measurably improves multi-session work.
- **Plan for long turns.** Single hard requests can run many minutes — stream, set generous timeouts, don't block a UI on one call.

## Token discipline
- Anti-overengineering guard: "Don't add features, refactor, or abstract beyond what the task requires. Simplest thing that works."
- Ground progress claims: "Only report work you can point to tool-result evidence for."
- For autonomous runs, add the no-early-stop reminder: act instead of announcing intent; end the turn only when done or blocked on the user.
- Cache-friendly prompts: frozen system prompt first, volatile content after the last cache breakpoint.
