---
name: adopt-existing-project
version: 1.0.0
description: Adecuar un proyecto Python YA EXISTENTE (legacy o con motor viejo embebido) al motor portable, orquestando las skills y scripts existentes en el orden correcto. Usar cuando se incorpora un repo con codigo previo como repo_destino. No usar para un destino nuevo o limpio (ver setup-agent-system) ni para crear un proyecto desde cero (ver scaffold-python-project).
triggers: [/adopt-project, /adopt-existing, /adecuar-proyecto]
author: agent
role: user
stage: setup
cycle_phase: [F0-arranque-sesion]
writes_memory: false
quality_gate: false
tags: [core, system, destination, host-extends, migration]
---

# adopt-existing-project

Protocolo de **adecuación** de un proyecto Python que **ya existe** (con código,
datos, posiblemente una copia vieja del motor embebida y/o sin Git) para que pase
a consumir el motor portable `orquestador_de_agentes` como `repo_destino`.

Es **pegamento operativo, NO un sistema paralelo.** No reimplementa la instalación,
el bootstrap ni la planificación: los **invoca en el orden correcto** para el caso
"proyecto preexistente", y solo añade lo que ninguna skill cubre hoy (cierre de
WPs legacy como históricos, `.gitignore` anti-fuga en raíz externa, sincronización
de entrypoints, verificación de portabilidad).

## Diferencia con skills hermanas (frontera explícita)

- `setup-agent-system` (`/agent-setup`): instala/sincroniza el link motor↔destino.
  **Esta skill lo INVOCA** en la Fase 2; no lo duplica. `setup-agent-system` asume
  un proyecto limpio o nuevo; `adopt-existing-project` asume legacy con fricción.
- `scaffold-python-project` (`/scaffold`): crea un proyecto Python **nuevo desde
  cero**. Si el proyecto no existe aún, usa esa, no esta.
- `secure-existing-project` (`/secure`): migra credenciales a `privada/`. **Esta
  skill la INVOCA** en la Fase 1 si hay secretos hardcodeados.
- `orchestrator_destination_bootstrap.md`: arranca una sesión en un destino **ya
  adecuado**. Es el paso SIGUIENTE a esta skill, no parte de ella.
- `manager-create-work-plan` / `orchestrate-pipeline`: ejecutan los tickets de
  desarrollo. Vienen DESPUÉS de adecuar.

## Cuándo usarla

- Tienes un proyecto Python que funciona pero no consume el motor actual.
- El proyecto tiene una copia vieja/embebida del motor (`agent_system/`,
  `agent_controller` legacy) que hay que integrar sin descartar el trabajo válido.
- El proyecto no tiene Git, o lo tiene pero nunca se publicó.
- Quieres dejarlo listo para abrir tickets `<PREFIX>` formales después.

## Cuándo NO usarla

- Proyecto nuevo desde cero → `scaffold-python-project`.
- Destino ya adecuado y solo quieres operarlo → `orchestrator_destination_bootstrap.md`.
- Solo actualizar un destino ya instalado al motor actual → `setup-agent-system --sync`.

---

## Checklist canónica de adecuación (5 fases)

> Las fases son secuenciales con gates. NO avances de fase con el gate en rojo.
> `MOTOR` = raíz de `orquestador_de_agentes`. `DEST` = raíz del proyecto a adecuar.
> Todas las operaciones de estado del destino usan `--project-root <DEST>` o
> `AGENT_PROJECT_ROOT=<DEST>`. El motor permanece **pristine** (verificable con
> `scripts/check_motor_pristine.py --snapshot` antes y `--check` después).

### FASE 1 — Inventario y seguridad (pre-flight)

1. **Topología:** confirma qué será `DEST` (la raíz externa real, no una subcarpeta
   de código). Decide el `Ticket prefix:` (3 letras, p.ej. `EXF`). `WOT-` es SOLO
   del motor/dogfooding, nunca de un destino.
2. **Inventario de sensibles:** localiza datos reales (config con credenciales,
   datos personales, Excels, logs). Anótalos: son lo que el `.gitignore` raíz DEBE
   excluir. Si hay secretos **hardcodeados en código** → invoca
   `secure-existing-project` (`/secure`) para moverlos a `privada/`.
3. **Backup del legacy:** si hay motor viejo embebido (`agent_system/` u otro),
   cópialo FUERA de `DEST` antes de tocar nada. **No se borra** (decisión de
   integración, no de descarte): se ignora en Git en la Fase 4.
4. **Git preexistente:** ¿`DEST` ya tiene `.git`? Barrido:
   `git -C <DEST> rev-parse --git-dir` + búsqueda recursiva de `.git`. Si hay
   historia previa, hay que auditarla por secretos ANTES de cualquier push
   (Fase 5), no asumir que está limpia.

**Gate F1:** topología decidida, sensibles inventariados, legacy respaldado, estado
Git conocido.

### FASE 2 — Instalación del motor (INVOCA setup-agent-system)

