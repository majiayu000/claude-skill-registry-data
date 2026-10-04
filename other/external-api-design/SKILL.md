---
name: external-api-design
kind: skill
status: ready
provenance:
  principles:
  - P019
  - P012
  - P052
  - P125
  - P108
  - P041
  - P057
  claims:
  - C00326
  - C00327
  - C00019
  - C00344
  - C00335
  - C00337
  - C00336
  - C00340
  - C00351
  - C00352
  - C00144
  - C00145
  source_anchors: []
  authored_from_digest: f48791f1431d371ec11fbc0316736a716b5f07c9d3fbd4ed2b258e20ef4f5875
---

# External API Design

## Purpose

Guide a caller designing how external clients reach the services, how caller identity
is handled at the edge, and how the external API evolves. This is the specialised
walkthrough for the **External API** group.

## When to use

Use when external or multiple client types (web, mobile, third-party) consume the
services, when edge authentication must be designed, or when the external API must
change without breaking clients. Do not use for purely internal service-to-service
traffic (route to `interservice-communication-selection`).

## Procedure

1. **Do not let external clients call services directly.** Fine-grained service APIs
   force chatty, battery-draining, high-latency interactions, break encapsulation, and
   expose client-unfriendly protocols; a single one-size-fits-all API rarely fits, and
   slow-to-update mobile apps bake in service knowledge that obstructs API change
   (C00326, C00327, P019). Front external clients with an API gateway or Backends for
   frontends (C00019, P125).

2. **Implement the gateway deliberately.** Use an off-the-shelf product (little
   effort, least flexible, often no API composition) or build on a gateway framework;
   require routing on method, headers, and path (not path-only, which cannot serve a
   CQRS command/query split), and write composition handlers in a reactive style that
   invokes services in parallel and degrades gracefully by treating non-essential
   providers as optional (C00344, P012).

3. **Give each client type its own API; prefer BFF.** Provide each client type a
   client-specific API rather than one shared API, and prefer Backends for frontends —
   a gateway per client type owned by that client's team, with an API-gateway team
   owning the shared common layer — for clear ownership, fault isolation, independent
   scalability, and to avoid a central development bottleneck (C00335, C00337, P052).

4. **Implement edge functions at the gateway.** Authentication, authorization, rate
   limiting, caching, metrics, and request logging belong at the edge before requests
   reach the services; authenticate at the edge for security and prefer in-gateway
   placement to avoid an extra network hop, and choose the gateway's I/O model
   (thread-per-connection is simple but limited; non-blocking event-loop I/O scales
   far better for I/O-intensive routing) (C00336, C00340, P108).

5. **Consider a graph-based API for diverse clients.** GraphQL's typed schema and
   resolvers let a client fetch exactly the data it needs in one round-trip (the engine
   performs API composition by recursively invoking resolvers), reducing per-client
   effort; optimise resolvers with per-request server-side batching and caching to
   avoid the N+1 problem (C00351, C00352, P041).

6. **Manage API evolution.** Use semantic versioning, prefer backward-compatible
   additive changes, follow the Robustness principle (default missing request
   attributes, ignore unknown response attributes), and for unavoidable breaking
   changes run old and new versions in parallel for a transition period, because
   clients cannot be forced to upgrade in lockstep (C00144, C00145, P057).

7. **Hand off.** The architecture owner decides and implements; this skill informs.

## Inputs

- **Required:** the external client types, the APIs they need, the edge
  authentication/authorisation requirements, and any API-evolution constraints.

## Output

A recommended edge design: an API gateway (or per-client BFFs) with its routing /
composition responsibilities, an edge-authentication approach, an optional
graph-based API where clients are diverse, and an API-evolution / versioning plan —
each tied to the caller's forces.

## References

- `references/microservice-pattern-language-map.md` — the External API and Security
  patterns.

## Provenance

Tier 2. Grounded in principles P019 (design the external API for clients), P012
(implement the API gateway), P052 (client-specific APIs / BFF), P125 (expose via
gateway/BFF), P108 (edge functions), P041 (graph-based API), and P057 (API
evolution), from `chris-richardson-mic-19016f24` (Microservices Patterns, Chris
Richardson, Manning 2018, `distillation-only`). No verbatim quotation.
