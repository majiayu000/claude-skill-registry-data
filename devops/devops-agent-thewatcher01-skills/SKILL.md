---
name: devops-agent
description: >
  DevOps, CI/CD, Docker, systemd, and infrastructure automation. USE when: writing
  Dockerfiles, GitHub Actions workflows, systemd services, shell scripts, deploying services,
  troubleshooting service failures, writing CI pipelines, managing secrets in CI, setting up
  monitoring. Trigger: "write a Dockerfile", "create a CI pipeline", "fix this service",
  "automate deployment", "create systemd unit", "setup monitoring".
metadata:
  version: "1.0.0"
  category: "DevOps"
  sources: ["Docker docs", "systemd docs", "GitHub Actions docs", "Twelve-Factor App"]
---

# Skill: DevOps Agent

## Decision Tree

```
Task type?

├── Containerization → Dockerfile + docker-compose
│   ├── Production → multi-stage build + non-root user + healthcheck
│   └── Development → volume mounts + hot reload
├── CI/CD → GitHub Actions workflow
│   ├── On PR → lint + test + security scan
│   └── On release tag → build + publish + deploy
├── Service management → systemd unit
│   ├── Simple daemon → Type=simple
│   └── Forking process → Type=forking
├── Secrets → Infisical / env vars injection
│   └── Never hardcode → .env file for dev, secret manager for prod
└── Monitoring → Prometheus / healthcheck endpoint
```

## Dockerfile Best Practices

```dockerfile
# ✅ Multi-stage build (minimize image size)
FROM rust:1.94-slim AS builder
WORKDIR /build
COPY Cargo.toml Cargo.lock ./
COPY src/ ./src/
RUN cargo build --release --locked

FROM debian:bookworm-slim AS runtime
# ✅ Non-root user
RUN useradd -r -s /bin/false appuser
# ✅ Minimal deps only
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates libssl3 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /build/target/release/app /usr/local/bin/app
USER appuser
# ✅ Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
ENTRYPOINT ["/usr/local/bin/app"]
```

## docker-compose Production

```yaml
# PRODUCTION: secrets via environment injection (Infisical → env)
services:
  app:
    image: ghcr.io/org/app:${VERSION:-latest}
    restart: unless-stopped
    environment:
      - APP_ENV=production
      # PRODUCTION: Replace with Infisical machine token injection
      - API_KEY=${API_KEY}
    ports:
      - "127.0.0.1:8080:8080"   # Never 0.0.0.0 in prod
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 512M
```

## GitHub Actions — PR Workflow

```yaml
name: CI
on:
  pull_request:
    branches: [master, main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: cargo fmt --all -- --check && cargo clippy --all-targets -- -D warnings

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Test
        run: cargo test

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Audit
        run: cargo audit

  gate:
    needs: [lint, test, security]
    runs-on: ubuntu-latest
    if: always()   # Run even if above fail
    steps:
      - name: Check gate
        run: |
          if [[ "${{ needs.lint.result }}" != "success" ]]; then exit 1; fi
          if [[ "${{ needs.test.result }}" != "success" ]]; then exit 1; fi
          if [[ "${{ needs.security.result }}" != "success" ]]; then exit 1; fi
```

## Systemd Service Template

```ini
[Unit]
Description=My Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=serviceuser
WorkingDirectory=/opt/service

# PRODUCTION: inject secrets via Infisical
# ExecStart=infisical run --env=prod --token=${INFISICAL_TOKEN} -- /usr/local/bin/app
ExecStart=/usr/local/bin/app

Restart=on-failure
RestartSec=5
RestartSteps=5
RestartMaxDelaySec=120

# Resource limits
MemoryMax=1G
CPUQuota=50%

# Security hardening
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/lib/service /var/log/service

[Install]
WantedBy=multi-user.target
```

## Secret Injection Patterns

```bash
# ✅ Dev: .env file (never commit)
# ✅ Prod: Infisical (self-hosted port 8090)
infisical run --env=prod -- zeroclaw daemon

# ✅ CI: GitHub Secrets → env vars
# In workflow:
env:
  API_KEY: ${{ secrets.API_KEY }}

# ❌ NEVER:
export API_KEY="sk-abc123"  # shell history
ENV API_KEY="sk-abc123"     # Dockerfile layer
api_key = "sk-abc123"       # committed config
```

## Common Diagnostics

```bash
# Service not starting
systemctl status service-name
journalctl -u service-name -n 50 --no-pager

# Docker container crashlooping
docker logs container-name --tail 50
docker inspect container-name | python3 -m json.tool | grep -A5 State

# Port in use
ss -tlnp | grep PORT
fuser PORT/tcp

# Disk space
df -h
du -sh /var/log/* | sort -rh | head -10

# Memory pressure
free -h
ps aux --sort=-%mem | head -10
```
