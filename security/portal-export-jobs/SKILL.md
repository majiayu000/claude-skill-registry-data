---
name: portal-export-jobs
description: Implement background export jobs — POST /api/export returns job_id immediately, BackgroundTasks run Polars joins, serialize CSV/XLSX, upload to GCS with 24h signed URLs, track state in the export_job table. Use when touching export endpoints, the export worker, GCS lifecycle, or the non-blocking concurrency test.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Export Jobs Skill

Export module: `! ls backend/app/services/export_service.py 2>/dev/null || echo "not created yet"`

## Rules — NON-NEGOTIABLE

- `POST /api/export` (scope `analista`+) valida la solicitud y responde INMEDIATAMENTE con `job_id`; el trabajo pesado corre en `BackgroundTasks`, nunca en el request.
- Estados del job: `queued | running | done | failed` — persistidos en la tabla `export_job` (migración dbmate, skill `portal-db-migrations`); el frontend hace polling a `GET /api/export/{job_id}`.
- Archivo final a GCS bajo `exports/{user}/{job_id}.{ext}` con signed URL de expiración 24 h; el bucket tiene lifecycle de 7 días (Terraform en `infra/`).
- Auditoría obligatoria en `export_job`: usuario, filtros solicitados, tamaño, duración.
- Un usuario solo consulta SUS jobs (dueño o `admin`); job ajeno → 403.
- La consulta a exportar pasa por la capa semántica (`SemanticQuery`); jamás filtros libres.
- Prueba de no-bloqueo obligatoria: durante un export de 1 M filas, `GET /api/catalog/search` responde < 500 ms.

## Endpoints

```python
# backend/app/api/export.py
from fastapi import APIRouter, BackgroundTasks, HTTPException, Security
from app.core.auth import get_current_user
from app.models.export import ExportRequest, ExportJobOut
from app.services.export_service import ExportService

router = APIRouter(prefix="/export", tags=["export"])


@router.post("", response_model=ExportJobOut, status_code=202)
async def create_export(
    body: ExportRequest,                       # SemanticQuery + format: csv|xlsx
    background_tasks: BackgroundTasks,
    current_user: UserOut = Security(get_current_user, scopes=["analista"]),
) -> ExportJobOut:
    """Register the job, schedule the worker, and return job_id immediately."""
    job = await ExportService.create_job(user=current_user, request=body)
    background_tasks.add_task(ExportService.run_job, job.id)
    return job                                  # status="queued"


@router.get("/{job_id}", response_model=ExportJobOut)
async def get_export(
    job_id: str,
    current_user: UserOut = Security(get_current_user, scopes=["analista"]),
) -> ExportJobOut:
    job = await ExportService.get_job(job_id)
    if job is None:
        raise HTTPException(404, "Job not found")
    if job.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "Access denied")
    return job                                  # includes signed_url when done
```

## Worker (BackgroundTasks + Polars + GCS)

```python
# backend/app/services/export_service.py (extracto)
import time
import polars as pl
from datetime import timedelta
from google.cloud import storage

@classmethod
async def run_job(cls, job_id: str) -> None:
    job = await cls._mark(job_id, status="running")
    start = time.monotonic()
    try:
        lf = await SemanticService.plan(job.query)          # semantic layer, lazy
        df = await asyncio.to_thread(lf.collect)            # heavy work off the loop
        local = settings.SCRATCH_DIR / f"{job_id}.{job.format}"
        if job.format == "csv":
            df.write_csv(local)
        else:
            df.write_excel(local)                           # polars xlsx writer
        url = await asyncio.to_thread(cls._upload_signed, job, local)
        await cls._mark(job_id, status="done", signed_url=url,
                        size_bytes=local.stat().st_size,
                        duration_s=time.monotonic() - start)
    except Exception as exc:
        logger.error("export_failed", job_id=job_id, error=str(exc))
        await cls._mark(job_id, status="failed", error=type(exc).__name__)

@classmethod
def _upload_signed(cls, job, local) -> str:
    blob = storage.Client().bucket(settings.GCS_EXPORTS_BUCKET).blob(
        f"exports/{job.user_id}/{job.id}.{job.format}")
    blob.upload_from_filename(local)
    return blob.generate_signed_url(version="v4", expiration=timedelta(hours=24))
```

## Migración `export_job` (referencia — detalle en `portal-db-migrations`)

```sql
-- migrate:up
CREATE TABLE export_job (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES app_user(id) ON DELETE RESTRICT,
    query JSONB NOT NULL,
    format TEXT NOT NULL CHECK (format IN ('csv', 'xlsx')),
    status TEXT NOT NULL DEFAULT 'queued'
        CHECK (status IN ('queued', 'running', 'done', 'failed')),
    signed_url TEXT,
    size_bytes BIGINT,
    duration_s REAL,
    error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at TIMESTAMPTZ
);
CREATE INDEX export_job_user_id_idx ON export_job(user_id);
-- migrate:down
DROP TABLE IF EXISTS export_job;
```

## Prueba de no-bloqueo

```python
# tests/backend/test_export_nonblocking.py
async def test_catalog_responds_during_heavy_export(client, analyst_token, big_export_body):
    await client.post("/api/export", json=big_export_body,          # ~1M rows
                      headers=analyst_token)
    t0 = time.perf_counter()
    r = await client.get("/api/catalog/search", params={"q": "saldo"},
                         headers=analyst_token)
    assert r.status_code == 200
    assert time.perf_counter() - t0 < 0.5      # < 500 ms while export runs
```

## Estados y contrato

| Estado | Significado | Campos poblados |
|--------|-------------|-----------------|
| `queued` | Job registrado, worker no iniciado | `id`, `created_at` |
| `running` | Worker ejecutando joins/serialización | — |
| `done` | Archivo en GCS | `signed_url`, `size_bytes`, `duration_s`, `finished_at` |
| `failed` | Error tipificado registrado | `error`, `finished_at` |
