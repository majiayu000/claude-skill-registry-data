---
name: backend-engineering
description: Use this skill whenever you are building the server side of an app — the endpoint, the handler, the mutation behind a form, the thing that runs after the request. Trigger on "build the API", "write this endpoint", "add a route handler", "make this a Server Action", "where does the business logic go", "process this in the background", "add a queue / worker / cron / scheduled job", "handle this webhook", "call this third-party API reliably", "make this idempotent", "why is my mutation firing twice", "this needs to be async", "should this be an edge function", or any request to persist, validate, or side-effect against untrusted input on a server. Fires even when the user never says the word "backend" — a form that writes to a DB, a payment side-effect, an email send, a Stripe/Slack/GitHub webhook receiver all count. It owns the IMPLEMENTATION behind a contract, not the contract itself. It does NOT design the wire contract (that is `api-and-interface-design`), design the schema (`database-schema-designer`), write the client fetch layer (`api-communication`), or own auth policy (`auth-and-authorization`) — it routes to those and builds the server logic that sits behind them.
---

# Backend Engineering

Backend-engineering builds the **server side** — the code that runs after a request crosses a trust boundary. It sits behind the contract that `api-and-interface-design` defines and in front of the schema `database-schema-designer` designs: given an approved shape, it decides *which server surface* runs the logic, *how the logic is layered*, *how input is validated and errors are shaped*, *what runs async*, and *how side effects stay idempotent and observable*.

