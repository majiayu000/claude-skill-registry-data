---
name: cognitive-compile
description: Use when source material must be transformed into a compact, evidence-aware model for learning, decisions, or an Obsidian concept note.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "one-shot"
  assumes: "The source material or a source-grounded summary is available."
  conflicts_with: "Inventing missing claims, erasing provenance, or presenting hypotheses as facts."
---

# Cognitive Compile

<skill_contract>
  <input>Source-grounded material, original question, learning or decision goal, audience, and destination.</input>
  <output>An eight-part evidence-aware mental model separating facts, mechanisms, conflicts, hypotheses, decisions, and action.</output>
  <done>Each material claim retains provenance and uncertainty, and one bounded next action answers the original question.</done>
  <non_goals>Inventing missing claims, erasing contradictions or provenance, or treating interpretation as source fact.</non_goals>

Compile information into a decision-ready mental model. Compression must preserve provenance, uncertainty, contradiction, and the original question.

## Usage Template

Provide: source material, original question, intended decision or learning goal, and preferred destination. Optional: existing wiki concepts to compare.

## Workflow

<intake>

Identify the source boundary, original question, audience, and required fidelity. Label direct source claims, external facts, and analyst inferences before synthesis.

</intake>

<unknowns_gate>

If the source is inaccessible, truncated, or missing the material needed to answer the question, return `INSUFFICIENT_EVIDENCE`. Ask one probe only when its answer changes the compile structure; otherwise proceed with explicit unknowns.

</unknowns_gate>

<execute>

Produce eight compact sections:

1. **Original question** — the problem the material helps answer.
2. **Key facts** — source-grounded claims with locators when available.
3. **Concepts and entities** — stable terms worth linking.
4. **Patterns** — mechanisms, feedback loops, or recurring structures.
5. **Conflicts** — contradictions with the source, prior knowledge, or internal claims.
6. **Hypotheses** — falsifiable interpretations, explicitly labeled.
7. **Decision support** — options, tradeoffs, and what the evidence changes.
8. **Action** — one bounded next test, note, or decision.

Prefer one durable concept note over several thin notes. Preserve source links or block references; do not rewrite immutable source notes.

</execute>

<evaluate>

Verify that every material conclusion traces to evidence or is labeled inference; the original question is answered; contradictions remain visible; and the action follows from the model. Remove summaries that merely restate the source without changing understanding.

</evaluate>

## Failure Protocol

- `NEEDS_INPUT`: the intended question or audience is absent and materially changes the output.
- `INSUFFICIENT_EVIDENCE`: the source cannot support the requested compile.
- `VERIFY_FAILED`: a conclusion lacks traceable evidence; downgrade it to hypothesis or remove it.

## Output Contract

Return `status`, `result` (the eight-section compile), `evidence` (source locators), `unknowns`, and `next_action`.

## Edge Cases

- Two sources disagree: preserve both claims, compare evidence quality, and state what observation could resolve the conflict.
- The source is mostly opinion: compile mechanisms and assumptions, but do not promote assertions into facts.

## Success Metrics

- The result answers one explicit question with traceable evidence.
- Facts, conflicts, and hypotheses are distinguishable at a glance.
- At least one decision or test becomes clearer.

## Quality Gates

- [ ] Source boundary and provenance are explicit.
- [ ] All eight sections are present or marked not applicable with reason.
- [ ] No hypothesis is phrased as established fact.
- [ ] The next action is bounded and verifiable.

</skill_contract>
