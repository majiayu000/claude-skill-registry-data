---
name: microcopy-polish
description: Improves interface microcopy such as labels, helper text, validation errors, confirmations, buttons, empty states, and status messages while preserving product meaning and page structure. Use when UI text is vague, inconsistent, overly technical, hard to act on, or broader than the available space, but the user does not want an entire page rewritten.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: writer
  audience: product-designers-content-designers-and-frontend-developers
  tags:
    - microcopy
    - content-design
    - ui-writing
    - error-messages
    - form-labels
    - user-feedback
  status: draft
  side_effects: none
---

# Microcopy Polish

## Purpose

Improve short, functional interface text without rewriting the surrounding page. Make each message clear, concise, consistent, accurate, and useful at the moment it appears while preserving product behavior, terminology, and intent.

## When to use this skill

Use this skill when:

- Labels, buttons, helper text, errors, confirmations, empty states, or status messages need refinement.
- UI text is vague, inconsistent, repetitive, overly technical, or difficult to act on.
- A flow needs a consistent voice and terminology across related states.
- Text needs to fit a constrained interface without losing essential meaning.
- The user requests a targeted microcopy review or before-and-after alternatives.

Do not use this skill when:

- The user wants an entire landing page, article, README, or marketing campaign rewritten.
- The main problem is missing interaction states, layout, visual hierarchy, or product behavior rather than wording.
- Legal, medical, security, or policy language may be changed without an authoritative source or reviewer.
- The copy cannot be made accurate without resolving a product decision first.

## Inputs to inspect

- The exact strings and the components or screens where they appear
- The user action, system state, and next available action for each string
- Nearby headings, controls, instructions, and repeated terminology
- Validation rules, error causes, permissions, limits, and recovery behavior
- Product voice, style guidance, glossary, and localization constraints when available
- Screenshots, prototypes, source files, tests, or issue reports that establish context

Inspect the smallest useful surface. Do not broaden a targeted microcopy task into a page-wide rewrite.

## Workflow

1. **Define the boundary.** List the strings and states in scope. Preserve surrounding prose, information architecture, component behavior, and product claims unless the user expands the task.
2. **Recover the context.** For each string, identify who sees it, when it appears, what happened, what the user needs to know, and what they can do next. Mark unsupported assumptions instead of inventing behavior.
3. **Identify the copy problem.** Classify it as ambiguity, missing context, inconsistent terminology, weak action wording, technical jargon, blame, verbosity, duplication, tone mismatch, inaccessible instruction, or inaccurate state feedback.
4. **Preserve meaning and contracts.** Keep required legal meaning, exact product terms, data consequences, input requirements, and distinctions between pending, success, partial success, and failure. Do not promise outcomes the interface cannot guarantee.
5. **Rewrite for the component.** Use the component's job to shape the text:
   - Labels name the information or choice, not an instruction to interact with the control.
   - Helper text supplies requirements or consequences that are useful before action.
   - Buttons state the action and, when ambiguity matters, its object.
   - Errors explain the problem in plain language and give a viable recovery step when one exists.
   - Confirmations state what happened and any important next step; avoid generic success language.
   - Status messages distinguish current activity, completion, interruption, and uncertainty.
   - Empty states explain the relevant condition and offer an appropriate next action without blaming the user.
6. **Make the set consistent.** Align terminology, capitalization, punctuation, tense, person, contractions, and action patterns across related strings. Use one term for one concept.
7. **Check accessibility and inclusion.** Do not rely only on position, color, shape, or sensory directions. Avoid idioms, unnecessary urgency, shame, blame, and ableist language. Keep control names understandable out of surrounding visual context when they may become accessible names.
8. **Stress-test the copy.** Check long values, pluralization, unknown names, destructive actions, offline or delayed outcomes, localization expansion, repeated announcements, and whether the proposed text still matches actual behavior.
9. **Present focused revisions.** Give one recommended version per string by default. Offer alternatives only when a real tone, length, or product tradeoff remains. Explain material changes briefly.
10. **Apply changes only when requested.** If implementation is requested, edit only the confirmed strings and update affected tests, fixtures, snapshots, translations, or documentation as needed.

## Output format

Return:

## Summary

A brief assessment of the main copy issues and the intended improvement.

## Recommended microcopy

| Location or state | Current | Recommended | Reason |
|---|---|---|---|

Use `Not provided` for missing copy. Keep reasons short and tied to clarity, actionability, consistency, accuracy, accessibility, or space.

## Open questions

- List only unresolved product behavior, terminology, policy, or voice decisions that materially affect the copy.

## Validation

- [ ] Each string matches the state and available user action.
- [ ] Product terms and factual meaning are preserved.
- [ ] Errors and destructive actions communicate consequences and recovery clearly.
- [ ] Related strings use consistent terminology and style.
- [ ] The work stays within the requested microcopy boundary.

If files were changed, replace the table's current-copy source with file references where useful and add a concise `Changes made` section.

## Quality bar

The task is complete only when:

- Every recommendation is grounded in the string's actual context and behavior.
- The wording is specific enough to act on without adding unsupported claims.
- Concision does not remove requirements, consequences, recovery guidance, or meaningful state distinctions.
- Control labels remain understandable and distinct when read independently.
- Related states form a coherent sequence rather than a collection of isolated rewrites.
- Full-page narrative, brand strategy, and interaction redesign remain out of scope unless explicitly requested.

## Edge cases

- If context is missing, provide a conditional recommendation and name the assumption.
- If a character limit is supplied, count against it and do not hide essential information merely to fit.
- If space is tight, move nonessential explanation to helper text only when the interface supports it; do not rely on placeholders as labels.
- For destructive actions, distinguish the action trigger, confirmation prompt, completion message, and undo or recovery state.
- For security and authentication errors, avoid revealing sensitive account or system details.
- For asynchronous operations, do not say an action succeeded while it is queued, processing, or uncertain.
- For localized products, avoid wordplay and account for text expansion, grammar, variables, and plural forms.
- If source strings are shared across contexts, flag the coupling before changing wording for only one use.

## Related skills

- `interface-state-coverage-review`
- `user-recovery-flow-planner`
- `ui-design-direction-builder`
