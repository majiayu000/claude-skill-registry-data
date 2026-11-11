---
name: contrato-api
description: Cómo documentar y versionar el contrato HTTP con el frontend en las APIs de la plantilla base — forma de BaseResponse y de los errores, el documento docs/frontend-<tema>.md con requests, respuestas y mensajes exactos, el CHANGELOG con versionado semántico del contrato (MAJOR/MINOR/PATCH) y qué cuenta como cambio que rompe. Usar al crear o cambiar un endpoint, un DTO, un mensaje de error o un código de error, al preparar un release, o cuando se pida documentar algo para el equipo del front.
---

# Contrato con el frontend

Lo que se versiona es el **contrato HTTP**, no el código interno. Todo cambio que el front pueda
notar (una ruta, un campo, un código de error, un mensaje que se muestra, un cálculo que cambia de
significado) se documenta **en el mismo cambio** que lo introduce.

## Forma de las respuestas

Todo endpoint responde `BaseResponse<T>`:

```json
{ "success": true, "code": "OK", "message": "…", "response": { … }, "error": null }
```

Errores (los arma `ExceptionMiddleware`):

```json
{
  "success": false,
  "code": "VALIDATION_ERROR",
  "message": "Primer error. | Segundo error.",
  "response": null,
  "error": { "code": "VALIDATION_ERROR", "message": "…", "traceId": "…", "errors": ["BusinessException"] }
}
```

| HTTP | Cuándo | Qué hace el front |
|---|---|---|
| 200 | Éxito; también un proceso por lotes con filas en error (el error va en la fila) | Muestra el resultado |
| 400 `VALIDATION_ERROR` | El Validator rechazó; los mensajes van unidos con ` \| ` | Muestra `message` al usuario |
| 400 otro código | Regla de negocio en el InputPort | Muestra `message`; decide por `code` |
| 403 | Sin permiso de pantalla, o sin alcance sobre el recurso (código propio) | Avisa; **no** cierra sesión |
| 401 | Solo sesión vencida o token inválido | Cierra sesión |
| 404 | El recurso no existe | Avisa |

Reglas:

- Los mensajes de error están escritos para el **usuario final**, en español, y el front los muestra
  tal cual: dicen qué está mal y cómo corregirlo.
- El front decide por `code`, nunca por el texto.
- En procesos por lotes (importaciones, masivas), un error de una fila **no** es un 4xx: la fila
  sale con su estado de error y su mensaje, y las demás se procesan.

## Documento para el front: `docs/frontend-<tema>.md`

Uno por funcionalidad o por cambio grande. Escrito para quien consume la API, no para quien la
programa:

1. **Qué cambió y por qué**, en dos o tres frases.
2. **Por endpoint:** método y ruta, permiso, request (con ejemplo), respuesta exitosa (con
   ejemplo) y **cada error posible con su mensaje exacto**.
3. **Antes y ahora**, cuando cambia algo que ya existía.
4. **Qué tiene que ajustar el front**, como lista de tareas.

- Los ejemplos JSON son reales: los nombres de campos en camelCase, tal como serializa la API.
- Si un campo queda obsoleto pero se mantiene por compatibilidad, decirlo ("se mantiene, siempre
  llega en `false`").
- Si el cambio toca un documento existente, se actualiza ese, no se crea otro que lo contradiga.

## CHANGELOG.md

Formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/), con todo lo pendiente en
`## [Unreleased]` y secciones `### Agregado`, `### Cambiado`, `### Corregido`, `### Eliminado` y
`### Base de datos`.

| Versión | Cuándo |
|---|---|
| **MAJOR** | Rompe al front: endpoint eliminado o renombrado, cambio incompatible en un DTO, cambio en la forma de `BaseResponse<T>`, permiso retirado, un caso que antes respondía 200 y ahora 4xx, o un cálculo que cambia de significado para datos existentes |
| **MINOR** | Compatible hacia atrás: endpoint nuevo, campo nuevo en una respuesta, reporte o política nueva |
| **PATCH** | Corrección sin tocar el contrato |

- Cada entrada dice **qué** cambió y, si no es obvio, **por qué**, en una o dos frases.
- `### Base de datos` lista las migraciones que arrastra el release.
- Al publicar: mover `[Unreleased]` a la versión con su fecha y actualizar `<Version>` en el
  `.csproj` con el mismo número del tag.

## Antes de dar un cambio por terminado

- [ ] ¿El front lo nota? Entonces está en `docs/frontend-<tema>.md` y en el `CHANGELOG`.
- [ ] Cada mensaje de error nuevo está copiado **exacto** en el documento.
- [ ] Si un caso que respondía 200 ahora responde 4xx, está marcado como cambio que rompe.
- [ ] Si hay migración, está en `### Base de datos`.
