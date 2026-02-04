---
name: pre-commit-review
description: ADVISORY validation of code against design principles that linters cannot enforce. Use after linter passes and tests pass to validate design quality. Categorizes findings as Design Debt, Readability Debt, or Polish Opportunities. Does NOT block commits.
---

# Pre-Commit Design Review

Expert design analysis that detects issues linters can't catch. Returns detailed report to caller with categorized findings and fix recommendations.

## What This Skill Does

**Pure Analysis & Reporting** - Generates report, doesn't fix anything or invoke skills.

### Input
- Files to review (specific files or all staged changes)
- Review mode: `full` (first run) or `incremental` (subsequent runs)
- Previous findings (optional, for incremental mode)
- Context (invoked by refactoring, orchestrator, subagent, or user)

### Output
- Structured report with categorized findings
- Each finding: `file:line`, issue, why it matters, fix strategy, effort estimate
- Prioritized by impact and effort
- Format: Parseable for combined analysis (when invoked by orchestrator)

### Invocation Modes

**1. Direct Skill Invocation** (User or Orchestrator)
- Full control, can invoke other skills
- Can make changes based on findings
- Interactive mode with user feedback

**2. Subagent Mode** (Task tool with go-code-reviewer)
- Read-only analysis, returns report only
- Cannot invoke other skills
- Used for parallel execution by orchestrator
- Designed for speed and focused analysis

### What Reviewer Detects (That Linters Can't)
- Primitive obsession (with juiciness scoring)
- Unstorified functions (mixed abstraction levels)
- Missing domain concepts (implicit types that should be explicit)
- Non-self-validating types (defensive code in methods)
- Poor comment quality (explaining what instead of why)
- File structure issues (too long, too many types)
- Generic package extraction opportunities
- Design bugs (nil deref, ignored errors, resource leaks)
- Test quality (weak assertions, missing use cases, mock overuse, conditionals in tests)

**See [reference.md](./reference.md) for complete detection checklist with examples**

## Who Invokes This Skill

1. **@refactoring skill** - After applying patterns, validates design quality remains high
2. **@linter-driven-development** - Phase 4, checks design quality after linter passes
3. **User** - Manual code review before commit

## Workflow

### Full Review Mode (First Run)

```
1. Read all files under review (using Read tool)
2. Apply design principles checklist from reference.md (LLM reasoning)
3. Search for usage patterns across codebase (using Grep tool)
4. Categorize findings:
   🐛 Bugs (nil deref, ignored errors, resource leaks)
   🔴 Design Debt (types, architecture, validation)
   🟡 Readability Debt (abstraction, flow, clarity)
   🟢 Polish (naming, docs, minor improvements)
5. Generate structured report with recommendations
6. Return report to caller (doesn't invoke other skills or make fixes)
```

### Incremental Review Mode (Subsequent Runs)

Used after fixes have been applied to verify resolution and detect new issues.

```
1. Read ONLY changed files since last review (using git diff)
2. Compare against previous findings:
   - Mark resolved issues as ✅ Fixed
   - Identify issues that still exist
3. Analyze changed code for NEW issues introduced by fixes
4. Generate delta report:
   - ✅ Fixed: Issues from previous run that are now resolved
   - ⚠️ Remaining: Issues that still need attention
   - 🆕 New: Issues introduced by recent changes
5. Return concise delta report (not full analysis)
```

**When to Use Incremental Mode:**
- After @refactoring skill applies fixes
- During iterative fix loop in Phase 4 of autopilot workflow
- User requests re-review after making changes

**Benefits:**
- Faster execution (only analyzes changed files)
- Clear feedback on what was fixed vs what remains
- Detects regressions introduced by fixes

## Detection Approach

**LLM-Powered Analysis** (not AST parsing or metrics calculation):

The reviewer reads code like a senior developer and applies design principles:
- Reads files with Read tool
- Searches patterns with Grep tool (find usages, duplications)
- Applies checklist from reference.md using LLM reasoning
- Pattern matches against anti-patterns
- Counts occurrences and calculates juiciness scores
- Generates findings with specific locations and fix guidance

**Division of Labor:**
- **Linter handles**: Complexity metrics, line counts, formatting, syntax
- **Reviewer handles**: Design patterns, domain modeling, conceptual issues

## Report Format

### Full Report (First Run)

```
📊 CODE REVIEW REPORT
Scope: [files reviewed]
Mode: FULL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total findings: 18
🐛 Bugs: 2 (fix immediately)
🔴 Design Debt: 5 (fix before commit)
🟡 Readability Debt: 8 (improves maintainability)
🟢 Polish: 3 (nice to have)

Estimated fix effort: 3.5 hours

[Detailed findings by category]
[Recommendations by priority]
[Skills to use for fixes]
```

### Incremental Report (Subsequent Runs)

```
📊 CODE REVIEW DELTA REPORT
Scope: [changed files only]
Mode: INCREMENTAL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Fixed: 4 (resolved from previous run)
⚠️ Remaining: 2 (still need attention)
🆕 New: 1 (introduced by recent changes)

[Detailed delta findings]
```

### Structured Output for Orchestrator Parsing

When invoked as subagent for combined analysis, output follows strict format:

```
🐛 BUGS
────────────────────────────────────────────────
file:line | Issue description | Why it matters | Fix strategy | Effort: [Trivial/Moderate/Significant]

🔴 DESIGN DEBT
────────────────────────────────────────────────
file:line | Issue description | Why it matters | Fix strategy | Effort: [Trivial/Moderate/Significant]

🟡 READABILITY DEBT
────────────────────────────────────────────────
file:line | Issue description | Why it matters | Fix strategy | Effort: [Trivial/Moderate/Significant]

🟢 POLISH
────────────────────────────────────────────────
file:line | Issue description | Why it matters | Fix strategy | Effort: [Trivial/Moderate/Significant]
```

**Effort Estimates:**
- **Trivial**: <5 minutes (extract constant, rename variable)
- **Moderate**: 5-20 minutes (extract function, storifying, create simple type)
- **Significant**: >20 minutes (architectural refactoring, complex type extraction)

**file:line Format:** Must be exact for orchestrator to correlate with linter errors
- Example: `pkg/parser.go:45`
- NOT: `parser.go line 45` or `pkg/parser.go (line 45)`

**See [examples.md](./examples.md) for complete report examples**

## What This Skill Does NOT Do

- ❌ Invoke other skills (@refactoring, @code-designing, @testing)
- ❌ Fix anything or make code changes
- ❌ Make decisions on behalf of user
- ❌ Parse AST or calculate complexity metrics (linter does this)
- ❌ Run linter (caller does this)
- ❌ Iterate or loop (caller decides whether to re-invoke)
- ❌ Block commits (findings are advisory)

## Integration with Other Skills

### Invoked by @refactoring
```
Refactoring completes → invoke reviewer → analyze report:
- Bugs found? → Fix immediately, re-run linter
- Design debt found? → Apply another refactoring pattern
- All clean? → Return success to orchestrator
```

### Invoked by @linter-driven-development
```
Phase 4 (after linter passes):
1. Invoke reviewer on all staged changes
2. Receive categorized report
3. Present findings to user with options:
   - Commit as-is (accept debt knowingly)
   - Fix critical issues only (bugs + design debt)
   - Fix all recommended (bugs + design + readability)
   - Fix everything (including polish)
4. Based on user choice:
   - Invoke @refactoring or @code-designing for chosen fixes
   - Return to Phase 3 (linter loop)
   - Iterate until user satisfied
```

### Invoked by User
```
Manual review request:
1. User invokes: @pre-commit-review on path/to/file.go
2. Receive detailed report
3. User decides how to proceed
4. User may invoke @refactoring or @code-designing for fixes
```

## Review Scope

**Primary Scope**: Changed code in commit
- All modified lines
- All new files
- Specific focus on design principle adherence

**Secondary Scope**: Context around changes
- Entire files containing modifications
- Flag patterns/issues outside commit scope (in BROADER CONTEXT section)
- Suggest broader refactoring opportunities if valuable

## Advisory Nature

**This review does NOT block commits.**

Purpose:
- ✅ Provide visibility into design quality
- ✅ Offer concrete improvement suggestions with examples
- ✅ Help maintain coding principles
- ✅ Guide refactoring decisions

Caller (or user) decides:
- Commit as-is (accept debt knowingly)
- Fix critical debt before commit (bugs, major design issues)
- Fix all debt before commit (comprehensive cleanup)
- Expand scope to broader refactor (when broader context issues found)

## Finding Categories

Findings are categorized by technical debt type and severity:

### 🐛 Bugs
**Will cause runtime failures or correctness issues**
- Nil dereferences, ignored errors, resource leaks
- Invalid nil returns, race conditions
- Fix immediately before any other work

### 🔴 Design Debt
**Will cause pain when extending/modifying code**
- Primitive obsession, missing domain types
- Non-self-validating types
- Wrong architecture (horizontal vs vertical)
- Fix before commit recommended

### 🟡 Readability Debt
**Makes code harder to understand and work with**
- Mixed abstraction levels, not storified
- Functions too long or complex
- Poor naming, unclear intent
- Fix improves team productivity

### 🟢 Polish Opportunities
**Minor improvements for consistency and quality**
- Non-idiomatic naming, missing examples
- Comment improvements, minor refactoring
- Low priority, nice to have

**See [reference.md](./reference.md) for detailed principles and examples for each category**

## Key Capabilities

**Detects 8 Issue Categories:**
1. Primitive Obsession - with juiciness scoring algorithm
2. Storifying - detects mixed abstraction levels
3. Missing Domain Concepts - identifies implicit types
4. Self-Validating Types - finds defensive code patterns
5. Comment Quality - analyzes what vs why
6. File Structure - checks size and responsibility boundaries
7. Testing Approach - validates test structure and quality
8. Design Bugs - catches common runtime issues

**For complete detection patterns and examples, see [reference.md](./reference.md)**
**For real-world review scenarios, see [examples.md](./examples.md)**

## Integration with Orchestrator

This skill is automatically invoked by @linter-driven-development workflow:
- **Phase 4**: Design review after linter passes
- **Iterative**: Re-invoked after fixes until clean or user accepts debt
- **Advisory**: Never blocks, always presents options

See [linter-driven-development workflow](../linter-driven-development/SKILL.md) for complete flow.
