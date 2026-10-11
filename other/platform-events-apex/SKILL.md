---
name: platform-events-apex
description: "Use when publishing or subscribing to Salesforce Platform Events from Apex, comparing Platform Events with Change Data Capture, or designing event-triggered error handling and monitoring. Triggers: 'EventBus.publish', 'platform event trigger', 'CDC vs Platform Events', 'replay ID', 'high-volume event'. NOT for Flow-only publish/subscribe automation."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Scalability
  - Reliability
tags:
  - platform-events
  - eventbus
  - cdc
  - replay-id
  - event-trigger
triggers:
  - "how do I publish platform events from Apex"
  - "CDC vs platform events for integration"
  - "platform event trigger subscriber pattern"
  - "EventBus publish results handling"
  - "replay ID management for event consumers"
inputs:
  - "publisher or subscriber use case and event volume"
  - "whether consumers are Apex triggers, external subscribers, or both"
  - "failure handling and retry expectations"
outputs:
  - "event architecture recommendation"
  - "review findings for publication, subscription, and monitoring risks"
  - "Apex publish and subscribe pattern with error handling"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

Use this skill when a design is moving toward event-driven integration and Apex is involved on the publishing or subscriber side. The goal is to publish events deliberately, consume them in a decoupled way, and separate Platform Events from Change Data Capture instead of treating them as interchangeable.

## Before Starting

- Is the system broadcasting a business event it owns, or mirroring a record change that Salesforce owns already?
- Will the subscriber be Apex, Flow, middleware, Pub/Sub API, or a mix?
- Do you need eventual consistency, replay handling for external consumers, or immediate transaction-level validation?

## Core Concepts

### Platform Events Are Explicit Business Messages

Platform Events are event records designed for decoupled publication and subscription. In Apex, publishers create event instances and call `EventBus.publish`. That is different from CDC, where Salesforce emits change events when records mutate. Use Platform Events when you want to define the payload and timing of the message instead of mirroring all record changes automatically.

### Publication Success Is Not “No Exception Thrown”

Publishing can be done for one event or a list, and the return value matters. `EventBus.publish` can return `Database.SaveResult` style results that tell you whether publication succeeded. Production code should inspect those results or otherwise classify failures. Treating event publication as fire-and-forget with no result handling is an observability gap.

### Subscriber Shape Depends On The Consumer

Apex platform event triggers subscribe asynchronously and run only in an `after insert` context. External consumers using Streaming or Pub/Sub APIs care about replay positions and subscriber durability. Replay ID management is not an Apex-trigger concern, but it is part of the architecture whenever middleware or external apps must recover missed events.

### CDC Solves A Different Problem

Change Data Capture is best when the event should represent Salesforce row changes. Platform Events are better when the event is a business fact or orchestration signal such as “Order Approved” or “Invoice Sync Requested.” Mixing these without a decision rule creates noisy payloads and unclear ownership.

## Common Patterns

### Publish Via A Service Boundary

**When to use:** Business logic has decided that an event should be emitted.

**How it works:** Build the event payload in a service class, publish a list where possible, and inspect results for failure logging.

**Why not the alternative:** Inline event creation inside many triggers or controllers duplicates payload rules and weakens monitoring.

### Event Trigger To Queueable Worker

**When to use:** Subscriber logic needs callouts, retries, or heavier processing.

**How it works:** Keep the platform event trigger thin and hand off durable work to Queueable Apex.

### CDC Versus Platform Event Decision

**When to use:** Architects are unsure whether to publish a custom event or consume record-change events.

**How it works:** Use CDC when record mutation itself is the signal. Use Platform Events when the signal is business-defined and may not map one-to-one to DML.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Need to broadcast a domain event like “Application Submitted” | Platform Event | Explicit payload and publisher-controlled timing |
| Need downstream systems to react to Account or Contact data changes | CDC | Change stream already represents row changes |
| Apex subscriber needs callouts or heavier orchestration | Platform event trigger + Queueable | Thin trigger, safer processing boundary |
| External consumer must recover after downtime | Replay-aware external subscriber | Replay handling belongs with external consumer state |


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] Publishers inspect publish results or log publication failures deliberately.
- [ ] Platform event triggers stay thin and avoid becoming integration god-classes.
- [ ] Event payloads represent business intent, not accidental object snapshots.
- [ ] CDC and Platform Events are chosen for clear, different reasons.
- [ ] External replay expectations are documented when non-Apex consumers exist.
- [ ] Monitoring includes event publication failures and subscriber failures.

## Salesforce-Specific Gotchas

1. **Apex platform event triggers are asynchronous `after insert` subscribers** — do not design them like normal object triggers.
2. **Replay IDs matter for external consumers, not as a substitute for Apex trigger state** — keep that responsibility in the consumer architecture.
3. **Publishing inside loops scales poorly** — collect events and publish in bulk.
4. **A successful transaction does not guarantee every subscriber succeeded** — subscriber monitoring must be independent.

## Output Artifacts

| Artifact | Description |
|---|---|
| Event decision guide | Recommendation for Platform Events vs CDC and publisher/subscriber boundaries |
| Publish/subscribe review | Findings on payload design, result handling, and consumer reliability |
| Event pattern scaffold | Sample `EventBus.publish` service and thin subscriber-trigger structure |

## Related Skills

- `apex/async-apex` — use when the subscriber workload really needs Queueable or Batch design rather than event design alone.
- `apex/exception-handling` — use when publication failures or subscriber exceptions need better classification and logging.
- `apex/callouts-and-http-integrations` — use when event consumers ultimately call external HTTP systems.
