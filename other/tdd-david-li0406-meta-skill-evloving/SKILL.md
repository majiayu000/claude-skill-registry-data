---
name: tdd
description: TDD methodology guidance for writing tests and implementing code. Use when writing tests, implementing features, or refactoring code.
---

# TDD Methodology

## Red-Green-Refactor Cycle

### Red Phase (Write Failing Test)

- Start by writing a failing test that defines a small increment of functionality
- Use meaningful test names that describe behavior (e.g., "shouldSumTwoPositiveNumbers")
- Make test failures clear and informative
- Write the simplest failing test first

### Green Phase (Make It Pass)

- Write just enough code to make the test pass - no more
- Use the simplest solution that could possibly work
- Do not add extra features or edge case handling yet

### Refactor Phase (Improve Structure)

- Refactor only when tests are passing
- Use established refactoring patterns with their proper names
- Make one refactoring change at a time
- Run tests after each refactoring step
- Prioritize refactorings that remove duplication or improve clarity

## Tidy First Approach

Separate all changes into two distinct types:

| Type       | Description                                | Examples                                  |
| ---------- | ------------------------------------------ | ----------------------------------------- |
| STRUCTURAL | Rearranging code without changing behavior | Renaming, extracting methods, moving code |
| BEHAVIORAL | Adding or modifying actual functionality   | New features, bug fixes                   |

Rules:

- Never mix structural and behavioral changes in the same commit
- Always make structural changes first when both are needed
- Validate structural changes do not alter behavior by running tests before and after

## Code Quality Standards

- Eliminate duplication ruthlessly
- Express intent clearly through naming and structure
- Make dependencies explicit
- Keep methods small and focused on a single responsibility
- Minimize state and side effects

## Defect Fixing Workflow

When fixing a defect:

1. First write an API-level failing test
2. Then write the smallest possible test that replicates the problem
3. Get both tests to pass

## Feature Implementation Workflow

1. Write a simple failing test for a small part of the feature
2. Implement the bare minimum to make it pass
3. Run tests to confirm they pass (Green)
4. Make any necessary structural changes (Tidy First)
5. Commit structural changes separately (use `git-commit` skill)
6. Add another test for the next small increment
7. Repeat until feature is complete

Always write one test at a time, make it run, then improve structure. Run all tests (except long-running tests) each time.
