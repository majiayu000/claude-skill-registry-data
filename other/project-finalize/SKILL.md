---
name: project-finalize
version: 2.0.0
description: Cierre profesional de un proyecto o fase importante con auditoria, limpieza, documentacion, versionado y verificacion final. Usar cuando el usuario pide dejar el repo listo para entrega, handoff o mantenimiento. No usar para cerrar una sesion de trabajo (ver manager-session-closeout) ni para publicar en Git (ver audit-git-publication).
triggers: [/finalize, close, /finish]
author: agent
role: shared
stage: close
cycle_phase: [F7-cierre-sesion]
writes_memory: false
quality_gate: false
tags: [core, system]
---

# project-finalize

Orquesta el cierre profesional de un proyecto o fase importante. Sirve para
dejar el repo limpio, documentado, versionado y listo para entrega, handoff o
mantenimiento.

## Overview

Activa esta skill cuando:
- El usuario dice "cierra el proyecto", "dejalo listo para entrega" o pide una limpieza final
- El Builder ya termino una implementacion importante y toca consolidar
- Hace falta alinear codigo, documentacion, version y artefactos antes de marcar DONE

### Regla de compatibilidad

- Usa `work_plan.md` como plan activo.
- No introduzcas `work_plan_cierre.md` como plan operativo salvo que tambien
  actualices controller, hooks, prompts y validadores que hoy dependen de
  `work_plan.md`.
- Si quieres trazabilidad adicional, crea `closeout_report.md` o archiva una
  copia final del plan, pero el carril operativo sigue siendo `work_plan.md`.

## Workflow

### Paso 1: Elegir modo de cierre

Usa `references/closeout-modes.md` para escoger entre:
- `DELIVERY` - Entrega profesional de algo que seguira vivo
- `RELEASE` - Publicacion de una version
- `HANDOFF` - Traspaso a otra persona o equipo
- `ARCHIVE` - Cierre o fin de vida

Identifica desde el inicio que aprobaciones humanas haran falta:
- borrados relevantes
- cambios estructurales
- bump de version
- tags o release
- archivado

### Paso 2: Manager crea el plan de cierre

Usa `references/closeout-plan-template.md`.

El plan debe incluir, como minimo:
1. Auditoria
2. Limpieza
3. Documentacion
4. Versionado / release readiness
5. Verificacion final

Todo lo que quede fuera de alcance va a `backlog.md`, no a TODOs ocultos.

### Paso 3: Builder ejecuta la auditoria

Auditar:
- archivos temporales, logs, debug y scripts locales
- codigo o docs muertos
- `TODO`, `FIXME`, ejemplos viejos y configuracion obsoleta
- riesgo de secrets y estado de `.env.example`
- deriva documental entre README, PROJECT, CLAUDE, docs de agentes y comandos
- estado de version, changelog y notas de release
- consistencia entre manifests y lockfiles
- huecos de mantenimiento: LICENSE, SECURITY, CONTRIBUTING, CODEOWNERS, soporte

Clasificar hallazgos en:
- `must-fix`
- `recommended`
- `defer-to-backlog`

### Paso 4: Manager revisa la auditoria

El Manager decide que entra en alcance y que se difiere.

Cualquier borrado de archivos, cambio estructural o riesgo de perdida de
contexto necesita aprobacion explicita antes de ejecutarse.

### Paso 5: Builder ejecuta la limpieza

- Eliminar artefactos temporales o locales si es seguro
- Podar scripts, ejemplos o docs obsoletos
- Normalizar estructura y nombres
- Ajustar `.gitignore` u otros ignores
- Verificar que no queden secrets, credenciales o rutas personales
- Preservar scaffolding deliberado; no borrar por intuicion

### Paso 6: Builder sincroniza documentacion

Actualizar solo lo que aplique de verdad:
- `README.md`
- `PROJECT.md`
- `CHANGELOG.md`
- `CLAUDE.md`
- reglas o docs de agentes
- resumen de arquitectura / ADR / limitaciones conocidas / migraciones
- instrucciones de run, test, install, deploy, rollback o handoff

Para repos compartidos o publicos, revisar tambien el checklist de
`references/closeout-checklist.md`.

### Paso 7: Builder prepara versionado y release readiness

- Reutilizar `version-changelog` para SemVer y CHANGELOG
- El tipo de bump lo valida el Manager
- El bump, tag o release requieren aprobacion humana en el punto adecuado
- Si hubo cambios incompatibles o deprecaciones, documentarlos de forma visible

### Paso 8: Builder cubre trust y governance

