---
name: builder-implement-from-plan
version: 2.0.0
description: Implementa en orden las tareas de un work_plan aprobado como rol builder, bajo el contrato de ejecucion de orchestrator_launch_builder (identidad y paridad del contrato, preflight, tests, gates focales, commit segun delivery_authority y handoff canonico al Manager). Usar cuando el controlador indica ROL ACTIVO BUILDER con accion IMPLEMENT sobre un plan aprobado. No usar para redactar o lanzar el arranque del Builder (ver orchestrator_prepare_and_launch_ticket), para revisar la entrega (ver manager-review-implementation) ni para un deliverable solo documental (ver builder-write-deliverable).
triggers: [/implement, implement, /code]
author: agent
role: builder
stage: implement
cycle_phase: [F5-implementacion]
writes_memory: false
quality_gate: false
tags: [core, system]
source_prompt: prompts/orchestrator_launch_builder.md
contract_id: cid-bui-implement-v1
---

# builder-implement-from-plan

Skill para implementar codigo segun un plan de trabajo aprobado.

## Overview

Cuando el Manager marca un plan como `APPROVED`, el Builder usa esta skill para:

1. Leer y entender el plan completo
2. Implementar tareas en orden (sin saltar fases)
3. Aplicar reglas de codigo (pathlib, type hints, etc.)
4. Registrar progreso y escalarse si es necesario

## Workflow

### Paso 0: Verificar Turno

```bash
python .agent/agent_controller.py
```

Debe indicar `ROL ACTIVO: BUILDER` y accion `IMPLEMENT`.

### Paso 1: Cargar Contexto

Leer en orden:

1. `.agent/rules/builder/` - restricciones del rol
2. `work_plan.md` - plan aprobado completo
3. `execution_log.md` - progreso previo
4. `references/code-rules.md` - reglas de codigo

### Paso 2: Identificar Tarea Actual

En `work_plan.md`, buscar:

- Primera fase con tareas pendientes `[ ]`
- Primera tarea no completada en esa fase

**NO saltar fases** - Implementar en orden.

### Paso 3: Verificar Pre-condiciones

Antes de implementar:

- [ ] Plan esta `APPROVED` (no `DRAFT` o `IN_PLANNING`)
- [ ] No hay tareas `USUARIO` pendientes en esta fase
- [ ] Entiendo que debo hacer (criterio de aceptacion claro)

### Paso 4: Implementar con Reglas de Codigo

Ver `references/code-rules.md` para detalles completos.

**Reglas esenciales:**

| Regla | Ejemplo | Incorrecto | Correcto |
|---|---|---|---|
| **Pathlib** | Rutas | `os.path.join()` | `Path() / "file"` |
| **Type hints** | Funciones | `def load():` | `def load() -> dict:` |
| **Docstrings** | Publicas | Sin docstring | `"""Carga config."""` |
| **Logging** | Errores | `print(e)` | `logger.error(e)` |
| **Try/except** | Excepciones | `except:` | `except ValueError:` |

### Paso 5: Probar el Codigo

```bash
# Ejecutar tests relacionados
python scripts/run_pytest_safe.py -- tests/test_[modulo].py -v

# Fallback
python scripts/run_pytest_safe.py -- tests/test_[modulo].py -v

# Verificar linting
ruff check src/[archivo].py
ruff format --check src/[archivo].py
```

**Si falla:** Corregir antes de continuar.

### Paso 6: Ejecutar builder-self-audit (OBLIGATORIO)

Antes de documentar la tarea como completada, ejecuta el skill `builder-self-audit`.

`builder-self-audit` cubre:

1. Protocolo "ya existia" con cita de linea
2. Completitud multi-archivo
3. Checklist anti-regresion para ISS/code smell
4. Gate completo ruff check + ruff format --check + pytest

**Solo si `builder-self-audit` pasa completamente, continua al Paso 7.**

### Paso 7: Documentar en execution_log.md

```markdown
### [OK] [FECHA] - [Nombre Tarea]

- **Archivo:** `src/[archivo].py`
- **Cambios:** [Descripcion breve]

**Codigo anadido:**

```python
# Ejemplo de funcion creada
def nueva_funcion() -> None:
    pass
```

**Tests:**
```bash
$ python scripts/run_pytest_safe.py
[archivo].py::test_nueva PASSED
```

**Hallazgos:** [Si aplica, referencia a findings.md]
```

### Paso 8: Marcar Tarea Completada

En `work_plan.md`:

- Cambiar `- [ ]` a `- [x]` para la tarea completada

### Paso 9: Verificar si Fase Completa

Si todas las tareas de la fase estan `[x]`:

1. Ejecutar los **gates focales** de la fase (loop rapido: no autorizan handoff)
2. Incluir `ruff format --check` sobre los archivos Python tocados
3. Si pasan -> Continuar con siguiente fase
4. Si fallan -> Corregir antes de continuar

### Paso 10: Cierre Canonico (solo al completar el plan entero)

El contrato de cierre canonico (comandos, orden, evidencia de bus, distincion
loop rapido vs cierre, y que hacer si `checkpoint/review-<ticket>` esta `stale`)
lo define el prompt canonico, no esta skill:

- `prompts/orchestrator_launch_builder.md`, secciones "Loop rapido vs cierre
  canonico (politica WOT-2026-011g)" y "Registro y cierre" (`cid-bui-implement-v1`).

Sigue esa fuente. Si esta skill y el prompt divergen, prevalece el prompt.

## Escalacion

**Escalar al Manager si:**

| Riesgo | Condicion | Accion |
|---|---|---|
| Bajo | 3+ intentos fallidos | Escalar |
| Medio | 2+ intentos fallidos | Escalar |
| Alto | 1 intento fallido | Escalar inmediatamente |
| Cualquiera | 30+ min bloqueado | Escalar |

**Como escalar:**

1. Documentar en `execution_log.md` intentos realizados
2. Anadir la escalacion a la superficie de review vigente
3. Cambiar estado a `BLOCKED`
4. Informar al usuario

## Output Format

### Al Completar Tarea

- Tarea marcada `[x]` en `work_plan.md`
- Entrada en `execution_log.md` con cambios y tests
- `findings.md` actualizado (si aplico hallazgos)

### Al Completar Fase

- Todas las tareas de la fase en `[x]`
- Gates focales de la fase pasados
- Resumen de la fase en `execution_log.md`

### Al Completar Plan

- Todas las fases completadas
- Resumen final en `execution_log.md`
- Cierre canonico ejecutado segun el Paso 10 (contrato en el prompt canonico)
- Estado cambiado a `READY_FOR_REVIEW` por el controller (no manualmente)

## References

- `references/code-rules.md` - Reglas completas de codigo Python
- `references/log-format.md` - Formato de execution_log.md
- `.agent/rules/builder/` - Restricciones del rol
- `.agent/workflows/builder_workflow.md` - Flujo completo

## Constraints

- **NO** modificar `work_plan.md` (excepto marcar tareas `[x]`)
- **NO** saltar fases del plan
- **NO** omitir type hints o docstrings
- **NO** usar `os.path` (usar `pathlib`)
- **SIEMPRE** escalar si se superan intentos segun riesgo
