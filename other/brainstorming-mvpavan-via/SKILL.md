---
name: brainstorming
description: Use when material scope or behavior decisions need exploration, or the user requests brainstorming. Handle a single routine ambiguity directly.
---

# Brainstorming

Resolve material scope or behavior decisions before committing to an approach.

## Route before grounding

- Clear, bounded behavior: return to the task; no interview or spec is required.
- One routine missing detail: infer from relevant code or ask one focused
  question, then continue independent work.
- Several live directions: use `references/exploration.md` when structured
  divergence would help.
- Requested interview: use the grilling skill. A written critique is a review,
  not automatic permission to interview or edit documents.
- Decisions already settled: synthesize them without reopening the discussion.

Read only the relevant existing code, authoritative docs and constraints needed
to distinguish the live choices. Name the closest existing solution before
proposing a new one.

## Resolve

Establish outcome, intended user, success criteria, constraints and exclusions.
Present materially different options with tradeoffs when alternatives remain.
Ask about consequential unresolved choices; group independent questions when
that is easier to answer. Carry prior decisions and authorization forward.
For interview technique or an explanation that benefits from a picture, consult
`references/interviewing.md` or `references/visuals.md`, respectively.

Stop exploring when a direction and its acceptance criteria are sufficient for
the next authorized step. Do not invent more questions or variants to fill a quota.

## Record and hand off

An in-chat decision is enough for bounded work unless a durable artifact was
requested. For a spec that planning or another session will consume, use
`references/spec-template.md`; default path is `docs/specs/YYYY-MM-DD-<topic>.md`.
Record sources, assumptions and excluded alternatives as needed for handoff.

A new unresolved spec is `Status: draft`. Mark it `Status: approved` only when
actual authorization covers its direction and scope, recording that evidence.
A blocking question must be resolved or explicitly excluded before approval.
Review consistency, scope and verifiability; independent critique is conditional
on material risk and the shared delegation policy.

This skill's output is decisions or a spec. Continue into planning/execution when
already authorized; a brainstorming-only request does not authorize code changes.
