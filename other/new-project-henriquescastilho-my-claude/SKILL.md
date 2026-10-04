---
name: new-project
description: Bootstrap a new project from PRD or idea. Creates folder structure, CLAUDE.md, initial implementation with security best practices. Use when starting any new project.
disable-model-invocation: true
allowed-tools: Read Write Edit Bash Grep Glob
---

# New Project Bootstrap

You are setting up a new DME Technology project from scratch.

## Step 1 — Understand the Input

Read `$ARGUMENTS` as either:
- A PRD file path → read it
- A project description → use it directly
- If empty, ask Henrique what the project is

Extract:
- **What** it does (core features)
- **Who** uses it (target user)
- **How** it deploys (web/mobile/API/CLI)
- **Tech constraints** (if any specified)

## Step 2 — Architecture Decision

Based on the requirements, choose the simplest viable stack:

| Type | Default Stack |
|------|---------------|
| Web app (SaaS) | Next.js + Supabase + Tailwind + shadcn/ui |
| API/Backend | Node.js + Express/Fastify + Postgres OR Python + FastAPI + Postgres |
| Mobile | Swift (iOS) or Flutter (cross-platform) |
| CLI tool | Python or Node.js |
| AI/ML | Python + FastAPI |

Present the stack choice with a 1-paragraph rationale. Wait for approval.

## Step 3 — Scaffold

After approval:

1. Initialize the project with the chosen framework's CLI
2. Create `.claude/` directory with project CLAUDE.md:

```markdown
# [Project Name]

## Stack
- Language: [X]
- Framework: [X]
- Database: [X]
- Deploy target: [Railway/Vercel/GCP]

## Architecture
[Brief description of the system]

## Conventions
- [Naming conventions detected or chosen]
- [File structure pattern]
- [Test framework]

## Security Requirements
- Authentication: [method]
- Authorization: [method]
- Data protection: [approach]

## Environment Variables
| Variable | Purpose | Where to set |
|----------|---------|-------------|
| DATABASE_URL | DB connection | .env / deploy platform |

## Commands
- Dev: `[command]`
- Build: `[command]`
- Test: `[command]`
- Lint: `[command]`
- Deploy: `[command]`
```

3. Set up the security foundations:
   - Auth system configured
   - Input validation library installed (Zod/Pydantic)
   - Security headers middleware
   - Rate limiting middleware
   - Environment variable management (.env + .env.example)
   - .gitignore with secrets excluded

4. Create the initial implementation (MVP core features)

5. Run full validation: lint + type-check + build

6. Initialize git, create initial commit

## Step 4 — Report

Show Henrique:
- What was created (file tree)
- How to run it locally
- What's the next step
- Any decisions he needs to make
