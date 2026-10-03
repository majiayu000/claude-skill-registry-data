---
name: opus-4-8
description: Claude Opus 4.8 (claude-opus-4-8) protocol — prompting, effort/thinking config, fast mode, token discipline. Trigger when working with, routing to, or writing code that calls Opus 4.8.
---

# Opus 4.8 — Workhorse-Flagship Protocol

Model ID: `claude-opus-4-8` · 1M context · 128K max output · $5 in / $25 out per MTok. The default choice for serious coding, agentic, and knowledge work — Fable-adjacent capability at half the price.

## Staleness guard
Model facts here (ID, pricing, limits, API rules) were verified 2026-07. If a newer Claude model generation exists, pricing looks off, or the API contradicts this file: verify against current docs (Models API / platform.claude.com or the claude-api skill) before relying on them, follow the live source, and log the correction in `learnings.md`.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — what worked, what wasted tokens, what you'd prompt differently. Merge instead of duplicating; delete disproven bullets.

## Hard API rules
- **Adaptive thinking is NOT on by default** — omitting `thinking` runs without thinking. Set `thinking: {type: "adaptive"}` explicitly for anything non-trivial.
- `budget_tokens`, `temperature`, `top_p`, `top_k` → 400. Assistant prefill → 400 (use `output_config.format` for structured output).
- `thinking.display` defaults to `"omitted"`; set `"summarized"` if reasoning is shown to users.
- Stream anything with `max_tokens` above ~16K.

## Unique capabilities — use them
- **Fast mode** (Opus 4.8/4.7 only): `client.beta.messages.create(..., speed="fast", betas=["fast-mode-2026-02-01"])` — same model, up to 2.5× output speed, premium price. Use for latency-critical paths.
- **Mid-conversation system messages** (Opus 4.8 only, no beta): append `{"role": "system", "content": ...}` to `messages[]` to inject operator instructions without invalidating the prompt cache.
- **Task budgets** (beta `task-budgets-2026-03-13`): give agentic loops a token ceiling the model can see and pace against; minimum 20K.

## Prompting patterns that matter on 4.8
- **Effort:** sweep `medium`/`high`/`xhigh` per route; default `high`, `xhigh` for coding/agentic. Higher effort up front often *reduces* total cost on agentic work (fewer turns). Reserve `max` for latency-insensitive hard problems.
- **Search-first nudge:** 4.8 under-reaches for search, subagents, memory, and custom tools by default. Say *when* to use each capability — in the system prompt and in each tool's own `description` ("Call this when…").
- **Silence default:** 4.8 narrates more than 4.7. If too chatty: "Default to silence between tool calls; one sentence when you find something or change direction; one–two sentences when done."
- **Autonomy guard:** 4.8 asks more often. "For minor choices, pick a reasonable option and note it. For scope changes or destructive actions, ask first." (~12pp fewer asks, no over-reach.)
- **Full spec first turn** for long-horizon work; run at `high`/`xhigh`.
- **Code review:** it follows "only high-severity" literally — tell it to report everything with confidence + severity, filter downstream.

## Token discipline
- Remove forced-progress scaffolding ("summarize every N tool calls") — 4.8 does this natively.
- Cache-first prompt layout: stable system + tools first, volatile content after the last breakpoint; verify with `usage.cache_read_input_tokens`.
- Delegate cheap fan-out (search, file sweeps, classification) to Haiku 4.5 subagents; keep 4.8 as orchestrator.
