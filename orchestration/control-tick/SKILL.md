---
name: control-tick
description: Market listener control.tick orchestrator
version: 1.0.0
author: PonyBunny
tags: [market-listener, orchestration, scheduler]
phases: [execution]
user-invocable: false
disable-model-invocation: false
---

# Skill — control.tick

## Intent
Run one deterministic market-listener cycle. Handles source selection, rate limiting, checkpoint read/write, retries, and metrics.

## Inputs

```yaml
tick:
  run_id: string
  now: iso8601
  max_sources_per_tick: 10
  max_items_per_source: 50
  default_time_window: "6h"
```

## Outputs

```yaml
tick_result:
  run_id: string
  sources_processed: int
  items_fetched: int
  items_scanned: int
  items_stored: int
  errors: int
  duration_ms: int
```

## Tools
- pg.select (read sources + checkpoints)
- pg.execute (approved statements only)
- pg.insert (run logs)

## Policy
- No LLM calls.
- Apply per-platform rate limits and exponential backoff.
- Update checkpoints only after successful processing.
- Enforce circuit breaker after repeated failures.

## Failure Modes
- Source failure: mark failure, apply backoff, continue other sources.
- DB down: fail the tick and do not process.
