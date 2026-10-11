---
name: agent-execution-mode
version: 1.0.0
description: Skill minima que apunta al nucleo de los 3 modos de ejecucion multiagente (Tradicional, 4 capas, Intermedio) por contract_id y sha256, SIN herramienta. Usar al arrancar una sesion que orqueste trabajo sobre tickets del backlog, o para cambiar de modo en caliente a mitad de conversacion. No usar para despachar lentes contra un proveedor concreto (eso vive en prompts/ensemble_loop.md) ni para el proceso Manager-Builder en si (eso vive en manager-orchestrator-loop).
triggers: [/agent-mode, /modo-agente, /execution-mode]
natural_language_triggers: ["usa las 4 capas", "usa 4 capas", "hazlo tu directamente", "modo tradicional", "modo intermedio", "cambia a 4 capas", "cambia a tradicional", "cambia a intermedio"]
author: agent
role: orchestrator
stage: orchestrator
writes_memory: false
quality_gate: false
tags: [core, process, orchestrator, portable]
source_prompt: prompts/agent_execution_modes.md
contract_id: cid-agent-execution-modes-v1
nucleo_sha256: 451b923a57b8197c19912087cd77c484400c7adcc920efd88e29ffa555c02663
status: frozen
---

# agent-execution-mode

Skill minima para invocar el nucleo de los 3 modos de ejecucion multiagente
(Tradicional / 4 capas / Intermedio). Esta skill SOLO apunta: no re-declara
criterios del nucleo ("skill apunta, prompt gobierna", X-09).

**Estado: `frozen`** (congelado tras 2 pasadas de bucle adversarial, ver
Seccion 6.1/6.2 del nucleo). Los criterios son normativos.

## Fuente canonica

- **Nucleo:** `prompts/agent_execution_modes.md`
  - `contract_id: cid-agent-execution-modes-v1`
  - `sha256: 451b923a57b8197c19912087cd77c484400c7adcc920efd88e29ffa555c02663`

## Como se invoca

- **Al arrancar una sesion** que vaya a orquestar trabajo sobre el backlog
  (un ticket suelto o un vuelo largo): el agente aplica la Seccion 2 del
  nucleo (señales de propuesta) y PROPONE un modo, nunca lo activa en
  silencio.
- **A mitad de conversacion** (`/agent-mode <tradicional|4capas|intermedio>`
  o en lenguaje natural, "cambia a 4 capas", "hazlo tu directamente"): el
  agente aplica el protocolo de cambio en caliente (Seccion 5 del nucleo).

## Contraproporcion (regla del repo: "skill apunta, prompt gobierna")

PROHIBIDO re-declarar criterios normativos (los 3 modos, las señales de
propuesta, la allowlist de blast-radius-alto, el protocolo de cambio en
caliente) en esta skill. Estos criterios viven una vez en el nucleo
(`prompts/agent_execution_modes.md`) y esta skill solo los remite. Si
divergen, prevalece el nucleo. La seccion "Identidad de contrato" de abajo
es MECANISMO de verificacion (igual que en `manager-orchestrator-loop`),
no contenido normativo nuevo -- aclarado tras bucle adversarial, Seccion 6
del nucleo, por una duda real de una lente sobre si esa seccion violaba
X-09.

## Identidad de contrato

Antes de seguir NINGUNA instruccion, verifica que el nucleo accesible tiene
el mismo sha256 que se declara aqui:

```bash
python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" prompts/agent_execution_modes.md
```

El resultado debe ser
`451b923a57b8197c19912087cd77c484400c7adcc920efd88e29ffa555c02663`.
Si no coincide, o si el nucleo no es accesible, DETENTE e informa al
orquestador. No continuar con un nucleo de hash diferente.

## Que gobierna el nucleo

Todo el contenido normativo (los 3 modos, las señales de propuesta, la
allowlist reusada, el protocolo de cambio en caliente, el gobierno de esta
misma propuesta) vive SOLO en `prompts/agent_execution_modes.md`: leelo
entero. Esta skill no lo resume a proposito.

## Distincion con skills hermanas

- `manager-orchestrator-loop`: el PROCESO Manager-Builder en si (bucles de
  revision adversarial sobre una estrategia/plan/prompt del ejecutor). Esta
  skill decide QUE PATRON DE DELEGACION usar (quien implementa, quien
  revisa); `manager-orchestrator-loop` decide COMO se gobierna cada decision
  dentro de ese patron. Son complementarias, no alternativas.
- `orchestrate-pipeline`/`orchestrate-autonomous-ticket-batch`: ejecutores
  concretos de un pipeline ya decidido. Esta skill se invoca ANTES, para
  decidir si ese pipeline corre en modo Tradicional, 4 capas o Intermedio.
- `ensemble_loop` (prompt, no skill): despachador de lentes de REVISION
  adversarial de una decision de diseño (el mecanismo que congelo el
  propio nucleo de esta skill). No decide el modo de ejecucion de tickets.
