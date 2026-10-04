---
name: spec-driven-development
description: Use when user wants to write a spec, create a PRD, or plan a new feature before implementation begins, when .forge/idea-brief.md exists and is ready to formalize, when requirements need to be captured before architecture or planning, or when a feature's scope and acceptance criteria need to be documented.
---

# Spec-Driven Development

## Overview

Turn a feature idea into a structured PRD at `.forge/prd.md` through interview, codebase exploration, and module design. Reads `.forge/idea-brief.md` if it exists to skip already-answered questions. Output feeds `architecture-and-contracts` and `planning-and-task-breakdown`.

## When to Use

- User wants to write a spec, PRD, or product requirements document
- User wants to plan a new feature before touching code
- `.forge/idea-brief.md` exists and is ready to formalize

## When NOT to Use

- `.forge/prd.md` already exists and is current — skip ahead to `architecture-and-contracts`
- Idea hasn't been pressure-tested — run `idea-griller` first
- Change is trivial (config tweak, single function) — just implement with `tdd`

## Context-Loaded Mode

If a comprehensive context document exists (e.g., `context/CONTEXT.md` or similar file with >500 lines of structured research, interviews, or domain analysis), skip the interview steps (Steps 1-3). The context document replaces the user interview — read it in full, extract requirements, and proceed directly to Step 4 (module design). Note in the PRD's Open Assumptions which sections were derived from context document vs. user confirmation.

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "The feature is simple, skip the spec" | Simple features grow. Write the scope down. |
| "I already know what to build" | The interview surfaces what you don't know you don't know |
| "Codebase exploration is optional" | PRDs written without it have wrong module assumptions |
| "User stories take too long" | Thin story list = thin acceptance criteria = broken scope |
| "We can define NFRs later" | NFRs defined late become hard constraints you can't meet |
| "Out of Scope can be empty" | Empty = everything is in scope = infinite scope |

## Red Flags

- Problem statement written from engineer's perspective, not user's
- User stories use passive voice ("system shall") instead of Given/When/Then or actor/want/benefit
- Out of Scope section is empty
- No non-functional requirements recorded
- Module list names files/functions instead of behavioral units
- Release phases not defined — everything is "phase 1"

## Core Process

### Step 0: Read the brief

Check for `.forge/idea-brief.md`. If it exists, read it. Skip questions already answered. Focus on gaps and open assumptions listed in the brief.

### Step 1: Understand the problem

If no brief: ask the user for a detailed description of the problem and solutions they've considered. Let them speak fully before asking follow-up questions.

### Step 2: Explore the codebase (greenfield-aware)

**Conditional.** Before dispatching the Explore agent, check whether a codebase exists:
- If the repo has source files (any `src/`, `lib/`, `app/`, language-specific entry points, or >5 source files at root), dispatch the Agent tool with `subagent_type=Explore`. Understand current architecture, patterns, and where new modules would attach. Verify the user's assertions against the actual code.
- If the repo is **empty or near-empty** (only `README.md`, `package.json`-shaped manifest, `.gitignore`, or no source files at all), **skip the Explore step**. Note in the PRD under "Codebase context": *"Greenfield — no existing code explored."* Do not dispatch Explore against an empty tree; the agent has nothing to find and the wasted turn obscures the actual state.

### Step 3: Interview to shared understanding

Walk down each branch of the design tree, resolving dependencies one at a time. Do not proceed while ambiguities exist. Ask about: edge cases, error paths, personas, NFRs, data lifecycle.

### Step 4: Design the modules

Identify major modules to build or modify. Prefer deep modules — small interface, large implementation, independently testable. Confirm with user. Ask which modules need tests.

### Step 5: Write .forge/prd.md

Create `.forge/` if it doesn't exist. Prepend a `forge:meta` dependency header (`generated_by: spec-driven-development`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/idea-brief.md]` if it exists else `[]` — paths only, never hashes, `generated_from: {.forge/idea-brief.md: <upstream content_hash AT generation time>}` if idea-brief exists else `{}`, `content_hash: <sha256 first 8 of THIS file's body>`) — see [forge-dependency-graph](../../references/forge-dependency-graph.md). Then write using the template below.

## PRD Template

```markdown
<!-- forge:meta
generated_by: spec-driven-development
generated_at: 2026-05-13T12:00:00Z
depends_on: [.forge/idea-brief.md]
generated_from:
  .forge/idea-brief.md: <idea-brief.md's content_hash at this moment>
content_hash: <first 8 chars of sha256 over this PRD's body>
-->

# PRD: [Feature Name]

## Problem Statement
[From the user's perspective — not the engineer's]

## Personas
[Named actor types with goals and context]

## Functional Requirements

### [Requirement group]
- Given [context], When [action], Then [outcome]

## Non-Functional Requirements
- Performance: [specific target]
- Security: [specific requirement]
- Reliability: [uptime / error rate target]

## Data Model
[Key entities, relationships, constraints — no file paths or code]

## Module Design
[Behavioral units to build or modify. Each: name, responsibility, interface shape]

## Release Phases
- **Phase 1 (MVP):** [scope]
- **Phase 2:** [scope]

## Out of Scope
[Explicit list. Non-empty required.]

## Open Assumptions
[Unresolved questions. Empty = suspicious.]
```

## Verification

Before marking complete, confirm:

- [ ] `.forge/idea-brief.md` read if it existed; gaps identified
- [ ] Codebase explored — user's assertions verified against real code
- [ ] All open assumptions from brief addressed or re-noted
- [ ] Problem statement from user's perspective
- [ ] Given/When/Then covers happy path AND error paths
- [ ] Out of Scope non-empty
- [ ] NFRs specific (no "fast" — give numbers)
- [ ] Module list confirmed with user
- [ ] Release phases defined
- [ ] `.forge/prd.md` written and readable

## Fit-Check

Before declaring done, emit one of:

- A short list of specific fit issues observed during this invocation (e.g., "Feature turned out to be a single config tweak — PRD is overscoped for the work; recommend `incremental-implementation` directly next time" / "PRD section on multi-tenancy doesn't apply — this is a single-tenant tool, see #40").
- The explicit line: **"No fit issues observed for this use case."**

Silence is not allowed. See [docs/skill-anatomy.md#fit-check](../../docs/skill-anatomy.md#fit-check-the-meta-honesty-step).
