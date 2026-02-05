---
name: implement-plan
description: Execute approved technical implementation plans with verification checkpoints. This skill should be used when implementing pre-approved development plans, feature implementations, or technical specifications that have defined phases, success criteria, and verification steps. Triggers on requests like "implement the plan", "execute the implementation plan", or when given a path to a plan file.
---

# Implement Plan

Execute approved technical implementation plans using an **orchestrator model** with subagent delegation, built-in verification checkpoints, progress tracking, and human-in-the-loop validation.

## Orchestration Model

**This session serves as the orchestrator.** Do NOT implement code directly in this session. Instead:

1. **Use subagents for ALL implementation work** - Spawn Task agents for each discrete piece of work (creating files, writing tests, running verifications)
2. **Parallelize where possible** - Launch multiple subagents concurrently when tasks have no dependencies
3. **This session coordinates** - Track progress, handle blockers, make decisions, but delegate actual coding

### Why Orchestration?

- **Context preservation**: Main session retains full plan context while subagents handle discrete tasks
- **Parallelization**: Independent tasks execute concurrently, dramatically reducing implementation time
- **Clean separation**: Orchestration logic stays separate from implementation details
- **Better error handling**: Failures in one subagent don't pollute the main context

## When to Use This Skill

- Implementing pre-approved technical plans or specifications
- Executing phased development work with defined success criteria
- Following structured implementation guides with verification steps
- Resuming partially-completed implementation work

## Getting Started

When given a plan path or asked to implement a plan:

1. **Locate the Plan**: Find the plan file (typically in `docs/plans/`, `thoughts/plans/`, or specified path)
2. **Read Completely**: Read the entire plan without pagination - full context is essential
3. **Check Progress**: Look for existing checkmarks (`- [x]`) indicating completed work
4. **Read Referenced Files**: Load all files mentioned in the plan fully
5. **Understand Interconnections**: Analyze how components fit together
6. **Create Progress Tracker**: Use TodoWrite to track implementation progress
7. **Begin Orchestration**: Start delegating to subagents only when requirements are clearly understood

If no plan path is provided, ask: "Which plan should I implement? Please provide the path or name?"

## Implementation Workflow

### Phase Execution Protocol

For each phase in the plan:

```
1. READ phase requirements and success criteria
2. IDENTIFY independent tasks that can be parallelized
3. SPAWN subagents for implementation work
4. MONITOR subagent progress and handle blockers
5. VERIFY against success criteria via verification subagent
6. FIX any issues (spawn fix subagents as needed)
7. UPDATE checkboxes in plan file using Edit tool
8. PAUSE for human verification (unless executing consecutive phases)
```

### Subagent Usage Guidelines

**Always run in background**: Use `run_in_background: true` for all Task agents to enable parallel execution. Use `AgentOutputTool` to check on progress.

**File Creation**: Spawn one subagent per file or logical group of related files
```
Task (run_in_background: true): "Create the authentication service at src/auth/auth.service.ts implementing JWT token generation and validation. Include methods for login(), logout(), and validateToken()."
```

**Testing**: Spawn dedicated subagent for writing and running tests
```
Task (run_in_background: true): "Write unit tests for src/auth/auth.service.ts covering login success, login failure, token validation, and logout scenarios. Run tests and report results."
```

**Verification**: Spawn subagent to run build/lint/test commands
```
Task (run_in_background: true): "Run full verification suite: npm run lint && npm run typecheck && npm test && npm run build. Report any failures with details."
```

**Research**: If implementation questions arise, spawn Explore agent to investigate codebase
```
Task (subagent_type: Explore, run_in_background: true): "Find how error handling is implemented in existing services. Look for patterns in src/services/ for consistent error response formats."
```

**Plan Updates**: Spawn subagent to update plan file checkboxes
```
Task (run_in_background: true): "Update the plan file at docs/plans/auth.md. Mark all Phase 2 tasks as complete by changing [ ] to [x] for the items listed."
```

### Parallelization Strategy

**Within a phase**, identify independent tasks and launch them concurrently:

```
Phase 2: Authentication Service
├── [PARALLEL] Subagent A: Create auth.service.ts
├── [PARALLEL] Subagent B: Create auth.guard.ts
├── [PARALLEL] Subagent C: Create jwt.strategy.ts
└── [SEQUENTIAL - after above complete] Subagent D: Write tests for all three
```

**Rules for parallelization**:
- Files with no dependencies on each other → parallel
- Files that import from each other → sequential (create dependency first)
- Tests → after implementation files exist
- Verification → after all phase files complete

### Progress Tracking

Maintain **triple tracking** in the orchestrator session:

1. **Plan File**: Update checkboxes (`- [ ]` → `- [x]`) as sections complete (spawn subagent for this)
2. **TodoWrite**: Track phase-level progress within current session
3. **Inline Status**: Provide brief status updates as subagents complete

#### Inline Status Format

Use concise status updates that flow naturally:

```
● Phase 2 Status:
  - 🔄 Subagent abc123: Creating auth.service.ts (running)
  - 🔄 Subagent def456: Creating auth.guard.ts (running)
  - 🔄 Subagent ghi789: Creating jwt.strategy.ts (running)

● Good progress:
  - ✅ auth.service.ts created
  - ✅ auth.guard.ts created
  - 🔄 jwt.strategy.ts (still running)
```

After all tasks in a phase complete:

```
● Phase 2 Complete!

  All verifications passed:
  - ✅ Build passes
  - ✅ Lint passes
  - ✅ Tests pass (47 passing)

  Now moving to Phase 3: [Phase Name]
```

