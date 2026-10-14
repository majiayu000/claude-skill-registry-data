---
name: requirements-clarify
description: Runs a structured Q&A session before starting any ambiguous task. Asks one question at a time using multiple choice first, surfaces assumptions, confirms understanding. Use when the user gives vague requests, incomplete specs, conflicting goals, missing context, or says anything like "build this", "make it work", "fix it", "implement feature", "refactor this", "add functionality", or any task where you need to clarify scope, constraints, or requirements before starting work. Not for simple well-defined tasks.
---

# Requirements Clarification

## When to Use

This skill activates **before** any non-trivial or ambiguous task. If the user's request is well-defined (single file change, clear bug fix with reproduction steps, obvious refactor with explicit scope), skip this skill.

Use when the request lacks:
- Clear scope or boundaries
- Success criteria
- Constraints (performance, compatibility, security)
- Context about affected systems
- Acceptance criteria

## Core Rule: One Question at a Time

Ask exactly one question per turn. Do not batch questions. Wait for the answer before proceeding.

This is the single most important rule. Multiple questions overwhelm the user and produces worse information.

## Questioning Funnel

Start broad, then narrow based on each answer. Do not skip levels unless the answer already provides the detail.

### Level 1 — Goal
*"What are you trying to accomplish?"*

Listen for: build vs fix vs change vs learn vs explore. Adjust all subsequent questions to match.

### Level 2 — Scope
*"What's the scope here — one file, a few files, multiple projects, or something architectural?"*

If the user says "I don't know," suggest concrete options: "Does it touch the frontend, backend, both, or something else?"

### Level 3 — Specifics
*"What specifically should change or be different when this is done?"*

Probe for concrete deliverables: new endpoint, modified behavior, removed feature, performance target.

### Level 4 — Constraints
*"Any constraints I should know about? Performance, compatibility, security, timeline?"*

Only ask if not already volunteered. Phrase as multiple choice when possible: "Are there performance requirements, security concerns, or specific compatibility targets?"

### Level 5 — Context
*"Have you already looked at anything related to this, or have any hunches about what needs to change?"*

Captures prior investigation, saves redundant exploration.

## Questioning Techniques

### Multiple Choice First

Prefer closed questions with options over open-ended ones:

Good: *"Should this be A) a new route, B) a modification to the existing one, or C) something else?"*
Bad: *"How should we handle this?"*

Open-ended is acceptable only when you genuinely cannot list reasonable options.

### Assumption Surfacing

When you have an assumption, state it explicitly and ask for confirmation:

*"I'm assuming this needs to work with the existing auth system. Is that correct?"*

After confirmation, do not re-ask. Move to the next unknown.

### Trade-off Questions

When multiple valid approaches exist, frame the trade-off:

*"Option A is faster to build but less flexible. Option B is more flexible but more complex. Which matters more here?"*

### Clarification Through Examples

When requirements are vague, offer a concrete example:

*"Just to make sure I understand — when you say 'dashboard', do you mean something like an admin panel with tables and charts, or a personal homepage with recent activity?"*

## Confirmation Step

After the Q&A, summarize your understanding and confirm before starting work:

*"Let me confirm what I'm hearing: [2-3 sentence summary]. Is that accurate?"*

Do not begin implementation until the user confirms or corrects the summary.

## Edge Cases

### User says "I don't know" or "You decide"
Pick the most reasonable default, state it clearly, and confirm: *"I'll go with [option] unless you say otherwise. Good?"*

### User gives partial requirements upfront
Skip questions already answered. Only ask about what's still unclear.

### User is clearly frustrated or in a hurry
Ask fewer questions. Prioritize: scope > specifics > constraints. Omit nice-to-have clarification.

### Requirements change mid-implementation
Stop. Re-confirm scope. *"That changes [x]. Just to confirm the new scope: [summary]. Correct?"*

## Anti-patterns

- **Mind reading**: Do not assume unstated requirements. Ask.
- **Premature implementation**: Do not start coding before confirmation step.
- **Question dumps**: Never ask more than one question per message.
- **Leading questions**: Do not steer the user toward your preferred approach. Present options neutrally.
- **Ignoring answered questions**: If the user already gave you scope, do not ask for it again.

## Bundled Script

Copy `clarify-requirements.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/requirements-clarify/scripts/clarify-requirements.ps1 .ai_scripts/
```

Generates a structured requirements template for a feature or task:

```powershell
.ai_scripts\clarify-requirements.ps1 -Topic "dark mode toggle" -OutputFile REQUIREMENTS.md
```

## Cross-references

- **code-collaborate-qa** — Both structure ambiguous requests. requirements-clarify handles general requirements; code-collaborate-qa handles code-specific questions.

- **anti-sycophancy** — Structured clarification prevents the AI from agreeing to a vague request.

- **break-repetitive-patterns** — Repetitive questions often mean requirements need clarification.
- **skill-loader** — Apply the capped selection policy when deciding which requirements or loop-breaking skills should also be active.
