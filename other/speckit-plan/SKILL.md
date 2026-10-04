---
name: "speckit-plan"
description: "Ejecuta el flujo de trabajo de planificación de implementación usando la plantilla de plan para generar artefactos de diseño."
argument-hint: "Orientación opcional para la fase de planificación"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/plan.md"
user-invocable: true
disable-model-invocation: false
---


## Entrada del usuario

```text
$ARGUMENTS
```

**DEBES** considerar la entrada del usuario antes de continuar (si no está vacía).

## Verificaciones previas a la ejecución

**Verifica los hooks de extensión (antes de planificar)**:
- Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.before_plan`
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
    Después de emitir el bloque anterior, **DEBES** invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma manera en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo, un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.
- Si no hay hooks registrados o `.specify/extensions.yml` no existe, omite silenciosamente

## Esquema

1. **Configuración**: Ejecuta `.specify/scripts/bash/setup-plan.sh --json` desde la raíz del repositorio y analiza el JSON para obtener FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. Para comillas simples en argumentos como "I'm Groot", usa la sintaxis de escape: por ejemplo 'I'\''m Groot' (o comillas dobles si es posible: "I'm Groot").

2. **Carga el contexto**: Lee FEATURE_SPEC y `.specify/memory/constitution.md`. Carga la plantilla de IMPL_PLAN (ya copiada).

3. **Ejecuta el flujo de trabajo del plan**: Sigue la estructura de la plantilla IMPL_PLAN para:
   - Completar el Contexto Técnico (marca los desconocidos como "NEEDS CLARIFICATION")
   - Completar la sección de Verificación de la Constitución a partir de la constitución
   - Evaluar las puertas de control (ERROR si hay violaciones no justificadas)
   - Fase 0: Generar research.md (resolver todos los NEEDS CLARIFICATION)
   - Fase 1: Generar data-model.md, contracts/, quickstart.md
   - Fase 1: Actualizar el contexto del agente ejecutando el script del agente
   - Reevaluar la Verificación de la Constitución después del diseño

## Hooks obligatorios posteriores a la ejecución

**DEBES completar esta sección antes de informar la finalización al usuario.**

Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si no existe, o no hay hooks registrados bajo `hooks.after_plan`, salta al Informe de finalización.
- Si existe, léelo y busca entradas bajo la clave `hooks.after_plan`.
- Si el YAML no se puede analizar o no es válido, omite la verificación de hooks silenciosamente y continúa al Informe de finalización.
- Filtra los hooks donde `enabled` sea explícitamente `false`. Trata los hooks sin un campo `enabled` como habilitados por defecto.
- Para cada hook restante, **no** intentes interpretar ni evaluar las expresiones `condition` del hook:
  - Si el hook no tiene campo `condition`, o es nulo/vacío, trata el hook como ejecutable
  - Si el hook define un `condition` no vacío, omite el hook y deja la evaluación de la condición a la implementación de HookExecutor
- Al construir comandos slash a partir de los nombres de comando del hook, reemplaza los puntos (`.`) por guiones (`-`). Por ejemplo, `speckit.git.commit` → `/speckit-git-commit`.
- Para cada hook ejecutable, muestra lo siguiente según su indicador `optional`:
  - **Hook obligatorio** (`optional: false`) — **DEBES emitir `EXECUTE_COMMAND:` para cada hook obligatorio**:
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    Después de emitir el bloque anterior, **DEBES** invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma manera en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo, un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.
  - **Hook opcional** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```

## Informe de finalización

El comando finaliza después de la planificación de la Fase 2. Informa la rama, la ruta de IMPL_PLAN y los artefactos generados.

## Fases

### Fase 0: Esquema e investigación

1. **Extrae los desconocidos del Contexto Técnico** anterior:
   - Para cada NEEDS CLARIFICATION → tarea de investigación
   - Para cada dependencia → tarea de mejores prácticas
   - Para cada integración → tarea de patrones

2. **Genera y despacha agentes de investigación**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolida los hallazgos** en `research.md` usando el formato:
   - Decisión: [qué se eligió]
   - Justificación: [por qué se eligió]
   - Alternativas consideradas: [qué más se evaluó]

**Resultado**: research.md con todos los NEEDS CLARIFICATION resueltos

### Fase 1: Diseño y contratos

**Prerrequisitos:** `research.md` completo

1. **Extrae las entidades de la especificación de la funcionalidad** → `data-model.md`:
   - Nombre de la entidad, campos, relaciones
   - Reglas de validación a partir de los requisitos
   - Transiciones de estado si corresponde

2. **Define los contratos de interfaz** (si el proyecto tiene interfaces externas) → `/contracts/`:
   - Identifica qué interfaces expone el proyecto a los usuarios u otros sistemas
   - Documenta el formato de contrato apropiado para el tipo de proyecto
   - Ejemplos: APIs públicas para bibliotecas, esquemas de comandos para herramientas CLI, endpoints para servicios web, gramáticas para parsers, contratos de UI para aplicaciones
   - Omite este paso si el proyecto es puramente interno (scripts de build, herramientas puntuales, etc.)

3. **Crea la guía de validación quickstart** → `quickstart.md`:
   - Documenta escenarios de validación ejecutables que demuestren que la funcionalidad funciona de extremo a extremo
   - Incluye prerrequisitos, comandos de configuración, comandos de prueba/ejecución y resultados esperados
   - Usa enlaces o referencias a los contratos y detalles del modelo de datos en lugar de duplicarlos
   - No incluyas código de implementación completo, cuerpos de modelos/servicios/controladores, migraciones ni suites de pruebas completas
   - Mantén este artefacto como una guía de validación/ejecución; los detalles de implementación pertenecen a `tasks.md` y a la fase de implementación

**Resultado**: data-model.md, /contracts/*, quickstart.md

## Reglas clave

- Usa rutas absolutas para las operaciones del sistema de archivos; usa rutas relativas al proyecto para las referencias en la documentación
- ERROR ante fallos de las puertas de control o aclaraciones sin resolver

## Completado cuando

- [ ] El flujo de trabajo del plan se ejecutó y se generaron los artefactos de diseño
- [ ] Los hooks de extensión se despacharon u omitieron según las reglas en Hooks obligatorios posteriores a la ejecución anteriores
- [ ] Se informó la finalización al usuario con la rama, la ruta del plan y los artefactos generados
