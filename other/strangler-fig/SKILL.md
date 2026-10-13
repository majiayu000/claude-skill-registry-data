---
name: strangler-fig
description: Extract functionality from a monolith incrementally using the Strangler Fig pattern
triggers: [strangler fig, monolith migration, extract service, decompose monolith, migrate to microservices, modularize]
audience: engineer, manager
---

# Strangler Fig Migration

## Context
The Strangler Fig pattern incrementally replaces a monolith by routing new traffic to new implementations while the old code is gradually retired — like a strangler fig vine that eventually replaces the host tree. It is the safest way to decompose a monolith because the system remains in production throughout the migration, and you can stop at any point.

Use this skill when:
- Extracting a service or module from a monolith
- Migrating a legacy system to a new architecture
- You need to rewrite a subsystem without a "big bang" replacement
- You want to modularize a monolith without going full microservices

## Instructions

### The Three Phases

#### Phase 1 — Identify and Prepare
1. **Choose a bounded context to extract first.** Pick something with:
   - Clear boundaries (limited integration with the rest of the system)
   - High business value or pain (a reason to do the work)
   - A stable-ish interface (the API it exposes to the rest of the monolith)

2. **Write characterization tests** on the existing monolith behavior before changing anything. These become the acceptance tests for the new implementation.

3. **Create an HTTP façade (or internal module boundary).** Route the identified functionality through a single entry point — a facade interface in the monolith — even if the implementation stays in place. This is the strangling surface.

#### Phase 2 — Build Alongside
4. **Build the new implementation** (new service, new module, new package) that satisfies the same interface captured in Phase 1.

5. **Deploy both.** Use a feature flag or proxy to route a small % of traffic to the new implementation.

6. **Run in parallel mode.** For critical paths, call both old and new, compare outputs, but serve from old. This is the "dark launch" / shadow mode.

7. **Gradually shift traffic.** Increase the % of traffic to the new implementation as confidence grows. Monitor for divergence.

#### Phase 3 — Retire the Old Code
8. **Once 100% of traffic is on the new implementation**, keep the old code behind the flag for one sprint as a fallback.

9. **Remove the old code path**, the feature flag, and the façade routing.

10. **Update the ADR** to record the decision and completion.

### Data Migration Considerations
- Never migrate data and code in the same step.
- Use the **Expand/Contract** pattern for database schema changes: add new columns/tables, migrate data, then remove old structures.
- If extracting a service, the new service should own its data — do not share a database between the monolith and the new service.

### When to Stop (Not Every Monolith Should Be Decomposed)
Do not extract a service unless:
- The team independently deploying it is a real benefit
- The operational overhead of a separate service is worth it
- The bounded context is truly independent (otherwise you create a distributed monolith)

A **well-structured monolith** with clear internal module boundaries is often better than a distributed system extracted prematurely.

### Decision Checklist Before Extracting
- [ ] Is this a genuine bounded context with a clear owner?
- [ ] Is the interface stable enough to version?
- [ ] Does the team have operational capacity to run a separate service?
- [ ] Is the data ownership clear?
- [ ] Have the characterization tests been written?

## Principles
- Source: [Strangler Fig Application — Martin Fowler](https://martinfowler.com/bliki/StranglerFigApplication.html)
- Source: [MonolithFirst — Martin Fowler](https://martinfowler.com/bliki/MonolithFirst.html)
- Key idea: *"The most important rule is: never stop the business to do the rewrite. The strangler fig lets you migrate incrementally while keeping the system in production throughout."*

## Output Format
When applying this skill, the agent should:
- Identify the candidate bounded context and assess extraction readiness
- List the characterization tests needed
- Generate the façade/proxy interface
- Produce a phased migration plan with rollback points
- Flag any data ownership or database coupling issues
- Create the ADR for the architectural decision