**Cardinal rule — validate at every trust boundary, keep handlers thin, make every side effect idempotent and observable.** Three inseparable clauses: (1) nothing crossing a boundary is trusted until it is *parsed* into a typed value (parse, don't validate); (2) the handler is a controller — it wires request→service→response and holds **zero** business logic; the logic lives in a testable service layer with no framework types in its signature; (3) any operation that charges a card, sends an email, mutates a row, or calls a third party must be safe to retry (idempotency key + at-least-once thinking) and must emit a trace/log/metric so you can see it in production. A backend you cannot replay safely and cannot see is a liability, not a feature.

**Second rule — build the lightest server that fits.** A Server Action beats a Route Handler beats a standalone service beats a queue — until the load, the boundary, or the failure mode demands the next rung. Do not stand up a NestJS microservice and a Kafka topic for a contact form. See the "when NOT to build a backend" table below.

---

## Sections

```
0. ROUTE      → classify the request; pick the section(s) that apply
1. SURFACE    → Route Handler vs Server Action vs standalone service vs edge
2. STRUCTURE  → thin controller → service → repository; where validation/auth/tx live
3. IMPLEMENT  → validate at the boundary (Zod) + a typed error taxonomy + safe error shapes
4. ASYNC      → jobs / queues / cron: when to go async, idempotency, retries, outbox
5. INTEGRATE  → webhooks in (verify + idempotent + fast-ack) and calls out (timeout/retry/breaker)
6. VERIFY     → hand off to the pipeline; nothing ships unproven
```

Move through only the sections the request touches. A single new endpoint is SURFACE→STRUCTURE→IMPLEMENT→VERIFY. "Process uploads in the background" is ASYNC. "Receive Stripe events" is INTEGRATE (and cross-links out — see below).

---

## Section 0 — ROUTE

Decide what the request actually needs before writing a line:

- "Write / build this endpoint or handler", "add an API route" → **SURFACE** then **STRUCTURE** + **IMPLEMENT**
- "Where does the business logic go", "this handler is 300 lines" → **STRUCTURE**
- "Validate this input", "shape the errors", "stop leaking stack traces" → **IMPLEMENT**
- "Do this in the background", "queue", "cron", "retry", "this is slow / times out" → **ASYNC**
- "Handle this webhook", "call this third-party reliably", "it fired twice" → **INTEGRATE**
- Ambiguous or greenfield service → SURFACE first; it decides whether a backend is even warranted.

If the request is really about the *wire contract* (status codes, pagination shape, versioning), that is `api-and-interface-design` — route there first, then come back to implement behind it.

---

## Section 1 — SURFACE (which server runs this)

Read `references/server-layer.md`. Pick the **lightest surface that fits** the mutation and its constraints:

| Signal | Surface |
|---|---|
| Form/mutation from your own Next.js UI, no public contract | **Server Action** (`"use server"`) — progressive enhancement, typed end to end |
| Called by third parties / mobile / webhooks / needs a stable URL + verb + status | **Route Handler** (`app/api/.../route.ts`) or a Hono/Fastify router |
| Read for a page | **RSC data access** directly in the Server Component — no endpoint at all |
| Heavy CPU, long-lived connections, own deploy/scaling, non-Vercel runtime | **standalone Node service** (Hono / Fastify / NestJS) — or **Go** for throughput-heavy or latency-critical services |
| Geo-distributed, tiny, no Node APIs (auth check, redirect, A/B) | **edge function / middleware** |

Server Actions and Route Handlers are the primary surface on the house stack (Next.js 15 App Router + RSC, Vercel-first); reach for a standalone service only when the platform boundary actually demands it. Whichever you pick, the layering below is identical.

---

## Section 2 — STRUCTURE (thin controller → service → repository)

Read `references/server-layer.md` (layering section). The handler is a **controller**: parse input, call one service function, map the result to a response. That is all it does. Business logic lives in a **service** whose signature speaks your domain types — no `Request`, `Response`, `NextRequest`, or `headers()` in it, so it is unit-testable without a server. Data access lives in a **repository** so the service does not know Drizzle from Prisma from `fetch`. Transactions and authorization checks live in the service (at the top of the operation), not sprinkled in the controller. This is "dependency-injection lite": pass collaborators in, don't import singletons deep in the tree. Placement of these files/folders is `arch`'s call — hand structure questions there.

---

## Section 3 — IMPLEMENT (validation + errors)

Read `references/validation-and-errors.md`. At **every** boundary — request body, query params, headers, env, third-party responses, queue payloads — run the bytes through a **Zod** (or valibot) schema and work only with the parsed, typed result. Never validate-then-use-the-raw-object. Build a **typed error taxonomy**: domain errors (expected — `NotFound`, `Forbidden`, `Conflict`, `ValidationError`) that map cleanly to HTTP status and a safe client shape, versus unexpected errors (bugs, dependency failures) that become a 500 with a correlation id and *nothing else*. Never let a stack trace, SQL string, or internal path reach the client. Enforce input size limits. Prefer a `Result` type (neverthrow) for expected failures and reserve `throw` for the truly exceptional — but be consistent within a codebase.

---

## Section 4 — ASYNC (jobs, queues, scheduling)

Read `references/jobs-and-scheduling.md`. Go async when work is slow, retryable, or can outlive the request (emails, image processing, third-party fan-out, report generation). Do **not** block an HTTP response on it. Pick the lightest queue: **Inngest** or **Trigger.dev** (durable steps, great on Vercel), **QStash** (HTTP-based, serverless-native), **BullMQ + Redis** (self-hosted control), **Vercel Cron / QStash schedules** for scheduled work. Every job needs an **idempotency key** (so a retry doesn't double-charge), **exponential backoff + a dead-letter queue**, and honest thinking about **at-least-once** delivery (exactly-once is mostly a myth — design consumers to be idempotent instead). Scheduled jobs need an **overlapping-run lock**. When a state change must reliably produce an event, use the **transactional outbox** (write the row and the outbox entry in one transaction; a relay publishes it).

---

## Section 5 — INTEGRATE (webhooks in, calls out)

Read `references/webhooks-and-integration.md`. **Receiving** a webhook: verify the signature (HMAC over the *raw* body — do not parse first), enforce a timestamp/replay window, dedupe on the provider's event id (idempotent processing), then **fast-ack with 2xx and process asynchronously** — never do slow work before returning, or the sender retries and you double-process. **Calling out**: every outbound call gets a timeout, bounded retries with backoff on idempotent operations, a circuit breaker for a failing dependency, and explicit rate-limit (429 / `Retry-After`) handling. Reliable *outbound* events use the outbox from Section 4. Note: **Stripe** webhooks specifically are owned by `stripe-integration-expert` — cross-link to it for billing/signature specifics rather than duplicating; this skill covers the general webhook mechanics.

---

## Orchestration

Backend-engineering owns the server *implementation*; it delegates everything around it. Route skill selection through **`decider`** (this repo's standard router — pass it the situation, stage, and tasks) and slot into the house pipeline **`PLAN → EXECUTE → [SECURE/A11Y/PERF] → REVIEW → TEST → VERIFY`**. This skill owns PLAN/EXECUTE for server logic; the closing gates are mandatory.

- Wire **contract** (routes, verbs, status codes, pagination, versioning, error shape) → **`api-and-interface-design`** *(it owns the contract; this skill owns the implementation behind it)*
- Database **schema**, migrations, indexes, RLS → **`database-schema-designer`**
- Client **data-fetching** layer (typed HTTP client, TanStack Query, token refresh) → **`api-communication`**
- **Auth** policy — sessions, tokens, RBAC/ABAC, who-can-do-what → **`auth-and-authorization`**
- **Telemetry** — tracing, metrics, structured logs, SLOs → **`observability-and-monitoring`**
- **Deploy / containers / IaC** — Dockerfile, runtime, infra → **`containerization-and-iac`**
- Code **placement / folder structure** for the new server files → **`arch`**
- Secrets / env hygiene → **`env-secrets-manager`**; **SECURE gate** → **`security-and-hardening`** (see below)
- REVIEW → **`code-review`**; TEST → **`test-driven-development`** / **`qa-tester`**; VERIFY → **`verify`**; deep debugging of a failing side effect → **`systematic-debugging`**; performance of a hot path → **`performance-optimization`**

**The SECURE gate is MANDATORY** — not optional — whenever the surface handles untrusted input, money, PII, or an irreversible action (which is nearly every backend). Run **`security-and-hardening`** before REVIEW; for a deeper audit, the security-officer agent signs off Critical/High findings. Reviewer agents that fit backend surfaces: the **api-platform-reviewer** (rate limits, webhook signing, idempotency, versioning), **db-migration-reviewer** (migration safety, rollback), **streaming-reviewer** (exactly-once, DLQ, backpressure for event-driven work), **infra-reviewer** (IaC/destructive-change safety), and **enterprise-saas-reviewer** (multi-tenant isolation). Read a chosen skill's own SKILL.md before running it.

---

## Enforcement over vibes

"Validate the input" and "keep handlers thin" are prose that drifts. Make them *fail the build*: every boundary parse is a Zod schema whose inferred type is the only type the service accepts (so an unvalidated object is a type error); a lint rule (or a dependency-cruiser boundary) forbids importing `next/server` / `Request` from the service layer (so business logic can't leak into a controller); env is parsed by a Zod schema at boot so a missing var crashes on start, not at 3am; idempotency keys are a required parameter, not a convention. An invariant without machine enforcement is a suggestion — emit the schema, the lint rule, the CI gate.

---

## Operating principles

- **Parse, don't validate.** Untrusted bytes become a typed value at the boundary or they don't enter. No raw request objects past the controller.
- **Thin handler, fat service.** Framework types stop at the controller. The service is plain functions over domain types — unit-testable without a server.
- **Idempotent by default.** Every side effect must be safe to retry. Assume at-least-once delivery everywhere; make consumers idempotent instead of chasing exactly-once.
- **Observable by default.** Every side-effecting path emits a trace/log/metric with a correlation id. If you can't see it in prod, it's broken and you don't know yet.
- **Lightest surface that fits.** Server Action → Route Handler → standalone service → queue. Climb only when load/boundary/failure-mode forces it.
- **Never leak internals.** Domain errors get a safe shape + status; unexpected errors get a 500 + correlation id and nothing else.
- **Delegate the edges.** Contract → `api-and-interface-design`; schema → `database-schema-designer`; auth → `auth-and-authorization`; structure → `arch`. This skill builds the middle.
- **Secure is not optional** on money/PII/untrusted-input/irreversible surfaces. Run the SECURE gate.
- **Match the user's language** (Russian, Uzbek, English).
- **Web-first, stack-aware.** Defaults tuned to Next.js 15 App Router + RSC + TypeScript strict + Vercel; Hono/Fastify/NestJS and Go covered when the platform boundary demands a standalone service.

---

## When NOT to build a backend (the lightest-thing table)

| The need | Don't build | Do this instead |
|---|---|---|
| Read data for a page | An API endpoint + client fetch | Query the DB directly in a **RSC** |
| Submit a form from your own UI | A REST endpoint + client `fetch` | A **Server Action** |
| A cheap auth check / redirect at the edge | A Node service | **Middleware / edge function** |
| One scheduled cleanup a day | A worker fleet | **Vercel Cron** hitting a Route Handler |
| A few background emails | Kafka + a consumer group | **Inngest / QStash** |
| Real event-driven scale, many consumers, ordering | Ad-hoc `setTimeout` | A real queue (**BullMQ/Kafka**) — now it's warranted |

The rung climbs only when the previous one actually breaks. Over-engineering a backend is as much a defect as under-engineering one.

---

## Worked examples (abbreviated)

**"Add an endpoint that creates an order and emails a receipt."**
ROUTE → SURFACE: it's called from our own checkout UI → **Server Action** (or Route Handler if mobile also calls it). STRUCTURE: `createOrder(input)` service; controller just parses + calls it. IMPLEMENT: Zod-parse the cart; domain errors `OutOfStock`/`PaymentDeclined` → typed 409/402; unexpected → 500 + correlation id. ASYNC: the receipt email does **not** block the response — enqueue an Inngest job with the order id as idempotency key. SECURE gate (money + PII) is mandatory → `security-and-hardening`. Then REVIEW→TEST→VERIFY.

**"We're getting duplicate charges when the webhook retries."**
ROUTE → INTEGRATE. Classic at-least-once: the sender retried because you did slow work before acking. Fix: verify HMAC on the raw body, dedupe on the provider event id (insert-if-not-exists), **return 2xx immediately**, process in a job. Charge logic keyed by event id so a replay is a no-op. If it's Stripe specifically, cross-link `stripe-integration-expert`. Hand the delivery-guarantee sign-off to the streaming-reviewer or api-platform-reviewer agent.

**"This report generation times out the request."**
ROUTE → ASYNC. Don't optimize the request — move it off it. Enqueue a job (Trigger.dev/Inngest), return `202` + a job id, let the client poll or subscribe. Job is idempotent on the report id, has backoff + a DLQ, and emits a trace. If the compute itself is the bottleneck, loop in `performance-optimization`.
