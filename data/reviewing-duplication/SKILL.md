---
name: reviewing-duplication
description: Automated tooling and detection patterns for identifying duplicate and copy-pasted code in JavaScript/TypeScript projects. Provides tool commands and refactoring patterns—not workflow or output formatting.
allowed-tools: Bash, Read, Grep, Glob
version: 1.0.0
---

# Duplication Review Skill

## Purpose

This skill provides automated duplication detection commands and manual search patterns. Use this as a reference for WHAT to check and HOW to detect duplicates—not for output formatting or workflow.

## Automated Duplication Detection

```bash
bash ~/.claude/plugins/marketplaces/claude-configs/review/scripts/review-duplicates.sh
```

**Uses:** jsinspect (preferred) or Lizard fallback

**Returns:**

- Number of duplicate blocks
- File:line locations of each instance
- Similarity percentage
- Lines of duplicated code

**Example output:**

```
Match - 2 instances
src/components/UserForm.tsx:45-67
src/components/AdminForm.tsx:23-45
```

## Manual Detection Patterns

When automated tools unavailable or for deeper analysis:

### Pattern 1: Configuration Objects

```bash

# Find similar object structures

grep -rn "const._=._{$" --include="*.ts" --include="*.tsx" <directory>
grep -rn "export.*{$" --include="_.ts" --include="_.tsx" <directory>
```

Look for: Similar property names, parallel structures

### Pattern 2: Validation Logic

```bash

# Find repeated validation patterns

grep -rn "if._length._<._return" --include="_.ts" --include="*.tsx" <directory>
grep -rn "if.*match._test" --include="_.ts" --include="*.tsx" <directory>
grep -rn "throw.*Error" --include="_.ts" --include="_.tsx" <directory>
```

Look for: Similar conditional checks, repeated error handling

### Pattern 3: Data Transformation

```bash

# Find similar transformation chains

grep -rn "\.map(" --include="_.ts" --include="_.tsx" <directory>
grep -rn "\.filter(" --include="_.ts" --include="_.tsx" <directory>
grep -rn "\.reduce(" --include="_.ts" --include="_.tsx" <directory>
```

Look for: Similar method chains, repeated transformations

### Pattern 4: File Organization Clues

```bash

# Find files with similar names (likely duplicates)

find <directory> -type f -name "_.ts" -o -name "_.tsx" | sort
```

Look for: Parallel naming (UserForm/AdminForm), similar directory structures

### Pattern 5: Function Signatures

```bash

# Find similar function declarations

grep -rn "function._{$" --include="_.ts" --include="_.tsx" <directory>
grep -rn "const._=._=>._{$" --include="_.ts" --include="_.tsx" <directory>
```

Look for: Matching parameter patterns, similar return types

## Duplication Type Classification

### Type 1: Exact Clones

**Characteristics:** Character-for-character identical
**Detection:** Automated tools catch these easily
**Example:**

```typescript
function validateEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

Appears in multiple files without changes.

### Type 2: Renamed Clones

**Characteristics:** Same structure, different identifiers
**Detection:** Look for similar line counts and control flow
**Example:**

```typescript
function getUserById(id: number) {
  /_ ... _/;
}
function getProductById(id: number) {
  /_ ... _/;
}
```

### Type 3: Near-miss Clones

**Characteristics:** Similar with minor modifications
**Detection:** Manual comparison after automated flagging
**Example:**

```typescript
function processOrders() {
  const items = getOrders();
  items.forEach((item) => validate(item));
  items.forEach((item) => transform(item));
  return items;
}

function processUsers() {
  const items = getUsers();
  items.forEach((item) => validate(item));
  items.forEach((item) => transform(item));
  return items;
}
```

### Type 4: Semantic Clones

**Characteristics:** Different code, same behavior
**Detection:** Requires understanding business logic
**Example:** Two different implementations of same algorithm

## Refactoring Patterns

### Pattern 1: Extract Function

**When:** Exact duplicates, 3+ instances
**Example:**

```typescript
// Before (duplicated)
if (user.age < 18) return false;
if (user.verified !== true) return false;
if (user.active !== true) return false;

// After (extracted)
function isEligible(user) {
  return user.age >= 18 && user.verified && user.active;
}
```

### Pattern 2: Extract Utility

**When:** Common operations repeated across files
**Example:**

```typescript
// Before (repeated in many files)
const formatted = date.toISOString().split('T')[0];

// After (utility)
function formatDate(date) {
  return date.toISOString().split('T')[0];
}
```

### Pattern 3: Template Method

**When:** Similar processing flows with variations
**Example:**

```typescript
// Before (structural duplicates)
function processA() {
  validate();
  transformA();
  persist();
}
function processB() {
  validate();
  transformB();
  persist();
}

// After (template)
function process(transformer) {
  validate();
  transformer();
  persist();
}
```

### Pattern 4: Parameterize Differences

**When:** Duplicates with single variation point
**Example:**

```typescript
// Before (duplicate with variation)
function getActiveUsers() {
  return users.filter((u) => u.status === 'active');
}
function getInactiveUsers() {
  return users.filter((u) => u.status === 'inactive');
}

// After (parameterized)
function getUsersByStatus(status) {
  return users.filter((u) => u.status === status);
}
```

## Severity Mapping

| Pattern                             | Severity | Rationale                                     |
| ----------------------------------- | -------- | --------------------------------------------- |
| Exact duplicates, 5+ instances      | critical | High maintenance burden, bug propagation risk |
| Exact duplicates, 3-4 instances     | high     | Significant maintenance cost                  |
| Structural duplicates, 3+ instances | high     | Refactoring opportunity with high value       |
| Exact duplicates, 2 instances       | medium   | Moderate maintenance burden                   |
| Structural duplicates, 2 instances  | medium   | Consider refactoring if likely to grow        |
| Near-miss clones, 2-3 instances     | medium   | Evaluate cost/benefit of extraction           |
| Test code duplication               | nitpick  | Acceptable for test clarity                   |
| Configuration duplication           | nitpick  | May be intentional, evaluate case-by-case     |

## When Duplication is Acceptable

**Test Code:**

- Test clarity preferred over DRY principle
- Explicit test cases easier to understand
- Fixtures can duplicate without issue

**Constants/Configuration:**

- Similar configs may be coincidental
- Premature abstraction creates coupling
- May evolve independently

**Prototypes/Experiments:**

- Early stage code, patterns unclear
- Wait for third instance before abstracting

**Different Domains:**

- Accidental similarity
- May diverge over time
- Wrong abstraction worse than duplication

## Red Flags (High Priority Indicators)

- Same bug appears in multiple locations
- Features require changes in N places
- Developers forget to update all copies
- Code review comments repeated across files
- Merge conflicts in similar code blocks
- Business logic duplicated across domains

## Analysis Priority

1. **Run automated duplication detection** (if tools available)
2. **Parse script output** for file:line references and instance counts
3. **Read flagged files** to understand context
4. **Classify duplication type** (exact, structural, near-miss, semantic)
5. **Count instances** (more instances = higher priority)
6. **Assess refactoring value:**
   - Instance count (3+ = high priority)
   - Likelihood of changing together
   - Complexity of extraction
   - Test vs production code
7. **Identify refactoring pattern** (extract function, utility, template, parameterize)
8. **Check for acceptable duplication** (tests, config, prototypes)

## Integration Notes

- This skill provides detection methods and refactoring patterns only
- Output formatting is handled by the calling agent
- Severity classification should align with agent's schema
- Do NOT include effort estimates or workflow instructions
- Focus on WHAT to detect and HOW to refactor, not report structure
