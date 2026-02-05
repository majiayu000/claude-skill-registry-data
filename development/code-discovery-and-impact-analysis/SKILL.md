---
name: code-discovery-and-impact-analysis
description: Discover project patterns and find all code usages before making changes. Use BEFORE renaming, refactoring, moving files, changing signatures, or adding features to ensure completeness and follow project conventions. Prevents incomplete refactors and assumption-based coding.
---

# Code Discovery & Impact Analysis

**Quick Reference:** Discover patterns and find all usages before making changes.

---

## Overview

This skill ensures Claude discovers both **how to change code** (patterns) and **what needs changing** (usages) before making modifications.

**Two-Phase Process:**
1. **Pattern Discovery** - Understand how similar code is organized (search_code)
2. **Usage Discovery** - Find ALL places that need updating (find_usage)

**Prevents:**
- Incomplete refactors (missing usages)
- Assumption-based coding (ignoring project patterns)
- Breaking changes (unknown dependencies)
- Inconsistent implementations (not following conventions)

---

## When to Use This Skill

**Automatically invoke BEFORE:**
- Renaming functions, classes, variables, or types
- Refactoring code structure
- Changing function/method signatures
- Moving or reorganizing files
- Modifying shared utilities or common code
- Updating types/interfaces
- Making architectural changes
- Adding new features (discover similar patterns first)

**Manual invocation when:**
- Uncertain about project conventions
- Need to understand how similar code is structured
- Planning major changes
- Reviewing code for completeness

---

## Depth Levels

**CRITICAL:** The tools behave differently based on maxResults:

### Pattern Discovery (search_code)
- **maxResults 1-3:** Returns FULL CODE CONTENT (`contentIncluded: true`)
- **maxResults 4+:** Returns ONLY METADATA - no code (`contentIncluded: false`)

**Recommendation:** Always use 1-3 for pattern discovery to see actual code

### Usage Discovery (find_usage)
- **All levels:** Always includes context (surrounding code lines)
- No difference in content quality between 1, 10, or 50 results

**Recommendation:** Use 10-15 by default, increase only if needed

---

### Minimal (maxResults: 1)
**Pattern Discovery:** Returns one complete code example
**Usage Discovery:** Returns one usage with context

**Use when:**
- Verifying a known pattern (just need confirmation)
- Checking if something exists
- Very localized, low-risk changes

### Light (maxResults: 2-3) - **DEFAULT for search_code**
**Pattern Discovery:** Returns 2-3 complete code examples with variations
**Usage Discovery:** Returns 2-3 usages with context

**Use when:**
- Learning how code is structured (see variations)
- Understanding naming/organization conventions
- Need to see different approaches
- Adding new features following existing patterns

**Why 2-3 for patterns:** This is the sweet spot - gets actual code content while showing variations

### Thorough (maxResults: 10-15) - **DEFAULT for find_usage**
**Pattern Discovery:** ⚠️ NOT RECOMMENDED - returns metadata only, no code
**Usage Discovery:** Returns 10-15 usages with full context

**Use when:**
- Finding all usages before refactoring
- Renaming functions/classes/variables
- Moving files or modules
- Changing shared utilities
- Complete impact analysis needed

**⚠️ Context Management:**
- search_code: Stay at 1-3 to get actual code
- find_usage: Use 10-15 by default
- Only increase to 20-50 if `results.length == maxResults` (indicates more exist)

---

## Discovery Workflow

### Step 1: Context Assessment

Ask yourself:
1. **What am I changing?**
   - Function/class/variable name?
   - File structure/organization?
   - Type/interface definition?
   - Shared utility or common code?

2. **What's the expected impact?**
   - Localized (same file/module)?
   - Module-wide (same feature area)?
   - Cross-cutting (used across codebase)?

3. **Which depth level?**
   - Minimal (1): Known patterns, just need reference
   - Light (2-3): Learning patterns, most changes (DEFAULT for patterns)
   - Thorough (4-15): Finding all usages, refactoring (DEFAULT for usages)

### Step 2: Pattern Discovery

**Goal:** Understand how to make changes correctly

Use `search_code` with appropriate maxResults (≤3 for code content):

```typescript
// Find similar classes/functions
search_code({
  query: "Service",
  types: ["class"],
  pathPattern: "services",
  maxResults: 3  // get actual code content
})

// Find similar file types
search_code({
  query: "repository",
  pathPattern: "modules",
  maxResults: 2  // light search, see variations
})
```

**Document findings:**
- File naming pattern
- Organization pattern (directory structure)
- Code structure (classes? functions? decorators?)
- Import patterns
- Naming conventions

### Step 3: Usage Discovery

**Goal:** Find ALL places that need updating

Use `find_usage` with appropriate maxResults (context always included):

```typescript
// Find all usages before renaming
find_usage({
  identifier: "oldFunctionName",
  maxResults: 15,  // start here, increase if results.length == maxResults
  exactMatch: true
})

// Find usages in specific area
find_usage({
  identifier: "ClassName",
  pathPattern: "modules/feature",
  maxResults: 10  // context always included regardless of count
})
```

**⚠️ Validate completeness:**
- If `results.length == maxResults`: Increase limit and search again
- If `results.length < maxResults`: All usages found
- Check for direct usages, indirect usages, dynamic usages, test files

### Step 4: Impact Analysis

Create a comprehensive map:
- Files affected: [count]
- Modules impacted: [list]
- Change complexity: [low/medium/high]
- Risk assessment: [rationale]
- Required changes: [detailed list with file:line]

### Step 5: Implementation with Validation

