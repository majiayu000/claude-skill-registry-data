---
name: model-comparison
description: Compare AI models across benchmarks, pricing, and capabilities. Use when the user asks to compare models, evaluate trade-offs, or pick the best model for a task.
---

# Model Comparison Skill

## Step 1 — Establish scope and coverage

Translate the request into explicit dimensions: task capability, benchmark quality, provider-endpoint throughput/latency, price, context, reliability, and any user-supplied constraints. Unquantified adjectives are ranking preferences, never hidden thresholds.

For a market-wide request:

1. Call `get_llm_leaderboard` for capability and benchmark context.
2. Call `search_fast_model_endpoints` without model IDs or invented numeric filters so it evaluates the catalog and returns endpoint-level price/speed evidence.
3. Check `coverage.complete`, `catalog_matches`, `evaluated_models`, and failures before making a superlative claim. If coverage is incomplete, continue discovery or label the result partial.

For named models, use `get_model_endpoints` for each exact catalog ID. Use `web_search` only for current facts or practical evidence missing from dashboard tools; it is not mandatory filler.

## Step 2 — Synthesize

Separate materially different capability tiers before comparing price and speed. A safety classifier, extractor, or tiny utility model is not a substitute for a general-purpose reasoning model simply because it is cheap or fast.

Build a comparison table with columns appropriate to the evidence, normally Model, Endpoint Provider, Capability/Benchmark, Throughput Percentile, Latency, Input $/1M, Output $/1M, and Uptime.

Then add:
- **Trade-off callouts**: quality vs speed vs cost — be explicit about where each model wins and loses
- **Practical notes**: distinguish measured facts from inference or external reports
- **Chart block** if comparing 3+ models

## Step 3 — Recommend

If the user supplies numeric constraints, apply them exactly. Otherwise return the Pareto-optimal tradeoffs within each relevant capability tier and explain how the choice changes with priorities. Do not invent a weighted score or filter, and do not call a partial sample "best."

## Output checklist

- At least one numeric metric per model (with units: tok/s, $ / 1M tokens)
- Coverage and metric scope disclosed
- Chart included for visual comparison when 3+ models
- Final recommendation is specific, not hedged