### Phase Completion Protocol

After all implementation subagents complete for a phase:

1. **Spawn verification subagent** to run build/lint/test
2. **Spawn plan update subagent** to mark checkboxes complete
3. **Report phase completion** with verification results
4. **List manual verification steps** if any in plan
5. **Await confirmation** before proceeding (unless executing consecutive phases)

```
● Phase 2 Complete!

  All verifications passed:
  - ✅ Build passes
  - ✅ Lint passes
  - ✅ Tests pass (47 passing)

  Manual verification steps:
  - [ ] POST /auth/login returns token
  - [ ] POST /auth/logout invalidates session
  - [ ] GET /auth/profile returns user (with token)

  Confirm to proceed to Phase 3.
```

**Note**: Skip pauses between consecutive phases if instructed to execute multiple phases. Pause only after the final phase.

### Handling Blockers and Decisions

When a subagent reports an issue or the orchestrator identifies a blocker:

1. **STOP** spawning new dependent subagents
2. **SURFACE** the blocker immediately to the user
3. **AWAIT** user decision before proceeding

```
● ⚠️ BLOCKER in Phase 2 - Decision Required

  Task: Creating jwt.strategy.ts

  Issue: Subagent reports existing JWT implementation in src/legacy/auth.js.
  The plan specifies creating new jwt.strategy.ts but doesn't mention legacy code.

  Options:
  A) Proceed with new implementation, mark legacy for removal
  B) Refactor legacy code instead of creating new file
  C) Create new file but import shared utilities from legacy

  Recommendation: Option A - cleaner separation

  How should I proceed?
```

## Handling Mismatches

When a subagent reports that reality diverges from the plan:

1. **STOP** - Do not spawn additional dependent subagents
2. **ANALYZE** - Review subagent findings and assess impact
3. **PRESENT** - Surface to user using blocker format (see above)

Common mismatch causes:
- Codebase evolved since plan creation
- Plan assumptions were incorrect
- Dependencies changed
- Better approaches discovered during implementation

**Orchestrator response**: Do not attempt to resolve mismatches autonomously. Surface them immediately—the orchestrator's job is to coordinate, not to make architectural decisions without user input.

## Resuming Interrupted Work

When a plan has existing checkmarks:

1. **Trust Completion**: Assume checked items are done correctly
2. **Find Resume Point**: Locate first unchecked item
3. **Verify Context**: Read surrounding completed work for context
4. **Continue Forward**: Pick up implementation from unchecked items

Only verify previous work if something seems inconsistent or broken.

## Implementation Philosophy

Plans are carefully designed guides, but judgment matters:

- **Follow Intent**: Adapt to what you find while honoring the plan's goals
- **Complete Phases**: Finish each phase fully before advancing
- **Maintain Context**: Verify changes fit the broader codebase
- **Communicate Issues**: Surface problems early rather than working around them
- **Forward Momentum**: Focus on implementing solutions, not just checking boxes

## Quality Gates

Before marking any phase complete:

| Check | Command/Action | Required |
|-------|----------------|----------|
| Tests Pass | `npm test` / `pytest` / project test command | Yes |
| Lint Clean | `npm run lint` / project lint command | Yes |
| Types Valid | `npm run typecheck` / type checking | Yes |
| Build Succeeds | `npm run build` / project build command | Yes |
| Manual Steps | As specified in plan | If listed |

## Example Orchestration Session

Here's how a typical implementation session flows:

```
USER: Implement the plan at docs/plans/auth-implementation.md

ORCHESTRATOR: [Reads plan, analyzes phases]

Phase 1: Database Schema

Now I'll spawn subagents for Phase 1 tasks in parallel:
1. Create migration file
2. Create password utilities

● 2 Task agents launched (ctrl+o to expand)
   ├─ Create users migration · Running in background
   │  ⎿  Launched
   └─ Create password utilities · Running in background
      ⎿  Launched

● Phase 1 Status:
  - 🔄 Subagent abc123: Creating migration (running)
  - 🔄 Subagent def456: Creating password utils (running)

● Agent Output abc123
  ⎿  Create users migration (24 lines)
     (ctrl+o to expand)

● Agent Output def456
  ⎿  Create password utilities (18 lines)
     (ctrl+o to expand)

● Good progress:
  - ✅ Migration file created
  - ✅ Password utilities created

  Now running verification:

● 2 Task agents launched (ctrl+o to expand)
   ├─ Phase 1 build/lint verify · Running in background
   │  ⎿  Launched
   └─ Update plan Phase 1 tasks · Running in background
      ⎿  Launched

● Agent Output verify123
  ⎿  Phase 1 build/lint verify (15 lines)
     (ctrl+o to expand)

● Phase 1 Complete!

  All verifications passed:
  - ✅ Build passes
  - ✅ Lint passes
  - ✅ Tests pass (12 passing)

  Manual verification steps:
  - [ ] Verify users table exists in database

  Confirm to proceed to Phase 2.
```

## Reference Materials

See `references/plan-format.md` for:
- Standard plan structure and formatting
- Phase organization guidelines
- Success criteria patterns
- Verification step templates

## Key Principles Summary

1. **Never implement directly** - Always delegate to subagents
2. **Parallelize aggressively** - Independent tasks run concurrently
3. **Track everything** - Plan file updates, TodoWrite, and status updates
4. **Surface blockers immediately** - Don't make decisions autonomously
5. **Verify before advancing** - Each phase gets full verification
6. **Preserve context** - Orchestrator maintains the big picture
