---
name: book--domain-driven-design-distilled--nano
description: >-
  DDD Distilled (Vaughn Vernon) — Minimal rules — essential one-liners only. Use when asked to apply DDD Distilled principles or review code against DDD Distilled standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Domain-Driven Design Distilled by Vaughn Vernon

## When to use

Use as compact DDD guidance when business language, context ownership, invariants, or integration meaning can affect the code.

## Primary bias to correct

DDD is selective modeling for real business complexity, not decorative layers, framework shape, or blanket tactical ceremony.

## Decision rules

- Start from business capability, subdomain type, Bounded Context, and local Ubiquitous Language before tactical patterns.
- Invest most design effort in the Core Domain; keep Supporting, Generic, CRUD, and mainly technical areas simpler.
- Put every meaningful model inside one explicit Bounded Context that owns its language, rules, semantics, code, tests, and integration contracts.
- Translate between contexts when meanings differ; never share domain classes or terms whose meanings diverge.
- Choose context relationships and integration mechanisms deliberately, including Conformist or Anticorruption Layer when foreign meaning is involved.
- Keep integration contracts separate from internal models, and do not expose Aggregate internals through REST or transport payloads.
- Use Entities for identity, Value Objects for validated meaning, Aggregates for small invariant boundaries, and Domain Events for meaningful past-tense facts.
- Modify one Aggregate per transaction by default; reference other Aggregates by identity and use eventual consistency when the business allows it.
- Keep business decisions in the domain model; Application Services coordinate use cases.
- Keep frameworks, persistence, transport, and external schemas out of the domain model.
- Use scenarios, acceptance tests, Event Storming, spikes, and domain-expert walkthroughs to learn quickly without hiding modeling debt.

## Trigger rules

- When language is fuzzy or overloaded, sharpen terms before coding.
- When one model absorbs unrelated concerns, redraw the subdomain or context boundary.
- When foreign models, schemas, APIs, or frameworks drive domain shape, add boundary translation.
- When a transaction wants many roots or a large graph, revisit Aggregate boundaries and consistency timing.
- When services, controllers, setters, flags, or primitives carry business decisions, expose the missing domain concept.
- When events are vague, command-like, or noisy field changes, redesign them as specific business facts.

## Final checklist

- Clear subdomain?
- Clear context?
- Clear language?
- Clear translation?
- Clear invariant boundary?
- Clear modeling debt?
