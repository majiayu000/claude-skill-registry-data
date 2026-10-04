---
name: module-scaffold
description: Genera el scaffold completo de un módulo nuevo del backend (Identidad, Club, Planificación, Seguimiento o Auditoría) siguiendo la guía operativa de Runcriticon y los 5 subdocumentos. Crea estructura de paquetes, errores sellados, IntegrationEvent, puertos de consulta de reglas de relación + auditor de accesos, casos de uso con Either + Raise DSL, repositorios con @AuthScope, listeners idempotentes, MetricasDelModulo, ConfigurationProperties, migración Flyway inicial con categorización RGPD, y tests stub. Cumple los 30+ ítems del checklist por construcción.
disable-model-invocation: true
---

# Module Scaffold — Runcriticon

Genera un módulo completo del backend con todos los ítems del checklist de [`docs/arquitectura/estructura-de-un-modulo.md`](../../../docs/arquitectura/estructura-de-un-modulo.md) ya cubiertos por construcción.

## Cuándo usar esta skill

- Crear cualquiera de los 5 módulos del backend en Fase 1 (`identidad`, `club`, `planificacion`, `salud`, `auditoria`).
- Crear un módulo futuro tras alcanzarse un disparador (multi-rol, soporte interno, etc.).

## Módulo vs esquema canónico (ADR-0004 D4)

El **nombre del paquete Java** (`com.runcriticon.{modulo}`) puede diferir del **nombre canónico del esquema** de base de datos. Esta distinción afecta migraciones Flyway, `@Table(schema=...)`, tabla `evento_procesado` y el tag `module` de métricas.

| Paquete Java (`{modulo}`) | Esquema canónico DB (`{esquema}`) |
|---------------------------|-----------------------------------|
| `identidad`               | `identidad`                       |
| `club`                    | `club_taxonomia`                  |
| `planificacion`           | `planificacion`                   |
| `salud`                   | `seguimiento`                     |
| `auditoria`               | `auditoria`                       |

Para módulos futuros, el esquema canónico lo fija el ADR de creación. Si no hay ADR, la skill pregunta antes de generar migraciones.

> En las plantillas, `{modulo}` es el nombre del paquete Java y `{esquema}` es el nombre canónico del esquema DB. Cuando difieren (filas 2 y 4), el wizard los trata como valores separados.

## Argumentos esperados

El usuario invoca con el nombre del módulo y, opcionalmente, el agregado raíz inicial:

```
/module-scaffold planificacion PlanSemanal
/module-scaffold identidad Usuario
```

Si no se indica agregado, la skill pregunta antes de continuar.

## Verificación previa

Antes de crear nada:

1. **Comprobar** que el módulo no existe ya en `backend/src/main/kotlin/com/runcriticon/`.
2. **Comprobar** que el esquema no existe ya en `backend/src/main/resources/db/migration/`.
3. **Confirmar** con el usuario via `AskUserQuestion`:
   - Categoría RGPD principal del módulo: `PII_PRIMARIA` (Identidad, Salud, Planificación), `AUDITORIA_*` (Auditoría), o `SIN_PII` (Club si solo guarda taxonomía).
   - ¿Tiene tablas con datos del alumno que deban borrarse al ejercer olvido? (impone `StudentDeletionListener`).
   - ¿Va a consumir eventos de otros módulos? (impone proyecciones locales).
   - Si el módulo es `club` o `salud`: confirmar que el esquema DB es `club_taxonomia` o `seguimiento` respectivamente (ver tabla "Módulo vs esquema canónico" — diferir aquí genera migraciones con esquema incorrecto).

## Estructura a generar

