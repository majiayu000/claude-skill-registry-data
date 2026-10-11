---
name: manager-create-work-plan
version: 2.0.0
description: Crea el work_plan estructurado que ejecutara el Builder, con fases, tareas, riesgos y criterios de aceptacion medibles. Usar cuando el usuario pide una funcionalidad o un cambio y el Manager debe formar el contrato. No usar para revisar una entrega (ver manager-review-implementation) ni si el requisito es ambiguo (primero grill-work-plan).
triggers: [/plan, create-plan, /schedule]
author: agent
role: manager
stage: plan
cycle_phase: [F2-contrato]
writes_memory: false
quality_gate: false
tags: [core, system]
---

# manager-create-work-plan

Skill para crear planes de trabajo detallados que el Builder pueda ejecutar.

## Overview

Cuando el usuario solicita una nueva funcionalidad, el Manager usa esta skill para:
1. Analizar el requerimiento y contexto actual
2. Identificar archivos privados necesarios (Fase 0)
3. Descomponer en fases con tareas 🤖/👤
4. Asignar niveles de riesgo (🟢/🟡/🔴)
5. Definir criterios de aceptación medibles
6. Documentar trade-offs considerados

## Workflow

### Paso 0: Verificar Turno

> **Carga de memoria:** antes de planificar, ejecuta el mecanismo descrito en
> `prompts/_shared/memory_bootstrap.md`. Motivo: el Manager que planifica sin
> corpus decide sin lecciones; las decisiones ya aprendidas se repiten.
```bash
python .agent/agent_controller.py
```
Debe indicar `ROL ACTIVO: MANAGER` y acción `CREATE_PLAN`.

### Paso 0b: Cargar lecciones de cierre

Antes de analizar el requerimiento, leer si existe:
- `.agent/runtime/memory/closeout_lessons.md`

Usar ese contexto para:
- evitar repetir errores de tickets previos
- reutilizar learnings aprobados como generalizables
- respetar learnings que siguen siendo locales al proyecto

Si el archivo no existe, continuar sin bloquear.

### Paso 1: Analizar Requerimiento

Entender del usuario:
- ¿Qué problema resuelve?
- ¿Qué resultado espera?
- ¿Hay restricciones de tiempo/tecnología?

Explorar código existente:
```bash
tree src/ -L 2
find src/ -name "*.py" | head -20
```

### Paso 2: Identificar Fase 0 (Usuario)

Determinar si se necesitan archivos en `privada/`:
- ¿Necesita credenciales/API keys?
- ¿Configuración personal del usuario?
- ¿Datos sensibles de empresa?

Si sí → Fase 0 con tareas 👤 para el usuario

### Paso 3: Crear work_plan.md

Usar `references/plan-template.md` como base.

Estructura obligatoria:
```markdown
# Plan de Trabajo: [Título]

## Metadata
- **ID:** WOT-[YYYY]-[NNN][x]
- **Estado:** 🟡 IN_PLANNING
- **deliverable_type:** code | documentation | research | analysis | mixed
- **Creado:** [FECHA]
- **Prioridad:** HIGH/MEDIUM/LOW
- **Asignado a:** Builder

## 🎯 Objetivo
[Descripción clara en 2-3 líneas]

## 📋 Contexto
[Situación actual, problema a resolver]

## Configuración Privada Requerida
[Lista de archivos necesarios en privada/]

## Plan de Implementación

### Tipos de Tareas
| Icono | Tipo | Ejecutor |
|-------|------|----------|
| 🤖 | TAREA AGENTE | Builder |
| 👤 | TAREA USUARIO | Usuario |

### Fase 0: [Nombre] (👤/🤖)
#### 0.1: 🤖/👤 [Nombre tarea]
- **Tipo:** 🤖/👤 TAREA [AGENTE/USUARIO]
- **Archivo:** `ruta/archivo.py`
- **Acción:** Crear/Modificar
- **Descripción:** [Qué hacer]
- **Riesgo:** 🟢/🟡/🔴 [Bajo/Medio/Alto]
- **Criterio de Aceptación:** [Medible y verificable]
- **Si falla:** [Acción a tomar]

### Fase 1: [Nombre]
...

## Trade-offs Considerados
| Opción | Pros | Contras | Decisión |
|--------|------|---------|----------|
| A | [+] | [-] | [Aceptada/Descartada] |

## 🚨 Guía de Riesgos
| Nivel | Significado | Acción del Builder |
|-------|-------------|-------------------|
| 🟢 Bajo | Rutinaria | Intentar 3 veces antes de escalar |
| 🟡 Medio | Requiere atención | Intentar 2 veces, escalar si dudas |
| 🔴 Alto | Crítica | Escalar al primer fallo |

## 🧪 Criterios de Aceptación Global
- [ ] [Criterio medible 1]
- [ ] [Criterio medible 2]
```

