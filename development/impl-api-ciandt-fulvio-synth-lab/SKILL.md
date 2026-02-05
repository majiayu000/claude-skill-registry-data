---
name: impl-api
description: Implementar routers e schemas da API em api/. Use quando criar endpoint, rota, schema de request/response, ou registrar router.
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# Implementar API (Camada de Routers e Schemas)

## Regras Arquiteturais (NON-NEGOTIABLE)

1. **Router SÓ faz**: `request → service.method() → response`
2. **SEM lógica de negócio** em routers (validações, cálculos, etc.)
3. **SEM prompts de LLM** em routers
4. **SEM acesso direto** a banco de dados
5. **Service via getter**: instanciar service em função getter com DI pattern
6. **Response models**: sempre especificar `response_model=` nos endpoints
7. **Schemas separados**: request/response em `api/schemas/`

## Estrutura de Arquivos

```
src/synth_lab/api/
├── main.py                   # App FastAPI, lifespan, middleware
├── errors.py                 # Exception handlers
├── routers/
│   └── {entities}.py         # Um arquivo por recurso (plural)
└── schemas/
    └── {entity}.py           # Schemas por entidade
```

**Convenções de nome:**
- Router: `{entities}.py` (plural: `synths.py`, `experiments.py`)
- Schema: `{entity}.py` (singular)
- Sufixos de schema:
  - `Create` - request de criação
  - `Update` - request de atualização
  - `Summary` - resposta resumida (listas)
  - `Detail` - resposta completa

## Padrões de Código

### Router

```python
"""
{Entity} router for synth-lab API.

Endpoints for {entity} operations.
"""

from fastapi import APIRouter, HTTPException, Path, Query

from synth_lab.api.schemas.{entity} import (
    {Entity}Create,
    {Entity}Detail,
    {Entity}Summary,
)
from synth_lab.models.pagination import PaginatedResponse, PaginationParams
from synth_lab.services.{entity}_service import {Entity}Service


router = APIRouter()


def get_{entity}_service() -> {Entity}Service:
    """Get {entity} service instance (DI pattern)."""
    return {Entity}Service()


@router.get("/list", response_model=PaginatedResponse[{Entity}Summary])
async def list_{entities}(
    limit: int = Query(default=50, ge=1, le=200, description="Items per page"),
    offset: int = Query(default=0, ge=0, description="Items to skip"),
    sort_by: str | None = Query(default=None, description="Sort field"),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
) -> PaginatedResponse[{Entity}Summary]:
    """List {entities} with pagination."""
    service = get_{entity}_service()
    params = PaginationParams(
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return service.list_{entities}(params)


@router.get("/{{{entity}_id}}", response_model={Entity}Detail)
async def get_{entity}(
    {entity}_id: str = Path(..., description="{Entity} ID"),
) -> {Entity}Detail:
    """Get {entity} by ID."""
    service = get_{entity}_service()
    return service.get_{entity}({entity}_id)


@router.post("/", response_model={Entity}Detail, status_code=201)
async def create_{entity}(
    data: {Entity}Create,
) -> {Entity}Detail:
    """Create new {entity}."""
    service = get_{entity}_service()
    return service.create_{entity}(
        name=data.name,
        description=data.description,
    )


@router.delete("/{{{entity}_id}}", status_code=204)
async def delete_{entity}(
    {entity}_id: str = Path(..., description="{Entity} ID"),
) -> None:
    """Delete {entity} by ID."""
    service = get_{entity}_service()
    service.delete_{entity}({entity}_id)
```

### Schemas

```python
"""
{Entity} schemas for API request/response.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class {Entity}Create(BaseModel):
    """Schema for creating a new {entity}."""

    name: str = Field(..., min_length=1, max_length=100, description="Name")
    description: str | None = Field(default=None, max_length=500)


class {Entity}Update(BaseModel):
    """Schema for updating an {entity}."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class {Entity}Summary(BaseModel):
    """Summary for list responses."""

    id: str = Field(..., description="{Entity} ID")
    name: str = Field(..., description="Name")
    created_at: datetime = Field(..., description="Creation timestamp")


class {Entity}Detail({Entity}Summary):
    """Full details for single item responses."""

    description: str | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    # Nested models
    metadata: dict | None = Field(default=None)
```

### Registrar Router em main.py

```python
# Em api/main.py

from synth_lab.api.routers import {entities}

# Registrar router
app.include_router(
    {entities}.router,
    prefix="/{entities}",
    tags=["{entities}"],
)
```

### Exception Handlers (api/errors.py)

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from synth_lab.services.errors import NotFoundError, ValidationError


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers."""

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content={"error": {"code": exc.code, "message": exc.message}},
        )

    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content={"error": {"code": exc.code, "message": exc.message}},
        )
```

## Checklist de Verificação

Antes de finalizar, verificar:

- [ ] Router só faz `request → service → response`
- [ ] SEM lógica de negócio no router
- [ ] Service instanciado via getter function
- [ ] `response_model=` em todos os endpoints
- [ ] Schemas em arquivo separado (`api/schemas/`)
- [ ] Schemas usam sufixos corretos (Create, Summary, Detail)
- [ ] Query/Path validators com descriptions
- [ ] Router registrado em `main.py` com prefix e tags
- [ ] Exception handlers para erros de domínio
- [ ] Docstrings em todos os endpoints
