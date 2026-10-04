---
name: tdd
description: Test-Driven Development discipline — red/green/refactor cycles for designing code from tests outward.
category: development
aliases:
- test-driven
- red-green-refactor
triggers:
- let's do TDD
- test first
- red green refactor
- write the test first
keywords:
- tdd
- test-driven
- red
- green
- refactor
- cycle
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- development
- green
- red
- tdd
- test-driven
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: write
credential_access: false
destructive_operations: false
---

# TDD (Test-Driven Development)

## Purpose

Apply TDD discipline: write a failing test first, make it pass with the simplest code, then
refactor. Use TDD when it improves design feedback, not as religion.

## When to Use

- Designing a new module or function
- Fixing a bug (write the failing test first)
- The interface is unclear and tests can drive it

## When NOT to Use

- Pure exploration / spike work
- UI / visual work without clear assertions
- Code with no testable seams

## Capabilities

- Drive implementation with failing tests
- Refactor with confidence
- Build tests that document intent

## Inputs

- The behavior to design or fix
- Test framework

## Workflow

1. **Red.** Write the smallest failing test that captures the desired behavior.
2. **Green.** Make it pass with the simplest code, even if naive.
3. **Refactor.** Improve structure while keeping tests green.
4. **Repeat.**

## Safety

- Don't write tests for code that already exists just to "have tests"
- Don't over-mock — design for testability first

## Source

Custom skill, written for this library. Based on Beck's TDD.

## Notes

Subset of `testing`. Use it specifically when you want red/green/refactor discipline.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "let's do TDD"; "test first"; "red green refactor".
