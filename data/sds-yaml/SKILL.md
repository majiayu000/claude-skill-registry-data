---
name: sds-yaml
description: Create machine-readable SDS YAML that maps cleanly to SEA™ DSL.
---

# SDS YAML authoring


## Required fields
- `sdsId: SDS-###`
- `boundedContext: <ctx>`
- `satisfiesPrds: [...]`
- `satisfiesAdrs: [...]`

## Recommended sections
- `domain.entities[]`
- `domain.valueObjects[]`
- `cqrs.commands[]`
- `cqrs.events[]`
- `cqrs.queries[]`
- `useCases[]`
- `ports.inbound[]`
- `ports.outbound[]`
- `adapters[]`
- `uow` (transaction boundary policy)
- `messageBus` (routing, retry, outbox)

## Mapping hint
Every command/query/event should correspond to a SEA™ `Flow` with `@cqrs`.
