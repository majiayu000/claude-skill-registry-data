---
name: armar-swagger
description: >-
  (Repo back · desarrollo) Consolidar los fragmentos de Contrato OpenAPI que cada
  Tarea del tablero dejó escritos, en un único openapi.yaml del slice; correr Spectral
  (linter de OpenAPI) y publicar Swagger UI. El contrato queda como fuente para el
  backend (lo valida/implementa) y el frontend (lo simula a partir del contrato). Usar cuando se
  pida "armá el swagger", "consolidá el contrato del slice", "generá el openapi.yaml",
  "/armar-swagger". NO inventa endpoints: solo junta lo que las Tareas ya
  especificaron. Español (Argentina).
---

# Armar swagger (backend)

Junta los fragmentos OpenAPI de las Tareas de un slice en un contrato único, lo valida
y lo publica. No diseña la API (eso lo cerró cada Tarea): consolida, valida y expone.

## Regla de oro
- **NO INVENTAR endpoints ni campos.** Si un fragmento está incompleto, se marca
  `⚠ pendiente` y se pregunta; no se completa por suposición.
- **Una sola fuente:** el `openapi.yaml` de la raíz del repo, versionado, que se consolida
  slice por slice (cada slice suma sus paths).
- **Un solo contrato:** el servidor sirve **ese mismo** `openapi.yaml` en `/swagger`, sin
  generar un segundo contrato a partir del código. Si el framework generara otro a partir de las
  anotaciones, habría dos contratos que pueden diferir: un endpoint o campo distinto entre el
  código y el `openapi.yaml` es un hallazgo.
- **Spectral manda:** si el linter falla, el contrato no se da por bueno.
- **Español (Argentina).**

## Flujo
1. Reunir los fragmentos `paths:` de las Tareas del slice (del contrato de cada Tarea).
2. Fusionar en `openapi.yaml` (info + paths + components/schemas), sin duplicar.
3. Correr el linter de OpenAPI (**Spectral**) con el ruleset `bin/spectral-oas.yaml` del
   repositorio del Cerebro; resolver hallazgos.
4. Publicar **Swagger UI** apuntando al yaml consolidado.
5. Dejar el contrato como fuente: back lo valida/implementa, front lo simula a partir de él.

## Entrada / Salida
- **Entrada:** fragmentos OpenAPI de las Tareas del slice.
- **Salida:** `openapi.yaml` validado + Swagger UI navegable.

## Barreras
- No agrega paths que ninguna Tarea especificó.
- Si dos Tareas definen el mismo endpoint distinto, es choque → se frena y se pregunta
  (ese chequeo lo hace `analizar-tareas` en el repo de conocimiento, antes de llegar acá).
