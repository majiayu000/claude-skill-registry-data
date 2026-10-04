---
name: "speckit-analyze"
description: "Realiza un análisis de consistencia y calidad no destructivo entre archivos (spec.md, plan.md y tasks.md) después de la generación de tareas."
argument-hint: "Áreas de enfoque opcionales para el análisis"
compatibility: "Requiere la estructura de proyecto de spec-kit con el directorio .specify/"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/analyze.md"
user-invocable: true
disable-model-invocation: false
---


## Entrada del usuario

```text
$ARGUMENTS
```

DEBES considerar la entrada del usuario antes de continuar (si no está vacía).

## Verificaciones previas a la ejecución

**Verificar hooks de extensión (antes del análisis)**:
- Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.before_analyze`
- Si el YAML no se puede analizar o es inválido, omite la verificación de hooks silenciosamente y continúa normalmente
- Filtra los hooks donde `enabled` sea explícitamente `false`. Trata los hooks sin un campo `enabled` como habilitados por defecto.
- Para cada hook restante, **no** intentes interpretar ni evaluar las expresiones `condition` del hook:
  - Si el hook no tiene un campo `condition`, o está vacío/nulo, trata el hook como ejecutable
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

    Wait for the result of the hook command before proceeding to the Goal.
    ```
    Después de emitir el bloque anterior, DEBES invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma manera en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo, un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.
- Si no hay hooks registrados o `.specify/extensions.yml` no existe, omite silenciosamente

## Objetivo

Identifica inconsistencias, duplicaciones, ambigüedades y elementos subespecificados en los tres artefactos principales (`spec.md`, `plan.md`, `tasks.md`) antes de la implementación. Este comando DEBE ejecutarse solo después de que `/speckit-tasks` haya producido con éxito un `tasks.md` completo.

## Restricciones de operación

**ESTRICTAMENTE DE SOLO LECTURA**: **No** modifiques ningún archivo. Muestra un informe de análisis estructurado. Ofrece un plan de remediación opcional (el usuario debe aprobarlo explícitamente antes de que se invoque manualmente cualquier comando de edición posterior).

**Autoridad de la constitución**: La constitución del proyecto (`.specify/memory/constitution.md`) es **innegociable** dentro del alcance de este análisis. Los conflictos con la constitución son automáticamente CRÍTICOS y requieren ajustar el spec, el plan o las tareas, no diluir, reinterpretar o ignorar silenciosamente el principio. Si un principio en sí necesita cambiar, eso debe ocurrir en una actualización explícita y separada de la constitución, fuera de `/speckit-analyze`.

## Pasos de ejecución

### 1. Inicializar el contexto de análisis

Ejecuta `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` una vez desde la raíz del repositorio y analiza el JSON para obtener FEATURE_DIR y AVAILABLE_DOCS. Deriva las rutas absolutas:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

Aborta con un mensaje de error si falta algún archivo requerido (indica al usuario que ejecute el comando de prerrequisito faltante).
Para comillas simples en argumentos como "I'm Groot", usa la sintaxis de escape: por ejemplo 'I'\''m Groot' (o comillas dobles si es posible: "I'm Groot").

### 2. Cargar artefactos (divulgación progresiva)

Carga solo el contexto mínimo necesario de cada artefacto:

**Desde spec.md:**

- Resumen/Contexto
- Requisitos funcionales
- Criterios de éxito (resultados medibles — por ejemplo: rendimiento, seguridad, disponibilidad, éxito del usuario, impacto en el negocio)
- Historias de usuario
- Casos límite (si están presentes)

**Desde plan.md:**

- Decisiones de arquitectura/stack
- Referencias al modelo de datos
- Fases
- Restricciones técnicas

**Desde tasks.md:**

- IDs de tareas
- Descripciones
- Agrupación por fases
- Marcadores de paralelismo [P]
- Rutas de archivo referenciadas

**Desde la constitución:**

- Carga `.specify/memory/constitution.md` para la validación de principios

### 3. Construir modelos semánticos

Crea representaciones internas (no incluyas los artefactos en bruto en la salida):

