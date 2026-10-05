---
name: migrate
description: Migration orchestrator that safely plans, executes, and verifies codebase or infrastructure migrations with rollback capabilities.
layer: orchestrator
category: orchestration
triggers:
  - "/migrate"
  - "migrate this"
  - "migration plan"
  - "upgrade to"
  - "move from X to Y"
  - "convert from X to Y"
inputs:
  - Source state description (current technology, version, or architecture)
  - Target state description (desired technology, version, or architecture)
  - Optional scope constraints (specific modules, files, or services)
  - Optional risk tolerance (conservative, moderate, aggressive)
outputs:
  - Detailed migration plan with phases
  - Backup or snapshot of affected code
  - Migrated code with all changes applied
  - Verification report (tests pass, no regressions)
  - Rollback plan with instructions
  - Migration summary with before/after comparison
linksTo:
  - plan
  - plan-validate
  - plan-archive
  - scout
  - research
  - test
  - fix
  - debug
  - refactor
  - code-review
  - optimize
  - sequential-thinking
  - git-workflow
  - commit-crafter
  - docs-writer
  - mermaid
linkedFrom:
  - team
preferredNextSkills:
  - test
  - ship
  - audit
fallbackSkills:
  - plan
  - refactor
riskLevel: high
memoryReadPolicy: full
memoryWritePolicy: always
sideEffects:
  - Creates backup branches or snapshots
  - Modifies source files (potentially many)
  - Modifies configuration files
  - May modify dependency files
  - Creates git commits at each phase
  - May modify database schemas
  - May modify infrastructure configuration
---

# Migrate

## Purpose

Migrate is the orchestrator for all types of migrations: framework upgrades, language version bumps, architecture shifts, database schema changes, dependency replacements, and technology swaps. It treats every migration as a high-risk operation and applies a disciplined process: plan thoroughly, back up everything, execute incrementally, verify at each step, and always have a rollback plan.

Migrations are inherently dangerous because they touch many files, change fundamental assumptions, and can introduce subtle regressions that only surface later. Migrate exists to make this process as safe and systematic as possible.

## Workflow

### Phase 1: Assess & Plan
1. **Parse the migration scope** -- Understand what's being migrated from and to. Identify all affected areas.
2. **Invoke `scout`** -- Scan the codebase to build a complete inventory of what needs to change:
   - Files using the old pattern/technology
   - Configuration files that reference it
   - Tests that depend on it
   - Documentation that mentions it
   - Dependencies that relate to it
3. **Invoke `research`** -- Look up the migration path:
   - Official migration guides (via Context7)
   - Known breaking changes between versions
   - Community-reported pitfalls
   - Codemods or automated migration tools available
4. **Invoke `sequential-thinking`** -- Reason through the migration order:
   - What must change first (foundations) vs last (consumers)
   - Which changes are independent vs dependent
   - Where the risk concentrations are
5. **Invoke `plan`** -- Create a phased migration plan:
   - Phase boundaries with clear milestones
   - Per-phase file lists and change descriptions
   - Risk assessment per phase
   - Estimated effort per phase
   - Rollback strategy per phase
6. **Invoke `plan-validate`** -- Verify the plan is complete and feasible.
7. **Invoke `mermaid`** (if complex) -- Visualize the migration dependency graph.
8. **Present the plan** -- Show the user the full migration plan. This is a mandatory checkpoint -- no migration proceeds without explicit user approval.

### Phase 2: Backup
9. **Invoke `git-workflow`** -- Create a migration branch from the current state.
10. **Create a pre-migration snapshot** -- Tag the current state so rollback is always one command away.
11. **Document the current state** -- Record:
    - Current versions of all affected dependencies
    - Current test results (baseline)
    - Current build output (baseline)

### Phase 3: Execute (Per Phase)
For each phase in the migration plan:

12. **Execute the changes** -- Apply the transformations for this phase:
    - Use codemods if available
    - Manual code changes following the plan
    - Configuration updates
    - Dependency changes
13. **Invoke `test`** -- Run relevant tests after each phase:
    - Tests for directly changed code
    - Tests for code that depends on changed code
    - Full suite at major phase boundaries
14. **Handle failures** -- If tests fail:
    - **Simple fixes**: Invoke `fix` to resolve
    - **Complex issues**: Invoke `debug` to investigate root cause
    - **Blocking issues**: Halt and report. Do not proceed to the next phase.
15. **Invoke `commit-crafter`** -- Commit the phase with a descriptive message like `migrate(phase-2): convert REST routes to GraphQL resolvers`.
16. **Phase checkpoint** -- Report phase completion, test results, and any concerns before proceeding.

### Phase 4: Verify
17. **Run full test suite** -- After all phases complete, run every test.
18. **Invoke `code-review`** -- Review the entire migration diff:
    - Check for incomplete migrations (old patterns still present)
    - Check for regressions
    - Check for unnecessary changes (scope creep)
    - Check for security implications
19. **Invoke `optimize`** (if applicable) -- If the migration was a framework upgrade, check that performance hasn't regressed.
20. **Invoke `scout`** -- Re-scan for any remaining references to the old pattern. Flag anything left behind.

