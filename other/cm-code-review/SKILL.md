---
name: cm-code-review
description: "Full review lifecycle — request reviews, handle feedback with technical rigor, and complete branch integration. Use when completing tasks, receiving feedback, or finishing feature branches."
token_budget: 1500
compressed: true
deprecated: false
---

# Code Review — Request + Receive + Complete

## TL;DR
- **Use when** task complete, before/during PR review
- **Pre-review**: lint, tests, diff scan, blast radius
- **Reads**: handoff/exec.json — **Writes**: handoff/review.json
- **Severity**: info | warn | error | critical
- **Next**: cm-quality-gate

> **Full review lifecycle in one skill:** Request → Receive → Integrate.

## Part A: Requesting Code Review

### When to Request

**Mandatory:**
- After each task in `cm-execution`
- After completing major features
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bugs

### How to Request

1. **Get git SHAs:**
   ```bash
   BASE_SHA=$(git rev-parse HEAD~1)
   HEAD_SHA=$(git rev-parse HEAD)
   ```

2. **Dispatch reviewer subagent** with:
   - What was implemented
   - Plan/requirements reference
   - Base and head SHAs
   - Brief description

3. **Act on feedback:**
   - Fix Critical issues immediately
   - Fix Important issues before proceeding
   - Note Minor issues for later
   - Push back if reviewer is wrong (with reasoning)

---

## Part B: Receiving Code Review

### When to Use
When receiving feedback — whether from human reviewers, AI reviewers, or code review subagents.

### The Protocol

```
1. READ feedback completely before responding
2. UNDERSTAND the technical reasoning
3. VERIFY if the feedback is technically correct
4. RESPOND with evidence, not agreement
```

### Response Framework

| Feedback Type | Response |
|--------------|----------|
| **Technically correct** | Fix it. Thank reviewer. |
| **Unclear intent** | Ask for clarification with specific questions |
| **Technically questionable** | Challenge with evidence (code, tests, docs) |
| **Stylistic preference** | Discuss trade-offs, defer to team convention |

### Red Flags — STOP

- Blindly implementing all suggestions without verification
- "Performative agreement" — saying yes without understanding
- Implementing a suggestion that breaks existing tests
- Making changes you can't justify technically

### Anti-Pattern: Performative Agreement

```
❌ "Good catch! Fixed."  (without verifying it's actually a problem)
✅ "I verified this: [evidence]. The suggestion is correct because [reason]. Fixed."
✅ "I investigated this: [evidence]. The current code is correct because [reason]."
```

---

## Part C: Finishing a Development Branch

### When to Use
When implementation is complete and all tests pass.

### The Process

1. **Verify current state:**
   ```bash
   npm run test:gate  # All tests must pass
   git status          # Working tree should be clean
   ```

2. **Present options to user:**

   | Option | When | Command |
   |--------|------|---------|
   | **Merge to main** | Feature ready | `git checkout main && git merge feature-branch` |
   | **Create PR** | Needs team review | `git push origin feature-branch` |
   | **Keep working** | More tasks remain | Continue on branch |
   | **Cleanup only** | Abandoned/merged | `git worktree remove path` |

3. **Execute chosen option**

4. **Cleanup:**
   - Remove the isolated worktree/workspace if your execution flow created one
   - Delete feature branch if merged
   - Update task tracking

### Rules
- Never merge with failing tests
- Never force push main/production
- Always use `cm-identity-guard` before git push

---

### Step FINAL: Record Review Learnings

After processing review feedback, ALWAYS update `.cm/CONTINUITY.md`:

- **Key Decisions:** If reviewer changed architecture approach, record with scope:
  `[Decision]: [Rationale] — scope: [global|module:{name}]`
- **Mistakes & Learnings:** If reviewer caught a pattern mistake, record with scope:
  - What Failed: [the pattern that was wrong]
  - How to Prevent: [correct pattern going forward]
  - Scope: [global | module:{name} | file:{path}]

**Anti-duplicate:** If similar learning exists, reinforce it instead of creating new.

> **Token savings:** Future code reviews in same project avoid repeating
> the same feedback. Reviewer patterns become accumulated knowledge.

---

## Integration

| Skill | Relationship |
|-------|-------------|
| `cm-execution` | Reviews after each task in execution |
| `cm-quality-gate` | Tests must pass before finishing branch |
| `cm-identity-guard` | Before git push |
| `cm-execution` | Cleanup isolated workspace after completion |

## Karpathy Discipline — Review Checklist

Block any PR/diff that violates these regardless of green tests:
- **Scope creep:** changed line that doesn't trace to the task → request removal.
- **Bloat:** new abstraction with one caller, premature config, error paths for impossible inputs → request simplification.
- **Side-effect edits:** unrelated formatting, renamed identifiers, "improved" comments not in scope → revert.
- **Hidden assumptions:** logic that depends on an unstated invariant → require it surfaced (test or doc) or rejected.
- **Weak goals:** PR description says "make it work" with no verifiable criterion → send back to planning.

**Review heuristic:** if you can't answer "what task forced this line?" for every changed line, the diff is too wide.

## The Bottom Line

**Review early. Verify feedback. Ship with evidence, not hope.**
