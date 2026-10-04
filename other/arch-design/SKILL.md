---
name: arch-design
version: 1.0.0
description: >
  System-design thinking before any doc or code: goals/non-goals,
  back-of-envelope numbers, components and contracts, failure modes,
  operability, security, trade-offs. Use for "design this system",
  "architecture for X", "trade-offs for X", "how should we architect",
  "API design", "data model for", "service boundaries", or before an ADR.
  Hands off to /ship:write-docs to record the decision. Not implementation
  planning (/ship:design — that turns a decided design into stories).
---

# Ship: Architecture Design

Think the design through before anything is written or built. The lenses
below apply to any system: a service, a CLI, a frontend, a data pipeline,
an agent runtime. Scale the depth to the decision — a single component
with clear constraints needs the frame, a contract sketch, and
trade-offs; a new system with unknowns needs every lens. Skipping a lens
is a judgment call you record with its reason ("no trust boundary
crossed — internal tool, single user"), never a silent omission.

_Path note: `../shared/*.md` references resolve against this skill's base
directory (announced as "Base directory for this skill" when the skill
loaded), not your working directory._

The quality bar for every lens: statements someone could prove wrong —
named numbers, named failure behaviors, named rejected alternatives.
Virtue words ("scalable", "robust", "flexible") with no test attached
are filler.

## Red Flag

**Never:**
- Jump to a solution before the frame (goals, non-goals, numbers) exists
- Present a design with zero numbers and zero rejected alternatives —
  that's a description, not a design
- Resolve a question from memory when the codebase can answer it
- Interrogate the user question-by-question — self-interview instead;
  user-owned calls become recorded assumptions
- Open many design branches at once — resolve dependencies in order
- Skip a lens silently — skip with a recorded reason, or don't skip

## Method — Walk the Lenses as a Self-Interview

Interview yourself relentlessly about every aspect of the design until
no unresolved question remains — the lenses below are the branches of
the tree. Take questions one at a time, in dependency order: resolve a
decision before opening the ones that build on it (storage before
schema, contract before internals) — an answer stacked on an unresolved
dependency is a guess, and opening many branches at once produces
shallow parallel guesses. For each question, state your recommended
answer, then resolve it with the strongest means available:

- **Codebase evidence** — if exploring the repo can answer it, explore;
  most questions die here. Never ask anyone what the code already says.
- **Arithmetic** — if a number decides it, compute the number (lens 2).
- **Judgment** — adopt your recommended answer and record it under
  Assumptions with what breaks if it's wrong.

Do not interview the user. Questions only they could answer (product
intent, priorities, external constraints) do not become blocking
prompts — adopt the recommended answer, mark the assumption, and
surface that short list when you present the analysis. The Q&A itself
is scaffolding, not deliverable: the analysis records the decisions it
produced.

## The Lenses

1. **Frame: goals, non-goals, requirements.** Functional capabilities;
   the non-functional numbers that bind the design (latency, throughput,
   availability, consistency, data volume); real constraints (existing
   stack, team, timeline, compliance, backward compatibility). Write
   explicit non-goals — a later reader must be able to tell deliberate
   exclusion from oversight. Never conflate "what we want" with "what
   exists": state the gap.
2. **Do the arithmetic.** Back-of-envelope estimates for the numbers
   that drive the shape: request rates, data growth, fan-out, budget
   per hop. Show the math — a computed number is falsifiable; "should
   scale fine" is not. Where a number is unknown, state the assumption
   and what breaks if it is 10× off.
3. **The boring option first.** Before designing anything new: does an
   existing utility, library, managed service, or simpler shape already
   cover this? Classify the decision — two-way door (reversible: pick
   the simple option fast and note the revisit trigger) or one-way door
   (hard to undo: full rigor). Most decisions are two-way doors;
   treating them all as one-way is how designs bloat.
4. **Components and contracts.** Responsibilities, data flow, data
   model, storage choices driven by access patterns. Define the
   contracts — interfaces, protocols, schemas — before the internals;
   they are what other people and later phases build against. Verify
   assumptions against the actual codebase, not memory.
5. **Failure modes.** For each component and dependency: what happens
   when it is down, slow, or returning garbage? What do concurrent
   access, retries, and duplicate delivery do? Name the blast radius
   and the degraded behavior a user sees ("if the queue dies, writes
   buffer locally for 10 minutes, then reject with a clear error" —
   never "handles failures gracefully"). Idempotency and
   partial-failure recovery are design decisions, not implementation
   details.
6. **Operability and rollout.** How does the system get from the
   current state to this design — the migration path, and whether it
   must be zero-downtime? What is the rollback story? Which metric or
   log line says it is working, and which signal says it is not? What
   does it cost to run? A design you cannot observe or roll back is
   not finished.
7. **Security and trust boundaries.** Where does data cross a trust
   line? AuthN/authZ at each boundary, secrets and credential handling,
   which data is sensitive and who may see it. One sentence when
   nothing crosses; a real section when anything does.
8. **Trade-off analysis.** For each major decision: at least two
   alternatives considered, concrete pros/cons, the deciding factor,
   and what you are giving up. A design with no rejected alternatives
   has not been designed.
9. **Revisit triggers.** Flag decisions that will not age well, with
   their trigger: load-dependent ("rethink at 10k rps"), time-bound
   ("chose X because Y isn't ready"), assumption-sensitive
   ("multi-region breaks this"). These are honest engineering, not
   weaknesses.

## Red-Team Before Presenting

Re-read the design as a skeptical staff engineer: what is the first
thing that breaks in production? Which number is least defensible?
Which alternative was dismissed too fast? If an attack lands, fix the
design, not the wording. For high-stakes or contested decisions,
dispatch a fresh peer challenge with only the draft (see
`../shared/runtime-resolution.md`) — the same adversarial pattern
/ship:design applies to specs.

## Execution Handoff

The analysis is the deliverable: the decision first, then the
load-bearing numbers, the failure modes that shaped it, the rejected
alternatives, and the assumptions the user should confirm (the
user-owned questions from the self-interview).

To make it durable, hand off to `/ship:write-docs` — it records the
decision as a design doc (design category: Boundaries required,
recommended body shape in that skill's conventions).

Output the report card (read `../shared/report-card.md` for the
standard format):

```
## [Arch Design] Report Card

| Field | Value |
|-------|-------|
| Status | <DONE / BLOCKED> |
| Summary | <the decision, one line> |

### Metrics
| Metric | Value |
|--------|-------|
| Lenses applied | <N>/9 (<skipped lenses + recorded reasons>) |
| Alternatives rejected | <N> |
| Assumptions recorded | <N> |
| Revisit triggers | <N> |

### Next Steps
1. **Record it** — /ship:write-docs to write the design doc / ADR
2. **Plan implementation** — /ship:design to turn it into executable stories
3. **Full workflow** — /ship:auto for end-to-end delivery
```
