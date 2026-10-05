---
name: cm-reactor
description: "Strategic codebase re-direction when requirements change, architecture doesn't fit, or tech debt blocks progress. TRIZ-powered pivot protocol for large codebases."
---

# Reactor — Strategic Codebase Re-direction

> **When the code works but the direction is wrong, you don't debug — you REACT.**
> TRIZ-powered protocol for pivoting large codebases without losing stability.

## When to Use

**ALWAYS when:**
- Requirements changed significantly after code was built
- Architecture no longer fits the problem (wrong patterns, wrong abstractions)
- 3+ patches on the same area — symptom of structural mismatch
- Tech debt blocks new feature development
- "We need to rewrite X" — STOP. Use this skill first.
- Migrating from one framework/library/pattern to another
- Post-mortem reveals systemic issues needing strategic change

**Skip when:**
- Simple bug fix → use `cm-debugging`
- Routine refactoring (extract method, rename) → use `cm-clean-code`
- New project from scratch → use `cm-project-bootstrap`
- Small scope change (< 5 files affected) → just refactor directly

## The Iron Law

```
NO REWRITE WITHOUT REACTOR ANALYSIS FIRST
```

Rewrites fail 70% of the time. Incremental strategic migration succeeds 90% of the time.

## TRIZ Principles Applied

| # | Principle | How Applied |
|---|-----------|-------------|
| **#35** | Parameter Change | Change the fundamental parameter (language, pattern, architecture) — not the symptom |
| **#28** | Mechanics Substitution | Replace one mechanism with a more effective one (OOP → FP, REST → GraphQL, etc.) |
| **#13** | The Other Way Around | Instead of adapting new code to old architecture, adapt old architecture to new requirements |
| **#25** | Self-Service | Design the migration so each component can migrate independently |
| **#1** | Segmentation | Break monolithic change into independent migration units |
| **#10** | Prior Action | Prepare the codebase (interfaces, adapters) BEFORE the actual migration |

## The 5-Phase Process

```
Phase 1: ASSESS    → Understand what's wrong and why (not just symptoms)
Phase 2: MAP       → Trace all dependencies and blast radius
Phase 3: DESIGN    → Plan the migration path with strangler fig pattern
Phase 4: EXECUTE   → Migrate incrementally, one unit at a time
Phase 5: VERIFY    → Confirm direction is correct + clean up old code
```

### Phase 1: ASSESS — Identify the Contradiction

> **Goal:** Find the TRIZ contradiction — what do we WANT vs what BLOCKS us?

1. **State the current direction:**
   ```
   Current: We built [X architecture/pattern/structure]
   Problem: It doesn't support [Y requirement/scale/use case]
   ```

2. **Identify the contradiction:**
   ```
   We WANT: [desired capability]
   But: [current architecture] prevents it because [technical reason]
   
   TRIZ Contradiction:
   Improving [parameter A] worsens [parameter B]
   Example: "Improving modularity worsens performance"
           "Improving flexibility worsens type safety"
   ```

3. **Define the Ideal Final Result (IFR):**
   ```
   The system ITSELF [achieves the goal]
   WITHOUT [the current blocking factor]
   WHILE maintaining [what currently works well]
   ```

4. **Scope assessment:**
   ```
   Files affected: [count from codeintell or grep]
   Components affected: [list]
   Tests affected: [count]
   External API changes: [yes/no — breaking change?]
   Estimated effort: [S/M/L/XL]
   Risk level: [Low/Medium/High/Critical]
   ```

### Phase 2: MAP — Dependency Analysis

> **Goal:** Know exactly what touches what before changing anything.

1. **Use Code Intelligence** (if available):
   ```
   codegraph_impact("target_symbol", depth=3)
   → Shows all callers, dependencies, affected files
   
   codegraph_context("target_module")
   → Shows architecture around the area
   ```

2. **Manual mapping** (if codegraph unavailable):
   ```
   grep -rn "import.*{module}" src/
   grep -rn "{function_name}" src/
   → Build dependency tree manually
   ```

3. **Categorize files by migration priority:**

   | Category | Description | Action |
   |----------|-------------|--------|
   | **Core** | The files that MUST change for the new direction | Migrate first |
   | **Dependent** | Files that import/use Core files | Migrate after Core, use adapters |
   | **Peripheral** | Files loosely connected | Migrate last or leave untouched |
   | **Dead** | Files no longer needed after migration | Flag for deletion in Phase 5 |

