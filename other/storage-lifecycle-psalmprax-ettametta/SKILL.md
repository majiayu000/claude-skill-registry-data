---
name: storage-lifecycle
description: Debug and troubleshoot ettametta's storage system — local/S3 provider, lifecycle management, disk threshold enforcement, and cloud migration. Use when uploads fail, disk fills up, or cloud migration stalls.
---

# Storage & Lifecycle Debugging

The storage service manages file uploads (local or S3-compatible), disk threshold enforcement, and automatic cloud migration of old outputs.

## Quick Diagnostics

```bash
# Disk usage for outputs
ls -la data/storage/outputs/ | head -20
du -sh data/storage/outputs/

# Storage stats via API
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/analytics/stats/storage

# Check storage provider setting
docker compose exec api python3 -c "from src.api.config import settings; print('PROVIDER:', settings.STORAGE_PROVIDER)"

# Check lifecycle task
celery -A src.api.utils.celery inspect active | grep lifecycle

# S3 connectivity (if cloud)
docker compose exec api python3 -c "
from src.services.storage.service import base_storage_service
print('Provider:', base_storage_service.provider)
"
```

## Architecture

### StorageService (`src/services/storage/service.py`)

Singleton: `base_storage_service`

Provider selection is runtime via `storage_provider` setting (default `"LOCAL"`):
- **LOCAL** — files in `data/storage/outputs/`, URLs as `/static/outputs/{filename}`
- **S3-compatible** — boto3 client, supports AWS/OCI/GCP/Azure/custom endpoints, presigned URLs

Key methods:
- `upload_file(path, filename)` → local path or S3 key
- `upload_to_cloud(path, filename)` → forces cloud regardless of provider
- `get_file_url(filename)` → presigned URL (cloud) or static URL (local)

### StorageManager (`src/services/storage/manager.py`)

Lifecycle logic:
- `enforce_threshold()` — migrates oldest files to cloud until disk usage ≤ 80% of 140 GB threshold
- `apply_retention_policy(days=90)` — deletes cloud objects older than 90 days
- Migration updates `VideoJobDB.output_path`, `NexusJobDB.output_path`, `ScheduledPostDB.video_path` in DB, then deletes local file

### Celery Task

`storage.manage_lifecycle` — runs daily. Calls `enforce_threshold()` then `apply_retention_policy()`.

### Key Files

| File | Purpose |
|------|---------|
| `src/services/storage/service.py` | `StorageService` — upload, download, provider abstraction |
| `src/services/storage/manager.py` | `StorageManager` — threshold, migration, retention |
| `src/services/storage/tasks.py` | Celery task for daily lifecycle management |
| `src/api/routes/analytics.py` | `GET /stats/storage` endpoint |

## Configuration

| Setting | Default | Purpose |
|---------|---------|---------|
| `STORAGE_PROVIDER` | `LOCAL` | Provider: AWS, OCI, GCP, AZURE, CUSTOM, LOCAL |
| `STORAGE_ENDPOINT` | — | S3-compatible endpoint URL |
| `STORAGE_BUCKET` | — | S3 bucket name |
| `STORAGE_ACCESS_KEY` | — | S3 access key (vault fallback) |
| `STORAGE_SECRET_KEY` | — | S3 secret key (vault fallback) |
| `STORAGE_REGION` | — | S3 region |
| `STORAGE_OUTPUT_DIR` | `data/storage/outputs` | Local output directory |
| `REMOTE_STORAGE_OUTPUT_DIR` | `/workspace/outputs` | Container output directory |

## Common Issues

### Disk full / threshold not enforced
Lifecycle task runs daily. Check if Celery beat is running:
```bash
celery -A src.api.utils.celery inspect scheduled | grep lifecycle
```
Threshold is 80% of 140 GB. Check current usage:
```bash
du -sh data/storage/outputs/
```

### Upload fails for LOCAL provider
Check directory permissions:
```bash
ls -la data/storage/outputs/
docker compose exec api id  # should be appuser (non-root)
```
Note: compose sets `user: "0:0"` (root), which overrides the Dockerfile's `appuser`.

### S3 upload fails
Check credentials:
```bash
docker compose exec api python3 -c "
from src.api.config import settings
print('Endpoint:', settings.STORAGE_ENDPOINT)
print('Bucket:', settings.STORAGE_BUCKET)
print('Key:', 'SET' if settings.STORAGE_ACCESS_KEY else 'MISSING')
"
```

### Cloud migration not updating DB paths
`StorageManager` updates three tables: `VideoJobDB`, `NexusJobDB`, `ScheduledPostDB`. If a new table stores output paths, it won't be migrated. Check `manager.py` for the hardcoded table list.

### Retention policy too aggressive
Default is 90 days. Cloud objects older than this are deleted. Check:
```bash
docker compose exec api python3 -c "
from src.services.storage.manager import StorageManager
m = StorageManager()
print('Retention days:', m.RETENTION_DAYS)
"
```

### presigned URLs expired
S3 presigned URLs have a default TTL. If shared links break, the URL was cached past expiry. `get_file_url()` generates fresh URLs on each call.

## Integration Points

| Caller | How it uses storage |
|--------|---------------------|
| Video engine tasks | `upload_file()` for rendered videos + thumbnails |
| Nexus engine | `upload_file()` for thumbnails |
| Analytics route | `GET /stats/storage` reads disk usage |
| Video preview route | Reads directly from `data/storage/outputs/` |

## Debugging Checklist

1. Provider: `settings.STORAGE_PROVIDER`
2. Disk usage: `du -sh data/storage/outputs/`
3. Threshold: 80% of 140 GB
4. Lifecycle task: `celery inspect active | grep lifecycle`
5. S3 credentials: `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`
6. Upload test: `curl -X POST /api/v1/video/upload` with a small file
7. Migration DB updates: check `output_path` columns in video/nexus/schedule tables