5. **Retira `.agent` residual** si existe uno parcial de exploraciones previas (el
   instalador aborta si `.agent/` ya existe sin ser una instalación válida): muévelo
   a backup y confirma `Test-Path <DEST>/.agent` == False antes de instalar.
6. **Instala** vía la skill canónica `setup-agent-system` (`/agent-setup`):
   `python <MOTOR>/scripts/install_agent_system.py --install --dest <DEST> --prefix <XXX> --yes`
   (corre `--dry-run` primero). Deja `motor_destination_link.json`, `agents.json`
   con `active_profile: host-project`, `PROJECT.md` con `Ticket prefix: <XXX>`.
7. **Rellena `PROJECT.md`** con la realidad del proyecto (stack real, topología
   código/datos, rutas críticas). Es el source-of-truth que `validate` inspecciona
   y lo que leerá un agente nuevo. No dejar placeholders.

**Gate F2:** `motor_destination_link.json` apunta al motor correcto; perfil
`host-project`; `PROJECT.md` con prefijo correcto y sin placeholders.

### FASE 3 — Integración del legacy + validate 0/0

8. **Cierra los WPs legacy como históricos**, NO los re-implementes si su código ya
   vive en `src/`. Un sistema motor viejo (v3.2 u otro) es incompatible con el bus
   nuevo: el cierre es **documental**, en
   `<DEST>/.agent/collaboration/_archive/HISTORIC_<WP-ID>.md`, con evidencia
   ejecutable (comandos + exit codes), no prosa. No intentes `--manager-approve`
   sobre un WP legacy: no es un ticket del bus nuevo.
9. **Si los tests legacy están en rojo por acoplamiento a la máquina** (rutas
   hardcodeadas tipo `/nonexistent`, dependencia de unidades `Z:`), arréglalos bajo
   un ticket `<PREFIX>` formal (no parche suelto), desacoplándolos con
   `tempfile`/`uuid`. Evidencia = salida de la suite verde determinista.
10. **Bootstrap + validate del destino:**
    - `python <MOTOR>/scripts/destination_context.py --bootstrap --project-root <DEST>`
    - `python <MOTOR>/.agent/agent_controller.py --validate --json --project-root <DEST>`

**Gate F3:** `validate --json` → **0 errores** (warnings de prefijo aceptables solo
si justificados); WPs legacy archivados con evidencia; suite del destino verde
corriendo desde la raíz del código real.

### FASE 4 — Git anti-fuga (commit local, sin push)

11. **`git init`** en la raíz externa `DEST` (si no existía). NO `git add` aún.
12. **`.gitignore` en la RAÍZ EXTERNA** (gate anti-fuga crítico). Si el proyecto
    tenía un `.gitignore` en una subcarpeta de código, NO cubre `privada/` cuando
    `privada/` es hermana de la subcarpeta en la raíz externa. Debe ignorar al
    menos: `privada/`, el config real con credenciales, los datos reales,
    `.claude/settings.local.json`, el bundle legacy (`agent_system/`),
    `.agent/runtime/`, `.agent/context/`, venvs, caches, logs.
13. **Verificación seca de exclusión** ANTES de stagear:
    `git -C <DEST> check-ignore -v <config-real> <datos-reales> .claude/settings.local.json`
    **PARAR si `check-ignore` NO matchea cualquier archivo sensible** (fuga
    garantizada).
14. **Commit local** solo si 13 está limpio. **Sin `git remote add`, sin `git push`.**

**Gate F4:** `check-ignore` matchea TODOS los sensibles; `git status` no muestra
ningún sensible como staged; commit local hecho en `main`.

### FASE 5 — Auditoría de publicación (si se va a publicar)

15. **Auditoría dry-run** sobre la historia (ya con HEAD, tras el commit de F4):
    invoca `audit-git-publication` (`/audit-git-publication`) =
    `python <MOTOR>/scripts/classify_publication.py --repo-root <DEST> --out <...>`
    + doble pasada adversarial de `prompts/audit_git_publication.md`. El JSON es
    `[RELATO]`, no evidencia: re-deriva cada `PUBLISH`/`DECIDE` por contenido.
16. **Gate de estado operativo:**
    `python <MOTOR>/scripts/check_destino_publish_ready.py --project-root <DEST> --motor-root <MOTOR>`
17. **Publicación** (acción humana): `git remote add` + `git push`. Repo **privado**
    si hay cualquier duda sobre datos. Si la auditoría detecta un secreto ya
    commiteado en F4, **rehacer el commit** (reset + corregir gitignore/redacción):
    borrarlo del tree no lo saca de la historia local.

**Gate F5 (publicación):** `check-ignore` + scan manual limpios; auditoría sin
secretos en árbol/historia; PII personal redactada; `check_destino_publish_ready`
sin drift. El veredicto humano de la Pasada B prevalece sobre el exit-code del script.

---

## Fricciones conocidas del motor al adecuar (workarounds verificados)

> Estas son limitaciones REALES observadas. Cada una tiene un follow-up o workaround.
> Documentarlas aquí evita que cada adecuación las redescubra a tropezones.