4. **Output: Migration Map Document**
   ```markdown
   ## Migration Map: [Initiative Name]
   
   ### Core (must change): [N files]
   - file_a.ts → [what changes]
   - file_b.ts → [what changes]
   
   ### Dependent (affected): [N files]
   - file_c.ts → [how affected]
   
   ### Peripheral (optional): [N files]
   - file_d.ts → [minimal change]
   
   ### Dead (remove after): [N files]
   - old_module.ts → DELETE after migration complete
   ```

### Phase 3: DESIGN — Strangler Fig Migration

> **Goal:** Design an incremental migration path — NEVER big-bang rewrite.

**Strangler Fig Pattern (TRIZ #10 Prior Action):**
```
1. Create NEW structure alongside OLD structure
2. Route NEW traffic/calls to NEW structure
3. Gradually migrate OLD consumers to NEW structure
4. Remove OLD structure when no longer used
```

**Migration design template:**
```markdown
## Migration Path

### Step 1: Create Adapter Layer
- [ ] Create interface/abstraction that both old and new code satisfy
- [ ] All consumers now use the adapter, not direct implementation

### Step 2: Build New Implementation
- [ ] New code behind the adapter — can be tested independently
- [ ] Feature flag or config switch between old/new

### Step 3: Gradual Cut-over
- [ ] Migrate consumers one-by-one to new implementation
- [ ] Each migration is a separate commit/PR
- [ ] Tests pass at EVERY step (never break green)

### Step 4: Clean up (→ triggers cm-clean-code)
- [ ] Remove old implementation
- [ ] Remove adapter layer (if no longer needed)
- [ ] Remove feature flag
- [ ] Update documentation
```

**Rules:**
- Never break the build at any step
- Each step MUST be independently deployable
- Tests must pass at every intermediate state
- If any step fails → STOP, don't cascade

### Phase 4: EXECUTE — Incremental Migration

> **Goal:** Execute migration plan step by step with quality gates.

**Use `cm-execution` Mode A (Batch) or Mode E (TRIZ-Parallel):**

```
For each migration step:
  1. Write/update tests FIRST (cm-tdd)
  2. Implement the change
  3. Run full test suite
  4. Commit with clear message: "reactor: [step description]"
  5. If tests fail → STOP, diagnose, fix before next step
  
Progress tracking:
  → Update OpenSpec `tasks.md` and `cm-tasks.json` with each completed migration step
  → Update CONTINUITY.md with migration status
```

**Commit convention:**
```
reactor: create adapter layer for auth module
reactor: implement new auth service behind adapter
reactor: migrate login page to new auth
reactor: migrate signup page to new auth
reactor: remove old auth implementation
reactor: cleanup — remove adapter (direct usage now)
```

### Phase 5: VERIFY & CLEAN

> **Goal:** Confirm the new direction works AND trigger cm-clean-code.

1. **Direction verification:**
   ```
   □ New architecture supports the originally blocked requirement
   □ Performance is equal or better
   □ All tests pass
   □ No regression in existing features
   □ Documentation updated
   ```

2. **Trigger cm-clean-code:**
   ```
   After reactor completes → ALWAYS run cm-clean-code
   Reason: Migration leaves dead code, unused imports, stale references
   ```

3. **Record in CONTINUITY.md:**
   ```
   Decision: Migrated [X] from [old pattern] to [new pattern]
   Rationale: [why — the TRIZ contradiction we resolved]
   Scope: module:[affected module]
   ```

---

## Red Flags — STOP

| Thought | Reality |
|---------|---------|
| "Let's just rewrite everything" | Big-bang rewrites fail 70%+ of the time |
| "It's faster to start from scratch" | You lose all edge-case handling and bug fixes |
| "We don't need tests during migration" | Migration without tests = guaranteed regression |
| "Let's change the direction AND add features" | One thing at a time. Direction first, features after |
| "This adapter layer is extra work" | Adapter saves you from big-bang. It pays for itself |
| "We can just search-and-replace" | Structural changes ≠ text changes |

## Integration

| Skill | When |
|-------|------|
| `cm-brainstorm-idea` | UPSTREAM: Identifies need for direction change |
| `cm-codeintell` | Phase 2: Dependency analysis via codegraph |
| `cm-planning` | Phase 3: Formalize migration plan |
| `cm-execution` | Phase 4: Execute migration steps |
| `cm-tdd` | Phase 4: Tests before each migration step |
| `cm-clean-code` | Phase 5: MANDATORY cleanup after reactor |
| `cm-debugging` | If migration introduces bugs |
| `cm-continuity` | Record direction decisions |

### Lifecycle Position

```
cm-brainstorm-idea → cm-reactor → cm-planning → cm-execution → cm-clean-code
     (analyze)       (redirect)     (plan)        (build)        (hygiene)
```

## The Bottom Line

**Don't rewrite. React. Migrate incrementally. Clean up after. Every step must pass tests.**
