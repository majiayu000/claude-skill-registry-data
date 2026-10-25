---
name: agents-md-intake-triage
version: 1.0.0
description: "Protocolo de admision que un agente corre ANTES de anadir contenido nuevo a AGENTS.md o CLAUDE.md (motor o repo_destino): barrido anti-duplicado sobre las superficies de documentacion, clasificacion por funcion y clase, regla de aterrizaje (ninguna adicion entra directa a la cuspide) y gate de presupuesto, con declaracion explicita obligatoria. Usar cuando se va a anadir contenido nuevo a AGENTS.md, CLAUDE.md o un modulo de .agent/rules/common/. No usar para trasladar contenido ya existente (ver doc-optimization), para triar tickets del backlog (ver backlog-triage) ni para promover aprendizajes a memoria (ver memory_upload / memory-consolidate)."
triggers: [/agents-md-triage, agents-md-intake]
author: agent
role: manager
stage: plan
writes_memory: false
quality_gate: false
tags: [core, system, documentation, context]
source_prompt: prompts/agents_md_intake_triage.md
contract_id: cid-agents-md-intake-triage-v1
---

# agents-md-intake-triage

Skill para el triaje de ADMISION de contenido nuevo a `AGENTS.md`/`CLAUDE.md` y
sus modulos de dominio, antes de escribir. Es el gate de admision que responde
al hueco de ENFORCEMENT de la incorporacion futura documentado en
`.agent/planning/agents_md_optimization/propuesta_restructuracion_arquitectonica.md`
(Seccion 5 hallazgo #3, convergente en 7+4 lentes).

NO reimplementa el metodo: el flujo completo (declarar raiz, barrido
anti-duplicado por superficies, clasificacion por funcion/clase, regla de
aterrizaje por defecto, gate de presupuesto antes/despues, declaracion
obligatoria) vive en `prompts/agents_md_intake_triage.md`. **El prompt es la
fuente de verdad; si algo diverge, prevalece el prompt** (X-09: skill apunta,
prompt gobierna).

## Cuando usarla

- Un agente va a anadir contenido nuevo a `AGENTS.md`, `CLAUDE.md`, un modulo de
  `.agent/rules/common/` o `.claude/rules/`, y hay que decidir SI entra, DONDE y
  CON QUE compensacion antes de escribir.

## Cuando NO usarla

- Para trasladar/recortar contenido YA existente en lo siempre-cargado (usar
  `doc-optimization`).
- Para triar tickets del backlog (usar `backlog-triage`: tria tickets, no
  documentacion siempre-cargada).
- Para promover aprendizajes a memoria (usar `memory_upload` /
  `memory-consolidate`: dominio memoria, no reglas operativas).

## Ver tambien (contratos citados por referencia, no copiados aqui)

Este triaje empaqueta tres contratos existentes, cada uno con su propio dueno
normativo (la skill y el prompt remiten, no re-declaran sus criterios):

- `prompts/doc_optimization.md` -- clasificacion por funcion/clase (PASO 1,
  PASO 2) y gate de presupuesto (PASO 1).
- `prompts/backlog_triage.md` -- Fase 0.ante (barrer todas las superficies con
  lectura completa).
- `prompts/memory_upload.md` -- "Procedimiento de barrido anti-duplicado":
  nunca descartar por titulo; `find_similar_signals.py` es senal, no veredicto.

## Prompt canonico

Leer y aplicar `prompts/agents_md_intake_triage.md`. Estados terminales,
declaracion obligatoria y restricciones duras: ver el prompt -- no se re-declaran
aqui.

## Restriccion dura

- La skill es puntero: no re-declara los pasos del prompt ni las cifras de los
  contratos duenos. Remite al prompt.
- No decide el destino final del cierre de sesion (ese es el prompt de cierre),
  ni ejecuta gate automatico de crecimiento (decision del usuario pendiente, ver
  prompt "Fuera de alcance").
