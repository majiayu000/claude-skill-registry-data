---
name: aep
description: Analyse-Explore-Plan methodology for thorough analysis and planning before development. Use when starting a new feature, investigating a problem, or needing to understand a codebase before making changes. Provides structured workflow with parallel exploration agents and clarification questions. Integrates with Architect skill for high-quality implementation plans.
---

# AEP Skill - Analyse, Explore, Plan

This skill defines the methodology for thorough analysis and planning before any development work.
It conditions all future context and decisions.

## Overview

AEP is a three-phase workflow designed to ensure deep understanding before implementation:

1. **Analyse** - Understand what the user really needs
2. **Explore** - Investigate the codebase thoroughly
3. **Plan** - Create a detailed implementation strategy

## Phase 1: ANALYSE

Deeply analyze the user's request by answering these questions:

### Core Understanding
- What is the core problem or need?
- What are the implicit requirements not explicitly stated?
- What constraints can be inferred from the context?
- What is the expected outcome or deliverable?

### Intent vs Literal
Think carefully about what the user **really wants** vs what they **literally said**.
Often the literal request is a symptom of a deeper need.

### Success Criteria
- How will we know the implementation is successful?
- What are the acceptance criteria?

## Phase 2: EXPLORE

Launch **up to 3 Explore agents IN PARALLEL** to thoroughly investigate the codebase:

### Agent 1: Existing Implementation
Search for:
- Similar patterns already in the codebase
- Related code that might be affected
- Existing solutions that could be reused or extended
- Code that does something similar we can learn from

Tools: `Glob`, `Grep`, `Read`

### Agent 2: Dependencies & Architecture
Understand:
- How this fits in the current architecture
- What dependencies exist (imports, services, modules)
- What will be impacted by changes
- Architectural constraints or patterns to follow

Tools: `Glob`, `Grep`, `Read`

### Agent 3: Test Patterns
Find:
- How similar features are tested
- Existing test utilities or helpers
- Test coverage expectations
- Integration vs unit test patterns used

Tools: `Glob`, `Grep`, `Read`

### Exploration Rules

1. **Use tools extensively** - Read more code than you think necessary
2. **Follow the breadcrumbs** - One file often leads to another
3. **Check documentation** - README, docs/, comments in code
4. **Look at recent changes** - `git log` can reveal context
5. **Thoroughness > Speed** - This phase conditions everything

## Phase 3: CLARIFY

Based on analysis and exploration, identify and ask about:

### Must-Clarify (blockers)
- Ambiguities that could lead to wrong implementation
- Technical choices that require user decision
- Scope boundaries that are unclear
- Conflicting requirements

### Should-Clarify (important)
- Priority between competing approaches
- Performance vs simplicity trade-offs
- Edge cases handling preferences

### Rule
**Do NOT proceed to planning if you have unresolved questions that could lead to wrong implementation.**

Ask questions using clear, specific language. Propose options when possible.

## Phase 4: PLAN

**IMPORTANT**: Before creating the plan, read and apply the Architect skill from `~/.claude/skills/architect/SKILL.md`.

The Architect skill provides:
- Phase design checklists (scope, files, dependencies, validation, rollback)
- Plan-level checklists (completeness, ordering, testing, risks)
- Universal patterns (feature flags, strangler fig, safe migrations)
- Anti-patterns to avoid (big bang phases, hidden dependencies, etc.)

### Apply Architect Guidelines

1. **Read the Architect skill** to internalize the principles
2. **Design phases** following the atomic phase rules (max 3 files, single goal)
3. **Order by risk** (infrastructure first, migrations last)
4. **Run checklists** on each phase before finalizing
5. **Document architectural decisions** when non-obvious choices are made

### Plan Structure

Create a detailed implementation plan with:

#### Context
- Summary of what you understood
- Key findings from exploration
- Assumptions made (if any)

#### Architectural Decisions (if applicable)
- Non-obvious technical choices
- Options considered and rationale
- Consequences for implementation

#### Approach
- Chosen technical approach
- Justification for the approach
- Alternatives considered and why rejected

#### Implementation Phases
For each phase, include:
- **Goal**: Single, clear objective
- **Files**: Explicit paths (max 3 per phase)
- **Dependencies**: What must be done before
- **Validation**: Concrete command or check
- **Commit message**: Conventional format

#### Risks & Mitigations
- What could go wrong
- How to handle each risk
- Fallback strategies

#### Testing Strategy
- How to validate the implementation
- What tests to write/modify
- Manual verification steps if needed

## Output Language

**ALL OUTPUT MUST BE IN FRENCH** - Questions, analysis, plan, everything communicated to the user must be written in French.

## Critical Rules

1. **NEVER rush through exploration** - This phase conditions everything
2. **ALWAYS ask questions** if something is unclear
3. **PREFER reading more code** than making assumptions
4. **THINK deeply** about edge cases and implications
5. **DOCUMENT your reasoning** for future reference
6. **Use parallel agents** for exploration efficiency

## Thinking Mode

**ULTRATHINK** - Use maximum reasoning tokens for this workflow.

This methodology requires deep analysis. Allocate maximum thinking capacity to:
- Thoroughly analyze the request and its implications
- Consider all edge cases and architectural impacts
- Evaluate multiple approaches before choosing one
- Anticipate potential issues and their mitigations
