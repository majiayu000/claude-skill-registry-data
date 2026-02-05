---
name: reviewing-complexity
description: Analyze code complexity and maintainability including cyclomatic complexity, function length, nesting depth, and cognitive load. Use when reviewing code maintainability, refactoring candidates, or technical debt assessment.
allowed-tools: Bash, Read, Grep, Glob
version: 1.0.0
---

# Complexity Review Skill

## Purpose

Provides automated complexity analysis commands and manual detection patterns for identifying hard-to-maintain code. Use this as a reference for WHAT to check and HOW to detect complexity issues—not for output formatting or workflow.

## Automated Complexity Analysis

Run Lizard complexity analyzer:

```bash
bash ~/.claude/plugins/marketplaces/claude-configs/review/scripts/review-complexity.sh
```

**Returns:**

- Functions with cyclomatic complexity >= 15
- NLOC (Non-comment Lines Of Code)
- CCN (Cyclomatic Complexity Number)
- Token count, parameter count, function length
- Format: `NLOC  CCN  Token  Parameter  Length  Location`

**Example output:**

```
45 18 234 5 50 src/utils.ts:calculateTotal
```

## Complexity Metrics Reference

### Cyclomatic Complexity (CCN)

Counts independent paths through code based on decision points: if/else, switch, loops, ternary operators, logical operators (&&, ||)

**Thresholds:**

- 1-5: Simple, easy to test
- 6-10: Moderate, acceptable
- 11-15: Complex, consider refactoring
- 16+: High risk, refactor recommended

### Function Length (NLOC)

Non-comment lines in a function.

**Thresholds:**

- 1-20: Good
- 21-50: Acceptable
- 51-100: Consider splitting
- 100+: Too long, refactor

### Parameter Count

**Thresholds:**

- 0-3: Good
- 4-5: Acceptable
- 6+: Too many, use object parameter

### Nesting Depth

Levels of indentation.

**Thresholds:**

- 1-2: Good
- 3: Acceptable
- 4+: Too deep, simplify

## Manual Detection Patterns

When automated tools unavailable or for deeper analysis, use Read/Grep to detect:

### Multiple Responsibilities

```bash

# Find functions with multiple comment sections

grep -A 50 "function\|const._=._=>" <file> | grep -c "^[[:space:]]\*\/\/"
```

Look for: Functions with validation + transformation + persistence + notification in one place

### Deep Nesting

```bash

# Find lines with >3 levels of indentation (12+ spaces)

grep -n "^[[:space:]]{12,}" <file>
```

Look for: Nested if statements >3 levels deep

### Long Conditional Chains

```bash

# Find files with many else-if statements

grep -c "else if" <file>
```

Look for: Functions with >5 else-if branches

### High Parameter Count

```bash

# Find function declarations

grep -n "function._([^)]_,[^)]_,[^)]_,[^)]_,[^)]_," <file>
```

Look for: Functions with >5 parameters

### Mixed Abstraction Levels

Use Read to identify functions that mix:

- High-level orchestration with low-level string manipulation
- Business logic with infrastructure concerns
- Domain logic with presentation logic

### Cognitive Load Indicators

**Magic Numbers:**

```bash
grep -n "[^a-zA-Z_][0-9]{2,}[^a-zA-Z_]" <file>
```

Look for: Unexplained numeric literals

**Excessive Comments:**

```bash

# Count comment density

total_lines=$(wc -l < <file>)
comment_lines=$(grep -c "^[[:space:]]\*\/\/" <file>)
```

Look for: Comment ratio >20% (indicates unclear code)

**Side Effects:**

```bash
grep -n "this\.\|global\.\|window\.\|process\.env" <file>
```

Look for: Functions accessing external state

## Complexity Sources to Identify

When reviewing flagged functions, identify specific causes:

