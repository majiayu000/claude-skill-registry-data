---
name: coding
description: 'General-purpose software engineering assistant: implement features, write functions, scaffold projects, and produce idiomatic code in many languages.'
category: development
aliases:
- programming
- software-engineering
- implement
- write-code
- build-feature
triggers:
- write this code
- implement this
- code this up
- help me code
- build a function
- write a script
- implement this feature
keywords:
- code
- function
- implement
- build
- script
- feature
- programming
- software
- develop
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- build
- code
- coding
- development
- function
- implement
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

# Coding

## Purpose

Help the user write, modify, and reason about code in any language. Focus on idiomatic,
testable, readable code with clear interfaces.

## When to Use

- User asks to implement a feature or function
- User wants help understanding or modifying existing code
- User is starting a new project or module

## When NOT to Use

- The bug is non-obvious (route to `debugging`)
- The user wants a security review (route to `code-review` then `secure-coding`)
- The user wants architectural design (route to `architecture`)

## Capabilities

- Implement features and functions
- Refactor for clarity and idiom
- Write idiomatic code for the chosen language
- Suggest tests for new code
- Document public APIs

## Inputs

- Language / framework
- Desired behavior
- Constraints (performance, style, dependencies)

## Tools

- The language toolchain
- Standard library reference
- Optional: linter, formatter

## Examples

**User:** "Write a Python function to dedupe a list of dicts by 'id'."
**Response:** Idiomatic implementation with type hints, docstring, edge-case handling, and a unit test.

## Safety

- Don't write code that accesses credentials without consent
- Don't write code that performs destructive filesystem operations without confirmation
- Cite sources when borrowing non-trivial patterns

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `debugging` (when something fails)
- `testing` (alongside implementation)
- `code-review` (before merging)
- `architecture` (for larger decisions)

## Workflow

1. Confirm the goal, scope, and constraints.
2. Inspect the available context before acting.
3. Apply the skill-specific guidance in this document.
4. Verify the result and report limitations or next steps.
