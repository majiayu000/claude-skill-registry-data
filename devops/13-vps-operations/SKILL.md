---
name: vps_operations
description: VPS deployment, directory layout, env sync, backup execution, SSH access, and operational procedures.
when_to_use:
  - Deploying to production VPS
  - Setting up new VPS
  - Running backups or restores
  - Debugging VPS issues
  - Environment sync checks
---

# VPS Operations (RESTO BOT)

## VPS details

- **Host**: 72.60.190.192 (Hostinger VPS)
- **SSH**: `ssh deploy@72.60.190.192` (key auth, no password)
- **OS**: Linux (Ubuntu-based)
- **Docker**: Available at `/usr/bin/docker`

## Directory layout

```text
/opt/resto/
  current/          -> symlink to active release
  releases/
    YYYYMMDD-HHMMSS-<sha>/    -> each release
  backups/          -> DB dumps
  secrets/          -> credential files (on VPS only)
```

## Production compose

```bash
cd /opt/resto/current
docker compose -f docker-compose.hostinger.prod.yml up -d
```

## External networks (must exist)

```bash
docker network create proxy 2>/dev/null || true
docker network create internal 2>/dev/null || true
```

## External volumes (must exist)

```bash
for vol in cms_uploads n8n_data ollama_data postgres_data redis_data traefik_data; do
  docker volume create "$vol" 2>/dev/null || true
done
```

## Secrets on VPS

Located at `/opt/resto/current/secrets/`:
- `n8n_encryption_key`
- `postgres_password`
- `redis_password`
- `strapi_db_password`
- `traefik_usersfile`

## Backup procedures

### PostgreSQL backup

```bash
ssh deploy@72.60.190.192 'cd /opt/resto/current && \
  docker compose -f docker-compose.hostinger.prod.yml exec -T postgres \
  pg_dump -U n8n -d n8n --format=custom > /opt/resto/backups/n8n_$(date +%Y%m%d_%H%M%S).dump'
```

### PostgreSQL restore

```bash
docker compose -f docker-compose.hostinger.prod.yml exec -T postgres \
  pg_restore -U n8n -d n8n --clean --if-exists < /opt/resto/backups/<backup_file>.dump
```

## Operational scripts

| Script | Purpose |
| --- | --- |
| `project/scripts/ops/deploy_staging_to_node.sh` | Deploy staging to VPS |
| `project/scripts/ops/rollback.sh` | Emergency rollback |
| `project/scripts/ops/provision_vps.sh` | Initial VPS setup |
| `project/scripts/preflight-prod.sh` | Pre-deploy validation |
| `project/scripts/smoke_security.sh` | Post-deploy smoke tests |
| `project/scripts/validate_cicd.sh` | CI/CD + VPS connectivity test |
| `project/scripts/validate_go_no_go.sh` | Go/no-go decision |

## Disk space warning

- VPS disk can fill up quickly (monitor with `df -h /`)
- Docker logs rotate (configured in compose)
- Clean old releases: keep last 3 in `/opt/resto/releases/`
- Clean Docker: `docker system prune -f` (never prune volumes)

## Environment sync

- Local `.env` must match VPS `.env` for all [REQUIRED] vars
- Secrets are VPS-only (not in git)
- Use `project/scripts/validate_cicd.sh --vps` to test connectivity

## Key files

- `project/docker-compose.hostinger.prod.yml`
- `project/.env`
- `project/scripts/ops/` (all ops scripts)
- `project/scripts/preflight-prod.sh`

## Required output

- Deploy log with timestamps
- Smoke test results
- PATCHLOG.md entry
- Rollback plan (always)
