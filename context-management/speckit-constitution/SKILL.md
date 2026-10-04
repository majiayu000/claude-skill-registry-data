---
name: "speckit-constitution"
description: "Crea o actualiza la constitución del proyecto a partir de entradas de principios interactivas o proporcionadas, asegurando que todas las plantillas dependientes se mantengan sincronizadas."
argument-hint: "Principios o valores para la constitución del proyecto"
compatibility: "Requiere la estructura de proyecto de spec-kit con el directorio .specify/"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/constitution.md"
user-invocable: true
disable-model-invocation: false
---


## Entrada del usuario

```text
$ARGUMENTS
```

DEBES considerar la entrada del usuario antes de continuar (si no está vacía).

## Verificaciones previas a la ejecución

**Verificar hooks de extensión (antes de la actualización de la constitución)**:
- Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.before_constitution`
- Si el YAML no se puede parsear o no es válido, omite la verificación de hooks silenciosamente y continúa normalmente
- Filtra los hooks donde `enabled` sea explícitamente `false`. Trata los hooks sin un campo `enabled` como habilitados por defecto.
- Para cada hook restante, NO intentes interpretar ni evaluar las expresiones `condition` del hook:
  - Si el hook no tiene campo `condition`, o está vacío/nulo, trata el hook como ejecutable
  - Si el hook define un `condition` no vacío, omite el hook y deja la evaluación de la condición a la implementación de HookExecutor
- Al construir comandos slash a partir de los nombres de comando del hook, reemplaza los puntos (`.`) por guiones (`-`). Por ejemplo, `speckit.git.commit` → `/speckit-git-commit`.
- Para cada hook ejecutable, produce lo siguiente según su bandera `optional`:
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
    Después de emitir el bloque anterior DEBES invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma forma en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.
- Si no hay hooks registrados o `.specify/extensions.yml` no existe, omite silenciosamente

## Esquema

Estás actualizando la constitución del proyecto en `.specify/memory/constitution.md`. Este archivo es una PLANTILLA que contiene tokens de marcador de posición entre corchetes (por ejemplo, `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Tu trabajo es (a) recopilar/derivar valores concretos, (b) completar la plantilla con precisión, y (c) propagar cualquier enmienda a los artefactos dependientes.

**Nota**: Si `.specify/memory/constitution.md` aún no existe, debería haberse inicializado a partir de `.specify/templates/constitution-template.md` durante la configuración del proyecto. Si falta, copia primero la plantilla.

Sigue este flujo de ejecución:

1. Carga la constitución existente en `.specify/memory/constitution.md`.
   - Identifica cada token de marcador de posición con la forma `[IDENTIFICADOR_EN_MAYUSCULAS]`.
   **IMPORTANTE**: El usuario podría requerir menos o más principios que los usados en la plantilla. Si se especifica un número, respétalo - sigue la plantilla general. Actualizarás el documento en consecuencia.

2. Recopila/deriva valores para los marcadores de posición:
   - Si la entrada del usuario (conversación) proporciona un valor, úsalo.
   - En caso contrario, infiérelo del contexto existente del repositorio (README, documentación, versiones previas de la constitución si están incrustadas).
   - Para las fechas de gobernanza: `RATIFICATION_DATE` es la fecha de adopción original (si se desconoce, pregunta o marca TODO), `LAST_AMENDED_DATE` es la fecha de hoy si se realizan cambios, en caso contrario mantén la anterior.
   - `CONSTITUTION_VERSION` debe incrementarse según las reglas de versionado semántico:
     - MAYOR (MAJOR): Eliminaciones o redefiniciones de gobernanza/principios incompatibles con versiones anteriores.
     - MENOR (MINOR): Nuevo principio/sección agregado o guía materialmente ampliada.
     - PARCHE (PATCH): Aclaraciones, redacción, corrección de errores tipográficos, refinamientos no semánticos.
   - Si el tipo de incremento de versión es ambiguo, propón un razonamiento antes de finalizar.

3. Redacta el contenido actualizado de la constitución:
   - Reemplaza cada marcador de posición con texto concreto (no deben quedar tokens entre corchetes excepto los espacios de plantilla intencionalmente retenidos que el proyecto haya decidido no definir todavía—justifica explícitamente cualquiera que quede).
   - Preserva la jerarquía de encabezados y los comentarios pueden eliminarse una vez reemplazados, a menos que sigan aportando una guía aclaratoria.
   - Asegúrate de que cada sección de Principio tenga: una línea de nombre concisa, un párrafo (o lista de viñetas) que capture las reglas no negociables, una justificación explícita si no es obvia.
   - Asegúrate de que la sección de Gobernanza liste el procedimiento de enmienda, la política de versionado y las expectativas de revisión de cumplimiento.

