---
name: context-shards
description: Build and use per-sequence project context shards so an agent can work on a feature film without loading the whole project state.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Context Shards

## Use

1. Read `../../references/CONTEXT_SHARDS.md`.
2. Read the current durable project state before you make a decision.
3. Work on the smallest valid `SEQ-###`, job frontier, or global gate.
4. Use `../../scripts/context_shards.py` for deterministic state changes or checks.
5. Save the result before you continue.
6. If the result blocks progress, keep the current Todo target blocked until the problem is fixed.

## Rules

- Do not load the full feature-film state when a sequence shard is sufficient. A shard includes the relevant canon and current story-state subset needed for its related character/location/prop IDs.
- Do not treat a shard as a second canon; authoritative project files still win.
- Do not infer completion from file existence alone.
- Do not hide an exception. Record the exception and the reason.
- Preserve stable IDs and project-relative paths.
- Use global checks only when the check needs global evidence.

## Done

The requested feature-scale state is written, validated, and traceable from durable project files.
