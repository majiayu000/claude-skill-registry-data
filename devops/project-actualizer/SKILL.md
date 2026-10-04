---
name: project-actualizer
description: Методология исследования проектов и создания .claude/ конфигурации
agents:
  - actualizer
user-invocable: false
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


## Use this skill when

- Initializing or updating `.claude/` configuration for a project
- Creating CLAUDE.md, PROJECT.md, rule files, agent definitions, and hooks
- Mapping a project's stack, framework, ORM, and deploy method to configuration artifacts
- Auditing an existing `.claude/` setup for orphan skills, missing agents, or bad rules

## Do not use this skill when

- The task is writing application code — this skill is for configuration generation only
- You need to generate reference documentation for a library — use the `reference-generator` agent

## Purpose

Framework for researching projects and creating `.claude/` configuration. Not a rigid algorithm — a set of principles and decision tables for producing high-quality, project-specific Claude configuration without generic descriptions, invented commands, or orphan skills.

## Capabilities

### Stack Detection

Identify the stack from root artifacts: `package.json` (JavaScript/TypeScript), `pyproject.toml` or `requirements.txt` (Python), `go.mod` (Go), `Cargo.toml` (Rust), `Gemfile` (Ruby), `composer.json` (PHP), `pom.xml` or `build.gradle` (Java), `*.csproj` (C#), `mix.exs` (Elixir), `deno.json` (Deno), `bun.lockb` (Bun).

Identify the framework from `package.json` dependencies: `next` → nextjs-app, `nuxt` → nuxt-app, `@sveltejs/kit` → sveltekit-app, `grammy`/`telegraf` → telegram-bot, `fastify`/`express`/`hono` → web-api, `@nestjs/core` → nestjs-app, `react` (without next) → react-app, `vue` (without nuxt) → vue-app, `electron` → desktop-app, `react-native`/`expo` → mobile-app.

Identify architecture from directory structure: `src/app/entities/features/shared/` → FSD, `src/controllers/models/views/` → MVC, `src/domain/application/infrastructure/` → Clean Architecture/DDD, `src/routes/middleware/handlers/` → Express/Fastify API, `src/commands/events/listeners/` → event-driven, `packages/` or `apps/` at root → Monorepo.

### What to Read

Read 5–7 files mandatory: root stack config (package.json, Cargo.toml, go.mod), compiler config (tsconfig.json, rustfmt.toml), linter/formatter (.eslintrc, .prettierrc, ruff.toml), CI config (.github/workflows/*.yml), Docker files (Dockerfile, docker-compose.yml), README.md or PROJECT.md.

Read 1–2 runtime/deployment files: `.env.example` for ENV schema, `ecosystem.config.js` for PM2, `docker-compose.yml` for services, `Procfile`/`fly.toml`/`vercel.json`/`serverless.yml` for cloud deploy, `.github/workflows/*.yml` for CI/CD.

Read 1–3 database/schema files based on ORM: Prisma → `prisma/schema.prisma`, Django → `*/models.py`, Rails → `db/schema.rb`, TypeORM/Drizzle/MikroORM → `src/**/entities/*.ts` or `src/**/schema.ts`. Also read the last 2–3 migrations for schema evolution context.

Read 2–3 optional files by need: a key source file for code patterns, a test file for framework and patterns.

Never read all files in `src/` — 2–3 representative files are sufficient. Never read lock files (package-lock.json, Cargo.lock), generated code (dist/, build/, .next/), or binary files.

### CLAUDE.md Structure

Mandatory sections in order: `## Stack` (one line of key technologies), `## Commands` (build, test, lint, dev, deploy), `## Rules` (3–7 critical rules as imperative sentences), `## Docs` (links to `.claude/` artifacts).

Optional sections between Commands and Rules: `## Deploy` only if there is a deploy procedure, `## Gotchas` only for non-obvious behaviors (max 3–5), `## Testing` only for project-specific test patterns.

Every line earns its place. No generic descriptions. No README copying.

### Deployment Mapping

Identify deploy method from artifacts: `ecosystem.config.*` → PM2 (`pm2 restart ecosystem.config.cjs`), `docker-compose.yml` → Docker Compose (`docker compose up -d --build`), `Dockerfile` without compose → Docker, `Procfile` → Heroku (`git push heroku main`), `fly.toml` → Fly.io (`fly deploy`), `vercel.json` → Vercel (`vercel --prod`), `serverless.yml` → Serverless Framework, `*.service` → Systemd, nothing → Manual (`node dist/index.js`).

### Environment Extraction

Priority: `.env.example` → parse directly. Then grep code for `process.env.VAR` (Node), `os.environ["VAR"]` (Python), `os.Getenv("VAR")` (Go). Then check docker-compose `environment:` sections.

Output as a table with Variable, Required, and Description columns. Never include secret values — only variable names.

### External Deps Extraction

Sources: docker-compose services (each service except the main app = external dep), ENV variable patterns (`DATABASE_URL`/`PG_*` → PostgreSQL, `REDIS_*` → Redis, `S3_*`/`AWS_*` → S3/AWS, `SMTP_*` → email, `TELEGRAM_*` → Telegram API, `STRIPE_*` → Stripe), package.json deps (`pg`/`@prisma/client` → PostgreSQL, `ioredis`/`redis` → Redis, `@aws-sdk/*` → AWS, `bullmq` → Redis for BullMQ).

### Command Verification

Before writing any command to Commands — verify it exists. For Node.js: read `scripts` from `package.json` and use only those. For Python: read `pyproject.toml` under `[tool.taskipy.tasks]` or `Makefile`. For Go/Rust: read `Makefile` or `Cargo.toml`. Invented commands are a critical error for downstream agents.

### Rules Decision Tree

Evaluate each potential rule: Is it a deterministic check? → use a hook instead. Is it derivable from the code? → don't add. Is it covered by a global skill? → don't add. Is it domain knowledge specific to this project? → STRUCTURE rule. Is it a model constraint? → SCAFFOLD rule with expiry note.

Each rule file has `paths:` frontmatter for scoped loading. Use `alwaysApply: true` only for global project-wide rules.

### Skills Mapping

Map stacks to skills: TypeScript → `typescript-pro`, `typescript-expert`; Python → `python-pro`, `fastapi-pro` (if FastAPI); Go → `golang-pro`; Rust → `rust-pro`; React/Next.js → `frontend-developer`, `react-best-practices`, `react-patterns`; Vue/Nuxt → `vue-developer`; Svelte → `svelte-developer`; NestJS → `nestjs-expert`; Telegram bot → `telegram-bot-builder`; SQL/DB → `postgresql`, `prisma-expert` (if Prisma); Testing → `testing-patterns`; Docker → `docker-expert`; Backend API → `nodejs-backend-patterns`, `api-patterns`; BullMQ/Workers → `bullmq-specialist`; Security → `backend-security-coder`.

Rule: only include skills with concrete value for this specific project. Fewer focused skills beats many generic ones. Every skill copied to `.claude/skills/` must appear in `skills:` of at least one agent — no orphan skills.

### Agents Matrix

Include: `coder` always (maxTurns 30), `reviewer` always (maxTurns 15), `debugger` always (maxTurns 20), `planner` for complex projects with monorepos or more than 50 files (maxTurns 20), `dba` if there is a database (maxTurns 20), `verifier` if there are tests or verify_steps (maxTurns 10), `refiner` for complex projects (maxTurns 10).

Each agent gets a `## Контекст проекта` section with real data: key files and their purpose, architectural patterns, stack and dependency tables, project-specific gotchas.

### Hooks

Only deterministic hooks — lint, typecheck, format. Never AI-based checks in hooks. Filter by file extension to avoid running tsc on .md/.json/.yaml changes. All commands end with `|| true` so hooks don't block the agent on informational errors.

TypeScript hook (PostToolUse, Edit/Write): check changed .ts/.tsx files with `npx tsc --noEmit --pretty 2>&1 | head -50`.

### Settings Merge Protocol

Never overwrite `settings.json` entirely. Always read the existing file first, parse it, preserve existing `permissions`, `allowedTools`, and `hooks`, add new hooks, then write the updated JSON.

### Reference Generation


## Behavioral Traits

- Reads 5–7 files to understand the project, not every file in src/
- Verifies every command against package.json scripts before writing it
- Includes only skills that have concrete value for the specific project
- Ensures every copied skill appears in at least one agent
- Never overwrites settings.json without merging existing content

## Important Constraints

- NEVER invent commands — read them from package.json/Makefile/Cargo.toml
- NEVER overwrite settings.json without merge — this destroys existing permissions
- NEVER include orphan skills — every skill must be assigned to an agent
- NEVER write generic rules like "write clean code" — not enforceable
- NEVER include secret values in Environment tables — variable names only
- NEVER add more than 7 rule files — cognitive overload for agents

## Anti-Patterns

Rule = description ("This project uses React") — Claude sees this in the code. CLAUDE.md = README (copying architecture docs) — Claude reads README itself. Empty context sections ("TODO") — better to omit the section. AI in hooks — expensive and unstable. Overwriting settings.json — destroys existing permissions. Reading all src/ files — 10–15 files are sufficient. Generic rules — not enforceable. Too many rule files (over 7) — cognitive overload.
