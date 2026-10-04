---
name: backend-feature-dev
description: >
  Desarrollo de una feature (caso de uso) dentro de un módulo backend existente:
  domain con Either, @ApplicationService con autorización explícita, adaptadores REST/JPA,
  migración Flyway y pirámide de tests completa, ajustado a ADR-0007/0008/0009/0010 y a los
  docs de arquitectura. Usar al añadir o modificar casos de uso en un módulo ya creado.
disable-model-invocation: false
---

# backend-feature-dev — Runcriticon

Guía el desarrollo de una feature dentro de un módulo backend **ya existente**, cumpliendo por construcción los ADRs del backend y los tres documentos de arquitectura. Actúa como arquitecto Kotlin/JVM: idioms de Kotlin y Arrow.kt, SOLID y Clean Architecture mapeados a la hexagonal del proyecto, y criterios de performance (JVM, JPA, pools) cuando tocan.

## Cuándo usar esta skill

- Añadir un caso de uso, endpoint o listener a un módulo existente.
- Modificar lógica de dominio o de aplicación de un módulo.
- **NO** para crear un módulo nuevo → `module-scaffold`.
- **NO** para crear integration events nuevos → `integration-event-creator`.
- **NO** para validar migraciones sueltas → `flyway-migration-checker`.

## Argumentos

```
/backend-feature-dev {modulo} {CasoDeUso}
```

Ejemplo: `/backend-feature-dev planificacion AsignarPlanAGrupo`. El caso de uso en castellano (lenguaje ubicuo, `docs/glosario.md`).

## Verificación previa (obligatoria)

1. El módulo existe en `backend/src/main/kotlin/com/runcriticon/{modulo}/`.
2. Leer el README del módulo y su sealed class de errores (`{modulo}/domain/{Modulo}Error.kt`).
3. **Esquema canónico vs paquete Java (ADR-0004 D4, ADR-0011 D9)**: para los módulos `club` y `salud`, el esquema DB y el tag `module` de métricas son `club_taxonomia` y `seguimiento` respectivamente — el paquete Java no coincide con el esquema en estos dos casos. Si el trabajo toca migraciones Flyway o métricas de esos módulos, usar el nombre canónico del esquema (no el del paquete).
4. Tener presentes los tres docs de arquitectura — son la autoridad junto con los ADRs:
   - `docs/arquitectura/estructura-de-un-modulo.md`
   - `docs/arquitectura/persistencia.md`
   - `docs/arquitectura/testing-de-modulos.md`

## Preguntas al usuario

Una tanda con `AskUserQuestion`:

1. **¿Punto de entrada?** — endpoint REST / listener de evento / ambos / job programado.
2. **¿Regla de autorización a nivel de objeto?** — la consulta a `AuthorizationMatrix` es siempre obligatoria; la pregunta es qué relación valida el puerto de consulta del módulo (entrenador↔grupo, alumno↔plan, solo RBAC...).
3. **¿Publica integration events nuevos?** — si sí, remitir a `/integration-event-creator` para el evento y sus 4 artefactos; esta skill solo añade la llamada al publicador.
4. **¿Toca persistencia?** — tabla/columna nueva → migración Flyway `V{YYYYMMDD}{NNNN}__descripcion.sql` (secuencia global entre módulos: comprobar todas las carpetas del día, ADR-0004 D9) backward-compatible (deploy-then-migrate).

## Workflow por capas

Orden estricto: **domain → application → infrastructure → tests**. La dependencia siempre apunta al dominio.

### 1. Domain (puro: Kotlin + Arrow + shared, nada más)

- Lógica nueva en el agregado o value object. Cero Spring/JPA/Jackson (ArchUnit lo parte).
- Errores nuevos como variantes de la sealed class del módulo (`PlanificacionError`, `IdentidadError`...). **No existe un `DomainError` compartido.**
- Regla de errores (ADR-0008 D11):
  - `Either<{Modulo}Error, T>` + `either { }` / `ensure` / `raise` → validaciones **esperables** (estado del agregado, datos de negocio).
  - `require`/`check` → precondiciones **imposibles** (bug del caller si fallan).
- Si necesita un colaborador externo nuevo: interface en `domain/ports/`.

### 2. Application

