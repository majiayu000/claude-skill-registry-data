---
name: manager-session-closeout
version: 1.1.0
description: Cierre de sesion del Manager que propone learnings, los clasifica como local, generalizable o dudoso y prepara el puente de mejora continua hacia el motor. Usar cuando termina un WP o una sesion relevante y hay que capturar lo aprendido con validacion humana. No usar para cerrar un proyecto entero (ver project-finalize) ni para volcar observaciones a memoria (ver session-close-observations).
triggers: [/closeout, /session-closeout, /close-session]
author: agent
role: manager
stage: close
cycle_phase: [F7-cierre-sesion]
writes_memory: true
quality_gate: false
tags: [core, system, improvement-loop, close]
---

# manager-session-closeout

Skill del Manager para cerrar sesiones con mejora continua de doble bucle: captura local de learnings, clasificacion humana y puente controlado hacia el motor.

## Overview

Activa esta skill al final de un WP completado o de una sesion relevante para:
- proponer learnings de cierre
- clasificarlos como `local`, `generalizable` o `dudoso`
- pedir validacion humana antes de publicar
- preparar el siguiente ciclo de planificacion con contexto util

### Cuando activar

- Un WP termino en `COMPLETED`
- Hay learnings de proceso, planificacion o alcance que merecen sobrevivir a la sesion
- Quieres separar señal local del proyecto de señal reutilizable por el motor

### Cuando NO activar

- Durante la implementacion activa de un WP
- Si no hay decisiones ni aprendizajes relevantes
- Si solo hubo cambios superficiales sin leccion reutilizable

## Workflow

### Paso 0: Barrer learnings upstream pendientes

Antes de generar nuevas salidas:
1. Leer `.agent/runtime/memory/UPSTREAM_LEARNINGS.md` si existe.
2. Revisar entradas en `## Pendientes de revision`.
3. Decrementar `ttl_wps` solo en las entradas que sigan pendientes.
4. Si `ttl_wps` llega a `0`, mover la entrada a `## Archivados`.
5. Si una entrada fue reclasificada como valida en esta sesion, moverla a `## Confirmados`.
6. Presentar al usuario las entradas que expiran o cambian de estado.

### Paso 1: Proponer learnings de la sesion

Generar un bloque con exactamente este formato por item:

```markdown
## Learnings propuestos

### 1
- learning: "..."
- categoria_propuesta: local|generalizable|dudoso
- origen: bug-fix|contrato|proceso|documental
- evidencia: "<commit sha | test | archivo:linea | comando + resultado>"
- razon: "..."

### 2
- learning: "..."
- categoria_propuesta: local|generalizable|dudoso
- origen: bug-fix|contrato|proceso|documental
- evidencia: "..."
- razon: "..."
```

Categorias permitidas:
- `local`
- `generalizable`
- `dudoso`

Taxonomia de `origen` (mejora el enrutado posterior):
- `bug-fix` — nacio de un defecto corregido; candidato a barrera de regresion
- `contrato` — define o cambia un contrato entre componentes; candidato a wing `engine`
- `proceso` — regla de flujo de trabajo o review; candidato a wing `meta`
- `documental` — drift docs/realidad; candidato a fix documental, no a memoria estable

Regla de evidencia: un learning sin campo `evidencia` verificable no puede
proponerse como `generalizable`; rebajalo a `dudoso` o descartalo. La
validacion humana debe poder comprobar el anchor sin reconstruir la sesion.

### Paso 2: Pedir validacion humana

El usuario debe poder responder por item con una de estas acciones:
- `accept`
- `recategorize: local|generalizable|dudoso`
- `discard`
- `defer: motivo`

### Bloque de validacion del usuario

```markdown
## Validacion del usuario

- 1: accept
- 2: recategorize: local
- 3: defer: falta evidencia suficiente
```

### Paso 3: Clasificar y enrutar

- `local` -> `observations.jsonl` del proyecto destino
- `generalizable` -> `UPSTREAM_LEARNINGS.md`
- `dudoso` -> `UPSTREAM_LEARNINGS.md` con `ttl_wps: 3`

### Paso 4: Preparar contexto para el siguiente ciclo

Escribir `closeout_lessons.md` como resumen puente para el siguiente `manager-create-work-plan`.

### Paso 5: Cerrar y reportar

Generar un resumen final con:
- learnings propuestos
- learnings aceptados
- learnings enviados al canal upstream
- learnings archivados por TTL

## Output Format

La skill no escribe por stdout como producto final. Su efecto esperado es:
- actualizar `observations.jsonl` cuando aplique
- actualizar `UPSTREAM_LEARNINGS.md` cuando aplique
- escribir `closeout_lessons.md`

## References

- [references/upstream-learnings-format.md](references/upstream-learnings-format.md)
- [references/scope-taxonomy.md](references/scope-taxonomy.md)
- [references/closeout-lessons-format.md](references/closeout-lessons-format.md)
- `../session-close-observations/SKILL.md`
- `../manager-create-work-plan/SKILL.md`
- `../project-finalize/SKILL.md`

## Constraints

- **NO** publicar learnings sin validacion humana
- **NO** tratar `dudoso` como permanente: TTL maximo 3 WPs
- **NO** mezclar learnings locales con generales
- **SIEMPRE** dejar explicito el estado final de cada learning
- **SIEMPRE** mantener el flujo listo para el siguiente plan

## Related Skills

- `session-close-observations`
- `manager-create-work-plan`
- `project-finalize`
