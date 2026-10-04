---
name: db-admin
description: >
  Administración de bases de datos — PostgreSQL, MySQL, Redis, SQLite.
  Esquemas, migraciones, índices, performance, backups y replicación.
  Trigger: Cuando necesitás administrar bases de datos, diseñar esquemas, optimizar queries, o configurar replicación.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Skill: db-admin

Bases de datos. Que las queries vuelen y los datos duerman tranquilos.

## Trigger

- Diseñar schema de base de datos
- Una query lenta necesita optimización
- Configurar migraciones (Alembic, Flyway)
- Planificar replicación, clustering o sharding
- Backup y recovery de DB
- Configurar connection pooling

## Workflow LEND

1. ANALIZAR
   ├── Motor: PostgreSQL, MySQL, Redis, SQLite
   ├── Carga: lecturas vs escrituras, volumen de datos, crecimiento
   ├── Estado actual: índices, queries lentas, conexiones, tamaño
   └── Requisitos: ACID, consistencia, disponibilidad, particionado

2. OFRECER (Menú del Senior)
   ├── A) Schema + índices — diseño normalizado, índices correctos, migraciones
   ├── B) Performance — EXPLAIN ANALYZE, índices avanzados (parciales, covering), vacuum, pooling
   └── C) Alta disponibilidad — replicación (streaming/síncrona), failover, clustering, sharding

3. ELEGIR → confirmación

4. HACER
   ├── Schema: normalizado (3FN), tipos correctos, constraints, migraciones con Alembic
   ├── Índices: B-tree para igualdad, GIN para búsqueda, parciales para filtros comunes, EXPLAIN ANALYZE para validar
   ├── Queries: evitar N+1, usar JOINs eficientes, LIMIT, cubrir índices
   ├── Pooling: PgBouncer (PostgreSQL), ProxySQL (MySQL), Connection Pooler SQLAlchemy
   ├── Replicación: streaming replication (PG), Group Replication (MySQL), Sentinel (Redis)
   ├── Mantenimiento: vacuum (PG), optimize (MySQL), VACUUM (SQLite), estadísticas actualizadas
   └── Monitoreo: pg_stat_activity, slow query log, conexiones activas, tamaño por tabla

5. VERIFICAR
   ├── Las queries se ejecutan en tiempo aceptable (< 100ms las críticas)
   ├── Las migraciones corren sin errores (probadas en staging)
   ├── Los backups se completan y se pueden restaurar
   └── La replicación está al día (lag < 1s)
