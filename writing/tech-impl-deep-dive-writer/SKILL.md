---
name: tech-impl-deep-dive-writer
description: Write mechanism-first technical implementation deep-dive articles for system/design/code explanations. Use when users ask for detailed implementation docs or engineering blog posts that must explain principles, data flow, trade-offs, and operations, and avoid source-location dumps or flashy/non-structured headings.
---

# Tech Implementation Deep-Dive Writer

Use this skill to produce technical implementation articles that read like serious engineering docs, not code-location inventories.

## Load References
- Required: `references/style-contract.md`
- Required: `references/outline-template.md`

## Writing Contract (Mandatory)
1. Use declarative, noun-phrase headings.
2. Do not use question-style titles in TOC headings.
3. Do not use sensational or marketing wording.
4. Keep a clear total-to-detail hierarchy (`##` for major layers, `###` for mechanisms).
5. Explain design intent and mechanism first; place code locations as supporting evidence only.
6. Keep source-index lists in an appendix section, not as the body core.

## Workflow
1. Clarify scope and boundaries of the article.
2. Define the core model (entities, events, invariants, constraints).
3. Explain the end-to-end data flow before component internals.
4. Expand each core mechanism with: purpose -> how it works -> failure modes.
5. Add architecture trade-offs and alternatives.
6. Add operations playbook (diagnostic or recovery flows).
7. Add a compact code index appendix.

## Body Structure
Use this sequence by default unless the user asks for a different structure:

1. Background and goals
2. Model and terminology
3. End-to-end architecture/data flow
4. Mechanism deep-dives (group by flow, not by file)
5. Storage/query/runtime behavior
6. UI/ops integration (if applicable)
7. Trade-offs and boundaries
8. Operations playbook
9. Code index appendix
10. Summary

## Mechanism Explanation Standard
For each major mechanism, include:
1. Problem statement: what this mechanism must solve.
2. Design decision: what was chosen and why.
3. Execution path: step-by-step runtime behavior.
4. Failure handling: what happens when inputs or dependencies are abnormal.
5. Practical signal: how operators/debuggers can observe or verify it.

## Quality Gates Before Final Output
1. Heading quality: no question headings, no inflated wording, consistent noun-phrase style.
2. Structure quality: major sections form a complete total-to-detail chain.
3. Explanation quality: every major section answers both "why" and "how".
4. Evidence quality: code references support claims but do not dominate narrative.
5. Operational quality: include at least 2 concrete troubleshooting scenarios.
6. Comparison quality: include at least 1 explicit trade-off table.

## Anti-Patterns (Must Avoid)
- Dumping large blocks of file:line pointers as the main content.
- Repeating "implementation at X" without explaining design rationale.
- Mixing architecture, API details, and UI details without section boundaries.
- Using vague chapter names such as "Other" or "Misc".
- Overusing slogans like "ultimate", "best", "revolutionary", "shocking".

## Output Policy
- Keep the main body explanation-first.
- Keep code index short and grouped by subsystem.
- Use diagrams and tables when they clarify mechanism or trade-off.
- Keep terminology stable once defined.
