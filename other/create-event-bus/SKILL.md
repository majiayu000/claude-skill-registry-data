---
name: create-event-bus
description: "Use when you need a type-safe event bus spec designed for inter-system communication. Triggers: 'event bus spec', 'define events'."
---

## 1. Overview
Translates narrative rules into a type-safe, decoupled event bus spec. Atomizes game logic into discrete events, typed payloads, and subscriber contracts. Output: `events_spec.md` — the communication contract for all game subsystems.

**Scenarios**: Inter-system communication contracts, decoupling tightly coupled systems, typed event contracts for parallel development.

## 2. Quick Reference

**Output**: `{TARGET_FOLDER}/docs/events_spec.md`. **Input**: `raw_rules.md`.

Workflow steps:
1. Rule Atomization — identify triggers (When), conditions (If), outcomes (Then) from rules
2. Event & Payload Definition — define semantic event name + typed payload fields per trigger
3. Subscriber Mapping — identify reacting systems, define action contracts
4. Architectural Validation — check for circularity, frequency optimization, decoupling
5. Export — write spec file

Key rules: route all inter-system communication through event bus; payloads are minimal and typed; events must be acyclic (no loops).

## 3. Workflow

1. **Rule Atomization** (`raw_rules.md`): Identify single-source triggers (When), conditions (If), outcomes (Then).
2. **Event & Payload Definition**: For each unique trigger, define semantic event name + typed payload (e.g., `damageAmount: Float`).
3. **Subscriber Mapping**: Identify reacting systems, define "Action Contracts" (reaction to event receipt).
4. **Architectural Validation**: Circularity checks, frequency optimization, decoupling verification.
5. **Export**: Write to `{TARGET_FOLDER}/docs/events_spec.md`.

## 3. Intercepts
- **[Tight Coupling]**: Direct system calls suggested → "Redirecting [A]→[B] through event bus as decoupled contract."
- **[Vague Trigger]**: Rule lacks clear causality → "Trigger too vague. Driven by discrete action or state change?"
- **[Vague Payload]**: Payload too broad/untyped → "Need typed fields (e.g., `amount: Float`, `sourceID: String`) for robust event contract."

## 4. Red Flags
- **Event Bus Communication**: Route all inter-system communication through event bus exclusively
- **Clear Triggers**: Define explicit "When" conditions for every rule
- **Typed Payloads**: Include typed payload fields for every event
- **Acyclic Events**: Ensure events do not trigger each other in loops
- **Focused Payloads**: Keep payloads minimal and specific to the trigger
