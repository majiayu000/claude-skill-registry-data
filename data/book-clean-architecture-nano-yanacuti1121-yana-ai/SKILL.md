---
name: book--clean-architecture--nano
description: >-
  Clean Architecture (Robert C. Martin) — Minimal rules — essential one-liners only. Use when asked to apply Clean Architecture principles or review code against Clean Architecture standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Clean Architecture by Robert C. Martin

## When to use

Use when tight context still needs to prevent framework-first design, database-shaped policy, layer bypass, or fake boundaries.

## Primary bias to correct

Details are plugins to policy, not the center of the design.

## Decision rules

- Source dependencies point inward. Domain and use cases must not import frameworks, databases, web, UI, queues, service clients, device, vendor, or infrastructure details.
- Entities guard enterprise invariants; focused use cases orchestrate application actions with plain input and output models.
- Frameworks, databases, web delivery, messaging, filesystems, clocks, networks, services, and hardware sit behind policy-owned ports and outer-layer adapters.
- Controllers, presenters, gateways, service listeners, mappers, and hardware adapters translate; they do not own business rules.
- Organize by use case, feature, or business capability. Avoid generic technical buckets, god services, shared utility escape hatches, and sideways coupling.
- Choose the lightest enforceable boundary that preserves likely change independence; a service, package, diagram, or folder name is not enough.
- Test policy through entities, use cases, and boundary contracts without real frameworks, databases, networks, services, or hardware.

## Trigger rules

- When framework, ORM, request, response, schema, transport, config, vendor, or hardware types enter core policy, move translation outward.
- When controllers, jobs, handlers, gateways, repositories, SQL, presenters, service listeners, or `*Service` classes grow business rules, move policy inward and split by use case.
- When core code constructs or calls volatile details directly, define an inward-owned port and wire the concrete implementation at the edge.
- When a shortcut bypasses a use case, crosses layers, creates a cycle, or hides coupling in `common` or `utils`, restore dependency direction and ownership.
- When constraints force a compromise, keep it outermost, name the violation, and preserve a future path to separation.

## Final checklist

- Policy independent of details?
- Dependencies inward?
- Use cases visible?
- Adapters humble?
- Boundaries enforced?
- Core tests detail-free?
