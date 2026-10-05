---
name: event-schema-design
description: Use when defining or reviewing runtime events, lifecycle payloads, and event-order expectations for PonyBunny.
---

# Event Schema Design

## Use this skill when
- adding lifecycle events
- changing event payloads
- improving observability
- reviewing event-driven runtime flow

## Goals
- make runtime flow explicit
- preserve traceability
- reduce ambiguity for producers and consumers
- support debugging and evaluation

## Process
1. Define the lifecycle.
2. Define the events.
3. Define required identifiers.
4. Define payload fields.
5. Define ordering assumptions.
6. Define producer and consumer expectations.
7. Define compatibility concerns.

## Output contract
Return:
- event list
- payload fields
- ordering notes
- producer notes
- consumer notes
- risks
