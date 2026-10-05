---
name: cm-clean-code
description: "Code hygiene gate — detect and eliminate dead code, duplicates, naming mess, and code smells. TRIZ-powered. Run after features, before PRs, during debt sprints."
token_budget: 1200
compressed: true
deprecated: false
---

# Clean Code — Code Hygiene Gate

## TL;DR
- **Use after** a feature lands, before PR review
- **Detects**: dead code, duplicates, naming smells, dependency drift
- **Powered by** TRIZ contradictions and Boy Scout rule
- **Next**: cm-code-review

> **Code that works is not enough. Code must be CLEAN.**
> Inspired by Clean Code (Robert C. Martin) + Refactoring (Martin Fowler) + TRIZ.

## When to Use

**ALWAYS when:**
- After completing a feature (mandatory hygiene pass before PR)
- After `cm-reactor` migration (cleanup dead code from migration)
- Before code review (`cm-code-review`) — clean FIRST, review AFTER
- During technical debt sprints
- When code smells are detected (see Detection section)
- After AI-generated code sessions (AI tends to leave mess)
- When file grows beyond 300 lines

**Run automatically after:**
- `cm-execution` completes a task batch
- `cm-reactor` Phase 5 (post-migration cleanup)
- `cm-tdd` Refactor phase (Red → Green → **Refactor**)

**Skip when:**
- Quick hotfix (patch first, clean later — but schedule the cleanup!)
- Prototype/spike code (will be thrown away)

## TRIZ Principles Applied

| # | Principle | How Applied |
|---|-----------|-------------|
| **#1** | Segmentation | Break large files/functions into focused units |
| **#10** | Prior Action | Clean BEFORE it rots — don't wait for tech debt sprint |
| **#6** | Universality | One function should serve one purpose (SRP) |
| **#27** | Cheap Short-living | Quick small cleanups > expensive large refactors |
| **#2** | Taking Out | Extract what doesn't belong — separate concerns |

## The 7-Point Hygiene Checklist

Run this checklist on every file touched. Each point has auto-detect criteria:

```
┌───┬──────────────────────┬──────────────────────────────┬────────────────────────┐
│ # │ Check                │ Auto-Detect                  │ Action                 │
├───┼──────────────────────┼──────────────────────────────┼────────────────────────┤
│ 1 │ Dead Code            │ Unused exports, unreachable  │ DELETE — don't comment │
│   │                      │ branches, commented-out code │ out, DELETE            │
├───┼──────────────────────┼──────────────────────────────┼────────────────────────┤
│ 2 │ Unused Imports       │ Import not used in file      │ REMOVE import line     │
├───┼──────────────────────┼──────────────────────────────┼────────────────────────┤
│ 3 │ Magic Numbers        │ Literal numbers in logic     │ EXTRACT to named const │
│   │ & Strings            │ Repeated string literals     │                        │
├───┼──────────────────────┼──────────────────────────────┼────────────────────────┤
│ 4 │ Naming               │ Single-letter vars (not i,j) │ RENAME to describe     │
│   │                      │ Abbreviations, inconsistent  │ intent clearly         │
├───┼──────────────────────┼──────────────────────────────┼────────────────────────┤
│ 5 │ Single Responsibility│ Function does 2+ things      │ EXTRACT into separate  │
│   │ (SRP)                │ Class has 5+ public methods  │ focused units          │
├───┼──────────────────────┼──────────────────────────────┼────────────────────────┤
│ 6 │ DRY (Don't Repeat)   │ Similar code blocks in 2+    │ EXTRACT shared logic   │
│   │                      │ places                       │ into reusable function │
├───┼──────────────────────┼──────────────────────────────┼────────────────────────┤
│ 7 │ Nesting Depth        │ if/for/while nested > 3      │ EXTRACT, early return, │
│   │                      │ levels deep                  │ guard clauses          │
└───┴──────────────────────┴──────────────────────────────┴────────────────────────┘
```

## The Process

### Phase 1: SCAN — Detect Code Smells

> **Goal:** Find what's dirty before cleaning.

**Automated scan (file-by-file):**

