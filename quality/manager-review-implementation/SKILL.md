---
name: manager-review-implementation
version: 2.0.0
description: Revisar cambios de codigo contra arquitectura del proyecto. Usar cuando el Builder entrega una implementacion (fase MANAGER_REVIEW de un ticket). No usar para cerrar tickets de Contract Formation en status frozen (ver validate_contract_formation.py) ni para auditar el contrato antes del Builder (ver audit_ticket_contract.md).
triggers: [/review, code-review, /approve]
author: agent
role: manager
stage: review
writes_memory: false
quality_gate: false
tags: [core, system]
source_prompt: prompts/manager_review.md
contract_id: cid-man-review-v2
---

# manager-review-implementation

Skill para revisar trabajo del Builder segun el plan aprobado y criterios de calidad.

## Overview

Cuando el Builder marca una tarea como `READY_FOR_REVIEW`, el Manager usa esta skill para:

1. Entender que se implemento (execution_log.md)
2. Verificar Quality Gates (ruff + runner seguro de pytest)
3. Revisar codigo contra criterios de aceptacion
4. Verificar seguridad (no secrets, arquitectura respetada)
5. Generar veredicto: APROBADO / CHANGES

## Workflow

### Paso 0: Verificar Turno

```bash
python .agent/agent_controller.py
```

Debe indicar `ROL ACTIVO: MANAGER`. Si dice BUILDER, informar al usuario.

### Paso 1: Cargar Contexto

Leer en orden:

1. `.agent/rules/manager/` - restricciones del rol
2. `work_plan.md` - plan aprobado con criterios de aceptacion
3. `execution_log.md` - que implemento el Builder
4. `references/review-checklist.md` - checklist de verificacion

### Paso 2: Leer el codigo directamente

**Regla de oro: no confies en el log; lee el codigo.**

Para cada archivo listado en `execution_log.md`, leelo directamente. No aceptes el resumen del Builder como unica evidencia.

Re-ejecuta tu mismo las validaciones tipo-especificas:

```bash
python -c "import yaml; yaml.safe_load(open('data/archivo.yaml', encoding='utf-8')); print('OK')"
```

**Senales de alerta que requieren verificacion adicional:**

- Builder reporta **"ya existia"** o **"ya estaba hecho"** -> lee el archivo y verifica que el contenido cumple el criterio del plan exacto, no solo que algo con ese nombre existe.
- Builder dice **"sin cambios necesarios"** -> verifica que el plan no requeria algo diferente.
- El plan modificaba **N archivos del mismo tipo** y el log solo menciona uno -> verifica los N archivos individualmente.
- El numero de tests **cambia >5%** -> investiga por que.

Para cada archivo, verifica:

| Verificacion | Que buscar? |
|---|---|
| **Cumple plan** | El codigo hace exactamente lo que pide el plan, sin funciones extra no solicitadas? |
| **Consistencia de estado** | Lo que reporta `execution_log.md` coincide con lo que hay realmente en disco? |
| **Type hints** | Todas las funciones tienen hints en argumentos y retorno? |
| **Docstrings** | Funciones y clases publicas tienen docstrings descriptivos? |
| **Pathlib** | Se usa `pathlib` de forma consistente para toda manipulacion de rutas? |
| **Manejo errores** | Hay `try/except` con logs especificos? Prohibido `except: pass`. |
| **Secrets** | No hay API keys, passwords ni rutas absolutas locales hardcodeadas? |
| **Codigo muerto** | Se eliminaron variables, imports y archivos `debug_*.py` temporales? |
| **Hub nodes** | Si existe `graphify-out/GRAPH_REPORT.md`, los archivos de alto grado tocados estan mencionados en el log? |

### Paso 3: Ejecutar Quality Gates

```bash
# 1. Linting (src/ + tests/)
ruff check . --exclude .agent

# 2. Tests
python scripts/run_pytest_safe.py

# Fallback
python scripts/run_pytest_safe.py -- tests/ -v

# 3. Verificar imports circulares
python -c "import src"
```

**Si falla algun gate:**

- Documentar blockers con veredicto `CHANGES`
- Notificar al Builder via la superficie de review vigente
- **NO aprobar hasta que pase todos los gates**

### Paso 4: Verificar Seguridad

