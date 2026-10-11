---
name: setup-agent-system
version: 2.1.0
description: Instalar o sincronizar un repo_destino para usar el motor externo orquestador_de_agentes con link portable, perfil host-project y preflight verificable. Usar cuando se instala el sistema en un destino nuevo, se sincroniza uno ya instalado, o se verifica su enlace al motor. No usar para un proyecto YA EXISTENTE con motor viejo embebido (ver adopt-existing-project) ni para crear un proyecto Python desde cero (ver scaffold-python-project).
triggers: [/agent-setup, /agent-install, /init]
author: agent
role: user
stage: setup
cycle_phase: [F0-arranque-sesion]
writes_memory: false
quality_gate: false
tags: [core, system, destination, host-extends]
---

# setup-agent-system

Prepara un `repo_destino` para consumir el motor externo
`orquestador_de_agentes` sin copiar el motor completo ni convertir el estado del
destino en estado del `repo_motor`.

## Modelo vigente

- `repo_motor`: raiz unica del motor portable.
- `repo_destino`: proyecto que conserva `.agent/` con estado, memoria,
  eventos y configuracion local.
- El destino referencia al motor mediante
  `.agent/config/motor_destination_link.json`.
- Los comandos operativos que tocan estado del destino usan
  `--project-root <repo_destino>` o `AGENT_PROJECT_ROOT=<repo_destino>`.
- El perfil de agentes instalado en destino debe quedar como `host-project`,
  no `engine-dev`.

## Cuando usarla

Usar para:

- instalar el sistema en un destino nuevo;
- sincronizar un destino ya instalado con el motor actual;
- verificar que un destino quedo enlazado al motor correcto;
- preparar el primer ciclo operativo antes de usar
  `prompts/orchestrator_destination_bootstrap.md`.

No usar para:

- copiar manualmente `.agent/agent_controller.py`, `scripts/` o `skills/` como
  codigo operativo del destino;
- retirar copias legacy sin revisar consumidores vivos;
- publicar el repo en Git. Para eso usa
  `scripts/check_destino_publish_ready.py` como gate pre-push de drift
  operativo, y `prompts/audit_git_publication.md` +
  `skills/audit-git-publication/SKILL.md` (`/audit-git-publication`) para la
  auditoria de primera publicacion publica.

## Preflight

1. Confirmar que el `repo_destino` tiene Git inicializado.
2. Confirmar Python 3.10+ y `uv` si el proyecto lo requiere.
3. Elegir o confirmar el `Ticket prefix:` del destino.
4. Confirmar que no hay secretos reales en el arbol antes de instalar.
5. Si existe `.claude/settings.json`, tratarlo como superficie sensible:
   despues de instalar, debe pasar
   `python <repo_motor>/scripts/check_claude_settings_portability.py .claude/settings.json`.

## Instalacion

Ejecutar desde el `repo_motor` o pasando rutas absolutas claras:

```powershell
python scripts/install_agent_system.py --install --dest <repo_destino> --prefix <XXX>
```

Si la version local del instalador difiere, ejecutar `--help` y usar el flag de
destino equivalente. No improvisar copia manual del bundle.

El instalador debe dejar como minimo:

- `.agent/config/motor_destination_link.json`;
- `.agent/config/agents.json` con `active_profile: host-project`;
- `PROJECT.md` con `Ticket prefix: <XXX>` si se proporciono prefijo;
- `.gitleaks.toml` seed si no existia configuracion local;
- superficies destino-keep declaradas en `MANIFEST.workspace`.

## Sincronizacion

Para actualizar un destino ya instalado:

```powershell
python scripts/install_agent_system.py --sync --dest <repo_destino>
```

Reglas:

- no usar `--sync` como poda ciega de host-extends;
- no borrar rutas trackeadas del destino;
- si existe `.agent/host-setup.sh` o `.agent/host-setup.ps1`, revisar las
  primeras lineas y pedir confirmacion humana salvo `--yes`;
- si el hook falla, la sync falla.

## Verificacion posterior

Desde el `repo_destino`:

```powershell
$env:AGENT_PROJECT_ROOT = (Resolve-Path .).Path
python <repo_motor>/scripts/destination_context.py --bootstrap --project-root .
python <repo_motor>/.agent/agent_controller.py --validate --json --project-root .
python <repo_motor>/scripts/memory_context.py --status
```

Resultado esperado:

- `destination_context.py` genera `.agent/context/destination_map.md`;
- `validate --json` devuelve 0 errores antes de arrancar Builder;
- `memory_context.py --status` resuelve memoria del destino, no del motor;
- `motor_destination_link.json` apunta al `repo_motor` correcto.

## Primer ciclo operativo

1. Usar `prompts/orchestrator_destination_bootstrap.md` para arrancar una sesion en el
   destino.
2. Si se van a ejecutar varios tickets, usar
   `prompts/orchestrator_pipeline.md` y
   `skills/orchestrate-pipeline/SKILL.md`.
3. Antes de publicar commits del destino que toquen `.agent/collaboration/`,
   correr:

```powershell
python <repo_motor>/scripts/check_destino_publish_ready.py --project-root <repo_destino> --motor-root <repo_motor>
```

4. Antes de una primera publicacion publica del repo, ejecutar la auditoria
   dry-run:

```powershell
python <repo_motor>/scripts/classify_publication.py --repo-root <repo_destino> --out <repo_destino>/orchestrator_pipeline/reports/publication_manifest.json
```

Luego aplicar `prompts/audit_git_publication.md`; no publicar solo por tener
un exit code verde de otro gate. La skill canonica para esa auditoria es
`skills/audit-git-publication/SKILL.md` (`/audit-git-publication`).

## Contrato de fallo

- Si falta `motor_destination_link.json`, el destino no esta bootstrappeado.
- Si `validate --json` tiene errores, no arrancar Builder.
- Si el root operativo apunta al motor en vez del destino, detenerse.
- Si un setup requiere escribir rutas fuera del destino o del motor declarado,
  pedir aprobacion humana.
- Si una instruccion antigua recomienda copiar `.agent/`, `scripts/` o
  `skills/` manualmente, tratarla como legacy y preferir el instalador.
