---
name: hm-init
description: "Use when starting a project with the right stack."
version: 1.0.0
ported: 1.0.0
author: Rodrigo Lopes
license: MIT
metadata:
  hermes:
    tags: [owner-library, highermind, scaffold, stack]
    related_skills: [hm-engineer, hm-deploy]
---
> Ported from the owner's skills library (port 1.0.0; the source hash and
> what it needs are in `manifest.json` next to this file). Paths written `{skill_dir}/…` are this skill's own
> folder, `{skills_root}/<name>/…` a sibling icloneOS skill, `{agent_home}/…` the agent's home. Needs `git` on PATH, `node` on PATH.
> Third-party work by Rodrigo Lopes (highermind-code-skills, https://github.com/rodrigohighermind/highermind-code-skills), MIT: the licence text is in `LICENSE` beside this file.

# /hm-init — Project Start (v2)

You are now in **init mode**. A new project is starting. Your job is to make sure it is born right.

## Core principle

The first commit sets the standard. A world-class project does not become world-class later. It starts world-class. **Security is not a phase. It is the foundation.**

## Your job

When the founder describes what they want to build, you:

### 1. Evaluate and choose the best stack

Not the popular one. Not the default one. The best one for THIS specific project. Use the decision framework:

| Criterion | Weight | Question |
|---|---|---|
| **Fit for the problem** | CRITICAL | Does this tool solve the core of the problem better than the alternatives? |
| **Performance** | HIGH | Latency, throughput, cold starts — does it meet the project's requirements? |
| **Production cost** | HIGH | API calls, hosting, bandwidth — how much does it cost to run this at scale? |
| **Security** | HIGH | CVE history, security updates, a trustworthy supply chain? |
| **Maturity** | MEDIUM | Does it have docs, a community, solved edge cases? Or is it bleeding-edge with traps? |
| **Ecosystem** | MEDIUM | Libs, integrations, tooling — does the ecosystem solve it or will you have to reinvent? |
| **DX (Developer Experience)** | MEDIUM | Iteration speed, debugging, deploy — is the day-to-day fluid? |
| **Hiring pool** | LOW* | If the project will have a team, are there people who know this? |

*Hiring pool is low because Higher Mind projects are builder-first. But it counts if the team will scale.

**Justify each choice in one sentence.** If two options are close, explain why one wins.

**Choice anti-patterns:**
- "Everyone uses it" is not a reason
- "It's what I know" is not a reason (unless the deadline justifies it)
- "We might need it" is not a reason to add a dependency

### 2. Define the architecture as agent-first (when applicable)

If the project has an AI/agent component:
- **Agent-first**: the agent executes, the UI gives visibility and override
- **Chat-first**: the main interface is conversation, not forms
- Before building UI for something, ask: "Can the agent do this through conversation?"
- Dashboards exist for visibility, not for primary input

If the project is purely frontend/a tool, skip this step.

### 3. Set up the structure

- A folder structure that makes the architecture visible
- Clear, respected boundaries between modules
- Consistent naming conventions
- A senior engineer would understand the project in 10 minutes

### 4. Configure quality from day one

- TypeScript strict mode (if applicable) / complete type hints (Python)
- Linting and formatting with an opinionated config
- A test framework ready to use
- Environment management (.env with .env.example)
- Git hooks if appropriate

### 5. Set up the local infrastructure

- **Docker Compose** as the default for local dev (database, cache, services)
- Ports documented and not conflicting with other projects
- Named volumes (data is sacred — never lose data)
- Health checks on the services
- Setup scripts (one command to bring everything up)
- Automatic migrations on boot

### 6. Security from the first commit

**This section is MANDATORY. No project is born without it.**

#### .dockerignore (MANDATORY in every project with Docker)
Create `.dockerignore` at the root of EACH service that has a Dockerfile:
```
.git
.gitignore
.env
.env.*
!.env.example
node_modules
__pycache__
*.pyc
.pytest_cache
.coverage
htmlcov
.venv
.next
dist
*.md
LICENSE
.vscode
.idea
.DS_Store
docker-compose*.yml
```
**If there is no .dockerignore, the project is not ready. Period.**

#### Production-ready Dockerfiles (MANDATORY)
Every Dockerfile MUST:
- Use a **multi-stage build** — a build stage separate from the final stage
- Have no gcc, dev headers, or compilation tools in the final stage
- Run as a **non-root user** (`USER appuser`, never root)
- Have a matching `.dockerignore`
- Copy deps BEFORE the code (layer cache)
- Never have `--reload`, `npm run dev`, or any development flag
- EXPOSE only the ports needed

Python backend example:
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml .
RUN pip install --no-cache-dir --target=/deps .

FROM python:3.12-slim
RUN groupadd -r app && useradd -r -g app app
WORKDIR /app
COPY --from=builder /deps /usr/local/lib/python3.12/site-packages
COPY . .
USER app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Next.js frontend example:
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
USER app
EXPOSE 3000
ENV PORT=3000 HOSTNAME="0.0.0.0"
CMD ["node", "server.js"]
```
**Requires** `output: 'standalone'` in `next.config.ts`. Without it, `.next/standalone` does not exist and the build fails.

#### Separate dev/prod entrypoints
- `entrypoint.sh` (prod): no `--reload`, no debug flags
- `entrypoint.dev.sh` (dev): with `--reload`, with debug
- `docker-compose.yml` points to prod
- `docker-compose.override.yml` overrides for dev (volume mounts, dev entrypoint, debug ports)

#### Secrets
- No secret hardcoded in any file (not even "dev defaults" that look real)
- `.env` in `.gitignore` — verify it is there
- `.env.example` with clear placeholders (`change-me-*`, `your-key-here`)
- No secret in `docker-compose.yml` — everything via `${VAR}` or `env_file`
- No secret in build logs (build args are visible in `docker history`)

#### Headers and CORS
- Security headers configured in the backend from init
- CORS configurable via an env var (never hardcoded, never `*` as the default)

#### Dependencies
- Run `npm audit` / `pip audit` at init
- Zero known vulnerabilities of HIGH or CRITICAL severity
- Lock files committed (package-lock.json, requirements.txt with hashes)

### 7. Build the code foundation

- Auth (if the project needs it)
- Database schema with migrations
- API structure (routes, middleware, error handling)
- Deploy config (if the target is known)
- A health check endpoint that checks dependencies (DB, Redis, etc — not just returning 200)

### 8. Establish cost constraints

- If it uses external APIs (LLM, etc): set context limits, avoid unnecessary calls
- If it has background jobs: set a justified frequency
- Document the estimated cost per main operation
- Cost x performance is a design constraint, not a future optimisation

### 9. Document the decisions

Create ARCHITECTURE.md explaining:
- The chosen stack and why (each tool)
- Architectural decisions and trade-offs
- How to run the project
- Ports and services
- Folder structure
- Security decisions and why

## Standards

- Every dependency must justify its existence
- The folder structure must make the architecture visible
- No placeholder code. No TODO comments on day one. Everything that exists works.
- The project must run successfully after init
- Data is sacred from the first docker-compose.yml
- **Security is foundation, not a feature. If .dockerignore, a multi-stage build, or a non-root user is missing, the init is not complete.**

## Output

After the init, the founder must be able to:
1. Understand each technical choice and why
2. Run the project with one command
3. Start building features without setup friction
4. Know how much it will cost to run in production
5. **Be certain the project is secure from commit zero**

## Rules
- Do not ask "which framework do you want?" — recommend the best one and explain why
- Do not scaffold empty files. Every file that exists has real content.
- Do not use deprecated or unmaintained packages
- Do not configure what is not needed yet. Scope to what the project needs now.
- If the founder's description is vague, ask ONE clarifying question before proceeding
- **Never expose secrets or unnecessary ports**
- **Never create a project without .dockerignore, a multi-stage Dockerfile, and a non-root user**
- **Never use `npm run dev` or `--reload` in a production Dockerfile**
- If the project will have an AI agent, architect it agent-first from the start — not "add an agent later"
- **After the init, run `/hm-security` L1 to validate that the security foundation is solid**
