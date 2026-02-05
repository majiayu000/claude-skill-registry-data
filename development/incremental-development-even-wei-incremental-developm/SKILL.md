---
name: incremental-development
description: "Structured incremental development workflow that enforces explicit scoping before implementation. Use when: (1) User says 'build', 'implement', 'develop', 'create feature', or 'add functionality', (2) Task involves multiple files or could have ripple effects, (3) User wants to avoid scope creep or premature implementation, (4) Breaking down complex tasks into verifiable steps. This skill prevents AI agents from jumping into code without a validated plan."
---

# Incremental Development

## Core Principle

Never write code until the scope is explicit and the approach is validated. Treat every task as having two distinct phases: **understand**, then **implement**.

## Phase 1: Understand (No Code)

Before touching any code, produce a brief plan covering:

1. **What files will be touched** — List specific paths
2. **What the change looks like at a high level** — One sentence per file
3. **What could go wrong** — Breaking changes, edge cases, dependencies
4. **What's explicitly out of scope** — Things you will NOT do

Output this plan and wait for confirmation before proceeding.

### Questions to Ask Yourself

- What is the smallest change that solves this?
- What existing patterns does this codebase use?
- What tests or contracts must still pass?

### Plan Output Format

Use this structure when presenting your plan:

```
## Plan

**Files:**
- `path/to/file1.ts` — Brief description of changes
- `path/to/file2.ts` — Brief description of changes

**Approach:**
[One paragraph explaining the strategy]

**Risks:**
- Risk 1: Description and mitigation
- Risk 2: Description and mitigation

**Out of scope:**
- Thing 1 (why it's excluded)
- Thing 2 (why it's excluded)

Ready to proceed?
```

## Phase 2: Implement (Incrementally)

Work in small, verifiable steps:

1. **One logical change per step** — If you can't describe it in one sentence, break it down
2. **Test or verify after each step** — Run tests, lint, or manually verify before continuing
3. **Commit mentally at each checkpoint** — Could you stop here and have working code?

### Implementation Output Format

Structure your implementation as discrete steps:

```
## Step 1: [Brief description]

[Implementation details]

✓ Verified: [How you verified it works]

---

## Step 2: [Brief description]

[Implementation details]

✓ Verified: [How you verified it works]
```

### Scope Guardrails

Do NOT:
- Refactor unrelated code you happen to notice
- Add abstractions "for future flexibility"
- Improve things outside the immediate task
- Change interfaces unless explicitly required

If you see something that should be fixed but is out of scope, note it separately and continue:

```
📝 Note for later: [Description of noticed issue]
```

## When to Re-plan

Return to Phase 1 if:
- You discover the change is larger than expected
- A dependency or assumption was wrong
- The user's requirements shift

Say: "I'm finding this is more complex than expected. Let me revise the plan before continuing."

## Escape Hatches

### Trivial Changes

For genuinely trivial changes (< 10 lines, single file, no interfaces affected), you may skip the formal plan—but still state what you're doing before doing it.

### User Override

If the user explicitly says "just do it" or "skip the planning," respect that—but note any risks you see.

## Summary

| Phase | Action | Output |
|-------|--------|--------|
| Understand | Analyze scope, identify risks | Plan document |
| Confirm | Wait for user approval | User says "proceed" |
| Implement | Small, verified steps | Working code + verification |
| Re-plan | If complexity exceeds expectations | Updated plan |
