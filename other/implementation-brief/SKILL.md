---
name: implementation-brief
description: Present a tentative, code-level approach for an already-planned application feature, fix, refactor, or maintenance change. Use to review likely module and function responsibilities, state ownership, configuration, and test seams before coding; not for implementation, scaffolding, or high-level requirements discovery.
---

# Implementation Brief

Present a plausible internal implementation approach for a planned application
change. This is a read-only design briefing, not a demand for a complete coding
blueprint. Unsettled details are expected and may remain delegated to the
implementing agent.

Primarily intended for feature additions and maintenance of existing apps. It
can also address a bounded part of a new project without attempting a complete
implementation design for the whole application.

## 1. Establish the change and code context

1. Identify the specific planned change and relevant high-level decisions from
   the conversation, project guidance, and specifications. Assume the intended
   feature has already been planned; do not reopen ordinary requirements work.
2. Reuse context and inspection findings already available in the session.
   Inspect only affected source, adjacent call sites, tests, and interfaces
   needed for useful implementation-level judgment. If code is unavailable,
   distinguish proposals from repository-verified facts.
3. Separate user-imposed constraints and existing contracts from advisory
   preferences, conventions, and the agent's own suggestions. Do not promote
   proposals or incidental examples into fixed requirements.
4. If the target change or its fundamental intended behaviour cannot be
   identified, stop and state that high-level blocker. Missing function names,
   algorithms, or other normal coding decisions are **not** blockers.

## 2. Form a provisional implementation approach

Discuss only the implementation decisions where advance consideration is
useful. Depending on the change, these may include:

- Affected files or modules and their cohesive responsibilities; distinguish
  existing paths from proposed additions.
- Likely entry points, orchestration, helper responsibilities, and delegation
  boundaries, avoiding unnecessary god functions, duplication, or trivial
  wrappers.
- Data flow and ownership of mutable state, configuration, and consequential
  defaults.
- Interfaces, error handling, dependency boundaries, and test seams where
  they materially influence implementation.
- Compatibility with existing patterns and explicitly prescribed implementation
  rules, including any fixed function signatures or scaffolds.

Prefer a few meaningful design decisions over an exhaustive function inventory.
Use examples or sketch-level signatures only when they clarify a consequential
choice. Leave algorithmic details and incidental structure open for coding.

## 3. Present decisions at their actual certainty

1. Present the likely implementation shape and explain important choices
   concisely, in proportion to the size of the change.
2. Make the status of consequential details clear:
   - **Established:** Explicit user decisions, project contracts, or facts
     confirmed from the existing code.
   - **Proposed:** The agent's recommended structure, subject to revision
     during implementation.
   - **Deferred:** Matters not yet known or not worth fixing before coding.
3. Treat **"not determined yet"** as a valid result. Do not fabricate precise
   implementation decisions to complete a checklist or demand user input for
   matters appropriately delegated to the agent.
4. Highlight an unresolved choice for user intervention only if it conflicts
   with an explicit constraint or materially changes an outcome the user must
   decide. Otherwise report it as provisional or deferred, without questioning.
5. Before presenting, assess the expected output size and choose an appropriate
   level of abstraction. If a detailed walkthrough would be lengthy, summarise by
   component, responsibility, and consequential design decision instead. Do not
   narrate algorithms, enumerate routine implementation steps, or produce
   extensive pseudocode unless explicitly requested.

## 4. Stop at the briefing

- Return a text presentation in the conversation, not slides or a permanent
  design artifact unless separately requested. Scale the detail from a brief
  fix to a more substantial change.
- Do not grill the user, seek approval, edit code, add scaffolds, run tests,
  or initiate implementation. In particular, do not invoke
  `implementation-seeding` automatically; that skill writes source anchors.
- Finish after the presentation, or after reporting a fundamental high-level
  blocker under section 1.
