---
name: refactor-manager
version: 2.0.0
description: Dirige una refactorizacion segura de codigo Python en 5 fases (analisis, plan, refactor, validacion, iteracion) con los cambios aprobados antes de ejecutarse. Usar cuando hay que reestructurar codigo sin cambiar su comportamiento. No usar para un fix puntual (ver systematic-debugging) ni para una funcionalidad nueva (ver manager-create-work-plan).
triggers: [/refactor, refactor-manager, refactor]
author: agent
role: shared
stage: review
cycle_phase: [F5-implementacion]
writes_memory: false
quality_gate: false
tags: [core, system]
---

# refactor-manager

Skill para que Manager dirija refactorización segura de código Python, reduciendo riesgo y manteniendo invariantes.

Basado en protocolo de Principal Engineer: separación estricta entre análisis, plan y ejecución.

## Overview

El Manager usa esta skill para refactorizar código de forma controlada:

1. **Fase 1 (Análisis):** el agente lee código, identifica problemas, documenta hallazgos (sin modificar)
2. **Fase 2 (Plan):** Manager revisa hallazgos y aprueba cambio mínimo propuesto
3. **Fase 3 (Refactor):** el agente ejecuta SOLO cambios aprobados
4. **Fase 4 (Validación):** Tests + ruff + regresión verifican cero impacto
5. **Fase 5 (Iteración):** Si fallos, el agente propone fix mínimo (no reescribir)

**Invariante:** Nunca cambiar comportamiento observable sin aprobación explícita.

## Workflow

### Prerequisitos
- Archivo target identificado (path absoluto o relativo)
- Manager disponible para revisar plan (fase 2)
- Proyecto con tests + ruff configurado

### Paso 1: Verificar Turno
```bash
python .agent/agent_controller.py
```
Si rol es BUILDER, informar al usuario: "Este skill es para Manager".

### Paso 2: Cargar Contexto
Leer en orden:
1. `.agent/rules/manager/refactoring-protocol.md` - reglas y protocolo
2. Archivo target - entender código actual
3. Casos de uso existentes - identificar invariantes

### Paso 3: Ejecutar FASE 1 — Análisis

**Objetivo:** Entender antes de tocar.

Tarea para el agente:
```
Analiza este archivo: [path]

NO MODIFIQUES NADA. Solo documenta:
1. ¿Qué hace el código?
2. ¿Cuáles son las responsabilidades?
3. Detecta:
   - Acoplamiento innecesario
   - Complejidad sin justificación
   - Duplicidad de código
   - Code smells (nombres confusos, funciones grandes, etc)
4. ¿Cuáles son los invariantes? (comportamiento que no puede cambiar)
5. ¿Hay incertidumbres? Márcalas como HIPÓTESIS

Salida:
[Análisis]
- ¿Qué hace?
- Responsabilidades
- Problemas detectados
- Invariantes
- Hipótesis/incertidumbres
```

El agente entrega reporte de análisis (NO código modificado).

**REGLA CRÍTICA:** Si hay dudas en fase 1 -> DETENERSE y preguntar.

### Paso 4: Manager Revisa Análisis

Manager lee reporte y decide:
- **CONTINUAR:** Acepta análisis, propone refactor mínimo
- **PROFUNDIZAR:** Pide análisis más detallado de ciertos aspectos
- **RECHAZAR:** El alcance es demasiado amplio o riesgoso

Si continuar, pasar a FASE 2.

### Paso 5: Ejecutar FASE 2 — Plan

**Objetivo:** Definir el cambio mínimo útil.

Tarea para el agente:
```
Basándote en el análisis previo, propone UN refactor pequeño:

1. ¿Cuál es el cambio propuesto?
2. ¿Por qué mejora el código?
3. ¿Qué NO se va a tocar?
4. ¿Cuáles son los riesgos?
5. ¿Cómo validaremos que no se rompió nada?

Alternativas descartadas (y por qué):
- [alternativa 1] Descartada - Razón
- [alternativa 2] Descartada - Razón

Salida:
[Plan]
- Cambio propuesto
- Justificación
- Qué no se toca
- Riesgos
- Estrategia de validación
```