```
backend/src/main/kotlin/com/runcriticon/{modulo}/
├── api/
│   └── events/
│       └── IntegrationEvent.kt          ← se reutiliza si ya existe en shared
├── domain/
│   ├── {Agregado}.kt                    ← raíz con require / Either
│   ├── ids.kt                           ← Typed IDs value class UUID v7
│   ├── {Modulo}Error.kt                 ← sealed class con variantes comunes + propias
│   ├── events/                          ← domain events internos
│   └── ports/
│       ├── {Agregado}Repository.kt
│       ├── {Relacion}Lookup.kt          ← puerto de consulta de una regla de relación (ADR-0009 D7)
│       └── (otros puertos según necesidad)
├── application/
│   ├── {Modulo}Config.kt                ← @EnableConfigurationProperties
│   ├── (CasosDeUsoServices).kt          ← @ApplicationService
│   ├── {Modulo}AccessAuditor.kt         ← publica AccesoDenegado (ADR-0009 D15, D16)
│   ├── listeners/
│   │   └── (placeholder + StudentDeletionListener.kt si aplica)
│   └── projections/
│       └── (placeholder con last_processed_event_*)
└── infrastructure/
    ├── rest/
    │   ├── {Agregado}Controller.kt
    │   ├── dto/
    │   └── (ResultadoControllerAdvice si no existe en shared)
    ├── persistencia/
    │   ├── {Agregado}Entity.kt          ← @RgpdCategory obligatorio
    │   ├── {Agregado}EntityRepository.kt
    │   ├── {Agregado}RepositoryImpl.kt  ← con @AuthScope
    │   └── {Agregado}Mapper.kt          ← @Konverter
    ├── config/
    │   └── {Modulo}Properties.kt        ← @ConfigurationProperties + @Validated
    └── observabilidad/
        └── {Modulo}Metrics.kt          ← bean con MeterRegistry
```

Más:

```
backend/src/main/resources/db/migration/{modulo}/
└── V{YYYYMMDD}{NNNN}__crea_esquema_y_{tabla}.sql

backend/src/main/kotlin/com/runcriticon/{modulo}/
├── README.md
├── RGPD.md                              ← si tiene PII
├── CONFIG.md                            ← secretos y propiedades del módulo
└── OBSERVABILIDAD.md                    ← métricas y alarmas del módulo

backend/src/test/kotlin/com/runcriticon/{modulo}/
├── architecture/
│   └── (tests ArchUnit del módulo)
├── domain/
│   └── {Agregado}Test.kt                ← BehaviorSpec con shouldBeRight/shouldBeLeft
└── (casos de uso de integración con Testcontainers)
```

Más en raíz si no existe:

```
schemas/{esquema}/                       ← carpeta vacía para JSON Schemas futuros
```

## Plantillas literales

### Domain — `{Agregado}.kt`

```kotlin
package com.runcriticon.{modulo}.domain

import arrow.core.Either
import arrow.core.raise.either
import arrow.core.raise.ensure

class {Agregado} private constructor(
    val id: {Agregado}Id,
    val clubId: ClubId,
    // ...
    private var estado: Estado{Agregado},
) {
    /**
     * TODO: documentar la operación principal.
     * Validaciones esperables → Either (ADR-0008 D11).
     * Precondiciones imposibles → require (caller bug).
     */
    fun ejecutarOperacionPrincipal(): Either<{Modulo}Error, EventoIntegracion> = either {
        ensure(estado == Estado{Agregado}.INICIAL) { {Modulo}Error.YaProcesado(id) }
        // lógica de dominio
        estado = Estado{Agregado}.PROCESADO
        EventoIntegracion.from(id, clubId)
    }

    companion object {
        fun nuevo(id: {Agregado}Id, clubId: ClubId): {Agregado} =
            {Agregado}(id, clubId, estado = Estado{Agregado}.INICIAL)
    }
}

enum class Estado{Agregado} { INICIAL, PROCESADO, ARCHIVADO }
```

### Domain — `ids.kt`

```kotlin
package com.runcriticon.{modulo}.domain

import com.github.f4b6a3.uuid.UuidCreator
import java.util.UUID

@JvmInline
value class {Agregado}Id(val value: UUID) {
    init {
        require(value.version() == 7) { "{Agregado}Id debe ser UUID v7" }
    }
    companion object {
        fun nuevo(): {Agregado}Id = {Agregado}Id(UuidCreator.getTimeOrderedEpoch())
    }
}
```

### Domain — `{Modulo}Error.kt`

```kotlin
package com.runcriticon.{modulo}.domain

import java.util.UUID

sealed class {Modulo}Error {
    // Variantes comunes con shape estandarizado
    data class Forbidden(val razon: String) : {Modulo}Error()
    data class NotFound(val recurso: String, val id: String) : {Modulo}Error()
    data class InvalidInput(val campo: String, val motivo: String) : {Modulo}Error()
    data object Conflict : {Modulo}Error()
    data class ProjectionStale(val modulo: String, val lagSeconds: Long) : {Modulo}Error()

    // Específicas del módulo {Modulo} — añadir según necesidad
    data class YaProcesado(val id: {Agregado}Id) : {Modulo}Error()
}
```

