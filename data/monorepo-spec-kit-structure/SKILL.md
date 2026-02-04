---
name: monorepo-spec-kit-structure
description: >
  Standard project layout and Spec-Kit usage patterns for AI-driven,
  spec-driven monorepos that host frontend, backend, and specs in a
  single repository.
---

# Monorepo + Spec-Kit Structure Skill

## When to use this Skill

Use this Skill whenever you are:

- Creating or modifying a **monorepo** that contains:
  - One or more frontends (e.g. Next.js).
  - One or more backends (e.g. FastAPI, Node, Go).
  - A shared **specs** folder managed by Spec-Kit or similar tools.
- Setting up the initial folder structure for an AI‑driven project that
  will be edited by tools like Claude Code + Spec-Kit.
- Deciding where to put `CLAUDE.md` files, specs, and configuration
  files so AI agents always see the right context. [file:10][web:11][web:24]

This Skill must work for any AI‑driven monorepo, not just a single hackathon.

## Core goals

- Keep **code and specs** together in a single monorepo, but clearly
  separated by responsibility:
  - `/specs` for requirements and architecture.
  - `/frontend` for UI/web clients.
  - `/backend` for APIs, agents, MCP servers, etc.
  - Optional `/infra` or `/deploy` folders for Kubernetes, Dapr, CI/CD.
- Make it easy for AI tools to:
  - Find the right specs.
  - Understand project layout.
  - Apply changes in the correct layer without confusion. [file:10][web:11]

## Recommended top-level layout

A typical spec-driven monorepo should follow a structure like:

- `/.spec-kit/` – Spec-Kit configuration and internal files.
- `/specs/` – Human-readable specs:
  - `overview.md` – project summary and current phase.
  - `architecture.md` – high-level system architecture.
  - `features/` – feature specs (e.g. `task-crud.md`, `authentication.md`).
  - `api/` – API endpoint and protocol specs.
  - `database/` – schema and model specs.
  - `ui/` – UI and UX specs (components, pages, flows).
  - `infra/` (optional) – deployment, K8s, Dapr, Kafka specs. [file:10][web:11]

- `/frontend/` – Frontend application(s), each with:
  - Its own `CLAUDE.md` for frontend-specific rules.
  - Standard framework layout (e.g. Next.js App Router).

- `/backend/` – Backend application(s), each with:
  - Its own `CLAUDE.md` for backend-specific rules.
  - Clear subfolders for models, routes, agents, MCP tools, etc.

- Root level:
  - `CLAUDE.md` – global instructions and navigation.
  - `.spec-kit/config.yaml` – Spec-Kit configuration for this repo.
  - `README.md` – human entrypoint. [file:10][web:11][web:24]

Exact names may vary, but the pattern should remain.

## Spec-Kit configuration principles

- The `.spec-kit/config.yaml` file should:

  - Declare the main specs directory (e.g. `specs`).
  - Define subdirectories for features, API, database, UI, and infra.
  - Optionally define **phases** or **feature groups** mapping to
    high-level milestones. [file:10][web:11]

- Example conceptual structure:

  - `structure.specs_dir = "specs"`
  - `structure.features_dir = "specs/features"`
  - `structure.api_dir = "specs/api"`
  - `structure.database_dir = "specs/database"`
  - `structure.ui_dir = "specs/ui"`

- The configuration must stay **in sync** with the actual folder layout:
  - If a folder is renamed or moved, update `.spec-kit/config.yaml`.
  - Avoid “orphaned” specs that are not referenced anywhere.

## CLAUDE.md layering

- Use multiple `CLAUDE.md` files with clear scopes:

  - **Root `CLAUDE.md`**:
    - Explain the overall project, monorepo layout, and Spec-Kit
      directory structure.
    - Describe how to reference specs (e.g. `@specs/features/task-crud.md`).
    - Provide high-level development workflow (spec → impl → tests). [file:10][web:11]

  - **Frontend `frontend/CLAUDE.md`**:
    - Frontend-specific stack (Next.js, TypeScript, Tailwind, etc.).
    - Rules for components, pages, routing, styling, API usage.

  - **Backend `backend/CLAUDE.md`**:
    - Backend stack (FastAPI, SQLModel, Agents SDK, MCP SDK, etc.).
    - Rules for routes, models, services, tools, and tests.

- CLAUDE.md files must not conflict:
  - Root file sets global rules.
  - Subfolder files add details for that layer without overriding
    fundamental principles (spec-driven, monorepo layout, etc.).

## Spec usage rules

- All significant changes must start from specs:

  - Add or update specs under `/specs` before changing code.
  - Reference specs explicitly in prompts (e.g. `@specs/features/task-crud.md`). [file:10][web:11][web:24]

- Specs should be **structured**, not free-form essays:

  - Include:
    - Context and goals.
    - User stories or scenarios.
    - Functional and non-functional requirements.
    - Acceptance criteria and test ideas.

- When specs change, code must be updated to match, not vice versa.

## Monorepo coding and navigation rules

- Frontend and backend code should not be mixed in the same folders.
- Cross-cutting concerns (types, contracts, shared models) should live
  in explicit shared modules, not hidden imports.
- Tools and agents (e.g. MCP servers, AI agents) should be placed where:

  - Their code is close to the services they interact with.
  - Related specs are easy to find (e.g. under `specs/api` or `specs/agents`). [file:10]

## Things to avoid

- Creating many small repos instead of a single monorepo when frontend,
  backend, and specs are tightly coupled.
- Hiding specs in random folders or mixing them with code files.
- Putting all instructions in a single, giant CLAUDE.md file without
  layer-specific guidance.
- Letting specs, `.spec-kit/config.yaml`, and actual folders drift out
  of sync. [web:11][web:24]

## References inside the repo

When present, this Skill should align with:

- `/.spec-kit/config.yaml` – Spec-Kit configuration.
- `/specs/...` – all specifications, organized by type.
- `/frontend/...` – frontend apps and their CLAUDE instructions.
- `/backend/...` – backend apps and their CLAUDE instructions.
- Root `CLAUDE.md` and `README.md` – primary navigation and workflow docs.

If these are missing, propose creating them following this structure
instead of inventing a new, ad-hoc monorepo layout.
