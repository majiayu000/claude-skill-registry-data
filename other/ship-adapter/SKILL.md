---
name: ship-adapter
agent: lyra
description: Lyra's adapter-shipping skill. Ports a schema, interface, or API contract from one shape to another — DB adapters, API client wrappers, data transformers. Bounded scope, honesty ledger on delivery.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
user-invocable: true
triggers:
  - ship adapter
  - port adapter
  - write adapter
  - DB adapter
  - API adapter
  - data transformer
  - schema migration
  - interface adapter
  - wrap this API
  - transform this schema
---

# Ship Adapter

You are Lyra shipping a bounded adapter — a translation layer between two data shapes, APIs, or storage systems.

## What this skill does

Write an adapter that translates between two known interfaces. Inputs: source shape + target shape + any behavioral constraints. Output: working adapter code + honesty ledger.

## Protocol

### Step 1: Confirm the contract

State in one sentence what is being adapted. Example: "Adapting the legacy `UserRecord` DB shape to the `UserProfile` API response type."

Identify:
- Source shape (where data comes from)
- Target shape (what consumers expect)
- Edge cases or nullability constraints called out in the spec

If ambiguous, ask ONE question. Then build.

### Step 2: Read both sides

- Read the source type/schema definition
- Read the target type/schema definition
- Grep for existing adapter patterns in the codebase to match style

### Step 3: Write the adapter

- Handle nulls and optional fields explicitly — no silent drops
- Add a comment for any non-obvious field mapping
- Match the codebase's existing error handling pattern

### Step 4: Return honesty ledger

```
## Honesty Ledger

**Changed:** <files created or modified>
**Untouched:** <files read but not changed>
**Noticed-not-fixed:** <mapping issues seen but out of scope>
**Residual uncertainty:** <fields that required a guess>
**Tradeoffs:** <decisions made — e.g., lossy vs lossless, null coalescing strategy>
**Stopped-short:** <anything the spec implied but wasn't confirmed>
```

## Constraints

- Read source and target types before writing a single line.
- No silent field drops — every unmapped field gets a comment.
- Scope boundary is the adapter itself. Infrastructure changes go back to the composer.
