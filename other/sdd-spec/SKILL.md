---
name: sdd-spec
description: >
  Escribe especificaciones técnicas en Given/When/Then. Describe QUÉ debe
  hacer el sistema, no CÓMO.
  Trigger: Después de sdd-propose para escribir o actualizar los specs del cambio.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: sdd-spec

Especificaciones técnicas. Si podés escribir un test a partir de un escenario, el spec está bien.

## Trigger

- La propuesta está aprobada
- Necesitás detallar el comportamiento esperado
- Hay que actualizar specs existentes por un cambio

## Workflow LEND

1. ANALIZAR
   ├── Propuesta: ¿qué dijimos que íbamos a hacer?
   ├── Alcance: ¿qué entra y qué NO entra en esta spec?
   ├── Escenarios: caso feliz, casos borde, errores
   └── Dependencias: ¿esto afecta a otras specs?

2. OFRECER (Menú del Senior)
   ├── A) Specs en lenguaje natural — Given/When/Then en markdown, sin tecnicismos
   ├── B) Specs formales — Gherkin, con ejemplos concretos y tablas de decisión
   └── C) Specs + tests — escenarios + esqueleto de tests para cada uno

3. ELEGIR → confirmación

4. HACER
   ├── Formato: Given (contexto), When (acción), Then (resultado esperado)
   ├── Cubrir: caso feliz, casos borde, errores, performance si aplica
   ├── Especificar: QUÉ debe pasar, no CÓMO implementarlo
   ├── Ejemplos concretos: datos de entrada y salida esperada
   └── Contract: si hay API, especificar request/response

5. VERIFICAR
   ├── Cada escenario es testeable
   ├── No hay ambigüedad en los criterios
   └── Los specs describen comportamiento, no implementación
