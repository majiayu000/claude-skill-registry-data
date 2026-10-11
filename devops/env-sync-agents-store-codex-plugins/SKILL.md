---
name: env-sync
description: |
  Synchronize .env with .env.example for Dify Docker deployments, including the optional envs/ templates — detect new, removed and changed variables, add missing ones with default values, preserve existing customizations, never print secrets. Use when syncing env variables, checking for new Dify configuration variables, comparing .env.example vs .env, "env sync", "new env variables", "missing environment variables", or after pulling Dify updates.
---

## Location

`.env.example` and `.env` live in `dify/docker/` (DOCKER_DIR). All commands below run from that directory.

Since 1.14.1 the configuration is split in two layers:

- **Root `.env.example`** — essential startup settings (about 240 keys). `.env` is your copy of it plus your changes.
- **`envs/**/*.env.example`** — optional, provider-specific and service-specific settings: `envs/core-services/` (`shared`, `api`, `web`, `worker`, `sandbox`, `plugin-daemon`, `dify-agent`, …), `envs/databases/`, `envs/infrastructure/`, `envs/vectorstores/`, `envs/security.env.example`. To use one you copy it without the `.example` suffix. `shared.env.example` alone holds more than 500 keys.

Compose reads `envs/**/*.env` when present (`required: false`) and reads `.env` **last**, so a value in `.env` wins. `*.env` files are gitignored; the `*.env.example` templates are tracked and change with every release.

An `.env` copied from an older, monolithic `.env.example` still works: it is read last. It simply does not follow the new split.

## Never Print Secrets

`.env` holds database and Redis passwords, `SECRET_KEY`, API keys and tokens. Never `cat .env`, never echo a value of a key whose name contains `SECRET`, `PASSWORD`, `PASSWD`, `TOKEN`, `KEY`, `CREDENTIAL`, `DSN`, `AUTH`, `URL`, `URI`, `JSON` or `BASE64`, nor any value that carries credentials, such as `redis://:<password>@host`. Show key **names** and, for harmless keys, the value from `.env.example` (the default). Output you produce lands in the session transcript.

## Edge Case: .env Does Not Exist

```bash
cd $DOCKER_DIR

if [ ! -f ".env" ]; then
  echo "WARNING: .env does not exist"
  echo "Creating from .env.example..."
  cp .env.example .env
  echo "CREATED .env from .env.example"
  echo ""
  echo "IMPORTANT: Review and set these security-sensitive keys:"
  grep -oE '^(SECRET_KEY|DB_PASSWORD|REDIS_PASSWORD|INIT_PASSWORD|DIFY_AGENT_API_TOKEN|DIFY_AGENT_SERVER_SECRET_KEY)=' .env
fi
```

`grep -o` with the `=` anchor prints the key names only. An empty `SECRET_KEY` is fine since 1.14.1: the API generates a key and stores it in `volumes/app/storage`. After creating, show the user which keys still carry development defaults.

## Default: the Official dify-env-sync.sh

When `dify-env-sync.sh` exists in DOCKER_DIR (there is also a `dify-env-sync.py`), run it first. What it does, read from the script:

- backs `.env` up to `env-backup/.env.backup_<timestamp>` before changing anything
- **rebuilds `.env` from the new `.env.example`**, line by line: a key that is still in the example keeps your value (when it differs from the example), a new key gets the example's value
- **drops every key that is not in the new example**: custom keys, keys that moved into `envs/` (SMTP and storage credentials, `DIFY_AGENT_RUN_RETENTION_SECONDS`) and keys removed upstream. Its closing "consider manually removing these variables" warning is misleading, because they are already gone; the only copy is the backup
- prints the keys whose value differs from the example, and the keys that are no longer in the example

The manual algorithm below compares **key names** only and only appends, so it misses a changed default; the script reports the changed values but loses keys.

**The script prints the current `.env` value of every differing key, passwords, secrets and credential-bearing URLs (`CELERY_BROKER_URL` ships as `redis://:<password>@redis:6379/1`) included.** Run it through a filter. It shows a value only when the key name does not look secret **and** the value is a number, a boolean or empty; everything else prints as `***`, and so do the analysis lines of a masked key. Any other line (the continuation of a multi-line value, such as a PEM key whose `\n` the script expands) is dropped:

