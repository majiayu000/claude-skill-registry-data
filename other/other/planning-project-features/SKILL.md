---
name: planning-project-features
description: Create implementation plans for features within a single project. Decomposes work into self-contained sub-plans with iterative multi-agent review. Use when planning new features, refactoring efforts, or any multi-step implementation. Never assumes or fills in gaps - always asks for clarification until requirements are complete.
---

# Planning Project Features

Create thorough, actionable implementation plans for features within a single project. **Never assume or guess** — ask until every gap is filled.

Plans are decomposed into a **master plan** (high-level orchestration) and **sub-plans** (self-contained, independently executable units). Before finalization, plans go through an **iterative multi-agent review loop** that surfaces architectural issues, risks, and implementation problems. This structure ensures that even the least capable executing agent can pick up a sub-plan and succeed without additional context.

## Core Principles

1. **No Assumptions**: If something is unclear, ambiguous, or missing — ask. Do not fill in gaps with reasonable defaults or best guesses.
2. **Relentless Clarification**: Ask as many questions as needed. A plan built on assumptions is worse than no plan.
3. **Atomic Decomposition**: Break work into the smallest self-contained sub-plans possible. Each sub-plan should be executable in isolation.
4. **Embedded Context**: Each sub-plan includes everything an executing agent needs — no reliance on reading other sub-plans or external documents.
5. **Convergent Review**: Plans are reviewed iteratively by specialized sub-agents until no new issues are found.

## Workflow

### Phase 1: Requirement Gathering

Before writing any plan, gather complete information:

1. **Understand the goal**: What problem does this solve? What does success look like?
2. **Identify scope**: What's in scope? What's explicitly out of scope?
3. **Map dependencies**: What existing code/systems does this touch?
4. **Clarify constraints**: Performance requirements? Backward compatibility? Tech stack restrictions?
5. **Define acceptance criteria**: How will we know it's done correctly?

**Ask questions until you can answer all of the above confidently.**

If the user says "just figure it out" or "use your judgment":
1. **First, educate**: Present the options you see, explain trade-offs, and help them make an informed decision
2. **If they persist**: Respect their choice to "vibe-code" and proceed with your best judgment, but document your assumptions clearly in the plan

### Phase 2: Codebase Exploration

Once requirements are clear:

1. **Read existing documentation first**: Check AGENTS.md for documentation pointers, then read relevant docs (domain, architecture, business processes, components). Existing documentation is dramatically cheaper than re-exploring code from scratch.
2. **Explore code only for gaps**: Search for relevant code, patterns, and conventions that documentation doesn't cover.
3. Identify files that will need modification
4. Note any architectural constraints or patterns to follow
5. Flag potential conflicts or risks
6. **Identify required skills**: Determine which skills (both global from `~/.claude/skills/` and local from `.claude/skills/`) an executing agent will need to follow project conventions correctly (e.g., `writing-go-code` for Go changes, `managing-chezmoi` for dotfile edits). Check the project's `AGENTS.md` for documented skill mappings.
7. **Flag documentation gaps**: If critical areas needed for the plan are undocumented, note them. Recommend the appropriate documenting skill:
   - Missing domain knowledge → `documenting-domain`
   - Missing architecture overview → `documenting-architecture`
   - Missing business workflow docs → `documenting-business-processes`
   - Missing component docs → `documenting-components`

   Present gaps to the user — they may want to create docs before planning continues, or accept the gap and proceed.

Share findings with the user and confirm understanding before proceeding.

### Phase 3: Decomposition

This is the most critical phase. Break the feature into sub-plans:

1. **Identify natural boundaries**: Look for seams in the work — different layers (data model, API, UI), different domains, or different files/modules.
2. **Minimize dependencies**: Each sub-plan should depend on as few other sub-plans as possible. Where dependencies exist, make them explicit and one-directional.
3. **Embed all necessary context**: Each sub-plan must include the interfaces, data shapes, conventions, and file contents an executing agent needs. Don't assume the agent has read the master plan or any other sub-plan.
4. **Define clear inputs and outputs**: If sub-plan B depends on sub-plan A, sub-plan B must specify exactly what it expects to exist (e.g., "a `UserService` interface in `internal/service/user.go` with methods `Create(ctx, user) error` and `GetByID(ctx, id) (User, error)`").
5. **Keep sub-plans small**: A good sub-plan should be completable in a single focused session. If it feels too big, split it further.

Present the decomposition to the user for review before writing the actual plan files.

### Phase 4: Plan Creation, Reviewer Assignment & Model Selection

Only after Phases 1-3 are complete:

1. **Create the plan directory and files**:

```
.claude/plans/<feature-name>/
├── 00-master.md          # Master plan: overview, ordering, dependencies
├── 01-<first-task>.md    # Sub-plan 1
├── 02-<second-task>.md   # Sub-plan 2
├── reviews/              # Review output (created during Phase 5)
└── ...
```

2. **Discover available local reviewers**: Read the project's `.claude/agents/` directory to find reviewer agents. Match each sub-plan to the most appropriate available reviewer based on the agent's description and the sub-plan's domain.

3. **Assign reviewers**: Write the chosen reviewer's name into each sub-plan's `## Reviewer` field.

4. **Validate**: If no suitable local reviewer exists for a sub-plan's domain, **warn the user** with a specific recommendation (e.g., "sub-plan 03 covers database migrations but no reviewer with that expertise exists in `.claude/agents/`"). Ask how to proceed — do not skip the review silently.

5. **Assign execution models**: For each sub-plan, assess complexity and recommend an execution model. This enables cost optimization by using cheaper models for straightforward work while reserving Opus for planning and review.

**Model Selection Decision Tree**:

| Use Haiku When | Use Sonnet When | Keep Opus For |
|----------------|-----------------|---------------|
| Following established patterns | Novel implementation approaches | Planning & decomposition |
| CRUD operations | Complex business logic | Architecture review |
| Straightforward integrations | Multiple edge cases to consider | Risk assessment |
| Test writing for existing code | Integration of multiple systems | Synthesis & coordination |
| Configuration changes | Performance-critical code | Multi-step reasoning |
| Documentation updates | Security-sensitive operations | Ambiguous requirements |
| File moves/renames | State machine implementations | |
| Simple data transformations | Error handling with recovery logic | |

**Assessment criteria**:
- **Haiku-appropriate**: Task follows clear patterns, has well-defined inputs/outputs, requires minimal decision-making
- **Sonnet-appropriate**: Task requires some architectural thinking, handles moderate complexity, balances multiple concerns
- **Opus-appropriate**: Rare for execution; only when sub-plan has residual ambiguity or requires creative problem-solving

Document the recommendation in each sub-plan's `## Execution Model` field with a brief rationale.

### Phase 5: Review Loop

After plan creation and reviewer assignment, run an iterative review process. The loop continues until all reviewers report no new findings.

#### Reviewer Agents

The review loop uses two types of reviewer agents:

**Global reviewers** (from `~/.claude/agents/`) — generic, project-agnostic:
- **`plan-architect-reviewer`** — Evaluates the decomposition, boundaries between sub-plans, dependency graph, and whether the pieces will fit together when assembled.
- **`plan-risk-reviewer`** — Identifies technical risks the planner missed: migration pitfalls, backward-compatibility landmines, missing rollback strategies, and sub-plans that may be harder or more complex than they appear.

**Local reviewers** (from `.claude/agents/`) — project-specific, domain-specialized:
- Each project defines its own reviewer agents tailored to the domains it works with (e.g., API, UI, database, infrastructure). These reviewers can preload project-specific skills via the `skills` frontmatter field for deep domain knowledge.
- The planner does not assume naming conventions — it discovers available agents and matches them to sub-plans by reading their descriptions.

#### Review Output Location

