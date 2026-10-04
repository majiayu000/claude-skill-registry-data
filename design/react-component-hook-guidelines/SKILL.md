---
name: react-component-hook-guidelines
description: Use when reviewing, refactoring, or implementing React components and custom Hooks with unclear boundaries or oversized props.
---

# React Component Hook Guidelines

## Overview

Guide the splitting, refactoring, and review of React page components, business components, presentation components, custom Hooks, and utility functions. Focus on responsibility boundaries, props width, state flow, branching, page orchestration, and coupling between UI and logic. Use this skill to decide whether logic belongs in a page, a Hook, a presentation component, or `lib/utils`.

## When to Use

Use this skill when the user asks to:
- Split a component or Hook
- Refactor a component, page, or Hook that feels too large or too heavy
- Review React code structure, component design, or Hook design
- Reduce prop width, state fan-out, or branch complexity
- Reorganize frontend layering or page orchestration
- Separate UI from logic, requests, routing, caching, modals, or analytics
- Extract business Hooks, presentation components, or pure utility functions

## Do not use

Do not use this skill for:
- Tasks unrelated to React components, Hooks, or page orchestration
- Pure backend work
- Simple style-only changes that do not involve boundaries, state flow, or props design

## Instructions

1. Identify the task type first: code review, refactor, new implementation, or layer or structure cleanup.
2. Locate the core unit: page component, business component, presentation component, custom Hook, or utility function.
3. Check whether the change has a single reason, then look for accidental coupling between props, state, effects, routing, caching, modals, and analytics.
4. Prefer boundary splits to reduce complexity. Do not use line count as a substitute for design judgment.

## Quick Decisions

- When you need to decide whether a component or Hook should be split, read [references/react-component-hook-rules.md](references/react-component-hook-rules.md).
- When reviewing existing React code, check in this order: responsibility boundary -> props design -> complexity -> branch expansion.
- When landing a refactor, extract business Hooks, presentation components, and pure functions first. Do not start with cosmetic style moves.
- When implementing a new component, decide first whether it is page orchestration, a business container, a presentation component, or a reusable UI component.

## Execution Rules

### Review

Check at least these questions:

- Does the file export only one main component or main Hook?
- Does it pass a page-level large state object or a full actions bundle directly to children?
- Does it couple UI, requests, routing, effects, caching, modals, or analytics?
- Does it contain more than 3 pattern branches and fit a mapping or strategy better?
- Is there logic that should be extracted into a Hook or `lib/utils`?

### Refactor

Prefer this split path:

1. Remove business state and side effects from the page component.
2. Extract reusable or testable state flow into a business Hook.
3. Split heavy JSX blocks into the smallest presentation components.
4. Move pure data transforms, validation, and mapping into `lib/` or `utils/`.
5. Narrow props to only the fields and callbacks the child truly needs.

### New Implementation

Before implementing, make these three decisions:

1. Is this an orchestration layer or a presentation layer?
2. Should the state logic move into a Hook?
3. Does this logic still make sense outside the React lifecycle? If yes, move it to `lib/utils`.

Additional hard rules:

- Code comments must be written in Chinese.
- Functions must have a function comment before the definition that explains the responsibility and the scenarios it handles.
- Hooks must have a function comment before the definition that explains the business responsibility, state scope, or side-effect boundary.
- Comments should explain responsibility, boundaries, and intent only. Do not write low-value line-by-line translation comments.

## Output Requirements

- If this is a review, list "issues found" first, then the proposed changes.
- If this is a refactor, clearly state the new boundaries: what stays in the page, what moves into Hooks, what moves into presentation components, and what moves into utility functions.
- If this is an implementation, keep code outputs aligned with the reference style, do not reintroduce "large object props" or "universal Hooks", and add function comments for any new or modified functions and Hooks.

## Exception Handling

Reasonable exceptions are allowed, but they must be explained. Common acceptable exceptions:

- A presentation component is a little long, but its visual structure is concentrated and stable.
- A file contains a few helper components that only serve the main component.
- A page entry file is a little long, but the business logic has already been extracted into Hooks.

If you cannot give a clear reason, default to tightening the boundary.