| Pattern                   | Detection Method               | Example                                   |
| ------------------------- | ------------------------------ | ----------------------------------------- |
| Multiple Responsibilities | Function does >1 distinct task | Validation + transformation + persistence |
| Deep Nesting              | Indentation >3 levels          | if > if > if > if                         |
| Long Conditional Chains   | >5 else-if branches            | type === 'A' \|\| type === 'B' \|\| ...   |
| Mixed Abstraction Levels  | High + low level code mixed    | orchestration + string manipulation       |
| Magic Numbers             | Unexplained literals           | if (status === 42)                        |
| Excessive Comments        | Comment ratio >20%             | Every line needs explanation              |
| Side Effects              | Modifies external state        | Accesses globals, mutates inputs          |
| High Parameter Count      | >5 parameters                  | function(a, b, c, d, e, f)                |

## Refactoring Patterns

Suggest these patterns based on complexity source:

### Extract Method

**When:** Function >50 lines or multiple responsibilities
**Pattern:**

```typescript
// Before: 40 lines doing validation + transformation + persistence
function process(data) {
  /_ 40 lines _/;
}

// After: 3 focused functions
function process(data) {
  validate(data);
  const transformed = transform(data);
  persist(transformed);
}
```

### Guard Clauses

**When:** Deep nesting >3 levels
**Pattern:**

```typescript
// Before: Nested ifs
if (valid) {
  if (ready) {
    if (allowed) {
      /_ logic _/;
    }
  }
}

// After: Early returns
if (!valid) return;
if (!ready) return;
if (!allowed) return;
/_ logic _/;
```

### Replace Conditional with Lookup

**When:** >5 else-if branches
**Pattern:**

```typescript
// Before: Long if-else chain
if (type === 'A') {
  doA();
} else if (type === 'B') {
  doB();
}

// After: Lookup table
const strategies = { A: doA, B: doB };
strategies[type]();
```

### Parameter Object

**When:** >5 parameters
**Pattern:**

```typescript
// Before: Many parameters
function create(name, email, age, address, phone, city) {}

// After: Object parameter
function create(userData: UserData) {}
```

### Extract Variable

**When:** Complex conditionals or magic numbers
**Pattern:**

```typescript
// Before: Unclear condition
if (user.age > 18 && user.status === 'active' && user.balance > 100) {
}

// After: Named boolean
const isEligibleUser = user.age > 18 && user.status === 'active' && user.balance > 100;
if (isEligibleUser) {
}
```

## Severity Mapping

Use these criteria when classifying findings:

| Metric            | Severity | Rationale                        |
| ----------------- | -------- | -------------------------------- |
| CCN >= 25         | critical | Extremely high risk, untestable  |
| CCN 20-24         | high     | High risk, difficult to maintain |
| CCN 15-19         | high     | Complex, refactor recommended    |
| NLOC > 100        | high     | Too long, hard to understand     |
| Nesting depth > 4 | high     | Hard to follow logic             |
| CCN 11-14         | medium   | Moderate complexity              |
| NLOC 51-100       | medium   | Consider splitting               |
| Parameters > 5    | medium   | Hard to use correctly            |
| Nesting depth 4   | medium   | Approaching complexity limit     |
| CCN 6-10          | nitpick  | Acceptable but monitor           |
| NLOC 21-50        | nitpick  | Acceptable length                |
| Parameters 4-5    | nitpick  | Consider object parameter        |

## Red Flags

Watch for these warning signs when reviewing complex functions:

- **Needs comments to explain logic** - Code should be self-documenting
- **Hard to write unit tests** - High complexity makes testing difficult
- **Frequent source of bugs** - Check git history for bug fixes
- **Developers avoid modifying** - Ask team about "scary" functions
- **Takes >5 minutes to understand** - Cognitive load too high
- **Mixed abstraction levels** - Doing too many things

## Analysis Priority

1. **Run Lizard script first** (if available)
2. **Parse Lizard output** for functions with CCN >= 15
3. **Read flagged functions** using Read tool
4. **Identify complexity sources** using patterns above
5. **Apply manual detection patterns** if Lizard unavailable
6. **Cross-reference with git history** (frequent changes = high-risk complexity)
7. **Suggest specific refactoring patterns** based on complexity source

## Integration Notes

- This skill provides detection methods and refactoring patterns only
- Output formatting is handled by the calling agent
- Severity classification should align with agent's schema
- Do NOT include effort estimates (handled by agent if needed)
- Focus on identifying complexity, not prescribing workflow