All review output is written to `reviews/` within the plan directory, named `<plan-file>.<reviewer-type>.md`:

```
.claude/plans/<feature-name>/reviews/
├── 00-master.architect.md      # Architecture review of master plan
├── 00-master.risk.md           # Risk review of master plan
├── 01-data-model.codebase.md   # Codebase review of sub-plan 01
├── 02-api-layer.codebase.md    # Codebase review of sub-plan 02
└── ...
```

This directory is ephemeral — already covered by the `.claude/plans/` ignore rule — but persists locally across sessions for reference.

#### Step 1: Master Plan Review

Launch `plan-architect-reviewer` and `plan-risk-reviewer` against the master plan (in parallel — they are independent). Pass the plan directory path so they can read all plan files and cross-reference against the codebase. Instruct each reviewer to write its output to `reviews/00-master.<reviewer-type>.md`.

Incorporate findings into both the master plan and affected sub-plans.

#### Step 2: Sub-Plan Review

After the master plan review is resolved, launch each sub-plan's assigned reviewer (from the `## Reviewer` field) against it. Sub-plan reviews can run in parallel — even when different sub-plans use different reviewers. Each reviewer writes its output to `reviews/<plan-file>.<reviewer-type>.md`.

**Output normalization**: If a local reviewer's output doesn't follow the standard format (Verdict, Critical Findings, Concerns, Observations), normalize it before incorporating. The planner interprets the reviewer's findings and translates them into actionable changes to the plan.

Incorporate findings into the sub-plans. If a sub-plan review surfaces an issue that affects the master plan (e.g., a missed dependency, a boundary that needs to shift), update the master plan and re-run affected master plan reviewers.

#### Step 3: Convergence

Repeat Steps 1-2 only for affected parts until no reviewer produces new findings. Do NOT restart the entire review — only re-review plans that changed.

The user may also request additional specialized reviewers (e.g., security, performance) for specific sub-plans. Add these on request, but they are not part of the default flow.

### Phase 6: User Approval

Present the fully reviewed plan (master + sub-plans) along with a summary of review findings and how they were addressed. Only mark as ready when the user explicitly approves.

### Post-Execution: Documentation Updates

After sub-plans have been executed, the `updating-documentation` skill should be run to keep project documentation in sync with the changes. This is not part of the planning workflow itself, but should be noted in the master plan as a final step:

```markdown
## Post-Execution
After all sub-plans are complete, run the `updating-documentation` skill to update affected docs.
```

This ensures that the documentation investment compounds — each feature execution improves docs for the next planning session.

## Master Plan Structure

The master plan is the orchestration document. It does NOT contain implementation details — those live in sub-plans.

```markdown
# Master Plan: <Feature Name>

## Summary
<Brief description of what this feature accomplishes>

## Requirements
<Bullet list of confirmed requirements from Phase 1>

## Scope
- **In scope**: ...
- **Out of scope**: ...

## Sub-Plans

| #  | Sub-Plan                | Depends On | Model  | Description                          |
|----|-------------------------|------------|--------|--------------------------------------|
| 01 | `01-<name>.md`          | —          | Haiku  | <What this sub-plan accomplishes>    |
| 02 | `02-<name>.md`          | 01         | Sonnet | <What this sub-plan accomplishes>    |
| 03 | `03-<name>.md`          | —          | Haiku  | <What this sub-plan accomplishes>    |
...

## Execution Order
<Describe which sub-plans can run in parallel and which must be sequential>
- **Parallel group 1**: 01, 03 (no dependencies)
- **Sequential**: 02 (after 01)
...

## Team Execution (Agent Teams)

**Use Agent Teams when**:
- ✅ Plan has 2+ sub-plans with meaningful scope
- ✅ Sub-plans are self-contained (minimal cross-dependencies)
- ✅ Sub-plans touch different files (avoid conflicts)
- ✅ Parallelization offers significant time savings

**Skip Agent Teams when**:
- ❌ Single sub-plan (just execute directly)
- ❌ Tiny sub-plans (overhead > benefit, e.g., "add one import")
- ❌ Highly coupled sub-plans (too much coordination needed)

**Setup**:
1. Enable Agent Teams: `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
2. Create the team:
   ```
   Create an agent team to execute .claude/plans/<feature-name>/00-master.md
   ```

