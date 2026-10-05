---
name: plan-execute
description: Multi-phase plan-then-execute workflow for non-trivial features and refactorings.
  Enforces strict intent gating between read-only planning mode (GitNexus impact analysis,
  multi-axis solution mapping) and execution mode.
argument-hint: <feature or refactoring goal>
---

<!-- Generated from workflows/plan-execute.md by tools/generate_integrations.py. Edit the source file, not this one. This is an execution WORKFLOW packaged as an Agent Skill so it is discoverable and directly invocable ("/plan-execute") in every compatible tool. -->

# Workflow: Plan-then-Execute

## When to Use
| Criteria | Match |
|----------|-------|
| Intention | complex_feature, refactor, moderate_change |
| Complexity | multi-file, moderate risk, needs up-front analysis |
| Power Mode | Balanced or Deep |
| Clarity | requirements are clear but implementation is non-trivial |

## Required Skills
- codebase-understanding (GitNexus) — for pre-analysis
- file-operations
- code-execution
- code-quality-testing
- communication-tone
- project-scaffolding (if new files needed)
- safety-profiles (default or strict)

## Flow

### Phase 0: Thinking Stage (Pre-Action)
- [ ] Is the user's intent clear? Re-evaluate on EVERY new message *(Factory)*
- [ ] Have I read the relevant code areas? NEVER change what I haven't read
- [ ] Do I understand the existing patterns and conventions?
- [ ] What's the blast radius of my planned changes? (GitNexus impact analysis)
- [ ] Verify: am I in PLAN mode or EXECUTE mode? Never mix the two

### Phase 1: Intent Gate (Factory pattern)
Determine: **Am I in plan mode or execute mode?**

- **Plan mode**: research, gather context, propose approach — NO file changes
- **Execute mode**: implement following the approved plan — NO scope changes

State your mode at the start: "I'm in PLAN mode. Let me research before making changes."

### Phase 2: Research & Context (Plan Mode)

```
1. READ gitnexus://repo/{name}/context → Codebase overview
2. query({search_query: "<relevant concept>"}) → Find related code
3. impact({target: "<planned change area>", direction: "upstream"})
   → Understand blast radius before designing solution
4. Read key source files for implementation details
5. Check existing patterns and conventions in the codebase
```

### Phase 3: Propose Plan (Plan Mode)
- **Multi-Axis Solution Mapping**: Map at least 2 distinct implementation approaches (evaluating trade-off axes: complexity vs performance vs maintainability vs blast radius) before selecting the optimal path.
Present to user:
- **What** needs to change (files, interfaces, data flow)
- **How** it will change (selected optimal approach & trade-off rationale)
- **Risk** assessment (based on GitNexus impact analysis)
- **Order** of changes (dependencies between changes)
- **What won't change** (scope boundaries)

### Phase 4: Execute (Execute Mode)
- After user approves the plan
- Follow the planned order precisely
- Implement one logical unit at a time
- After each unit: verify it works before moving on

### Phase 5: Real Test Verification & Shipping Sync
- Run tests for affected execution flows
- **Real Test Contract**: Wait on real completion signals, not fixed sleeps. Test against non-cached truth endpoints or vary cache keys. Isolate tests from persisted service state.
- **Shipping Verification**: Run full test verification suite (`pnpm test` / `npm run verify`) prior to committing.
- **Documentation Synchronization**: If code changes alter API contracts, configuration, or developer workflows, update corresponding documentation files in the same change set.
- `detect_changes()` to confirm scope matches plan
- Linter on new/changed files

### Phase 5b: Sanity Check
- [ ] Does the implementation match the approved plan? Any deviations?
- [ ] Have all planned files been created/modified? No orphaned code? *(Kiro)*
- [ ] `detect_changes()` — is scope limited to what was planned?
- [ ] Does the existing functionality still work? (regression check)
- [ ] Are there linter errors or test failures?

### Phase 6: Report
- What was implemented (matching the plan)
- Any deviations from the plan (and why)
- Verification results

## Token Budget
- **Typical**: 15K-60K tokens
- **Max recommended**: 100K tokens
- **Warning threshold**: >100K → switch to Spec-Driven or session summarization

## GitNexus Integration — Heavy in Plan Phase
- `query` — understanding related code
- `impact` — pre-implementation blast radius
- `context` — interface understanding
- `detect_changes` — post-implementation verification

## Hallucination Watchpoints
- Switching to execute mode without user approval
- Adding scope/features not in the approved plan
- Skipping research phase for "obvious" changes
- Not checking blast radius before implementation
- Inconsistent: plan says one thing, code does another

## Example
```
User: "Add rate limiting to the API"

PLAN MODE:
1. query({search_query: "api middleware request handling"})
   → Found: apiMiddleware, requestHandler, authMiddleware
2. impact({target: "apiMiddleware", direction: "upstream"})
   → d=1: router definitions, request handler
3. Plan:
   - New file: src/middleware/rateLimiter.ts
   - Integration: add to apiMiddleware chain
   - Uses express-rate-limit package
   - Risk: LOW (middleware pattern already exists)

USER: "Looks good, proceed"

EXECUTE MODE:
1. pnpm install express-rate-limit
2. Create src/middleware/rateLimiter.ts
3. Wire into apiMiddleware
4. verify → linter clean, tests pass
```
