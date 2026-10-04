---
name: flyway-migration-checker
description: Verifica que una migración Flyway de Runcriticon sea compatible hacia atrás (deploy-then-migrate, ADR-0010 D11), siga la convención de nombres y carpeta por módulo, declare la categoría RGPD de cada tabla nueva, y respete las reglas de persistencia (esquema por módulo, sin FK cruzado, club_id indexado). Usar antes de mergear una PR con migraciones SQL.
---

# Flyway Migration Checker — Runcriticon

Verifica una migración Flyway contra las reglas de [`docs/arquitectura/persistencia.md`](../../../docs/arquitectura/persistencia.md) y ADR-0010 D11 (compatibilidad hacia atrás). Cruce: ADR-0004 D4, ADR-0014 D5.

## Cuándo usar

Antes de mergear cualquier PR que añade o modifica un archivo en `backend/src/main/resources/db/migration/{modulo}/`.

## Argumentos

```
/flyway-migration-checker                          # revisa todas las migraciones del diff vs main
/flyway-migration-checker planificacion/V202606010300__crea_plan.sql
```

## Checklist de verificación

### Bloque A — Convención de nombres y ubicación (ADR-0004 D4, D9)

> **Historial único**: Flyway aplica las seis carpetas desde un solo `public.flyway_schema_history`, así que la **secuencia de versiones es global entre módulos**, no por carpeta (ADR-0004 D9).

- [ ] ¿Está en `db/migration/{modulo}/` (carpeta por módulo, no carpeta única)?
- [ ] ¿El nombre sigue `V{YYYYMMDD}{NNNN}__descripcion_snake.sql` (fecha + secuencia de 4 dígitos)?
- [ ] ¿La versión es **única en todas las carpetas** de `db/migration/`? (`ls backend/src/main/resources/db/migration/*/V{YYYYMMDD}*` — dos ficheros con la misma versión en carpetas distintas chocan igual).
- [ ] ¿La versión es **mayor que la máxima presente en `main`**? Sin `out-of-order`, una versión menor que la última aplicada falla la validación de Flyway al arrancar en `staging`/producción, y el test de CI desde cero **no** lo detecta. Si `main` avanzó, renombrar al rebasar.
- [ ] ¿La descripción usa verbos claros (`crea_`, `anade_`, `migra_`)?

### Bloque B — Esquema por módulo (ADR-0004 D4)

> **Nombre canónico del esquema**: el `{modulo}` en `CREATE SCHEMA` y en las tablas es el **nombre canónico DB**, que puede diferir del paquete Java. Para los módulos del MVP: `club` → `club_taxonomia`, `salud` → `seguimiento` (los otros tres coinciden). Si la migración usa el nombre del paquete en vez del canónico, es un error bloqueante.

- [ ] ¿`CREATE SCHEMA IF NOT EXISTS {esquema_canonico}` si es la primera migración del módulo?
- [ ] ¿Todas las tablas viven en el esquema canónico del módulo (`{esquema_canonico}.{tabla}`)?
- [ ] ¿**Ninguna FK cruza esquemas**? (referencias entre módulos = UUID sin FK)
- [ ] ¿Ninguna consulta/JOIN cruza esquemas?

### Bloque C — Categoría RGPD (ADR-0014 D5)

- [ ] ¿Cada `CREATE TABLE` lleva un **comentario** que declara su categoría RGPD (1-6) y su política de borrado/retención?
- [ ] Si la tabla es categoría 1 (PII primaria): ¿el módulo tiene `StudentDeletionListener`? (cruce rgpd-en-modulos.md §3)
- [ ] Si es categoría 2/3 (auditoría): ¿hay job de purga programado? (cruce persistencia.md §12)

### Bloque D — Tipos y constraints (persistencia.md §3-§5)

- [ ] ¿IDs como `UUID` (generados en aplicación, no `gen_random_uuid()` server-side)?
- [ ] ¿Fechas como `TIMESTAMPTZ` (nunca `TIMESTAMP` sin zona)?
- [ ] ¿`JSONB` solo para value objects con shape variable, con `CHECK` contra estructura?
- [ ] ¿Enums como `VARCHAR(N) CHECK (col IN (...))`, no `ENUM` nativo?
- [ ] ¿Índice por `club_id` en cada tabla de dominio (ADR-0006 D22, ADR-0009 D4)?
- [ ] ¿Constraints universales (`NOT NULL`, `CHECK`, `UNIQUE` compuesto)?
- [ ] Si crea proyección local: ¿tiene `last_processed_event_id` + `last_processed_event_ts`? (ADR-0009 D9)
- [ ] Si el módulo consume eventos: ¿tiene tabla `{modulo}.evento_procesado(listener, event_id)`? (ADR-0007 D9)

### Bloque E — Compatibilidad hacia atrás (ADR-0010 D11) — EL CRÍTICO

La regla **deploy-then-migrate**: la versión nueva de la app debe poder correr con el esquema viejo Y el nuevo. Detectar operaciones **breaking**:

- [ ] ❌ `DROP COLUMN` de una columna que la app actual aún lee → hacer en dos pasos.
- [ ] ❌ `ALTER COLUMN ... SET NOT NULL` sobre columna existente sin default → romper si hay filas null o inserts sin el campo.
- [ ] ❌ `RENAME COLUMN` / `RENAME TABLE` de algo en uso → la app vieja deja de encontrarlo.
- [ ] ❌ Cambiar tipo de columna de forma incompatible.
- [ ] ❌ Añadir FK a una tabla con datos que podrían violarla.
- [ ] ✅ `ADD COLUMN` nullable o con default → seguro.
- [ ] ✅ `CREATE TABLE` / `CREATE INDEX CONCURRENTLY` → seguro.
- [ ] ✅ Migración de datos en tarea separada, luego `SET NOT NULL` cuando la app nueva esté validada.

## Formato de salida

```markdown
# Flyway Migration Check — {migración(es)}

## ✅ Cumple
- (bullets de lo que está bien)

## ❌ Bloqueante — compatibilidad hacia atrás
- {operación breaking} en {migración}: {por qué rompe} → {fix en dos pasos}. (ADR-0010 D11)

## ❌ Bloqueante — reglas de persistencia
- {regla violada} (ADR-XXXX DN).

## ⚠️ Advertencias
- (cosas a vigilar: falta índice por club_id, falta comentario de categoría, etc.)

## Conclusión
SEGURA PARA MERGE / REQUIERE CAMBIOS / BLOQUEADA + razón.
```

## Patrón de migración breaking en dos pasos

Si la migración necesita un cambio rompiente, proponer la división:

```sql
-- PASO 1 (esta release): añadir lo nuevo, nullable, sin tocar lo viejo.
ALTER TABLE planificacion.sesion ADD COLUMN ritmo_v2 JSONB;

-- (tarea de migración de datos: poblar ritmo_v2 desde ritmo)

-- PASO 2 (release siguiente, cuando la app nueva ya esté en producción):
-- ALTER TABLE planificacion.sesion ALTER COLUMN ritmo_v2 SET NOT NULL;
-- ALTER TABLE planificacion.sesion DROP COLUMN ritmo;
```

## Reglas

- **El bloque E es el más importante**: una migración breaking en producción tumba el rollback (ADR-0010 D12 depende de que las migraciones sean compatibles hacia atrás).
- **No alucinar**: si una operación es ambigua, marcar como "verificar manualmente".
- **Cruce inline** a la sub-decisión en cada hallazgo.
