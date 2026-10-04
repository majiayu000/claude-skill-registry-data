---
name: spring-modulith-debug
description: Interpreta violaciones de fronteras de Spring Modulith y errores típicos del outbox de eventos en Runcriticon, y propone el fix coherente con events-first (proyección local + evento en lugar de llamada síncrona). Usar cuando ApplicationModules.verify() falla, cuando un @ApplicationModuleListener no se dispara, o cuando hay eventos atascados en event_publication.
---

# Spring Modulith Debug — Runcriticon

Traduce los errores típicos de Spring Modulith a un fix coherente con la arquitectura events-first (ADR-0007). Cruce: [`docs/arquitectura/estructura-de-un-modulo.md`](../../../docs/arquitectura/estructura-de-un-modulo.md) §6, [`docs/arquitectura/persistencia.md`](../../../docs/arquitectura/persistencia.md) §6-§8.

## Cuándo usar

- `ApplicationModules.verify()` falla en el test `ModulithFronterasTest`.
- Un `@ApplicationModuleListener` no se dispara cuando se publica un evento.
- Eventos atascados en `public.event_publication` (DLQ implícita).
- Dudas sobre dónde colocar un listener, una proyección o un evento.

## Catálogo de errores y fixes

### Error 1 — Violación de frontera: llamada síncrona entre módulos

```
Module 'planificacion' depends on module 'club' via ...ClubService
```

**Causa**: un módulo llama síncronamente a una clase de otro módulo. Prohibido por ADR-0007 D7.

**Fix**:
1. El módulo consumidor mantiene una **proyección local** de lo que necesita.
2. El módulo origen **publica un integration event** cuando el dato cambia.
3. El consumidor lo recibe con `@ApplicationModuleListener` y actualiza su proyección.

Ejemplo: si Planificación necesita saber los alumnos de un grupo, NO llama a `ClubService.getAlumnos(grupoId)`. Mantiene `planificacion.miembros_grupo` alimentada por `AlumnoAsignadoAGrupo`.

### Error 2 — Acceso a tipos internos de otro módulo

```
Module 'seguimiento' depends on non-exposed type com.runcriticon.club_taxonomia.domain.Tag
```

**Causa**: se importa un tipo de `domain`/`application`/`infrastructure` de otro módulo. Solo `api/` es público.

**Fix**: el dato necesario viaja en el **payload del integration event** (tipos planos), no como referencia al tipo interno. La proyección local guarda su propia representación.

### Error 3 — Listener no se dispara

**Causas posibles**:
1. El listener no está en un `@Component` gestionado por Spring.
2. El método no tiene `@ApplicationModuleListener` (sino `@EventListener` plano — que no usa el outbox transaccional).
3. El evento se publica fuera de una transacción.
4. El paquete del listener no es reconocido por Spring Modulith.

**Fix**: verificar que (a) el listener es `@Component` en `application/listeners/`, (b) usa `@ApplicationModuleListener` (que combina `@TransactionalEventListener` + `@Async` + propagación de contexto), (c) el publicador publica dentro de la transacción del caso de uso.

### Error 4 — Eventos atascados en `event_publication`

**Síntoma**: filas con `completion_date IS NULL` que no avanzan; métrica `outbox_dlq_events > 0`.

**Causas**:
1. El listener lanza excepción repetidamente (se agotan los 5 reintentos — ADR-0007 D13).
2. El listener no es idempotente y falla al reprocesar.
3. Un cambio breaking en el evento rompió la deserialización del consumidor.

**Fix**:
1. Revisar logs del listener (filtrar por `trace_id` del evento).
2. Corregir la causa raíz.
3. Republicar vía endpoint admin `POST /admin/events/republish` (ADR-0007 D13).
4. Verificar idempotencia: el listener debe usar `tracker.marcarSiNuevo(...)` antes de la lógica.

### Error 5 — Listener procesa el evento dos veces (efectos duplicados)

**Causa**: el outbox garantiza **at-least-once**, no exactly-once. El listener no es idempotente.

**Fix**: añadir la guarda de idempotencia con la tabla `{modulo}.evento_procesado(listener, event_id)`:

```kotlin
if (!tracker.marcarSiNuevo("{modulo}.{Listener}", evento.eventId)) return
```

Y diseñar la operación como upsert idempotente (ver `persistencia.md` §7-§8).

### Error 6 — Proyección desactualizada / lag alto

**Síntoma**: `projection_lag_seconds > 60` → autorización fail-closed (ADR-0009 D9).

**Causas**: listener lento, eventos atascados (Error 4), o el listener no actualiza `last_processed_event_ts`.

**Fix**: verificar que el listener actualiza ambas columnas (`last_processed_event_id`, `last_processed_event_ts`) al consumir; revisar si hay backlog en el outbox; si la proyección se corrompió, reproyectar desde snapshot (`persistencia.md` §9).

### Error 7 — Pérdida de trace_id entre módulos

**Síntoma**: el log del listener no comparte `trace_id` con la petición que originó el evento.

**Causa**: Spring Modulith no propaga el W3C Trace Context entre listeners automáticamente.

**Fix**: el evento lleva `traceparent` (7º campo) y el listener lo restaura con `MdcRestorerForEvents.restaurar(evento)` al inicio (ADR-0011 D4).

## Proceso de diagnóstico

1. **Capturar el error exacto** (output de `ApplicationModules.verify()` o stacktrace del listener).
2. **Clasificarlo** en uno de los 7 errores de arriba.
3. **Proponer el fix** coherente con events-first — nunca "añade una llamada síncrona para arreglarlo rápido".
4. **Cruzar** con la sub-decisión del ADR y el subdocumento.
5. **Si aplica**, generar el código del fix (proyección local, listener idempotente, etc.).

## Regla de oro del debug

**La solución a una violación de frontera NUNCA es relajar la regla.** Si dos módulos necesitan comunicarse, la respuesta siempre es: evento + proyección local. Si parece que hace falta una llamada síncrona, es señal de que las fronteras de los bounded contexts están mal trazadas — reabrir ADR-0007, no saltarse la regla.

## Comandos útiles

```bash
# Ver la documentación de módulos generada por Spring Modulith
./gradlew test --tests "*ModulithFronterasTest"
ls backend/build/spring-modulith/

# Ver eventos atascados en el outbox (con la BD local levantada)
docker-compose exec postgres psql -U runcriticon -d runcriticon_local \
  -c "SELECT listener_id, event_type, publication_date FROM event_publication WHERE completion_date IS NULL;"
```