El agente entrega propuesta de plan (sin código).

### Paso 6: Manager Aprueba Plan

Manager lee plan y decide:
- **APROBADO:** Procede a FASE 3
- **AJUSTES:** Pide cambios al plan (scope, riesgos, etc)
- **RECHAZADO:** Plan no cumple criterios

Si no aprobado, iterar Fase 2 o abandonar.

### Paso 7: Ejecutar FASE 3 — Refactor

**Objetivo:** Aplicar SOLO el cambio definido.

Tarea para el agente:
```
Implementa el plan aprobado:

1. Lee el código original
2. Aplica SOLO los cambios del plan (sin extras)
3. Mantén invariantes intactos
4. Código debe ser:
   - Completo (no fragmentos rotos)
   - Consistente con el proyecto
   - Legible

Salida: Código modificado listo para validación
```

El agente entrega código refactorizado.

**REGLA:** Si tentación de hacer "un cambio más" → DETENER y documentar para próxima iteración.

### Paso 8: Ejecutar FASE 4 — Validación

**Objetivo:** Demostrar que no se rompió nada.

Tarea para el agente + sistemas automáticos:
```
Valida que el refactor no rompe nada:

1. Syntax check: python -m py_compile [archivo]
2. Imports: python -c "import [módulo]"
3. Linting: ruff check [archivo]
4. Tests:
   - ¿Qué tests existentes usan este código?
   - ¿Todos los tests pasan?
   - ¿Coverage se mantiene?
5. Regresión manual:
   - Casos felices (happy path)
   - Edge cases
   - Error handling
6. Comportamiento observable:
   - ¿El código hace exactamente lo mismo que antes (desde afuera)?

Salida:
[Validación]
- Casos a testear
- Tests sugeridos (si hay gaps)
- Resultado: PASS / FAIL / PARCIAL
- Riesgos abiertos (si hay)
```

Si FAIL → pasar a FASE 5. Si PASS → refactor completado exitosamente.

### Paso 9: Ejecutar FASE 5 — Iteración (si hay errores)

**Objetivo:** Corregir sin reescribir.

Si tests fallan:
```
1. Analiza causa raíz:
   - ¿Qué test falla exactamente?
   - ¿Por qué? (síntomas vs causa real)
   - ¿Es el refactor o era pre-existente?

2. Propone fix MÍNIMO:
   - Una línea si posible
   - Máximo 3-5 líneas
   - NUNCA reescribir funciones completas

3. Aplica fix y reintentar validación

4. Si sigue fallando después de 2 intentos:
   → Reportar y abandonar el refactor
   → Documentar bloqueador
```

**REGLA:** Si necesitas reescribir > 20% del código del plan → DETENER. El plan fue deficiente.

### Paso 10: Manager Aprueba o Rechaza

Manager revisa:
1. Código refactorizado (lectura directa, no confíes en logs)
2. Reporte de validación
3. Hallazgos de cada fase

Decisión final:
- **APROBADO:** Refactor listo para merge/commit
- **RECHAZADO CON FEEDBACK:** Documento qué cambiar, reintentar
- **CANCELADO:** Aprendizajes documentados para futuro

## Invariantes NO Negociables

**PROHIBIDO:**
1. Cambiar comportamiento observable sin autorización explícita
2. Modificar APIs públicas o contratos externos
3. Introducir dependencias nuevas sin justificación
4. Mezclar refactor con rediseño o migración
5. Reescribir en lugar de refactor mínimo
6. Ignorar resultados de tests
7. Asumir comportamiento (siempre validar)

✅ **OBLIGATORIO:**
1. Análisis antes de cualquier cambio
2. Plan aprobado antes de ejecución
3. Separación estricta: análisis ≠ ejecución
4. Validación exhaustiva después
5. Documentar decisiones y bloqueadores
6. Si hay duda → preguntar, no asumir

