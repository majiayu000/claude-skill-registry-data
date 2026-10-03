---
name: sonnet-5
description: Claude Sonnet 5 (claude-sonnet-5) protocol — near-Opus coding at Sonnet cost, effort tuning, literal instruction patterns. Trigger when working with, routing to, or writing code that calls Sonnet 5.
---

# Sonnet 5 — Speed-Value Protocol

Model ID: `claude-sonnet-5` · 1M context · 128K max output · $3 in / $15 out per MTok ($2/$10 intro through 2026-08-31). Near-Opus quality on coding and agentic work at a fraction of the cost — the best default when Opus-tier depth isn't required.

## Staleness guard
Model facts here (ID, pricing, limits, API rules) were verified 2026-07. Intro pricing expires 2026-08-31. If a newer Claude model generation exists or the API contradicts this file: verify against current docs (Models API / platform.claude.com or the claude-api skill), follow the live source, and log the correction in `learnings.md`.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — what worked, what wasted tokens, what you'd prompt differently. Merge instead of duplicating; delete disproven bullets.

## Hard API rules
- **Adaptive thinking is ON when `thinking` is omitted** (opposite of Opus 4.8). Set `{type: "disabled"}` explicitly only for latency-critical simple paths — prefer adaptive + `effort: "low"`.
- `budget_tokens` → 400. Non-default `temperature`/`top_p`/`top_k` → 400. Assistant prefill → 400.
- New tokenizer: ~30% more tokens than Sonnet 4.6 for the same text — re-baseline `max_tokens` and budgets with `count_tokens`.
- `thinking.display` defaults to `"omitted"` — set `"summarized"` if you show reasoning.

## Where it shines
- Interactive coding sessions, medium-complexity agent loops, high-volume pipelines where Opus cost doesn't pay for itself.
- First Sonnet with `xhigh` effort and high-res vision (2576px) — use `xhigh` for its hardest coding tasks.
- Rough mapping: Sonnet 5 `medium` ≈ Sonnet 4.6 `high`; Sonnet 5 `high` ≈ Sonnet 4.6 `max`.

## Prompting patterns that matter on Sonnet 5
- **It is very literal.** It won't generalize an instruction across items or infer unstated requests. State scope explicitly ("apply to every section, not just the first"). Re-baseline holdover style directives — they now apply at face value.
- **More agentic by default** — reaches for tools and self-verification readily. With thinking disabled it's less tool-eager; add an explicit tool-triggering nudge if you disable thinking.
- **Drop forced progress scaffolding** — its native interim updates are good.
- **Effort over prompting:** if reasoning is shallow at `low`/`medium`, raise effort rather than adding "think carefully" prose.
- **Design variety:** no temperature — use "propose 4 distinct visual directions, pick one" instead.
- **Code review:** report-everything-filter-downstream, same as Opus.

## Token discipline
- Leave `max_tokens` headroom at `xhigh`/`max` — adaptive thinking shares the output budget; `stop_reason: "max_tokens"` with a wall of thinking means the budget was too tight.
- Cache-first layout; verify `cache_read_input_tokens`.
- Route true fan-out grunt work down to Haiku 4.5; route work Sonnet repeatedly fails at up to Opus 4.8 rather than retrying.
