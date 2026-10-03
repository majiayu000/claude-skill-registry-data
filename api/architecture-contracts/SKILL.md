---
name: architecture-contracts
description: Route durable architecture decisions and consumer-facing interface contract reviews; not for implementation sequencing, data analysis, or release execution.
---

# Architecture Contracts

Choose one primary mode and read only its workflow. Use both only when an architecture decision and its external contract must be evaluated together.

| Mode | Use when | Workflow |
| --- | --- | --- |
| `architecture-decision-records` | Record an architectural choice, alternatives, consequences, reversibility, or migration. | [Architecture decision records](references/workflows/architecture-decision-records.md) |
| `api-contract-review` | Review API, RPC, SDK, event, webhook, schema, versioning, or compatibility promises. | [API contract review](references/workflows/api-contract-review.md) |

Do not load sibling workflows or artifacts prospectively. Do not approve breaking or irreversible choices when consumers, authority, or migration constraints remain unknown.
