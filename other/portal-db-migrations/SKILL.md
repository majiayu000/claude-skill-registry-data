---
name: portal-db-migrations
description: Create reversible SQL migrations with dbmate for PostgreSQL 15 + pgvector. Use when adding tables (catalog_source, catalog_field, catalog_tribal_note, app_user, export_job), columns, indexes, extensions, or seed data for the Portal Centralizado de Datos Financieros.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal DB Migrations Skill (dbmate)

Current migrations: `! ls db/migrations/ 2>/dev/null | head -10`

## Rules — NON-NEGOTIABLE

- `make db-new SLUG=x` (dbmate new) para TODO cambio de esquema; archivo `db/migrations/<timestamp>_<slug>.sql`.
- Siempre secciones `-- migrate:up` y `-- migrate:down` (reversible); `db/schema.sql` versionado en git tras cada `make db-up`.
- Jamás editar una migración ya aplicada: se corrige con una migración nueva.
- Jamás `SQLModel.metadata.create_all()` en prod — dbmate es la única vía de cambio de esquema (los modelos SQLModel solo REFLEJAN, ver `portal-db-models`).
- Extensiones vía migración: `CREATE EXTENSION IF NOT EXISTS vector;` (pgvector, fase RAG).
- Timestamps `TIMESTAMPTZ DEFAULT now()`; FKs con `ON DELETE` explícito; unicidad de negocio con `UNIQUE` (respaldan los 409 del API).
- Seeds de demo (usuarios, catálogo) viven en migraciones o en `db/seeds/` invocados por `make data`; contraseñas seed SIEMPRE pre-hasheadas con Argon2 (nunca texto plano en SQL).

## Migraciones canónicas del proyecto

| Orden | Slug | Contenido |
|-------|------|-----------|
| 1 | `create_catalog` | `catalog_source`, `catalog_field`, `catalog_tribal_note` |
| 2 | `create_app_user` | `app_user` + seed 7 usuarios (hashes Argon2) |
| 3 | `create_export_job` | `export_job` con auditoría |
| 4 | `enable_pgvector` | `CREATE EXTENSION vector` + columna `embedding` en `catalog_field` + índice HNSW |

## create_catalog

```sql
-- migrate:up
CREATE TABLE catalog_source (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,               -- 'creditos' | 'liquidez' | 'derivados'
    description TEXT NOT NULL,
    owner_area TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE catalog_field (
    id BIGSERIAL PRIMARY KEY,
    source_id BIGINT NOT NULL REFERENCES catalog_source(id) ON DELETE CASCADE,
    physical_name TEXT NOT NULL,             -- cryptic silo column, e.g. 'sdo_cap'
    business_name TEXT NOT NULL,             -- e.g. 'saldo de capital'
    definition TEXT NOT NULL,
    sensitivity TEXT NOT NULL CHECK (sensitivity IN ('publica', 'interna', 'restringida')),
    metric_agg TEXT CHECK (metric_agg IN ('sum', 'mean', 'count', 'max')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_id, physical_name)
);
CREATE INDEX catalog_field_business_name_idx ON catalog_field
    USING gin (to_tsvector('spanish', business_name || ' ' || definition));

CREATE TABLE catalog_tribal_note (
    id BIGSERIAL PRIMARY KEY,
    field_id BIGINT NOT NULL REFERENCES catalog_field(id) ON DELETE CASCADE,
    note TEXT NOT NULL,                      -- e.g. 'fecha valor es T+1'
    applicability TEXT NOT NULL,             -- Tk-Boost applicability condition
    author TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- migrate:down
DROP TABLE IF EXISTS catalog_tribal_note;
DROP TABLE IF EXISTS catalog_field;
DROP TABLE IF EXISTS catalog_source;
```

## create_app_user (+ seed)

```sql
-- migrate:up
CREATE TABLE app_user (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    hashed_password TEXT NOT NULL,           -- argon2id via pwdlib, never plaintext
    role TEXT NOT NULL CHECK (role IN ('operativo', 'analista', 'directivo', 'admin')),
    disabled BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Seed: 1 admin + 2 por perfil (7 total). Hashes generados con
-- python -c "from pwdlib import PasswordHash; print(PasswordHash.recommended().hash('...'))"
INSERT INTO app_user (username, email, full_name, hashed_password, role) VALUES
    ('admin',       'admin@portal.demo',  'Admin Portal',      '$argon2id$...', 'admin'),
    ('operativo1',  'op1@portal.demo',    'Operativo Uno',     '$argon2id$...', 'operativo'),
    ('operativo2',  'op2@portal.demo',    'Operativo Dos',     '$argon2id$...', 'operativo'),
    ('analista1',   'an1@portal.demo',    'Analista Uno',      '$argon2id$...', 'analista'),
    ('analista2',   'an2@portal.demo',    'Analista Dos',      '$argon2id$...', 'analista'),
    ('directivo1',  'dir1@portal.demo',   'Directivo Uno',     '$argon2id$...', 'directivo'),
    ('directivo2',  'dir2@portal.demo',   'Directivo Dos',     '$argon2id$...', 'directivo');

-- migrate:down
DROP TABLE IF EXISTS app_user;
```

## enable_pgvector (fase RAG)

```sql
-- migrate:up
CREATE EXTENSION IF NOT EXISTS vector;
ALTER TABLE catalog_field ADD COLUMN embedding VECTOR(768);   -- Gemini embedding dim
CREATE INDEX catalog_field_embedding_idx ON catalog_field
    USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);

-- migrate:down
DROP INDEX IF EXISTS catalog_field_embedding_idx;
ALTER TABLE catalog_field DROP COLUMN IF EXISTS embedding;
DROP EXTENSION IF EXISTS vector;
```

## Comandos

```bash
make db-new SLUG=create_catalog    # dbmate new create_catalog
make db-up                         # dbmate up (aplica + regenera schema.sql)
make db-rollback                   # dbmate rollback (última migración)
dbmate status                      # migraciones pendientes/aplicadas
```
