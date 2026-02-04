---
name: sea-flow-annotations
description: Enforce Flow-only CQRS tagging and recommended metadata.
---

# SEA™ Flow annotation contract


## Mandatory
Every Flow includes:
```sea
@cqrs { "kind": "command" }
```

## Recommended templates
Command:
```sea
@cqrs { "kind": "command" }
@tx { "transactional": true }
@idempotency { "enabled": true, "key": "header:X-Idempotency-Key" }
```

Event:
```sea
@cqrs { "kind": "event" }
@outbox { "mode": "required" }
```

Query:
```sea
@cqrs { "kind": "query" }
@read_model { "name": "CustomerSummary" }
```

## Rules
- JSON must be valid
- Use nested JSON only