### Paso 4: Asignar Riesgos

Para cada tarea, usar guía en `references/risk-guide.md`:

**🟢 Bajo:**
- Crear archivos nuevos
- Modificar templates
- Tests simples

**🟡 Medio:**
- Modificar lógica existente
- Cambios en configuración
- Integraciones

**🔴 Alto:**
- Cambios arquitectónicos
- Migraciones de datos
- Cambios en seguridad

### Paso 5: Definir Criterios de Aceptación

Cada tarea necesita criterios **SMART**:
- **S**pecific: Qué exactamente
- **M**easurable: Cómo se verifica
- **A**chievable: Realista
- **R**elevant: Al plan
- **T**ime-bound: Cuándo listo

Ejemplo bueno:
> "Crear `validate_all.py` que detecte 9 directorios de skills y valide frontmatter YAML con campos: name, version, description, author, tags"

Ejemplo malo:
> "Crear script de validación"

### Paso 6: Documentar Trade-offs

Si hay decisiones arquitectónicas:

```markdown
## Trade-offs Considerados

| Opción | Pros | Contras | Decisión |
|--------|------|---------|----------|
| SQLite local | Simple, sin servidor | No escalable | ✅ Elegida |
| PostgreSQL | Escalable | Requiere setup | Descartada |

**Razón:** Para MVP, SQLite es suficiente.
```

Crear ADR en `.agent/decisions/` si es decisión importante.

### Paso 7: Aprobar Plan

Checklist antes de aprobar:
- [ ] ID único y descriptivo
- [ ] Fase 0 incluida si hay archivos privados
- [ ] Todas las tareas tienen riesgo asignado
- [ ] Criterios de aceptación son medibles
- [ ] Trade-offs documentados (si aplica)
- [ ] Ninguna fase tiene campos duplicados (p.ej. dos lineas `Descripcion:` en la misma fase); si se actualizo un campo, borrar la version anterior antes de aprobar
- [ ] No hay contradiccion entre `Descripcion` y `Criterios de Aceptacion` de la misma fase; si difieren, reconciliarlos explicitamente antes de aprobar — nunca asumir que uno manda sobre el otro sin corregir el texto
- [ ] Todo criterio verificable de una fase tiene su comando o accion correspondiente en la seccion `Calidad`; si un criterio de aceptacion no aparece ahi, el Manager puede aprobarlo sin haberlo verificado
- [ ] Si un comando se usa en dos modos distintos (p.ej. `--dry-run` vs ejecucion real, `--force` vs sin flag), la Descripcion especifica explicitamente cual es la accion de la fase y cual es la comprobacion previa, en ese orden; si el plan usa `--dry-run`, la fase real debe existir como paso separado — dry-run nunca sustituye la ejecucion real ni cuenta como validacion de cierre
- [ ] Si `work_plan.md` y `STRATEGY_WOT-*.md` coexisten, el resumen corto no puede contradecir al largo en ningun punto operativo (comandos, flags, orden de pasos); si difieren, el largo (work_plan.md) manda y el corto debe regenerarse antes de aprobar
- [ ] Si una fase depende de actualizar `PROJECT.md` o `CHANGELOG.md` manualmente, la Descripcion especifica quien lo actualiza (Builder/Manager) y con que criterio o contenido minimo; la ambiguedad aqui produce fases declaradas completas sin que los archivos se hayan tocado
- [ ] El estado de `STATE.md` y `execution_log.md` debe usar el enum valido del controller para cierre o avance (`APPROVED`, `IN_PROGRESS`, `READY_FOR_REVIEW`, `COMPLETED`, etc.); `IDLE` solo sirve como sentinel de workspace sin ticket activo y no debe usarse para cerrar un ticket del motor

Cambiar estado: `🟡 IN_PLANNING` → `🟢 APPROVED`

