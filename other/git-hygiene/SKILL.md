---
name: git-hygiene
description: Use when committing, pushing, creating or deleting branches or tags, merging, rewriting history, or when asked to "add everything" or push to main in this repository.
---

# Git en este repositorio (público)

## Reglas

| Regla | Caso real |
|---|---|
| Ramas nuevas desde `main` (`git checkout -b feature/<x> main`). A `main` solo llega una fusión que Cristian aprueba. | Fusión de la Sesión A, 01-10-2026. |
| Nunca hagas `git add .`, `-A` ni de una carpeta entera (`docs`). Añade rutas explícitas y revisa `git diff --cached --stat`. | En `ff30092` entraron 512 capturas en bruto (~300 MB). |
| El repositorio es **público**: no puede entrar ninguna clave de Anthropic. El hook `.githooks/pre-commit` lo bloquea (actívalo una vez por clon: `git config core.hooksPath .githooks`) y `SecretScanTests` lo comprueba. `anthropic_api_key.txt` está ignorado. | Dos claves llegaron a `main` en las escenas del primer commit. Hubo que revocarlas. |
| No van al repositorio `Builds/`, `Logs/`, `.superpowers/`, `docs/screenshots/*/anim/`, `.claude/scheduled_tasks.lock` ni ningún archivo de más de 5 MB. De `.claude/`, solo `skills/`. Si `git status` muestra algo de eso como nuevo, falta en `.gitignore`: añádelo, no lo subas. | `.gitignore` solo ignoraba `anim/` del 30-09, y 200 capturas del 01-10 aparecían como nuevas. |
| Nada de servicios o ajustes que nadie ha pedido. | `git checkout -- ProjectSettings/UnityConnectSettings.asset`: el editor activó Unity Connect solo. |
| Nunca reescribas historia remota sin permiso. Si se aprueba: primero etiquetas de backup subidas a origin, y luego `--force-with-lease=<rama>:<hash esperado>`. | Limpieza de `ff30092` (01-10-2026). |
| Commit y push al final de cada bloque. Antes de cerrar, ejecuta las suites. | |
| No borres ramas ni etiquetas sin confirmación. `git branch -d` (nunca `-D`) y solo tras comprobar `merge-base --is-ancestor` con `origin/main`. | `feature/dia3` y las etiquetas `backup/*` se guardan hasta ~08-10-2026. |

## Si piden "añade todo y súbelo a main"

1. No a `main`: a una rama nueva desde `main`.
2. Con `git status`, separa lo que va de lo que no (capturas en bruto, Logs, ajustes del editor).
3. `git add <rutas>` y `git diff --cached --stat`.
4. Commit: el hook busca claves.
5. `git push origin <rama>`. La fusión a `main` se propone; no se hace sin aprobación.
