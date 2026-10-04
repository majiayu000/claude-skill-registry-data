---
name: interrogating-design
description: >-
  Systematically interrogates a worldbuilding decision, lore proposal, or science
  derivation through exhaustive questioning until all implications, contradictions,
  and dependencies are resolved. Use when stress-testing a new concept, validating
  a proposed rule, or when user says "grill me", "stress test this", "what are the
  implications", "does this break anything", "think through this with me",
  "challenge this idea", or "red team this". Does NOT write content — interrogation only.
model: opus
effort: max
---

# Interrogating Design

Interview me about every aspect of this decision until we reach shared
understanding. Walk down each branch of the decision tree, resolving
dependencies one by one. For each question, provide your recommended answer.
Ask one question at a time. If a question can be answered by exploring
existing documents, explore them instead.

## OODA Loop Mode (Boyd)

Run the interrogation as an iterative cycle:
- **Observe:** Read all relevant files, grep for related terms
- **Orient:** Synthesize against foundational constraints — destroy outdated
  mental models if new data contradicts them
- **Decide:** Formulate a specific hypothesis
- **Act:** Test the hypothesis against the repo

## Dependency-Order Walkthrough

Check implications in layer order (customize for your universe):
1. Foundations — contradicts core axiom or definitions?
2. Physics — violates particle mechanics, fields, or temporal rules?
3. Chemistry/Biology — contradicts established life sciences?
4. Civilizations & Narrative — contradicts existing canon?

## Adversarial Red Teaming Escalation

1. Does it contradict any explicit rule?
2. Does it contradict any implicit constraint (downstream implications)?
3. Does it survive cross-civilization application?
4. Would a hostile reader find it inconsistent?
5. Strip the narrative beauty — is the bare mechanism still valid?

## Russell Conjugation Check

Restate the proposal in the most boring, clinical language possible.
If it only works in emotive framing, it's aesthetic, not physics.

## After Validation

1. Self-review for placeholders, contradictions, ambiguity
2. Present in digestible sections
3. Save to `meta/design-decisions/YYYY-MM-DD-<topic>.md`
4. Transition to /planning-worldbuilding or /writing-science

## Out of Scope

Does NOT write content. Does NOT modify files. Only interrogates and validates.
