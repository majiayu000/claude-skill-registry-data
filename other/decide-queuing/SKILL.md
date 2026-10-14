---
name: decide-queuing
description: When to queue work vs execute synchronously. Async decisions.
---

# Skill: Queuing

> "If it can fail and retry, it's a Job."

## The Decision

**Queue as Job when:**
- External API call (Shopify, Stripe, Email)
- Execution > 100ms
- Operation can fail and should retry
- User doesn't need immediate result

**Execute Synchronously when:**
- User is waiting for the result
- Failure should show immediately
- Fast, in-memory computation

## The Heuristic

Ask: *"Can this fail, and should we retry without user intervention?"*

- **Yes** → Job
- **No** → Sync

## The Quick Test

| Ask Yourself  | Answer | Use  |
|---------------|--------|------|
| External API? | Yes    | Job  |
| User waiting? | Yes    | Sync |
| Needs retry?  | Yes    | Job  |
| < 100ms?      | Yes    | Sync |

## Real-World Examples

For concrete examples, see [examples.md](examples.md).
