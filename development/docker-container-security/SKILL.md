---
name: docker-container-security
description: Run containers with a defensive baseline that survives production. Covers non-root users, read-only filesystems, dropped Linux capabilities, secret mounts instead of build-time bake-in, image scanning with trivy, distroless and minimal base images, and the Docker-bypasses-UFW firewall pitfall. Invoke when adding Docker to a VPS with UFW, writing a new Dockerfile, or pushing an image to a public registry.
---

# Docker / Container Security

A pragmatic baseline for Docker on a single VPS or a small cluster. Covers the Dockerfile, the run-time configuration, and the host-side gotchas — particularly the UFW-bypass that catches most people once.

## When to invoke

- Installing Docker on a VPS that has UFW (read the UFW section first — Docker bypasses UFW by default)
- Writing a new Dockerfile or `docker-compose.yml` for production
- Pushing an image to a public registry
- Periodic audit of running containers
- After a base-image CVE that affects your stack

## The UFW bypass — read this first

Docker manipulates `iptables` directly. By default, **ports published with `-p` are exposed to the world**, even if UFW says they should not be. `ufw status` will mislead you.

Two options:

**Option A — use `ufw-docker`** (community-maintained, robust):

```bash
# Install ufw-docker
sudo wget -O /usr/local/bin/ufw-docker \
  https://github.com/chaifeng/ufw-docker/raw/master/ufw-docker
sudo chmod +x /usr/local/bin/ufw-docker
sudo ufw-docker install
sudo systemctl restart ufw

# Then allow per-container:
sudo ufw-docker allow web 80/tcp
```

**Option B — bind to localhost when you front with a reverse proxy**:

```yaml
# docker-compose.yml — bind to 127.0.0.1, not 0.0.0.0
services:
  app:
    ports:
      - "127.0.0.1:9000:9000"   # host nginx proxies to this
```

Verify:

```bash
sudo ss -tlnp | grep docker     # should not show 0.0.0.0:<port> for internal services
```

## Dockerfile baseline

Every production Dockerfile should:

1. **Run as a non-root user**
2. **Pin the base image** to a specific digest or version tag (not `latest`)
3. **Drop build tools** from the final image
4. **Not contain secrets** baked in

```dockerfile
# Pin to specific Node version; consider digest pinning for stricter supply chain
FROM node:20.11.1-bookworm-slim AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

FROM node:20.11.1-bookworm-slim
WORKDIR /app

# Create non-root user
RUN groupadd -r app && useradd -r -g app -d /app -s /sbin/nologin app

COPY --from=deps /app/node_modules ./node_modules
COPY --chown=app:app . .

USER app
EXPOSE 3000

# Use exec form so the process becomes PID 1 and receives signals
CMD ["node", "server.js"]
```

Notes:

- **`-slim`** is much smaller than the default tag. **Distroless** (`gcr.io/distroless/nodejs20-debian12`) is smaller and shell-less — harder to live in if an attacker gets RCE
- **Multi-stage** to leave compilers / dev deps out of the runtime image
- **`--chown` on `COPY`** so files are not owned by root inside the image
- **`USER` last** so all later instructions run as that user

## Run-time hardening

For each container, prefer the most restrictive run-time options the app actually tolerates.

```bash
docker run -d \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \              # only if the app needs to bind <1024
  --security-opt no-new-privileges:true \
  --pids-limit 200 \
  --memory 512m \
  --cpus 1 \
  -p 127.0.0.1:3000:3000 \
  --name myapp myapp:1.2.3
```

In `docker-compose.yml`:

```yaml
services:
  app:
    image: myapp:1.2.3
    read_only: true
    tmpfs:
      - /tmp:size=64m,noexec,nosuid
    cap_drop: [ALL]
    cap_add: [NET_BIND_SERVICE]
    security_opt:
      - no-new-privileges:true
    pids_limit: 200
    mem_limit: 512m
    cpus: 1.0
    user: "1000:1000"
    restart: unless-stopped
```

What each flag does:

- **`--read-only`** — root filesystem cannot be modified. Writable dirs are explicit `tmpfs` mounts or volumes.
- **`--cap-drop=ALL` + selective `--cap-add`** — drop all Linux capabilities, add only what the app needs. Most apps need none.
- **`--security-opt no-new-privileges`** — process cannot gain privileges via `setuid` binaries.
- **`--pids-limit`** — caps fork-bomb DoS.
- **`--memory` / `--cpus`** — prevents one runaway container from killing the host.

