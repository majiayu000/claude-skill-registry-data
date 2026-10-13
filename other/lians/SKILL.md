---
name: lians
description: Use Lians financial-grade agent memory - store and recall facts with a bitemporal model so stale revisions never contaminate context. Use whenever an agent needs persistent memory in finance, healthcare, or legal work, or when a task asks "what did we know on/before <date>", needs an audit trail, or must erase a data subject.
---

# Lians Memory

Lians is a memory layer for AI agents built for regulated environments. Unlike a
plain vector store, it uses a **bitemporal** model: every fact carries the
business time it became true (`event_time`) and the system time it was known
(`valid_from`/`valid_to`). When a new fact supersedes an old one, the old one is
excluded from recall automatically - but remains reconstructable for any past date.

Use Lians when the agent works with facts that **change over time**: guidance
revisions, dosage changes, matter status, prior decisions - and when those changes
must be auditable.

## Setup

```bash
pip install lians-sdk          # hosted / self-hosted
pip install lians-sdk[local]   # zero-setup local SQLite (no server, no API key)
```

Environment (hosted/self-hosted): `LIANS_URL`, `LIANS_API_KEY`, `LIANS_AGENT_ID`.
Get a free key at api.lians.dev. Local mode needs none.

## Clients (same API surface)

```python
from lians import LiansClient        # sync HTTP - scripts, CLIs
from lians import AsyncLiansClient   # async HTTP - FastAPI, async frameworks
from lians import LocalLiansClient   # local SQLite - prototyping, CI, notebooks
```

## Core operations

```python
from datetime import datetime, timezone
mem = LiansClient(base_url=os.environ["LIANS_URL"], api_key=os.environ["LIANS_API_KEY"])

# Store - event_time is the BUSINESS time the fact became true, not now
mem.add(agent_id="desk", content="NVDA guidance raised to $40B",
        event_time=datetime(2025, 11, 19, tzinfo=timezone.utc),
        metadata={"ticker": "NVDA", "metric": "revenue_guidance"})

# Recall - current, non-stale facts only
res = mem.recall(agent_id="desk", query="NVDA guidance", k=5)
for m in res["memories"]:
    print(m["event_time"], m["content"])

# Point-in-time - what did we know on a past date?
mem.recall_at(agent_id="desk", query="NVDA guidance",
              as_of=datetime(2025, 9, 1, tzinfo=timezone.utc))

# From a conversation
mem.add_from_messages(agent_id="desk",
    messages=[{"role": "assistant", "content": "TSLA Q4 deliveries hit 495k"}])
```

## Drop-in agent loop - the harness

For a turn-based agent, the harness handles recall-before / remember-after for you:

```python
from lians import LiansClient, LiansMemoryHarness

harness = LiansMemoryHarness(mem, agent_id="desk", domain="finance")  # finance|healthcare|legal

context = harness.recall_context("NVDA guidance")    # ready to inject into a prompt
harness.remember("Desk note: guidance now $40B")     # write after the turn
# or both in one call:
answer = harness.run_turn(user_query, generate=lambda ctx, q: call_model(ctx, q))
```

Scope writes to a data subject and information barrier when needed:

```python
harness = LiansMemoryHarness(mem, agent_id="care-3",
                             subject_id="MRN-00042",   # per-subject key → crypto-shred target
                             barrier_group="oncology", # information-barrier tag
                             domain="healthcare")
```

## Compliance surfaces

| Need | Call |
|------|------|
| Full knowledge state at date T | `mem.snapshot(agent_id, as_of=T)` |
| Verify SEC 17a-4 audit chain | `mem.verify_chain()` |
| Detect lookahead bias in a backtest | `mem.backtest_check(agent_id, simulation_as_of=T)` |
| GDPR/HIPAA crypto-shred a subject | `mem.erase(subject_id, request_ref)` |

## Rules

- `event_time` = when the fact became true (business time), **not** now. Store the
  precision you were given; never fabricate a timestamp.
- For any "what did we know on/before <date>" question, use `recall_at` /
  `snapshot` - never present-state `recall`.
- Report audit/snapshot output literally; do not paraphrase evidentiary results.
- If a recalled fact's `content` is `null`, it was crypto-shredded - say so.
- `erase()` is irreversible and needs a request reference - confirm before running.

## Domain metadata (enables keyed supersession)

- finance → `{"ticker": "...", "metric": "..."}`
- healthcare → `{"patient_id": "...", "condition": "..."}`
- legal → `{"matter_id": "...", "claim_type": "..."}`
