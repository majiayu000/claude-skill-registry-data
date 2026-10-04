---
name: "speckit-tasks"
description: "Genera un tasks.md accionable y ordenado por dependencias para la funcionalidad, basado en los artefactos de diseño disponibles."
argument-hint: "Restricciones opcionales para la generación de tareas"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/tasks.md"
user-invocable: true
disable-model-invocation: false
---


## Entrada del usuario

```text
$ARGUMENTS
```

**DEBES** considerar la entrada del usuario antes de continuar (si no está vacía).

## Verificaciones previas a la ejecución

**Verifica los hooks de extensión (antes de generar tareas)**:
- Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.before_tasks`
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

1. **Configuración**: Ejecuta `.specify/scripts/bash/setup-tasks.sh --json` desde la raíz del repositorio y analiza FEATURE_DIR, TASKS_TEMPLATE y la lista AVAILABLE_DOCS. `FEATURE_DIR` y `TASKS_TEMPLATE` deben ser rutas absolutas cuando se proporcionen. `AVAILABLE_DOCS` es una lista de nombres de documentos/rutas relativas disponibles bajo `FEATURE_DIR` (por ejemplo `research.md` o `contracts/`). Para comillas simples en argumentos como "I'm Groot", usa la sintaxis de escape: por ejemplo 'I'\''m Groot' (o comillas dobles si es posible: "I'm Groot").

2. **Carga los documentos de diseño**: Lee desde FEATURE_DIR:
   - **Requerido**: plan.md (stack tecnológico, bibliotecas, estructura), spec.md (historias de usuario con prioridades)
   - **Opcional**: data-model.md (entidades), contracts/ (contratos de interfaz), research.md (decisiones), quickstart.md (escenarios de prueba)
   - **SI EXISTE**: Carga `.specify/memory/constitution.md` para los principios del proyecto y las restricciones de gobernanza
   - Nota: No todos los proyectos tienen todos los documentos. Genera tareas según lo que esté disponible.

3. **Ejecuta el flujo de generación de tareas**:
   - Carga plan.md y extrae el stack tecnológico, bibliotecas y estructura del proyecto
   - Carga spec.md y extrae las historias de usuario con sus prioridades (P1, P2, P3, etc.)
   - Si existe data-model.md: Extrae las entidades y mapéalas a las historias de usuario
   - Si existe contracts/: Mapea los contratos de interfaz a las historias de usuario
   - Si existe research.md: Extrae las decisiones para las tareas de configuración
   - Genera las tareas organizadas por historia de usuario (ver Reglas de Generación de Tareas más abajo)
   - Genera el grafo de dependencias mostrando el orden de finalización de las historias de usuario
   - Crea ejemplos de ejecución paralela por historia de usuario
   - Valida la completitud de las tareas (cada historia de usuario tiene todas las tareas necesarias, comprobable de forma independiente)

4. **Genera tasks.md**: Lee la plantilla de tareas desde TASKS_TEMPLATE (de la salida JSON de arriba) y úsala como estructura. Si TASKS_TEMPLATE está vacío, recurre a `.specify/templates/tasks-template.md`. Complétala con:
   - Nombre correcto de la funcionalidad tomado de plan.md
   - Fase 1: Tareas de configuración (inicialización del proyecto)
   - Fase 2: Tareas fundacionales (prerrequisitos bloqueantes para todas las historias de usuario)
   - Fase 3+: Una fase por historia de usuario (en orden de prioridad según spec.md)
   - Cada fase incluye: objetivo de la historia, criterios de prueba independiente, pruebas (si se solicitan), tareas de implementación
   - Fase final: Pulido y aspectos transversales
   - Todas las tareas deben seguir el formato estricto de checklist (ver Reglas de Generación de Tareas más abajo)
   - Rutas de archivo claras para cada tarea
   - Sección de Dependencias mostrando el orden de finalización de las historias
   - Ejemplos de ejecución paralela por historia
   - Sección de estrategia de implementación (MVP primero, entrega incremental)

## Hooks obligatorios posteriores a la ejecución

**DEBES completar esta sección antes de informar la finalización al usuario.**

Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si no existe, o no hay hooks registrados bajo `hooks.after_tasks`, salta al Informe de finalización.
- Si existe, léelo y busca entradas bajo la clave `hooks.after_tasks`.
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
    Después de emitir el bloque anterior, DEBES invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma manera en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo, un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.
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

Muestra la ruta al tasks.md generado y un resumen:
- Cantidad total de tareas
- Cantidad de tareas por historia de usuario
- Oportunidades de paralelización identificadas
- Criterios de prueba independiente para cada historia
- Alcance de MVP sugerido (típicamente solo la Historia de Usuario 1)
- Validación de formato: Confirma que TODAS las tareas siguen el formato de checklist (checkbox, ID, etiquetas, rutas de archivo)

Contexto para la generación de tareas: $ARGUMENTS

El tasks.md debe ser inmediatamente ejecutable - cada tarea debe ser lo suficientemente específica para que un LLM pueda completarla sin contexto adicional.

## Reglas de generación de tareas

**CRÍTICO**: Las tareas DEBEN organizarse por historia de usuario para permitir implementación y prueba independientes.

**Las pruebas son OPCIONALES**: Genera tareas de prueba solo si se solicitan explícitamente en la especificación de la funcionalidad o si el usuario pide un enfoque TDD.

### Formato de checklist (REQUERIDO)

Toda tarea DEBE seguir estrictamente este formato:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Componentes del formato**:

1. **Checkbox**: SIEMPRE comienza con `- [ ]` (checkbox de markdown)
2. **ID de tarea**: Número secuencial (T001, T002, T003...) en orden de ejecución
3. **Marcador [P]**: Inclúyelo SOLO si la tarea es paralelizable (archivos distintos, sin dependencias de tareas incompletas)
4. **Etiqueta [Story]**: REQUERIDA solo para tareas de fase de historia de usuario
   - Formato: [US1], [US2], [US3], etc. (mapea a las historias de usuario de spec.md)
   - Fase de configuración: SIN etiqueta de historia
   - Fase fundacional: SIN etiqueta de historia
   - Fases de Historia de Usuario: DEBEN tener etiqueta de historia
   - Fase de pulido: SIN etiqueta de historia
5. **Descripción**: Acción clara con la ruta de archivo exacta

**Ejemplos**:

- ✅ CORRECTO: `- [ ] T001 Create project structure per implementation plan`
- ✅ CORRECTO: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECTO: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ CORRECTO: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ INCORRECTO: `- [ ] Create User model` (falta el ID y la etiqueta de historia)
- ❌ INCORRECTO: `T001 [US1] Create model` (falta el checkbox)
- ❌ INCORRECTO: `- [ ] [US1] Create User model` (falta el ID de tarea)
- ❌ INCORRECTO: `- [ ] T001 [US1] Create model` (falta la ruta de archivo)

### Organización de tareas

1. **Desde las historias de usuario (spec.md)** - ORGANIZACIÓN PRINCIPAL:
   - Cada historia de usuario (P1, P2, P3...) obtiene su propia fase
   - Mapea todos los componentes relacionados a su historia:
     - Modelos necesarios para esa historia
     - Servicios necesarios para esa historia
     - Interfaces/UI necesarias para esa historia
     - Si se solicitan pruebas: Pruebas específicas de esa historia
   - Marca las dependencias entre historias (la mayoría de las historias deberían ser independientes)

2. **Desde los contratos**:
   - Mapea cada contrato de interfaz → a la historia de usuario a la que sirve
   - Si se solicitan pruebas: Cada contrato de interfaz → tarea de prueba de contrato [P] antes de la implementación en la fase de esa historia

3. **Desde el modelo de datos**:
   - Mapea cada entidad a la(s) historia(s) de usuario que la necesitan
   - Si la entidad sirve a varias historias: Colócala en la historia más temprana o en la fase de Configuración
   - Relaciones → tareas de capa de servicio en la fase de historia apropiada

4. **Desde configuración/infraestructura**:
   - Infraestructura compartida → Fase de Configuración (Fase 1)
   - Tareas fundacionales/bloqueantes → Fase Fundacional (Fase 2)
   - Configuración específica de historia → dentro de la fase de esa historia

### Estructura de fases

- **Fase 1**: Configuración (inicialización del proyecto)
- **Fase 2**: Fundacional (prerrequisitos bloqueantes - DEBE completarse antes de las historias de usuario)
- **Fase 3+**: Historias de Usuario en orden de prioridad (P1, P2, P3...)
  - Dentro de cada historia: Pruebas (si se solicitan) → Modelos → Servicios → Endpoints → Integración
  - Cada fase debe ser un incremento completo, comprobable de forma independiente
- **Fase final**: Pulido y aspectos transversales

## Hecho cuando

- [ ] tasks.md generado con todas las fases, IDs de tareas y rutas de archivo
- [ ] Los hooks de extensión se despacharon u omitieron según las reglas en Hooks obligatorios posteriores a la ejecución de arriba
- [ ] Se informó la finalización al usuario con la cantidad de tareas, el desglose por historia y el alcance de MVP
