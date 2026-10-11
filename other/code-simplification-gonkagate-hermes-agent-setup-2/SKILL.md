---
name: code-simplification
description: "Simplify code for clarity without changing behavior. Use when code works but is harder to read, maintain, or extend than it should be; especially after a feature lands, during review cleanup, or when unnecessary complexity has accumulated. Use this as a general simplification skill, and prefer `typescript-refactoring-and-simplification-patterns` when the task needs deeper TypeScript backend refactor judgment."
---

# Code Simplification

> Inspired by the upstream
> [`code-simplification`](https://github.com/addyosmani/agent-skills/blob/main/skills/code-simplification/SKILL.md)
> skill.

## Overview

Simplify code by reducing complexity while preserving exact behavior. The goal
is not fewer lines. The goal is code that is easier to read, understand,
modify, and debug.

Every simplification should pass one test:

`Would a new teammate understand this faster than the original?`

## When to Use

- After a feature is working and tests pass, but the implementation feels
  heavier than it needs to be
- During review when readability or complexity issues are flagged
- When you encounter deeply nested logic, long functions, or unclear naming
- When refactoring code written under time pressure
- When consolidating related logic scattered across a small number of files
- After merging changes that introduced duplication or inconsistency

**When NOT to use:**

- The code is already clean and readable
- You do not understand what the code does yet
- The code is performance-critical and the simpler version may be slower
- You are about to replace the module entirely
- The task is really an architecture change or behavior change hiding inside
  "cleanup"
- The task needs TypeScript-backend-specific simplification judgment that
  belongs in `typescript-refactoring-and-simplification-patterns`

## Repository-Specific Anchors

For `hermes-agent-setup`, simplify in a way that preserves repository truth:

- read `AGENTS.md` before making contract-adjacent simplifications
- preserve the current shipped-runtime reality unless the task explicitly
  changes that contract
- do not simplify away security constraints around secret handling, config
  layering, or truthful diagnostics
- when a simplification affects CLI contract, docs, packaging, or mirrored
  skills, verify with `npm run ci`

Project consistency matters more than personal preference. In this repository,
follow `AGENTS.md`, nearby code, tests, and docs rather than importing an
external style.

## The Five Principles

### 1. Preserve Behavior Exactly

Do not change what the code does, only how it expresses it.

Preserve:

- inputs and outputs
- side effects and their order
- error behavior
- edge cases
- public contract wording when the surface is intentionally part of the shipped
  helper contract

Ask before every change:

- Does this produce the same result for every relevant input?
- Does this keep the same error behavior?
- Does this preserve the same side effects and ordering?
- Do existing tests still pass without being rewritten to accommodate drift?

If you are not sure a simplification preserves behavior, do not make it.

### 2. Follow Project Conventions

Simplification means making code more consistent with the codebase, not imposing
outside preferences.

Before simplifying:

1. Read `AGENTS.md` and nearby tests
2. Study how neighboring code handles similar patterns
3. Match the repository's style for:
   - naming
   - module structure
   - error handling
   - test shape
   - documentation truthfulness

If a simplification makes the code less aligned with local conventions, it is
churn, not improvement.

### 3. Prefer Clarity Over Cleverness

Explicit code beats compact code when the compact version requires a mental
pause to parse.

Examples:

```ts
// UNCLEAR
const label = isNew ? "New" : isUpdated ? "Updated" : "Active";

// CLEARER
function getStatusLabel(): string {
  if (isNew) return "New";
  if (isUpdated) return "Updated";
  return "Active";
}
```

```ts
// UNCLEAR
return input.length > 0 ? true : false;

// CLEARER
return input.length > 0;
```

### 4. Maintain Balance

Simplification can fail by over-simplifying.

Watch for these traps:

- inlining too aggressively and losing a useful concept name
- combining unrelated logic into one larger function
- removing an abstraction that exists for testability or future extension
- optimizing for line count instead of comprehension
- deleting scaffolding that intentionally documents current product boundaries

### 5. Scope to What Changed

Default to simplifying the code already under discussion.

Avoid drive-by cleanup in unrelated areas unless explicitly asked. Unscoped
simplification creates noisy diffs and risks regressions.

## The Simplification Process

### Step 1: Understand Before Touching

Before changing or removing anything, understand why it exists.

Answer these first:

- What is this code responsible for?
- What calls it and what does it call?
- What edge cases and error paths matter?
- Which tests define expected behavior?
- Why might it have been written this way?
- In this repository, is part of the complexity deliberate because it protects
  shipped-runtime truth, packaging, docs, or security invariants?

If you cannot answer those questions, read more context first.

### Step 2: Identify Simplification Opportunities

Look for concrete signals, not vague style discomfort.

**Structural complexity**

- Deep nesting, especially `3+` levels
- Long functions doing multiple jobs
- Nested ternaries
- Repeated conditionals
- Boolean flag parameters that hide intent

**Naming and readability**

- Generic names like `data`, `value`, `result`, `temp`
- Abbreviations that are not standard in the codebase
- Misleading names that hide side effects
- Comments explaining only what the code obviously does

**Redundancy**

- Duplicated logic
- Dead code or unreachable branches
- Thin wrappers that add no value
- Over-engineered patterns for a single simple use case
- Redundant type assertions

### Step 3: Apply Changes Incrementally

Make one simplification at a time.

For each simplification:

1. Make the smallest change
2. Run the relevant checks
3. If they pass, keep going
4. If they fail, revert and reconsider

Do not batch many unrelated simplifications into one hard-to-review change.

If the refactor is large enough to touch hundreds of lines, prefer automation
or break it into smaller slices instead of editing manually in one sweep.

### Step 4: Verify the Result

After simplifying, step back and compare before and after:

- Is the new version genuinely easier to understand?
- Did you introduce any pattern that feels foreign to the repository?
- Is the diff clean and easy to review?
- Does the change preserve truthful docs and shipped-runtime claims?

If the new version is not clearly better, revert it.

## High-Value Simplifications In This Repo

- tightening helper code or docs without overclaiming unsupported behavior
- deleting small dead branches, redundant helpers, or repeated doc wording
- reducing conditional clutter in tests while keeping contract intent visible
- shrinking duplicated skill-pack assertions while preserving readability
- clarifying naming around config layers, provider identity, and security
  invariants

## Common Rationalizations

| Rationalization                              | Reality                                                                                   |
| -------------------------------------------- | ----------------------------------------------------------------------------------------- |
| "It works, so leave it alone"                | Working code that is hard to read becomes slow and risky to change later.                 |
| "Fewer lines is always simpler"              | A one-line dense expression is often harder to parse than a short explicit block.         |
| "I will clean up this unrelated area too"    | Unscoped simplification creates noisy diffs and avoidable regressions.                    |
| "The original author must have had a reason" | Sometimes yes. Check context first, but do not preserve accidental complexity by default. |
| "I can refactor while changing behavior"     | Separate cleanup from behavior change whenever possible.                                  |

## Red Flags

- Simplification that requires changing tests because behavior drifted
- Code that ends up longer and harder to follow than before
- Renaming to match personal taste rather than repository conventions
- Removing error handling because it looks noisy
- Simplifying code you still do not understand
- Large cleanup commits that mix unrelated areas
- Simplification that weakens `AGENTS.md` contract truth or security guarantees

## Verification

After a simplification pass, confirm:

- [ ] Existing tests still pass without semantic rewrites
- [ ] Build succeeds
- [ ] Formatter and lint-style checks still pass
- [ ] The diff is incremental and reviewable
- [ ] No unrelated cleanup leaked into the change
- [ ] Local conventions still match the surrounding repository
- [ ] No security checks or contract guards were removed or weakened
- [ ] Current shipped-runtime truth is still described honestly
- [ ] `npm run ci` passed when the simplification touched contract surfaces
