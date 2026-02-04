---
name: lint-instructions
description: Detect and fix violations of project instructions defined in .claude/rules/. Use when checking code compliance, reviewing changes, or when the user asks about instruction violations.
---

# Instruction Linter

Validates code against project-specific rules defined in `.claude/rules/`.

## When to Use

- Before committing changes
- After implementing a new feature
- When reviewing code for compliance
- When user asks to check instruction compliance

## Instructions

### 1. Load All Rules

Read all instruction files:

```
.claude/rules/code-style.md
.claude/rules/cross-framework.md
.claude/rules/packages/core.md
.claude/rules/packages/react.md
.claude/rules/packages/vue.md
.claude/rules/packages/svelte.md
.claude/rules/demo.md
```

### 2. Check Categories

For each category, verify compliance:

#### Code Style (code-style.md)
- [ ] Function declarations: exports use `function`, callbacks use arrows
- [ ] Type safety: `satisfies` over type annotations, type guards over `as` casts
- [ ] Documentation: JSDoc on public APIs

#### Cross-Framework (cross-framework.md)
- [ ] Component parity: all components exist in React/Vue/Svelte
- [ ] Props equivalence: same props interface across frameworks
- [ ] Hook/Composable/Rune equivalence: same options, similar return types
- [ ] Core centralization: shared types/constants/utils in @vizel/core

#### Core Package (packages/core.md)
- [ ] No framework dependencies (React, Vue, Svelte)
- [ ] All shared types defined here
- [ ] All constants defined here

#### Framework Packages (packages/react.md, vue.md, svelte.md)
- [ ] Only framework-specific wrappers
- [ ] Correct idioms (hooks vs composables vs runes)
- [ ] Proper context usage

### 3. Report Format

```markdown
## Instruction Compliance Report

### ✅ Passing
- [rule]: [description]

### ❌ Violations
- [rule]: [file:line] - [issue description]
  - **Fix**: [suggested fix]

### ⚠️ Warnings
- [rule]: [potential issue]
```

### 4. Auto-Fix When Possible

For fixable violations:
1. Show the violation
2. Propose the fix
3. Apply if user approves

## Example Usage

User: "Check if my changes follow the project rules"

1. Read recent git changes: `git diff --name-only HEAD~1`
2. Load relevant rule files based on changed paths
3. Check each changed file against applicable rules
4. Report violations with fixes

## Checklist Commands

Quick checks to run:

```bash
# Biome handles: formatting, imports, exports, naming
bun run check

# Type safety
bun run typecheck

# Build verification
bun run build
```

## Common Violations

| Violation | Rule | Fix |
|-----------|------|-----|
| `export const fn = () => {}` | code-style | Use `export function fn() {}` |
| `data as Type` | code-style | Use type guard function |
| Type in framework package | cross-framework | Move to @vizel/core |
| Missing component in one framework | cross-framework | Add equivalent component |
| `default export` | Biome | Use named export |
