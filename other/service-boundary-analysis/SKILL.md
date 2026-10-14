---
name: service-boundary-analysis
description: "Trigger: service boundary analysis, microservice inputs/outputs, API/consumer/output mapping. Map one backend boundary with evidence and confidence."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "2.0.0"
---

# Service Boundary Analysis

## Contract

Statically inspect one backend service, module, worker, or API. Identify inputs and externally visible outputs. No execution, edits, security review, schema design, or certainty for dynamic wiring.

Require exact target, scope, exclusions, report path. Multi-service workspaces get one report per service.

## Taxonomy

Inputs: HTTP/API, RPC, messages/streams, WebSocket/SSE, scheduled jobs, CLI/batch/workers, file/object triggers, config loading.

Outputs: database writes, external calls, event publishing, cache changes, file/object writes, search/vector writes, notifications, job scheduling, boundary-relevant telemetry. Ignore local debug logs.

## Evidence

Use routes, annotations, registrations, imports, handlers, clients, repositories, publishers, schedulers, config, healthy graph edges. Trace cross-file wiring before relying on names.

- `high`: direct mechanism and peer/destination evidence.
- `medium`: corroborated registration, convention, or cross-file wiring.
- `low`: plausible, incomplete, or dynamic.

Each row includes `file:line`, symbol when available, discovery method. Put unresolved reflection, generation, missing config, or indirection under `Uncertain`; never inflate confidence.

## Flow

1. Detect language/framework from manifests, target files.
2. Find input registrations, handlers.
3. Find output clients, side effects.
4. Trace each candidate to peer/destination.
5. Group repeated equivalent boundaries.
6. Write one compact report.

## Output

```markdown
# Service Boundary Report

## Scope
<target, inspected paths, exclusions>

## Inputs
| Category | Mechanism | Source/peer | Evidence | Confidence | Notes |
|---|---|---|---|---|---|

## Outputs
| Category | Mechanism | Destination | Evidence | Confidence | Notes |
|---|---|---|---|---|---|

## Uncertain
- <finding, evidence, limit>

## Limitations
- <uninspected or runtime-only behavior>
```

Keep mandatory tables when empty; use `No evidence found in inspected scope.` instead of placeholder rows. Omit empty `Uncertain` and `Limitations` sections.