**Checklist de Seguridad:**

- [ ] No hay strings de conexion/credenciales en codigo
- [ ] Variables de entorno usadas via `settings.py`
- [ ] Patron cascada respetado (`privada/` -> `publica/`)
- [ ] `.gitignore` protege `privada/`, `.env`, `data/`
- [ ] No hay `print()` con datos sensibles

### Paso 5: Generar Veredicto

Antes de emitir el veredicto en texto, escribe el decision artifact
estructurado (canal primario del bridge; el transcript es fallback):

- Ruta: `.agent/runtime/reviews/decision_<ticket_id>.json` (en `repo_destino`).
- Contenido: `{"ticket_id": "<ticket_id>", "decision": "APROBADO|CHANGES", "blockers": []}`
- En `CHANGES`, lista cada blocker como string breve en `blockers`.
- Si no puedes escribir el archivo, emite igualmente el veredicto en texto.

#### Barrera de regresion (SOLO bugfix/regresion/barrera-nueva)

Aplica el Paso 3 de `prompts/manager_review.md` (fuente normativa, contract_id cid-man-review-v2): revierte el fix, el test debe FALLAR (exit != 0); restaura, debe PASAR (exit 0). El Paso 3 gobierna ademas QUE mutacion ejecutar y COMO leer el `exit_code`: no elijas la mutacion por tu cuenta ni des por buena la barrera sin abrirlo. Registra el par con el formato literal:

```
mutation-verify:
  sin_fix:  command: <cmd>   exit_code: <!=0>   # DEBE ser rojo
  con_fix:  command: <cmd>   exit_code: 0       # DEBE ser verde
```

Sin ese par de exit-codes reales no se emite `APROBADO` para code/mixed que corrigen bug. NO redeclares aqui los criterios normativos: viven en `prompts/manager_review.md` y esta skill solo remite (regla skill-apunta-prompt-gobierna).

#### Opcion A: APROBADO

Si pasa todos los gates y verificaciones:

1. En `work_plan.md`: cambiar estado a `COMPLETED`
2. Registrar decision `APROBADO` en la superficie de review vigente
3. Notificar handoff al usuario
4. Limpiar `execution_log.md` para proxima sesion

#### Opcion B: CHANGES

Si hay problemas menores:

```markdown
### REV-[ID]: Cambios Solicitados

- **Plan ID:** WOT-XXX
- **Tipo:** CHANGES
- **Prioridad:** [Alta/Media/Baja]
- **Estado:** PENDING

**Problemas encontrados:**
1. [Descripcion del problema]
2. [Descripcion del problema]

**Cambios solicitados:**
1. [Cambio especifico]
2. [Cambio especifico]

**Referencia:** Ver execution_log.md seccion [X]
```

## Output Format

### Veredicto en la superficie de review vigente

```markdown
### REV-[ID]: Revision de [Plan ID]

- **Fecha:** [YYYY-MM-DD HH:MM]
- **Revisor:** Manager
- **Veredicto:** [APPROVED | CHANGES]
- **Estado:** RESOLVED / PENDING

**Resumen:**
[2-3 lineas de resumen]

**Quality Gates:**
- [x] Ruff: PASSED
- [x] Pytest: PASSED (X/Y tests)
- [x] Seguridad: VERIFIED

**Archivos revisados:**
- `src/[archivo].py` - [OK | Cambios solicitados]

**Notas:**
[Observaciones adicionales]
```

### Notificacion al Builder (notifications.md)

```markdown
## [FECHA] Revision Completa: Manager -> Builder

**Plan:** WOT-XXX
**Veredicto:** [APPROVED | CHANGES]
**Accion requerida:** [Ver feedback de review | Continuar con siguiente tarea]
**Estado:** PENDING
```

## References

- `references/review-checklist.md` - Checklist detallado de revision
- `references/verdict-format.md` - Templates de veredictos
- `.agent/rules/manager/` - Restricciones del rol Manager
- `.agent/workflows/manager_workflow.md` - Flujo completo

## Constraints

- **NO** modificar codigo en `src/` o `tests/`
- **NO** escribir en `execution_log.md` (solo lectura)
- **NO** aprobar sin verificar Quality Gates
- **SIEMPRE** documentar la decision en la superficie de review vigente