```kotlin
@ApplicationService
class {CasoDeUso}Service(
    private val repositorio: {Agregado}Repository,
    private val relacion: {Relacion}Lookup,          // puerto de consulta de la regla de relación (ADR-0009 D7)
    private val auditor: {Modulo}AccessAuditor,      // publica AccesoDenegado (ADR-0009 D15, D16)
    private val publicador: PublicadorDeEventos,
) {
    fun ejecutar(actor: Principal, ...): Either<{Modulo}Error, {Resultado}> = either {
        ensure(AuthorizationMatrix.can(actor.role, Resource.X, Action.Y)) {   // SIEMPRE primera guarda
            auditor.denegado(actor, Resource.X, Action.Y, aggregateId = actor.userId, motivo = "RBAC")
            {Modulo}Error.Forbidden
        }
        val agregado = repositorio.buscar(ClubId.of(actor.clubId), id)
        ensureNotNull(agregado) { auditor.denegado(...); {Modulo}Error.Forbidden }
        ensure(relacion.is{Relacion}(ClubId.of(actor.clubId), ..., agregado.x)) {  // nivel de objeto
            auditor.denegado(...); {Modulo}Error.Forbidden
        }
        val evento = agregado.{operacion}(...).bind()
        repositorio.guardar(agregado)
        publicador.publicar(evento)
        evento
    }
}
```

- `@ApplicationService` (anotación propia de `shared`) — `AuthorizationArchTest` verifica que la clase accede a `AuthorizationMatrix` o se declara exenta a nivel de clase (`@NoAuthRequired`/`@AuthenticatedOnly`). No verifica la relación ni la emisión de `AccesoDenegado`: eso lo cubren los tests.
- **No se usa `@PreAuthorize` de Spring Security** (backend/CLAUDE.md): la capa RBAC del controller va con la anotación propia `@Authorize("RECURSO:ACCION")` o `@NoAuthRequired` con justificación — ArchUnit exige una de las dos en todo handler público (ADR-0009 D13). El nivel de objeto se valida aquí, en el propio caso de uso, contra los puertos de consulta del módulo sobre sus proyecciones locales (fail-closed si lag ≥ 60 s). No existe `AutorizacionService` por módulo (ADR-0009 D7).
- Toda guarda que devuelve `Forbidden`/`ProjectionStale` publica `AccesoDenegado` con su motivo (ADR-0009 D7, D15).
- Si la regla de relación es nueva: método nuevo en un puerto de consulta de `application/ports/outbound/persistence/` (p. ej. `CoachGroupLookup`) + adaptador en `infrastructure/`. Si ya existe, reutilízalo: una regla, un sitio.
- Si consume un evento: listener en `application/listeners/` con `@ApplicationModuleListener`, restauración de `traceparent`, e idempotencia vía `EventoProcesadoTracker.marcarSiNuevo(listener, eventId)`.

### 3. Infrastructure

- **Controller**: cada handler público con `@Authorize("RECURSO:ACCION")` o `@NoAuthRequired` justificado (ArchUnit lo exige). DTOs propios en `rest/dto/` (Konvert para mapear), traducción `Either → HTTP` con la extension `toResponse(...)` del módulo. Cuerpo neutro en denegaciones (ADR-0009 D12); body estructurado `code/field` solo en validación 400 (ADR-0008 D11).
- **Repository**: método nuevo con `@AuthScope(Scope.CLUB, ...)` obligatorio (o `@NoAuthScope` + comentario justificativo + auditoría).
- **Entidad JPA**: separada del agregado, en `infrastructure/persistencia/`. Mapper `@Konverter` propio por par tipo-tipo. Columna nueva → migración compatible hacia atrás.
- **Migración**: `db/migration/{modulo}/V{YYYYMMDD}{NNNN}__{descripcion}.sql` con comentario de categoría RGPD (1-6) si crea tabla. Sin FK cruzando esquemas. Índice por `club_id`.

### 4. Tests (pirámide de testing-de-modulos.md)

| Test | Obligatorio | Patrón |
|------|-------------|--------|
| Unitario de dominio | Sí | Kotest `BehaviorSpec` + `shouldBeRight`/`shouldBeLeft<{Modulo}Error.X>`; sin Spring ni BD |
| Integración | Sí, si toca BD/listeners | `IntegrationTestBase` (Testcontainers Postgres) + `@Transactional` rollback |
| **Acceso cruzado** | **Sí, por cada caso de uso con nivel de objeto** | Dos principals del mismo club → `Forbidden`; dos clubes → repositorio devuelve `null` (ADR-0009 D14) |
| Idempotencia | Sí, si hay listener | Consumir el mismo evento dos veces → un solo efecto |
| Builders | Sí | Fluent con defaults válidos (`PlanSemanalBuilder().enBorrador().build()`); `TestPrincipals` para principals |

- Cobertura objetivo (ADR-0010): domain ≥ 90 %, application ≥ 80 %, infrastructure ≥ 60 % — sin sacrificar el catálogo de tests críticos del módulo (actualizar su tabla en el README de tests si la feature añade un caso crítico).
- ArchUnit y fronteras de Modulith ya corren en CI; no hay que añadir reglas salvo concepto nuevo.