**Team Lead Instructions**:
- Use this master plan as the roadmap
- Assign sub-plans to teammates based on the dependency graph
- Each teammate should load the Required Skills listed in their assigned sub-plan before starting
- Use the recommended models from the Sub-Plans table above
- Coordinate handoffs when dependencies complete
- Synthesize results when all sub-plans finish

**Suggested Team Structure**:
```
Create a team with <N> teammates to execute .claude/plans/<feature-name>/00-master.md:
- Teammate 1: Execute 01-<name>.md using Haiku (load skills: <skill-list>)
- Teammate 2: Execute 02-<name>.md using Sonnet (load skills: <skill-list>, requires 01 complete)
- Teammate 3: Execute 03-<name>.md using Haiku (load skills: <skill-list>, can start immediately)
...
```

**File Ownership** (prevent conflicts):
| Sub-Plan | Primary Files |
|----------|---------------|
| 01       | <files this sub-plan creates/modifies> |
| 02       | <files this sub-plan creates/modifies> |
...

**Communication Points**:
<When teammates might need to coordinate>
- After 01 completes: Notify teammate 2 that dependencies are ready
- If <event>: Broadcast to all teammates about <change>
...

## Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| ...  | ...        |

## Post-Execution
After all sub-plans are complete, run the `updating-documentation` skill to update affected project documentation.
```

## Sub-Plan Structure

Each sub-plan is a **self-contained execution unit**. An agent should be able to pick up a sub-plan and execute it without reading anything else.

```markdown
# Sub-Plan: <Task Name>

## Objective
<What this sub-plan accomplishes and why>

## Required Skills
<Skills the executing agent MUST load before starting>
- `skill-name` — reason it's needed

## Reviewer
<Local reviewer agent assigned during Phase 4, or "None" if no suitable reviewer was found>

## Execution Model
**Recommended**: Haiku | Sonnet | Opus
**Rationale**: <Why this model is appropriate for this sub-plan>

Examples:
- Haiku: "Standard CRUD implementation following existing patterns in the codebase"
- Sonnet: "Complex business logic with multiple edge cases and error handling scenarios"
- Opus: "Novel architectural approach requiring creative problem-solving" (rare)

## Prerequisites
<What must exist before this sub-plan can be executed>
- <Specific file, interface, or state expected from a prior sub-plan — include the actual signatures/shapes, not just references>
- Or: "None — this sub-plan has no dependencies"

## Context
<Essential context embedded directly — relevant interfaces, data shapes, conventions, architectural decisions the agent needs to know>

## Primary Files
<Files this sub-plan primarily creates or modifies — helps prevent conflicts in parallel execution>
- `path/to/file.ext` (create | modify)
- `path/to/other.ext` (modify)

## Implementation Steps
1. <Step with clear deliverable>
2. <Step with clear deliverable>
...

## Acceptance Criteria
- [ ] <Criterion 1>
- [ ] <Criterion 2>
...
```

## Rules (Non-Negotiable)

- **Never write a plan based on incomplete information**
- **Never invent requirements the user didn't specify**
- **Always decompose into sub-plans** — a single monolithic plan is a failure mode
- **Each sub-plan must be self-contained** — embed context, don't reference other sub-plans
- **Always list required skills in every sub-plan** — an executing agent without the right skills will produce subpar results or get stuck
- **Always run the review loop before presenting to the user** — unreviewed plans are draft plans, not finished plans
- **Save plans to `.claude/plans/<feature-name>/`** in the local repository — not to `~/.claude/`, and never with random/generated filenames
- **Ask for clarification even if it feels repetitive** — it's better than introducing garbage
