---
name: decide-events
description: When to use Events & Listeners vs direct calls. Decoupling decisions.
---

# Skill: Events

> "Events are for side effects. Actions are for intent."

## The Decision

**Use Events when:**
- Side effects can multiply (notifications, logs, syncs)
- Consumers don't need the result
- Cross-domain communication is needed
- The trigger shouldn't know about all consequences

**Use Direct Calls when:**
- The caller needs a return value
- There's exactly one consumer, forever
- Failure must halt the operation

## The Heuristic

Ask: *"If I add another consequence later, should the caller change?"*

- **No** → Event
- **Yes** → Direct call

## The Quick Test

| Ask Yourself                 | Answer | Use    |
|------------------------------|--------|--------|
| Multiple reactions possible? | Yes    | Event  |
| Caller needs result?         | Yes    | Direct |
| External system involved?    | Yes    | Event  |
| Single, obvious dependency?  | Yes    | Direct |

## Real-World Examples

For concrete examples, see [examples.md](examples.md).
