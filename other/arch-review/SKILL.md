---
name: arch-review
description: "Stress-test designs before they ship—constraints, trade-offs, failure modes, and ADR-worthy decisions. Use for ADRs, big refactors, new services, or when ‘it works on my laptop’ isn’t enough."
---

# Architecture Review

**Challenge** a design without owning the team’s roadmap: clarify **forces** (scale, money, people, regulation), surface **risks**, and leave **decisions** traceable—usually as an ADR or review notes.

## Inputs you need (ask early)

- **Goal** and non-goals; **users** and SLAs; **constraints** (budget, deadline, org skills).
- **Current pain**—latency, incidents, cost, velocity—not buzzwords.
- **Alternatives** considered, even if rough.

## Review lens (pick what fits)

- **Failure**: blast radius, partial outages, data loss, replay.
- **Ops**: deploy model, rollbacks, observability, on-call load.
- **Change**: team size, Conway’s law, long-term ownership.
- **Security**: trust boundaries, secrets, supply chain—at architecture depth, not a full pentest.

## Output shape

- **Summary** of the proposal in your own words (catches misunderstandings).
- **Top risks** with severity; **mitigations** or experiments.
- **Open questions** for the team—not a pretend-final design.

## Not this

- Replacing the team’s **product** judgment; rubber-stamping; 20-page templates nobody reads.

## Done when

- The team can explain **what they decided**, **why**, and **what would falsify** the choice later.
