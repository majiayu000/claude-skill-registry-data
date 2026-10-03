---
name: portal-backend-api
description: Create or modify FastAPI routers, endpoints, and SSE handlers for the Portal Centralizado de Datos Financieros. Use when adding endpoints (/api/auth/token, /api/users, /api/catalog/search, /api/creditos, /api/liquidez, /api/derivados, /api/export, /api/chat SSE), implementing handlers, or wiring routers into the app.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Backend API Skill

Current branch: `! git branch --show-current`
Existing routers: `! ls backend/app/api/ 2>/dev/null || echo "no api dir found"`

## Rules — NON-NEGOTIABLE

- Todo endpoint de datos exige `Security(get_current_user, scopes=[...])`; 401 sin token (`WWW-Authenticate: Bearer`), 403 autenticado sin permiso (skill `portal-auth-jwt`).
- Router recibe → Service procesa → Model persiste. Cero lógica de negocio en routers.
- Respuestas SIEMPRE con modelos Pydantic (`response_model=`); nunca SQLModel crudo ni DataFrames serializados a mano.
- Errores tipificados: métrica/dimensión inexistente → 422 con sugerencias fuzzy del catálogo; `username`/`email` duplicado → 409; silo caído → 503 parcial tipificado.
- `/api/chat` devuelve `StreamingResponse(media_type="text/event-stream")` con eventos `tool_call`, `token`, `error`, `done`; desconexión del cliente cancela la llamada LLM.
- Contraseñas y prompts crudos jamás en respuestas ni logs; logging con `structlog.get_logger()`, nunca `print()`.
- Type hints obligatorios; docstrings Google-style en inglés.

## Endpoints Canónicos

| Method | Path | Scope mínimo | Skill complementaria |
|--------|------|--------------|----------------------|
| GET  | `/healthz` | público | — |
| POST | `/api/auth/token` | público (OAuth2 password) | `portal-auth-jwt` |
| GET/POST | `/api/users` | `admin` | `portal-auth-jwt` |
| GET/PATCH/DELETE | `/api/users/{id}` | `admin` | `portal-auth-jwt` |
| GET  | `/api/catalog/search` | autenticado (cualquier rol) | `portal-catalog-rag` |
| POST | `/api/creditos` | `operativo`+ (puntual) / `analista`+ (agregación) | `portal-semantic-layer` |
| POST | `/api/liquidez` | `operativo`+ / `analista`+ | `portal-semantic-layer` |
| POST | `/api/derivados` | `operativo`+ / `analista`+ | `portal-semantic-layer` |
| POST | `/api/export` | `analista`+ | `portal-export-jobs` |
| GET  | `/api/export/{job_id}` | `analista`+ (dueño del job) | `portal-export-jobs` |
| POST | `/api/chat` SSE | autenticado; tools heredan el Bearer | `portal-auth-jwt` |

## Router de dominio (capa semántica)

```python
# backend/app/api/creditos.py
from fastapi import APIRouter, Security
from app.core.auth import get_current_user
from app.models.user import UserOut
from app.models.semantic import SemanticQuery, SemanticResult
from app.services.semantic_service import SemanticService

router = APIRouter(prefix="/creditos", tags=["creditos"])


@router.post("", response_model=SemanticResult)
async def query_creditos(
    body: SemanticQuery,
    current_user: UserOut = Security(get_current_user, scopes=["operativo"]),
) -> SemanticResult:
    """Run a governed semantic query against the creditos silo."""
    return await SemanticService.run(silo="creditos", query=body, user=current_user)
```

Agregaciones y cruces exigen scope superior dentro del service (no duplicar routers):
`SemanticService` eleva a 403 si `query.is_aggregation` y el rol es solo `operativo`.

## Chat SSE con cancelacion real

```python
# backend/app/api/chat.py
from fastapi import APIRouter, Request, Security
from fastapi.responses import StreamingResponse
from app.core.auth import get_current_user, oauth2_scheme
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_class=StreamingResponse)
async def chat(
    request: Request,
    body: ChatRequest,
    current_user: UserOut = Security(get_current_user, scopes=[]),
) -> StreamingResponse:
    """Stream ADK agent events; client disconnect cancels the LLM call."""
    bearer = request.headers["authorization"].removeprefix("Bearer ").strip()

    async def event_stream():
        async for event in ChatService.run(body=body, user=current_user, bearer=bearer):
            if await request.is_disconnected():
                await ChatService.cancel(body.session_id)
                break
            yield f"event: {event.type}\ndata: {event.model_dump_json()}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

## Errores tipificados 422 (fuzzy match del catálogo)

```python
# backend/app/services/semantic_service.py (extracto)
from app.utils.errors import UnknownMetricError

try:
    plan = compile_query(query, catalog)
except UnknownMetricError as exc:
    raise HTTPException(
        status_code=422,
        detail={
            "error": "unknown_metric",
            "metric": exc.metric,
            "suggestions": catalog.fuzzy_match(exc.metric, top_k=3),
        },
    ) from exc
```

## Registro de routers

```python
# backend/app/main.py
from app.api import auth, users, catalog, creditos, liquidez, derivados, export, chat

for r in (auth.router, users.router, catalog.router, creditos.router,
          liquidez.router, derivados.router, export.router, chat.router):
    app.include_router(r, prefix="/api")
```

## Logging estructurado

```python
import structlog
logger = structlog.get_logger()
logger.info("semantic_query", silo="creditos", user_id=current_user.id,
            metric=body.metric, row_count=result.row_count)
# NUNCA loggear body completo del chat ni contraseñas; prompts solo como llm.prompt_hash
```