Aplicar solo cuando la madurez del proyecto lo justifique:
- `LICENSE`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `CODEOWNERS`
- `CITATION.cff` si el software debe citarse
- SBOM para software distribuible
- artifact attestation / provenance para builds publicadas
- estado de mantenimiento: `active`, `maintenance-only` o `archived`

### Paso 8d: Builder verifica atribuciones externas (CREDITS.md)

Si el `work_plan.md` del WP que se cierra contiene alguno de estos marcadores, la atribución es obligatoria:
- `Origen externo:` con URL de GitHub
- `Inspired by:` con repo + SHA
- `Origen:` apuntando a un archivo `.agent/runtime/compare/*.md` (output de `repo-compare`)

Builder debe verificar:
1. `CREDITS.md` en raíz del repo tiene una fila en la tabla principal con el WP-ID correspondiente.
2. La fila incluye: `WP`, `Source` (link al repo + SHA si posible), `Pattern`, `License`, `Adapted vs Ported`.
3. La columna `License` no es `[verify]` (humano debe haber confirmado la licencia del repo source).

Si falta la fila → **PARAR y avisar al usuario**. No cerrar el WP hasta que la atribución exista. Plantilla disponible en `skills/repo-compare/references/output-format.md` sección "Credits Block Template".

Si el WP no tiene origen externo (es trabajo propio del proyecto): este paso es no-op, continuar.

### Paso 9: Builder hace la verificacion final

- Ejecutar `builder-run-quality-gates`
- Ejecutar `builder-self-audit`
- Hacer smoke test de instalacion o ejecucion en entorno limpio si es viable
- Verificar documentacion contra comandos, rutas y outputs reales
- Registrar evidencia final en `execution_log.md`

### Paso 9a: Builder ejecuta preflight de entrega

Antes de `--mark-ready` y antes del `git push`, ejecutar el comando canonico unico:

```powershell
python scripts/prepush_check.py
```

Este wrapper ejecuta en secuencia fija:
1. Delivery Hygiene Check (hooks mutadores, artefactos generados, arbol limpio)
2. Ruff Check (linting de Python)
3. Ruff Format Check (formato de codigo)
4. Agent Controller Validate (validacion de tickets)
5. Git Status Check (arbol sin cambios)
6. Validate All (skills, informacional - no bloqueante)

- Si el preflight falla, el Builder debe parar, ejecutar la pasada mutadora manualmente (`uv run pre-commit run --all-files --hook-stage pre-commit`), corregir los errores reportados y volver a ejecutar el preflight hasta que todos los checks bloqueantes pasen.
- Los artefactos generados que se reescriben con frecuencia, como `.agent/context/project-map.json`, deben estar excluidos del formateo y de los hooks que los mutan.
- El objetivo es detectar el fallo antes del mail, no descubrirlo en GitHub Actions.
- **Regla de parada:** si el preflight reporta errores, no se puede ejecutar `--mark-ready` ni `git push` hasta corregir y verificar que el arbol queda limpio.
- **Comando unico:** este wrapper reemplaza la lista manual dispersa de comandos; el operador solo necesita recordar `python scripts/prepush_check.py`.

### Paso 9b: Builder ejecuta cierre de release repetible

- Ejecutar cierre atómico: `python .agent/agent_controller.py --mark-ready --json --force`
- Esto sincroniza `execution_log.md`, `TURN.md` y `STATE.md` automáticamente
- Valida no hay drift entre archivos canónicos
- Prepara el ticket para review sin drift post-review
- Registrar evidencia del comando ejecutado en `execution_log.md`

> **Nota — pipeline de cierre de sesion:** los pasos 9c-9f estan automatizados
> en `scripts/session_closeout.py`, invocable con
> `python .agent/agent_controller.py --session-close [--dry-run] [--force]`.
> Para cierres de SESION usa el pipeline (incluye ademas rotacion de
> review_queue y archivado de manager_feedback que no estan listados aqui).
> Ejecuta estos pasos a mano solo para diagnostico puntual o cierres de
> PROYECTO donde necesites control paso a paso.

### Paso 9c: Builder genera snapshot de auditoría local

- Ejecutar `python scripts/local_audit.py`
- Revisar `.agent/runtime/audit/AUDIT.md` (40 líneas) para detectar drift no capturado por `--validate`:
  - Versión vs ticket en curso
  - Skills nuevas no documentadas en AGENTS.md
  - WPs recientes coherentes con CHANGELOG
  - Active Plan ID consistente con `STATE.md`
  - Si detecta drift → para y reporta antes de marcar `COMPLETED`.
  - Si OK → continuar con el cierre del Manager (Paso 10).
  - El output queda en `.agent/runtime/audit/` (gitignored, sirve como entrada `Paso 0` del `session_bootstrap` en la próxima sesión).

