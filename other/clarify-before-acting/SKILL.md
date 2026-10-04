---
name: clarify-before-acting
description: Surfaces ambiguity in one sentence and asks before acting, rather than silently picking. Use when a request supports more than one reasonable interpretation, when an external value the request does not pin down is required, when a project-specific convention must be chosen, or when an unexpected state of the world is encountered.
derives_from: ../../governance/clarify-before-acting.md
---

# Clarify Before Acting

## Overview

Silent picks impose unwind cost on the requestor when the pick turns out wrong. This skill catches the ambiguity before action, surfaces it as a one-sentence question with named alternatives, and lets the requestor resolve it cheaply before the work commits.

The discipline is from the canonical rule [`governance/clarify-before-acting.md`](../../governance/clarify-before-acting.md), which is the source of truth for the full ambiguity-detection taxonomy, the ask-vs-default decision rule, the tool-specific guidance, and the framework-alignment table. This skill is the workflow wrapper: ambiguity detection and the question-formulation format.

## When to Use

- The request supports more than one reasonable interpretation, and the implementations would diverge materially.
- An external value the request does not pin down is required to proceed (a date, a timezone, a library version, a target branch, an output format, a file path, a permission level, a default behaviour for an edge case).
- A project-specific convention must be chosen (whether to bump a per-document version, whether to add a CHANGELOG entry, whether to land on a feature branch or a phase branch, whether tests are required for this kind of change).
- A trade-off must be made that the requestor would reasonably want to weigh in on (backwards compatibility vs cleanliness, performance vs readability, breadth-of-fix vs scope-of-PR).
- The state of the world is unclear (an unfamiliar branch exists, a lock file is present, a partially-applied migration is detected, a stash with content is found). Investigate first, then ask whether to preserve, resolve, or discard.

Before the ask-vs-default decision, run the **compute-first gate**: if the answer is a findable fact the assistant can retrieve itself (a file location, a citation, a count, a version, where a term is used in the project, what a document currently says), retrieve it with a `grep` or a read and surface the answer, do not ask the requestor for it. The ask-vs-default test governs only the genuine ambiguities and authorial choices that survive this gate, never findable facts.

Not all ambiguity warrants asking. If the wrong-guess cost is bounded to a quick edit AND a sensible convention exists in the project, the language community, or the immediate context, default and document the default in the response so the requestor can override it. Ask when the wrong choice would produce work the requestor would want to unwind, or when the choice has consequences beyond this PR (target branch, public API shape, dependency choice, security-sensitive default).

## Process

The clarification format from the canonical rule, applied to each detected ambiguity:

1. **One sentence**. The user reads one line, picks an answer, and the work proceeds. Multi-paragraph clarifications hide the actual decision and create friction.
2. **Named alternatives**. List two-to-four specific options. Open-ended "what should I do?" pushes the work back onto the requestor; named alternatives let them pick.
3. **Recommended option, if one stands out**. Identify it as "(recommended)" and put it first. The requestor can accept the recommendation with a one-word confirmation or pick a different option.
4. **State the consequence**. One short clause per option explaining what that option implies, so the requestor can answer without re-reading the request.

When a structured-question primitive is available (for example `AskUserQuestion` in Claude Code), prefer it over open-ended chat. Pass a complete one-sentence question, 2-4 named options as a closed set, the recommended option labelled and listed first when one stands out, and a one-line description per option explaining the consequence. The primitive produces a structured answer that is easy to parse and audit.

A clarification is not a request to re-explain the original task. The requestor explained it; the assistant's job is to identify the specific ambiguity and resolve it with minimal friction.

## Red Flags

- Asking the requestor for a fact a `grep` or file read would answer, instead of retrieving it (the compute-first gate fires before the ask-vs-default decision).
- Silently picking when the wrong guess would require unwinding.
- Asking after acting ("I went ahead and used branch X; want me to switch?" is post-hoc consent-seeking, not a clarification).
- Asking trivia (pinging the user for every micro-decision that has a sensible default; signal-to-noise erodes and eventually the user hand-waves "do whatever", which collapses the discipline back into silent picking).
- Hiding the ambiguity in narration ("I will pick X, but let me know if that is not right" is a silent pick with a fig leaf).
- Treating a previously-given answer as durable when the scope has changed (last week's authorization is for last week's scope, not this week's different task).
- Combining a leading recommendation with sham alternatives ("Should I do X (which is obviously what you want) or Y (which makes no sense)?" is theatre, not a real clarification).
- Asking a question that requires the user to scroll back to context (the question should be self-contained).

## Verification

The clarification is verified when:

- The ambiguity has been named in one sentence.
- 2-4 specific options have been listed as a closed set.
- A recommended option is identified when one option stands out, and labelled `(recommended)`.
- The consequence of each option is stated in one short clause.
- The question is self-contained: the user can answer without re-reading the original request.

If the structured-question primitive is in use, the same five properties apply to its `question`, `options`, and per-option `description` fields.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I will just pick the obvious one; the user can correct me later." | The user pays the unwind cost. The cost of one extra clarification is always lower than the cost of unwound work. |
| "I do not want to bother the user with a small question." | The signal that a question is "small" is that the wrong-guess cost is bounded. Defaulting and documenting the default is fine in that case. Surfacing it before acting is fine in any case. |
| "I will pick now and ask if it turns out wrong." | The wrong-pick discovery is the unwind. By that point, the work is done. |
| "The plan I submitted earlier covered this." | Plan-mode approvals stand for the scope they cover, not for ambiguities the plan glossed over. |

## See Also

- Canonical rule [`governance/clarify-before-acting.md`](../../governance/clarify-before-acting.md): the five ambiguity-detection categories (multi-interpretation requests, missing external values, project-convention choices, trade-offs, unclear world state), the ask-vs-default decision rule with concrete examples on each side, tool-specific guidance (structured-question primitives, plan mode, investigation-first, scope-creep surfacing), exception cases (pre-authorized durable instructions, emergency response, reversible exploration), and the framework-alignment table.
- Related skill [`evidence-grounded-completion`](../evidence-grounded-completion/SKILL.md): handles verification after action. This skill handles ambiguity before action; the two are complementary halves of the agent-collaboration discipline.
- Related skill [`gate-discipline-diagnose`](../gate-discipline-diagnose/SKILL.md): when a gate failure exposes an ambiguity in how to respond, use this skill before picking a response.
- Related skill [`validation-sweep`](../validation-sweep/SKILL.md): when the project-wide sweep surfaces an out-of-window finding, use this skill to triage the ambiguous "action / defer / dismiss" choice with named alternatives rather than auto-deferring.
- Related skill [`fresh-reader-validation`](../fresh-reader-validation/SKILL.md): when the fresh reader surfaces an ambiguity the document chose not to resolve, use this skill to surface the choice before completing the document.
- Related skill [`surface-instruction-concern`](../surface-instruction-concern/SKILL.md): the harm-side counterpart, for the instruction that is clear but counterproductive to execute as given.
