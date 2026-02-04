---
name: tech-stack-analyzer
description: Delegates tech stack detection to a lightweight agent. Use when you need to know the project's language, frameworks, or dependencies without loading manifest files into context.
---

# Tech Stack Analyzer Skill

This skill delegates tech stack detection to a specialized lightweight agent, keeping your context lean.

## When to Invoke This Skill

Invoke this skill when ANY of these conditions are true:

1. **Need to know the tech stack**: You need to identify the project's language, framework, or dependencies
2. **Framework-specific decisions**: You need to choose patterns or libraries based on what the project uses
3. **Test framework identification**: You need to know what testing framework is configured
4. **Build tool detection**: You need to know how to build, run, or test the project
5. **Dependency analysis**: You need to check what packages/libraries are already installed

## Why Use This Skill?

**Without this skill**: You would read package.json, go.mod, requirements.txt, etc. directly, loading hundreds of lines of dependencies into your context.

**With this skill**: The tech-stack-analyzer agent (haiku model) reads manifests and returns a concise 30-50 line summary.

**Context savings**: 70-90% reduction in manifest-related context usage.

## Invocation

When you need tech stack information, invoke the agent:

```
Task(subagent_type="tech-stack-analyzer", prompt="
Analyze this project's tech stack.
")
```

For specific focus areas:

```
Task(subagent_type="tech-stack-analyzer", prompt="
Analyze this project's tech stack.
Focus on: testing framework and test utilities
")
```

## What tech-stack-analyzer Will Do

The agent will:

1. **Find manifests**: Locate package.json, go.mod, requirements.txt, Cargo.toml, etc.
2. **Read selectively**: Read only first 50-100 lines of each manifest
3. **Extract key info**: Language, runtime, frameworks, test tools, build tools
4. **Detect patterns**: Monorepo, microservices, serverless structures
5. **Return summary**: Concise structured output with versions and key dependencies

## Expected Output

You will receive a structured summary like:

```
## Tech Stack Summary

**Language**: TypeScript 5.3
**Runtime**: Node.js 20.x

**Frameworks**:
- Web: Express 4.18
- UI: React 18.2

**Testing**:
- Framework: Jest 29
- Utilities: React Testing Library

**Build**:
- Bundler: Vite 5.0
- Task Runner: npm scripts

**Key Dependencies**:
- Database: PostgreSQL (pg driver)
- ORM: Prisma 5.7
```

## Example Usage

**Scenario**: You need to write a new service and want to match existing patterns.

**Without skill**: Read package.json (200+ lines), tsconfig.json, check for frameworks manually.

**With skill**:
```
Task(subagent_type="tech-stack-analyzer", prompt="Analyze this project's tech stack.")
```

**Result**: You know it's Express + TypeScript + Prisma in 30 lines of context.

## Do NOT Invoke When

- You already know the tech stack from earlier in the conversation
- The user has explicitly told you the tech stack
- You only need to check a single specific file (use Read directly)
- The project has no manifest files (empty/new project)

## Consumers

This skill is particularly useful for:
- `init-explorer` - Initial project understanding
- `architecture-evaluator` - Making architectural decisions
- `test-creator` - Matching test framework conventions
- `coder` - Following project patterns
