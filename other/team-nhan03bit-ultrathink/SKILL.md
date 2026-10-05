---
name: team
description: Multi-agent team coordinator that breaks complex tasks into parallel or sequential workstreams, delegates to specialized skills, and merges results.
layer: orchestrator
category: orchestration
triggers:
  - "/team"
  - "coordinate a team"
  - "parallelize this work"
  - "split this into workstreams"
  - "multi-agent build"
inputs:
  - Complex task description requiring multiple concurrent or sequential workstreams
  - Optional team composition preferences
  - Optional priority ordering
  - Optional dependency graph between subtasks
outputs:
  - Coordinated results from all workstreams
  - Dependency resolution report
  - Merged final output with conflict resolution
  - Team execution summary with per-workstream status
linksTo:
  - cook
  - plan
  - scout
  - research
  - brainstorm
  - code-review
  - test
  - fix
  - refactor
  - optimize
  - debug
  - kanban
  - sequential-thinking
  - mermaid
  - docs-writer
linkedFrom:
  - kanban
preferredNextSkills:
  - ship
  - code-review
  - pr-writer
fallbackSkills:
  - cook
  - plan
riskLevel: high
memoryReadPolicy: full
memoryWritePolicy: always
sideEffects:
  - Creates or modifies multiple source files across workstreams
  - Creates git commits per workstream or as a batch
  - May create temporary coordination artifacts
  - Modifies project state across multiple modules
---

# Team

## Purpose

Team is the multi-agent coordinator for tasks too large or complex for a single skill to handle alone. It decomposes a big objective into workstreams, identifies dependencies between them, assigns each workstream to the appropriate skill (often `cook` for feature work, but also `research`, `refactor`, `audit`, etc.), manages execution order, and merges results.

Team thinks in terms of a dependency graph: which tasks can run in parallel, which must be sequential, and where integration points exist. It acts as the project manager that keeps all workstreams aligned and resolves conflicts when their outputs overlap.

## Workflow

### Phase 1: Decompose
1. **Parse the objective** -- Understand the full scope of the complex task.
2. **Invoke `plan`** -- Create a high-level project plan that identifies discrete workstreams.
3. **Invoke `sequential-thinking`** -- For tasks with non-obvious dependencies, reason through the execution order.
4. **Build the dependency graph** -- Map out which workstreams depend on which, using `mermaid` to visualize if the graph is complex.

### Phase 2: Assign
5. **Map workstreams to skills** -- Each workstream gets a primary skill:
   - Feature work -> `cook`
   - Research tasks -> `research`
   - Refactoring -> `refactor`
   - Performance work -> `optimize`
   - Exploration -> `brainstorm`
   - Testing -> `test`
6. **Set execution order** -- Determine which workstreams can run in parallel and which must wait for dependencies.
7. **Present the team plan** -- Show the user the workstream breakdown, assignments, and execution order. Get confirmation for high-risk decompositions.

### Phase 3: Execute
8. **Run independent workstreams** -- Start all workstreams with no unmet dependencies.
9. **Monitor progress** -- Track completion status of each workstream.
10. **Resolve blockers** -- If a workstream fails or gets stuck:
    - Invoke `debug` or `fix` for code issues
    - Invoke `brainstorm` for design ambiguity
    - Escalate to user for requirement clarification
11. **Trigger dependent workstreams** -- As dependencies are satisfied, start waiting workstreams.

### Phase 4: Integrate
12. **Merge results** -- Combine outputs from all workstreams. Detect and resolve conflicts (e.g., two workstreams modified the same file).
13. **Invoke `code-review`** -- Review the integrated result as a whole, focusing on cross-workstream interfaces.
14. **Invoke `test`** -- Run integration tests across workstreams to verify the combined output works.
15. **Fix integration issues** -- Address any problems found during integration review or testing.

### Phase 5: Report
16. **Generate summary** -- Produce a team execution report:
    - What each workstream accomplished
    - Any issues encountered and how they were resolved
    - Integration test results
    - Recommended next steps
17. **Suggest follow-ups** -- Recommend `ship`, `pr-writer`, or additional `cook` runs for remaining work.

## Workstream Templates