## Secrets — never bake them in

Anything in `ENV` or `ARG` ends up in image layers. Anyone who can pull the image can extract them.

```bash
# Bad
docker build --build-arg STRIPE_KEY=sk_live_... .

# Good — at runtime, from env
docker run -e STRIPE_KEY="$STRIPE_KEY" myapp

# Better — Docker secrets (Swarm) or mounted files
docker run -v /run/secrets/stripe:/run/secrets/stripe:ro myapp
# app reads /run/secrets/stripe

# Best — a real secret manager (Vault, cloud KMS) with short-lived tokens
```

To inspect a built image for accidental secrets:

```bash
docker history --no-trunc myapp:1.2.3
docker save myapp:1.2.3 -o myapp.tar
tar -xf myapp.tar
# search the layer tarballs for .env / known token prefixes
```

## Image scanning

Run a scanner on every image before deploy. **Trivy** is the most common choice and is fast enough for CI.

```bash
trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:1.2.3
```

In GitHub Actions:

```yaml
- name: Build image
  run: docker build -t myapp:${{ github.sha }} .
- name: Scan with Trivy
  uses: aquasecurity/trivy-action@<pinned-sha>
  with:
    image-ref: 'myapp:${{ github.sha }}'
    severity: 'HIGH,CRITICAL'
    exit-code: '1'
```

Scan on a schedule too — vulnerabilities are discovered after images are built. A weekly re-scan catches newly-known CVEs in already-deployed images.

## Network segmentation

Default Docker bridge network puts all containers on one flat L2 segment. They can reach each other freely.

```yaml
# docker-compose.yml — isolate concerns
networks:
  frontend:
  backend:
    internal: true                # no external connectivity
  database:
    internal: true

services:
  web:
    networks: [frontend, backend]
  api:
    networks: [backend, database]
  db:
    networks: [database]
```

`internal: true` networks have no NAT to the outside — only useful for intra-cluster communication. The DB cannot connect out to the internet, which limits exfil if compromised.

## Periodic audit

```bash
# What is running with --privileged or as root?
docker ps --format 'table {{.Names}}\t{{.Image}}' | tail -n +2 | while read name img; do
  user=$(docker inspect --format '{{.Config.User}}' "$name")
  priv=$(docker inspect --format '{{.HostConfig.Privileged}}' "$name")
  echo "$name  image=$img  user='${user:-<root>}'  privileged=$priv"
done

# Containers with publicly-bound ports
docker ps --format '{{.Names}}\t{{.Ports}}' | grep -E '0\.0\.0\.0|:::' || echo "OK - none"

# Images older than 90 days
docker images --format '{{.Repository}}:{{.Tag}} {{.CreatedSince}}' | grep -E '(months|year)'

# Stopped containers + dangling images — clean up unless you need forensic state
docker container prune -f --filter 'until=720h'   # 30 days
docker image prune -f
```

## Compose-file checklist

Before deploying any `docker-compose.yml` to production, walk this:

- [ ] No `latest` tags; versions are pinned (and ideally digest-pinned for critical images)
- [ ] Every service has `user:` set to a non-root UID:GID
- [ ] `read_only: true` wherever the app tolerates it (most do)
- [ ] `cap_drop: [ALL]` + minimal `cap_add`
- [ ] `security_opt: [no-new-privileges:true]`
- [ ] `mem_limit` and `pids_limit` set
- [ ] Ports bound to `127.0.0.1` unless intentionally public
- [ ] No secrets in `environment:` — use `env_file:` (gitignored), Docker secrets, or a manager
- [ ] Internal networks (`internal: true`) used to keep DB/cache off the public bridge
- [ ] `restart: unless-stopped` rather than `always` (so manual stops stick)
- [ ] Volumes are named, not anonymous (named volumes survive `docker compose down`, anonymous do not)

## What this skill will not do

- Help bypass container isolation on systems you do not own
- Recommend `--privileged`, `--cap-add=SYS_ADMIN`, or running as root unless there is a documented, narrow need
- Replace a full Kubernetes security review (different stack, different controls)
