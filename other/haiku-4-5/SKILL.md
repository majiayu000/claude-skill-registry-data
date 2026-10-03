---
name: haiku-4-5
description: Claude Haiku 4.5 (claude-haiku-4-5) protocol — fast/cheap fan-out patterns, what to route to it and what not, thinking config. Trigger when working with, routing to, or writing code that calls Haiku 4.5.
---

# Haiku 4.5 — Speed-and-Volume Protocol

Model ID: `claude-haiku-4-5` (full: `claude-haiku-4-5-20251001`) · 200K context · 64K max output · $1 in / $5 out per MTok. The fastest, cheapest current model — its job is volume, latency, and fan-out, not depth.

## Staleness guard
Model facts here (ID, pricing, limits, API rules) were verified 2026-07. If a newer Haiku exists or the API contradicts this file: verify against current docs (Models API / platform.claude.com or the claude-api skill), follow the live source, and log the correction in `learnings.md`.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — what worked, what wasted tokens, what you'd prompt differently. Merge instead of duplicating; delete disproven bullets.

## Hard API rules (older-generation surface — different from Opus/Sonnet 5)
- Thinking uses the **legacy config**: `thinking: {type: "enabled", budget_tokens: N}` — N ≥ 1024 and strictly less than `max_tokens`. Adaptive thinking is not available; omit `thinking` for no thinking (the usual choice for Haiku work).
- **`effort` errors on Haiku 4.5** — don't send `output_config.effort`.
- `temperature`/`top_p` allowed (not both), unlike Opus 4.7+ / Sonnet 5.
- 200K context and 64K max output — the smallest limits in the lineup; chunk accordingly. Stream above ~16K output.
- Separate rate-limit pool from older Haiku models.

## Route TO Haiku
- Classification, extraction, tagging, routing, dedup, summarizing individual documents.
- Subagent fan-out: file sweeps, grep-and-report, per-item checks across many items — dozens of parallel Haiku calls cost less than one Opus turn.
- Latency-critical UI paths (autocomplete, quick answers, validators).
- High-volume batch pipelines (pair with the Batches API for another 50% off).

## Do NOT route to Haiku
- Multi-step architecture or debugging, long-horizon agent loops, anything where a wrong answer costs more than the Opus/Sonnet premium. Retrying Haiku three times on hard work costs more than one Sonnet call and still fails.

## Prompting patterns that matter on Haiku
- **Be maximally explicit.** Small models reward rigid structure: enumerate steps, give the exact output format, include one or two worked examples. What Fable treats as over-prescriptive is exactly right here.
- **Constrain output:** use structured outputs (`output_config.format` json_schema) or enum-field tools for classification — don't parse free text.
- **Tight `max_tokens`** (e.g. 256 for classification) — Haiku's cost is per token like everyone else; short outputs are the point.
- One task per call. Compound instructions degrade fast — split them.

## Token discipline
- Cache the shared prefix across the fan-out (min cacheable prefix on Haiku 4.5 is 4096 tokens).
- Send only the slice of context each call needs — never the whole file set to every worker.
- Aggregate Haiku outputs with a stronger model rather than asking Haiku to synthesize across items.
