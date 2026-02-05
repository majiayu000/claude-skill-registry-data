---
name: implementation-prep
description: Use when preparing to implement instructions by reviewing documentation and TODO.md so the actual work starts with a shared plan.
---

# Implementation Preparation

This skill focuses on the preparatory phase: collect every requirement detail, align it with the repository's documentation, and make the TODO list the single source of truth for the implementation plan before writing any code.

## Preparation Flow
1. **Clarify the request.** Repeat back what you heard, surface assumptions, and ask any follow-ups needed to make the scope airtight.
2. **Document reconnaissance.** Hunt for relevant documentation (architecture notes, READMEs, design briefs, API docs, workflow guides) and log the sections that confirm behavior, constraints, or interfaces you will touch.
3. **TODO.md audit.** Open the nearest TODO.md, read its outstanding tickets, and match them against the incoming request. Update it with the new task, references to the docs you read, and links to follow-up questions; if the repo lacks a TODO.md, create one at the project root and mention it in your summary.
4. **Plan synthesis.** Translate everything into a plan that spells out (a) user-visible changes, (b) dependencies, (c) verification steps, and (d) open questions that still need answers.
5. **Share the plan.** Present the doc/TODO references, the plan, and any blocking items back to the requester before touching the codebase.

## Document & TODO Strategy
- Treat documentation as the contract. Highlight exact files/sections that describe the data flows, APIs, or UX patterns the change must respect and keep links handy for teammates.
- Use TODO.md as a living checklist: note what you will do, why it matters, what passes for success, and when you expect to revisit each item. Prefer short, precise sentences (e.g., "Confirm auth flow described in docs/security.md before touching token refresh").
- When multiple docs apply, build a mini "map" inside your plan that notes how they interplay (e.g., "Setup described in docs/ops/deploy.md; UI constraints in design/interaction.md; TODO entry references both so no one misses the coupling").

## Deliverables Before Implementation
- A written summary that links to the docs you read and the TODO.md entries you created/updated.
- A structured task breakdown (e.g., sections for UI, backend, tests, docs) showing what you will work on, dependencies, and verification.
- A list of clarifying questions that remain unanswered.
- A TODO.md entry (or amendment) that the team can follow to see the plan’s status and the next steps.

## When to Use
Apply this skill whenever you receive a new implementation request—feature, bug, refactor, or documentation change—that requires coordination, multiple files, or a clear record of what you learned before you code.