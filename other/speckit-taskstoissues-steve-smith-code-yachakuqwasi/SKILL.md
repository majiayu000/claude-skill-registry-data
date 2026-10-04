---
name: "speckit-taskstoissues"
description: "Convierte las tareas existentes en issues de GitHub accionables y ordenados por dependencias para la funcionalidad, basado en los artefactos de diseño disponibles."
argument-hint: "Filtro o etiqueta opcional para los issues de GitHub"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/taskstoissues.md"
user-invocable: true
disable-model-invocation: false
---


## Entrada del usuario

```text
$ARGUMENTS
```

**DEBES** considerar la entrada del usuario antes de continuar (si no está vacía).

## Verificaciones previas a la ejecución

**Verifica los hooks de extensión (antes de convertir tareas en issues)**:
- Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.before_taskstoissues`
- Si el YAML no se puede analizar o no es válido, omite la verificación de hooks silenciosamente y continúa normalmente
- Filtra los hooks donde `enabled` sea explícitamente `false`. Trata los hooks sin un campo `enabled` como habilitados por defecto.
- Para cada hook restante, **no** intentes interpretar ni evaluar las expresiones `condition` del hook:
  - Si el hook no tiene campo `condition`, o es nulo/vacío, trata el hook como ejecutable
  - Si el hook define un `condition` no vacío, omite el hook y deja la evaluación de la condición a la implementación de HookExecutor
- Al construir comandos slash a partir de los nombres de comando del hook, reemplaza los puntos (`.`) por guiones (`-`). Por ejemplo, `speckit.git.commit` → `/speckit-git-commit`.
- Para cada hook ejecutable, muestra lo siguiente según su indicador `optional`:
  - **Hook opcional** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Hook obligatorio** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Outline.
    ```
    Después de emitir el bloque anterior, DEBES invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma manera en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo, un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.
- Si no hay hooks registrados o `.specify/extensions.yml` no existe, omite silenciosamente

## Esquema

1. Ejecuta `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` desde la raíz del repositorio y analiza FEATURE_DIR y la lista AVAILABLE_DOCS. Todas las rutas deben ser absolutas. Para comillas simples en argumentos como "I'm Groot", usa la sintaxis de escape: por ejemplo 'I'\''m Groot' (o comillas dobles si es posible: "I'm Groot").
1. **SI EXISTE**: Carga `.specify/memory/constitution.md` para los principios del proyecto y las restricciones de gobernanza.
1. Desde el script ejecutado, extrae la ruta a **tasks**.
1. Obtén el remoto de Git ejecutando:

```bash
git config --get remote.origin.url
```

> [!CAUTION]
> SOLO CONTINÚA CON LOS SIGUIENTES PASOS SI EL REMOTO ES UNA URL DE GITHUB

1. **Obtén los issues existentes para deduplicar**: Antes de crear nada, construye el conjunto de IDs de tareas que vas a procesar a partir de `tasks.md` (cada uno es una `T` seguida de tres dígitos, p. ej. `T001`). Luego usa la herramienta `list_issues` del servidor MCP de GitHub para buscar issues que ya cubran esos IDs. No pases un valor de `state`, ya que omitirlo hace que la herramienta devuelva tanto issues abiertos como cerrados. Solicita `perPage: 100` para reducir el número de llamadas, y como la herramienta usa paginación basada en cursores, solicita las páginas con el parámetro `after` (usando el `endCursor` de la respuesta anterior). Para cada título de issue, compáralo contra el patrón de ID de tarea `\bT\d{3}\b` (con límites de palabra para que tokens como `ST001` o `T0010` no se emparejen por error; esto también reconoce títulos escritos como `T001 ...`, `T001: ...` o `[T001] ...`) y, cuando coincida con uno de tus IDs de tarea, marca ese ID como que ya tiene un issue. Deja de paginar tan pronto como todos los IDs de tarea hayan sido emparejados, o cuando ya no haya más páginas, para no seguir obteniendo todo el historial de issues del repositorio una vez que todos los IDs de tarea estén contabilizados. Esto acota el número de llamadas en repositorios con historiales de issues grandes y sigue evitando duplicados cuando el comando se vuelve a ejecutar después de regenerar `tasks.md` o de reinvocar la skill.
1. Para cada tarea de la lista, usa el servidor MCP de GitHub para crear un nuevo issue en el repositorio representativo del remoto de Git. Las líneas de tarea en `tasks.md` comienzan con un checkbox de markdown, así que primero elimina el `- [ ]` inicial (y cualquier marcador `[P]` / `[US#]`) para recuperar el ID de la tarea y su descripción. Crea el issue con un único título canónico de la forma `T001: <descripción>`, con el ID escrito una sola vez seguido de la descripción de la tarea (por ejemplo, la línea `- [ ] T001 Create project structure` se convierte en el título `T001: Create project structure`).
   - **Omite** cualquier tarea cuyo ID ya esté presente en el conjunto de issues existentes del paso anterior, e infórmalo (por ejemplo, `T001 already has an issue, skipping`).
   - Crea issues únicamente para las tareas que aún no tengan un issue correspondiente.

> [!CAUTION]
> BAJO NINGUNA CIRCUNSTANCIA CREES ISSUES EN REPOSITORIOS QUE NO COINCIDAN CON LA URL DEL REMOTO

## Verificaciones posteriores a la ejecución

**Verifica los hooks de extensión (después de convertir tareas en issues)**:
Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.after_taskstoissues`
- Si el YAML no se puede analizar o no es válido, omite la verificación de hooks silenciosamente y continúa normalmente
- Filtra los hooks donde `enabled` sea explícitamente `false`. Trata los hooks sin un campo `enabled` como habilitados por defecto.
- Para cada hook restante, **no** intentes interpretar ni evaluar las expresiones `condition` del hook:
  - Si el hook no tiene campo `condition`, o es nulo/vacío, trata el hook como ejecutable
  - Si el hook define un `condition` no vacío, omite el hook y deja la evaluación de la condición a la implementación de HookExecutor
- Al construir comandos slash a partir de los nombres de comando del hook, reemplaza los puntos (`.`) por guiones (`-`). Por ejemplo, `speckit.git.commit` → `/speckit-git-commit`.
- Para cada hook ejecutable, muestra lo siguiente según su indicador `optional`:
  - **Hook opcional** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Hook obligatorio** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    Después de emitir el bloque anterior, DEBES invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma manera en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo, un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.
- Si no hay hooks registrados o `.specify/extensions.yml` no existe, omite silenciosamente
