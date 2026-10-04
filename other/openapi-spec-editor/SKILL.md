---
name: openapi-spec-editor
description: >
  Guía cualquier cambio del contrato de API por el workflow contract-first de ADR-0001 D10:
  spec primero en api/openapi.yaml, clasificación aditivo vs breaking (breaking → PR propia
  etiquetada breaking-api), regeneración de clientes, implementación back+front en el mismo PR
  y revisión cruzada. Usar al añadir o modificar cualquier endpoint, campo o status code.
disable-model-invocation: false
---

# openapi-spec-editor — Runcriticon

`api/openapi.yaml` es **la fuente de verdad** del contrato (ADR-0001 D10). Esta skill impone el workflow que hace barato el contract-first: sin disciplina degenera en *"el back implementa y alguien actualiza la spec si se acuerda"* — el peor de los mundos, citado literalmente en el ADR.

## Cuándo usar esta skill

- Añadir un endpoint, campo, parámetro o status code.
- Cambiar o eliminar cualquier cosa del contrato.
- Crear la spec inicial (aún no existe — ver Bootstrap).
- **NO** para revisar semántica REST de un contrato ya escrito → `api-contract-review`.

## Argumentos

```
/openapi-spec-editor {descripcion-del-cambio}
```

Ej.: `/openapi-spec-editor añadir GET /grupos con filtro por tag`.

## Bootstrap (si `api/openapi.yaml` no existe)

Estado actual del repo: la spec **aún no existe**. La primera invocación la crea:

```yaml
openapi: 3.0.3
info:
  title: Runcriticon API
  version: 0.1.0
  description: API del MVP. Contract-first (ADR-0001 D10) — esta spec es la fuente de verdad.
servers:
  - url: /api          # mismo origen, sin /v1 (ADR-0001 D10/D11)
paths: {}
components:
  schemas:
    Error:             # shape de error 4xx (ADR-0008 D11, ADR-0012 D19)
      type: object
      required: [code, message]
      properties:
        code:    { type: string, description: "Código estable que el frontend traduce" }
        field:   { type: string, description: "Campo del formulario, si aplica" }
        message: { type: string, description: "Solo para debugging — el frontend NUNCA lo muestra" }
        details: { type: object, additionalProperties: true }
```

Avisar además de lo que el bootstrap NO hace: cablear los generadores en los builds (`ng-openapi-gen` como script npm en frontend; `openapi-generator` template `kotlin-spring` como plugin Gradle en backend; **el código generado no se commitea** — D10). Eso es una tarea de build propia; señalarla, no improvisarla.

## Workflow del cambio (orden vinculante)

1. **Editar la spec primero.** El cambio nace en `api/openapi.yaml`, no en el controller.
2. **Clasificar el cambio**:

   | Aditivo (mismo PR que la implementación) | Breaking (PR propia, etiqueta `breaking-api`) |
   |---|---|
   | Endpoint nuevo | Eliminar endpoint o campo |
   | Campo de respuesta nuevo | Cambiar tipo o formato de un campo |
   | Campo de request **opcional** nuevo | Hacer requerido un campo opcional (request) |
   | Status code nuevo documentado | Renombrar campo o cambiar URL |
   | Enum: valor nuevo (si el cliente tolera desconocidos) | Cambiar el significado de un status code |

   El PR `breaking-api` lleva análisis de impacto en el cuerpo: qué consumidores se rompen y cómo migran. En MVP el único consumidor es la SPA (se despliega junta — coste bajo), pero el etiquetado disciplina para cuando haya app móvil.
   **Nunca mezclar cambios breaking y no-breaking en el mismo PR.**

3. **Regenerar clientes** (cuando los generadores estén cableados): script npm en frontend, task Gradle en backend. CI verifica el alineamiento; los artefactos no se commitean.
4. **Implementar backend y frontend en el mismo PR** que la spec (cambios atómicos — D9 monorepo).
5. **Test de contrato en verde** — obligatorio para mergear (ADR-0010). Es lo único que impide que la spec derive de la realidad en silencio.
6. **Revisión cruzada obligatoria**: al menos un aprobador del lado opuesto al que origina el cambio (back↔front).

## Convenciones de la spec

- **Lenguaje ubicuo en castellano** en paths y schemas: `/alumnos`, `/planes/{planId}/publicar`, schema `ReporteSesion` (`docs/glosario.md`). Paths en kebab-case si son compuestos: `/reportes-sesion`.
- **Sin `/v1/`**: una sola URL `app.runcriticon.com/api/...`. El versionado se decide en un ADR nuevo cuando aparezca un segundo consumidor que no se despliegue con la SPA.
- **Errores 4xx** referencian el schema `Error` común; **403 con cuerpo neutro** (ADR-0009 D12 — sin filtrar el porqué).
- **Acciones que no son CRUD** como sub-recurso verbo en infinitivo: `POST /planes/{id}/publicar` (coherente con los casos de uso del dominio).
- **La propiedad de la spec es del que cambia el endpoint** (no hay owner único — D10); la intención se documenta en el PR.
- `operationId` estable y en castellano (`publicarPlan`) — es el nombre del método generado en ambos clientes.

## Antipatrones

- Implementar primero y "actualizar la spec luego" — el orden del PR es spec → regeneración → implementación → tests.
- Editar código generado a mano "porque pica una vez" — se sobreescribe y crea deriva silenciosa.
- Escribir un servicio HTTP a mano en el frontend en lugar de regenerar (frontend/CLAUDE.md lo prohíbe).
- Introducir `/v1/` preventivo "por si acaso".
- Colar un breaking disfrazado de aditivo (p. ej. estrechar un enum existente).
- Exponer el shape de una entidad JPA o de un agregado como schema — los DTOs del contrato son propios.

## Referencias

- ADR-0001 **D10** (contract-first: workflow, propiedad, coste asumido 15-30 min/PR), D9 (monorepo), D11 (mismo origen)
- ADR-0008 D11 / ADR-0012 D19 (shape de error estructurado), ADR-0009 D12 (cuerpo neutro en denegaciones)
- [api-contract-review](../api-contract-review/SKILL.md) — revisión semántica REST del contrato ya escrito
- [backend-feature-dev](../backend-feature-dev/SKILL.md) y [frontend-feature-dev](../frontend-feature-dev/SKILL.md) — la implementación a ambos lados del contrato