4. Lista de verificación de propagación de consistencia (convierte la lista de verificación previa en validaciones activas):
   - Lee `.specify/templates/plan-template.md` y asegúrate de que cualquier "Constitution Check" o reglas se alineen con los principios actualizados.
   - Lee `.specify/templates/spec-template.md` para la alineación de alcance/requisitos—actualízalo si la constitución agrega/elimina secciones o restricciones obligatorias.
   - Lee `.specify/templates/tasks-template.md` y asegúrate de que la categorización de tareas refleje los tipos de tareas nuevos o eliminados impulsados por principios (por ejemplo, observabilidad, versionado, disciplina de pruebas).
   - Lee cada archivo de comando en `.specify/templates/commands/*.md` (incluido este) para verificar que no queden referencias obsoletas (nombres específicos de agente como CLAUDE únicamente) cuando se requiera una guía genérica.
   - Lee cualquier documento de guía en tiempo de ejecución (por ejemplo, `README.md`, `docs/quickstart.md`, o archivos de guía específicos de agente si están presentes). Actualiza las referencias a los principios modificados.

5. Produce un Reporte de Impacto de Sincronización (antepuesto como un comentario HTML al principio del archivo de constitución después de la actualización):
   - Cambio de versión: anterior → nueva
   - Lista de principios modificados (título anterior → título nuevo si se renombró)
   - Secciones agregadas
   - Secciones eliminadas
   - Plantillas que requieren actualización (✅ actualizada / ⚠ pendiente) con rutas de archivo
   - TODOs de seguimiento si algún marcador de posición fue diferido intencionalmente.

6. Validación antes de la salida final:
   - No quedan tokens entre corchetes sin explicar.
   - La línea de versión coincide con el reporte.
   - Fechas en formato ISO AAAA-MM-DD.
   - Los principios son declarativos, verificables y libres de lenguaje vago ("debería" → reemplazar con DEBE/DEBERÍA y su justificación cuando corresponda).

7. Escribe la constitución completada de vuelta en `.specify/memory/constitution.md` (sobrescribir).

8. Muestra un resumen final al usuario con:
   - Nueva versión y justificación del incremento.
   - Cualquier archivo marcado para seguimiento manual.
   - Mensaje de commit sugerido (por ejemplo, `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Requisitos de formato y estilo:

- Usa los encabezados Markdown exactamente como en la plantilla (no degrades/promuevas niveles).
- Ajusta las líneas de justificación largas para mantener la legibilidad (idealmente <100 caracteres) pero no lo fuerces con saltos incómodos.
- Mantén una sola línea en blanco entre secciones.
- Evita espacios en blanco al final de línea.

Si el usuario proporciona actualizaciones parciales (por ejemplo, solo la revisión de un principio), aun así realiza los pasos de validación y decisión de versión.

Si falta información crítica (por ejemplo, la fecha de ratificación es realmente desconocida), inserta `TODO(<FIELD_NAME>): explanation` e inclúyela en el Reporte de Impacto de Sincronización bajo los elementos diferidos.

No crees una nueva plantilla; opera siempre sobre el archivo existente `.specify/memory/constitution.md`.

## Verificaciones posteriores a la ejecución

**Verificar hooks de extensión (después de la actualización de la constitución)**:
Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.after_constitution`
- Si el YAML no se puede parsear o no es válido, omite la verificación de hooks silenciosamente y continúa normalmente
- Filtra los hooks donde `enabled` sea explícitamente `false`. Trata los hooks sin un campo `enabled` como habilitados por defecto.
- Para cada hook restante, NO intentes interpretar ni evaluar las expresiones `condition` del hook:
  - Si el hook no tiene campo `condition`, o está vacío/nulo, trata el hook como ejecutable
  - Si el hook define un `condition` no vacío, omite el hook y deja la evaluación de la condición a la implementación de HookExecutor
- Al construir comandos slash a partir de los nombres de comando del hook, reemplaza los puntos (`.`) por guiones (`-`). Por ejemplo, `speckit.git.commit` → `/speckit-git-commit`.
- Para cada hook ejecutable, produce lo siguiente según su bandera `optional`:
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
    Después de emitir el bloque anterior DEBES invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma forma en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.
- Si no hay hooks registrados o `.specify/extensions.yml` no existe, omite silenciosamente
