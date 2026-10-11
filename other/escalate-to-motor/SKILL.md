---
name: escalate-to-motor
version: 1.0.0
description: Contrato de redaccion de un escalado destino a motor como ficha FP en el buzon backlog_inbox del WORKSPACE DEL MOTOR, con recibo reejecutable, procedencia por claim y condicion de rechazo declarada. Usar cuando un repo_destino detecta un defecto, deuda o propuesta que pertenece al motor y no al destino; se invoca en el chat del destino. No usar para el pipeline de tickets del destino (ver orchestrate-pipeline) ni para la escalacion intra-repo de Builder a Manager (ver manager-resolve-escalation); no autoriza a tocar repo_motor.
triggers: [/escalate-to-motor, escalar-al-motor, escalado-motor]
author: agent
role: auditor
stage: review
writes_memory: false
quality_gate: false
tags: [core, escalation, motor, destino]
source_prompt: prompts/escalate_to_motor.md
contract_id: cid-escalate-to-motor-v1
---

# escalate-to-motor

Skill para escalar al MOTOR un hallazgo que pertenece al motor y no al
`repo_destino` desde el que se detecta.

## Fuente canonica

Leer y aplicar ENTERO:

- `<MOTOR_ROOT>/prompts/escalate_to_motor.md`

Este SKILL es un PUNTERO. No re-declara clasificaciones, secciones obligatorias,
reglas de autoridad ni criterios de aceptacion: viven una sola vez en el prompt.
Si esta skill y el prompt divergen, **prevalece el prompt** y la divergencia es un
bug de la skill.

## Cuando usarla

- Un destino detecta un defecto, deuda o propuesta cuya superficie es el MOTOR.
- El hallazgo no se puede arreglar desde el destino (el motor es read-only).

## Cuando NO usarla

- Es un escalado Builder -> Manager dentro de una sesion: eso es
  `manager-resolve-escalation`, otra skill y otro contrato.

El criterio de que hallazgos pertenecen al motor y cuales al destino lo define el
prompt (seccion 0); no se re-declara aqui.

## Contratos relacionados (no los repitas: cumplelos)

- Ingesta y fusion: Bloque 8.bis de
  `<MOTOR_ROOT>/prompts/orchestrator_session_close_full_audit.md`.
- Formato y reglas del buzon:
  `<destination_root>/.agent/collaboration/backlog_inbox/README.md`.