### Paso 9d: Builder genera observaciones de cierre de sesion

- Ejecutar `python scripts/session_close_observations.py --ticket WOT-2026-XXX --verbose`
- Revisar `.agent/runtime/memory/session_close_report.md` para verificar:
  - Observaciones generadas y filtradas
  - Razones de rechazo (si las hay)
  - Topics cubiertos en este ciclo
- Validar que las observaciones validadas se appendearon a `observations.jsonl`
- Este paso es **obligatorio** antes de consolidar memoria en cierres de sesion largos
- **Skill relacionada**: `session-close-observations`

### Paso 9d.5: Manager clasifica learnings de cierre

- Si el cierre genero learnings que deben separarse por alcance, ejecutar `manager-session-closeout`
- Revisar `closeout_lessons.md` y la cola de learnings upstream antes de consolidar memoria
- Clasificar cada learning como `local`, `generalizable` o `dudoso`
- Aplicar TTL de 3 WPs a los items `dudoso`
- Preparar el puente humano hacia el siguiente ciclo de planificacion
- **Skill relacionada**: `manager-session-closeout`

### Paso 9e: Builder ejecuta consolidación de memoria (opcional)

- Ejecutar `python scripts/memory_consolidate.py --verbose` (dry-run primero)
- Revisar `.agent/runtime/memory/CONSOLIDATION_REPORT.md` para verificar cifras
- Si OK, ejecutar `python scripts/memory_consolidate.py --apply --verbose`
- Validar que `MEMORY.md` se regeneró correctamente
- Este paso es opcional; invocar solo en cierres de sesión largos o cuando `observations.jsonl` haya crecido significativamente
- **Origen externo**: Oportunidad #4 de `garrytan/gbrain` (dream cycle pattern) - ver `CREDITS.md`
- **Pre-requisito**: Haber ejecutado Paso 9d (`session_close_observations.py`) para generar observaciones de cierre

### Paso 9f: Builder verifica housekeeping del histórico (sugerencia)

- Si `execution_log.md` supera ~10 entradas WP completadas, considerar ejecutar:
  - `python scripts/archive_execution_log.py --dry-run` para previsualizar
  - `python scripts/archive_execution_log.py --apply` para archivar tickets cerrados
- Este paso es **solo una sugerencia**; el archivado requiere decisión humana
- El guard `check_no_history_truncation` protege contra truncados peligrosos sin archive
- **Origen externo**: integración interna basada en necesidad detectada tras WP-2026-097

### Paso 10: Manager cierra

El Manager relee archivos cambiados, valida que el cierre atómico se ejecutó correctamente, comprueba
coherencia entre docs, version y estado sincronizado, y marca el plan `COMPLETED`.

Si el proyecto termina o cambia de manos, dejar explicito:
- estado de mantenimiento
- backlog pendiente
- decision de handoff o archivado

**Regla de cierre repetible:** El cierre solo se considera completo tras la ejecución del protocolo atómico por Builder y la validación por Manager. Esto asegura releases repetibles y reduce drift post-review.

## Output Format

1. `work_plan.md` actualizado y completado
2. `execution_log.md` con hallazgos, acciones y evidencia
3. `closeout_report.md` opcional como resumen permanente del cierre
4. Documentacion y metadatos sincronizados
5. `notifications.md` con handoffs o aprobaciones si aplica

## References

- `references/closeout-modes.md` - Modos de cierre y cuando usarlos
- `references/closeout-plan-template.md` - Esqueleto del plan de cierre
- `references/closeout-checklist.md` - Checklist minimo, recomendado y avanzado
- `../version-changelog/SKILL.md` - Versionado y changelog
- `../builder-self-audit/SKILL.md` - Auditoria obligatoria del Builder
- `../builder-run-quality-gates/SKILL.md` - Quality gates finales
- `../manager-review-implementation/SKILL.md` - Revision final del Manager
- `../session-close-observations/SKILL.md` - Generar observaciones de cierre
- `../manager-session-closeout/SKILL.md` - Clasificar learnings de cierre y preparar el puente humano
- `../memory-consolidate/SKILL.md` - Consolidacion de memoria

## Constraints

- **NO** usar `work_plan_cierre.md` como plan activo sin actualizar antes el tooling
- **NO** borrar archivos o mover estructura por intuicion
- **NO** cerrar sin documentar que queda fuera de alcance y que va a backlog
- **SIEMPRE** dejar explicito el estado de mantenimiento al cerrar
- **SIEMPRE** pedir aprobacion humana para bump, tag, release o archivado
- **SIEMPRE** verificar que la documentacion describe el estado real del repo
- **SIEMPRE** ejecutar el preflight de entrega antes del `--mark-ready` y del push final
