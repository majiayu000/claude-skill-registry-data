---
name: backlog-admit
version: 1.0.0
description: Alta de un ticket nuevo como fila de backlog.md con el recibo mecanico BACKLOG-ADMISSION-RECIBO que emite backlog_db_compare.py y contrasta check_backlog_admission.py. Usar cuando el PASO 0 del protocolo de hallazgos decide que la senal merece una fila nueva, antes de commitear el alta. No usar para el triaje pre-pipeline (ver backlog-triage) ni para escalar un hallazgo del motor al buzon (ver escalate-to-motor).
triggers: [/backlog-admit, backlog-admit, /alta-backlog]
author: agent
role: builder
stage: plan
writes_memory: false
quality_gate: false
tags: [backlog, admission, gate]
source_prompt: prompts/backlog_admit.md
contract_id: cid-backlog-admit-v1
---

# backlog-admit

Skill para dar de alta un ticket nuevo en el backlog del repo del alta,
incluyendo el recibo de barrido que satisface el guard
`check_backlog_admission.py`.

## Overview

Cuando un hallazgo del PASO 0 se clasifica como ALTA (fila nueva en
`backlog.md`), esta skill guia la generacion del recibo y el commit correcto.

## Workflow

1. Leer el prompt canonico: `prompts/backlog_admit.md`
2. Ejecutar el barrido previo (PASO 0 del protocolo)
3. Generar el recibo con `backlog_db_compare.py --emit-recibo`
4. Commit con el recibo en el mensaje

## References

- `prompts/backlog_admit.md` -- prompt canonico (contract_id: cid-backlog-admit-v1)
- `scripts/backlog_db_compare.py` -- generador del recibo (--emit-recibo)
- `scripts/check_backlog_admission.py` -- guard que contrasta el recibo

## Constraints

- Esta skill es PUNTERO operativo al prompt canonico.
- PROHIBIDO re-declarar criterios normativos en esta SKILL.md.
- Si esta skill y el prompt divergen, prevalece el prompt.
