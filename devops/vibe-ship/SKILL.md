---
name: vibe-ship
description: Generates a complete, production-ready deployment setup for any app in one pass -- Dockerfile, docker-compose.yml, .dockerignore, CI/CD (GitHub Actions), scalability config (health checks, resource limits, K8s on request), and security hardening (non-root user, secrets, dependency scanning). Auto-detects the stack from repo files (package.json, requirements.txt, go.mod, pom.xml, Gemfile, etc.) and writes real working files, not just advice. Also audits an EXISTING Dockerfile/compose/CI setup with a static scoring script and reports concrete findings. Use whenever the user asks to "dockerize", "containerize", "make this deployable", "production-ready", "vibe ship this", "add CI/CD", "set up deployment", "ship this app", requests a Dockerfile/docker-compose/GitHub Actions workflow, or wants a deployment setup reviewed -- even for just one piece (e.g. "add a Dockerfile"), since the full set is interdependent.
---

# vibe-ship

Turns any codebase into something that can be deployed with `docker compose up` and shipped through CI/CD with sane, hardened defaults - all generated in one pass, tailored to the actual project. You bring the vibe; this brings the infrastructure.

## Two modes

1. **Generate** (default) - no deployment files exist yet, or the user wants a fresh setup. Walk through the workflow below.
2. **Audit** - deployment files already exist and the user wants them reviewed/scored rather than replaced. Skip straight to "Audit an existing setup" below.

---

## Generate: Workflow

### 1. Detect the stack

Look for these signal files in the project root (and one level into common subfolders like `backend/`, `server/`, `api/`):

| File found | Stack | Default port | Start command |
|---|---|---|---|
| `package.json` | Node.js | 3000 | read `scripts.start` |
| `requirements.txt` / `pyproject.toml` | Python | 8000 | detect Flask/FastAPI/Django |
| `go.mod` | Go | 8080 | `go build` |
| `pom.xml` / `build.gradle` | Java/Kotlin (JVM) | 8080 | detect Spring Boot / Gradle app |
| `Gemfile` | Ruby | 3000 | detect Rails/Sinatra |
| `Cargo.toml` | Rust | 8080 | `cargo build --release` |
| `composer.json` | PHP | 8000 | detect Laravel/Symfony |

If multiple signal files exist (e.g. a `frontend/` and `backend/` folder), treat it as a **multi-service app** - generate one Dockerfile per service plus a docker-compose.yml that wires them together.

If you can't confidently detect a stack, ask the user rather than guessing - a wrong Dockerfile base image is worse than no Dockerfile.

Also detect:
- **Package manager** (npm vs yarn vs pnpm, pip vs poetry vs uv) from lockfiles present.
- **Database/cache dependencies** (look for `pg`, `mongoose`, `redis`, `sqlalchemy`, etc. in dependency files) - these become services in docker-compose.yml.
- **Existing `.env` or `.env.example`** - never overwrite; read it to learn what env vars the app expects.
- **Existing Dockerfile/CI config** - if present, offer Audit mode instead of silently overwriting.

### 2. Read the relevant stack reference

Before writing the Dockerfile, read `references/docker-patterns.md` and jump to the section matching the detected stack. It has copy-ready multi-stage Dockerfile templates per language - adapt to the project's actual entry point, build command, and dependencies rather than pasting blind.

Also skim `references/anti-patterns.md` so the generated files avoid the common mistakes listed there by construction.

### 3. Generate the files

Write these into the project (paths relative to repo root unless multi-service):

1. **`Dockerfile`** - multi-stage build (build stage + slim runtime stage), non-root user, `HEALTHCHECK` instruction, pinned base image version.
2. **`.dockerignore`** - excludes `node_modules`, `.git`, `.env`, build artifacts, test files, etc. per stack.
3. **`docker-compose.yml`** - the app service plus any detected dependent services (postgres, redis, etc.) with named volumes, resource limits, a shared network, env vars from `.env`.
4. **`.env.example`** - every env var the app reads, with placeholder values and a comment on what each is for. Never put real secrets here.
5. **`.github/workflows/ci-cd.yml`** - see `references/cicd-patterns.md`. At minimum: install deps → lint → test → build Docker image → (on main branch) push to a registry, plus a dependency vulnerability scan step. Ask which registry (Docker Hub / GHCR / ECR / GCR) before filling in the push step - default to GHCR since it needs no extra secrets beyond `GITHUB_TOKEN`.
6. **`DEPLOYMENT.md`** - a short doc at the project root summarizing what was generated, how to run it locally (`docker compose up`), how CI/CD triggers, and a checklist of anything the user still needs to do manually.

For scalability and security specifics, read `references/scalability-checklist.md` and `references/security-checklist.md` before finalizing the Dockerfile and compose file - apply every relevant item, and note anything needing manual follow-up in `DEPLOYMENT.md` rather than silently skipping it.

If the user mentions Kubernetes, a specific cloud provider, or says Compose alone isn't enough, read `references/kubernetes.md` and generate manifests there instead of (or alongside) docker-compose.yml.

### 4. Run the audit script on what you just generated

Run `scripts/audit.py` against the generated Dockerfile/compose/CI files as a final sanity pass (see next section for usage). Fix anything it flags before presenting to the user - it should score clean on your own output.

### 5. Summarize, don't dump

Don't paste all file contents into the chat. Give a short summary: what was created, what stack was detected, what services are wired up, the audit score, and point to `DEPLOYMENT.md` for details. Offer to walk through any specific file if the user wants to review it.

---

## Audit: Reviewing an existing setup

When the user already has a Dockerfile, docker-compose.yml, or CI config and wants it reviewed rather than replaced:

```bash
python3 scripts/audit.py --path /path/to/project
```

This statically scans for the Dockerfile, docker-compose.yml, and `.github/workflows/*.yml` under the given path and checks each against the same rules in `references/security-checklist.md`, `references/scalability-checklist.md`, and `references/anti-patterns.md` - no Docker daemon or network access needed, pure text analysis. It prints a scored report (CRITICAL/HIGH/MEDIUM/LOW findings) with file:line references and a fix suggestion per finding.

Walk through the findings with the user, prioritizing CRITICAL/HIGH first (things like running as root, `:latest` tags, secrets in `ARG`/`ENV`, missing `.dockerignore`). Offer to fix them directly rather than just listing them.

## Principles

- **Real files, not essays.** Working artifacts the user can run, not a markdown lecture.
- **Multi-stage builds always.** Never ship build tools or dev dependencies in the final image.
- **Non-root by default.** Every Dockerfile creates and switches to an unprivileged user before `CMD`.
- **Never hardcode secrets.** Anything sensitive goes through env vars / `.env` (gitignored) with `.env.example` as the documented template.
- **Don't clobber existing config.** If deployment files already exist, offer Audit mode instead of overwriting.
- **Scale defaults, not over-engineering.** Health checks and resource limits by default; Kubernetes/Terraform/autoscaling only on request or when the project clearly needs it.