Añadir notificación:
```markdown
## 📨 [FECHA] Handoff: Manager → Builder
**Plan:** WOT-XXX
**Acción requerida:** Implementar según work_plan.md
**Estado:** PENDING
```

## Handoff canonico al Builder (OBLIGATORIO)

Preparar la documentacion para el Builder NO es solo aprobar el work_plan.
Son SIETE artefactos. Omitir uno deja el ciclo incompleto. Error recurrente:
olvidar `STRATEGY_WOT-*.md` y `AUDIT_WOT-*.md`.

Checklist obligatorio, en orden:

0. `TP Check` en `AUDIT_WOT` — verificar contra `../../_shared/ticket-anti-patterns.md` antes de aprobar el `work_plan`.
1. `work_plan.md` — contenido completo + `Estado: APPROVED`.
2. `STRATEGY_WOT-XXXX.md` — estrategia tecnica del ticket (en `.agent/collaboration/`).
3. `AUDIT_WOT-XXXX.md` — criterios que el Manager verificara en el review.
4. `execution_log.md` — `Estado: IN_PROGRESS`, bitacora inicializada.
5. `TURN.md` — regenerar a `ROL=BUILDER`:
   `python .agent/agent_controller.py --reset-turn --force`
   Sin `--reset-turn` el controller NO sobrescribe un TURN.md existente.
6. `STATE.md` — lo regenera el mismo comando del paso 5.
7. Bus — emitir `STATE_CHANGED -> IN_PROGRESS`:
   `python .agent/agent_controller.py --bootstrap-ticket --json`
   Idempotente (`already_bootstrapped` si ya existe).

Verificacion final OBLIGATORIA:
`python .agent/agent_controller.py --validate --json --force` -> 0 errores.

Solo con los 7 artefactos + validate en verde el turno es del Builder y el
launcher abrira su ventana del Builder.

## Output Format

El handoff al Builder genera/actualiza, sin omitir ninguno:
1. `work_plan.md` (APPROVED)
2. `STRATEGY_WOT-XXXX.md` (estrategia tecnica)
3. `AUDIT_WOT-XXXX.md` (criterios de auditoria)
4. `execution_log.md` (IN_PROGRESS)
5. `TURN.md` + `STATE.md` (regenerados con `--reset-turn`)
6. Bus: evento `STATE_CHANGED -> IN_PROGRESS`
7. `--validate` en verde
8. `notifications.md` con handoff al Builder (opcional)
9. ADR en `.agent/decisions/` (opcional, si trade-off significativo)

## References

- `references/plan-template.md` - Template base del plan
- `references/risk-guide.md` - Guía de asignación de riesgos
- `.agent/templates/work_plan_template.md` - Template completo del sistema
- `.agent/rules/manager/` - Restricciones del rol

- `references/plan-quality-checklist.md` - Checklist de calidad para planes y audits
- `../../_shared/ticket-anti-patterns.md` - Catalogo TP compartido para prompts de Manager y Builder
- `../manager-session-closeout/SKILL.md` - Cierre de sesion y puente de learnings

## TP Check obligatorio

Antes de aprobar cualquier `work_plan.md`, el Manager debe rellenar en `AUDIT_WOT-XXXX.md` una seccion `## TP Check` usando:

1. `../../_shared/ticket-anti-patterns.md` como catalogo de referencia.
2. `references/plan-quality-checklist.md` como checklist de aprobacion.
3. Evidencia literal para cada check: seccion, linea, test, comando o diff.

Regla de aprobacion:
- Si un TP aplica y no puede cerrarse con una linea concreta, el plan sigue en borrador.
- Si el plan y el audit no coinciden en secuencia, archivos o criterios, el ticket no pasa a `APPROVED`.
- Si el texto usa semantica blanda sin definir el mecanismo, se corrige antes del handoff.
- Si el ticket introduce una nueva gate de calidad, aplica ese gate manualmente sobre el propio `AUDIT_WP` antes de confiar en automatizacion futura.
- Si existe `.agent/runtime/memory/closeout_lessons.md`, usalo como contexto antes de redactar un nuevo plan.

## Constraints

- **NO** asignar tareas del usuario (👤) al Builder
- **NO** omitir Fase 0 si hay archivos privados
- **SIEMPRE** incluir criterios de aceptación medibles
- **SIEMPRE** asignar nivel de riesgo a cada tarea
