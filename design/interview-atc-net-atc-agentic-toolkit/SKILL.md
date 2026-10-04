---
name: interview
description: Conduct a structured interview about a feature or topic to gather requirements and produce a specification. This skill should be used when users want to think through a feature, clarify requirements, or create an implementation plan before coding.
disable-model-invocation: true
user-invocable: true
argument-hint: "<topic or feature description>"
---

# Interview

Conduct a detailed interview to gather requirements and produce a written specification. The interview starts broad (problem discovery) and progressively converges toward a concrete implementation plan.

$ARGUMENTS

## Critical Rules

**ALWAYS:**
- Explore the codebase BEFORE asking questions — understand existing patterns, models, and domain concepts first
- Use `AskUserQuestion` for every interview question — never assume answers
- Ask ONE focused question at a time (with 2-4 options when appropriate) — avoid walls of questions
- Write the final plan to a file, not just chat output
- Write the plan in the same language the user uses

**NEVER:**
- Skip Phase 1 (context gathering) — uninformed questions waste the user's time
- Ask more than 2 questions per turn
- Continue interviewing when you have enough information — converge and write the plan

## Phase 1: Context Gathering

Before asking any questions, silently explore the codebase to understand:

1. **Existing architecture** — project structure, key patterns, frameworks in use
2. **Related features** — similar functionality that already exists
3. **Domain concepts** — models, entities, terminology from the codebase and docs/
4. **Conventions** — naming, file organization, testing patterns

This phase is silent — do not narrate what you're reading. Use the knowledge to ask informed questions.

## Phase 2: Interview

### Calibration (First Question)

Start by understanding the scope. Based on the user's initial description and what you found in Phase 1, calibrate the interview depth:

- **Small** (bug fix, config change, minor tweak): 2-4 questions, focus on the specific problem
- **Medium** (new endpoint, new component, feature extension): 4-8 questions, cover happy path + edge cases
- **Large** (new subsystem, architectural change, cross-cutting feature): 8-15 questions, cover all areas below

Tell the user the estimated scope and question count so they know what to expect.

### Interview Flow

Progress through these stages in order. Skip stages that don't apply to the scope.

#### Stage 1: Problem Discovery
- What problem does this solve? Why now?
- Who are the users? What are their goals?
- What happens today without this feature?

#### Stage 2: Solution Shape
- What does the happy path look like end to end?
- What variations or modes exist?
- How does this interact with existing features?

#### Stage 3: Edge Cases & Constraints
- What can go wrong? How should errors be handled?
- Are there performance, security, or data constraints?
- What is explicitly out of scope (for now)?

#### Stage 4: Implementation Details
- Data model implications — new entities, schema changes, migrations?
- UI/UX flow and states (if applicable)?
- API surface — endpoints, contracts, versioning?
- What needs to be tested? What are the acceptance criteria?

### Convergence Criteria

Stop interviewing when ALL of these are true:

1. You can describe the happy path without any gaps
2. Error handling and edge cases are addressed
3. The technical approach is clear (no hand-waving)
4. Scope boundaries are explicit (what's in, what's out)

If you're unsure whether you have enough, ask one final confirmation question summarizing your understanding and asking if anything is missing.

## Phase 3: Write the Plan

Write the plan to a markdown file in the project. Default location: `docs/plans/` directory, or the project root if no docs/ exists. Use a descriptive filename based on the feature (e.g., `docs/plans/user-export-feature.md`).

Ask the user where to save it if the location isn't obvious.

Follow the template in `references/plan-template.md` for structure. Adapt sections based on scope — small features don't need every section.

### After Writing

- Show the user the file path
- Offer to refine any section
- If the user wants to iterate, update the file in place rather than rewriting from scratch
