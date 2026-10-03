---
name: claude-all-models
description: Route tasks across the Claude lineup — model selection, delegation, cost/speed trade-offs, cache discipline. Trigger for any model-selection, routing, multi-model, or cost-optimization decision.
---

# All Models — Fleet Protocol

Treat the lineup as one machine with four gears. The single biggest lever for correctness AND cost is routing each task to the cheapest model that reliably does it — then never re-doing work on a bigger model that a smaller one already finished.

## Staleness guard
The lineup table below was verified 2026-07. Model lineups change: before load-bearing routing/cost decisions, confirm the current lineup (Models API / platform.claude.com or the claude-api skill). New models slot into the same gear logic; update the table and log the change in `learnings.md`.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — routing decisions that paid off or backfired, cost surprises, delegation patterns that worked. Merge instead of duplicating; delete disproven bullets.

## The lineup (current, verified)

| Model | ID | Context / Max out | $/MTok in–out | Role |
|---|---|---|---|---|
| Fable 5 | `claude-fable-5` | 1M / 128K | 10 – 50 | Hardest problems only; long-horizon autonomy |
| Opus 4.8 | `claude-opus-4-8` | 1M / 128K | 5 – 25 | Default flagship: serious coding, agents, review |
| Sonnet 5 | `claude-sonnet-5` | 1M / 128K | 3 – 15 (intro 2–10 to 2026-08-31) | Near-Opus coding at volume; interactive work |
| Haiku 4.5 | `claude-haiku-4-5` | 200K / 64K | 1 – 5 | Fan-out, classification, latency paths |

Per-model depth lives in the sibling skills: `fable-5`, `opus-4-8`, `sonnet-5`, `haiku-4-5` — load the one matching the model you're actually driving.

## Routing rules
1. **Start one gear lower than instinct says.** Escalate on demonstrated failure, not anticipated difficulty. Sonnet 5 at `high` handles most of what people reflexively send to Opus.
2. **Never retry a failure on the same gear more than once.** Two failures → escalate with the failure context attached ("Sonnet tried X, output was wrong because Y").
3. **Never send finished work back up.** If Haiku classified 500 items, have the bigger model spot-check a sample, not redo them.
4. **Orchestrator high, workers low.** One Opus/Fable orchestrator delegating to Haiku/Sonnet subagents beats one giant model doing everything serially — cheaper and faster.
5. **Match effort before matching model.** Bumping Sonnet `high → xhigh` is cheaper than switching to Opus; try it first.

## API-surface differences that bite when switching models
- Thinking: Fable = always on (omit param) · Opus 4.8 = off unless `{type:"adaptive"}` set · Sonnet 5 = adaptive when omitted · Haiku = legacy `budget_tokens` only.
- `effort`: supported Fable/Opus/Sonnet 5 (`low`→`max`); errors on Haiku 4.5.
- Sampling params: rejected on Fable/Opus 4.8/Sonnet 5; allowed on Haiku.
- **Switching models mid-conversation invalidates the prompt cache** — spawn a subagent on the other model instead of swapping the main loop.
- Tokenizers differ — re-baseline `max_tokens` with `count_tokens` per model, never reuse counts.

## Cost discipline
- Prompt caching first: stable prefix (tools → system) frozen, volatile content last; verify `cache_read_input_tokens` > 0.
- Batches API = 50% off anything non-latency-sensitive; pair with Haiku for the cheapest possible per-item cost.
- Fable's fallback: ship `fallbacks: [{"model": "claude-opus-4-8"}]` so refusals degrade instead of failing.
- Log which model produced what; when reviewing costs, cut by moving traffic down-gear before cutting features.

## Regression eval — not yet built
No harness exists to catch a skill or routing change regressing across the lineup. Not worth building speculatively. **Build it when:** the same skill shows behavior drift after 2+ routing/model changes to it — that's the signal a fixed prompt-set eval would have caught earlier and cheaper than debugging it live.
