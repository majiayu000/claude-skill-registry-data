---
name: lwc-state-management
description: "Share state across LWCs using pub/sub, Lightning Message Service, @wire, and reactive stores. NOT for in-component reactivity."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Scalability
  - User Experience
triggers:
  - "lwc shared state"
  - "lightning message service"
  - "pubsub lwc"
  - "lwc global store"
tags:
  - state
  - lms
  - wire
  - architecture
inputs:
  - "components that need to share state"
  - "scope (tab-local / app-wide)"
outputs:
  - "state-management decision + implementation snippets"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

# LWC State Management

LWC has four state-sharing mechanisms: (1) parent→child via public @api properties, (2) @wire for server-synced data, (3) Lightning Message Service for sibling LWCs/Aura, (4) custom events for child→parent. This skill picks the right mechanism based on component distance and persistence requirements, and shows why legacy pubsub and heavy external stores (Redux, MobX) should be avoided in favor of these native primitives plus tiny singleton signals.

## When to Use

Any time two non-parent/child LWCs must stay in sync. Not for tiny local state.

Typical trigger phrases that should route to this skill: `lwc shared state`, `lightning message service`, `pubsub lwc`, `lwc global store`.

## Recommended Workflow

1. Parent→child: public @api props + custom events.
2. Sibling LWCs: Lightning Message Service via a message channel (`@salesforce/messageChannel/Foo__c`).
3. Server data: `@wire` — it's reactive and cached.
4. App-wide reactive store: a singleton module exporting a signal-like observable; use sparingly.
5. For Aura↔LWC interop use LMS; pubsub library is legacy.

## Key Considerations

- LMS requires a Custom Metadata record for the channel — check it in.
- @wire refresh via `refreshApex` or `getRecordNotifyChange`.
- Don't import Redux into LWC (bundle bloat); use a tiny hand-rolled store.
- Sibling components must both subscribe after render.

## Worked Examples (see `references/examples.md`)

- *Sibling refresh via LMS* — Edit panel + list panel
- *App-wide current region* — Multi-region switcher

## Common Gotchas (see `references/gotchas.md`)

- **Missing message channel** — LMS silently no-ops.
- **Race on subscription** — First publish missed.
- **Redux-style overhead** — Bundle bloat, debug complexity.

## Top LLM Anti-Patterns (full list in `references/llm-anti-patterns.md`)

- pubsub library in new code
- Bundling Redux/MobX into LWC
- Forgetting to deploy message channel

## Official Sources Used

- Lightning Web Components Developer Guide — https://developer.salesforce.com/docs/platform/lwc/guide/
- Lightning Data Service — https://developer.salesforce.com/docs/platform/lwc/guide/data-wire-service-about.html
- LWC Recipes — https://github.com/trailheadapps/lwc-recipes
- SLDS 2 — https://www.lightningdesignsystem.com/2e/
