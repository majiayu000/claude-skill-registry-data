---
name: implementing-typescript
description: Implements concise, streamlined TypeScript/React code matching exact architect specifications. Use when writing TypeScript code, creating modules, or when the user asks to implement features in TypeScript/React.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebSearch, WebFetch
  argument-hint: [feature-name]
  stability: stable
  content-hash: sha256:d2cac197cd70af4f908c5301064dc42bdc1fa79e68c7c3a236e7c97ae521a99e
---

# TypeScript Implementation

**Target**: $ARGUMENTS

Creates **focused, streamlined** TypeScript/React implementations following architect
specifications exactly. No over-engineering.

## TypeScript Standards

See `references/typescript-best-practices.md` for comprehensive TypeScript guidelines.
See `references/react-best-practices.md` for React patterns.
See `references/vite-conventions.md` for Vite project conventions.

## Workflow

1. **Read architect specifications** from provided documents
2. **Validate scope** — Simple (single module) vs Complex (multi-module)
3. **Study existing patterns** in `src/` structure
4. **Implement minimal solution** matching stated functionality
5. **Create focused tests** matching task complexity
6. **Run validation** and fix all issues

## Implementation Strategy

**Simple Tasks**: Single module, strict TypeScript, proper typing, inline exports

**Complex Tasks**: Multi-module with React components, async patterns, proper interfaces, custom hooks

**Always**: Use existing project patterns, pass validation

## Output Standards

**Simple Tasks**: Minimal functions with proper type annotations and error handling
**Complex Tasks**: Complete modules with interfaces, components, tests, and documentation
**All outputs**: Concise, streamlined, no unnecessary complexity

## Quality Checks

Before completing any task:

```bash
npx tsc --noEmit && npx vitest run && npx eslint .   # eslint: type-checked config, see references
```

All type checks, tests, and lints must pass.
