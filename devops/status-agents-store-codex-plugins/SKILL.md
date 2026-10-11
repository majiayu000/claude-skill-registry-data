---
name: status
description: Show current Dify instance status — git branch, running version vs latest stable tag, container health, .env sync state
---

# Dify Status

Show current state of a self-hosted Dify instance without making any changes.

## Process

### Step 1: Detect Working Directory

```bash
if [ -f "docker-compose.yaml" ] && [ -f ".env.example" ]; then
  DOCKER_DIR="$(pwd)"
  DIFY_ROOT="$(dirname "$(pwd)")"
elif [ -d "docker" ] && [ -f "docker/docker-compose.yaml" ]; then
  DOCKER_DIR="$(pwd)/docker"
  DIFY_ROOT="$(pwd)"
else
  echo "ERROR: Cannot find Dify Docker setup."
  echo "Run this from dify/ or dify/docker/ directory."
  exit 1
fi
```

### Step 2: Git and Version Status

The running version is the image tag in `docker-compose.yaml`; it is compared with the latest **stable tag**, never with `origin/main` (which is ahead of the last release by development commits).

```bash
cd "$DIFY_ROOT"
echo "=== Git Status ==="
echo "Branch: $(git branch --show-current)"      # empty = detached HEAD (official clone)
echo "Commit: $(git rev-parse --short HEAD)"
echo "Date:   $(git log -1 --format=%ci)"

DIRTY=$(git status --porcelain)
[ -z "$DIRTY" ] && echo "Working tree: clean" || echo "Working tree: dirty ($(echo "$DIRTY" | wc -l | tr -d ' ') files)"

echo ""
echo "=== Version ==="
git fetch origin --tags --quiet 2>/dev/null
RUNNING=$(grep -m1 -oE 'langgenius/dify-api:[0-9][^ ]*' "$DOCKER_DIR/docker-compose.yaml" | cut -d: -f2)
LATEST_TAG=$(git tag --list | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -1)
echo "Running version: ${RUNNING:-unknown}   (image tag in docker-compose.yaml)"
echo "Latest stable:   ${LATEST_TAG:-unknown}"
if [ -n "$RUNNING" ] && [ -n "$LATEST_TAG" ]; then
  OLDEST=$(printf '%s\n' "$RUNNING" "$LATEST_TAG" | sort -V | head -1)
  if [ "$RUNNING" = "$LATEST_TAG" ]; then echo "Up to date"
  elif [ "$OLDEST" = "$RUNNING" ]; then echo "Update available — run /dify-ops:update"
  else echo "Ahead of the latest stable tag (running a newer tag or main)"; fi
fi

# Heads-up: the bundled Weaviate needs a staged upgrade across 1.17.1
VS=$(grep -E '^VECTOR_STORE=' "$DOCKER_DIR/.env" 2>/dev/null | tail -1 | cut -d= -f2); VS=${VS:-weaviate}
if [ "$VS" = weaviate ] && [ -n "$(ls -A "$DOCKER_DIR/volumes/weaviate" 2>/dev/null)" ] \
   && [ "$(printf '%s\n' "${RUNNING:-0}" 1.17.1 | sort -V | head -1)" != 1.17.1 ] \
   && [ "$(printf '%s\n' "${LATEST_TAG:-0}" 1.17.1 | sort -V | head -1)" = 1.17.1 ]; then
  echo "NOTE: updating to 1.17.1 or newer moves the bundled Weaviate 1.27.0 -> 1.39.2 and needs a staged volume upgrade first."
  echo "      /dify-ops:update stops and points to the runbook; see the update-workflow skill."
fi
```

### Step 3: .env Sync Check

Compares key names in `.env` with `.env.example`, then checks the keys a name comparison misses. It never prints a value of a secret-looking key.

```bash
cd "$DOCKER_DIR"
echo ""
echo "=== Environment Status ==="

if [ ! -f ".env" ]; then
  echo ".env: MISSING — run /dify-ops:update to create"
else
  NEW_COUNT=$(comm -23 <(grep -oE '^[A-Z_][A-Z0-9_]*=' .env.example | sort -u) <(grep -oE '^[A-Z_][A-Z0-9_]*=' .env | sort -u) | wc -l | tr -d ' ')
  REMOVED_COUNT=$(comm -13 <(grep -oE '^[A-Z_][A-Z0-9_]*=' .env.example | sort -u) <(grep -oE '^[A-Z_][A-Z0-9_]*=' .env | sort -u) | wc -l | tr -d ' ')

  echo ".env: exists"
  [ "$NEW_COUNT" -gt 0 ] && echo "Missing vars: $NEW_COUNT (run /dify-ops:update to add)" || echo "Missing vars: 0 — in sync"
  [ "$REMOVED_COUNT" -gt 0 ] && echo "Extra vars:   $REMOVED_COUNT (deprecated, moved to envs/, or custom)"

  grep -q '^COMPOSE_PROFILES=.*collaboration' .env || echo "COMPOSE_PROFILES: no 'collaboration' profile — api_websocket does not start (default since 1.14.1)"
  grep -q '^EDITION=' .env && echo "EDITION is set — renamed DEPLOYMENT_EDITION in 1.17.0"
fi

# Optional templates: envs/**/*.env the user created, against their paired *.env.example
find envs -name '*.env' -type f 2>/dev/null | while read -r f; do
  tpl="$f.example"
  [ -f "$tpl" ] || { echo "$f: no template $tpl"; continue; }
  n=$(comm -23 <(grep -oE '^[A-Z_][A-Z0-9_]*' "$tpl" | sort -u) <(grep -oE '^[A-Z_][A-Z0-9_]*' "$f" | sort -u) | wc -l | tr -d ' ')
  [ "$n" -gt 0 ] && echo "$f: $n new key(s) in its template"
done
```

### Step 4: Docker Container Status

The project name comes from the labels of the running `api` container of this directory:

```bash
echo ""
echo "=== Container Status ==="

PROJECT_NAME=$(docker ps --filter "label=com.docker.compose.service=api" \
  --filter "label=com.docker.compose.project.working_dir=$DOCKER_DIR" \
  --format '{{.Label "com.docker.compose.project"}}' 2>/dev/null | head -1)
if [ -n "$PROJECT_NAME" ]; then
  echo "Docker project: $PROJECT_NAME"
  cd "$DOCKER_DIR"
  COMPOSE_PROJECT_NAME="$PROJECT_NAME" docker compose ps 2>/dev/null || docker ps --filter "label=com.docker.compose.project=$PROJECT_NAME" --format "table {{.Names}}\t{{.Status}}"
else
  echo "No running Dify containers detected"
fi
```

A healthy stack shows every service `Up` or `healthy`; `init_permissions` is a one-shot task and shows `Exited (0)`.

### Step 5: Health Check

The host port is `EXPOSE_NGINX_PORT` (default 80). `NGINX_PORT` is the container-internal port and must not be read here.

```bash
PORT=$(grep -E '^EXPOSE_NGINX_PORT=' "$DOCKER_DIR/.env" 2>/dev/null | tail -1 | cut -d= -f2)
PORT=${PORT:-80}
echo ""
echo "=== Health ==="
curl -s -o /dev/null -w "Web UI (port $PORT): HTTP %{http_code}" "http://localhost:${PORT}" 2>/dev/null || echo "Web UI: not reachable"
```