- **Inventario de requisitos**: Para cada Requisito Funcional (FR-###) y Criterio de Éxito (SC-###), registra una clave estable. Usa el identificador explícito FR-/SC- como clave principal cuando esté presente, y opcionalmente deriva también un slug de frase imperativa para facilitar la lectura (por ejemplo, "User can upload file" → `user-can-upload-file`). Incluye solo los elementos de Criterios de Éxito que requieran trabajo construible (por ejemplo, infraestructura de pruebas de carga, herramientas de auditoría de seguridad), y excluye las métricas de resultado posteriores al lanzamiento y los KPI de negocio (por ejemplo, "Reduce support tickets by 50%").
- **Inventario de historias de usuario/acciones**: Acciones discretas del usuario con criterios de aceptación
- **Mapeo de cobertura de tareas**: Asigna cada tarea a uno o más requisitos o historias (inferencia por palabra clave / patrones de referencia explícitos como IDs o frases clave)
- **Conjunto de reglas de la constitución**: Extrae los nombres de los principios y las declaraciones normativas DEBE/DEBERÍA

### 4. Pasadas de detección (análisis eficiente en tokens)

Concéntrate en hallazgos de alta relevancia. Limita a 50 hallazgos en total; agrega el resto en un resumen de desbordamiento.

#### A. Detección de duplicación

- Identifica requisitos casi duplicados
- Marca la redacción de menor calidad para su consolidación

#### B. Detección de ambigüedad

- Marca adjetivos vagos (rápido, escalable, seguro, intuitivo, robusto) que carezcan de criterios medibles
- Marca los marcadores de posición sin resolver (TODO, TKTK, ???, `<placeholder>`, etc.)

#### C. Subespecificación

- Requisitos con verbos pero sin objeto o resultado medible
- Historias de usuario sin alineación con los criterios de aceptación
- Tareas que hacen referencia a archivos o componentes no definidos en el spec/plan

#### D. Alineación con la constitución

- Cualquier requisito o elemento del plan que entre en conflicto con un principio DEBE
- Secciones obligatorias o puertas de calidad faltantes de la constitución

#### E. Brechas de cobertura

- Requisitos sin tareas asociadas
- Tareas sin requisito/historia asignada
- Criterios de éxito que requieren trabajo construible (rendimiento, seguridad, disponibilidad) no reflejados en las tareas

#### F. Inconsistencia

- Deriva de terminología (el mismo concepto nombrado de manera diferente entre archivos)
- Entidades de datos referenciadas en el plan pero ausentes en el spec (o viceversa)
- Contradicciones en el orden de las tareas (por ejemplo, tareas de integración antes de tareas de configuración base sin nota de dependencia)
- Requisitos en conflicto (por ejemplo, uno requiere Next.js mientras otro especifica Vue)

### 5. Asignación de severidad

Usa esta heurística para priorizar los hallazgos:

- **CRÍTICA**: Viola un DEBE de la constitución, falta un artefacto principal del spec, o un requisito sin cobertura que bloquea la funcionalidad base
- **ALTA**: Requisito duplicado o en conflicto, atributo de seguridad/rendimiento ambiguo, criterio de aceptación no verificable
- **MEDIA**: Deriva de terminología, falta de cobertura de tareas no funcionales, caso límite subespecificado
- **BAJA**: Mejoras de estilo/redacción, redundancia menor que no afecta el orden de ejecución

### 6. Producir un informe de análisis compacto

Muestra un informe en Markdown (sin escribir archivos) con la siguiente estructura:

## Informe de análisis de especificación

| ID | Categoría | Severidad | Ubicación(es) | Resumen | Recomendación |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplicación | ALTA | spec.md:L120-134 | Dos requisitos similares ... | Combinar la redacción; conservar la versión más clara |

(Agrega una fila por cada hallazgo; genera IDs estables con el prefijo de la inicial de la categoría.)

**Tabla resumen de cobertura:**

| Clave de requisito | ¿Tiene tarea? | IDs de tarea | Notas |
|-----------------|-----------|----------|-------|

**Problemas de alineación con la constitución:** (si los hay)

**Tareas sin asignar:** (si las hay)

**Métricas:**

- Total de requisitos
- Total de tareas
- % de cobertura (requisitos con >=1 tarea)
- Cantidad de ambigüedades
- Cantidad de duplicaciones
- Cantidad de problemas críticos

### 7. Proporcionar próximas acciones

Al final del informe, muestra un bloque conciso de próximas acciones:

- Si existen problemas CRÍTICOS: recomienda resolverlos antes de `/speckit-implement`
- Si solo hay BAJA/MEDIA: el usuario puede continuar, pero proporciona sugerencias de mejora
- Proporciona sugerencias de comandos explícitas: por ejemplo, "Run /speckit-specify with refinement", "Run /speckit-plan to adjust architecture", "Manually edit tasks.md to add coverage for 'performance-metrics'"

### 8. Ofrecer remediación

Pregunta al usuario: "¿Te gustaría que sugiera ediciones de remediación concretas para los N problemas principales?" (NO las apliques automáticamente.)

### 9. Verificar hooks de extensión

Después de reportar, verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.after_analyze`
- Si el YAML no se puede analizar o es inválido, omite la verificación de hooks silenciosamente y continúa normalmente
- Filtra los hooks donde `enabled` sea explícitamente `false`. Trata los hooks sin un campo `enabled` como habilitados por defecto.
- Para cada hook restante, **no** intentes interpretar ni evaluar las expresiones `condition` del hook:
  - Si el hook no tiene un campo `condition`, o está vacío/nulo, trata el hook como ejecutable
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

## Principios de operación

### Eficiencia de contexto

- **Tokens mínimos de alta señal**: Concéntrate en hallazgos accionables, no en documentación exhaustiva
- **Divulgación progresiva**: Carga los artefactos de forma incremental; no vuelques todo el contenido en el análisis
- **Salida eficiente en tokens**: Limita la tabla de hallazgos a 50 filas; resume el excedente
- **Resultados deterministas**: Volver a ejecutar sin cambios debe producir IDs y conteos consistentes

### Directrices de análisis

- **NUNCA modifiques archivos** (este es un análisis de solo lectura)
- **NUNCA inventes secciones faltantes** (si están ausentes, repórtalo con precisión)
- **Prioriza las violaciones de la constitución** (estas son siempre CRÍTICAS)
- **Usa ejemplos en lugar de reglas exhaustivas** (cita casos específicos, no patrones genéricos)
- **Reporta cero problemas con elegancia** (emite un informe de éxito con estadísticas de cobertura)

## Contexto

$ARGUMENTS
