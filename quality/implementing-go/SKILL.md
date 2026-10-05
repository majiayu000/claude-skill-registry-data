---
name: implementing-go
description: Implements concise, streamlined Go code matching exact architect specifications. Use when writing Go code, creating packages, or when the user asks to implement features in Go.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebSearch, WebFetch
  argument-hint: [feature-name]
  stability: stable
  content-hash: sha256:efb2236c389be7d5d5311931961aeb3044c4ff360740706b80446fd0a74f7ae5
---

# Go Implementation

**Target**: $ARGUMENTS

Creates **focused, streamlined** Go implementations following architect
specifications exactly. No over-engineering.

## Go Standards

See `references/go-best-practices.md` for comprehensive Go guidelines.

## Workflow

1. **Read architect specifications** from provided documents
2. **Validate scope** — Simple (single package) vs Complex (multi-package)
3. **Study existing patterns** in package structure
4. **Implement minimal solution** matching stated functionality
5. **Create focused tests** matching task complexity
6. **Run validation** and fix all issues

## Implementation Strategy

**Simple Tasks**: Single package, minimal structs, error wrapping with `%w`, table-driven tests

**Complex Tasks**: Multi-package with interfaces, goroutines with context, custom error types, integration tests

**Always**: Use existing project patterns, pass validation

## Output Standards

**Simple Tasks**: Minimal functions with proper error handling
**Complex Tasks**: Complete packages with interfaces, tests, and documentation
**All outputs**: Concise, streamlined, no unnecessary complexity

## Quality Checks

Before completing any task:

```bash
go test ./... && go vet ./... && golangci-lint run
```

All tests, vet checks, and linting must pass.