### Domain — `events/{Evento}Interno.kt`

```kotlin
package com.runcriticon.{modulo}.domain.events

import java.time.Instant

data class {Evento}Interno(
    val id: {Agregado}Id,
    val occurredAt: Instant,
)
```

### Domain — `api/events/{Evento}.kt`

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
    // payload específico
) : IntegrationEvent {
    companion object {
        fun from(id: {Agregado}Id, clubId: ClubId): {Evento} = {Evento}(
            eventId = UUID.randomUUID(),
            aggregateId = id.value,
            occurredAt = Instant.now(),
            clubId = clubId.value,
            actorId = PrincipalContext.actual()?.userId,
            traceparent = OpenTelemetryHelper.actualTraceparent(),
        )
    }
}
```

### Domain — `ports/{Agregado}Repository.kt`

```kotlin
package com.runcriticon.{modulo}.domain.ports

import com.runcriticon.{modulo}.domain.{Agregado}
import com.runcriticon.{modulo}.domain.{Agregado}Id

interface {Agregado}Repository {
    fun guardar(agregado: {Agregado})
    fun buscar(id: {Agregado}Id): {Agregado}?
}
```

### Puerto de consulta — `{Relacion}Lookup.kt`

No hay `{Modulo}AutorizacionService` (ADR-0009 D7): el caso de uso consulta la `AuthorizationMatrix` directamente y cada regla de relación vive una vez en un puerto de consulta sobre la proyección local, reutilizado por todos los casos de uso que la necesitan (modelo real: `planificacion/application/ports/outbound/persistence/CoachGroupLookup.kt`).

```kotlin
package com.runcriticon.{modulo}.application.ports.outbound.persistence

import com.runcriticon.shared.tenancy.ClubId

interface {Relacion}Lookup {
    // Una regla de relación por método; se consulta desde el caso de uso con ensure(...)
    fun is{Relacion}(clubId: ClubId, actorId: PersonId, objetoId: {Agregado}Id): Boolean
}
```

### Application — caso de uso con @ApplicationService

```kotlin
package com.runcriticon.{modulo}.application

import arrow.core.Either
import arrow.core.raise.either
import com.runcriticon.shared.annotations.ApplicationService
import com.runcriticon.shared.autorizacion.PrincipalProvider
import com.runcriticon.shared.eventos.PublicadorDeEventos
import com.runcriticon.{modulo}.api.events.{Evento}
import com.runcriticon.{modulo}.domain.{Agregado}Id
import com.runcriticon.{modulo}.domain.{Modulo}Error
import com.runcriticon.{modulo}.domain.ports.{Agregado}Repository
import com.runcriticon.{modulo}.application.ports.outbound.persistence.{Relacion}Lookup
import com.runcriticon.{modulo}.infrastructure.observabilidad.{Modulo}Metrics

@ApplicationService
class EjecutarOperacionPrincipalService(
    private val repositorio: {Agregado}Repository,
    private val relacion: {Relacion}Lookup,
    private val auditor: {Modulo}AccessAuditor,
    private val publicador: PublicadorDeEventos,
    private val metricas: {Modulo}Metrics,
) {
    fun ejecutar(actor: Principal, id: {Agregado}Id): Either<{Modulo}Error, {Evento}> = either {
        // 1. RBAC contra la matriz, inline y al inicio (ADR-0009 D7, D13). Cada guarda publica AccesoDenegado.
        ensure(AuthorizationMatrix.can(actor.role, Resource.X, Action.Y)) {
            auditor.denegado(actor, Resource.X, Action.Y, aggregateId = actor.userId, motivo = "RBAC")
            {Modulo}Error.Forbidden
        }
        // 2. Nivel de objeto vía puerto de consulta (ADR-0009 D3, D7)
        ensure(relacion.is{Relacion}(ClubId.of(actor.clubId), PersonId.of(actor.userId), id)) {
            auditor.denegado(actor, Resource.X, Action.Y, aggregateId = id.value, motivo = "No{Relacion}")
            {Modulo}Error.Forbidden
        }

        val agregado = repositorio.buscar(ClubId.of(actor.clubId), id)
            ?: raise({Modulo}Error.NotFound("{Agregado}", id.value.toString()))

        val evento = agregado.ejecutarOperacionPrincipal().bind()

        repositorio.guardar(agregado)
        publicador.publicar(evento)

        metricas.operacionPrincipal.increment()

        evento
    }
}
```

### Application — `StudentDeletionListener` (si tiene PII)

```kotlin
package com.runcriticon.{modulo}.application.listeners

