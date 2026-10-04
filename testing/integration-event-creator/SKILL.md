---
name: integration-event-creator
description: Crea un integration event público nuevo de un módulo del backend con todos sus artefactos coherentes - clase Kotlin en api/events con los 6 campos obligatorios + traceparent, JSON Schema versionado en schemas/{modulo}/, test de contrato con @Tag("contract"), actualización del README del módulo, y stub del listener consumidor si otro módulo debe reaccionar. Usar al modelar un hecho de dominio que otros módulos deben conocer.
disable-model-invocation: true
---

# Integration Event Creator — Runcriticon

Crea un integration event público y **todos** sus artefactos a la vez, evitando que se queden desincronizados. Cruce: ADR-0007 D11/D12, [`docs/arquitectura/estructura-de-un-modulo.md`](../../../docs/arquitectura/estructura-de-un-modulo.md) §3 y §6.

## Cuándo usar

Cuando un módulo necesita publicar un hecho de dominio que **otros módulos deben conocer** (no un domain event interno). Ejemplos: `PlanPublicado`, `AlumnoAsignadoAGrupo`, `MarcaActualizada`, `ConsentimientoRevocado`.

## Argumentos

```
/integration-event-creator planificacion PlanPublicado
/integration-event-creator salud MarcaActualizada
```

## Verificación previa

1. **Confirmar** que es integration event (público, va a `api/events/`) y no domain event interno (va a `domain/events/`).
2. **Preguntar** el payload específico (qué campos lleva además de los 6 obligatorios).
3. **Preguntar** qué módulos lo consumen (para generar stubs de listeners).
4. **Comprobar** que no existe ya un evento con ese nombre.

## Artefactos a generar (los 5)

### 1. Clase Kotlin del evento — `api/events/{Evento}.kt`

```kotlin
package com.runcriticon.{modulo}.api.events

import com.runcriticon.shared.eventos.IntegrationEvent
import java.time.Instant
import java.util.UUID

data class {Evento}(
    override val eventId: UUID,
    override val aggregateId: UUID,
    override val occurredAt: Instant,
    override val version: Int = 1,
    override val clubId: UUID,
    override val actorId: UUID?,
    override val traceparent: String?,
    // --- payload específico ---
    val {campo1}: {Tipo1},
    val {campo2}: {Tipo2},
) : IntegrationEvent
```

Con un `companion object` factory que rellena los 6 campos del contexto actual:

```kotlin
    companion object {
        fun from(/* parámetros del dominio */): {Evento} = {Evento}(
            eventId = UUID.randomUUID(),
            aggregateId = /* id del agregado */.value,
            occurredAt = Instant.now(),
            clubId = /* clubId */.value,
            actorId = PrincipalContext.actual()?.userId,
            traceparent = OpenTelemetryHelper.actualTraceparent(),
            // payload
        )
    }
```

### 2. JSON Schema — `schemas/{modulo}/{evento-kebab}-v1.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://runcriticon.com/schemas/{modulo}/{evento-kebab}-v1.json",
  "title": "{Evento}",
  "type": "object",
  "required": ["eventId", "aggregateId", "occurredAt", "version", "clubId", "{campo1}"],
  "properties": {
    "eventId":     { "type": "string", "format": "uuid" },
    "aggregateId": { "type": "string", "format": "uuid" },
    "occurredAt":  { "type": "string", "format": "date-time" },
    "version":     { "type": "integer", "minimum": 1 },
    "clubId":      { "type": "string", "format": "uuid" },
    "actorId":     { "type": ["string", "null"], "format": "uuid" },
    "traceparent": { "type": ["string", "null"] },
    "{campo1}":    { "type": "{json-type}" }
  },
  "additionalProperties": false
}
```

`actorId` y `traceparent` son nullable; van fuera de `required`.

### 3. Test de contrato — `test/.../contracts/{Evento}ContractTest.kt`

```kotlin
package com.runcriticon.{modulo}.contracts

import com.networknt.schema.JsonSchemaFactory
import com.networknt.schema.SpecVersion
import io.kotest.matchers.collections.shouldBeEmpty
import org.junit.jupiter.api.Tag
import org.junit.jupiter.api.Test
import java.nio.file.Path

@Tag("contract")
class {Evento}ContractTest {

    private val schema = JsonSchemaFactory
        .getInstance(SpecVersion.VersionFlag.V202012)
        .getSchema(Path.of("../schemas/{modulo}/{evento-kebab}-v1.json").toUri())

    @Test
    fun `{Evento} serializado cumple el JSON Schema v1`() {
        val evento = {Evento}Builder().build()
        val json = objectMapper.valueToTree<com.fasterxml.jackson.databind.JsonNode>(evento)
        schema.validate(json).shouldBeEmpty()
    }
}
```

### 4. Actualización del README del módulo

Añadir a `backend/src/main/kotlin/com/runcriticon/{modulo}/README.md`:

```markdown
## Eventos publicados

| Evento | Cuándo | Schema | Consumido por |
|---|---|---|---|
| `{Evento}` v1 | {cuándo se emite} | `schemas/{modulo}/{evento-kebab}-v1.json` | {módulos consumidores} |
```

### 5. Stubs de listeners en módulos consumidores

Por cada módulo que consume el evento, crear/ampliar un listener en `{consumidor}/application/listeners/`:

```kotlin
@Component
class {Evento}Listener(
    private val proyeccion: {Proyeccion},
    private val tracker: EventoProcesadoTracker,
) {
    @ApplicationModuleListener
    fun on(evento: {Evento}) {
        try {
            MdcRestorerForEvents.restaurar(evento)
            if (!tracker.marcarSiNuevo("{consumidor}.{Evento}Listener", evento.eventId)) return
            // TODO: actualizar la proyección local idempotentemente
        } finally {
            MdcRestorerForEvents.limpiar()
        }
    }
}
```

## Después de generar

1. **Recordar al usuario** que el `companion.from(...)` debe llamarse desde el método del agregado que produce el hecho (`api/events` no se construye a mano en el caso de uso).
2. **Avisar** de que el job `contractTest` del CI validará el schema (ADR-0007 D11).
3. **Si hay listeners consumidores**, recordar que la proyección local necesita columnas `last_processed_event_id` + `last_processed_event_ts` (ADR-0009 D9) — sugerir migración Flyway si la proyección es nueva.

## Versionado breaking (cuando el evento ya existe)

Si el usuario pide modificar un evento de forma rompiente:

- Crear `{evento-kebab}-v2.json` y `{Evento}V2.kt` (NO modificar v1).
- Activar dual-publishing: el emisor publica v1 Y v2 durante 4 semanas (ADR-0007 D11).
- Documentar la ventana de migración en el README del módulo.

## Reglas

- **Los 6 campos obligatorios son no negociables.** `eventId`, `aggregateId`, `occurredAt`, `version`, `clubId`, `actorId`. Más `traceparent` opcional (ADR-0011 D4).
- **El schema vive en la raíz** `schemas/`, no en `src/main/resources` (accesible para herramientas externas — ADR-0007 D11).
- **`additionalProperties: false`** en el schema para detectar campos no declarados.
- **Listeners idempotentes** siempre, vía `evento_procesado` (ADR-0007 D9).

## Antipatrones

- Evento sin JSON Schema (rompe el job `contractTest`).
- Evento con tipos de `domain` en el payload (debe ser serializable, primitivos + UUIDs + tipos planos).
- Modificar un evento v1 existente en vez de crear v2.
- Listener sin `tracker.marcarSiNuevo` ni `MdcRestorerForEvents`.
