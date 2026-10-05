---
name: dircreative-idea-intake
description: Parse a rough idea into project brief, inferred channel, constraints, and missing decisions.
---

# Idea Intake

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/chat-co-creation-interface.md`
- `docs/film-preproduction/creative-copy-deck-capability.md`
- `docs/film-preproduction/schemas/project.yaml`
- `docs/film-preproduction/research/channel-playbooks.md`

## Inputs

- raw user idea
- optional channel, duration, aspect ratio, references, constraints

## Outputs

- project brief
- parsed intent
- channel inference
- facts, source evidence, and labeled inferences
- audience tension, business objective, single-minded proposition, and avoid-cliches
- missing decisions
- recommended next stage only when it belongs to the requested output set

## Chat Surface

Return the requested first concept or a compact brief with the decision-changing
assumptions. Reuse supplied channel, duration, audience and constraints. A complete
brief needs no factual reconfirmation. Follow the root project-interaction
choice if pacing is still unknown; explicit self-direction already selects direct execution. If a critical fact is missing, explain its
specific effect and continue independent creative work.

## Creative Foundation Gate

Separate source facts, observed evidence and creative inferences. In a formal
creative-foundation handoff, bind facts and source_evidence_ids, keep unique
resolving IDs and source verification, and validate that exact schema. Do not
require a formal ID register for a rough concept in chat.

For commercial work, make audience tension, business objective,
single_minded_proposition and avoid_cliches concrete. A strategy may be proposed
as a hypothesis; product performance, price, historical assertions and research
claims require evidence before being presented as facts.

## Rules

- Infer a channel only when evidence is strong.
- Keep uncertainty explicit.
- Distinguish `story_duration` from `generation_unit_limit`. A 15s video model cap means each generated group is at most 15s, not necessarily that the story is 15s.
- If the duration meaning is ambiguous, ask one clarification question before scripting.
- Separate facts from inferences in both the artifact and the chat preview.
- A factual proposition needs supporting facts; a proposed creative strategy is labeled judgment until validated.
- Record category cliches and familiar visual shortcuts the downstream concept should avoid.
- Intake supplies constraints to the controller. When the user requested further creative work, continue to that work without a brief-confirmation round.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Include `skill_run_receipt` with input artifacts, output artifacts, fail-closed ID status, source-evidence and inference binding status, tension/SMP source status, commercial-strategy status, decisions, unresolved questions, QA status, and `next_recommended_skill: director-room`.
