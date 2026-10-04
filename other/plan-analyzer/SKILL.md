---
name: plan-analyzer
description: "Analyze a plan .md file for issues, concerns, and improvements. Verifies assumptions against the actual codebase and provides direct actionable feedback."
disable-model-invocation: false
context: fork
allowed-tools: Read Grep Glob Bash
---

# Plan Analyzer

Critically review an implementation plan file against the actual codebase. Verify every assumption, identify risks, and provide direct actionable feedback.

## Input

The user provides a path to a `.md` plan file (typically in `~/.claude/plans/`). If no path is given, check `~/.claude/plans/` for the most recently modified `.md` file and confirm with the user.

## Workflow

### Step 1: Read and Parse the Plan

Read the plan file. Identify:
- **Files referenced** — every file path mentioned as created, modified, or explicitly not modified
- **Assumptions** — stated invariants, safety claims, behavioral expectations
- **Data flow** — how state moves between composables/components/stores
- **Risk areas** — anything marked "Medium" or "High" risk, or touching shared utilities

### Step 2: Verify Against Codebase (Parallel)

Launch parallel reads/searches to verify the plan's claims:

**For every file listed as modified:**
- Read the file — confirm the line numbers, variable names, and structure match the plan's description
- Check that the plan's "current approach" column accurately describes what exists

**For every file listed as NOT modified:**
- Grep for the key patterns the plan claims are untouched (watchers, computed properties, keys)
- Confirm no hidden coupling would be affected by the proposed changes

**For stated invariants:**
- Trace the actual code path to verify the claim holds
- Look for edge cases the plan may not have considered

**For new patterns introduced:**
- Search for existing precedents in the codebase (does this pattern already exist? is there a convention?)
- Check if the approach conflicts with existing abstractions

### Step 3: Analyze for Issues

Evaluate each aspect with specific attention to:

**Correctness**
- Will the proposed code actually work as described?
- Are there race conditions, timing issues, or ordering dependencies?
- Do reactive dependencies chain correctly (watchers, computed, refs)?

**Completeness**
- Are all affected files accounted for? Grep for usages of modified APIs/exports
- Are edge cases covered? (empty states, error states, SSR vs client, navigation patterns)
- Does the test plan cover the critical paths and the stated invariants?

**Coupling & Side Effects**
- Do changes to shared utilities (composables, stores, utils) affect other consumers?
- Are there implicit dependencies through global state (`useState`, stores, provide/inject)?
- Could the changes cause hydration mismatches?

**Implementation Order**
- Can the steps actually be executed in the stated order?
- Are there hidden dependencies between steps?
- Can intermediate steps be tested independently?

### Step 4: Present Findings

Structure feedback as a direct assessment:

```markdown
## What's solid
- [Briefly note what the plan gets right — validates confidence in the approach]

## Issues and concerns

**1. [Issue title] (HIGH/MEDIUM/LOW RISK)**
[Explanation with specific file:line references]
[Why it's a problem]
**Suggestion:** [Concrete fix]

**2. [Next issue]...**

## Summary of recommended changes

| Priority | Issue | Action |
|----------|-------|--------|
| High | ... | ... |
| Medium | ... | ... |
| Low | ... | ... |

## Verdict
[Ready to implement / Needs revisions / Needs rethinking]
```

**Severity levels:**
- **HIGH** — Will cause bugs, data loss, or regressions if not fixed
- **MEDIUM** — Creates maintenance burden, hidden coupling, or fragile behavior
- **LOW** — Stylistic, minor UX concern, or nice-to-have improvement

### Step 5: On Re-review

If the user updates the plan and asks for re-review:
- Re-read the file
- Check each previously raised concern against the updated text
- Call out which issues were addressed well, which were partially addressed, and which remain
- Only raise new concerns if the update introduced them

## Principles

- **Verify, don't trust** — read the actual files, don't take the plan's descriptions at face value
- **Be specific** — reference file:line, show the actual code that contradicts or confirms claims
- **Be actionable** — every concern must have a concrete suggestion
- **Don't nitpick** — focus on things that would cause bugs or maintenance pain, not style preferences
- **Acknowledge what's good** — plans that correctly identify risks and invariants deserve recognition