```
For each file modified in current task:

  1. SIZE CHECK:
     IF lines > 300 → FLAG "Large file — consider splitting"
     IF any function > 50 lines → FLAG "Long function — extract methods"
  
  2. IMPORT CHECK:
     Scan imports → cross-reference with usage in file body
     Unused import → FLAG for removal
  
  3. DEAD CODE CHECK:
     Commented-out code blocks → FLAG for deletion
     Functions not called anywhere → FLAG (verify with codeintell)
     Unreachable code after return/throw → FLAG
  
  4. DUPLICATION CHECK:
     Similar code blocks (>5 lines identical/near-identical) → FLAG
     Copy-paste patterns → FLAG
  
  5. NAMING CHECK:
     Single-char variables (except loop vars i,j,k) → FLAG
     Inconsistent casing (camelCase vs snake_case in same file) → FLAG
     Generic names (data, result, temp, item, value, obj) → FLAG
  
  6. COMPLEXITY CHECK:
     Nesting > 3 levels → FLAG
     Function with > 4 parameters → FLAG
     Cyclomatic complexity > 10 → FLAG
```

**Output: Smell Report**

```markdown
## Clean Code Scan: [filename]

| # | Smell | Line | Severity | Auto-fix? |
|---|-------|------|----------|-----------|
| 1 | Unused import: lodash | 3 | Low | ✅ Yes |
| 2 | Magic number: 86400 | 47 | Medium | ✅ Yes |
| 3 | Long function: processData (78 lines) | 23-101 | High | 🔧 Manual |
| 4 | Dead code: commented block | 112-125 | Low | ✅ Yes |

**Total smells: 4 | Auto-fixable: 3 | Manual: 1**
```

### Phase 2: CLEAN — Apply Fixes

> **Goal:** Fix each smell, one at a time, with tests passing between each fix.

**Rules (from refactoring.guru + Martin Fowler):**
1. **Tests first:** Ensure tests exist and pass BEFORE cleaning
2. **One change at a time:** Fix one smell → run tests → commit → next smell
3. **Behavior preservation:** Clean code MUST NOT change functionality
4. **No feature additions:** Cleaning and feature work are SEPARATE commits

**Fix patterns:**

#### Fix 1: Dead Code & Unused Imports
```
Action: DELETE (not comment out)
Rationale: Version control is your backup, not comments
Commit: "clean: remove dead code in [file]"
```

#### Fix 2: Magic Numbers → Named Constants
```
Before: if (retryCount > 3) { ... }
         setTimeout(fn, 86400000)

After:   const MAX_RETRIES = 3;
         const ONE_DAY_MS = 86_400_000;
         if (retryCount > MAX_RETRIES) { ... }
         setTimeout(fn, ONE_DAY_MS)

Commit: "clean: extract magic numbers in [file]"
```

#### Fix 3: Extract Method (TRIZ #2 Taking Out)
```
Before: 50+ line function doing validation + calculation + persistence

After:  function processOrder(order) {
          validateOrder(order);
          const total = calculateTotal(order);
          return persistOrder(order, total);
        }

Commit: "clean: extract methods from [function] in [file]"
```

#### Fix 4: Reduce Nesting (Guard Clauses)
```
Before: function foo(x) {
          if (x) {
            if (x.valid) {
              if (x.items.length > 0) {
                // actual logic buried 3 levels deep
              }
            }
          }
        }

After:  function foo(x) {
          if (!x) return;
          if (!x.valid) return;
          if (x.items.length === 0) return;
          // actual logic at top level
        }

Commit: "clean: reduce nesting with guard clauses in [file]"
```

#### Fix 5: DRY — Extract Shared Logic
```
Before: // In file_a.ts
        const formatted = `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}`
        
        // In file_b.ts (same pattern)
        const formatted = `${d.getFullYear()}-${d.getMonth()+1}-${d.getDate()}`

After:  // In utils/date.ts
        export function formatDate(date: Date): string { ... }
        
        // Both files import formatDate()

Commit: "clean: extract shared date formatting to utils"
```

