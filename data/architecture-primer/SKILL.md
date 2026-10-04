---
name: architecture-primer
description: This skill should be used when the user wants to design, plan, or decide the architecture of a system, app, or platform from scratch. Trigger phrases include "how do I structure this", "what architecture should I use", "how does this scale", "monolith or microservices", "what database", "what stack", "design the system", "how do I handle X users". Inspired by the System Design Primer. It runs a discovery phase, applies a decision tree, and outputs concrete architecture decisions with trade-offs.
---

# Architecture Primer

This skill turns a vague "how should I build this?" into concrete, justified architecture decisions. It is based on the System Design Primer, adapted to favor shipping over over-engineering.

Analogy: do not design a 10-lane highway before knowing if 10 cars or 10 million cars will use it. Measure the traffic first, then build the road.

## PHASE 1 — Discovery (mandatory before any decision)

Never propose an architecture before completing discovery. Ask questions 2-3 at a time, in plain language, in these three blocks. Skip any question the user already answered.

**Block A — Scale**
- How many users do you expect at launch? And in 12 months?
- Are users in one region or several countries?
- Is usage steady, or does it spike (e.g. launches, business hours, campaigns)?

**Block B — Nature of the system**
- Does it read more than it writes, or the other way around?
- What happens if it goes down for 1 hour — is it critical?
- Does the data need immediate consistency, or is a short delay acceptable?

**Block C — Context**
- Is there a technical team, or just you?
- Roughly what monthly infrastructure budget is realistic?
- When do you need the MVP live?

## PHASE 2 — Decision tree

Apply these rules using the discovery answers. Each rule has a default; deviate only with a concrete reason.

### Monolith vs Microservices
- Team under 5 people → **monolith, always**.
- MVP or under 6 months to ship → **monolith, always**.
- Over 100k daily active users → evaluate microservices for the parts that actually hurt.
- Rule: **start monolith, split when it hurts.** Premature microservices add ops cost with no benefit.

### SQL vs NoSQL
- Relational data needing integrity → **PostgreSQL**.
- Flexible documents, horizontal scale → **MongoDB**.
- Cache / sessions / real-time → **Redis**.
- Full-text search → **Elasticsearch**.
- Rule: **PostgreSQL by default; switch only with a concrete reason.**

### Cache
- Same query repeats a lot → **Redis**.
- Data that rarely changes but is read often → **CDN or Redis**.
- Data unique per user on every request → **no cache** (it would not hit).

### Message queue
- Tasks that can run later (emails, notifications, exports) → **yes**.
- Spikes that could overwhelm the database → **yes** (absorb the burst).
- Everything synchronous and simple → **no** (added complexity not worth it).

## PHASE 3 — Required output

Always deliver these five sections, in this order:

1. **Executive summary** — 3 lines, plain language.
2. **Architecture decisions** — each as:
   - **Decision:** what was chosen
   - **Why:** the reason, tied to a discovery answer
   - **Trade-off:** what is given up
3. **Recommended stack** — concrete tools and services.
4. **Mermaid diagram** of the components, e.g.:
   ```mermaid
   graph TD
     User[User] --> CDN[CDN]
     CDN --> App[Monolith API]
     App --> DB[(PostgreSQL)]
     App --> Cache[(Redis)]
     App --> Queue[Queue] --> Worker[Background Worker]
   ```
5. **Risks and review triggers** — what could break, and the concrete signal (e.g. "revisit when writes exceed 500/s" or "split the billing service when the team passes 8 engineers").

## Principles that are never violated

- **Do not over-engineer the MVP.** The MVP's job is to validate, not to scale.
- **Availability beats perfection.** A system that is up and imperfect beats a perfect one that is down.
- **Measure before optimizing.** No premature optimization without data.
- **The team matters.** The best architecture is the one the team can actually maintain.