## Política de excepciones (regla cerrada)

- **Negocio → `Either`, siempre.** Las "jerarquías de excepciones" de negocio no existen en este proyecto: la jerarquía es la sealed class `{Modulo}Error`.
- **Excepciones solo técnicas y solo en infrastructure**: lo que lance un SDK/driver se captura en el adaptador (`runCatching { ... }.onFailure { raise(...) }`) y se traduce a una variante del error del módulo.
- El `@RestControllerAdvice` captura excepciones de framework → 500 con cuerpo neutro.
- `require`/`check` lanzan `IllegalArgumentException`/`IllegalStateException` — correcto, porque son bugs, no flujos.

## Checklist final antes de entregar

- [ ] `domain` sin imports prohibidos (Spring/JPA/Jackson/SDKs) — Arrow sí permitido
- [ ] Caso de uso `@ApplicationService` que devuelve `Either` y autoriza en la primera línea
- [ ] Listener (si hay): idempotente + restaura `traceparent` + actualiza `last_processed_event_*` si toca proyección
- [ ] Repositorio con `@AuthScope`; consulta filtra por `club_id`
- [ ] Migración (si hay): backward-compatible, comentario RGPD, sin FK cruzada, índice `club_id`
- [ ] Test de acceso cruzado del caso de uso
- [ ] Métricas/MDC: el módulo ya emite `module={modulo}`; métricas de negocio nuevas vía Micrometer con tag `module`
- [ ] Nombres de dominio en castellano (glosario); `./gradlew detekt ktlintCheck` limpio
- [ ] No commitear automáticamente — dejar el diff para revisión

## Antipatrones

| Antipatrón | Por qué está prohibido |
|------------|------------------------|
| Lanzar excepciones para errores de negocio | ADR-0008 D11: el flujo de error es `Either` |
| Llamada síncrona a otro módulo | ADR-0007: events-first; Modulith parte el build |
| Leer tablas de otro esquema | Proyección local o nada (ADR-0004 D4) |
| `@PreAuthorize` de Spring Security | RBAC declarativo con la anotación propia `@Authorize` en el controller; nivel de objeto en el caso de uso, contra los puertos de consulta del módulo (ADR-0009 D7, D13) |
| Anotar clases de dominio con `@Entity`/`@Component` | Dominio puro; entidad JPA separada + Konvert |
| MapStruct / mapeo por reflection | Konvert compilado (ADR-0008 D6) |
| Editar una migración ya aplicada | Siempre migración nueva |
| `@Autowired` por campo | Inyección por constructor |
| Inglés en conceptos de dominio | Lenguaje ubicuo castellano (`docs/glosario.md`) |
| Mapper global que mapea todo | Un `@Konverter` por par tipo-tipo |
| Devolver `NotFound` cuando es denegación | Acceso a objeto ajeno del mismo club → `Forbidden`; otro club → el `@AuthScope` hace que no exista |

## Referencias

Material de consulta de esta skill:

- [referencias/kotlin-arrow.md](referencias/kotlin-arrow.md) — idioms Kotlin del proyecto, Either/Raise, errores sellados, value classes
- [referencias/patrones-disenio.md](referencias/patrones-disenio.md) — SOLID/Clean mapeados a la hexagonal, DDD táctico, Strategy/Factory idiomáticos
- [referencias/spring-boot.md](referencias/spring-boot.md) — prácticas Spring Boot 3.x del proyecto: transacciones, listeners, config, observabilidad
- [referencias/jvm-performance.md](referencias/jvm-performance.md) — GraalVM CE 25, GC, heap, leaks, thread pools, HikariCP, guía JMH
- [referencias/jpa-hibernate.md](referencias/jpa-hibernate.md) — N+1, fetch, batch, open-in-view, JSONB, proyecciones de lectura

Autoridad (si hay conflicto, gana el ADR):

- `docs/arquitectura/estructura-de-un-modulo.md` · `persistencia.md` · `testing-de-modulos.md`
- ADR-0004 (PostgreSQL), ADR-0007 (events-first), ADR-0008 (hexagonal + Either), ADR-0009 (autorización 3 capas), ADR-0010 (CI + cobertura), ADR-0011 (observabilidad), ADR-0013 (secretos), ADR-0014 (RGPD), ADR-0016 (runtime GraalVM)
- Skills hermanas: `module-scaffold`, `integration-event-creator`, `flyway-migration-checker`, `spring-modulith-debug`, `glosario-guardian`
