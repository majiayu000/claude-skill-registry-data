---
name: sdd-design
description: >
  Traduce specs (QUÉ) en un plan técnico concreto (CÓMO). Documenta
  decisiones de arquitectura, data flow y cambios de archivos.
  Trigger: Después de sdd-spec para diseñar la implementación técnica.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: sdd-design

Diseño técnico. No solo "qué archivos tocar" sino "por qué esta solución".

## Trigger

- Los specs están listos y aprobados
- Necesitás decidir cómo implementar los specs
- Hay tradeoffs de arquitectura que discutir

## Workflow LEND

1. ANALIZAR
   ├── Specs: ¿qué escenarios tenemos que cumplir?
   ├── Stack actual: ¿qué herramientas y patrones ya existen?
   ├── Restricciones: tiempo, rendimiento, escalabilidad, mantenibilidad
   └── Alternativas: pensar 2+ enfoques antes de decidir

2. OFRECER (Menú del Senior)
   ├── A) Diseño simple — qué archivos crear/modificar, en qué orden
   ├── B) Diseño con ADR — archivos + data flow + decisiones documentadas
   └── C) Diseño detallado — archivos + interfaces + data flow + ADR + diagrama

3. ELEGIR → confirmación

4. HACER
   ├── Listar archivos a crear, modificar y eliminar
   ├── Diagramar data flow (entradas, procesos, salidas)
   ├── Documentar decisiones: "elegí X sobre Y porque..."
   ├── Definir interfaces y contratos entre módulos
   └── ADR: registrar decisión con contexto, opciones y resultado

5. VERIFICAR
   ├── El diseño cubre todos los escenarios de los specs
   ├── Las decisiones están justificadas
   └── Cualquier dev puede implementar a partir del diseño
