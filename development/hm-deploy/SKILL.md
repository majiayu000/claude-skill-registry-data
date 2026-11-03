---
name: hm-deploy
description: "Use when validating a deploy or a local environment."
version: 1.0.0
ported: 1.0.0
author: Rodrigo Lopes
license: MIT
metadata:
  hermes:
    tags: [owner-library, highermind, deploy, docker, security]
    related_skills: [hm-security, hm-qa]
---
> Ported from the owner's skills library (port 1.0.0; the source hash and
> what it needs are in `manifest.json` next to this file). Paths written `{skill_dir}/…` are this skill's own
> folder, `{skills_root}/<name>/…` a sibling icloneOS skill, `{agent_home}/…` the agent's home. Needs `docker` on PATH.
> Third-party work by Rodrigo Lopes (highermind-code-skills, https://github.com/rodrigohighermind/highermind-code-skills), MIT: the licence text is in `LICENSE` beside this file.

# /hm-deploy — Deploy Validation (v2)

You are now in **deploy mode**. Your job is to make sure the project is ready to leave local and go out into the world. Or that the local environment is healthy and reproducible.

## Core principle

Deploy is not the last step. It is an engineering layer. If the deploy is fragile, the product is fragile. If bringing up the environment depends on tribal knowledge, the project is not ready. **Deploy security is not a final checklist — it is a prerequisite.**

## When to use

- Before going to production for the first time
- When the local environment stopped working
- When the infra changed (new service, new port, new variable)
- To validate that anyone can bring the project up from scratch
- After a significant refactor

## What you validate

### 0. Security Gate (FIRST — before everything)

**This section is blocking. If any CRITICAL item fails, the deploy is NOT ready. It does not matter if everything else works.**

| Check | Criterion | Severity |
|---|---|---|
| `.dockerignore` | Exists in EACH service with a Dockerfile. Excludes: `.env`, `.env.*`, `.git`, `node_modules`, `__pycache__`, `.venv`, `.next` | **CRITICAL** — without it, secrets leak into the Docker image layers. Anyone with access to the image extracts .env |
| Prod-ready Dockerfile | Multi-stage build. No gcc/dev headers in the final image. No `npm run dev`. No `--reload`. No `--debug`. | **CRITICAL** — a dev server in production = unstable hot reload + exposed source maps + info leak |
| Non-root user | The container runs as a non-root user (`USER appuser`) | **HIGH** — if the container is compromised, the attacker has root |
| Build secrets | No secret in the Dockerfile (COPY, ARG, ENV with real values) | **CRITICAL** — visible in `docker history`, unrecoverable |
| Secrets in compose | docker-compose.yml uses `${VAR}` or `env_file`, never literal secret values | **CRITICAL** — a compose committed to git = public secrets |
| Separate entrypoint | dev (with --reload) and prod (without --reload) are different entrypoints | **HIGH** — a single entrypoint tries to serve two purposes and fails at both |
| Dependency audit | Zero HIGH/CRITICAL CVEs in dependencies (`npm audit`, `pip audit`) | **HIGH** — a known vulnerability is an open door |
| CORS | Configurable via an env var. Never `*` in production. Never a hardcoded localhost. | **HIGH** — CORS `*` lets any origin make authenticated requests |
| Swagger/Debug | `/docs`, `/redoc`, debug mode disabled when `APP_ENV != development` | **HIGH** — documentation endpoints expose the whole API surface |

**If `.dockerignore` does not exist: STOP EVERYTHING. Create it before continuing the validation.**

### 1. Docker & Containers

**Bring-up:**
- Does `docker compose up` bring up every service without errors?
- Do all containers become healthy? (not just running — healthy)
- Is the dependency order correct? (database before the API, etc)
- Do the container logs show a clean startup?

**Rebuild:**
- Are code changes reflected after `docker compose build <service> && docker compose up -d <service>`?
- Does the Dockerfile use a multi-stage build?
- Is the layer cache optimised? (deps before the code copy)
- Does the final image have no unnecessary dev tools?
- Is the final image size reasonable? (Python slim < 200MB, Node alpine < 150MB)

**Sacred data:**
- Are volumes named (never anonymous)?
- Does `docker compose down` (without -v) preserve all data?
- Does database data survive a container rebuild?
- If there is local production data, is it protected against `down -v`?

### 2. Environment & Configuration

- Does `.env.example` exist and have ALL the variables needed?
- Is no secret hardcoded in the code or in docker-compose.yml?
- Are sensitive variables marked as such in .env.example? (with `change-me` or `your-key-here`)
- Do the default values make sense for local dev?
- Are ports documented and not colliding with other projects?

**Port checklist (Higher Mind projects):**
| Project | API | Web | Postgres | Redis | Others |
|---|---|---|---|---|---|
| higher-mind-os | 8000 | 3000 | 5432 | 6379 | — |
| scout | 8001 | 3000 | 5433 | 6381 | — |
| hm-finance | 8003 | 3001 | 5434 | — | — |
| orion-finance | 8005 | 3002 | 5436 | 6383 | MinIO 9000-9001 |
| hm-product-lab | 8004 | — | 5435 | 6382 | — |

If the project is new, choose ports that do not collide.

### 3. Database & Migrations

- Do migrations run automatically on container boot?
- Are migrations in order and without gaps?
- Is no migration destructive without being reversible?
- Does the current schema reflect every applied migration?
- Does the app's connection to the database work right after bring-up?

### 4. Health & Monitoring

- Does a health check endpoint exist? (`/health` or `/api/health`)
- Does the health check return the status of dependent services (database, cache, etc)?
- The health check does NOT return just `{"status": "ok"}` — it checks the real connection to DB and Redis
- Are logs structured and useful (not too verbose)?
- Are errors logged with enough context to debug?

### 5. Reproducibility

The definitive test: **clean clone**.
1. Clone the repo
2. Copy `.env.example` to `.env`
3. Run `docker compose up`
4. Does the project work?

If any extra step is needed, documentation or automation is missing.

### 6. Deploy security (complementary checklist)

Beyond the Security Gate (section 0), verify:
- No unnecessary port exposed
- HTTPS configured (if production/homologation)
- Secrets are not in the build logs
- `.env` is in `.gitignore`
- Rate limiting on public endpoints
- Security headers configured (X-Content-Type-Options, X-Frame-Options, etc.)
- Logs do not contain secrets, tokens, or passwords

### 7. Scripts & DX

- Is there a README or ARCHITECTURE.md with setup instructions?
- Is the setup one command (or at most two)?
- Are development scripts documented? (how to run tests, how to rebuild, etc)
- Do a Makefile or convenience scripts exist if needed?

## Output format

```
SECURITY GATE
[Check]: PASSED/FAILED (details)
Gate: PASSED / BLOCKED (N critical, M high)

CONTAINERS
[Service]: healthy/unhealthy (details)
Build: OK/FAILED (details)
Data: protected/at risk (details)

ENVIRONMENT
.env.example: complete/incomplete (missing variables)
Secrets: safe/exposed (details)
Ports: OK/conflict (details)

DATABASE
Migrations: OK/failed (details)
Connection: OK/failed
Persistent data: yes/no

HEALTH
Endpoint: exists/does not exist
Services: all healthy/X unhealthy

REPRODUCIBILITY
Clean clone: works/fails at step X

COMPLEMENTARY SECURITY
[Check]: OK/issue (details)

VERDICT
Ready for deploy / BLOCKED — X critical, Y high to resolve first
```

> For a complete security audit (OWASP ASVS, LLM, multi-tenant, business logic), use `/hm-security` once the deploy is working.

## Rules
- **The Security Gate is the FIRST thing that runs. If it fails, do not continue.**
- Never assume "it works on my machine" is enough
- Data is sacred. If the validation shows a risk of data loss, it is CRITICAL.
- Every finding has a specific fix. Not just "configure it better."
- If the project does not come up from scratch with one command, that is a finding.
- If a secret is exposed, it is CRITICAL. No exceptions.
- **If `.dockerignore` does not exist, it is CRITICAL. Period.**
- **If the Dockerfile runs a dev server or --reload, it is CRITICAL. Period.**
- **If the container runs as root, it is HIGH. Period.**
- Test the clean clone mentally (or for real). Every manual step is technical debt.
- The standard: a new engineer joins the team on Monday and has the project running before lunch.
