---
name: zao-bench
description: Benchmark ZOE's model stack - cost, latency, and EMPIRICAL prompt-cache hit rate per model tier (claude haiku/sonnet via the CLI, deepseek via OpenRouter), plus a live wiring check of ZOE's shipped features (cross-family critic, tracing, verify-replan, nudge-ladder, cost-ledger). Use when Zaal asks to "benchmark ZOE", "test the model tiers", "prove caching is working", "how much does a ZOE call cost", "is the deploy healthy / are the features live", or types /zao-bench. Produces a dated markdown report. Read-only + cheap (a few tiny model calls) - no prod writes, no deploys.
---

# zao-bench

Turn "it's probably cached / it should be cheaper" into DATA. This is ZAO's internal
benchmark harness for the ZOE model stack - the "test everything one by one + make
internal benchmarks" tool (Zaal 2026-08-06). It measures each tier and proves whether
caching actually fires, instead of assuming it.

## What it measures

1. **Per model tier** (claude/haiku, claude/sonnet via the `claude` CLI; deepseek via
   OpenRouter): input tokens, output tokens, cost (usd), latency (ms) - run TWICE.
2. **Cache hit, empirically.** The trick: run the same prompt twice. A working
   prompt-cache shows up on run 2 as `cache_read_input_tokens` (claude) /
   `prompt_cache_hit_tokens` (deepseek). If run 2 shows cached tokens + a lower cost,
   caching is real - proven, not assumed. (First bench, 2026-08-06: claude auto-caches
   big - haiku 50k cached / -50% cost on repeat; deepseek did NOT show a hit for a
   small prompt - a real gap to chase, not the assumption we started with.)
3. **ZOE feature wiring (live).** Confirms the shipped upgrades are actually deployed:
   cross-family critic (`runCritiqueModel`), step tracing (`trace.ts` + traces written),
   verify-replan (the `bare` flag gone), nudge-ladder (+ its flag), cost-ledger.

## How to run

The runner lives beside this file and executes on the VPS (where the `claude` CLI +
the OpenRouter key live). It writes a dated report to `~/.zao/bench/` and prints it.

```bash
# default prompt suite
ssh vps 'bash ~/zao-os/.claude/skills/zao-bench/bench.sh'
# or a custom prompt (e.g. a long reused context to test caching on real payloads)
ssh vps 'bash ~/zao-os/.claude/skills/zao-bench/bench.sh "your prompt here"'
```

(If the repo path differs on the VPS, `scp` the script over first, or run it from the
deployed clone. The script sources `~/zao-bot-live/bot/.env` for the OpenRouter key -
it never prints the key.)

## How to read the report

- **cache hit YES on run 2** = that tier caches repeated context. Compare run1 vs run2
  cost - the drop is your caching savings, measured.
- **cache hit NO** where you expected YES = the caching you assumed isn't firing
  (small prompt below the cache threshold, or the provider isn't surfacing it). Chase it.
- **cost/latency across tiers** = validates the routing choices: the cheap tier should
  be materially cheaper for grunt work (`claude-usage.md`, doc 2208).
- **a feature "missing"** = not deployed; check the autodeploy (`zoe-autodeploy.sh`).

## Extending it

- Add a tier: a new `*_run()` fn that returns `in|cache|out|cost|ms` + a `row` call.
- Add a real-payload cache test: pass a large reused context as `$1` (small prompts
  fall below provider cache thresholds - that is why the default suite under-reports
  deepseek caching).
- Add a feature check: one line in the "ZOE feature wiring" block asserting the file +
  a grep for the wired symbol.

## Guards

- Read-only + cheap: a handful of tiny model calls per run (cents). No prod writes, no
  deploys, no wallet/on-chain. Safe to run anytime.
- Never prints secrets - the OpenRouter key is sourced from `.env`, used, never echoed
  (`secret-hygiene.md`).
- Report the numbers honestly - a "no cache" or a "missing feature" is a finding, not a
  failure to hide (`anti-fabrication.md`, `silent-failure-guard.md`).

## Source

Built 2026-08-06 after grounding found ZOE's Claude calls already auto-cache via the CLI
and the loops route to DeepSeek - so the doc 2208 "build prompt caching" was largely a
non-gap, and what was actually needed was a way to MEASURE it. Companion: doc 2208 (cost
levers), `claude-usage.md` (surface tiering), the ZOE cost-ledger + trace.
