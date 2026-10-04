---
name: "speckit-converge"
description: "Evalúa el código base actual frente al spec, plan y tareas de la funcionalidad, y luego agrega el trabajo pendiente como nuevas tareas en tasks.md para que implement pueda completarlo."
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/converge.md"
user-invocable: true
disable-model-invocation: false
---


## Entrada del usuario

```text
$ARGUMENTS
```

**DEBE** considerar la entrada del usuario antes de continuar (si no está vacía).

## Verificaciones previas a la ejecución

**Verificar hooks de extensión (antes de la convergencia)**:

- Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.before_converge`
- Si el YAML no se puede analizar o no es válido, omite la verificación de hooks silenciosamente y continúa con normalidad
- Filtra los hooks donde `enabled` sea explícitamente `false`. Trata los hooks sin el campo `enabled` como habilitados por defecto.
- Para cada hook restante, **no** intentes interpretar ni evaluar las expresiones `condition` del hook:
  - Si el hook no tiene campo `condition`, o está vacío/null, trata el hook como ejecutable
  - Si el hook define un `condition` no vacío, omite el hook y deja la evaluación de la condición a la implementación de HookExecutor
- Al construir comandos slash a partir de los nombres de comando del hook, reemplaza los puntos (`.`) por guiones (`-`). Por ejemplo, `speckit.git.commit` → `/speckit-git-commit`.
- Para cada hook ejecutable, muestra lo siguiente según su indicador `optional`:
  - **Hook opcional** (`optional: true`):

    ```text
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```

  - **Hook obligatorio** (`optional: false`):

    ```text
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Goal.
    ```
    Después de emitir el bloque anterior, DEBE invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma forma en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo, un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.

- Si no hay hooks registrados o `.specify/extensions.yml` no existe, omite silenciosamente

## Objetivo

Cierra la brecha entre lo que exigen la especificación, el plan y las tareas de una funcionalidad y lo que el código base implementa actualmente. Lee `spec.md`, `plan.md` y `tasks.md` como la **única fuente de intención** (con la constitución como restricciones rectoras), evalúa el estado actual del código, determina qué requisitos, criterios de aceptación, decisiones del plan y tareas existentes están incumplidos, incompletos o solo parcialmente satisfechos, y **agrega cada pieza de trabajo pendiente como una nueva tarea trazable** al final de `tasks.md` para que `/speckit-implement` pueda completarla. Este comando DEBE ejecutarse únicamente después de que `/speckit-implement` se haya ejecutado sobre el `tasks.md` actual, y después de que `/speckit-tasks` haya producido un `tasks.md` completo.

Esto **no** es una herramienta de diff y **no** rastrea cambios. Evalúa el estado presente del código en relación con los artefactos de la funcionalidad — sin git, sin comparación de ramas, sin historial.

## Restricciones de operación

**SOLO AGREGAR, NUNCA REESCRIBIR**: La **única** escritura del comando es agregar una nueva sección `## Phase N: Convergence` a `tasks.md`. NO DEBE:

- modificar `spec.md` o `plan.md` de ninguna manera;
- reescribir, renumerar, reordenar o eliminar ninguna tarea existente (incluidas las tareas de una fase de Convergence anterior);
- modificar, crear o eliminar código de la aplicación — completar las tareas agregadas es tarea de `/speckit-implement`.

Cuando el código base ya satisface todo, el comando DEBE dejar `tasks.md` **sin cambios, byte por byte** (sin encabezado vacío de Convergence) e informar un resultado limpio.

**Autoridad de la constitución**: La constitución del proyecto (`.specify/memory/constitution.md`) es **innegociable**. El código que viola un principio DEBE es el hallazgo de mayor severidad y produce una tarea de remediación correspondiente. Si la constitución es una plantilla sin completar, omite las verificaciones de la constitución de forma controlada en lugar de fallar.

## Pasos de ejecución

### 1. Inicializar el contexto de convergencia

