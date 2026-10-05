---
name: data-store-record
description: Market listener data.store_record persistence + dedupe
version: 1.0.0
author: PonyBunny
tags: [market-listener, persistence, dedupe]
phases: [execution]
user-invocable: false
disable-model-invocation: false
---

# Skill — data.store_record

## Intent
Persist observation records in Postgres, enforcing append-only semantics and dedupe.

## Inputs

```yaml
store_request:
  platform: string
  source_id: string
  permalink: string
  author: string|null
  created_at: iso8601|null
  problem_raw_text: string
  surrounding_context: string
  label: string
  signal_markers: string[]
  role_guess: string
  role_confidence: number
  raw_text_hash: string
  ingest_run_id: string
```

## Outputs

```yaml
store_result:
  stored: boolean
  record_id: string|null
  deduped: boolean
```

## Tools
- pg.select
- pg.insert
- pg.execute (approved statements only)

## Policy
- Append-only: never update existing observation records.
- Dedupe on permalink and raw_text_hash.
- Never delete data.

## Failure Modes
- Dedupe hit: return deduped true and do not insert.
- DB error: bubble error to orchestrator.
