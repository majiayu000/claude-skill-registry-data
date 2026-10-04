---
name: stack-detection
description: Detect the language, framework, and tooling stack of a project or set of files to load the right engineering skills.
compatibility: opencode
metadata:
  audience: engineers
  purpose: skill-routing
---
## What I do

Guide the engineer agent in detecting the technology stack of the code being worked on, so the correct language and framework skills are loaded automatically.

## When to use me

Load this skill at the start of any engineering task before loading stack-specific skills. Use it to determine which of the available stack skills to load.

## Detection approach

Detect the stack by examining the files involved in the current task, the project root, and build configuration. Use the most specific signal available.

### Step 1: Check the files being changed

Look at the file extensions and import statements in the files listed in the spec's Changes section:

| Extension / pattern | Stack skill to load |
|---|---|
| `.java` | `java-stack` |
| `.groovy`, `.gradle`, `.gradle.kts` | `groovy-stack` |
| `.go` | `go-stack` |
| `.rs`, `Cargo.toml` | `rust-stack` |
| `.py`, `.pyi` | `python-stack` |
| `.js`, `.mjs`, `.cjs`, `.ts`, `.mts` | `javascript-stack` |
| `.jsx`, `.tsx` | `javascript-stack` + `react-stack` |
| `.swift` | Swift project (mockup renderer hint: `swiftui-mockup-renderer`) |
| `.sql`, migration files | `database-stack` |

### Step 2: Check project root markers

If the files being changed don't make the stack obvious, check the project root:

| Marker | Stack skill |
|---|---|
| `pom.xml`, `build.gradle`, `build.gradle.kts` | `java-stack` (and/or `groovy-stack` for Gradle/Spock) |
| `go.mod` | `go-stack` |
| `Cargo.toml`, `Cargo.lock` | `rust-stack` |
| `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile` | `python-stack` |
| `package.json` | `javascript-stack` |
| `package.json` with react dependency | `javascript-stack` + `react-stack` |
| `tsconfig.json` | `javascript-stack` |
| `Package.swift`, `*.xcodeproj`, `*.xcworkspace` | Swift project (mockup renderer hint: `swiftui-mockup-renderer`) |

### Step 3: Load multiple skills for mixed-stack work

If the task spans multiple stacks (e.g., a Go backend API + React frontend), load all relevant stack skills. There is no conflict — each skill covers its own domain.

## Always load

Regardless of stack detection, always load these skills for any engineering task:
- `implementation-principles`
- `testing-and-validation`

## Available stack skills

- `java-stack` — Java, JVM conventions, Spring, service design
- `groovy-stack` — Groovy, Gradle, DSLs, Spock testing
- `go-stack` — Go packages, concurrency, operational correctness
- `rust-stack` — Rust ownership, error handling, crate design
- `python-stack` — Python project structure, type safety, dependency management, testing
- `javascript-stack` — JavaScript, TypeScript, Node runtime safety
- `react-stack` — React components, state management, accessibility
- `database-stack` — Schema, migrations, queries, rollout safety

## Supplementary skills

Load these when the task involves their domain, regardless of language:
- `api-design-and-contracts` — when API endpoints or contracts are involved
- `integration-boundaries` — when external service integrations are involved
- `performance-optimization` — when performance work is the goal
- `security-review` — when security-sensitive code is being written
