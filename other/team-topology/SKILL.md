---
name: team-topology
description: Apply Team Topologies patterns to design effective team structures. Classify teams as stream-aligned, platform, enabling, or complicated-subsystem. Define interaction modes (collaboration, X-as-a-Service, facilitating) to reduce cognitive load and optimize delivery flow.
triggers:
  - "team structure"
  - "reorganize teams"
  - "cognitive load"
  - "platform team"
  - "team dependencies"
  - "Conway's Law"
audience:
  - manager
  - engineer
---

# Team Topology

Design team structures that minimize cognitive load and maximize flow of change.

## Core Team Types

### Stream-Aligned Team
- Owns a slice of business value end-to-end (feature, product area, user journey)
- Ships independently; has all capabilities needed (dev, test, deploy, monitor)
- **Goal**: Fast flow with minimal external dependencies
- **Anti-pattern**: Team owns code but not deployment or monitoring

### Platform Team
- Provides self-service internal products that stream-aligned teams consume
- Reduces cognitive load for other teams — they shouldn't need to know how the platform works
- **Goal**: Improve developer experience; measured by adoption, not features shipped
- **Anti-pattern**: Platform team that becomes a bottleneck or requires tickets to use

### Enabling Team
- Temporary by design — exists to upskill stream-aligned teams
- Brings expertise (security, performance, accessibility) then steps back
- **Goal**: Leave teams more capable; dissolves or reforms around new problem
- **Anti-pattern**: Enabling team that never transfers knowledge and stays forever

### Complicated-Subsystem Team
- Owns a component requiring deep specialist knowledge (ML models, DSP, cryptography)
- Small, stable, provides well-defined API to the rest of the org
- **Goal**: Isolate complexity so stream-aligned teams don't need to understand it
- **Anti-pattern**: Every team becomes "complicated-subsystem" to avoid accountability

---

## Interaction Modes

| Mode | When to Use | Signs It's Working |
|---|---|---|
| **Collaboration** | Exploring unknown territory together | Joint design sessions, shared ownership, short-lived |
| **X-as-a-Service** | Well-understood, stable capability | Self-service, API/docs sufficient, no meetings needed |
| **Facilitating** | Enabling team helping another learn | Knowledge transfers, team becomes self-sufficient |

**Rule**: Collaboration is expensive. Default to X-as-a-Service once the interface is stable.

---

## Cognitive Load Assessment

For each team, evaluate:

```
Team: [name]
Type: [stream-aligned / platform / enabling / complicated-subsystem]

Cognitive load check:
[ ] Team can deploy without help from another team
[ ] Team understands what they own end-to-end
[ ] Team has < 3 active collaboration-mode dependencies
[ ] Oncall rotation is sustainable (no hero engineers)
[ ] Team size: 5-9 people (Dunbar / two-pizza)

Current blockers:
- [External team dependencies that slow delivery]
- [Domains too large for one team to own]
- [Missing capabilities (no one owns observability, security, etc.)]

Recommendation: [restructure / hire / extract platform / create enabling team]
```

---

## Conway's Law Application

> "Organizations design systems that mirror their communication structures." — Mel Conway

**Reverse Conway Maneuver**: Design your team topology first, then let the architecture follow.

1. Draw the architecture you *want* to have
2. Design teams that can own each bounded context independently
3. Minimize inter-team API surface to only stable, versioned contracts
4. Use enabling teams to close gaps during transition

---

## Team Interaction Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| Tightly coupled teams | PRs waiting on another team | Extract shared capability to platform team |
| Ownership vacuum | "That's not our problem" | Assign explicit ownership, use ADR to document |
| Too many collaborations | Constant cross-team meetings | Move to X-as-a-Service, define API contract |
| Siloed specialists | Only one person can do X | Enabling team → knowledge transfer → dissolve |
| Big-bang reorg | Everything changes at once | Incremental topology shifts, measure cognitive load |

---

## Output Template

```markdown
## Team Topology Recommendation

### Current State
- [List teams and their current types/responsibilities]
- [Identified pain points: cognitive load, slow flow, dependencies]

### Target State
| Team | Type | Owns | Interaction Mode with Others |
|---|---|---|---|
| [name] | stream-aligned | [bounded context] | X-as-a-Service from platform |
| [name] | platform | [shared capability] | X-as-a-Service to stream teams |

### Transition Plan
1. [First step — least disruptive change]
2. [Second step]
3. [Stabilize and measure]

### Success Metrics
- Deployment frequency per stream-aligned team
- Lead time for change
- Number of cross-team dependencies per sprint
- Team-reported cognitive load (1-5 survey)
```

---

## References
- *Team Topologies* — Matthew Skelton & Manuel Pais (2019)
- Martin Fowler: [Conway's Law](https://martinfowler.com/bliki/ConwaysLaw.html)
- DORA: Organizational performance and team structure research
- LeadDev: [Platform Engineering](https://leaddev.com/platform-engineering)
