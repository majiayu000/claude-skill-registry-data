---
name: portal-testing
description: Write pytest + pytest-asyncio backend tests and Vue Test Utils/vitest frontend tests for the Portal Centralizado de Datos Financieros — connectors, auth/RBAC 401/403 matrix, semantic layer reference queries, export non-blocking, SSE cancellation, post-deploy smoke tests, TTFT/P90 measurement. Use when writing or running any test.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Testing Skill

## Rules — NON-NEGOTIABLE

- Cobertura ≥70% backend (auth, capa semántica, export), ≥50% frontend (componentes críticos con Vue Test Utils/vitest).
- Datos SIEMPRE de la semilla fija (`make data`): las 10 consultas de referencia de la capa semántica tienen resultados esperados deterministas.
- Sin llamadas reales a Gemini en tests: mock del gateway LLM y de las tools ADK.
- Pruebas de permisos parametrizadas por rol (los 4 scopes): 401 sin/mal token, 403 autenticado sin permiso.
- Cancelación SSE probada: cortar el stream a mitad NO deja tareas colgadas (cleanup de generadores verificado).
- Smoke tests post-deploy en el pipeline: login, catálogo, consulta semántica, chat con tool call, export.

## Conectores async

```python
# backend/tests/test_extractors.py
import pytest

@pytest.mark.asyncio
async def test_read_silo_ok(seeded_silos):
    df = await read_silo("creditos")
    assert df.height > 0

@pytest.mark.asyncio
async def test_silo_down_graceful_degradation(monkeypatch):
    monkeypatch.setattr("ml.data.extractors._read_parquet", _raise_io_error)
    with pytest.raises(SiloUnavailableError):     # error tipificado, no crash global
        await read_silo("derivados")
    assert (await read_silo("liquidez")).height > 0   # los demas silos siguen vivos

@pytest.mark.asyncio
async def test_cache_hit(seeded_silos, freeze_ttl):
    first = await read_silo("creditos")
    second = await read_silo("creditos")           # dentro del TTL: no relee disco
    assert second is first
```

## Matriz de permisos

```python
# backend/tests/test_auth.py
MATRIX = [
    ("/api/catalog/search", "operativo", 200),
    ("/api/export", "operativo", 403),        # export exige analista+
    ("/api/export", "analista", 202),
    ("/api/users", "directivo", 403),         # usuarios solo admin
    ("/api/users", "admin", 200),
]

@pytest.mark.parametrize("path,role,expected", MATRIX)
@pytest.mark.asyncio
async def test_permission_matrix(client, token_for, path, role, expected):
    r = await client.get(path, headers={"Authorization": f"Bearer {token_for(role)}"})
    assert r.status_code == expected

@pytest.mark.asyncio
async def test_401_variants(client, expired_token):
    assert (await client.get("/api/catalog/search")).status_code == 401
    r = await client.get("/api/catalog/search",
                         headers={"Authorization": f"Bearer {expired_token}"})
    assert r.status_code == 401 and r.headers["WWW-Authenticate"] == "Bearer"
```

Cubrir también: login ok / credenciales malas, admin no puede auto-degradarse (400/409), duplicados → 409.

## Capa semántica, export y SSE

```python
# 10 consultas de referencia (Anexo C) sobre semilla fija
@pytest.mark.parametrize("case", load_reference_queries())   # tests/data/reference_queries.json
@pytest.mark.asyncio
async def test_reference_query(client, analyst_headers, case):
    r = await client.post(f"/api/{case['silo']}", json=case["query"], headers=analyst_headers)
    assert r.json()["rows"] == case["expected_rows"]

# Export no bloquea
@pytest.mark.asyncio
async def test_catalog_responds_during_export(client, analyst_headers):
    job = await client.post("/api/export", json=BIG_EXPORT, headers=analyst_headers)
    t0 = time.monotonic()
    r = await client.get("/api/catalog/search?q=liquidez", headers=analyst_headers)
    assert r.status_code == 200 and time.monotonic() - t0 < 0.5   # < 500 ms

# Cancelacion SSE sin tareas colgadas
@pytest.mark.asyncio
async def test_sse_cancellation_cleanup(client, user_headers):
    async with client.stream("POST", "/api/chat", json=Q, headers=user_headers) as s:
        await anext(s.aiter_lines())   # primer evento recibido
    await asyncio.sleep(0.1)           # desconexion simulada al salir del context
    assert not [t for t in asyncio.all_tasks() if "agent_run" in repr(t)]
```

## Frontend (vitest + Vue Test Utils)

Componentes críticos: tarjeta de tool call (estados anuncio/ejecución/resultado/error), login, tabla admin de usuarios. `mount()` con Pinia de prueba; asserts sobre estados renderizados, no sobre internals.

## Smoke tests y medición TTFT

```bash
make test                       # pytest con cobertura + vitest
pytest tests/smoke/ --base-url "$CLOUD_RUN_URL"   # post-deploy: login, catalogo,
                                                  # consulta semantica, chat tool call, export
python scripts/measure_ttft.py --runs 50          # >=50 corridas -> p50/p90 percentiles
```

`measure_ttft.py`: abre el stream SSE, cronometra hasta el primer evento `token`, repite ≥50 veces y reporta p50/p90 (objetivos: TTFT p50 < 700 ms, P90 consulta completa < 15 s). Resultados documentados para A5.

## QA Checklist

- [ ] Cobertura ≥70% backend / ≥50% frontend
- [ ] Matriz 401/403 parametrizada por los 4 roles en verde
- [ ] 10 consultas de referencia deterministas sobre semilla fija
- [ ] Export no-bloqueo < 500 ms verificado
- [ ] Cancelación SSE sin tareas colgadas
- [ ] Mocks para Gemini/ADK (cero llamadas reales)
- [ ] Smoke tests verdes en el pipeline post-deploy
- [ ] TTFT/P90 medidos con ≥50 corridas y documentados
