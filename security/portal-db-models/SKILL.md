---
name: portal-db-models
description: Define SQLModel ORM models mirroring the dbmate schema (app_user, catalog_source, catalog_field, catalog_tribal_note, export_job) with Pydantic request/response types. Use when creating or modifying models, enums, soft-delete logic, or API schemas for the Portal.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal DB Models Skill (SQLModel)

Models dir: `! ls backend/app/models/ 2>/dev/null || echo "no models dir yet"`

## Rules — NON-NEGOTIABLE

- Los modelos SQLModel REFLEJAN el esquema creado por dbmate; NUNCA lo generan: jamás `SQLModel.metadata.create_all()` fuera de fixtures de test aislados. dbmate manda (skill `portal-db-migrations`).
- Patrón de tres clases: `XBase` (campos compartidos, Pydantic) → `X` (`table=True`, ORM) → `XOut`/`XCreate`/`XUpdate` (contratos API). Los routers solo exponen `XOut`.
- Soft delete de usuarios: `disabled = true`; nunca borrado físico (auditoría).
- Campos de auditoría en toda tabla: `created_at: datetime` (`TIMESTAMPTZ` en BD); `export_job` añade `finished_at`, `size_bytes`, `duration_s`.
- `hashed_password` NUNCA aparece en ningún modelo `*Out` ni en logs.
- Roles como `str, enum.Enum` (`operativo | analista | directivo | admin`) — mismos literales que los scopes JWT.
- Sesión async con `sqlalchemy.ext.asyncio`; type hints y docstrings Google-style en inglés.

## Rol y usuario (app_user)

```python
# backend/app/models/user.py
import enum
import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field

class Role(str, enum.Enum):
    operativo = "operativo"
    analista = "analista"
    directivo = "directivo"
    admin = "admin"

class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, max_length=64)
    email: str = Field(unique=True, max_length=255)
    full_name: str = Field(max_length=255)
    role: Role
    disabled: bool = False

class AppUser(UserBase, table=True):
    __tablename__ = "app_user"
    id: uuid.UUID | None = Field(default=None, primary_key=True)
    hashed_password: str                      # argon2id, never serialized out
    created_at: datetime | None = Field(default=None)

class UserOut(UserBase):
    id: uuid.UUID
    created_at: datetime                      # no hashed_password, by design

class UserCreate(SQLModel):
    username: str
    email: str
    full_name: str
    role: Role
    password: str = Field(min_length=12)      # hashed in service, never stored raw

class UserUpdate(SQLModel):                   # all optional: email, full_name, role, password
    email: str | None = None
    full_name: str | None = None
    role: Role | None = None
    password: str | None = None
```

## Catálogo (source, field, tribal note)

```python
# backend/app/models/catalog.py
class CatalogSource(SQLModel, table=True):
    __tablename__ = "catalog_source"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)            # creditos | liquidez | derivados
    description: str
    owner_area: str
    created_at: datetime | None = None

class CatalogField(SQLModel, table=True):
    __tablename__ = "catalog_field"
    id: int | None = Field(default=None, primary_key=True)
    source_id: int = Field(foreign_key="catalog_source.id", index=True)
    physical_name: str                        # cryptic silo column
    business_name: str
    definition: str
    sensitivity: str                          # publica | interna | restringida
    metric_agg: str | None = None             # sum | mean | count | max
    embedding: list[float] | None = Field(    # pgvector, RAG phase
        default=None, sa_column=Column(Vector(768)))
    created_at: datetime | None = None

class CatalogTribalNote(SQLModel, table=True):
    __tablename__ = "catalog_tribal_note"
    id: int | None = Field(default=None, primary_key=True)
    field_id: int = Field(foreign_key="catalog_field.id", index=True)
    note: str
    applicability: str                        # Tk-Boost applicability condition
    author: str
    created_at: datetime | None = None

class CatalogHit(SQLModel):
    """API response contract for /api/catalog/search."""
    business_name: str
    definition: str
    source: str
    physical_name: str
    tribal_notes: list[str] = []
    score: float
```

## Export job

```python
# backend/app/models/export.py
class ExportJob(SQLModel, table=True):
    __tablename__ = "export_job"
    id: uuid.UUID | None = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="app_user.id", index=True)
    query: dict = Field(sa_column=Column(JSONB, nullable=False))   # SemanticQuery dump
    format: str                               # csv | xlsx
    status: str = "queued"                    # queued | running | done | failed
    signed_url: str | None = None
    size_bytes: int | None = None
    duration_s: float | None = None
    error: str | None = None
    created_at: datetime | None = None
    finished_at: datetime | None = None

class ExportJobOut(SQLModel):
    id: uuid.UUID
    status: str
    format: str
    signed_url: str | None = None
    created_at: datetime
    finished_at: datetime | None = None
```
