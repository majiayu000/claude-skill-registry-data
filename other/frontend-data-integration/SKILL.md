---
name: frontend-data-integration
description: "Analiza o implementa integraciones de datos entre frontend y backend respetando el patrón real del repositorio. Usa esta skill cuando la tarea implique leer, enviar o persistir datos; revisar services, clients, handlers, repositories, rutas API, payloads o contratos; o detectar dependencias backend, uploads, adjuntos, permisos o persistencia real. Cargala antes de modificar cualquier service o hook de datos, si la feature requiere nuevos campos en el payload, no asumir que el backend los acepta sin haberla cargado primero."
---

## Propósito

Resolver integraciones de datos sin imponer una arquitectura externa y sin presentar una solución local como si fuera una integración completa.

## Cuándo usarla

Usala cuando la tarea implique:

- cuando una feature de UI requiera subir, adjuntar, enviar o persistir información más allá del estado local, o cuando quede parcialmente preparada por una dependencia backend pendiente;
- services, API clients, handlers, repositories, rutas API, payloads, DTOs o contratos;
- archivos, adjuntos, uploads, multipart o `FormData`;
- permisos, validaciones de servidor o dependencias backend;
- revisión de carpetas o archivos vinculados con `services`, `api`, `clients`, `handlers`, `repositories` o equivalentes.

## Reglas

- No inventes endpoints, campos, permisos ni contratos como si ya existieran.
- Si hacen falta, proponelos explícitamente como **requerimientos backend a validar**, no como hechos.
- Reutilizá los services, clients, handlers, repositories, hooks o helpers existentes cuando corresponda.
- No saltees capas que el repo ya usa para auth, errores o configuración.
- Mantené naming, manejo de errores, serialización y tipos alineados con el proyecto.
- Diferenciá:
  - implementación completa;
  - implementación frontend parcial;
  - dependencia backend pendiente.
- Si el frontend queda parcialmente preparado y la implementación completa depende de backend, leé `references/frontend-follow-up-after-backend.md` y devolvé el bloque **Siguiente paso Frontend cuando BE esté listo**.
- Si la tarea involucra archivos, adjuntos, uploads, multipart o `FormData`, consultá la referencia específica de uploads antes de cerrar la solución.
- Si detectás una dependencia backend pendiente, consultá las referencias de handoff correspondientes y devolvé de forma explícita:
  - **Mensaje para Backend**;
  - **Siguiente paso Frontend cuando BE esté listo**, si la implementación FE queda parcial.

## Referencias a consultar según el caso

- Si necesitás identificar el patrón de integración del repo, leé `references/pattern-detection.md`.
- Si el proyecto usa Next.js con handlers o rutas API intermedias, leé `references/nextjs-service-handler.md`.
- Si detectás que la solución requiere un cambio backend real o un contrato todavía no confirmado, leé `references/backend-handoff.md`.
- Si el frontend queda parcialmente preparado a la espera de backend, leé `references/frontend-follow-up-after-backend.md`.

## Modos de resolución

### A. Dependencia backend detectada

Cuando el frontend puede avanzar parcialmente pero el backend aún no existe o no está confirmado:

- implementá solo lo que sea honesto implementar del lado FE;
- dejá explícito qué falta del backend;
- agregá el bloque **Mensaje para Backend**;
- agregá el bloque **Siguiente paso Frontend cuando BE esté listo**.

### B. Contrato existente

Cuando el repo ya tiene endpoint, service, client o handler equivalente:

- reutilizá el patrón;
- conectá la UI o feature;
- no abras una nueva vía de integración innecesaria.

### C. Nueva integración con contrato definido

Cuando el backend ya fue especificado:

- implementá service/client/handler o la capa correspondiente;
- integrá el consumidor;
- mantené el contrato tipado y visible.

## Salida esperada

La respuesta debe dejar claro:

- qué patrón de integración se detectó;
- qué se implementó;
- qué se asumió;
- qué queda pendiente del backend, si aplica;
- qué debe conectarse luego en frontend, si aplica.
