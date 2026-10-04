---
name: greenfield-scaffolding
description: Bootstrap a new project's Hero workspace with stack-appropriate conventions, decisions, and initial specs.
compatibility: opencode
metadata:
  audience: any-agent
  purpose: project-onboarding
---
## What I do

After `hero init` on a new project, generate starter knowledge entries
tailored to the detected tech stack. This gives a fresh workspace immediate
value instead of being an empty folder.

## When to use me

- After `hero init` on a new project
- When `/scan` detects a stack but no conventions exist yet
- When the user says "set up hero for this project" or "onboard this codebase"

## Steps

1. Run `hero scan` to detect the tech stack (languages, frameworks, build tools)
2. Based on the detected stack, generate:

   **Conventions** (write to `.hero/knowledge/conventions/`):
   - Error handling patterns for the detected language
   - Testing conventions (test location, naming, runner)
   - API design patterns (if web framework detected)
   - Git workflow (branch naming, commit message format)

   **Decisions** (write to `.hero/knowledge/decisions/`):
   - Why this tech stack was chosen (ask the user or note "pre-existing")
   - Package manager choice
   - Build tool rationale

   **Initial specs** (write to `.hero/planning/features/`):
   - A "project health" spec covering CI, linting, test coverage targets
   - A "documentation" spec if README is thin

3. Run `hero index` to make everything searchable
4. Run `hero install project . --target <detected-tool>` to wire up MCP

## Stack-specific templates

| Stack | Conventions generated |
|---|---|
| Go | error wrapping, table-driven tests, package naming |
| TypeScript/Node | ESM imports, async/await patterns, type strictness |
| Python | virtual env, type hints, pytest conventions |
| Java/Kotlin | package structure, dependency injection, Gradle/Maven |
| Rust | error handling (thiserror/anyhow), module structure |
| React | component patterns, state management, testing-library |

## What not to do

- Don't generate conventions that contradict existing code patterns
- Don't assume a framework — detect it first
- Don't overwrite existing conventions or decisions
- Keep generated content concise — starter quality, not comprehensive
