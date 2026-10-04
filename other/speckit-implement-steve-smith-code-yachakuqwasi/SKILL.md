---
name: "speckit-implement"
description: "Ejecuta el plan de implementación procesando y ejecutando todas las tareas definidas en tasks.md"
argument-hint: "Orientación de implementación opcional o filtro de tareas"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/implement.md"
user-invocable: true
disable-model-invocation: false
---


## Entrada del usuario

```text
$ARGUMENTS
```

**DEBE** considerar la entrada del usuario antes de continuar (si no está vacía).

## Verificaciones previas a la ejecución

**Verificar hooks de extensión (antes de la implementación)**:
- Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.before_implement`
- Si el YAML no se puede analizar o no es válido, omite la verificación de hooks silenciosamente y continúa con normalidad
- Filtra los hooks donde `enabled` sea explícitamente `false`. Trata los hooks sin el campo `enabled` como habilitados por defecto.
- Para cada hook restante, **no** intentes interpretar ni evaluar las expresiones `condition` del hook:
  - Si el hook no tiene campo `condition`, o está vacío/null, trata el hook como ejecutable
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
    Después de emitir el bloque anterior, DEBE invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma forma en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo, un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.
- Si no hay hooks registrados o `.specify/extensions.yml` no existe, omite silenciosamente

## Esquema

1. Ejecuta `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` desde la raíz del repositorio y analiza FEATURE_DIR y la lista AVAILABLE_DOCS. Todas las rutas deben ser absolutas. Para comillas simples en argumentos como "I'm Groot", usa la sintaxis de escape: por ejemplo 'I'\''m Groot' (o comillas dobles si es posible: "I'm Groot").

2. **Verificar el estado de los checklists** (si existe FEATURE_DIR/checklists/):
   - Escanea todos los archivos de checklist en el directorio checklists/
   - Para cada checklist, cuenta:
     - Elementos totales: todas las líneas que coincidan con `- [ ]`, `- [X]` o `- [x]`
     - Elementos completados: líneas que coincidan con `- [X]` o `- [x]`
     - Elementos incompletos: líneas que coincidan con `- [ ]`
   - Crea una tabla de estado:

     ```text
     | Checklist | Total | Completed | Incomplete | Status |
     |-----------|-------|-----------|------------|--------|
     | ux.md     | 12    | 12        | 0          | ✓ PASS |
     | test.md   | 8     | 5         | 3          | ✗ FAIL |
     | security.md | 6   | 6         | 0          | ✓ PASS |
     ```

   - Calcula el estado general:
     - **PASS**: todos los checklists tienen 0 elementos incompletos
     - **FAIL**: uno o más checklists tienen elementos incompletos

   - **Si algún checklist está incompleto**:
     - Muestra la tabla con los conteos de elementos incompletos
     - **DETENTE** y pregunta: "Algunos checklists están incompletos. ¿Deseas continuar con la implementación de todos modos? (sí/no)"
     - Espera la respuesta del usuario antes de continuar
     - Si el usuario dice "no" o "espera" o "detente", detén la ejecución
     - Si el usuario dice "sí" o "continuar" o "proceder", continúa con el paso 3

   - **Si todos los checklists están completos**:
     - Muestra la tabla indicando que todos los checklists pasaron
     - Continúa automáticamente al paso 3

3. Carga y analiza el contexto de implementación:
   - **REQUERIDO**: lee tasks.md para obtener la lista completa de tareas y el plan de ejecución
   - **REQUERIDO**: lee plan.md para el stack tecnológico, la arquitectura y la estructura de archivos
   - **SI EXISTE**: lee data-model.md para las entidades y relaciones
   - **SI EXISTE**: lee contracts/ para las especificaciones de API y los requisitos de prueba
   - **SI EXISTE**: lee research.md para las decisiones técnicas y las restricciones
   - **SI EXISTE**: lee .specify/memory/constitution.md para las restricciones de gobernanza
   - **SI EXISTE**: lee quickstart.md para los escenarios de integración

4. **Verificación de la configuración del proyecto**:
   - **REQUERIDO**: crea/verifica los archivos ignore según la configuración real del proyecto:

   **Lógica de detección y creación**:
   - Verifica si el siguiente comando se ejecuta con éxito para determinar si el repositorio es un repo git (crea/verifica .gitignore si es así):

     ```sh
     git rev-parse --git-dir 2>/dev/null
     ```

   - Verifica si existe Dockerfile* o si Docker aparece en plan.md → crea/verifica .dockerignore
   - Verifica si existe .eslintrc* → crea/verifica .eslintignore
   - Verifica si existe eslint.config.* → asegúrate de que las entradas `ignores` de la configuración cubran los patrones requeridos
   - Verifica si existe .prettierrc* → crea/verifica .prettierignore
   - Verifica si existe .npmrc o package.json → crea/verifica .npmignore (si se publica)
   - Verifica si existen archivos terraform (*.tf) → crea/verifica .terraformignore
   - Verifica si se necesita .helmignore (hay charts de helm presentes) → crea/verifica .helmignore

   **Si el archivo ignore ya existe**: verifica que contenga los patrones esenciales, agrega solo los patrones críticos faltantes
   **Si falta el archivo ignore**: créalo con el conjunto completo de patrones para la tecnología detectada

   **Patrones comunes por tecnología** (según el stack tecnológico de plan.md):
   - **Node.js/JavaScript/TypeScript**: `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
   - **Python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
   - **Java**: `target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
   - **C#/.NET**: `bin/`, `obj/`, `*.user`, `*.suo`, `packages/`
   - **Go**: `*.exe`, `*.test`, `vendor/`, `*.out`
   - **Ruby**: `.bundle/`, `log/`, `tmp/`, `*.gem`, `vendor/bundle/`
   - **PHP**: `vendor/`, `*.log`, `*.cache`, `*.env`
   - **Rust**: `target/`, `debug/`, `release/`, `*.rs.bk`, `*.rlib`, `*.prof*`, `.idea/`, `*.log`, `.env*`
   - **Kotlin**: `build/`, `out/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, `*.iml`, `*.log`, `.env*`
   - **C++**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.so`, `*.a`, `*.exe`, `*.dll`, `.idea/`, `*.log`, `.env*`
   - **C**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.a`, `*.so`, `*.exe`, `*.dll`, `autom4te.cache/`, `config.status`, `config.log`, `.idea/`, `*.log`, `.env*`
   - **Swift**: `.build/`, `DerivedData/`, `*.swiftpm/`, `Packages/`
   - **R**: `.Rproj.user/`, `.Rhistory`, `.RData`, `.Ruserdata`, `*.Rproj`, `packrat/`, `renv/`
   - **Universal**: `.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

   **Patrones específicos por herramienta**:
   - **Docker**: `node_modules/`, `.git/`, `Dockerfile*`, `.dockerignore`, `*.log*`, `.env*`, `coverage/`
   - **ESLint**: `node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
   - **Prettier**: `node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - **Terraform**: `.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
   - **Kubernetes/k8s**: `*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`, `*.key`, `*.crt`