#### Fix 6: Improve Naming
```
Before: const d = getData();
        const r = process(d);
        const x = r.filter(i => i.v > 0);

After:  const orders = fetchPendingOrders();
        const processedOrders = applyDiscounts(orders);
        const validOrders = processedOrders.filter(order => order.total > 0);

Commit: "clean: improve naming in [file]"
```

### Phase 3: VERIFY — Confirm Cleanliness

> **Goal:** Ensure cleanup didn't break anything and meets standards.

```
Verification Checklist:
  □ All tests pass (exact same test results as before)
  □ No functionality changed (behavior preservation)
  □ 7-Point Checklist passes on all modified files
  □ No new code smells introduced
  □ Commit history is clean (one commit per fix type)
```

**Re-run Phase 1 scan on cleaned files:**
- If smells remain → iterate Phase 2-3
- If clean → mark task as done

---

## SOLID Quick Reference

Apply SOLID during Phase 2 when restructuring:

| Principle | Meaning | Quick Test |
|-----------|---------|------------|
| **S** — Single Responsibility | One class/function = one reason to change | "Can you describe what it does in one sentence without 'and'?" |
| **O** — Open/Closed | Open for extension, closed for modification | "Can you add behavior without changing existing code?" |
| **L** — Liskov Substitution | Subtypes must be substitutable | "Can you swap implementations without breaking callers?" |
| **I** — Interface Segregation | No client forced to depend on unused methods | "Does every consumer use all methods of this interface?" |
| **D** — Dependency Inversion | Depend on abstractions, not concretions | "Do high-level modules import from low-level modules?" |

---

## Red Flags — STOP

| Thought | Reality |
|---------|---------|
| "It works, don't touch it" | Working ≠ maintainable. Clean it now or pay 10x later |
| "I'll clean it up later" | Later never comes. Clean after each feature |
| "Cleaning wastes time" | 10 min cleaning saves 2 hours debugging later |
| "It's just one small hack" | Hacks compound. Today's hack is tomorrow's tech debt |
| "AI generated it, must be clean" | AI creates functional code, rarely clean code |
| "Let me refactor AND add features" | Separate commits. Never mix. |
| "Comments explain the complex code" | If code needs comments, simplify the CODE |

## Commit Convention

```
clean: remove dead code in [file/module]
clean: extract magic numbers in [file]
clean: improve naming in [file]
clean: reduce nesting in [function]
clean: extract [method] from [function]
clean: remove unused imports in [file]
clean: apply DRY — extract shared [logic] to [util]
```

## Integration

| Skill | Relationship |
|-------|-------------|
| `cm-tdd` | Tests MUST pass before and after cleaning (Red → Green → **Refactor**) |
| `cm-reactor` | Reactor triggers cm-clean-code in Phase 5 (post-migration cleanup) |
| `cm-execution` | After task batch → run hygiene pass |
| `cm-code-review` | Clean FIRST → review AFTER (reviewers see clean code) |
| `cm-quality-gate` | Cleanliness as a quality dimension |
| `cm-debugging` | After bug fix → clean the surrounding code |
| `cm-continuity` | Record cleanup decisions and patterns learned |
| `cm-codeintell` | Verify dead code with call graph before deleting |

### Lifecycle Position

```
cm-execution → cm-clean-code → cm-code-review → cm-quality-gate → cm-safe-deploy
   (build)      (hygiene)        (review)          (verify)         (ship)
```

## Karpathy Discipline — Simplicity First

Combat over-engineering at the source, not after the fact:
- **No features beyond what was asked.** No "while I'm here" additions.
- **No abstractions for single-use code.** Three similar lines beats a premature interface.
- **No flexibility/configurability that wasn't requested.** YAGNI is the default.
- **No error handling for impossible scenarios.** Trust internal callers; validate at boundaries.
- **200 lines that should be 50 → rewrite, don't ship.**

**Senior-engineer test:** "Would a senior call this overcomplicated?" If yes, simplify before commit.

## The Bottom Line

**Clean code = investment. Dirty code = debt. Pay as you go, or pay with interest later.**