## Roles y Responsabilidades

### Manager (Tú)
- Aprobación de Fase 1 (análisis comprensible?)
- Aprobación de Fase 2 (plan aceptable?)
- Validación final (código respetuoso con invariantes?)
- Decisión final: aprobado/rechazado/ajustes

### Agente IA (Claude Code)
- Fase 1: Análisis (no escribir código)
- Fase 2: Propuesta de plan (no escribir código)
- Fase 3: Refactor controlado
- Fase 4: Validación automatizada
- Fase 5: Fix mínimo iterativo

### Sistema (Tests + Ruff)
- Validación sintáctica
- Linting
- Regresión automatizada
- Behavioural tests

## Ejemplo: Refactorizar run_pytest_safe.py

```bash
# Manager inicia invocando la skill por su trigger en Claude Code:
#   /refactor  (query: "Refactoriza scripts/run_pytest_safe.py")
#
# Target: scripts/run_pytest_safe.py
# Scope: Mejorar error handling (no cambiar comportamiento)
# Constraint: Debe seguir 5 fases del protocolo
# Manager rol: revisa cada fase
#
# [DEPRECATED - WT-2026-254a] La invocacion legacy via
#   python scripts/orquestador.py --skill /refactor --query "..."
# pertenecia al motor Goose/Claw, deprecado. No usar en proyectos nuevos.

# El agente ejecuta:
# FASE 1: Analiza run_pytest_safe.py
#   → Identifica: exception handling inconsistente, nombres confusos, etc
#   → Documenta invariantes: exit codes (0=ok, 1=fail, 2=error)
#   → Propone cambios: mejorar try/except, clarificar nombres
#
# FASE 2: Manager aprueba plan
#   → El agente propone: agregar type hints, mejorar docstrings
#   → Manager: "Aprobado, pero SOLO error handling, no type hints aún"
#   → Plan ajustado: mínimo cambio
#
# FASE 3: Refactor
#   → El agente aplica cambios aprobados
#
# FASE 4: Validación
#   → Tests pasan? ✓
#   → Ruff clean? ✓
#   → Comportamiento igual? ✓
#
# FASE 5: Iteración
#   → Refactor exitoso, fin
```

## Troubleshooting

**P: ¿Qué si el agente propone un cambio demasiado grande en FASE 2?**
R: Rechazar y pedir subdivisión. El plan debe ser mínimo.

**P: ¿Qué si tests fallan en FASE 4?**
R: Fase 5: analizar causa raíz, fix mínimo. Si 2+ intentos fallan, abandonar.

**P: ¿Puedo hacer dos refactors en uno?**
R: No. Un refactor = una responsabilidad. Si necesitas dos, crear dos tickets.

**P: ¿Debo seguir TODAS las 5 fases?**
R: Sí. Cada fase previene errores diferentes. Saltarse una es riesgoso.

## Prompts asociados

Esta skill define el **protocolo** (5 fases). Los prompts operativos viven en archivos hermanos:

- `PROMPT_TEMPLATE.md` — Meta-prompt largo: rol, invariantes, clasificacion A/B/C/D, preflight, criterios de aceptacion, plan de rollback. Pasalo como contexto base al agente ejecutor.
- `EXECUTION_PROMPT.md` — Prompts cortos del dia a dia: analisis + plan, aplicar sub-fase, foco en zona concreta, auditoria "no hace falta refactor", tests de caracterizacion.
- `../../prompts/orchestrator_refactor_bootstrap.md` — Paste-ready para arrancar una sesion nueva de refactor con cualquier backend.

## Referencias

- `.agent/rules/manager/refactoring-protocol.md` — Protocolo completo
- `CLAUDE.md` sección 3l — Integración TICKET #010
- `WP-2026-010` — Plan de implementación (legacy-compat: ticket historico de origen; ver glosario WOT-2026-010a)
