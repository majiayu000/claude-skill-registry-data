---
name: session-hop
version: 1.0.0
description: Puente entre sesiones, de solo lectura, que produce el arranque de la sesion siguiente con el METODO heredado y el ESTADO re-medido (cada dato con su comando y exit code) y como mucho lo escribe en orchestrator_pipeline/arranques/. Usar cuando se prepara el arranque de la sesion siguiente con continuidad medida, al final de una sesion o desde el estado ya recolectado. No usar para la auditoria adversarial previa al cierre (ver session-close-full-audit), para definir el rol o el metodo de la sesion siguiente (ver orchestrator_session_bootstrap), para leer el estado de UN ticket (comandos /pause-work, /resume-work y /session-report) ni para ejecutar el trabajo de la sesion; no cierra la sesion.
triggers: [/session-hop, session-hop]
author: agent
role: manager
stage: plan
writes_memory: false
quality_gate: false
tags: [core, system, session]
source_prompt: prompts/session_hop.md
contract_id: cid-session-hop-v1
---

# session-hop

Skill para preparar el arranque de una sesion nueva que continua a otra.

**El prompt `prompts/session_hop.md` es la fuente de verdad**; si esta skill y el prompt
divergen, prevalece el prompt y la divergencia es un bug de esta skill. Esta pagina es
puntero operativo: **no re-declara criterios**.

## Cuando usarla

Al terminar una sesion (o al pausarla) cuando la siguiente deba continuar el trabajo:
un vuelo que sigue a un triaje, una auditoria hermana que sigue a un cierre, una sesion
de diseno que releva a otra.

## Cuando NO usarla

- Para **cerrar** una sesion: eso es `session-close-full-audit` +
  `agent_controller.py --session-close`.
- Para resumir el estado operativo de UN ticket: eso ya lo hacen `/pause-work`,
  `/resume-work` y `/session-report`, que son ortogonales a esta skill.
- Para definir el ROL de la sesion nueva: eso es
  `prompts/orchestrator_session_bootstrap.md` (o su variante `_design`). Esta skill
  transporta la CONTINUIDAD, no el rol.

## Workflow

Los pasos, sus reglas y sus restricciones viven en `prompts/session_hop.md` (Pasos 1-7 y
"Restriccion dura"). Leelo entero antes de producir el arranque.

Herramienta de apoyo:

```bash
python <MOTOR_ROOT>/scripts/collect_session_state.py --project-root <DESTINO_ROOT>
```

El script recolecta hechos con su `command:` y su `exit_code:`. El juicio lo emite el
agente, no el script.

## Alcance

Es del **motor**: gobierna contratos, topologia motor<->destino y memoria portable, que
no son propiedad de ningun destino. `MANIFEST.workspace` excluye `scripts/` y `skills/`
del destino, asi que esta capacidad no se instala en los proyectos destino.
