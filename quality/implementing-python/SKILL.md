---
name: implementing-python
description: Implements concise, streamlined Python code matching exact architect specifications. Use when writing Python code, creating modules, or when the user asks to implement features in Python.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebSearch, WebFetch
  argument-hint: [feature-name]
  stability: stable
  content-hash: sha256:202611f850f48c0ffb59ba553331765e55a322c2242757f1e2d31ce0a9340f3a
  last-verified-cc-version: 1.0.34
---

# Python Implementation

**Target**: $ARGUMENTS

Creates **focused, streamlined** Python implementations following architect
specifications exactly. No over-engineering.

## Python Standards

See `references/python-best-practices.md` for comprehensive Python guidelines.

## Workflow

1. **Read architect specifications** from provided documents
2. **Validate scope** - Simple (100-200 lines) vs Complex (500+ lines)
3. **Study existing patterns** in `src/` structure
4. **Implement minimal solution** matching stated functionality
5. **Create focused tests** matching task complexity
6. **Run `make validate`** and fix all issues

## Implementation Strategy

**Simple Tasks**: Minimal functions, basic error handling, lightweight
dependencies, focused tests

**Complex Tasks**: Class-based architecture, comprehensive validation,
necessary dependencies, full test coverage

**Always**: Use existing project patterns, pass `make validate`

## Output Standards

**Simple Tasks**: Minimal Python functions with basic type hints
**Complex Tasks**: Complete modules with comprehensive testing
**All outputs**: Concise, streamlined, no unnecessary complexity

## Quality Checks

Before completing any task:

```bash
make validate
```

All type checks, linting, and tests must pass.
