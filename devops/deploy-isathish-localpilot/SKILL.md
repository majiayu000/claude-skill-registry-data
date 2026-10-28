---
name: deploy
description: Make a project deployable and ship it — detect the stack and target, add Dockerfile/CI/config, environment and secrets handling, health checks, a release checklist, and run or document the deploy. USE WHEN the user says "deploy", "ship it", "production", "Dockerfile", "docker compose", "CI/CD", "GitHub Actions", "publish", "release", "host this", or names a platform (Vercel, Netlify, Fly.io, Render, Railway, Azure, AWS, GCP, Kubernetes, VPS).
---

# Deploy

Goal: a repeatable, documented path from `main` to a running service, with secrets out of the repo and a way back.

## 1. Detect what exists
- Stack & runtime version: manifest files (`package.json` engines, `.nvmrc`, `pyproject.toml`/`runtime.txt`, `go.mod`, `Cargo.toml`, `*.csproj`), build and start commands, output folder (static site vs server).
- Deployment artefacts already present: `Dockerfile`, `docker-compose*.yml`, `.github/workflows/*`, `vercel.json`, `netlify.toml`, `fly.toml`, `render.yaml`, `Procfile`, `k8s/`, `infra/`, Terraform/Bicep, `azure.yaml`. Extend them; don't create a second system.
- Config: how env vars are read (`process.env`, `os.environ`, config files), `.env.example`, ports, database/cache URLs, external services.
- Target: if the user named a platform use it; else infer from existing artefacts; else ask ONE question with 2–3 fitting options (e.g. static → Vercel/Netlify/GitHub Pages; container → Fly.io/Render/Azure Container Apps; serverless → Vercel/Cloudflare/Azure Functions). Prefer what the repo already hints at.

## 2. Make it deployable
- **Build is reproducible**: pinned runtime version, lockfile committed, `build` and `start` scripts, no dev-only steps at runtime.
- **Configuration from environment**: every secret/URL/port read from env with sane defaults for local dev; create/refresh `.env.example` with every variable documented; `.env*` in `.gitignore`. Never commit real secrets; if one is in the repo, flag it and tell the user to rotate it.
- **Container** (when the target runs containers): multi-stage `Dockerfile` (build stage → slim runtime image), non-root user, `.dockerignore`, `HEALTHCHECK` or a `/health` route, `EXPOSE` the port, logs to stdout. `docker compose` for local dependencies (db, cache).
- **Health & observability**: a health endpoint, structured logs, startup logging of version + config (never secrets), error reporting hook if the project already uses one.
- **CI**: a workflow that on push/PR installs → lint → typecheck → test → build, and on `main`/tags deploys. Use the platform's official action/CLI; secrets via the CI secret store (`${{ secrets.X }}`), never inline.
- **Database**: migrations run as an explicit step before the new version receives traffic; document rollback.

## 3. Verify locally before pushing
- `run_command`: build the production artefact (`npm run build`, `docker build -t app .`), run it (`docker run -p …`), hit the health endpoint (`curl -f http://localhost:PORT/health`), and for web apps `browser_inspect` the running app for console/network errors.
- Check the image size and startup logs for missing env vars.

## 4. Deploy or hand off
- If the CLI and credentials are available (`vercel`, `fly`, `az`, `gh`, `kubectl` — check with `which`), run the deploy with `run_command`, watch the output, and verify the live URL (`curl -I`, `browser_inspect`). Ask with `ask_user` before anything irreversible (prod DB migration, deleting resources, force pushes).
- Otherwise write `docs/deploy.md`: prerequisites, one-time setup (accounts, secrets to create and where), the deploy command(s), how to check health and logs, how to roll back. Keep it copy-pasteable.

## 5. Release checklist (put in the summary)
- [ ] Version bumped / tag created · [ ] Changelog updated · [ ] Tests & build green in CI · [ ] Env vars set on the platform · [ ] Migrations applied · [ ] Health check green · [ ] Rollback path known.
