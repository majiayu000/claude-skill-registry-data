---
name: get-architecture
description: Analyze the current software project and produce a polished architecture report explaining what the repository does, how it is structured, and how the system works. Use when the user asks to understand a repo, get architecture, explain project structure, onboard to a codebase, summarize system design, identify entrypoints, map data/control flow, or describe build, test, deployment, configuration, persistence, authentication, frontend/backend/API boundaries, services, workers, or integrations across web apps, APIs, CLIs, libraries, monorepos, mobile apps, desktop apps, and infrastructure repositories.
---

# Get Architecture

## Workflow

Inspect the repository before answering. Do not make code changes.

1. Inventory the project:
   - Start with `rg --files` when available.
   - Identify README files, package manifests, lockfiles, build/config files, entrypoints, route definitions, service layers, tests, deployment files, infrastructure files, and source directories.
   - For large repos, focus on files that reveal purpose, runtime, boundaries, and execution flow; state the scope inspected.
2. Determine project purpose:
   - Prefer README content, app metadata, package descriptions, route names, CLI commands, tests, deployment config, and source structure over guesses.
   - Label uncertainty clearly when intent cannot be fully inferred.
3. Identify the technology stack:
   - Detect languages, frameworks, runtimes, package managers, build systems, test tools, databases/storage, external services, auth providers, queues, infrastructure, and deployment targets from concrete files.
4. Map architecture:
   - Explain top-level directory structure.
   - Identify main application entrypoints and run/build/test commands.
   - Explain core modules, services, components, and responsibilities.
   - Describe frontend/backend/API boundaries when present.
   - Trace data flow from user input or external events through routing, business logic, persistence/integrations, and response/output.
   - Trace control flow through startup, request handling, jobs, CLIs, or event handlers.
   - Note dependency relationships between important modules.
   - Explain configuration, environment variables, secrets handling, and runtime settings.
   - Describe persistence/database/storage layer and migrations/schema definitions.
   - Describe authentication and authorization if present.
   - Describe background jobs, workers, queues, scheduled tasks, or async processing if present.
   - Explain testing strategy and build/deployment/runtime flow.
5. Ground claims in evidence:
   - Cite relevant file paths and line numbers whenever possible.
   - Use the host app's clickable local file-link format when available; otherwise use `path:line`.
   - Prefer concrete wording such as "The app appears to..." when evidence is incomplete.
   - Avoid inventing external integrations, databases, deployment targets, or architectural patterns not supported by the repository.

## Investigation Hints

Prioritize these file types and locations:

- Purpose and usage: `README*`, docs, examples, package descriptions, CLI help text.
- Manifests and package managers: `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `pyproject.toml`, `requirements*.txt`, `Pipfile`, `poetry.lock`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `.csproj`, `Gemfile`, `composer.json`.
- Entrypoints and routes: framework boot files, `src/main*`, `src/index*`, `app/*`, `pages/*`, `routes/*`, `api/*`, `server*`, `cmd/*`, CLI command definitions.
- Configuration: `.env*` examples, config directories, framework config, build config, Docker/Compose files, Kubernetes manifests, Terraform, CI workflows.
- Domain and service layers: controllers, handlers, services, repositories, models, schemas, stores, jobs, workers.
- Persistence: migrations, schema files, ORM config, database clients, storage adapters.
- Tests: unit, integration, e2e, fixture, and test utility files.

Use non-mutating inspection commands. Do not install dependencies, update lockfiles, run migrations, or start services unless the user explicitly asks.

## Final Report Format

Always use this exact heading structure in the final response. Keep a section even when nothing is detected; write "Not evident from the inspected files" or a concise uncertainty note.

# Project Overview

Explain what the project appears to do in plain English.

# Architecture Summary

Give a detailed explanation of the overall architecture.
This should also include an in-depth architecture map.

# Technology Stack

List the detected languages, frameworks, libraries, runtimes, package managers, databases, infrastructure tools, and testing tools.

# Repository Structure

Explain the important top-level folders and files, including what each one is responsible for.

# Main Entry Points

Identify the files or commands where the app starts, builds, runs, or exposes APIs.

# Core Components

Break down the major modules/components/services and explain their responsibilities.

# Data Flow

Explain how data moves through the system, including user input, API calls, business logic, persistence, and responses.

# External Integrations

Describe third-party APIs, services, SDKs, databases, queues, auth providers, or cloud services used by the project.

# Configuration and Environment

Explain how configuration is handled, including env files, config modules, secrets, build settings, and runtime settings.

# Build, Test, and Deployment

Explain how the project is built, tested, run locally, and deployed, based on scripts and config files.

# Notable Patterns and Design Decisions

Identify architectural patterns such as MVC, layered architecture, clean architecture, microservices, monorepo, plugin architecture, event-driven design, serverless, or infrastructure-as-code.

# Risks, Gaps, or Open Questions

List anything unclear, missing, risky, or worth investigating further.

# Suggested Next Files to Read

Recommend the most useful files for a developer to read next to understand the project quickly.
