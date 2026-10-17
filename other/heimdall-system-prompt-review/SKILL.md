---
name: heimdall-system-prompt-review
description: Review agent definitions and system prompts for behavioral coverage, failure modes, and stakeholder impact through simulation and adversarial probing.
---

# System Prompt Review

## Purpose

Review system prompts (agent definitions, role prompts, skill instructions) by independently simulating and probing them — not by conformance-checking against the writer's rubric. A prompt is a program; judge it by predicted behavior under stress, not prose quality.

The core insight is **reference-but-not-mirror**. The writing principles are a *diagnostic vocabulary* applied after findings surface, not the method of finding them. The review's method is simulation, probing, and consequence-tracing — operations with no counterpart in writing. The writing principles organize findings; they do not generate them.

## When to Use

- When reviewing an agent definition, system prompt, role prompt, or SKILL.md file.
- Before a prompt ships, to verify predicted behavior under normal, edge, and adversarial conditions.
- When the prompt's behavioral specification — not its prose — is the evaluation target.

This differs from documentation review: documentation review asks "can a reader understand this?"; this skill asks "will an agent behave correctly under this specification?" Different evaluation targets. Prose quality, domain security, and accessibility belong to the sibling domain skills; this skill evaluates behavioral specification quality.

## Workflow

1. **Reconstruct purpose, with disclosure.**
   - State from the artifact plus its deployment context: "This prompt defines an agent that does X, receives Y, produces Z, and must not do W."
   - Reconstruct *purpose* (what the prompt is for), not *intent* (what the writer was thinking). Disclose the reconstruction so it can be checked. If purpose cannot be reconstructed, that is itself a blocking finding.

2. **Simulate behavior before checking structure.**
   - Walk three scenario classes and state the *predicted behavior* for each: (a) normal case — typical input, expected path; (b) edge case — tool failure, malformed input, missing fields, ambiguity; (c) worst case — contradictory instructions, impossible request, adversarial or injection-style payload.
   - Generate at least one adversarial input designed to break the prompt. If prediction is ambiguous or unspecified, that is a finding — not a guess. Simulation precedes structure-checking: a prompt can satisfy every structural principle and still produce catastrophically wrong behavior.

3. **Probe for unspecified behavior.**
   - Enumerate decision points where the agent must choose and the prompt specifies no rule — each defaults to an uncontrolled training prior.
   - For each constraint pair, construct an input where both apply; if precedence is unspecified, that is a finding. For every major action, ask what happens when it fails; missing failure behavior is the most common defect.

4. **Check coverage — using writing principles as diagnostic vocabulary, not a checklist.**
   - Coverage target: input classes, output contracts, failure behavior, boundaries, invariants, decision rules.
   - Map each finding to a writing principle as a *label after surfacing it* ("unspecified decision point" → principle 7), so feedback is actionable. The principle number categorizes; it does not generate findings.
   - Distinguish structural absence from contextual necessity — a pure function with no I/O needs no tool-unavailability handling. Suppress contextually unnecessary findings; over-flagging erodes trust.

5. **Evaluate system-context fit.**
   - Does the prompt conflict with sibling agents, create role overlap, duplicate an existing skill, or reference unavailable tools? Read at least one sibling prompt and check the prompt follows established structural conventions — invented structure makes it an outlier operators cannot maintain by analogy.

6. **Assess stakeholder impact.**
   - Trace each significant instruction to human consequence: what does the affected party experience when it is followed, when it is not, and at the boundary (ambiguous context, vulnerable user)?
   - Surface invisible stakeholders — who is affected who is not represented in the prompt? Evaluate from the position of the party with the least power to recover. Check unstated user assumptions (developer, English-speaking, no accessibility needs).

7. **Meta-check and deliver verdict.**
   - Ask: are there quality dimensions this prompt needs that the writing principles do *not* cover (injection resistance, accessibility, multi-agent coordination, drift resistance)? Name the gap — the writing skill itself may need evolution.
   - Report by severity, not by principle number: blocking (missing coverage, failed simulation, constraint conflict, safety gap), major (missing failure behavior, untestable output, system-context mismatch), minor (style, ordering, voice).
   - For each finding state: the scenario → predicted behavior → intended behavior → the gap. Do not state "principle 4 violated."
   - **Do not rewrite the prompt.** Identify the defect and the fix's requirements; do not produce the fix. Review that becomes rewrite becomes competing implementation and erodes independence.

## Quality Criteria

- Simulated the prompt through normal, edge, and worst cases — not just read it.
- Constructed at least one adversarial input designed to break the prompt.
- Identified what the writing principles do *not* cover for this prompt's domain.
- Represented stakeholders who are not in the room — especially the party with the least power to recover from a failure.
- Each finding names a scenario, a predicted behavior, an intended behavior, and a gap — not a principle number alone.
- Suppressed contextually unnecessary findings; over-flagging is as harmful as under-flagging.

## Anti-Patterns

- **Conformance-checking**: grading against the writer's own rubric. Shares the writer's blind spots; produces the illusion of independent review.
- **Checkbox theater**: mirroring the writing principles as a checklist. Produces compliance theater, Goodhart convergence, and stasis lock.
- **Skipping simulation**: reading the prompt without walking scenarios. A prompt can read well and behave catastrophically.
- **Ignoring system context**: evaluating the artifact in isolation, missing conflicts with sibling agents or unavailable tools.
- **Rewriting instead of reviewing**: producing the fix rather than the finding. Erases independence and creates competing implementation.
- **Treating principles as the method**: using "check that principle N was followed" to generate findings, rather than as a diagnostic label applied after simulation surfaces them.
- **Over-flagging**: reporting every structural absence as a defect regardless of contextual necessity. Erodes trust and buries blocking findings.
