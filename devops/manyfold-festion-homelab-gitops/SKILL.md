---
name: manyfold
description: Self-hosted 3D model library manager for organizing, viewing, and managing 3D print files. Use when the user asks about deploying, configuring, or using Manyfold for managing STL/OBJ/3MF collections. Triggers on phrases like "Manyfold", "3D model library", "manage my 3D prints", "self-hosted model manager", "organize STL files", "3D print collection", or any Docker/homelab deployment involving 3D model organization.
---

# Manyfold Skill

Manyfold is a self-hosted web application for managing 3D print file collections with interactive previews, metadata organization, and Fediverse federation support.

## Quick Reference

**Docker Image**: `ghcr.io/manyfold3d/manyfold:latest`
**Default Port**: 3214
**Web UI**: `http://{server}:3214`

## Deployment Options

### Minimal (Solo with SQLite)

```yaml
services:
  manyfold:
    image: ghcr.io/manyfold3d/manyfold-solo:latest
    ports:
      - "3214:3214"
    volumes:
      - /path/to/config:/config
      - /path/to/models:/libraries
    environment:
      SECRET_KEY_BASE: <generate-128-char-hex>
      PUID: 1000
      PGID: 1000
    restart: unless-stopped
```

### Production (PostgreSQL + Redis)

```yaml
services:
  manyfold:
    image: ghcr.io/manyfold3d/manyfold:latest
    ports:
      - "3214:3214"
    volumes:
      - /path/to/models:/libraries
    environment:
      DATABASE_URL: postgresql://manyfold:password@db/manyfold?pool=5
      REDIS_URL: redis://redis:6379/1
      SECRET_KEY_BASE: <generate-128-char-hex>
      PUID: 1000
      PGID: 1000
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - DAC_OVERRIDE
      - SETUID
      - SETGID
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: manyfold
      POSTGRES_PASSWORD: password
      POSTGRES_DB: manyfold

  redis:
    image: redis:7

volumes:
  db_data:
```

## Required Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY_BASE` | 128-char hex string for cookie signing. Generate with `openssl rand -hex 64` |
| `PUID` / `PGID` | User/group ID for file permissions. Get with `id` command |
| `REDIS_URL` | Redis connection (not needed for solo image). Format: `redis://host:6379/1` |

## Database Configuration

**Option 1: DATABASE_URL** (recommended)
- PostgreSQL: `postgresql://user:pass@host/dbname?pool=5`
- MySQL: `mysql2://user:pass@host/dbname?pool=5`
- SQLite: `sqlite3:/config/manyfold.sqlite3?pool=5`

**Option 2: Individual variables**
- `DATABASE_ADAPTER`: postgresql, mysql2, or sqlite3
- `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_NAME`

## Key Optional Features

| Variable | Description |
|----------|-------------|
| `MULTIUSER=enabled` | Enable login, roles, permissions |
| `FEDERATION=enabled` | ActivityPub/Fediverse support |
| `HTTPS_ONLY=enabled` | Force HTTPS, set HSTS headers |
| `DEMO_MODE=enabled` | Disable all destructive operations |

## OIDC Single Sign-On

```
OIDC_CLIENT_ID=<client-id>
OIDC_CLIENT_SECRET=<secret>
OIDC_ISSUER=https://auth.example.com/
OIDC_NAME=Authentik
FORCE_OIDC=enabled  # Optional: disable local login
```

## Email (SMTP)

```
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=user
SMTP_PASSWORD=pass
SMTP_FROM_ADDRESS=manyfold@example.com
PUBLIC_HOSTNAME=manyfold.example.com
```

## Performance Tuning

| Variable | Default | Description |
|----------|---------|-------------|
| `WEB_CONCURRENCY` | 4 | Web worker processes |
| `RAILS_MAX_THREADS` | 16 | Threads per worker |
| `DEFAULT_WORKER_CONCURRENCY` | 4 | Background job threads |
| `PERFORMANCE_WORKER_CONCURRENCY` | 1 | Heavy job threads (analysis, conversion) |

## Security Settings

```
MAX_FILE_UPLOAD_SIZE=536870912    # 512MB in bytes
MAX_FILE_EXTRACT_SIZE=1073741824  # 1GB in bytes
MIN_PASSWORD_SCORE=4              # 0-4, higher = stricter
```

## Core Concepts

- **Library**: Storage location (local folder or S3 bucket) containing models
- **Model**: A folder containing related 3D files (parts, images, docs)
- **Creator**: Content author/designer
- **Collection**: Grouping of related models
- **Tags**: Organizational keywords

## User Workflows

### Initial Setup
1. Access web UI at `http://server:3214`
2. Create admin account (email, username, password)
3. Add first library (path inside container, e.g., `/libraries`)
4. Scan runs automatically to index existing files

### Scanning
- **Scan for new files**: Detect new folders/files added outside Manyfold
- **Rescan all models**: Re-check existing models for problems/metadata

### Uploading
- Upload ZIP archives (extracted as separate models)
- Upload individual STL/OBJ files (creates single model)
- Progress shown during upload, extraction happens in background

### External Integrations (v0.118+)
Import metadata from Thingiverse, MyMiniFactory, Cults3D:
1. Configure API keys in Settings > Integrations
2. Add link to model page
3. Click sync icon to import metadata/images
4. Or paste URL in search bar for direct import

## Supported File Formats

See references/supported_formats.md for complete list.

**3D Models with Preview**: STL, OBJ, 3MF, GLTF/GLB, FBX, PLY, 3DS
**Slicer Files**: GCode (preview), Chitubox, Lychee
**Images**: PNG, JPG, GIF, WebP, SVG, TIFF, BMP
**Documents**: PDF, Markdown, TXT
**Archives**: ZIP, RAR, 7z, gzip, bzip2

## Troubleshooting

### Container won't start
- Ensure `SECRET_KEY_BASE` is set
- Check `PUID`/`PGID` have read/write access to mounted volumes
- Verify Redis is accessible (for full image)

### Files not appearing
- Check library path matches container mount (not host path)
- Run manual scan from web UI
- Verify file extensions are supported

### Permission errors
- Match `PUID`/`PGID` to owner of library folders
- Ensure container has write access for temp files

### Health check
`wget --no-verbose --tries=1 --spider http://localhost:3214/health`

## Reverse Proxy

Set `RAILS_RELATIVE_URL_ROOT=/manyfold` for non-root paths.

Required headers for HTTPS proxy:
- `X-Forwarded-Proto: https`
- `X-Forwarded-For`
- `Host`

**Note**: Federation requires domain root (no subpath).

## Additional References

- Configuration details: references/configuration.md
- All supported formats: references/supported_formats.md