import com.runcriticon.shared.eventos.AlumnoEliminado
import com.runcriticon.shared.eventos.EventoProcesadoTracker
import com.runcriticon.shared.observabilidad.MdcRestorerForEvents
import org.springframework.modulith.events.ApplicationModuleListener
import org.springframework.stereotype.Component

@Component
class StudentDeletionListener(
    // Inyectar repositorios de tablas con PII del alumno
    private val tracker: EventoProcesadoTracker,
) {
    @ApplicationModuleListener
    fun on(evento: AlumnoEliminado) {
        try {
            MdcRestorerForEvents.restaurar(evento)

            if (!tracker.marcarSiNuevo("{modulo}.StudentDeletionListener", evento.eventId)) return

            // TODO: borrado físico de tablas PII_PRIMARIA del módulo
            // Para tablas de categoría 2/3: llamar a anonimiza_evento_auditoria(...)
        } finally {
            MdcRestorerForEvents.limpiar()
        }
    }
}
```

### Infrastructure — `{Agregado}Entity.kt` con @RgpdCategory

```kotlin
package com.runcriticon.{modulo}.infrastructure.persistencia

import com.runcriticon.shared.rgpd.Category
import com.runcriticon.shared.rgpd.RgpdCategory
import jakarta.persistence.*
import java.time.Instant
import java.util.UUID

@Entity
@Table(name = "{agregado_snake}", schema = "{esquema}")
@RgpdCategory(Category.PII_PRIMARIA)  // ← Ajustar según categoría real
class {Agregado}Entity(
    @Id @Column(name = "id") var id: UUID,
    @Column(name = "club_id", nullable = false) var clubId: UUID,
    @Column(name = "estado", nullable = false, length = 20) var estado: String,
    @Version var version: Long = 0,
    @Column(name = "created_at", nullable = false, updatable = false) var createdAt: Instant? = null,
    @Column(name = "updated_at", nullable = false) var updatedAt: Instant? = null,
)
```

### Infrastructure — `{Agregado}RepositoryImpl.kt` con @AuthScope

```kotlin
package com.runcriticon.{modulo}.infrastructure.persistencia

import com.runcriticon.shared.autorizacion.AuthScope
import com.runcriticon.shared.autorizacion.Scope
import com.runcriticon.{modulo}.domain.{Agregado}
import com.runcriticon.{modulo}.domain.{Agregado}Id
import com.runcriticon.{modulo}.domain.ports.{Agregado}Repository
import org.springframework.stereotype.Repository

@Repository
class {Agregado}RepositoryImpl(
    private val entityRepo: {Agregado}EntityRepository,
    private val mapper: {Agregado}Mapper,
) : {Agregado}Repository {

    @AuthScope(Scope.CLUB)
    override fun buscar(id: {Agregado}Id): {Agregado}? =
        entityRepo.findById(id.value).orElse(null)?.let(mapper::aDominio)

    @AuthScope(Scope.CLUB)
    override fun guardar(agregado: {Agregado}) {
        entityRepo.save(mapper.aEntidad(agregado))
    }
}
```

### Infrastructure — `{Agregado}Controller.kt` con @Authorize

```kotlin
package com.runcriticon.{modulo}.infrastructure.rest

import com.runcriticon.shared.autorizacion.Authorize
import com.runcriticon.{modulo}.application.EjecutarOperacionPrincipalService
import com.runcriticon.{modulo}.domain.{Agregado}Id
import com.runcriticon.shared.rest.toResponse
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import java.util.UUID