### Phase 5: Rollback Plan
21. **Document the rollback procedure** -- Create explicit rollback instructions:
    - Git commands to revert to the pre-migration tag
    - Dependency rollback commands
    - Database rollback steps (if applicable)
    - Configuration rollback steps
22. **Test the rollback** (if high-risk) -- For critical migrations, actually test that the rollback works on a branch.

### Phase 6: Complete
23. **Invoke `docs-writer`** -- Update documentation to reflect the new state.
24. **Invoke `plan-archive`** -- Archive the migration plan for future reference.
25. **Present migration summary** -- Report:
    - Total files changed
    - Tests before vs after
    - Any remaining TODO items
    - Rollback instructions
    - Recommended next steps (usually `ship`)

## Migration Types

### Framework Upgrade
```
Example: Next.js 14 -> Next.js 15
Phases:
  1. Update dependencies + config
  2. Migrate deprecated APIs
  3. Update routing patterns
  4. Update data fetching patterns
  5. Full test + review
```

### Language Version Bump
```
Example: Node.js 18 -> Node.js 22
Phases:
  1. Update engine constraints
  2. Replace deprecated APIs
  3. Adopt new language features (optional)
  4. Update CI/CD node version
  5. Full test + review
```

### Technology Swap
```
Example: Styled-components -> Tailwind CSS
Phases:
  1. Install Tailwind, configure
  2. Convert shared/base components
  3. Convert feature components
  4. Convert page-level components
  5. Remove styled-components
  6. Full test + visual review
```

### Database Migration
```
Example: MySQL -> PostgreSQL
Phases:
  1. Set up PostgreSQL, schema migration
  2. Update ORM config + queries
  3. Data migration scripts
  4. Update connection handling
  5. Parallel run + data verification
  6. Cutover
```

### Architecture Shift
```
Example: Monolith -> Microservices
Phases:
  1. Identify service boundaries
  2. Extract shared libraries
  3. Extract first service
  4. Set up inter-service communication
  5. Extract remaining services
  6. Remove monolith routing
```

## Decision Points

| Condition | Action |
|-----------|--------|
| Official migration guide exists | Follow it, supplement with codemod |
| Codemod available | Use it for bulk changes, review output |
| Migration affects database | Require explicit backup + rollback test |
| Test suite is insufficient | Write migration-specific tests before migrating |
| Phase fails after 3 fix attempts | Halt, report, ask user for direction |
| Migration is < 10 files | Simplify to single-phase execution |
| Migration is > 100 files | Mandatory multi-phase with checkpoints |

## Usage

Use Migrate for any change that transforms the project from one state to another at a foundational level. This is distinct from `refactor` (which restructures without changing technology) and `cook` (which adds features).

**Best for:**
- Framework or library version upgrades
- Technology swaps (one library for another)
- Architecture transformations
- Database migrations
- Language version upgrades
- Build tool migrations

**Not ideal for:**
- Adding new features (use `cook`)
- Code restructuring without technology change (use `refactor`)
- Deploying existing code (use `ship`)
- Quick dependency updates with no breaking changes (just update and test)

## Examples

### Example 1: Framework upgrade
```
User: /migrate Upgrade from React 18 to React 19

Migrate workflow:
1. scout -> Find all React imports, hook usage, deprecated patterns
2. research -> React 19 migration guide, breaking changes list
3. plan -> 4 phases: deps, compiler setup, API updates, new features
4. Backup -> Tag pre-migration, create branch
5. Phase 1 -> Update react, react-dom, types
6. Phase 2 -> Set up React compiler, remove useMemo/useCallback where safe
7. Phase 3 -> Update deprecated APIs (forwardRef removal, etc.)
8. Phase 4 -> Adopt new patterns (use(), Actions)
9. Verify -> Full test suite, code-review, scout for remnants
10. Rollback plan -> Document revert steps
```

### Example 2: ORM migration
```
User: /migrate Move from Prisma to Drizzle ORM

Migrate workflow:
1. scout -> Inventory all Prisma models, queries, migrations
2. research -> Drizzle schema syntax, query API differences
3. plan -> 5 phases: schema, queries, migrations, middleware, cleanup
4. Backup -> Tag pre-migration
5. Phase 1 -> Convert Prisma schema to Drizzle schema
6. Phase 2 -> Rewrite queries (findMany -> select, etc.)
7. Phase 3 -> Set up Drizzle migration system
8. Phase 4 -> Update middleware and utilities
9. Phase 5 -> Remove Prisma, clean up
10. Verify -> Full test suite, data integrity checks
```

## Guardrails

- **Never migrate without a plan.** Every migration must be planned and approved by the user.
- **Never migrate without backups.** A pre-migration git tag is mandatory.
- **Always verify per-phase.** Run tests after every phase, not just at the end.
- **Always have a rollback plan.** Document exactly how to undo the migration.
- **Never mix migration with feature work.** A migration branch changes technology, not behavior.
- **Scout before AND after.** Check for remnants of the old pattern after migration completes.
- **Commit per phase.** Each phase gets its own commit for granular rollback capability.
- **Halt on unexpected failures.** If something breaks that the plan didn't anticipate, stop and reassess.
