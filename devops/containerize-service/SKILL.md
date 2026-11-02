---
name: containerize-service
description: Use when a backend or full-stack service needs a production container image — multi-stage Dockerfile per track (Node/pnpm, Go, Python/uv), non-root, digest-pinned bases, health check, SBOM and provenance, image scan.
---

# Containerize Service

One image per service, built once, run as a non-root user, healthy only when the service says so. The same image goes to `dev`, `stg` and `prd` ([environments.md](../_shared/environments.md)).

## 1. Audit current state (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null                       # languages, package_manager, backend.track, hosting
ls Dockerfile* .dockerignore compose*.y*ml deploy/ 2>/dev/null
ls pnpm-lock.yaml go.mod pyproject.toml uv.lock 2>/dev/null     # which track(s)
grep -rn "healthz\|/health" --include=*.ts --include=*.go --include=*.py . 2>/dev/null | grep -v node_modules | head -3
docker --version && docker buildx version
```

Read from the profile: `languages`, `package_manager` (pnpm, go, uv), `backend.track` (hono, nextjs, go, fastapi), `hosting`. If there is no profile, detect from the lockfiles above. Ask one question only when two tracks match (a monorepo) and the choice changes the output: which service to containerize. Suggest `set-up-stack-profile` if the profile is missing.

## 2. Decide
- No `Dockerfile` → full (steps 3 to 7).
- `Dockerfile` exists → delta: check each line of the checklist below, fix only what fails.
- All checks pass and `trivy` is clean → say "already in place" and stop.

Checklist: multi-stage; every `FROM` has `@sha256:`; final stage non-root; `.dockerignore` excludes `.git`, `node_modules`, `.env*`; `HEALTHCHECK` present; no secret in `ENV`, `ARG` or `COPY`; `--frozen-lockfile`, `--locked` or `go mod download` before source copy.

## 3. Detect the track
| Evidence | Track | Template in [dockerfile-patterns.md](./dockerfile-patterns.md) |
|---|---|---|
| `package.json` + `pnpm-lock.yaml` (Hono, Fastify, Nest) | Node/pnpm | "Node (pnpm)" |
| `package.json` with `next` | Node/pnpm, Next.js | "Node (pnpm)" plus the standalone note |
| `go.mod` | Go static | "Go" |
| `pyproject.toml` + `uv.lock` (FastAPI) | Python/uv | "Python (uv)" |
| `npm`/`yarn`/`bun` lockfile | same shape; swap the install line | keep the stage layout |

Hosted on Vercel (`hosting: [vercel]`) and no worker or long-running process: no image needed. Stop and say so; use [deploy-to-vercel](../deploy-to-vercel/SKILL.md).

## 4. Install only what is missing
Nothing on the host except Docker with BuildKit (`docker buildx version`). Do not install language toolchains for the image; the build stage carries them. Create `.dockerignore` first:

```gitignore
.git
node_modules
dist
.venv
__pycache__
bin
*.test
.env*
!.env.example
Dockerfile
.dockerignore
```

## 5. Generate the seams
1. **Health seam.** The service exposes `GET /healthz` returning 200 when it can serve. The image probes it with the service's own binary, because distroless has no `curl` or shell. Code for each track is in [dockerfile-patterns.md](./dockerfile-patterns.md).
2. **Dockerfile** from the track template. Set the three `ARG … IMAGE=` lines to the digests in [stack-versions.md](../_shared/stack-versions.md); re-read the digest with `docker buildx imagetools inspect <image:tag> --format '{{.Manifest.Digest}}'`.
3. **Graceful shutdown.** The process handles `SIGTERM` and finishes in-flight requests within 10 s. Compose and Kubernetes send `SIGTERM` first.

## 6. Wire
- **Build locally** with attestations and check them:
  ```bash
  docker buildx build --sbom=true --provenance=mode=max -t localhost:5005/app:test --push .
  ```
  Attestations need `--push`, or the containerd image store, or a `docker-container` builder. In CI the pipeline builds with `provenance: false` and signs once with `actions/attest`; see [set-up-delivery-pipeline](../set-up-delivery-pipeline/SKILL.md). Do not add a second build path here.
- **Scan** with Trivy from a pinned image, not the GitHub Action (its tags were rewritten in March 2026):
  ```bash
  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v trivy-cache:/root/.cache \
    ghcr.io/aquasecurity/trivy:0.75.0@sha256:af6acf9a6b85dfe389a1941505c0ce9efef52a4719635e1a962f022a3d855daa \
    image --exit-code 1 --severity HIGH,CRITICAL --ignore-unfixed --no-progress app:test
  ```
  Grype (`anchore/grype`) is an equal choice if you already use Syft SBOMs.
- **Probes.** Compose uses the image `HEALTHCHECK`. Kubernetes ignores it; define `readinessProbe` and `livenessProbe` against `/healthz`.
- Compose and the host: [deploy-to-hetzner](../deploy-to-hetzner/SKILL.md), [deploy-to-ionos](../deploy-to-ionos/SKILL.md).

## 7. Verify
```bash
docker build -t app:test . && docker image inspect app:test --format '{{.Config.User}}'
```
Expect a non-root user (`65532`, `nonroot` or `10001:10001`), never empty or `0`.
```bash
docker run -d --name app-test -p 3000:3000 app:test && sleep 12 && curl -fsS localhost:3000/healthz
docker inspect app-test --format '{{.State.Health.Status}}'     # healthy
docker rm -f app-test
```
Expect `ok` and `healthy`. Reproducibility check (same digest twice):
```bash
for i in 1 2; do docker buildx build --no-cache --provenance=false --sbom=false \
  --build-arg SOURCE_DATE_EPOCH=1760000000 --output type=oci,dest=/tmp/r$i.tar,rewrite-timestamp=true . ; done
for i in 1 2; do tar -xOf /tmp/r$i.tar index.json | grep -o 'sha256:[a-f0-9]*' | head -1; done
```
Expect two identical digests. Trivy exits 0.

## References
- [container-patterns.md](./container-patterns.md): the rules and why (base image, user, pinning, health, SBOM, scanning, secrets).
- [dockerfile-patterns.md](./dockerfile-patterns.md): the three templates, built and run during authoring.
- [../_shared/environments.md](../_shared/environments.md): build once, promote the digest.
- [../../core/_shared/security-baseline.md](../../core/_shared/security-baseline.md), [../../core/_shared/engineering-principles.md](../../core/_shared/engineering-principles.md).