```bash
cd $DOCKER_DIR
bash dify-env-sync.sh 2>&1 | awk '
  { gsub(/\033\[[0-9;]*m/, "") }
  /^\[[0-9]+\] [A-Za-z_][A-Za-z0-9_]*$/ { key = $2; hide = 0; print; next }
  /^  \.env +[(]current[)]/ {
    val = $0; sub(/^[^:]*: ?/, "", val)
    hide = (key ~ /SECRET|PASSWORD|PASSWD|TOKEN|KEY|CREDENTIAL|DSN|AUTH|URL|URI|JSON|BASE64/) || (tolower(val) !~ /^(true|false|[0-9]+)?$/)
    if (hide) sub(/:.*/, ": ***")
    print; next }
  /^  \.env\.example/ { if (hide) sub(/:.*/, ": ***"); print; next }
  /^  [^ ]/ { if (!hide) print; next }
  /^\[(INFO|SUCCESS|WARNING|ERROR)\]/ { print; next }
  /^$/ { print; next }
  { next }'                                                  # a continuation line of a multi-line value (a PEM key): never printed
```

The filter uses only POSIX awk and was checked with gawk, mawk and busybox awk. Never run the script bare inside an agent session. If it fails, fall back to the manual algorithm.

### Restore the Dropped Keys

After the script, compare the key **names** of the backup with the new `.env`, and say where each dropped key belongs. Never print values:

```bash
cd $DOCKER_DIR
DROPPED=$(comm -23 <(grep -oE '^[A-Z_][A-Z0-9_]*' "$BACKUP_DIR/.env" | sort -u) <(grep -oE '^[A-Z_][A-Z0-9_]*' .env | sort -u))
for K in $DROPPED; do
  T=$(grep -rl "^$K=" envs --include='*.env.example' 2>/dev/null | sed 's/\.example$//' | sort | paste -sd' ' -)
  if [ -n "$T" ]; then echo "$K -> $T"; else echo "$K -> .env   (no template declares it: custom, or removed upstream)"; fi
done
```

