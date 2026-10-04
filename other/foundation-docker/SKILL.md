---
name: foundation-docker
description: Generate Dockerfile, docker-compose.yaml, and container config — multi-stage build (builder + slim runtime), non-root user, health check, dev/prod compose split, .dockerignore, Makefile docker targets, end-to-end `docker compose up` smoke test. Loads at containerization bootstrap when no Dockerfile exists, or when the operator says "containerize this", "add Docker", "set up docker-compose".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# foundation-docker

The foundation skill that authors a project's container layer. AICP's pattern (per [docker-compose.yaml](../../../docker-compose.yaml) + Dockerfile.localai): LocalAI runs in Docker with GPU passthrough on `:8090`; AICP itself runs natively on the host (single-operator). Sister fleet projects use the same dev/prod compose-split pattern.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **No Dockerfile exists**: project has no `Dockerfile`, no `docker-compose.yaml`, no `.dockerignore`. Operator wants to containerize.
- **Direct verb**: operator says "containerize this", "add Docker", "set up docker-compose", "make this run in a container", "we need a docker image".
- **Foundation-stage of project-lifecycle**: a new sister project at the foundation stage; container layer is one of the foundation deliverables.
- **CI requires container**: `foundation-ci` decided to run tests inside a container; that needs the Dockerfile authored first.

Do NOT load when:

- Dockerfile exists but is broken — load `feature-iterate` (refine) or `quality-debt` (it's debt-flagged).
- Adding a new compose service to existing compose — load `feature-implement` with the service as the deliverable.
- Tuning compose envs (`CONTEXT_SIZE`, `THREADS`) for an existing setup — load `config-deploy` (per-env compose tuning).
- The project is intentionally container-free (single-operator local Python tool) — respect that. AICP itself isn't fully containerized.

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Read project; decide the container shape

**Trigger**: skill loaded; operator confirmed greenfield containerization.

**Process**:

1. Read [pyproject.toml](../../../pyproject.toml) (or equivalent manifest) — capture: language version floor, runtime deps, build deps, entry points.
2. Read [docs/architecture.md](../../../docs/architecture.md) Deployment Model section. Decide:
   - **Single service** (one app process): one Dockerfile + simple compose.
   - **Multi-service** (app + DB + cache + monitoring): compose orchestrates each.
   - **Sidecars** (e.g., LocalAI inference + AICP wrapper): compose with depends_on chain.
3. Decide GPU requirements:
   - **None**: stock base image (e.g., `python:3.11-slim`).
   - **CUDA**: nvidia-cuda base + NVIDIA Container Toolkit on host (architecture mentions GPU).
4. Decide dev vs prod split:
   - **dev**: bind-mount source for hot reload, expose ports, looser secrets.
   - **prod**: COPY source into image, healthcheck, restart policy, no host volumes for source.
   - One `docker-compose.yaml` (prod-shape) + `docker-compose.override.yaml` (dev-only, auto-merged) is the canonical pattern.
5. State the plan (single-vs-multi service, GPU yes/no, dev/prod split). Wait for "go".

**Quality bar (Operation 1 done when)**:

- [ ] Service count + composition decided (single / multi / sidecar).
- [ ] GPU requirement read from architecture, not assumed.
- [ ] dev/prod split strategy chosen.
- [ ] Operator approved.

### Operation 2: Author Dockerfile + .dockerignore

**Trigger**: Operation 1 plan approved.

**Process**:

1. Author `Dockerfile` with multi-stage build:
   ```dockerfile
   # Stage 1: builder — compile + install deps
   FROM python:3.11-slim AS builder
   WORKDIR /build
   COPY pyproject.toml ./
   RUN pip install --user --no-cache-dir -e ".[dev]"
   COPY . .

   # Stage 2: runtime — slim, non-root, health-checked
   FROM python:3.11-slim AS runtime
   RUN useradd --create-home --shell /bin/bash app
   WORKDIR /home/app
   COPY --from=builder --chown=app:app /root/.local /home/app/.local
   COPY --chown=app:app . .
   USER app
   ENV PATH=/home/app/.local/bin:$PATH
   HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
     CMD <project-cli> --check || exit 1
   EXPOSE <port>
   CMD ["<project-cli>", "<args>"]
   ```
2. Layer ordering: deps BEFORE code. `pyproject.toml` (rarely changes) copied first, then `pip install`, then `COPY . .` last. This keeps the dep layer cached across most code changes.
3. Author `.dockerignore` to keep image small:
   ```
   .git/
   .venv/
   __pycache__/
   *.pyc
   .pytest_cache/
   .ruff_cache/
   tests/
   docs/
   wiki/
   .env
   .env.*
   *.gguf
   *.safetensors
   models/
   ```
4. Pin the base image to a specific tag, not `:latest` — `python:3.11-slim` is OK (slim moves slowly), `python:3.11.9-slim-bookworm` is more reproducible.
5. Run as non-root (`USER app`). Most container CVEs come from running as root; this is the highest-leverage one-line fix.

**Quality bar (Operation 2 done when)**:

- [ ] Dockerfile uses multi-stage (builder + runtime).
- [ ] Deps installed BEFORE source COPY (cache-friendly layering).
- [ ] Non-root user via `USER app` directive.
- [ ] Healthcheck wired to a real readiness command.
- [ ] Base image pinned (not `:latest`).
- [ ] `.dockerignore` excludes test fixtures, caches, secrets, large model files.
- [ ] Image builds: `docker build -t <name>:test .` exits 0.
- [ ] Final image size reasonable (target: <500MB for Python apps without ML weights).

### Operation 3: Author docker-compose + dev override

**Trigger**: Operation 2 image builds.

**Process**:

1. Author `docker-compose.yaml` (prod-shape):
   ```yaml
   services:
     app:
       build: .
       restart: unless-stopped
       env_file: .env
       ports:
         - "${APP_PORT:-8000}:8000"
       healthcheck:
         test: ["CMD", "<cli>", "--check"]
         interval: 30s
         start_period: 15s
       # GPU passthrough only if architecture requires it
       # deploy:
       #   resources:
       #     reservations:
       #       devices: [{driver: nvidia, capabilities: [gpu]}]
   ```
2. Author `docker-compose.override.yaml` (dev-only, auto-merged):
   ```yaml
   services:
     app:
       build:
         target: builder  # use builder stage in dev for tools
       volumes:
         - .:/home/app  # bind-mount source for hot reload
       environment:
         - DEBUG=1
       command: <hot-reload-command>
   ```
3. For multi-service (per Operation 1), add database/cache/monitoring services with `depends_on` + `healthcheck`. App should `depends_on: [{ <service>: { condition: service_healthy } }]` — not just `service_started`.
4. Configure networking: services on the same custom network can resolve each other by service name (e.g., `db:5432`). Don't expose ports that don't need to be host-visible.
5. Add Makefile targets that mirror compose actions:
   ```make
   build: ; docker compose build
   up:    ; docker compose up -d
   down:  ; docker compose down
   logs:  ; docker compose logs -f
   shell: ; docker compose exec app bash
   ```

**Quality bar (Operation 3 done when)**:

- [ ] Prod compose has restart policy + healthcheck + env_file.
- [ ] Dev override uses bind-mount for hot reload; doesn't bake source.
- [ ] Services use service-name DNS; only host-needed ports exposed.
- [ ] `depends_on` uses `condition: service_healthy` where applicable.
- [ ] Makefile has `build`, `up`, `down`, `logs`, `shell` targets.
- [ ] No literal secrets in compose YAML (env_file references, no inline values).

### Operation 4: Smoke test + document

**Trigger**: Operation 3 compose written.

**Process**:

1. Smoke test the dev path:
   ```bash
   make build          # docker compose build
   make up             # bring everything up
   docker compose ps   # verify containers in "running (healthy)" state
   <project-cli> --check  # via host or `docker compose exec app <cli> --check`
   make logs           # confirm clean startup, no error tracebacks
   make down           # tear down clean
   ```
2. Smoke test the prod path: build with `docker compose --file docker-compose.yaml up -d` (no override). Verify:
   - Source is COPIED, not bind-mounted (verify by `docker compose exec app ls /home/app` shows the COPY'd tree).
   - `docker compose exec app whoami` returns `app`, not `root`.
   - Healthcheck passes (`docker compose ps` shows `(healthy)` not `(unhealthy)` or `(starting)`).
3. Document:
   - README "Running with Docker" section: build, up, healthcheck, ports, env vars.
   - Common operations: `make logs`, `make shell`, env override pattern.
   - Note GPU prerequisites if applicable (NVIDIA Container Toolkit, driver version).
4. Suggest the next foundation skill if applicable: `foundation-ci` (CI runs in container), `foundation-config` (env-var plumbing), `foundation-logging` (container log driver).

**Quality bar (Operation 4 done when)**:

- [ ] Dev path: `make build && make up && make down` cycle exits 0; healthcheck passes during `up`.
- [ ] Prod path: image runs as non-root, source is COPY'd not bind-mounted, healthcheck reports healthy.
- [ ] README has a Docker section with build + up + ops commands.
- [ ] Next-step skill suggested.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Cache-busting layer order

`COPY . .` BEFORE `pip install`. Result: ANY code change invalidates the dep layer; every rebuild reinstalls all deps (60s+ wasted per change).

**The rule**: stable inputs (deps, base packages) come before volatile inputs (source code). `pyproject.toml` first, install, then COPY source. Verify by changing one file in `aicp/` and rebuilding — should reuse the dep layer (visible as `CACHED` in `docker build` output).

### Gotcha 2: Running as root

No `USER` directive; container runs as root. CVE in any installed package becomes a host compromise. Volume mounts may write files owned by root, frustrating dev workflow.

**The rule**: every Dockerfile has `RUN useradd --create-home app` + `USER app` before `CMD`. Verify: `docker compose exec app whoami` returns `app` not `root`. If you need root for debugging, use `docker compose exec --user root app` per-call, don't change the Dockerfile.

### Gotcha 3: Secrets baked into image

`COPY .env .` or `ENV API_KEY=sk-...` in the Dockerfile. Secret is now in the image layers — anyone who pulls the image (registry, CI cache) sees the value, even if you "remove" it in a later step.

**The rule**: secrets via `env_file: .env` at compose runtime, NOT via Dockerfile build. `.dockerignore` MUST list `.env` and `.env.*`. Verify nothing leaked: `docker history <image>` should show no env vars holding secrets.

### Gotcha 4: Healthcheck that always passes

`HEALTHCHECK CMD true` (or absent). Container reports healthy even when the app process is wedged. Compose `depends_on: condition: service_healthy` becomes a lie.

**The rule**: healthcheck calls a real readiness endpoint (`<cli> --check` for AICP-domain, `curl -f localhost:<port>/healthz` for HTTP). Test failure mode: deliberately break the app inside the container, verify healthcheck transitions to `(unhealthy)` within `interval × retries`.

### Gotcha 5: Latest tag everywhere

`FROM python:latest`, `FROM postgres:latest` — feels future-proof, actually means each rebuild may pull a different image. Reproducibility broken; "works on my machine" returns.

**The rule**: pin every base image (`python:3.11-slim` minimum, `python:3.11.9-slim-bookworm` for full reproducibility). Same for compose images (`postgres:16` not `postgres:latest`). Document the upgrade cadence in README.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

The canonical AICP-domain Docker reference: [docker-compose.yaml](../../../docker-compose.yaml) (LocalAI service with GPU passthrough on `:8090`, watchdog config, env-driven tuning) + alternative configs at [docker-compose.multi-gpu.yaml](../../../docker-compose.multi-gpu.yaml) and [docker-compose.p2p.yaml](../../../docker-compose.p2p.yaml).

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP-specific scope notes:

- AICP itself runs natively on the host (Python venv); LocalAI runs in Docker. This split is intentional — the AI control plane stays close to the operator.
- For sister fleet projects (Mission Control, Plane integration), full containerization is the norm.
- GPU passthrough requires NVIDIA Container Toolkit (per [SETUP.md](../../../SETUP.md) prerequisites).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| foundation-ci | Pipeline that runs tests in containers | foundation-docker authors images; foundation-ci uses them |
| config-deploy | Tune compose envs per environment | foundation-docker provides plumbing; config-deploy picks values |
| ops-deploy | Deploy the built image to runtime | foundation-docker builds; ops-deploy ships |
| infra-monitoring | Add Prometheus/Grafana sidecars | Adds NEW services; foundation-docker is greenfield containerization |
| ops-scale | Adjust replicas/resources | Tunes existing compose; foundation-docker authors |
