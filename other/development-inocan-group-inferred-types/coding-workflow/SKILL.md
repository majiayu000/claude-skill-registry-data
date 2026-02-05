---
name: coding-workflow
description: Best practices for coding, debugging, and refactoring. Use when reviewing code, debugging issues, refactoring, or establishing coding patterns.
---

# Coding Workflow Best Practices

## Code Review Approach

1. **Understand before changing**: Read the code thoroughly before suggesting modifications
2. **Check for patterns**: Look for existing patterns in the codebase and follow them
3. **Consider edge cases**: Think about null, empty, boundary conditions
4. **Security awareness**: Watch for injection, XSS, improper auth patterns

## Debugging Strategy

1. **Reproduce first**: Confirm the issue before attempting fixes
2. **Isolate the problem**: Narrow down to the smallest reproducible case
3. **Read error messages carefully**: They often contain the solution
4. **Check recent changes**: What changed since it last worked?
5. **Verify assumptions**: Test each assumption individually

## Refactoring Guidelines

1. **Tests first**: Ensure tests exist before refactoring
2. **Small steps**: Make incremental changes, verify each step
3. **One thing at a time**: Don't mix refactoring with feature changes
4. **Preserve behavior**: Refactoring should not change functionality

## Common Pitfalls

- Fixing symptoms instead of root causes
- Over-engineering simple solutions
- Ignoring existing patterns in the codebase
- Making changes without understanding context
- Skipping validation of user inputs at boundaries

## Accumulated Learnings

See [learnings.md](learnings.md) for session-learned insights that supplement these guidelines.
