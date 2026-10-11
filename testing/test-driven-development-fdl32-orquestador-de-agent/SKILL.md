---
name: test-driven-development
version: 2.0.0
description: Metodologia Red/Green/Refactor que escribe el test primero, el codigo minimo despues y refactoriza, para cumplir los requisitos sin regresiones. Usar cuando se implementa logica nueva o se corrige un bug determinista reproducible. No usar para PoC exploratorios, tareas solo documentales ni refactors puros cubiertos por la suite.
author: agent
role: shared
stage: implement
cycle_phase: [F5-implementacion]
writes_memory: false
quality_gate: false
tags: [process, testing, methodology]
triggers: [/tdd, /test-driven, tdd]
---

# test-driven-development

## Cuándo usar
- Implementación de nuevas funcionalidades lógicas.
- Resolución de bugs deterministas reproducibles.

## Cuándo NO usar
- Exploración de viabilidad (PoC) o prototipado exploratorio.
- Tareas de sólo documentación o análisis técnico.
- Refactorizaciones estructurales puras (donde la suite de tests ya existe y garantiza el comportamiento).

---

## Pasos

### Paso 1 — Red (Escribir un test que falle)
1. Escribe el test unitario o de integración para capturar el nuevo requisito o bug.
2. Ejecuta los tests del proyecto:
   ```bash
   python scripts/run_pytest_safe.py
   ```
3. Verifica que el test falla.
   - ✅ Falla por la razón esperada → OK.
   - ❌ Pasa o falla por un error sintáctico → Corrige el test. PARA.

### Paso 2 — Green (Hacer pasar el test)
1. Escribe el código de producción **mínimo necesario** para que el test pase. No racionalices ni añadas código defensivo no cubierto.
2. Ejecuta nuevamente los tests:
   ```bash
   python scripts/run_pytest_safe.py
   ```
3. Verifica el resultado.
   - ✅ Pasa → OK.
   - ❌ Sigue fallando → Simplifica tu implementación. PARA.

### Paso 3 — Refactor (Mejorar diseño)
1. Limpia el código, elimina duplicaciones e incrementa la legibilidad sin alterar el comportamiento.
2. Ejecuta el quality gate completo para asegurar que no hay regresiones ni violaciones de estilo:
   ```bash
   ruff check .
   python scripts/run_pytest_safe.py
   ```
3. Verifica que todo el proyecto sigue en verde.
   - ✅ Todo OK → Ciclo terminado.

## Anti-Racionalizaciones
- "Escribo la implementación primero porque la tengo muy clara" → Prohibido bajo este skill.
- "Añado esta lógica ahora que estoy editando este archivo" → Prohibido si no hay un test que lo justifique.