1. Make all identified changes
2. Follow discovered patterns
3. Validate completeness:
   ```typescript
   // Verify old references are gone
   find_usage({ identifier: "oldName", maxResults: 10 })
   // Expected: 0 results

   // Verify new references are correct
   find_usage({ identifier: "newName", maxResults: 10 })

   // Check for errors
   check_errors({ pathPattern: "[affected area]" })
   ```

---

## Common Scenarios

### Scenario 1: Renaming a Function

```
1. find_usage({ identifier: "oldFunctionName", maxResults: 15 })
   (increase if results.length == 15)
2. Document all locations (file:line)
3. Update function definition
4. Update all call sites
5. Validate: find_usage("oldFunctionName") → 0 results
6. Validate: find_usage("newFunctionName") → all updated
```

### Scenario 2: Refactoring a Module

```
1. Pattern discovery: search_code for similar modules (maxResults: 3)
   Get actual code to see structure
2. Usage discovery: find_usage for module exports (maxResults: 15)
3. Map all imports and dependencies
4. Plan refactor following discovered patterns
5. Update all usages
6. Validate with check_errors
```

### Scenario 3: Moving a File

```
1. Pattern discovery: where do similar files live?
   search_code({ query: "[file type]", maxResults: 2-3 })
   Get code to see organization
2. Find all imports: find_usage for file exports (maxResults: 15)
3. Move file to new location
4. Update all import statements
5. Verify: check_errors()
```

### Scenario 4: Changing Function Signature

```
1. find_usage({ identifier: "functionName", maxResults: 15 })
2. Analyze how function is currently called (context included in results)
3. Update function signature
4. Update every call site with new parameters
5. Validate with check_errors (catches missed call sites)
```

### Scenario 5: Adding New Feature

```
1. Pattern discovery: find similar features
   search_code({ query: "[similar feature]", maxResults: 2-3 })
   Get actual code to see implementation
2. Document patterns from code content:
   - File organization
   - Naming conventions
   - Code structure
   - Import patterns
3. Implement new feature following patterns
4. No usage discovery needed (new code)
```

---

## Output Template

Report discoveries using this format:

```markdown
## Discovery & Impact Report

**Change:** [What I'm changing]
**Depth:** [quick/balanced/comprehensive]
**Impact:** [localized/module-wide/cross-cutting]

### Phase 1: Pattern Discovery
**Found:** [N] similar patterns

1. **File Organization:** [pattern]
   - Location: [path pattern]
   - Example: [file path]

2. **Naming:** [pattern]
   - Examples: [list]

3. **Structure:** [description]
   - Approach: [classes/functions/etc.]

4. **Dependencies:** [import pattern]

**Recommendation:** [How to structure the change]

### Phase 2: Usage Discovery
**Found:** [N] usages across [M] files

| File | Line | Context |
|------|------|---------|
| [path] | [line] | [usage] |

**Completeness:**
- [✓/⚠️] All usages found
- [✓/⚠️] Indirect dependencies checked
- [✓/⚠️] Test files included

### Impact Analysis
**Affected:** [modules/files]
**Complexity:** [low/medium/high]
**Risk:** [low/medium/high] - [reason]

**Changes Required:**
1. [file:line] - [change]
2. [file:line] - [change]

### Implementation Plan
1. [Step 1]
2. [Step 2]

**Validation:**
1. find_usage([old]) → 0 results
2. find_usage([new]) → all updated
3. check_errors() → no issues

**Ready:** [yes/need clarification]
```

---

## Best Practices

### Always Do:
- ✓ Use find_usage before renaming anything
- ✓ Check if results.length == maxResults (may need higher limit)
- ✓ Document all findings before making changes
- ✓ Validate completeness after changes
- ✓ Follow discovered patterns, don't assume generic ones
- ✓ Include test files in usage discovery

### Never Do:
- ✗ Assume generic patterns without discovering project-specific ones
- ✗ Rename without running find_usage first
- ✗ Stop at maxResults if results.length == maxResults
- ✗ Skip validation after changes
- ✗ Ignore edge cases or unusual patterns

### When Uncertain:
- Ask the user for clarification
- Present multiple discovered patterns
- Run comprehensive search (higher maxResults)
- Document what you found and what's unclear

---

## Integration with Existing Skills

Works alongside:
- **api-design-patterns** - API-specific pattern validation
- **separation-of-responsibilities** - Layer separation checks
- **user-access-control** - Authorization pattern validation
- **module-architecture** - Module structure validation

**Workflow:**
1. Use THIS skill first (discover + find usages)
2. Make changes following discovered patterns
3. Use specific skills for domain validation
4. Use code-evaluation for final check

---

## Checklist

Before making changes:
- [ ] Ran pattern discovery (search_code)
- [ ] Documented patterns found
- [ ] Ran usage discovery (find_usage)
- [ ] Checked if more usages exist (results.length < maxResults)
- [ ] Created impact analysis
- [ ] Planned all required changes

After making changes:
- [ ] Updated all identified locations
- [ ] Validated old references gone (find_usage → 0)
- [ ] Validated new references correct
- [ ] Ran check_errors
- [ ] Followed discovered patterns

---

## Summary

**Key Takeaways:**
1. **search_code:** Use maxResults 1-3 to get actual code content (4+ returns metadata only)
2. **find_usage:** Always includes context, use 10-15 by default
3. Always discover patterns before assuming generic ones
4. Find ALL usages before renaming or refactoring
5. Validate completeness after changes
6. If results.length == maxResults, search again with higher limit
7. Pattern discovery + usage discovery = complete changes

**Remember:** This skill prevents incomplete refactors and ensures changes follow project conventions. Use it proactively, not reactively.
