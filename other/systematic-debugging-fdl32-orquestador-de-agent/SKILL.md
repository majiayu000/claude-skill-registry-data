---
name: systematic-debugging
version: 2.0.0
description: Proceso riguroso de cuatro fases para diagnosticar y corregir errores, priorizando la investigación de causa raíz y limitando los intentos iterativos ciegos a un umbral estricto. Usar cuando un error no es trivial y la causa no es obvia a primera vista. No usar para typos o fallos de linter (corrigelos directo).
author: agent
role: shared
stage: implement
cycle_phase: [F5-implementacion]
writes_memory: false
quality_gate: false
tags: [process, debugging, methodology]
triggers: [/debug, /systematic-debugging, debug]
---

# systematic-debugging

## Cuándo usar
- Ante errores inesperados o fallos en los tests que no tienen una causa evidente inmediata.
- Cuando la resolución requiere entender el flujo asíncrono o complejo del sistema.
- Tras el segundo intento fallido de corregir un error mediante ensayo y error.

## Cuándo NO usar
- Errores de linting estáticos directos (ej. violaciones de estilo de `ruff`) donde la corrección es mecánica.
- Errores de sintaxis reportados explícitamente por el compilador o intérprete.

---

## Pasos

### Fase 1 — Análisis de Patrón
1. Examina el stacktrace completo y el contexto del estado del sistema.
2. Identifica la función exacta y los componentes que fallan, sin asumir inmediatamente la culpa.

### Fase 2 — Investigación de Causa Raíz
1. Lee y analiza el código circundante y los tests asociados.
2. Formula una hipótesis mínima, técnica y comprobable sobre el origen del fallo.
   - ❌ Sin hipótesis clara → PROHIBIDO parchear ciegamente el código. PARA.

### Fase 3 — Implementación de Hipótesis Mínima
1. Aplica el cambio **más pequeño posible** en el código para validar la hipótesis.
2. Ejecuta el entorno de validación para contrastar el resultado:
   ```bash
   python scripts/run_pytest_safe.py
   ```

### Fase 4 — Control de Umbral (Límite de 3 Intentos)
Registra tus ciclos de intento-fallo para evitar el bucle infinito:
- **Intento 1-2:** Si el fallo persiste, descarta la hipótesis anterior, vuelve a la Fase 1 y formula una nueva.
- **Intento 3 (Fallo):** Si al tercer intento la solución falla, detén la iteración.
  - Asume que la premisa arquitectónica, el entendimiento del framework o el test en sí mismo es incorrecto.
  - Documenta todo lo hallado en `execution_log.md` y eleva la visibilidad al humano.
