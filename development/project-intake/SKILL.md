---
id: core.project-intake
name: Project Intake
description: >
  Collects the minimum repository context needed before an agent changes Angular, TypeScript, JavaScript, testing, architecture, or quality code.
stack:
  - Angular
  - TypeScript
  - JavaScript
category: core
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - project intake
  - inspect repository
  - understand project
  - repo context
  - before coding
---

# Project Intake

## Purpose

Use this skill to understand the project before selecting specialized skills or editing code. The goal is to gather enough context to act safely without creating a long discovery phase.

## When to Use

Use this skill when:

- Starting work in an unfamiliar repository.
- The framework, tooling, or architecture is unclear.
- The task may depend on Angular, TypeScript, RxJS, Node, package manager, tests, or linting.
- The user asks for a refactor, migration, performance improvement, or architecture change.
- The repo may be an app, library, monorepo, microfrontend, package, or design system.

## When Not to Use

Do not use this skill when:

- The user provides all relevant context and the change is trivial.
- The task only edits documentation unrelated to project structure.
- A previous intake in the same turn already established the required facts.

## Inputs Required

Inspect these files when present:

```txt
package.json
angular.json
nx.json
workspace.json
tsconfig.json
tsconfig.base.json
eslint.config.js
.eslintrc.json
jest.config.ts
vitest.config.ts
karma.conf.js
package-lock.json
pnpm-lock.yaml
yarn.lock
README.md
AGENTS.md
```

Identify:

```txt
project type: app, library, monorepo, microfrontend, package, design system
frameworks: Angular, TypeScript, JavaScript, Node, RxJS
tooling: package manager, build system, test runner, linting
architecture: standalone, NgModules, mixed, feature libraries
state model: RxJS, Signals, NgRx, ComponentStore, custom service state
quality gates: tests, lint, formatting, coverage, CI
agent assets: agents/ngautopilot/subagents if present
```

## Version Compatibility

This skill does not decide API compatibility. It gathers inputs for `core.stack-version-detection` and `core.compatibility-router`.

When versions are not obvious, report uncertainty instead of guessing.

## Decision Rules

Collect only what the task needs:

```txt
performance task -> Angular version, templates, build, affected component, measurement tools
architecture task -> folder structure, component/service responsibilities, state model
testing task -> test runner, existing test style, mocks, coverage expectations
migration task -> current versions, target versions, lockfile, deprecated APIs
quality task -> lint config, TypeScript config, existing conventions
dependency injection task -> Angular version, provider locations, service lifetime, tests, bootstrap style
```

Prefer repository evidence over assumptions.

## Execution Workflow

Use this workflow:

```txt
1. Check git status and project root.
2. Read package and workspace metadata.
3. Detect project type and tooling.
4. Inspect only relevant source areas.
5. Summarize active constraints.
6. Hand off to version detection or skill routing.
```

## Do

Recommended intake pattern:

```txt
Read the smallest set of files that can answer what this project is, how it is built, how it is tested, and which conventions must be preserved.
```

## Do Not

Avoid repository-wide exploration without a reason:

```txt
Read every source file before changing one component.
```

Avoid assuming a monorepo layout means Nx without checking files.

Avoid assuming a package manager when multiple lockfiles exist; report the conflict.

## Output Format

Use this format:

```md
## Project Intake

- Project type:
- Frameworks:
- Package manager:
- Build system:
- Testing:
- Linting:
- Architecture style:
- State model:
- Relevant constraints:
```

## Review Checklist

- [ ] The project root is identified.
- [ ] Package manager evidence is checked.
- [ ] Framework and tooling files are inspected.
- [ ] Relevant project instructions are considered.
- [ ] Unknowns are explicitly stated.
- [ ] Intake remains proportional to the task.

## Risks

- Too little intake can select the wrong skill.
- Too much intake can delay simple tasks.
- Conflicting lockfiles or configs can mislead command selection.
- Ignoring local instructions can violate project conventions.

## Examples

```txt
Task: Add a Jest unit test.
Intake focus: package.json, jest config, existing nearby specs.
```

```txt
Task: Refactor Angular state.
Intake focus: Angular version, state libraries, affected feature folders, existing service/facade patterns.
```

## Expected Output

1. Identify the minimum project context needed.
2. Report project type, tooling, and relevant constraints.
3. Avoid unsupported assumptions.
4. Pass clear inputs to routing and compatibility skills.
5. Keep discovery proportional to risk.