@RestController
@RequestMapping("/{recursos}")
class {Agregado}Controller(
    private val servicio: EjecutarOperacionPrincipalService,
) {
    /**
     * TODO: ajustar verbo HTTP, ruta y los strings RECURSO:ACCION (ADR-0009 D13).
     * Cada handler público DEBE llevar @Authorize o @NoAuthRequired — ArchUnit lo exige.
     */
    @PostMapping("/{id}/operar")
    @Authorize("{RECURSO}:{ACCION}")     // ← rellenar, ej. "PLAN:PUBLICAR"
    fun operarSobre(@PathVariable id: UUID): ResponseEntity<*> =
        servicio.ejecutar({Agregado}Id(id)).toResponse()
}
```

> **Reglas obligatorias de cada handler (ADR-0009 D13):**
> - `@Authorize("RECURSO:ACCION")` — o `@NoAuthRequired(justificacion = "...")` para endpoints públicos.
> - Los strings `RECURSO` y `ACCION` los define el caso de uso; ArchUnit falla en CI si falta la anotación.
> - **Nunca `@PreAuthorize`** — no se usa en este proyecto; `@Authorize` es la anotación propia.
> - `toResponse()` convierte `Either<{Modulo}Error, T>` al código HTTP correcto (sin `when` en el controller).

### Infrastructure — `{Modulo}Metrics.kt`

```kotlin
package com.runcriticon.{modulo}.infrastructure.observabilidad

import io.micrometer.core.instrument.Counter
import io.micrometer.core.instrument.MeterRegistry
import io.micrometer.core.instrument.Timer
import org.springframework.stereotype.Component

@Component
class {Modulo}Metrics(registry: MeterRegistry) {

    val operacionPrincipal: Counter = Counter
        .builder("{esquema}.operaciones_total")
        .description("TODO: documentar la métrica de negocio")
        .tag("module", "{esquema}")     // nombre canónico del esquema, no del paquete (ADR-0011 D9)
        .register(registry)

    val tiempoOperacion: Timer = Timer
        .builder("{esquema}.operacion_seconds")
        .description("Latencia del caso de uso principal")
        .tag("module", "{esquema}")
        .publishPercentiles(0.5, 0.95, 0.99)
        .register(registry)
}
```

### Infrastructure — `{Modulo}Properties.kt`

```kotlin
package com.runcriticon.{modulo}.infrastructure.config

import jakarta.validation.Valid
import jakarta.validation.constraints.Min
import jakarta.validation.constraints.NotNull
import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.validation.annotation.Validated

@ConfigurationProperties(prefix = "runcriticon.{modulo}")
@Validated
data class {Modulo}Properties(
    @field:Valid
    val parametros: Parametros = Parametros(),
) {
    data class Parametros(
        @field:Min(1)
        val timeoutSegundos: Int = 60,
        @field:NotNull
        val activado: Boolean = true,
    )
}
```

### Application — `{Modulo}Config.kt`

```kotlin
package com.runcriticon.{modulo}.application

import com.runcriticon.{modulo}.infrastructure.config.{Modulo}Properties
import org.springframework.boot.context.properties.EnableConfigurationProperties
import org.springframework.context.annotation.Configuration

@Configuration
@EnableConfigurationProperties({Modulo}Properties::class)
class {Modulo}Config
```

### Migración Flyway inicial

```sql
-- backend/src/main/resources/db/migration/{modulo}/V{YYYYMMDD}{NNNN}__crea_esquema_y_{tabla}.sql
-- {modulo} = nombre del paquete Java (ej. "club"); {esquema} = nombre canónico DB (ej. "club_taxonomia")

CREATE SCHEMA IF NOT EXISTS {esquema};

