---
name: tech-debt-reducer
description: Systematic technical debt reduction and code optimization agent. Use when refactoring code, reducing complexity, eliminating code smells, improving performance, cleaning up unused code, or modernizing legacy patterns. Handles dependency updates, architecture improvements, and codebase health metrics.
metadata:
  author: coachone
  version: "1.0"
compatibility: Requires Node.js 18+, TypeScript. Optional ESLint, Prettier for linting.
allowed-tools: Bash(git:*) Bash(grep:*) Bash(find:*) Bash(npm:*) Bash(npx:*) Read Write
---

# 🔧 Tech Debt Reducer

Systematic approach to identifying, prioritizing, and eliminating technical debt while improving code quality and performance.

## Quick Reference

| Task | Command/Action |
|------|----------------|
| Analyze complexity | Run `scripts/analyze-complexity.ts` |
| Find unused code | Run `scripts/find-unused.ts` |
| Detect code smells | Run `scripts/detect-smells.ts` |
| Generate debt report | Run `scripts/debt-report.ts` |
| Prioritize debt items | Follow "Prioritization Matrix" section |

## Core Methodology

### Phase 1: Assessment (ALWAYS FIRST)

Before any refactoring, assess the current state:

```markdown
## 📊 Tech Debt Assessment

### Codebase Metrics
- **Total Files**: [count]
- **Lines of Code**: [count]
- **Average Complexity**: [score]
- **Test Coverage**: [percentage]
- **Dependency Age**: [stats]

### Identified Issues
| Category | Count | Severity | Effort |
|----------|-------|----------|--------|
| Code Smells | X | High/Med/Low | S/M/L |
| Unused Code | X | Low | S |
| Complex Functions | X | Med | M |
| Outdated Deps | X | High | M |
| Missing Types | X | Med | S |
```

### Phase 2: Categorization

Classify debt into categories:

| Category | Description | Examples |
|----------|-------------|----------|
| **Architecture** | Structural issues | Circular deps, wrong abstractions |
| **Code Quality** | Maintainability issues | Long functions, duplicate code |
| **Performance** | Speed/memory issues | N+1 queries, memory leaks |
| **Security** | Vulnerability issues | Outdated deps, exposed secrets |
| **Testing** | Coverage gaps | Missing tests, flaky tests |
| **Documentation** | Knowledge gaps | Missing docs, outdated comments |

### Phase 3: Prioritization Matrix

Use the **Impact vs Effort** matrix:

```
High Impact │  Quick Wins    │  Strategic
            │  (Do First)    │  (Plan Carefully)
────────────┼────────────────┼─────────────────
Low Impact  │  Fill-ins      │  Avoid
            │  (If Time)     │  (Not Worth It)
            └────────────────┴─────────────────
              Low Effort       High Effort
```

**Priority Formula**: `Score = (Impact × Risk) / Effort`

### Phase 4: Refactoring Patterns

See [references/REFACTORING_PATTERNS.md](references/REFACTORING_PATTERNS.md) for detailed patterns.

#### Safe Refactoring Workflow

```
1. ✅ Ensure tests exist (or write them first)
2. 📸 Create snapshot/checkpoint (git commit)
3. 🔧 Apply ONE refactoring at a time
4. 🧪 Run tests after each change
5. 📝 Commit with descriptive message
6. 🔄 Repeat
```

## Code Smell Detection

### Common Smells and Fixes

| Smell | Detection | Fix |
|-------|-----------|-----|
| **Long Function** | >50 lines | Extract methods |
| **Large Class** | >300 lines | Split into smaller classes |
| **Long Parameter List** | >4 params | Use parameter object |
| **Duplicate Code** | Similar blocks | Extract common function |
| **Dead Code** | Unreachable code | Remove safely |
| **Magic Numbers** | Hardcoded values | Extract constants |
| **God Object** | Does too much | Single responsibility |
| **Feature Envy** | Uses other class data | Move method |

### TypeScript-Specific Smells

| Smell | Example | Fix |
|-------|---------|-----|
| `any` abuse | `data: any` | Proper types |
| Missing null checks | `obj.prop` | Optional chaining `?.` |
| Type assertions | `as Type` | Type guards |
| Implicit any | No param types | Explicit types |
| No return types | Functions without | Add return types |

## Performance Optimization

### Quick Wins

```typescript
// ❌ Bad: Multiple re-renders
const items = data.filter(x => x.active).map(x => x.name);

// ✅ Good: Single pass with reduce
const items = data.reduce((acc, x) => {
  if (x.active) acc.push(x.name);
  return acc;
}, []);

// ❌ Bad: Creating functions in render
<Button onClick={() => handleClick(id)} />

// ✅ Good: useCallback or handler
const handleButtonClick = useCallback(() => handleClick(id), [id]);

// ❌ Bad: Missing memoization
const expensiveValue = computeExpensive(data);

// ✅ Good: useMemo for expensive computations
const expensiveValue = useMemo(() => computeExpensive(data), [data]);
```

### Database Query Optimization

```typescript
// ❌ Bad: N+1 Query
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { userId: user.id } });
}

// ✅ Good: Include related data
const users = await prisma.user.findMany({
  include: { posts: true }
});

// ✅ Better: Select only needed fields
const users = await prisma.user.findMany({
  select: { id: true, name: true, posts: { select: { title: true } } }
});
```

## Dependency Management

### Update Strategy

1. **Check outdated**: `npm outdated`
2. **Review changelogs** for breaking changes
3. **Update in order**: patch → minor → major
4. **Test after each major update**

### Cleanup Unused Dependencies

```bash
# Find unused dependencies
npx depcheck

# Analyze bundle size
npx webpack-bundle-analyzer

# Check for duplicates
npm dedupe
```

## Output Template

After completing debt reduction work:

```markdown
## 🔧 Tech Debt Report

### 📊 Before/After Metrics
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Complexity | X | Y | -Z% |
| Lines of Code | X | Y | -Z% |
| Test Coverage | X% | Y% | +Z% |
| Bundle Size | X KB | Y KB | -Z% |

### ✅ Changes Made
1. [Description of change 1]
2. [Description of change 2]

### 🧪 Tests
- [ ] All existing tests pass
- [ ] New tests added for refactored code
- [ ] No regressions detected

### 📝 Follow-up Items
- [ ] Item that needs future attention
```

## Safety Guidelines

- ❌ **NEVER** refactor without tests
- ❌ **NEVER** make multiple unrelated changes in one commit
- ❌ **NEVER** refactor and add features simultaneously
- ✅ **ALWAYS** commit working state before refactoring
- ✅ **ALWAYS** run tests after each change
- ✅ **ALWAYS** preserve external behavior

## Escalation Criteria

Stop and reassess if:
- Tests start failing unexpectedly
- Refactoring scope grows beyond initial estimate
- Performance degrades after optimization
- Breaking changes affect public API
