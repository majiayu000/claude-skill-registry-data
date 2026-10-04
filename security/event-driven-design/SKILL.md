---
name: event-driven-design
description: When designing loosely coupled systems that react to state changes asynchronously.
version: 2.0.0
category: architecture
tags: [architecture, events, async]
skill_type: architecture
author: skiLLM
license: MIT
compatible_agents: [claude-code, cursor, copilot, codex]
estimated_context_tokens: 2000
dangerous: false
requires_review: true
security_level: review-required
dependencies: []
triggers: [event, async, decoupling, event bus, message broker]
permissions:
  filesystem: { read: true, write: true }
  network: { outbound: true }
  shell: { execute: false }
input_requirements: [microservices or monolithic architecture, message broker setup]
output_contract: [immutable events, idempotent consumers, dead letter queues]
failure_conditions: [event loss, duplicate processing, synchronous coupling]
last_updated: 2026-05-15
---

# Event-Driven Design

## Purpose
Tightly coupled systems break and scale poorly. Event-driven architectures decouple producers from consumers by using immutable, timestamped facts as the communication mechanism. This enables systems to evolve independently, scale horizontally, and handle distributed failures gracefully.

## When to use
- De-coupling monolithic microservices
- Implementing long-running asynchronous workflows (e.g., video processing, email sending)
- Triggering multiple side-effects across different domains from a single action
- Designing systems that need to replay history or audit changes

## When NOT to use
- Simple synchronous request-response flows (don't add unnecessary complexity)
- Real-time bidirectional communication (use WebSockets instead)
- Workflows requiring immediate response to action

## Inputs required
- Microservices or monolithic application with clear domain boundaries
- Message broker infrastructure (Kafka, RabbitMQ, EventBridge, etc.)
- Understanding of event sourcing concepts

## Workflow
1. **Define Events**: Identify state changes in the domain and model them as past-tense events (e.g., `OrderPlaced`, `UserRegistered`, `PaymentProcessed`)
2. **Design Event Payloads**: Include Event ID, Timestamp, Event Type, and minimal required data (avoid large nested objects)
3. **Publishing Mechanism**: Have the producer system emit the event to a Message Broker without caring who consumes it
4. **Idempotent Consumers**: Ensure consumer services can process the same event multiple times without adverse side effects
5. **Handle Failures**: Implement Dead Letter Queues (DLQ) for events that consumers repeatedly fail to process
6. **Track Processing**: Add idempotency keys or processed event IDs to detect duplicates
7. **Monitor**: Set up alerts for DLQ messages and processing delays

## Rules
- MUST model events as immutable facts (past tense: `OrderPlaced` not `PlaceOrder`)
- MUST NEVER modify or delete events once emitted (audit trail requirement)
- MUST make consumers idempotent (same event processed multiple times = same outcome)
- MUST avoid deeply nested, rapidly changing entity graphs in payloads
- MUST include Event ID, Timestamp, Event Type in all events
- MUST implement Dead Letter Queues for failed events
- MUST NOT use synchronous HTTP calls as part of event workflows

## Anti-patterns
- **Commands as Events**: Naming events like actions (`SendEmailEvent`) rather than facts (`UserCreated`)
- **Distributed Monolith**: Systems requiring synchronous HTTP calls *in response* to an event before completing their workflow
- **Huge Event Payloads**: Sending entire entity graphs; include only IDs and essential context
- **No Idempotency**: Processing events without tracking duplicate processing
- **Synchronous Dependencies**: Event handler blocks waiting for another service response
- **Event Loss**: Not persisting events to broker; memory-only event storage

## Failure conditions
- Events cannot be replayed (no persistence)
- Consumers not idempotent (duplicates cause data corruption)
- No Dead Letter Queue for failed events
- Synchronous dependencies between event producers and consumers
- Event payloads change format without versioning support

## Validation checklist
- [ ] All events named as past-tense facts (not commands)
- [ ] Events are immutable after emission
- [ ] Event payloads include ID, Timestamp, Type
- [ ] Consumers are idempotent (can process same event multiple times safely)
- [ ] Dead Letter Queue configured and monitored
- [ ] No synchronous HTTP dependencies in event handlers
- [ ] Event versioning strategy defined
- [ ] Idempotency keys tracked (to detect duplicates)
- [ ] Monitoring/alerting on DLQ messages
- [ ] Event processing latency within SLA

## Output format
- **Event schema**: Event ID, Timestamp, Type, Payload (minimal data)
- **Payload format**: JSON with primitive types, IDs, not full objects
- **Consumer pattern**: Read event, validate idempotency key, process, mark as processed
- **Infrastructure**: Message broker setup with persistence and DLQ
- **Monitoring**: Dashboards for event processing latency and DLQ depth

## Security considerations
- Event payloads MUST NOT contain credentials or PII
- Access control MUST be enforced at consumer (not all services can listen to all events)
- Event encryption MUST be used for sensitive domains
- Audit logging MUST track who published and consumed events
- Dead Letter Queues MUST be monitored (may contain sensitive data)

## Agent execution notes
- Agent MAY: Define events, create event handlers, implement idempotency, set up DLQ
- Agent MUST NEVER: Use commands instead of events, create synchronous dependencies, lose events
- Agent MUST ASK: Before adding new event types, before changing event schema, before removing DLQ
- Agent MUST VALIDATE: Events are facts not commands, consumers are idempotent, DLQ configured

## Example

**❌ Anti-pattern (Commands as events, synchronous coupling, no idempotency):**
```javascript
// WRONG: Command not event
publishEvent('SendEmail', { userId, subject });

// WRONG: Synchronous dependency
async function handleOrderPlaced(event) {
  const order = await orderService.fetch(event.orderId); // Blocks on external service
  await emailService.send(order.email); // Fails if service is down
}

// WRONG: No idempotency tracking - processes duplicate
async function handleUserCreated(event) {
  await database.createUser(event); // Processes same event twice = duplicate user
}
```

**✅ Correct pattern (Events, async, idempotent):**
```javascript
// CORRECT: Past-tense event with minimal payload
publishEvent({
  type: 'UserCreated',
  id: uuid(),
  timestamp: new Date(),
  payload: {
    userId: event.userId,
    email: event.email
  }
});

// CORRECT: Asynchronous, idempotent consumer
async function handleUserCreated(event) {
  // 1. Track processed events (idempotency)
  const alreadyProcessed = await cache.get(`processed:${event.id}`);
  if (alreadyProcessed) return; // Skip duplicate
  
  // 2. Process without waiting for external services
  await emailQueue.enqueue({
    email: event.payload.email,
    template: 'welcome'
  });
  
  // 3. Mark as processed
  await cache.set(`processed:${event.id}`, true, { ttl: 86400 });
}

// 4. Dead Letter Queue for failed events
async function handleFailedEvent(event, error) {
  await dlq.store({
    originalEvent: event,
    error: error.message,
    timestamp: new Date(),
    retryCount: 0
  });
}
```
