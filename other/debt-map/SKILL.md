---
description: Map and prioritise technical debt across your codebase
argument-hint: "[directory or project]"
allowed-tools:
  - Read
  - Agent
  - Glob
  - Grep
  - Bash(git log:*, wc:*, find:*)
---

Scan a codebase for technical debt. Score files by complexity, test coverage, age, and known issues. Output a prioritised debt payoff plan.

## Steps

### Step 1: Define scope

If the user specified a directory, use that. Otherwise scan the entire project (excluding node_modules, .git, vendor, build directories).

### Step 2: Automated scans (parallel agents)

**Agent 1 — TODO/FIXME/HACK scan:**
- Search for TODO, FIXME, HACK, XXX, TEMP, WORKAROUND comments
- For each: file, line, content, age (git blame)
- Categorise: technical debt, missing feature, known bug, cleanup needed

**Agent 2 — Complexity hotspots:**
- Find the largest files (by line count)
- Find files with the deepest nesting (proxy for complexity)
- Find files with the most functions/methods
- Identify files changed most frequently (`git log --format='' --name-only | sort | uniq -c | sort -rn | head -20`)
- Cross-reference: files that are BOTH complex AND frequently changed are top priority

**Agent 3 — Code health signals:**
- Check for deprecated API usage (grep for @deprecated, console.warn deprecation patterns)
- Find unused exports or dead code patterns
- Check dependency health (outdated packages in package.json / requirements.txt)
- Look for duplicated code patterns (similar function signatures, copy-paste indicators)

### Step 3: Score each debt item

Score on two dimensions:

**Impact (how much it hurts):**
- 3 = Affects users, causes bugs, blocks features
- 2 = Slows development, makes changes risky
- 1 = Code smell, readability issue, style concern

**Effort (how hard to fix):**
- 3 = Major refactor, multiple files, breaking changes
- 2 = Moderate work, contained to one area
- 1 = Quick fix, under an hour

**Priority = Impact / Effort** — high impact + low effort = fix first.

### Step 4: Generate the debt map

```markdown
# Technical Debt Map — [Project]

**Date:** [date]
**Files scanned:** [count]
**Debt items found:** [count]

## Summary
- **Critical (fix now):** [count]
- **High (fix this sprint):** [count]
- **Medium (schedule it):** [count]
- **Low (when convenient):** [count]

## Hotspots
Files with the most concentrated debt:

| File | Debt Items | Complexity | Change Frequency | Priority |
|------|-----------|------------|-----------------|----------|
| [file] | [count] | [high/med/low] | [commits/month] | Critical |

## Debt Inventory

### Critical Priority
1. **[file:line]** — [description]
   - Impact: [3] / Effort: [1]
   - Recommendation: [specific action]

### High Priority
[items]

### Medium Priority
[items]

### Low Priority
[items]

## Payoff Plan

### This Week
- [ ] [specific fix with file reference]
- [ ] [specific fix]

### This Month
- [ ] [larger refactor]
- [ ] [dependency updates]

### Backlog
- [ ] [items to schedule later]

## Metrics to Track
- Total TODO/FIXME count (currently: [X])
- Average file complexity score
- Outdated dependency count (currently: [X])

---
Re-run this command monthly to track progress.
```

Output the summary and top 3 items to fix first.
