---
name: comment-minimizer
description: "Eliminates noisy, redundant, and obvious comments (//, #, /* */); enforces self-documenting identifiers and clean code."
---

# Comment Minimizer & Clean Code Protocol

Enforce clean, self-documenting code by eliminating redundant comments and cognitive clutter.

---

## 1. Zero Obvious Comments Rule

Delete any comment that simply restates what the code expresses:
- Bad: `// increment counter` followed by `i++;`
- Bad: `# set user status` followed by `user.status = 'active'`
- Bad: `// check if list is empty` followed by `if (items.length === 0)`
- Rule: If a comment can be inferred from reading the identifier name, delete the comment.

---

## 2. Refactor Comments into Code

Instead of explaining confusing code with a comment, refactor the code to be self-explanatory:
1. **Explanatory Variables**:
   - Bad: `if (u.age >= 18 && u.hasVerifiedEmail && !u.isSuspended) // check if eligible`
   - Good: `const isEligibleToTransact = user.age >= 18 && user.hasVerifiedEmail && !user.isSuspended;`
2. **Extract Function**:
   - Bad: `// calculate tax with surcharge` + 15 lines of math
   - Good: `calculateTaxWithSurcharge(orderTotal, regionCode)`

---

## 3. Permissible Comments Only

Retain or add comments strictly in these 3 exceptional cases:
1. **Non-Obvious Business Rationale**: Explaining *why* a decision was made when it contradicts standard convention.
2. **Upstream Bug Workaround**: Linking to a specific issue tracker URL or vendor ticket.
3. **Complex Algorithmic Edge Cases**: Explaining non-trivial mathematical formulas or bitwise operations.
4. Delete all commented-out dead code; rely on git history instead.