Ejecuta `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` una vez desde la raíz del repositorio y analiza el JSON para obtener FEATURE_DIR y AVAILABLE_DOCS. Deriva las rutas absolutas:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md
- CONSTITUTION = `.specify/memory/constitution.md` (si está presente)
Si falta `spec.md`, `plan.md` o `tasks.md`, DETENTE con un mensaje claro y accionable que nombre el comando prerrequisito a ejecutar (`/speckit-specify` si falta el spec, `/speckit-plan` si falta el plan, `/speckit-tasks` si faltan las tareas). No produzcas una salida parcial.
Para comillas simples en argumentos como "I'm Groot", usa la sintaxis de escape: por ejemplo 'I'\''m Groot' (o comillas dobles si es posible: "I'm Groot").

### 2. Cargar artefactos (divulgación progresiva)

Carga solo el contexto mínimo necesario de cada artefacto:

**Desde spec.md:**

- Requisitos funcionales (FR-###)
- Criterios de éxito (SC-###) — incluye solo los elementos que requieren trabajo construible; excluye las métricas de resultado posteriores al lanzamiento y los KPI de negocio
- Historias de usuario y sus escenarios de aceptación
- Casos límite (si están presentes)

**Desde plan.md:**

- Elecciones de arquitectura/stack y decisiones técnicas
- Referencias del modelo de datos
- Fases y puntos de contacto nombrados (archivos/componentes que el plan indica que se crearán o editarán)
- Restricciones técnicas

**Desde tasks.md:**

- IDs de tareas (para calcular el siguiente ID y el siguiente número de fase)
- Descripciones, agrupación por fases y rutas de archivo referenciadas

**Desde la constitución (si no es una plantilla sin completar):**

- Nombres de principios y declaraciones normativas DEBE/DEBERÍA

### 3. Construir el inventario de intenciones

Crea un modelo interno (no repitas los artefactos en bruto):

- **Inventario de requisitos**: una clave estable por cada escenario de aceptación FR-### / SC-### / historia de usuario (p. ej. `US1/AC2`), más las decisiones del plan y los principios de la constitución que impongan obligaciones construibles.
- **Mapa de alcance del código**: a partir de las rutas de archivo nombradas en `plan.md` y `tasks.md`, más una búsqueda por palabras clave de los conceptos que describe cada requisito, deriva el conjunto de archivos fuente y componentes dentro del alcance de la evaluación. Limita la evaluación a estos — **no** infieras un alcance más allá de lo que definen los artefactos.

### 4. Evaluar el código base y clasificar los hallazgos

Para cada elemento del inventario de intenciones, inspecciona el código actual dentro del alcance y produce un `Finding` solo cuando exista una brecha. Clasifica cada hallazgo por **tipo de brecha**:

- **`missing`**: el trabajo requerido está completamente ausente del código.
- **`partial`**: el trabajo existe pero aún no satisface completamente el requisito / criterio de aceptación / decisión del plan.
- **`contradicts`**: el código hace algo que entra en conflicto con la intención declarada o con un principio DEBE de la constitución.
- **`unrequested`**: el código contiene trabajo no solicitado por el spec, el plan o las tareas (se muestra para conocimiento — converge **no** elimina código, solo agrega una tarea para revisarlo/justificarlo o eliminarlo).

Cada `Finding` registra: un id estable, el `source-ref` al que se remonta, el `gap-type`, una severidad, y una breve descripción legible por humanos con la evidencia (el archivo/área observada).

**Casos límite:**

- **Poco o ningún código todavía**: trata todo el alcance especificado como trabajo pendiente `missing` en lugar de fallar.
- **No queda nada**: produce cero hallazgos y sigue la rama converged en el Paso 7.

### 5. Asignar severidad

- **CRITICAL**: viola un principio DEBE de la constitución, o una brecha `missing`/`contradicts` que bloquea la funcionalidad base de una historia de usuario P1.
- **HIGH**: una brecha `missing` o `partial` en un requisito funcional o criterio de aceptación principal.
- **MEDIUM**: una brecha `partial` en un requisito secundario, o una adición `unrequested` con justificación poco clara.
- **LOW**: brechas parciales menores, pulido, o adiciones `unrequested` de bajo riesgo.

### 6. Presentar el resumen de hallazgos en la sesión

Antes de agregar nada, muestra un resumen compacto y clasificado por severidad (todavía sin escribir en el archivo):

## Hallazgos de convergencia

| ID | Tipo de brecha | Severidad | Origen | Evidencia | Trabajo pendiente |
|----|----------|----------|--------|----------|----------------|
| F1 | missing  | HIGH     | FR-008 | Ejemplo: no se detectó protección de solo-agregar en path/to/module.py al escribir tasks.md | Agregar la aplicación de la regla de solo-agregar |

**Métricas de resumen:**

- Requisitos / criterios de aceptación verificados
- Decisiones del plan verificadas
- Principios de la constitución verificados (o "omitido — plantilla")
- Hallazgos por tipo de brecha (missing / partial / contradicts / unrequested)
- Hallazgos por severidad

### 7. Agregar tareas de convergencia (o informar que ya convergió)

**Si hay uno o más hallazgos accionables** (resultado `tasks_appended`):

Agrega al **final** de `tasks.md`, según el contrato de anexado:

1. Escanea todos los IDs de tareas existentes; sea `M` el máximo. Determina el siguiente número de fase `N` (la fase existente más alta + 1).
2. Escribe un único encabezado de sección nuevo `## Phase N: Convergence`.
3. Emite un elemento de checklist por cada hallazgo accionable, ordenando primero CRITICAL/HIGH, asignando IDs con ceros a la izquierda `T{M+1:03d}, T{M+2:03d}, …`:

   ```markdown
   - [ ] T042 <imperative description> per <source-ref> (<gap-type>)
   ```

   `<source-ref>` remonta la tarea a su origen: p. ej. `FR-003`, `SC-002`,
   `US1/AC2`, `plan: storage decision`, `Constitution II`.

   `<gap-type>` es uno de `missing`, `partial`, `contradicts`, `unrequested`.

   Las tareas de violación de la constitución DEBEN emitirse primero y describirse como
   `CRITICAL`.
4. Nunca reutilices ni renumeres los IDs existentes. Si ya existe una fase de Convergence previa, agrega una nueva, numerada por separado, debajo de ella — no toques la anterior.

**Si no hay hallazgos accionables** (resultado `converged`):

- **No** modifiques `tasks.md` en absoluto — sin encabezado de fase vacío.
- Informa: **"✅ Converged — la implementación satisface el spec, el plan y las tareas."**
- Incluye los recuentos resumidos de lo que se verificó.

### 8. Proporcionar próximas acciones (traspaso)

- En `tasks_appended`: indica cuántas tareas se agregaron y bajo qué fase, y recomienda
  ejecutar `/speckit-implement` para completarlas; señala que una ejecución de convergencia
  posterior encontrará menos elementos pendientes o ninguno.
- En `converged`: recomienda continuar con la revisión / abrir un PR. No se necesita otra
  pasada de implement para el alcance especificado de esta funcionalidad.

### 9. Verificar hooks de extensión

Después de producir el resultado, verifica si `.specify/extensions.yml` existe en la raíz del proyecto.

- Si existe, léelo y busca entradas bajo la clave `hooks.after_converge`
- Si el YAML no se puede analizar o no es válido, omite la verificación de hooks silenciosamente y continúa con normalidad
- Filtra los hooks donde `enabled` sea explícitamente `false`. Trata los hooks sin el campo `enabled` como habilitados por defecto.
- Para cada hook restante, **no** intentes interpretar ni evaluar las expresiones `condition` del hook:
  - Si el hook no tiene campo `condition`, o está vacío/null, trata el hook como ejecutable
  - Si el hook define un `condition` no vacío, omite el hook y deja la evaluación de la condición a la implementación de HookExecutor
- Informa el resultado de la convergencia (`converged` o `tasks_appended`) en la sesión antes de listar
  cualquier hook, para que los usuarios puedan decidir si ejecutan comandos de seguimiento opcionales.
- Al construir comandos slash a partir de los nombres de comando del hook, reemplaza los puntos (`.`) por guiones (`-`). Por ejemplo, `speckit.git.commit` → `/speckit-git-commit`.
- Para cada hook ejecutable, muestra lo siguiente según su indicador `optional`:
  - **Hook opcional** (`optional: true`):

    ```text
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```

  - **Hook obligatorio** (`optional: false`):

    ```text
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    Después de emitir el bloque anterior, DEBE invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma forma en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo, un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.

- Si no hay hooks registrados o `.specify/extensions.yml` no existe, omite silenciosamente
