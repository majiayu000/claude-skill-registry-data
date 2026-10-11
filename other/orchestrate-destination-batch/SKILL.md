---
name: orchestrate-destination-batch
version: 1.0.0
description: Orquesta en un lote secuencial varios repo_destino hasta un estado de publicacion explicito, uno a uno, clasificandolos con batch_destination_controller.py, conduciendo Contract Formation y el pipeline por ticket con los prompts canonicos y dejando un manifest global reanudable. Usar cuando hay que preparar y auditar varios repo_destino para publicacion remota en un unico lote. No usar para sustituir el pipeline por destino (ver orchestrate-pipeline), Contract Formation (ver contract_formation_pipeline) ni la auditoria de publicacion (ver audit-git-publication); no crea repos remotos ni hace push.
triggers: [/batch-destinos, orchestrate-destination-batch, preparar-repos, batch-publicacion]
author: agent
role: orchestrator
stage: meta
writes_memory: false
quality_gate: false
tags: [core, system, chat-flow, publication]
source_prompt: prompts/orchestrator_destination_batch.md
contract_id: cid-orchestrator-destination-batch-v1
---

# orchestrate-destination-batch

Wrapper operativo para conducir un lote de `repo_destino` y dejarlos listos para
publicacion remota privada. El gobierno normativo vive en
`prompts/orchestrator_destination_batch.md`; si esta skill y el prompt divergen,
prevalece el prompt.

Esta skill NO es un orquestador nuevo: reusa `orchestrate-pipeline` por destino y
`audit-git-publication` para la decision de publicacion. Solo coordina el orden
entre destinos y materializa un manifest con evidencia por repo.

## Cuando usarla

- Tienes varios repos que deben integrarse con el motor y quedar listos para
  GitHub privado.
- Quieres procesarlos uno a uno, de forma reanudable, sin un verde agregado.
- Quieres separar `integrado`, `clasificado`, `auditado` y `publicable`.

## Cuando NO usarla

- Para un solo destino: usa `orchestrate-pipeline` directamente.
- Para publicar/pushear: el batch NO crea el repo remoto ni hace push. Eso
  requiere permiso humano explicito fuera del batch autonomo.

## Herramienta determinista

```powershell
python <MOTOR_ROOT>/scripts/batch_destination_controller.py `
  --repos <REPOS_JSON> `
  --motor-root <MOTOR_ROOT> `
  --out-dir <OUT_DIR> `
  --run-readonly-gates
```

`<REPOS_JSON>` declara los destinos (agnostico, sin numero fijo):

```json
{
  "repos": [
    {"path": "<abs>/repo-a", "shared_surfaces": ["api:orders"], "authorized_motor_write": false},
    {"path": "<abs>/repo-b", "shared_surfaces": ["api:orders"]}
  ]
}
```

Salida: `batch_manifest.json` + `batch_manifest.md` en `<OUT_DIR>`. Cada fila
lleva su `evidence[]` con `path:` / `command:`. El manifest es indice reanudable,
no fuente de verdad: el estado real vive en `.agent/`, bus, backlog, git y
closeouts.

## Regla de publicacion (no la rompas)

`publishable=true` SOLO con las tres capas:

1. `integrated_local` — `check_destino_publish_ready.py` (estado vivo).
2. `publication_classified` — `classify_publication.py` con historia completa.
   Su verdict es **[RELATO]**, no evidencia final.
3. `publication_audit_passed` — Pasada B de `prompts/audit_git_publication.md`
   (un agente abre archivos y re-deriva por contenido) con closeout.

El verdict del script determinista NUNCA basta por si solo: `next_action`
mostrara `RUN_AUDIT_GIT_PUBLICATION_PASS_B` hasta que exista la evidencia de
auditoria.

## Flujo resumido (detalle en el prompt)

1. Topologia por destino: re-fijar y verificar `AGENT_PROJECT_ROOT`.
2. Clasificar con `batch_destination_controller.py --run-readonly-gates`.
3. Adoptar/reparar si `adopted=false`.
4. Contract Formation + `audit_cf_ticket_contract.md` si `contract_ready=false`.
5. `orchestrate-pipeline` por ticket (snapshot/check motor ya es canon ahi).
6. Auditorias de cierre + clasificacion de publicacion (historia completa).
7. `audit-git-publication` Pasada B.
8. Recheck inter-repo de superficies compartidas.
9. Siguiente destino.

## Criterios de parada

Stop-candidates NO detienen el lote por sospecha temprana: se documentan tras N
intentos adversariales y se presentan en el informe. Solo un
`GLOBAL_PIPELINE_BLOCKER` (fallo sistemico externo) detiene el lote completo.
Detalle de taxonomia en `prompts/orchestrator_destination_batch.md`.
