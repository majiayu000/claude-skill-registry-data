---
name: docker-compose-dev
description: Run mjr.wtf locally using Docker Compose (SQLite), including migrations, logs, and teardown.
license: MIT
compatibility: Requires docker, docker compose, bash, git, and make.
metadata:
  repo: mjrwtf
  runner: github-copilot-cli
  version: 1.1
allowed-tools: Bash(git:*) Bash(make:*) Bash(docker:*) Bash(curl:*) Read
---

## Quick start (SQLite via compose)

1) Create env file:

```bash
cp .env.example .env
# set AUTH_TOKENS (recommended) or AUTH_TOKEN
```

2) Run migrations on the host (required on first run):

```bash
mkdir -p data
export DATABASE_URL=./data/database.db
make build-migrate
make migrate-up
```

3) Start services:

```bash
make docker-compose-up
```

4) Verify health:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/ready
```

## Useful ops

```bash
make docker-compose-logs
make docker-compose-ps
make docker-compose-down
```
