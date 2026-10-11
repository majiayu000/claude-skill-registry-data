---
name: manager-orchestrator-loop
version: 1.0.0
description: Skill minima que apunta al nucleo del proceso Manager-Builder por contract_id y sha256, SIN herramienta. Usar cuando un Manager necesita orquestar un objetivo con bucles de revision adversarial sobre una estrategia, sobre cada plan y sobre el prompt del ejecutor, en CUALQUIER sistema. No usar para despachar lentes contra un proveedor concreto ni para encargar una tarea a un backend (eso vive en prompts/ensemble_loop.md y prompts/builder_invocation_contract.md).
triggers: [/manager-loop, /manager-orchestrator, /proceso-manager]
author: agent
role: manager
stage: orchestrator
writes_memory: false
quality_gate: false
tags: [core, process, orchestrator, portable]
source_prompt: prompts/manager_orchestrator_loop.md
contract_id: cid-manager-orchestrator-loop-v1
nucleo_sha256: 909543817393de016021657c85fa298fd1db768c5702f2aff86bde93df1bd19b
---

# manager-orchestrator-loop

Skill minima para invocar el nucleo del proceso Manager-Builder portatil.
Esta skill SOLO apunta: no re-declara criterios del nucleo ("skill apunta,
prompt gobierna").

## Fuente canonica

- **Nucleo:** `prompts/manager_orchestrator_loop.md`
  - `contract_id: cid-manager-orchestrator-loop-v1`
  - `sha256: 909543817393de016021657c85fa298fd1db768c5702f2aff86bde93df1bd19b`

## Adaptador de referencia

- `prompts/manager_orchestrator_loop_adapter_motor.md`: traduce cada capacidad del
  nucleo a los comandos reales de este motor (si divergen, prevalece el nucleo).

## Contraproporcion (regla del repo: "skill apunta, prompt gobierna")

PROHIBIDO re-declarar criterios normativos (estados, roles, reglas de validez
de un bucle, plantillas, esquemas, metricas) en esta skill. Estos criterios
viven una vez en el nucleo (`prompts/manager_orchestrator_loop.md`) y esta
skill solo los remite. Si divergen, prevalece el nucleo.

## Identidad de contrato

Antes de seguir NINGUNA instruccion, verifica que el nucleo accesible tiene el
mismo sha256 que se declara aqui:

```bash
# En el repo del motor:
python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" <ruta_al_nucleo>
```

El resultado debe ser `909543817393de016021657c85fa298fd1db768c5702f2aff86bde93df1bd19b`.
Si no coincide, o si el nucleo no es accesible, DETENTE e informa al
orquestador. No continuar con un nucleo de hash diferente.

## Que gobierna el nucleo

Todo el contenido normativo (roles, capacidades, validez de un bucle, estados, plantillas, esquemas y metricas) vive
SOLO en `prompts/manager_orchestrator_loop.md`: leelo entero. Esta skill no lo resume a proposito: un resumen deriva del
nucleo en cuanto este cambia (paso en su primera version: el resumen ya citaba esquemas que el nucleo habia renombrado).

## Distincion con skills hermanas

- `ensemble_loop`: despachador de lentes (proveedor concreto). El nucleo no
  sabe de proveedores; el ADAPTADOR traduce.
- `builder-implement-from-plan`: contraparte del Builder. El Manager apunta al
  nucleo; el Builder implementa segun work_plan aprobado.
- `manager-review-implementation`: revision de implementacion del Builder. El
  nucleo define el ciclo completo; esta skill cubre la fase REVISION.
