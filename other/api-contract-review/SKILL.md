---
name: api-contract-review
description: Revisa los contratos de la API REST en cuanto a semántica HTTP, compatibilidad hacia atrás y coherencia de las respuestas. Úsala cuando el usuario solicite «revisar la API», «comprobar endpoints» o «revisión REST», o antes de publicar cambios en la API. Para editar o crear la spec OpenAPI con el workflow contract-first, usar openapi-spec-editor.
---

# API Contract Review — Runcriticon

Audita controllers y la spec `api/openapi.yaml` contra los patrones del proyecto: lenguaje ubicuo en castellano, `Either<{Modulo}Error, T>` → HTTP vía `toResponse()`, `@Authorize` en handlers, y política de versionado del MVP (ADR-0001 D10). Cruce: ADR-0001 D10, ADR-0008 D11, ADR-0009 D12/D13, ADR-0012 D14/D19.

## Cuándo usar

- Antes de publicar cambios en `api/openapi.yaml` o en cualquier `*Controller.kt`.
- Al revisar un PR con nuevos endpoints o modificación de DTOs.
- Cuando el usuario pide «revisar la API», «comprobar endpoints» o «compatibilidad hacia atrás».

> Para crear o editar la spec OpenAPI, usar `openapi-spec-editor`.

## Problemas bloqueantes

| Problema | Síntoma | Cruce |
|---|---|---|
| Breaking sin etiquetar | Eliminar/renombrar campo/endpoint en PR normal | ADR-0001 D10 — requiere PR propia con label `breaking-api` |
| Handler sin `@Authorize` | Handler público sin `@Authorize` ni `@NoAuthRequired` | ADR-0009 D13 — ArchUnit lo detecta en CI |
| Entity leak | Clase `@Entity` o `domain` en el body de respuesta | ADR-0008 D11 — solo DTOs en `api/` |
| `Either` aplanado a mano | `when (result)` en el controller | El patrón es `result.toResponse()` — el `when` va en `toResponse` |
| Anglicismo en ruta/DTO | `/api/workouts`, `class WorkoutDto` | ADR-0008 — lenguaje ubicuo en castellano; usar `sesion`, `plan`, `alumno` |
| 403 con detalle de motivo | Body 403 describe por qué se deniega | Security leak — el body de 403 debe ser neutro |

## Either → HTTP: el contrato de status codes

Toda la traducción de error a HTTP vive en la extensión `toResponse()`. El controller solo llama:

```kotlin
@GetMapping("/{id}")
@Authorize("PLAN:LEER")
fun obtener(@PathVariable id: UUID): ResponseEntity<*> =
    servicio.obtener(PlanId(id)).toResponse()
```

El `when` exhaustivo sobre `{Modulo}Error` está en `toResponse()`, no en el controller. Revisar que el controller **no** tenga:
- `when (result) { is Either.Left -> ... is Either.Right -> ... }` inline
- `try/catch` sobre el caso de uso
- Llamadas a `ResponseEntity.status(...)` directas

### Mapeo canónico Either → HTTP

| `{Modulo}Error` | HTTP | Notas |
|---|---|---|
| `NotFound` | 404 | Solo si el recurso es propio del club; si es de otro club → 404 también (no 403, para no filtrar) |
| `Forbidden` | 403 | Body neutro: `{"code":"FORBIDDEN"}` — sin detallar el motivo |
| `InvalidInput(campo, motivo)` | 400 | Body incluye `field` y `message` |
| `Conflict` | 409 | |
| `ProjectionStale` | 503 | Autorización fail-closed (ADR-0009 D9) |

### Shape del error 4xx

```json
{
  "code": "PLAN_NOT_FOUND",
  "field": null,
  "message": "El plan solicitado no existe",
  "details": []
}
```

- `code`: legible por máquina; el frontend lo traduce — **nunca muestra `message` directamente al usuario**.
- `field`: presente en errores de validación (`InvalidInput`), `null` en el resto.
- El body de **403 es siempre neutro** — no filtrar si el objeto existe pero pertenece a otro club.

## Semántica HTTP

Solo verificar lo que el modelo no puede inferir del contexto: el proyecto no usa `@ResponseStatus` en las clases de dominio, el status correcto sale de `toResponse()`. Confirmar que:

- `POST` de creación devuelve `201 Created` con `Location` header.
- `DELETE` devuelve `204 No Content`.
- `GET` no tiene efectos secundarios — si cambia estado, debe ser `POST`/`PATCH`.
- `PUT`/`PATCH` son idempotentes tal como están implementados.

## Versionado de API (ADR-0001 D10)

**Sin `/v1/`** en el MVP — único consumidor es la SPA del monorepo, se despliega junto al backend. No marcar como problema la ausencia de prefijo de versión: es la decisión vigente.

Lo que sí se revisa:
- Cambios **breaking** (eliminar campo/endpoint, cambiar tipo, renombrar, cambiar status code) van en **PR propia con label `breaking-api`** y análisis de impacto — nunca mezclados con cambios aditivos.
- La spec `api/openapi.yaml` debe cambiar **en el mismo PR** que la implementación.
- Cambios aditivos son tolerantes: el cliente generado ignora campos nuevos.

Disparador de reapertura: cuando aparezca un segundo consumidor desacoplado del ciclo de release de la SPA.

## Checklist de revisión

### Autorización y seguridad
- [ ] Cada handler público tiene `@Authorize("RECURSO:ACCION")` o `@NoAuthRequired(justificacion = "...")` (ADR-0009 D13)
- [ ] Body de 403 es neutro; el recurso de otro club devuelve 404, no 403 (ADR-0009 D12)
- [ ] Sin stack traces en el body de respuesta de errores

### Diseño del contrato
- [ ] Rutas y DTOs en lenguaje ubicuo castellano (ADR-0008): `/planes/{id}/publicar`, `class PlanDto`, `alumnoId`
- [ ] Solo DTOs en `infrastructure/rest/dto/` expuestos en la API — nada de clases de `domain`
- [ ] `toResponse()` centraliza la traducción `Either → HTTP`; el controller no hace `when` sobre el `Either`
- [ ] Colecciones con paginación si pueden crecer más de ~50 elementos

### Compatibilidad
- [ ] Sin cambios breaking mezclados con cambios aditivos (ADR-0001 D10)
- [ ] PR de breaking lleva label `breaking-api` y análisis de impacto
- [ ] La spec `api/openapi.yaml` refleja los cambios del PR

### Coherencia con la spec
- [ ] Los tipos, nombres de campo y status codes del controller coinciden con `api/openapi.yaml`
- [ ] Ningún endpoint implementado sin spec, ni spec sin implementación

## Formato del informe

```markdown
## API Contract Review — {fichero / PR}

### ❌ Bloqueantes
- Handler `POST /planes/{id}/publicar` sin `@Authorize` (ADR-0009 D13)

### ⚠️ Advertencias
- DTO `PlanResponse` expone campo `entrenadorId` no declarado en openapi.yaml

### ✅ Sin problemas
- Semántica HTTP, versionado, shape de errores

### Conclusión
REQUIERE CAMBIOS / CONTRATO CORRECTO
```
