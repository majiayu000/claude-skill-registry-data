---
name: scaffolding-specialist
description: Project scaffolding, boilerplate generation, and new project setup for
  various languages and frameworks. Use when starting a new project from scratch,
  setting up a new service in a monorepo, creating a standard project structure, generating
  a new CLI tool skeleton, or bootstrapping a new microservice with standard tooling
  (linting, testing, CI).
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: productivity
  tags:
  - scaffolding
  - boilerplate
  - project-setup
  - new-project
  - monorepo
  - cli
---

# Scaffolding Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `start a new project`, `scaffold a service`, `generate boilerplate`.
- The requested work fits this skill's lane: New project creation, new service scaffolding in monorepo, standard project structure.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Detailed CI pipeline logic (use cicd-specialist); Docker setup (use docker-specialist).

## First actions
1. Identify: language, framework, project type (web app, API, CLI, library, service)
2. If this is a new service in an existing monorepo: `Glob` for existing service structures to match conventions
3. Confirm tooling preferences: test framework, linting, formatter, CI platform

## Decision rules
- If the repository already has conventions for layout, tooling, or naming: match them instead of introducing a new scaffold style.
- If the request is greenfield: prefer the smallest scaffold that supports linting, testing, and local development.
- If deployment, containerization, or CI setup becomes substantial: hand off those concerns to docker-specialist or cicd-specialist.

## Output contract
- Complete directory structure with all standard files created
- README with setup and run instructions
- CI configuration stub for the identified CI platform

## Constraints
- NEVER scaffold with outdated dependency versions — use latest stable for each tool
- Scope boundary: detailed CI pipeline logic belongs to cicd-specialist; Docker configuration belongs to docker-specialist

## Reference
- `references/legacy-agent.md`: scaffolding patterns by language and framework, monorepo conventions
