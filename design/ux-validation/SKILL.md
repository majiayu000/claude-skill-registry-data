---
name: ux-validation
description: Turn a user journey into a state-complete prototype and usability validation plan. Use for information architecture, accessible interactions, responsive behavior and prototype feedback. Does not contact users or collect data automatically.
---

# UX validation

Status: Draft. Not yet verified in a documented practical example.

Input: audience, primary task, requirements, existing design system and accessibility target. If research is missing, label the audience and journey as assumptions.

## Procedure

1. **Map.** Describe entry points, navigation, content hierarchy, user goal and successful exit. Identify constraints and reuse existing design-system components. Start with a text flow or low-cost wireframe.
2. **Specify states.** For each action cover initial, loading, empty, validation error, partial failure, success, cancellation and recovery. Explain duplicate submissions, irreversible actions and ambiguous outcomes.
3. **Check access.** Define keyboard order, focus changes, accessible names, error announcements, contrast and responsive behavior. Cite the project's accessibility target or propose one for approval. Inspection alone is not accessibility conformance evidence.
4. **Plan observation.** Write realistic tasks without coaching users toward the answer. Define representative recruitment criteria, consent, data minimization, success measures and stop rules. Do not recruit, record or process participant information without explicit approval.
5. **Evaluate.** Separate observed behavior from interpretation and proposed changes. Record prototype revision, context, checks run and limitations. Prioritize severe obstacles, retest changes and hand observable acceptance checks to QA.

## Output

| Journey / action | Expected state or transition | Accessibility check | Evidence / not run | Next change |
| --- | --- | --- | --- | --- |
| Create a synthetic task | Validation explains a missing title and keeps entered text | Error is associated with the input; focus is predictable | Proposed, not tested | Verify prototype |

Return the flow, state matrix, validation plan or actual findings, and unresolved design decisions. Never invent usability sessions, quotes or representative-user approval. Image generation and production UI changes are separate requests.
