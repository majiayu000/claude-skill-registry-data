---
name: data-in-transit-review
description: Review a repository or local folder with a focus on how data moves between components, services, users, and external systems. Use when Codex needs to inspect APIs, message flows, webhooks, queues, events, file transfers, network boundaries, encryption in transit, transport protocols, or trust assumptions around data movement.
---

# Data In Transit Review

## Overview

Use this skill to build a focused, evidence-based review of how a codebase sends, receives, forwards, transforms, and protects data while it is moving between systems or components. Trace where data enters, where it leaves, how it is carried, and which boundaries or intermediaries are trusted along the way.

Prefer one concrete flow or integration over a broad but shallow survey. Make uncertainty explicit and label inferred edges clearly.

## Workflow

### 1. Establish the review scope

Choose the smallest meaningful transit slice before reading everything.

Start with:

- the README and architecture docs
- dependency manifests and framework config
- obvious transport entrypoints such as routes, handlers, controllers, webhooks, queue consumers, publishers, API clients, SDK wrappers, file transfer jobs, or streaming pipelines

If the folder or codebase is large, choose one of these scopes and say which one you chose:

- one request and response path
- one external integration
- one async message or event flow
- one file transfer or export path

### 2. Identify transit boundaries

Identify the main paths where data crosses boundaries:

- client-to-server and server-to-server APIs
- internal service calls and RPC boundaries
- message queues, event buses, streams, and background workers
- webhooks, callbacks, and third-party integrations
- file uploads, downloads, sync jobs, and bulk exports
- proxies, gateways, load balancers, service meshes, and other intermediaries

Also capture the transport assumptions:

- HTTP, HTTPS, WebSocket, gRPC, AMQP, Kafka, S3-style transfer, SMTP, FTP, or custom protocols
- encryption in transit, signing, integrity checks, replay protections, and retry behavior
- metadata carriers such as headers, claims, correlation IDs, tenant IDs, or auth context

Prefer code search over assumptions. Follow concrete route registration, client initialization, publisher setup, and callback wiring.

### 3. Trace the primary transit path

Trace data from the first inbound edge to the next boundary crossing or final outbound destination. Look for:

- where input is received and parsed
- validation, canonicalization, and schema checks
- transformation, enrichment, batching, or serialization
- routing, forwarding, publishing, or upload behavior
- retries, deduplication, ordering, backpressure, or timeout handling
- response handling, acknowledgements, and downstream propagation
- logging, tracing, or metrics that expose payload or metadata

Capture where trust changes, where data is re-encoded, and where sensitive fields may be exposed.

### 4. Review the key functions

For every important function in the chosen flow, review the function instead of only naming it. Capture:

- file path
- function or method name
- role in the transit flow
- direct callers and important callees, if visible
- expected inputs
- emitted, forwarded, or received data
- validation, normalization, or integrity checks performed
- side effects and downstream dependencies
- failure modes, retry assumptions, and security concerns

Prioritize functions that:

- receive untrusted network or file-transfer input
- build outbound requests, messages, or payloads
- attach auth, tenant, or correlation metadata
- serialize or deserialize structured data
- handle retries, dead letters, or fallback paths
- trust upstream headers or downstream acknowledgements

### 5. Surface transit findings

Call out issues that materially affect how much the transport design can be trusted, especially:

- missing validation at ingress or egress boundaries
- disabled TLS, weak certificate handling, or unclear trust of intermediaries
- missing integrity checks, signatures, nonce, replay, or ordering protections
- sensitive data sent in plaintext, logs, headers, URLs, or weakly protected metadata
- surprising fan-out, hidden forwarding, or side-channel copies
- weak timeout, retry, or deduplication behavior that can cause duplication or loss
- excessive trust in upstream headers, callback payloads, or internal network location
- transport paths that bypass expected gateways, policies, or observability
- bulk export, sync, or webhook paths that are easy to overlook

Separate confirmed findings from open questions.

### 6. Deliver a concise report

Default to this structure:

1. Scope reviewed
2. High-level data-in-transit flow
3. Step-by-step function review
4. Findings and open questions

## Search Strategy

Use fast repository discovery first:

- `rg --files` for project shape
- `rg` for transit signals such as `route`, `handler`, `controller`, `request`, `response`, `client`, `fetch`, `axios`, `requests`, `http`, `grpc`, `webhook`, `callback`, `publish`, `consume`, `queue`, `topic`, `stream`, `kafka`, `rabbit`, `upload`, `download`, `send`, `receive`, `headers`, `tls`, `ssl`, `proxy`
- framework-specific files such as `routes`, `controllers`, `handlers`, `clients`, `transport`, `gateway`, `middleware`, `consumers`, `publishers`, `workers`, `webhooks`

Prioritize these signals:

- files where data first enters from outside the trust boundary
- functions that build or send outbound payloads
- code that bridges one transport or trust domain to another
- code that handles sensitive, high-volume, or cross-tenant traffic

## Output Rules

Be explicit about evidence quality:

- say `confirmed` when the code directly shows the path
- say `inferred` when the path is likely but not fully wired in the inspected files
- say `not verified` when an external service, managed transport, proxy, or generated layer is missing

Do not present storage-only concerns as transit findings unless they materially affect movement, confidentiality, integrity, or availability while data is in motion.

When presenting the flow, prefer real functions and files over generic labels like "integration layer".

## Example Requests

- Review this repo and explain how customer data moves from API request to downstream services.
- Inspect this codebase and map the webhook ingestion and forwarding path.
- Review this folder with a focus on queue, event, and retry behavior.
- Trace file upload and export flows here and call out transport or trust-boundary risks.