-- Categoría 1 (PII_PRIMARIA): TODO descripción de los datos del agregado.
-- Retención: hasta baja + 30 días de gracia. Borrado físico al consumir AlumnoEliminado.
CREATE TABLE {esquema}.{tabla} (
    id          UUID PRIMARY KEY,
    club_id     UUID NOT NULL,
    estado      VARCHAR(20) NOT NULL CHECK (estado IN ('INICIAL', 'PROCESADO', 'ARCHIVADO')),
    version     BIGINT NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_{tabla}_club_id ON {esquema}.{tabla}(club_id);

-- Tabla para idempotencia de listeners del módulo (ADR-0007 D9)
CREATE TABLE {esquema}.evento_procesado (
    listener      VARCHAR(120) NOT NULL,
    event_id      UUID         NOT NULL,
    processed_at  TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (listener, event_id)
);
```

### Test stub — `{Agregado}Test.kt`

```kotlin
package com.runcriticon.{modulo}.domain

import io.kotest.assertions.arrow.core.shouldBeLeft
import io.kotest.assertions.arrow.core.shouldBeRight
import io.kotest.core.spec.style.BehaviorSpec
import io.kotest.matchers.shouldBe

class {Agregado}Test : BehaviorSpec({

    given("un {Agregado} en estado INICIAL") {
        // val agregado = {Agregado}Builder().inicial().build()

        `when`("se ejecuta la operación principal") {
            // val resultado = agregado.ejecutarOperacionPrincipal()

            then("devuelve Either.Right con el evento") {
                // val evento = resultado.shouldBeRight()
                // evento.aggregateId shouldBe agregado.id.value
            }
        }
    }

    given("un {Agregado} ya PROCESADO") {

        `when`("se intenta ejecutar de nuevo") {

            then("devuelve Either.Left con YaProcesado") {
                // resultado.shouldBeLeft<{Modulo}Error.YaProcesado>()
            }
        }
    }
})
```

### Documentación del módulo

#### `README.md`

```markdown
# Módulo {Modulo}

TODO: descripción del módulo, eventos publicados/consumidos, dependencias.

## Categoría RGPD principal

- Tabla {tabla}: PII_PRIMARIA

## Eventos publicados

- `{Evento}` v1 → schema en `schemas/{esquema}/{evento}-v1.json`

## Eventos consumidos

- TODO

## Dependencias

- Núcleo compartido: `com.runcriticon.shared.autorizacion`
```

#### `RGPD.md` (si tiene PII)

Plantilla completa heredada de [`docs/arquitectura/rgpd-en-modulos.md`](../../../docs/arquitectura/rgpd-en-modulos.md) §9.

#### `CONFIG.md`

Plantilla completa heredada de [`docs/arquitectura/configuracion-y-secretos-en-modulos.md`](../../../docs/arquitectura/configuracion-y-secretos-en-modulos.md) §3.

#### `OBSERVABILIDAD.md`

Plantilla con alarmas mínimas + métricas de negocio (cruce [`docs/arquitectura/observabilidad-por-modulo.md`](../../../docs/arquitectura/observabilidad-por-modulo.md) §11).

## Después de generar

1. **Listar al usuario los 30+ ítems del checklist** y marcar cuáles quedan ya cubiertos por construcción.
2. **Avisar de los ítems que requieren completar manualmente**: lógica concreta del agregado, mappers Konvert, strings `RECURSO:ACCION` reales en `@Authorize` de cada handler, integración con otros módulos, JSON Schema del integration event.
3. **Verificar que el controller generado tiene `@Authorize` o `@NoAuthRequired` en todos los handlers** — sin esto, ArchUnit falla en CI (ADR-0009 D13).
4. **Sugerir el siguiente paso**: completar la operación principal del agregado o registrar el primer evento de integración.
5. **No commitear automáticamente** — dejar al usuario revisar el diff.

## Antipatrones a evitar

- Crear ficheros con `package com.runcriticon...` pero el archivo en otro path.
- Olvidar `@RgpdCategory` en una entidad nueva (ArchUnit lo detecta pero el error de CI es tardío).
- `@PreAuthorize` de Spring Security en controllers — no se usa (backend/CLAUDE.md): todo handler público lleva la anotación propia `@Authorize("RECURSO:ACCION")` o `@NoAuthRequired` con justificación; ArchUnit lo exige (ADR-0009 D13).
- Listener sin `MdcRestorerForEvents` y `tracker.marcarSiNuevo` envueltos en try/finally.
- Mapper con anotaciones JPA en clases de `domain` (rompe ADR-0008 D6).

## Referencias

- [`docs/arquitectura/estructura-de-un-modulo.md`](../../../docs/arquitectura/estructura-de-un-modulo.md) — guía principal con ejemplo de PlanSemanal.
- [`docs/arquitectura/persistencia.md`](../../../docs/arquitectura/persistencia.md), [`testing-de-modulos.md`](../../../docs/arquitectura/testing-de-modulos.md), [`rgpd-en-modulos.md`](../../../docs/arquitectura/rgpd-en-modulos.md), [`observabilidad-por-modulo.md`](../../../docs/arquitectura/observabilidad-por-modulo.md), [`configuracion-y-secretos-en-modulos.md`](../../../docs/arquitectura/configuracion-y-secretos-en-modulos.md) — 5 subdocumentos.
- ADRs invocados: 0004, 0007, 0008, 0009, 0011, 0013, 0014.
