---
name: serverless-architecture
description: "Serverless is a billing-and-scaling model, not a badge of modernity."
---

# Serverless Architecture (Verbose)

## Core Patterns

### When Serverless Wins and When It Loses

Serverless is a billing-and-scaling model, not a badge of modernity. The decision
turns almost entirely on the shape of your load.

| Load shape | Serverless (FaaS) | Always-on container / VM |
|---|---|---|
| Spiky, unpredictable | Excellent — scales instantly, idle costs ~nothing | Wasteful — provisioned for a peak that is rare |
| Low or zero baseline | Excellent — scale-to-zero | Wasteful — paying to sit idle |
| Event-driven / glue | Excellent — natural fit | Awkward — a service babysitting a queue |
| Steady, high throughput | Poor — per-invocation cost adds up, cold starts hurt | Excellent — near-capacity utilization is cheap |
| Latency-critical, tight p99 | Risky — cold starts add tail latency | Predictable — warm process always ready |
| Long-running jobs | Poor — invocation timeout | Fine — no artificial ceiling |

The classic mistake is porting a steady, high-QPS API to functions to "be
serverless" and being surprised by both the bill and the tail latency. The
inverse mistake is running a cron job or a webhook receiver on an always-on
fleet, paying 24/7 for seconds of work per day.

A useful crossover intuition: below some steady request rate, per-invocation
billing is cheaper; above it, reserved always-on compute wins. You do not need
the exact number — you need to know which side of it your workload sits on, and
that it moves as traffic grows.

### Statelessness and the Execution Lifecycle

A function instance is created, may serve one or many invocations, is frozen
between them, and is eventually destroyed — all outside your control. Two
consequences drive the design:

- **No durable local state.** Anything written to memory or local disk may vanish
  before the next call and is never shared across concurrent instances. Persist
  state in a managed database or cache (managed-database-selection,
  distributed-caching-design).
- **Initialization is reused when warm.** Code outside the handler runs once per
  instance, not once per request. Put expensive one-time setup — SDK clients,
  DB connection pools, config loads — there, so warm invocations skip it.

```python
# module scope: runs at cold start, reused across warm invocations
db = connect_pool()          # do this ONCE per instance
client = StorageClient()

def handler(event, context):
    # per-request work only; keep this path lean
    return process(event, db, client)
```

Every platform imposes a per-invocation timeout you must design around. Work that
cannot finish inside it must be decomposed into steps or handed to a batch/queue
system — never assume you can raise the ceiling far enough.

### Cold Starts

A cold start is the time to provision a runtime, load your code, and run
initialization before the first request is served. It is paid whenever the
platform adds an instance — the first request after idle, and every request that
scales the fleet up.

Drivers and mitigations:

- **Package size / dependency weight** → trim dependencies, avoid pulling entire
  SDKs when a submodule will do.
- **Heavy init** → move it to module scope so it amortizes across warm calls;
  lazy-load anything not needed on every path.
- **Runtime choice** → interpreted/lightweight runtimes generally start faster
  than heavy JVM-style ones.
- **VPC / private-network attachment** → historically adds startup cost; keep
  functions out of a VPC unless they need private resources.
- **Latency-critical paths** → use provisioned/warmed concurrency to keep
  instances hot, accepting that it reintroduces an always-on cost.

Load-test the scale-from-zero and scale-up paths explicitly (see load-testing).
Cold starts are invisible in steady-state testing and then surface as p99 spikes
in production.

### Event-Driven Composition

Serverless systems are wired together by events, not by services calling each
other directly:

```
S3 object created ─▶ Lambda (thumbnail)  ─▶ writes derived object
API Gateway  ─▶ Lambda (handler) ─▶ SQS ─▶ Lambda (worker) ─▶ DynamoDB
EventBridge schedule ─▶ Lambda (nightly rollup)
```

Keep each function single-purpose and let a queue or pub/sub topic sit between
producers and consumers. That decouples them, absorbs bursts, and gives you a
natural retry and dead-letter boundary. Fan-out (one event, many independent
consumers) is done with a topic, not by one function invoking several others.

### Orchestrating Multi-Step Workflows

Chaining functions by direct synchronous invocation is an anti-pattern: the
caller is billed while it blocks waiting for the callee, and their timeouts
become coupled — the outer function can time out mid-way, leaving partial work.

Use a managed orchestrator for anything with steps, branching, or retries:

- **AWS Step Functions** — a JSON/ASL state machine with built-in retry,
  catch, parallel, and wait states.
- **Google Cloud Workflows** / **Azure Durable Functions** — equivalents.

The orchestrator owns the state and progress; each function stays a small,
stateless step. For high fan-out or buffering, prefer an asynchronous queue
between steps over a synchronous chain.

### Idempotency and Failure Handling

Event sources and queues generally guarantee at-least-once delivery, so any
handler can run more than once on the same message — after a retry, a
redelivery, or a duplicate publish. Handlers must be idempotent: processing the
same event twice must not double-charge, double-send, or corrupt state (see
idempotency-patterns for keys and dedup tables).

Wire a dead-letter queue on every asynchronous source so that a message which
keeps failing is parked for inspection instead of retried forever or dropped
silently. Emit structured logs and traces per invocation — distributed tracing
across function boundaries is how you reconstruct an event's path.

## Common Anti-Patterns

❌ **Porting a steady high-QPS service to FaaS to "be serverless".**
✅ Match the model to the load shape — always-on compute for steady throughput,
serverless for spiky or event-driven work.

❌ **Storing state in a function's local memory or disk** and expecting it next
time.
✅ Externalize all state to a managed store; treat every invocation as fresh.

❌ **One function synchronously invoking the next, several deep.**
✅ Use a workflow orchestrator, or decouple steps with a queue or topic.

❌ **Non-idempotent handlers on an at-least-once source.**
✅ Make every handler idempotent and add a dead-letter queue for poison messages.

❌ **Ignoring cold starts until production.**
✅ Trim packages, keep init out of the hot path, load-test scale-from-zero, and
use provisioned concurrency where tail latency matters.

❌ **A long-running job fighting the invocation timeout.**
✅ Decompose it into steps under an orchestrator, or move it to a batch service.

❌ **Putting a function in a VPC by reflex.**
✅ Attach to private networking only when it needs a private resource; accept the
startup cost knowingly.

## Serverless Architecture Checklist

- [ ] Load shape confirmed to favour serverless (spiky / low-baseline / event-driven)
- [ ] All durable state externalized to a managed store
- [ ] Expensive initialization moved to module scope, reused across warm calls
- [ ] Work fits inside the invocation timeout, or is decomposed
- [ ] Cold-start budget understood; scale-from-zero load-tested
- [ ] Provisioned concurrency used only where tail latency demands it
- [ ] Functions single-purpose, composed via events and queues/topics
- [ ] Multi-step flows run under an orchestrator, not synchronous chains
- [ ] Handlers idempotent against at-least-once delivery
- [ ] Dead-letter queues on every asynchronous source
- [ ] Structured logs and distributed tracing across function boundaries
- [ ] Cost modeled against an always-on alternative at expected steady load
