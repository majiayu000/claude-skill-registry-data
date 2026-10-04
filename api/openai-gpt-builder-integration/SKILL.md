---
name: openai-gpt-builder-integration
description: Configura un Custom GPT en OpenAI GPT Builder de forma completa y verificable a partir de artefactos del repositorio. Use when the user asks to integrate, publish, leave ready, or validate a fully configured GPT in OpenAI, including actions, instructions, capabilities, starters, and smoke tests.
---

# OpenAI GPT Builder Integration

## Purpose

Integrar y dejar operativo un Custom GPT en OpenAI GPT Builder usando la fuente del repositorio, con evidencia de configuracion y pruebas de humo.

## Inputs Expected

- Repositorio fuente (normalmente `Calculadora-BMC` y/o `Calculadora-BMC-GPT`).
- Archivos de configuracion GPT:
  - instrucciones (`gpt/instructions/*.md`)
  - acciones OpenAPI (`gpt/actions/*.yaml`)
  - ejemplos de payload (`gpt/examples/*.md`)
  - checklist operativo (`docs/builder-setup-checklist.md` si existe)
- Entorno de destino: GPT Builder en OpenAI (UI web).

Si faltan archivos clave, detectarlo temprano y proponer la correccion antes de seguir.

## Mandatory Execution Rules

1. No inventar URLs, operationIds ni esquemas: siempre leer desde repositorio.
2. No declarar "configurado" sin validacion funcional minima.
3. Mantener un solo paso `in_progress` a la vez.
4. Si la UI de OpenAI cambia, adaptar el flujo pero conservar objetivos de verificacion.
5. Cuando haya ambiguedad (por ejemplo, auth de Actions), pedir confirmacion puntual.
6. Mantener respuestas operativas y concisas en espanol (salvo pedido contrario).

## Workflow

Copiar esta lista y mantenerla actualizada durante la ejecucion:

```text
Builder Integration Progress:
- [ ] 1. Relevar artefactos fuente
- [ ] 2. Validar prerequisitos tecnicos
- [ ] 3. Configurar identidad e instrucciones del GPT
- [ ] 4. Cargar y validar Actions (OpenAPI + auth)
- [ ] 5. Configurar capabilities y conversation starters
- [ ] 6. Ejecutar smoke tests conversacionales
- [ ] 7. Emitir reporte final de estado
```

### 1) Relevar artefactos fuente

- Identificar archivos canonicos:
  - `gpt/instructions/system.md`
  - `gpt/instructions/session-qualification.md`
  - `gpt/instructions/manual-gates.md`
  - `gpt/instructions/maintenance.md`
  - `gpt/actions/openapi.yaml` (y variantes si aplican)
- Consolidar una matriz "esperado vs observado" para:
  - identidad GPT (nombre, descripcion, tono)
  - instrucciones del sistema
  - acciones y operationIds esperados
  - starters

### 2) Validar prerequisitos tecnicos

- Confirmar que cada OpenAPI tenga:
  - servidor de produccion valido
  - `operationId` estable y unico
  - respuestas de error JSON (`400/401/500` segun aplique)
  - referencias sin ruptura
- Confirmar endpoints alcanzables en entorno objetivo (si corresponde).
- Si hay bloqueos, frenar y documentar "bloqueante + accion propuesta".

### 3) Configurar identidad e instrucciones del GPT

En GPT Builder:

1. Definir nombre y descripcion final.
2. Pegar instrucciones unificadas desde archivos fuente.
3. Verificar inclusion explicita de:
   - flujo de decision (intake -> qualify -> quote -> persist -> approve)
   - politicas de seguridad de herramientas
   - contrato de confirmacion manual (`CONFIRMATION::...`)
   - manejo de errores y degradacion controlada

### 4) Cargar y validar Actions (OpenAPI + auth)

Para cada accion:

1. Importar especificacion OpenAPI correcta.
2. Configurar autenticacion en Builder (API key, bearer u otro esquema definido).
3. Ejecutar prueba basica de invocacion desde Builder.
4. Validar que los errores retornen JSON parseable.

Si aparece `Failed to Parse JSON`:

- inspeccionar respuesta real del endpoint
- confirmar `content-type: application/json`
- validar estructura de body y schema OpenAPI

### 5) Configurar capabilities y conversation starters

- Activar solo capacidades necesarias para el caso de uso.
- Cargar starters alineados con escenarios reales del negocio.
- Evitar starters genericos que no ejerzan Actions.

### 6) Ejecutar smoke tests conversacionales

Correr pruebas minimas:

1. Caso feliz: cotizacion completa sin errores.
2. Caso con dato faltante: el GPT solicita aclaracion y no inventa.
3. Caso de error backend: reporta error entendible y accion siguiente.
4. Caso de confirmacion manual: exige contrato `CONFIRMATION::...` antes de avanzar.

Registrar para cada prueba: entrada, accion llamada, resultado, estado (PASS/FAIL).

### 7) Emitir reporte final de estado

Entregar:

1. Estado de configuracion en Builder (listo/no listo).
2. Brechas pendientes (si existen) con prioridad.
3. Evidencia resumida de smoke tests.
4. Proximos pasos de go-live.

## Final Output Format

Responder siempre con esta estructura:

1. Estado final en OpenAI GPT Builder
2. Configuracion aplicada (identidad, instrucciones, actions, capabilities, starters)
3. Resultados de smoke tests (PASS/FAIL)
4. Bloqueantes o riesgos residuales
5. Siguientes pasos recomendados

## Additional Resources

- Builder field mapping and validation checklist: [reference.md](reference.md)
- Practical setup and testing examples: [examples.md](examples.md)
