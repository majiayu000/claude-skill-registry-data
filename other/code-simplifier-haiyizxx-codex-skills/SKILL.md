---
name: code-simplifier
description: Simplify and refine code for clarity, consistency, modularity, functional-style data flow, and maintainability without changing behavior. Use when the user asks to simplify, clean up, make code more elegant, reduce complexity, improve readability, refactor modules one by one, reduce side effects, or run a final polish pass on touched files.
---

# Code Simplifier

## Core Contract

Preserve behavior exactly. Change structure, names, and local organization only when the result is easier to read, easier to maintain, or more consistent with the project.

Default scope is the current diff, recently touched files, or the files the user named. Do not broaden into unrelated refactors unless the user explicitly asks.

If the user asks for review only, report simplification opportunities without editing. If the user asks for a fix or cleanup, implement the smallest safe change and verify it.

Prefer the user's clean-code defaults: simple structure, explicit data flow, low side effects, and functional-style helpers where they make the code easier to read. Preserve public APIs by default unless the user explicitly allows breaking callers.

## Workflow

1. Inspect the real code and the current diff before editing.
2. Read applicable local rules first: `AGENTS.md`, `CLAUDE.md`, formatter/linter configs, tests, and nearby code style.
3. State assumptions and success checks for non-trivial changes.
4. Identify simplification opportunities that are directly tied to the requested scope.
5. For review work, rank findings by payoff and risk with exact file/line references. Prefer checking one module at a time when the repo is broad.
6. Edit surgically, preserving public APIs, side effects, errors, return values, data shapes, timing, and test expectations.
7. Run the narrowest meaningful verification: targeted tests, type checks, lint, formatting, or a diff review when tests are not practical.
8. Summarize what changed and what was verified.

## User Refactoring Preferences

- Prefer pure functions or private helpers for deterministic transforms: parse, validate, project, filter, aggregate, convert, and format.
- Keep mutation and I/O at clear boundaries. Make state changes obvious by isolating them in small methods.
- Use small dataclasses or typed result objects when a repeated tuple/dict carries a real domain concept.
- Use classes only when they clarify ownership of state, lifecycle, or an external resource. Do not wrap stateless helpers in classes just for abstraction.
- Split long functions into named stages when each stage has a clear input/output and can be tested or reviewed independently.
- Check standard-library, dependency, and existing repo helpers before writing custom utility code. Avoid rebuilding common parsing, geometry, tensor, routing, serialization, or validation behavior.
- Keep module surfaces boring: public entry points stay small; implementation details move behind private helpers or private modules only when that improves navigation.

## Simplification Rules

Prefer:

- Flatter control flow with guard clauses when it reduces nesting.
- Explicit names that make data flow and intent obvious.
- Small helper extraction only when it removes real duplication or isolates a clear concept.
- Functional-style pipelines where intermediate values are named and side effects are delayed or isolated.
- Straightforward conditionals over nested ternaries or dense one-liners.
- Existing project patterns over new abstractions.
- Existing libraries and local utilities over hand-rolled replacements, when the dependency is already available and behavior matches.
- Removing comments that only repeat the code, while keeping comments that explain non-obvious constraints.
- Deleting imports, variables, and helpers made unused by your own edits.

Avoid:

- Changing behavior to make code prettier.
- Combining unrelated concerns into one function.
- Replacing clear code with clever or overly compact code.
- Adding configurability, generality, or framework changes that were not requested.
- Introducing abstraction layers before there are clear repeated concepts or state boundaries.
- Moving code into private modules just to reduce file length when local helper extraction would be clearer.
- Reformatting unrelated sections.
- Deleting pre-existing dead code unless the user asked for cleanup of that code.

## Project Standards

Apply repository-specific standards over generic preferences. If local guidance conflicts with a generic simplification idea, follow the local guidance unless it would be incorrect for the task.

When a project has no explicit rule, match nearby code. Keep naming, module layout, import style, error handling, component patterns, and test style consistent with the surrounding codebase.

## Verification

A simplification is complete only when there is evidence that behavior was preserved. Prefer an executable check that covers the touched code. If no good check exists, inspect the diff carefully and say which verification was not run.

When tests fail for reasons outside the touched scope, report the failing command and the relevant failure instead of hiding it or broadening the change.