### Feature Team (3+ features in parallel)
```
Objective: "Build user dashboard with analytics, settings, and notifications"

Workstream A (cook): Analytics dashboard component + API
Workstream B (cook): Settings page with preferences
Workstream C (cook): Notification center + WebSocket integration
Workstream D (research): Evaluate charting libraries [no deps]
Integration: Merge all into dashboard layout, test navigation
```

### Refactor Team (large-scale restructuring)
```
Objective: "Migrate from REST to GraphQL"

Workstream A (research): GraphQL schema design from existing REST
Workstream B (scout): Inventory all REST endpoints and consumers
Workstream C (cook): Build GraphQL server + resolvers [depends on A, B]
Workstream D (refactor): Update frontend to use GraphQL client [depends on C]
Workstream E (test): End-to-end tests for new API [depends on C]
Integration: Verify all endpoints migrated, no REST calls remain
```

### Investigation Team (multi-angle research)
```
Objective: "Evaluate and select a state management solution"

Workstream A (research): Redux Toolkit evaluation
Workstream B (research): Zustand evaluation
Workstream C (research): Jotai evaluation
Workstream D (brainstorm): Compare results from A, B, C [depends on A, B, C]
Integration: Produce recommendation document
```

## Decision Points

| Condition | Action |
|-----------|--------|
| Task has < 2 workstreams | Use `cook` directly instead of `team` |
| Dependency graph is circular | Invoke `sequential-thinking` to break the cycle |
| Workstream fails after 2 retries | Escalate to user with context |
| Two workstreams conflict on same file | Invoke `code-review` on both, then merge manually |
| User wants visibility into progress | Use `kanban` to track workstream status |
| Integration tests fail | Invoke `debug` on the failure, then `fix` |

## Usage

Use Team when the task is too large, too parallelizable, or too cross-cutting for a single Cook run. Team is the coordinator, not the implementer -- it delegates all actual work to other skills.

**Best for:**
- Multi-feature sprints
- Large-scale refactoring across many modules
- Parallel research or evaluation tasks
- Cross-cutting changes (e.g., "add authentication to all routes")
- Any task where saying "do this all sequentially" would be wasteful

**Not ideal for:**
- Single features (use `cook`)
- Simple tasks with no parallelism (use `cook` or the appropriate hub skill directly)
- Release management (use `ship`)

## Examples

### Example 1: Multi-feature build
```
User: /team Build a complete user profile system: profile page, avatar upload,
       activity history, and privacy settings

Team plan:
  Workstream A (cook): Profile page with user info display/edit
  Workstream B (cook): Avatar upload with image processing
  Workstream C (cook): Activity history feed component + API
  Workstream D (cook): Privacy settings page + API
  Dependencies: A completes first (establishes profile data model),
                then B, C, D can run in parallel
  Integration: Wire all into profile layout, shared navigation, e2e tests
```

### Example 2: Tech stack migration
```
User: /team Migrate our CSS from styled-components to Tailwind CSS

Team plan:
  Workstream A (research): Tailwind config matching current design tokens
  Workstream B (scout): Inventory all styled-components usage
  Workstream C (cook): Set up Tailwind, convert shared components [depends on A, B]
  Workstream D (cook): Convert page-level components [depends on C]
  Workstream E (test): Visual regression tests [depends on C]
  Workstream F (refactor): Remove styled-components dependency [depends on D, E]
  Integration: Full visual regression pass, bundle size comparison
```

### Example 3: Investigation and decision
```
User: /team Evaluate whether we should use PostgreSQL or MongoDB for our
       new analytics service

Team plan:
  Workstream A (research): PostgreSQL for time-series analytics
  Workstream B (research): MongoDB for analytics document storage
  Workstream C (scout): Current data access patterns in the codebase
  Workstream D (brainstorm): Synthesize findings [depends on A, B, C]
  Integration: Decision document with recommendation and trade-offs
```

## Guardrails

- **Never skip decomposition.** Even if it seems obvious, formally break the task into workstreams.
- **Respect dependencies.** Never start a workstream before its dependencies are met.
- **Always integrate.** Parallel workstreams must be merged and tested together.
- **Escalate conflicts.** If two workstreams produce incompatible outputs, surface this to the user.
- **Cap parallelism.** Do not run more than 8 workstreams simultaneously. Use `isolation: "worktree"` for workstreams that may touch overlapping files.
- **Track everything.** Every workstream gets a status (pending, active, done, failed) and a summary.
