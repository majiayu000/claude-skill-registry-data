---
name: simplify
description: Review code changes for quality, complexity, and duplication. Invoke with /simplify
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob
---

# Code Simplification Review

Analyze code changes for quality issues, simplification opportunities, and duplicate code patterns.

## Step 1: Verify Git Repository

```bash
git rev-parse --git-dir 2>&1
```

If this fails, respond with:
```
Error: Not a git repository. Navigate to a git repo to use /simplify.
```

## Step 2: Detect Branch Context

```bash
# Get current branch
BRANCH=$(git branch --show-current)

# Check for main/master
git rev-parse --verify main 2>/dev/null
git rev-parse --verify master 2>/dev/null
```

**Decision Logic:**
- On `main`/`master` → analyze uncommitted changes (`git diff HEAD`)
- On feature branch + `main` exists → compare to main (`git diff main...HEAD`)
- On feature branch + `master` exists → compare to master (`git diff master...HEAD`)

## Step 3: Gather Changes

Get the diff and changed files based on context:

**On main/master (uncommitted changes):**
```bash
git diff HEAD
git diff --name-status HEAD
```

**On feature branch:**
```bash
git diff main...HEAD   # or master...HEAD
git diff --name-status main...HEAD
```

If no changes found, report: "No changes to analyze."

## Step 4: Read Changed Files

For each changed file, read the full current content to understand context:
- Use the Read tool to get the complete file
- Note the specific lines that changed from the diff

## Step 5: Analyze for Issues

Review each changed file for these categories:

### 5.1 Code Quality Issues
- Poor error handling patterns
- Missing null/undefined checks where needed
- Inconsistent naming conventions
- Magic numbers or strings without constants
- Functions doing too many things
- Missing type annotations (TypeScript)
- Potential bugs or edge cases

### 5.2 Function Complexity & Pure Function Extraction

**Analyze each function for complexity indicators:**
- Line count (flag >30 lines)
- Nesting depth (flag >2 levels)
- Number of responsibilities (flag >1 clear responsibility)
- Cyclomatic complexity (multiple branches/conditions)
- Mixed concerns (I/O, validation, transformation, side effects in one function)

**Identify extraction candidates - logic that can become pure functions:**
- Data transformations (mapping, filtering, formatting)
- Validation logic (input checking, business rules)
- Calculations and computations
- String/date/number formatting
- Conditional logic that determines a value
- Any code block that takes input and produces output without side effects

**Pure function characteristics to enforce:**
- Same input → same output (deterministic)
- No side effects (no mutations, no I/O, no external state)
- Easy to test in isolation
- Self-documenting through clear naming

**Example extraction:**
```
BEFORE (mixed concerns):
function processOrder(order) {
  // validation
  if (!order.items || order.items.length === 0) throw new Error('Empty');
  // calculation
  const subtotal = order.items.reduce((sum, i) => sum + i.price * i.qty, 0);
  const tax = subtotal * 0.1;
  const total = subtotal + tax;
  // side effect
  await db.save({ ...order, total });
  return total;
}

AFTER (extracted pure functions):
const validateOrder = (order) => {
  if (!order.items?.length) throw new Error('Empty');
  return order;
};

const calculateOrderTotal = (items, taxRate = 0.1) => {
  const subtotal = items.reduce((sum, i) => sum + i.price * i.qty, 0);
  return { subtotal, tax: subtotal * taxRate, total: subtotal * (1 + taxRate) };
};

async function processOrder(order) {
  validateOrder(order);
  const totals = calculateOrderTotal(order.items);
  await db.save({ ...order, ...totals });
  return totals.total;
}
```

### 5.3 General Simplification Opportunities
- Deeply nested conditionals (>2 levels)
- Nested ternary operators (always flag these)
- Overly complex expressions
- Unnecessary abstractions or indirection
- Verbose code that could be clearer
- Repeated patterns that could use a helper

### 5.4 Duplicate Code
- Similar logic repeated across files
- Copy-pasted code with minor variations
- Patterns that could be extracted to shared utilities
- Repeated validation or transformation logic

## Step 6: Generate Report

Present findings grouped by category with confidence levels:

```
## Code Simplification Report

**Branch:** [branch name]
**Comparing:** [what vs what]
**Files analyzed:** [count]

---

### Quality Issues

#### [filename]:[line]
**Issue:** [description]
**Confidence:** High/Medium/Low
**Suggestion:**
```[language]
[suggested fix]
```

---

### Function Complexity (Extract Pure Functions)

#### [filename]:[function_name] (lines X-Y)
**Complexity:** [line count] lines, [nesting depth] levels deep, [responsibility count] responsibilities
**Problem:** [why it's too complex - mixed concerns, multiple responsibilities, etc.]
**Extract as pure functions:**
```[language]
[extracted pure function(s)]
```
**Refactored original:**
```[language]
[simplified orchestrating function]
```

---

### Simplification Opportunities

#### [filename]:[line]
**Current:** [what it does now]
**Problem:** [why it's complex]
**Suggested:**
```[language]
[simplified version]
```

---

### Duplicate Code

#### Pattern: [description]
**Found in:**
- [file1]:[lines]
- [file2]:[lines]

**Suggestion:** Extract to shared utility in [suggested location]
```[language]
[extracted helper]
```

---

## Summary

- **Quality issues:** [count]
- **Complex functions to refactor:** [count]
- **Simplification opportunities:** [count]
- **Duplicate patterns:** [count]

**Priority fixes:** [top 3 most impactful items]
```

## Guidelines

### What to Flag
- Functions over 30 lines (extract pure functions)
- Functions with multiple responsibilities (validation + transformation + I/O)
- Functions mixing pure logic with side effects
- Nesting deeper than 2 levels
- Nested ternaries (always)
- Copy-pasted code blocks
- Missing error handling at boundaries
- Unclear variable names
- Complex boolean expressions

### What NOT to Flag
- Style preferences without clear benefit
- Micro-optimizations that reduce readability
- Working code that's "fine" but not perfect
- Patterns consistent with rest of codebase
- Edge cases already handled elsewhere

### Confidence Levels
- **High**: Clear improvement, low risk of breaking
- **Medium**: Likely improvement, needs verification
- **Low**: Subjective or context-dependent

### Tone
- Be direct and actionable
- Explain the "why" briefly
- Provide concrete code suggestions
- Focus on maintainability over cleverness
