---
name: implement-event-bus
description: "Use when you have an event spec (events_spec.md) and need to generate the EventBus class, typed event structs, subscriber interface, and routing."
---

## 1. Overview

Implements a typed event bus from an event spec — generates event structs, subscriber interfaces, and publish/subscribe routing that keeps handlers non-blocking. Core principle: strict typing and lightweight handlers prevent coupling and stalls.

## 2. When to Use

Use when:
- You have an `events_spec.md` and need the EventBus class, typed event structs, subscriber interface, and routing generated.
- System communication is becoming tightly coupled via direct calls and you want event-driven decoupling.
- Handlers for high-frequency events must stay non-blocking.

Do not use when:
- The event spec doesn't exist yet — run the event design step first.
- You only need one-off callbacks between two objects — an event bus is overkill.

## 3. Triggers & Red Flags
**Red Flags**:
- **Acyclic Handlers**: Subscribers do not publish events that trigger their own handlers
- **Non-Blocking Handlers**: Keep event loop operations lightweight; use async tasks for heavy work like disk I/O
- **Strictly Typed Payloads**: Use typed structures for all event payloads

## Quality Gates
- Event handlers complete quickly — keep operations lightweight to maintain high-frequency responsiveness
- Buffer sizes sized appropriately per frequency tier to prevent blocking
- All events use strongly-typed structures exclusively

## 3. Workflow

1. **Platform Detection**: Scan config for target language/platform.
2. **Event & Enum Generation** (`events_spec.md`): Generate all event structures + idiomatic enums.
3. **Subscriber Interface**: Type-safe subscriber interface/trait/protocol with all handler methods from spec.
4. **EventBus & Routing**: Core subscribe/publish/unsubscribe with buffer sizes per frequency tier to prevent blocking.

## 4. Intercepts
- **[Circularity]**: Subscriber publishes self-triggering event → "[Event X] causes own handler re-trigger. Implement debounce or change trigger?"
- **[Blocking I/O]**: Handler has heavy ops → "[Handler] performs blocking I/O. Stall risk on high-freq events. Move to async task or worker thread?"

**Imperative**: Non-blocking handlers for high-frequency events. Appropriate buffer sizes. Keep operations lightweight in handlers.

## 5. Final Integrity Audit
- [ ] Every event in `events_spec.md` has a corresponding typed struct and enum entry
- [ ] Subscriber interface exposes all handler methods defined in the spec; no orphaned events without consumers documented
- [ ] EventBus provides subscribe/publish/unsubscribe with frequency-tier-appropriate buffering (no blocking calls)