`$BACKUP_DIR/.env` is the copy taken before the sync (the update command's backup; with a stand-alone sync use the file in `env-backup/`). Offer each key to the user:

- a key that templates under `envs/` declare goes into one of the matching `envs/**/*.env` files (when several are listed, ask which; the file is created if missing and may hold just that key)
- a key that no template declares is either custom (restore into `.env`) or removed upstream (check the release notes; leave it dropped)

Restore by copying the line from the backup, which prints nothing:

```bash
restore() { mkdir -p "$(dirname "$2")"; grep "^$1=" "$BACKUP_DIR/.env" | tail -1 >> "$2"; }   # restore <KEY> <target-file>
restore <KEY> <target-file>
```

## Sync Algorithm (manual fallback)

### Step 1: Extract Keys

```bash
cd $DOCKER_DIR

# Keys from .env.example (skip comments and empty lines)
grep -E '^[A-Z_][A-Z0-9_]*=' .env.example | cut -d= -f1 | sort > /tmp/dify-env-example-keys

# Keys from .env
grep -E '^[A-Z_][A-Z0-9_]*=' .env | cut -d= -f1 | sort > /tmp/dify-env-keys
```

### Step 2: Find New Variables

```bash
# Keys in .env.example that are NOT in .env
NEW_KEYS=$(comm -23 /tmp/dify-env-example-keys /tmp/dify-env-keys)

if [ -z "$NEW_KEYS" ]; then
  echo "No new environment variables found. .env is up to date."
else
  echo "Found new variables:"
  echo "$NEW_KEYS" | wc -l
fi
```

### Step 3: Extract Full Lines for New Variables

The new keys come from `.env.example`, so their values are defaults and safe to show:

```bash
for KEY in $NEW_KEYS; do
  LINE=$(grep -E "^${KEY}=" .env.example | head -1)
  VALUE=$(echo "$LINE" | cut -d= -f2-)
  echo "$KEY=$VALUE"
done
```

### Step 4: Show User What Will Be Added

Present as a table before making changes (the rows below are examples of the shape, not real variables):

```
| Variable                         | Default Value                    | Action Required? |
|----------------------------------|----------------------------------|------------------|
| DIFY_AGENT_API_TOKEN             | *-for-dev-only                   | YES — development default |
| DIFY_AGENT_SERVER_SECRET_KEY     | (development default)            | YES — development default |
| WEBSOCKET_MAX_HTTP_BUFFER_SIZE   | 10485760                         | No               |
```

**Flag as "Action Required"** any variable that:
- matches `*SECRET*`, `*PASSWORD*`, `*KEY*` (but not `*_TIMEOUT*` or `*_SIZE*`) or `*TOKEN*`
- has an empty value
- carries a **development default**: a value ending in `-for-dev-only`, `difyai123456`, or any value that the release notes say to change in production (`DIFY_AGENT_API_TOKEN`, `DIFY_AGENT_SERVER_SECRET_KEY` since 1.16.1)

### Step 5: Append to .env

After user confirms:

```bash
cd $DOCKER_DIR

echo "" >> .env
echo "# --- Added by dify-ops update on $(date +%Y-%m-%d) ---" >> .env

for KEY in $NEW_KEYS; do
  LINE=$(grep -E "^${KEY}=" .env.example | head -1)
  echo "$LINE" >> .env
done

echo "Added $(echo "$NEW_KEYS" | wc -l | tr -d ' ') new variables to .env"
```

## Optional Templates: envs/

For every `envs/**/*.env` the user created, compare it with its paired template. Show new keys, never add them automatically:

```bash
cd $DOCKER_DIR
find envs -name '*.env' -type f | while read -r f; do
  tpl="$f.example"
  [ -f "$tpl" ] || { echo "$f: no template $tpl (removed upstream?)"; continue; }
  new=$(comm -23 <(grep -oE '^[A-Z_][A-Z0-9_]*' "$tpl" | sort -u) <(grep -oE '^[A-Z_][A-Z0-9_]*' "$f" | sort -u))
  [ -n "$new" ] && { echo "$f — new keys in the template:"; echo "$new"; }
done
```

Also list templates that are new in this release and might be worth enabling (`git diff --name-status <old>..<new> -- docker/envs`). Copying a template to `*.env` is the user's decision.

## Cases That Need an Explicit Check

A key-by-key comparison does not catch these; check them after every update to 1.14.1 or newer:

| Key | What changed | Check |
|-----|--------------|-------|
| `COMPOSE_PROFILES` | Default gained `collaboration` in 1.14.1; the `api_websocket` service starts only with that profile | `grep -m1 '^COMPOSE_PROFILES=' .env` — add `collaboration` if an older `.env` lacks it |
| `EDITION` | Renamed `DEPLOYMENT_EDITION` in 1.17.0 (template: `envs/core-services/shared.env.example`) | If `.env` sets `EDITION`, rename it |
| `DIFY_AGENT_RUN_RETENTION_SECONDS` | Default dropped from 3 days to 2 hours in 1.17.1 and the key moved from the root file into `envs/core-services/dify-agent.env.example` | An `.env` copied from 1.16.x pins 3 days, but the official script drops the key (it left the root example), so the 2-hour default applies — restore the key into `envs/core-services/dify-agent.env` to keep the old value |
| `DIFY_AGENT_SHELLCTL_AUTH_TOKEN`, `DIFY_AGENT_SHELLCTL_ENTRYPOINT` | Removed in 1.17.0 | Drop from `.env` |
| `EXPOSE_NGINX_PORT`, `EXPOSE_NGINX_SSL_PORT` | Host ports; `NGINX_PORT` is the container-internal port | Read `EXPOSE_NGINX_PORT` for the URL, never `NGINX_PORT` |
| `SECRET_KEY` | Empty means generated and stored in `volumes/app/storage` (1.14.1) | Never change after start; keep the storage directory in the backup |

Read the "Environment Variable Changes" section of every release between the old and the new version: `gh release view <tag> -R langgenius/dify --json body -q .body`.

## Checking Removed Variables

With the official script the removed keys are already dropped from `.env`: use "Restore the Dropped Keys" above. With the manual algorithm nothing is deleted, so check for variables in `.env` that are no longer in `.env.example`:

```bash
REMOVED_KEYS=$(comm -13 /tmp/dify-env-example-keys /tmp/dify-env-keys)
if [ -n "$REMOVED_KEYS" ]; then
  echo ""
  echo "Note: These variables are in .env but no longer in .env.example:"
  echo "$REMOVED_KEYS"
  echo "They may be deprecated or moved to envs/. Check Dify release notes before removing."
fi
```

Keys that left the root file may simply have moved into a template under `envs/`: search there (`grep -rl "^KEY=" envs`) before calling one deprecated. Do NOT automatically remove these — just inform the user. They may be custom additions.

Clean up the temporary key lists once both checks are done:

```bash
rm -f /tmp/dify-env-example-keys /tmp/dify-env-keys
```

## Security-Sensitive Variables

When adding new variables, flag these for special attention:

| Pattern | Why |
|---------|-----|
| `SECRET_KEY` | Application secret — unique per instance; empty = generated and stored in `volumes/app/storage` |
| `*_PASSWORD` | Database, Redis passwords — must match service config |
| `*_API_KEY` | External service credentials |
| `*_SECRET` | OAuth, webhook secrets |
| `*_TOKEN` | Auth tokens |
| `INIT_PASSWORD` | Initial admin password |
| `*-for-dev-only`, `difyai123456` | Development defaults — never keep them in production |

If any of these are added with empty or development defaults, warn the user explicitly.