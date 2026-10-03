---
name: portal-data-connectors
description: Implement async Parquet extractors for the financial silos (creditos, liquidez, derivados) with threadpool offloading, in-memory TTL cache, and graceful degradation per silo. Use when writing ml/data/extractors.py, typed silo exceptions, or pytest-asyncio connector tests.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Data Connectors Skill

Silos on disk: `! ls data/silos/ 2>/dev/null || echo "run make data first"`

## Rules — NON-NEGOTIABLE

- Lectura de Parquet SIEMPRE vía `async def` que delega a threadpool (`asyncio.to_thread` / `run_in_executor`); jamás bloquear el event loop con IO Polars síncrono en un handler.
- Graceful degradation por silo: si un silo falla, los demás siguen respondiendo; el error se propaga como excepción tipificada propia (`SiloUnavailableError`), nunca un `Exception` genérico.
- Caché TTL en memoria para lecturas repetitivas; TTL configurable vía Settings (`SILO_CACHE_TTL_SECONDS`, default 300).
- Los extractores devuelven `pl.LazyFrame` (scan, no read completo) para que el compilador semántico decida qué materializar.
- Rutas de silos desde Pydantic Settings (`DATA_SILOS_DIR`), nunca hardcodeadas.
- Pruebas `pytest-asyncio` obligatorias: éxito, silo caído, caché hit/miss (criterio de aceptación del plan).

## Excepciones tipificadas

```python
# ml/data/errors.py
class SiloError(Exception):
    """Base error for silo extraction failures."""
    def __init__(self, silo: str, message: str) -> None:
        self.silo = silo
        super().__init__(f"[{silo}] {message}")

class SiloUnavailableError(SiloError):
    """Silo file missing, corrupt, or unreadable."""

class SiloTimeoutError(SiloError):
    """Extraction exceeded the configured deadline."""
```

## Extractor async con threadpool y caché TTL

```python
# ml/data/extractors.py
import asyncio
import time
import polars as pl
import structlog
from app.core.config import settings
from ml.data.errors import SiloUnavailableError

logger = structlog.get_logger()
SILOS = ("creditos", "liquidez", "derivados")
_cache: dict[str, tuple[float, pl.LazyFrame]] = {}

def _scan_sync(silo: str) -> pl.LazyFrame:
    path = settings.DATA_SILOS_DIR / f"{silo}.parquet"
    if not path.exists():
        raise SiloUnavailableError(silo, f"parquet not found at {path}")
    return pl.scan_parquet(path)


async def get_silo(silo: str) -> pl.LazyFrame:
    """Return a LazyFrame for the silo, offloading IO to a threadpool with TTL cache."""
    if silo not in SILOS:
        raise SiloUnavailableError(silo, "unknown silo")
    now = time.monotonic()
    cached = _cache.get(silo)
    if cached and now - cached[0] < settings.SILO_CACHE_TTL_SECONDS:
        logger.debug("silo_cache_hit", silo=silo)
        return cached[1]
    try:
        lf = await asyncio.to_thread(_scan_sync, silo)
    except SiloUnavailableError:
        raise
    except Exception as exc:  # corrupt file, permission error, etc.
        raise SiloUnavailableError(silo, str(exc)) from exc
    _cache[silo] = (now, lf)
    logger.info("silo_loaded", silo=silo)
    return lf


def invalidate_cache(silo: str | None = None) -> None:
    """Drop cached entries (all silos when silo is None)."""
    if silo is None:
        _cache.clear()
    else:
        _cache.pop(silo, None)
```

## Degradación en el servicio (un silo caído no tumba el resto)

```python
# backend/app/services/semantic_service.py (extracto)
try:
    lf = await get_silo(silo)
except SiloUnavailableError as exc:
    logger.warning("silo_unavailable", silo=exc.silo)
    raise HTTPException(status_code=503,
                        detail={"error": "silo_unavailable", "silo": exc.silo}) from exc
```

## Pruebas pytest-asyncio

```python
# tests/ml/test_extractors.py
import pytest
from ml.data import extractors
from ml.data.errors import SiloUnavailableError

pytestmark = pytest.mark.asyncio


async def test_get_silo_success(synthetic_silos):
    lf = await extractors.get_silo("creditos")
    assert lf.collect_schema().len() > 0


async def test_silo_down_is_typed(monkeypatch, tmp_path):
    monkeypatch.setattr(extractors.settings, "DATA_SILOS_DIR", tmp_path)
    extractors.invalidate_cache()
    with pytest.raises(SiloUnavailableError) as exc:
        await extractors.get_silo("liquidez")
    assert exc.value.silo == "liquidez"


async def test_cache_hit_and_miss(synthetic_silos, monkeypatch):
    extractors.invalidate_cache()
    calls: list[str] = []
    real = extractors._scan_sync
    monkeypatch.setattr(extractors, "_scan_sync", lambda s: calls.append(s) or real(s))
    await extractors.get_silo("derivados")   # miss -> scan
    await extractors.get_silo("derivados")   # hit -> no scan
    assert calls == ["derivados"]
```

## Referencias

| Pieza | Ubicación |
|-------|-----------|
| Extractores async + caché | `ml/data/extractors.py` |
| Errores tipificados | `ml/data/errors.py` |
| Pruebas de conectores | `tests/ml/test_extractors.py` |
| Generadores (upstream) | `ml/data/generators.py` — skill `portal-synthetic-data` |
