---
name: fleet-build-order
description: "The scaffold→foundation→infrastructure→features pattern — the order of building at every level"
user-invocable: false
---

# Build Order — Scaffold → Foundation → Infrastructure → Features

> "There is also the very important notion of the order of things and the repeated scaffold, foundation, infrastructure, features chain of evolution and design and engineering."

This pattern applies to tasks, epics, projects, and the fleet itself.

## The Four Stages

### Scaffold
The basics: core configuration files, project structure, technology stack.
- What files exist? What's the directory structure?
- What tools, frameworks, languages?
- What's the CI? What's the deployment model?
- Scaffolding is FAST — it's just the structure, no substance yet.

### Foundation
The spine: modules/packages, design system, architecture documents, diagrams.
- What modules compose the system?
- What design patterns apply?
- What's the data model? The API contracts?
- Foundation is THOUGHTFUL — wrong foundation = wrong building.

### Infrastructure
Building ON the foundation: implementation of core systems, testing, monitoring.
- Implementation follows the design from Foundation.
- Tests validate against the architecture.
- Monitoring observes what Foundation designed.
- Infrastructure is METHODICAL — one brick at a time, in order.

### Features
The special capabilities: unique product features, user-facing differentiators.
- Features BUILD ON infrastructure that builds on foundation.
- A feature without infrastructure is a hack.
- Infrastructure without foundation is technical debt.
- Foundation without scaffold is chaos.

## The Skyscraper Analogy

> "To build a skyscraper like we aim, there is always an order."

- **Skyscraper** = the ideal. Proper order. Strong foundation. Everything in place.
- **Pyramid** = the compromise. Wider base, shorter reach. Still structured.
- **Mountain** = spaghetti. No order. Deprecated patterns. Technical debt.

## When to Apply

**Breaking an epic:** Is this scaffold work (structure), foundation (design), infrastructure (implementation), or features (capabilities)?

**Starting a task:** What stage is this at? If there's no scaffold, you need scaffold first. If there's no foundation, building infrastructure is premature.

**Reviewing work:** Did this follow the order? Code that jumps to features without foundation is debt.

## In the Fleet

The fleet itself follows this order:
- **Scaffold:** Config files, agent templates, gateway setup, IaC scripts
- **Foundation:** Architecture docs, standards, methodology, synergy matrix
- **Infrastructure:** Orchestrator, MCP tools, chains, immune system, Navigator
- **Features:** Autonomous mode, multi-model, RAG, federation
