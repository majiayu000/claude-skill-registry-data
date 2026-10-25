---
name: orchestrate-child-dispatch-multiticket-multibackend-unlimited
version: 1.0.0
description: Gobierno EXPERIMENTAL que anade al ejecutor autonomo el dispatch real padre/hijo por ticket (Capa 0 -> Manager-hijo -> Builder/Revisor) sobre MAS DE UN backend (Claude Code, Kilo, OpenCode), con lock sostenido del SO anti split-brain, registro de identidad Builder!=Revisor verificable por transporte, decision de workspace por ticket y el paso de integracion antes del push agrupado. Usar cuando un vuelo multi-ticket necesita dispatch real a backends distintos, no solo el pipeline de un unico backend. No usar si el vuelo cabe en un solo backend (ver orchestrate-autonomous-ticket-batch, orchestrate-pipeline, orchestrate-pipeline-codeonly); no redeclara el PREDICATE, las 8 barreras ni el GROUP_STOP_REPORT de esos prompts.
triggers: [/orchestrate-child-dispatch, orchestrate-child-dispatch-multibackend, dispatch-hijos-multibackend]
author: agent
role: orchestrator
stage: meta
writes_memory: false
quality_gate: false
tags: [core, system, orchestration, multibackend, experimental]
source_prompt: prompts/orchestrator_child_dispatch_multiticket_multibackend_unlimited.md
contract_id: cid-orchestrator-child-dispatch-multiticket-multibackend-unlimited-v1
status: experimental
---

# orchestrate-child-dispatch-multiticket-multibackend-unlimited

Skill minima que apunta al gobierno de dispatch padre/hijo multi-ticket,
multi-backend, sin tope de tickets por vuelo. **Esta skill SOLO apunta: no
re-declara criterios normativos** ("skill apunta, prompt gobierna", X-09,
`AGENTS.md`).

**Estado: EXPERIMENTAL.** La condicion de promocion a uso rutinario vive
UNICAMENTE en el nucleo (seccion "Que NO hacer", ultimo bullet) -- esta skill
no la repite ni la resume en palabras propias: una paráfrasis aqui es
exactamente la segunda fuente de interpretacion que X-09 prohibe. Lee el
nucleo para saber que evidencia falta.

## Fuente canonica

- **Nucleo:** `prompts/orchestrator_child_dispatch_multiticket_multibackend_unlimited.md`
  - `contract_id: cid-orchestrator-child-dispatch-multiticket-multibackend-unlimited-v1`
- **Diseno congelado que lo origina:**
  `.agent/planning/PROPUESTA_orquestador_hijos_multibackend_vuelo_sin_limite_20261020.md`.
  La lista exacta de secciones load-bearing vive SOLO en el encabezado del
  nucleo -- no se repite aqui (hallazgo Ronda 2, nan_deepseek-fallback: una
  segunda copia de esa lista en la skill es el mismo vector de
  desincronizacion que X-09 existe para evitar).

## Que gobierna el nucleo (no redeclarado aqui)

Lock sostenido del SO de la Capa 0, mecanismo de lanzamiento por backend y su gate
de restriccion de despacho, registro de lanzamiento e identidad Builder!=
Revisor y su gate de identidad no verificada, decision de workspace por
ticket, integracion antes del push agrupado, las condiciones de parada
propias de este gobierno adicional, y la condicion exacta de promocion a
canonico. **Todo vive en el prompt, con su semantica exacta -- leelo entero
antes de aplicar o de citar cualquiera de sus gates.**

## Distincion con skills hermanas (nunca sustituye, siempre se APILA)

- **`orchestrate-autonomous-ticket-batch`**: consume el DAG de `/backlog-triage`
  y cierra tickets con el PREDICATE de 9 condiciones, las 8 barreras y el
  `GROUP_STOP_REPORT`. Esta skill NO los redeclara -- se inserta DENTRO del
  lanzamiento de Builder de ese ejecutor cuando un ticket necesita un
  Manager-hijo propio en un backend distinto.
- **`orchestrate-pipeline` / `orchestrate-pipeline-codeonly`**: pipeline
  por-ticket de UN solo backend. Si el vuelo entero cabe en uno, usa esas, no
  esta.
- **`kilo_trio_dispatch`** (prompt, sin skill propia todavia): ya cubre el
  mecanismo de lanzamiento Kilo completo. Esta skill remite, no redeclara.
- **`manager-orchestrator-loop`**: nucleo Manager-Builder generico de
  cualquier sistema, sin nocion de backend ni de dispatch padre/hijo
  multi-backend. Dominio distinto.

## Condicion de entrada

Antes de invocar esta skill, verifica el Paso 0 del nucleo -- no redeclarado
aqui a proposito (hallazgo de Ronda 1: una version anterior de esta skill
transcribia las dos condiciones del Paso 0, violando X-09). Si el nucleo
dice que no aplica, no uses esta skill.