- **`classify_publication.py` y los fixtures de seguridad de tests** → los
  archivos de test de redacción/publicación (p.ej. `tests/test_redact.py`,
  `tests/test_classify_publication.py`) embeben marcadores de secreto FALSOS a
  propósito para ejercitar el scanner. **Resuelto** por la allowlist
  `SECURITY_FIXTURE_PATHS` en `classify_publication.py`: esos paths nombrados se
  eximen tanto en el tree-scan como en el history-scan, sin perder fail-closed
  para cualquier otro path (un blob mixto fixture+no-fixture NO se exime).
  Placeholder seguro en docs: usa `API_KEY=<API_KEY>`, no un valor opaco largo.

- **Mecánica real de `.gitignore` en el tree-scan** (corrige una nota previa
  imprecisa): `_collect_repo_files` usa
  `git ls-files --others --exclude-standard`, así que SÍ respeta los archivos
  *untracked* ignorados (no los escanea). PERO escanea los archivos *tracked*
  aunque estén gitignored (un secreto ya commiteado se detecta aunque luego se
  añada al `.gitignore`). El history-scan recorre blobs de toda la historia.
  **Workaround para tracked-ignored legítimos:** la Pasada B refuta cada flag
  con `git check-ignore` + `git ls-files` confirmando que el archivo no es
  publicable y, si procede, rehaciendo el commit.

- **`run_pytest_safe.py` asume pytest instalado** → falso rojo
  (`No module named pytest`) en destinos que usan `unittest` aunque la suite pase.
  **Workaround:** `uv pip install pytest` solo en el `.venv` del destino (pytest
  corre los tests unittest nativamente), sin tocar `pyproject`/`uv.lock`.
  *(Registrado como follow-up del motor: detectar runner pytest|unittest.)*

- **El cierre canónico de un ticket cuyo checkpoint toca `.agent/collaboration/`**
  (markdowns de orquestación, no código) puede requerir
  `--mark-ready --scope-override "<razón>"` porque el scope-gate los trata como
  cambio fuera de los Files Likely Touched. **Workaround:** usar `--scope-override`
  con razón auditable (artefactos de orquestación, no código productivo).

- **`project_scanner.py` no regenera el project-map del destino** (escanea por
  `cwd`/`__file__`, no por `--project-root`). **Workaround:** usar
  `destination_context.py --bootstrap --project-root <DEST>` para el
  `destination_map.md`; el project-map JSON del destino se corrige a mano si hace
  falta.

- **Múltiples entrypoints/lanzadores legacy** (`.bat`, wrappers Espanso, accesos
  directos) se desincronizan al cambiar el entrypoint. **Barrera:** tras cambiar
  cualquier lanzador, `grep` por el nombre del entrypoint viejo en TODO el repo y
  actualizar todos. En `.bat`, `%~dp0` YA termina en `\`: no añadir `.` ni `/`.

- **Aplanado que mueve el producto a la raíz (rutas hardcodeadas en lanzadores).**
  Cuando un destino se aplana (el producto sube de `publica/repo/` o
  `z_automatizacion/publica/repo/` a la raíz), TODO lanzador con ruta absoluta o
  relativa al subdirectorio viejo se rompe SILENCIOSAMENTE. **Check obligatorio,
  antes y después del aplanado:** `grep -rl "publica/repo\|z_automatizacion"
  --include="*.bat" --include="*.ps1" --include="*.sh" <dest>` y actualizar cada
  ruta a la nueva ubicación (en `.bat` usar `cd /d "%~dp0"` para la raíz, sin
  añadir `.`/`/`). (Verificado: `fiscal.bat` en Contabilidad apuntaba a
  `...\z_automatizacion\publica\repo` y se habría roto al aplanar.) Sin este
  check, el aplanado deja el proyecto sin punto de entrada funcional.

## Contrato de fallo

- Si `check-ignore` no matchea un archivo sensible, **detente**: no se hace
  `git add` hasta resolverlo.
- Si `validate --json` tiene errores, no avances a Git ni a publicación.
- Si el motor deja de estar pristine (`check_motor_pristine.py --check` falla),
  detente y revierte en el motor: el destino no debe escribir en el motor.
- Si la raíz operativa apunta al motor en vez del destino, detente.
- Si un WP legacy "no cierra" por gates del sistema viejo, NO fuerces el bus nuevo:
  ciérralo como histórico documental.

## Referencias

- `skills/setup-agent-system/SKILL.md` — instalación/sync (invocada en F2).
- `skills/secure-existing-project/SKILL.md` — migración de secretos (F1 si aplica).
- `skills/audit-git-publication/SKILL.md` — auditoría de publicación (F5).
- `prompts/orchestrator_destination_bootstrap.md` — arranque de sesión (paso siguiente).
- `prompts/audit_git_publication.md` — protocolo de doble pasada de publicación.
- `scripts/install_agent_system.py`, `destination_context.py`,
  `check_destino_publish_ready.py`, `classify_publication.py`,
  `check_motor_pristine.py` — herramientas invocadas.