5. Analiza la estructura de tasks.md y extrae:
   - **Fases de las tareas**: Setup, Tests, Core, Integration, Polish
   - **Dependencias de las tareas**: reglas de ejecución secuencial vs. paralela
   - **Detalles de las tareas**: ID, descripción, rutas de archivo, marcadores paralelos [P]
   - **Flujo de ejecución**: orden y requisitos de dependencia

6. Ejecuta la implementación siguiendo el plan de tareas:
   - **Ejecución fase por fase**: completa cada fase antes de pasar a la siguiente
   - **Respeta las dependencias**: ejecuta las tareas secuenciales en orden; las tareas paralelas [P] pueden ejecutarse juntas
   - **Sigue el enfoque TDD**: ejecuta las tareas de prueba antes de sus correspondientes tareas de implementación
   - **Coordinación basada en archivos**: las tareas que afectan a los mismos archivos deben ejecutarse secuencialmente
   - **Puntos de control de validación**: verifica la finalización de cada fase antes de continuar

7. Reglas de ejecución de la implementación:
   - **Primero la configuración**: inicializa la estructura del proyecto, las dependencias y la configuración
   - **Pruebas antes que código**: si es necesario, escribe pruebas para contratos, entidades y escenarios de integración
   - **Desarrollo del núcleo**: implementa modelos, servicios, comandos CLI, endpoints
   - **Trabajo de integración**: conexiones a bases de datos, middleware, logging, servicios externos
   - **Pulido y validación**: pruebas unitarias, optimización de rendimiento, documentación

8. Seguimiento del progreso y manejo de errores:
   - Informa el progreso después de cada tarea completada
   - Detén la ejecución si falla alguna tarea no paralela
   - Para las tareas paralelas [P], continúa con las que tuvieron éxito e informa las que fallaron
   - Proporciona mensajes de error claros con contexto para depuración
   - Sugiere los próximos pasos si la implementación no puede continuar
   - **IMPORTANTE**: para las tareas completadas, asegúrate de marcarlas como [X] en el archivo de tareas.

9. Validación de finalización:
   - Verifica que todas las tareas requeridas estén completadas
   - Comprueba que las funcionalidades implementadas coincidan con la especificación original
   - Valida que las pruebas pasen y que la cobertura cumpla con los requisitos
   - Confirma que la implementación sigue el plan técnico

Nota: este comando asume que existe un desglose completo de tareas en tasks.md. Si las tareas están incompletas o faltan, sugiere ejecutar primero `/speckit-tasks` para regenerar la lista de tareas.

## Hooks obligatorios posteriores a la ejecución

**DEBE completar esta sección antes de informar la finalización al usuario.**

Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si no existe, o no hay hooks registrados bajo `hooks.after_implement`, pasa directamente al Informe de finalización.
- Si existe, léelo y busca entradas bajo la clave `hooks.after_implement`.
- Si el YAML no se puede analizar o no es válido, omite la verificación de hooks silenciosamente y continúa hacia el Informe de finalización.
- Filtra los hooks donde `enabled` sea explícitamente `false`. Trata los hooks sin el campo `enabled` como habilitados por defecto.
- Para cada hook restante, **no** intentes interpretar ni evaluar las expresiones `condition` del hook:
  - Si el hook no tiene campo `condition`, o está vacío/null, trata el hook como ejecutable
  - Si el hook define un `condition` no vacío, omite el hook y deja la evaluación de la condición a la implementación de HookExecutor
- Al construir comandos slash a partir de los nombres de comando del hook, reemplaza los puntos (`.`) por guiones (`-`). Por ejemplo, `speckit.git.commit` → `/speckit-git-commit`.
- Para cada hook ejecutable, muestra lo siguiente según su indicador `optional`:
  - **Hook obligatorio** (`optional: false`) — **DEBE emitir `EXECUTE_COMMAND:` para cada hook obligatorio**:
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    Después de emitir el bloque anterior, DEBE invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma forma en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo, un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.
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

Informa el estado final con un resumen del trabajo completado.

## Se considera hecho cuando

- [ ] Todas las tareas en tasks.md están completadas y marcadas como `[X]`
- [ ] La implementación está validada contra la especificación, el plan y la cobertura de pruebas
- [ ] Los hooks de extensión se despacharon u omitieron según las reglas de la sección Hooks obligatorios posteriores a la ejecución anterior
- [ ] La finalización se informó al usuario con un resumen del trabajo completado
