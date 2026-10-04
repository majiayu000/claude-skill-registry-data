---
name: "speckit-specify"
description: "Crea o actualiza la especificación de la funcionalidad a partir de una descripción en lenguaje natural."
argument-hint: "Describe la funcionalidad que quieres especificar"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/specify.md"
user-invocable: true
disable-model-invocation: false
---


## Entrada del usuario

```text
$ARGUMENTS
```

**DEBES** considerar la entrada del usuario antes de continuar (si no está vacía).

## Verificaciones previas a la ejecución

**Verifica los hooks de extensión (antes de especificar)**:
- Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.before_specify`
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

El texto que el usuario escribió después de `/speckit-specify` en el mensaje que dispara el comando **es** la descripción de la funcionalidad. Asume que siempre la tienes disponible en esta conversación, aunque `$ARGUMENTS` aparezca literalmente más abajo. No le pidas al usuario que la repita, salvo que haya enviado un comando vacío.

Dada esa descripción de la funcionalidad, haz esto:

1. **Genera un nombre corto conciso** (2-4 palabras) para la funcionalidad:
   - Analiza la descripción de la funcionalidad y extrae las palabras clave más significativas
   - Crea un nombre corto de 2-4 palabras que capture la esencia de la funcionalidad
   - Usa el formato acción-sustantivo cuando sea posible (p. ej., "add-user-auth", "fix-payment-bug")
   - Preserva términos técnicos y siglas (OAuth2, API, JWT, etc.)
   - Mantenlo conciso pero lo suficientemente descriptivo para entender la funcionalidad de un vistazo
   - Ejemplos:
     - "Quiero agregar autenticación de usuarios" → "user-auth"
     - "Implementar integración OAuth2 para la API" → "oauth2-api-integration"
     - "Crear un dashboard de analítica" → "analytics-dashboard"
     - "Corregir el bug de timeout en el procesamiento de pagos" → "fix-payment-timeout"

2. **Creación de rama** (opcional, vía hook):

   Si un hook `before_specify` se ejecutó exitosamente en las Verificaciones previas a la ejecución de arriba, habrá creado/cambiado a una rama git y producido un JSON con `BRANCH_NAME` y `FEATURE_NUM`. Toma nota de estos valores como referencia, pero el nombre de la rama **no** determina el nombre del directorio del spec.

   Si el usuario proporcionó explícitamente `GIT_BRANCH_NAME`, pásalo al hook para que el script de rama use ese valor exacto como nombre de la rama (evitando toda generación de prefijo/sufijo).

3. **Crea el directorio de la funcionalidad del spec**:

   Los specs viven bajo el directorio `specs/` por defecto, a menos que el usuario proporcione explícitamente `SPECIFY_FEATURE_DIRECTORY`.

   **Orden de resolución para `SPECIFY_FEATURE_DIRECTORY`**:
   1. Si el usuario proporcionó explícitamente `SPECIFY_FEATURE_DIRECTORY` (p. ej., vía variable de entorno, argumento o configuración), úsalo tal cual
   2. En caso contrario, autogénéralo bajo `specs/`:
      - Verifica `.specify/init-options.json` para `feature_numbering` (preferido) o `branch_numbering` (obsoleto, solo para migración — se eliminará en una versión futura)
      - Si es `"timestamp"`: el prefijo es `YYYYMMDD-HHMMSS` (marca de tiempo actual)
      - Si es `"sequential"` o está ausente: el prefijo es `NNN` (el siguiente número de 3 dígitos disponible tras escanear los directorios existentes en `specs/`)
      - Construye el nombre del directorio: `<prefijo>-<nombre-corto>` (p. ej., `003-user-auth` o `20260319-143022-user-auth`)
      - Establece `SPECIFY_FEATURE_DIRECTORY` como `specs/<nombre-de-directorio>`
      - Si se usó `branch_numbering` (y `feature_numbering` estaba ausente), emite una advertencia de una línea: "⚠️ `branch_numbering` en init-options.json está obsoleto. Renómbralo a `feature_numbering`."

   **Crea el directorio y el archivo del spec**:
   - `mkdir -p SPECIFY_FEATURE_DIRECTORY`
   - Resuelve la `spec-template` activa a través de la pila de resolución de presets/plantillas de Spec Kit (equivalente a `specify preset resolve spec-template`)
   - Copia el archivo `spec-template` resuelto a `SPECIFY_FEATURE_DIRECTORY/spec.md` como punto de partida
   - Establece `SPEC_FILE` como `SPECIFY_FEATURE_DIRECTORY/spec.md`
   - Persiste la ruta resuelta en `.specify/feature.json`:
     ```json
     {
       "feature_directory": "<resolved feature dir>"
     }
     ```
     Escribe el valor real de la ruta del directorio resuelto (por ejemplo, `specs/003-user-auth`), no el string literal `SPECIFY_FEATURE_DIRECTORY`.
     Esto permite que los comandos posteriores (`/speckit-plan`, `/speckit-tasks`, etc.) localicen el directorio de la funcionalidad sin depender de convenciones de nombres de rama git.

   **IMPORTANTE**:
   - Solo debes crear una funcionalidad por invocación de `/speckit-specify`
   - El nombre del directorio del spec y el nombre de la rama git son independientes — pueden ser el mismo, pero eso es decisión del usuario
   - El directorio y el archivo del spec siempre son creados por este comando, nunca por el hook

4. Carga el archivo `spec-template` activo resuelto para entender las secciones requeridas.

5. **SI EXISTE**: Carga `.specify/memory/constitution.md` para los principios del proyecto y las restricciones de gobernanza.

6. Sigue este flujo de ejecución:
    1. Analiza la descripción del usuario a partir de los argumentos
       Si está vacía: ERROR "No se proporcionó descripción de la funcionalidad"
    2. Extrae los conceptos clave de la descripción
       Identifica: actores, acciones, datos, restricciones
    3. Para los aspectos poco claros:
       - Haz suposiciones informadas basadas en el contexto y los estándares de la industria
       - Marca con [NEEDS CLARIFICATION: pregunta específica] solo si:
         - La elección impacta significativamente el alcance de la funcionalidad o la experiencia del usuario
         - Existen múltiples interpretaciones razonables con implicaciones distintas
         - No existe un valor por defecto razonable
       - **LÍMITE: Máximo 3 marcadores [NEEDS CLARIFICATION] en total**
       - Prioriza las aclaraciones por impacto: alcance > seguridad/privacidad > experiencia de usuario > detalles técnicos
    4. Completa la sección de Escenarios de Usuario y Pruebas
       Si no hay un flujo de usuario claro: ERROR "No se pueden determinar los escenarios de usuario"
    5. Genera los Requisitos Funcionales
       Cada requisito debe ser comprobable
       Usa valores por defecto razonables para los detalles no especificados (documenta las suposiciones en la sección de Suposiciones)
    6. Define los Criterios de Éxito
       Crea resultados medibles y agnósticos de tecnología
       Incluye tanto métricas cuantitativas (tiempo, rendimiento, volumen) como medidas cualitativas (satisfacción del usuario, finalización de tareas)
       Cada criterio debe ser verificable sin detalles de implementación
    7. Identifica las Entidades Clave (si hay datos involucrados)
    8. Retorna: SUCCESS (spec listo para la planificación)

6. Escribe la especificación en SPEC_FILE usando la estructura de la plantilla, reemplazando los marcadores de posición con detalles concretos derivados de la descripción de la funcionalidad (argumentos), preservando el orden de las secciones y los encabezados.

7. **Validación de calidad de la especificación**: Después de escribir el spec inicial, valídalo contra los criterios de calidad:

   a. **Crea la lista de verificación de calidad del spec**: Genera un archivo de checklist en `SPECIFY_FEATURE_DIRECTORY/checklists/requirements.md` usando la estructura de la plantilla de checklist con estos elementos de validación:

      ```markdown
      # Checklist de Calidad de la Especificación: [FEATURE NAME]
      
      **Propósito**: Validar la completitud y calidad de la especificación antes de pasar a la planificación
      **Creado**: [DATE]
      **Funcionalidad**: [Link to spec.md]
      
      ## Calidad del contenido
      
      - [ ] Sin detalles de implementación (lenguajes, frameworks, APIs)
      - [ ] Enfocado en el valor para el usuario y las necesidades de negocio
      - [ ] Escrito para stakeholders no técnicos
      - [ ] Todas las secciones obligatorias completadas
      
      ## Completitud de los requisitos
      
      - [ ] No quedan marcadores [NEEDS CLARIFICATION]
      - [ ] Los requisitos son comprobables e inequívocos
      - [ ] Los criterios de éxito son medibles
      - [ ] Los criterios de éxito son agnósticos de tecnología (sin detalles de implementación)
      - [ ] Todos los escenarios de aceptación están definidos
      - [ ] Los casos límite están identificados
      - [ ] El alcance está claramente delimitado
      - [ ] Las dependencias y suposiciones están identificadas
      
      ## Preparación de la funcionalidad
      
      - [ ] Todos los requisitos funcionales tienen criterios de aceptación claros
      - [ ] Los escenarios de usuario cubren los flujos principales
      - [ ] La funcionalidad cumple los resultados medibles definidos en los Criterios de Éxito
      - [ ] Ningún detalle de implementación se filtra en la especificación
      
      ## Notas
      
      - Los elementos marcados como incompletos requieren actualizar el spec antes de `/speckit-clarify` o `/speckit-plan`
      ```

   b. **Ejecuta la verificación de validación**: Revisa el spec contra cada elemento de la checklist:
      - Para cada elemento, determina si pasa o falla
      - Documenta los problemas específicos encontrados (cita las secciones relevantes del spec)

   c. **Maneja los resultados de la validación**:

      - **Si todos los elementos pasan**: Marca la checklist como completa y continúa con la sección de Hooks obligatorios posteriores a la ejecución

      - **Si algunos elementos fallan (excluyendo [NEEDS CLARIFICATION])**:
        1. Lista los elementos que fallan y los problemas específicos
        2. Actualiza el spec para resolver cada problema
        3. Vuelve a ejecutar la validación hasta que todos los elementos pasen (máximo 3 iteraciones)
        4. Si sigue fallando después de 3 iteraciones, documenta los problemas restantes en las notas de la checklist y advierte al usuario

      - **Si quedan marcadores [NEEDS CLARIFICATION]**:
        1. Extrae todos los marcadores [NEEDS CLARIFICATION: ...] del spec
        2. **VERIFICACIÓN DE LÍMITE**: Si existen más de 3 marcadores, conserva solo los 3 más críticos (por impacto en alcance/seguridad/UX) y haz suposiciones informadas para el resto
        3. Para cada aclaración necesaria (máximo 3), presenta opciones al usuario en este formato:

           ```markdown
           ## Pregunta [N]: [Topic]
           
           **Contexto**: [Quote relevant spec section]
           
           **Qué necesitamos saber**: [Specific question from NEEDS CLARIFICATION marker]
           
           **Respuestas sugeridas**:
           
           | Opción | Respuesta | Implicaciones |
           |--------|--------|--------------|
           | A      | [Primera respuesta sugerida] | [Qué significa esto para la funcionalidad] |
           | B      | [Segunda respuesta sugerida] | [Qué significa esto para la funcionalidad] |
           | C      | [Tercera respuesta sugerida] | [Qué significa esto para la funcionalidad] |
           | Personalizada | Proporciona tu propia respuesta | [Explica cómo dar una respuesta personalizada] |
           
           **Tu elección**: _[Esperar respuesta del usuario]_
           ```

        4. **CRÍTICO - Formato de tablas**: Asegúrate de que las tablas markdown estén correctamente formateadas:
           - Usa espaciado consistente con las barras verticales alineadas
           - Cada celda debe tener espacios alrededor del contenido: `| Contenido |`, no `|Contenido|`
           - El separador del encabezado debe tener al menos 3 guiones: `|--------|`
           - Verifica que la tabla se renderice correctamente en la vista previa de markdown
        5. Numera las preguntas secuencialmente (Q1, Q2, Q3 - máximo 3 en total)
        6. Presenta todas las preguntas juntas antes de esperar respuestas
        7. Espera a que el usuario responda con sus elecciones para todas las preguntas (p. ej., "Q1: A, Q2: Custom - [detalles], Q3: B")
        8. Actualiza el spec reemplazando cada marcador [NEEDS CLARIFICATION] con la respuesta seleccionada o proporcionada por el usuario
        9. Vuelve a ejecutar la validación después de que se resuelvan todas las aclaraciones

   d. **Actualiza la checklist**: Después de cada iteración de validación, actualiza el archivo de checklist con el estado actual de aprobado/fallido

## Hooks obligatorios posteriores a la ejecución

**DEBES completar esta sección antes de informar la finalización al usuario.**

Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si no existe, o no hay hooks registrados bajo `hooks.after_specify`, salta al Informe de finalización.
- Si existe, léelo y busca entradas bajo la clave `hooks.after_specify`.
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

Informa la finalización al usuario con:
- `SPECIFY_FEATURE_DIRECTORY` — la ruta del directorio de la funcionalidad
- `SPEC_FILE` — la ruta del archivo del spec
- Resumen de resultados de la checklist
- Preparación para la siguiente fase (`/speckit-clarify` o `/speckit-plan`)

**NOTA:** La creación de la rama la maneja el hook `before_specify` (extensión de git). La creación del directorio y el archivo del spec siempre las maneja este comando central.

## Guías rápidas

- Enfócate en el **QUÉ** necesitan los usuarios y el **POR QUÉ**.
- Evita el CÓMO implementarlo (sin stack tecnológico, APIs, estructura de código).
- Escrito para stakeholders de negocio, no para desarrolladores.
- NO crees ninguna checklist embebida en el spec. Eso será un comando separado.

### Requisitos de sección

- **Secciones obligatorias**: Deben completarse para toda funcionalidad
- **Secciones opcionales**: Inclúyelas solo cuando sean relevantes para la funcionalidad
- Cuando una sección no aplique, elimínala por completo (no la dejes como "N/A")

### Para generación por IA

Al crear este spec a partir de un prompt del usuario:

1. **Haz suposiciones informadas**: Usa el contexto, los estándares de la industria y patrones comunes para llenar los vacíos
2. **Documenta las suposiciones**: Registra los valores por defecto razonables en la sección de Suposiciones
3. **Limita las aclaraciones**: Máximo 3 marcadores [NEEDS CLARIFICATION] - úsalos solo para decisiones críticas que:
   - Impacten significativamente el alcance de la funcionalidad o la experiencia del usuario
   - Tengan múltiples interpretaciones razonables con implicaciones distintas
   - Carezcan de cualquier valor por defecto razonable
4. **Prioriza las aclaraciones**: alcance > seguridad/privacidad > experiencia de usuario > detalles técnicos
5. **Piensa como un tester**: Todo requisito vago debería fallar el elemento de checklist "comprobable e inequívoco"
6. **Áreas comunes que necesitan aclaración** (solo si no existe un valor por defecto razonable):
   - Alcance y límites de la funcionalidad (incluir/excluir casos de uso específicos)
   - Tipos de usuario y permisos (si son posibles múltiples interpretaciones conflictivas)
   - Requisitos de seguridad/cumplimiento (cuando sean legal o financieramente significativos)

**Ejemplos de valores por defecto razonables** (no preguntes sobre esto):

- Retención de datos: Prácticas estándar de la industria para el dominio
- Objetivos de rendimiento: Expectativas estándar de apps web/móviles salvo que se especifique lo contrario
- Manejo de errores: Mensajes amigables para el usuario con fallbacks apropiados
- Método de autenticación: Basado en sesión estándar u OAuth2 para apps web
- Patrones de integración: Usa los patrones apropiados para el proyecto (REST/GraphQL para servicios web, llamadas a funciones para bibliotecas, argumentos CLI para herramientas, etc.)

### Guías de criterios de éxito

Los criterios de éxito deben ser:

1. **Medibles**: Incluir métricas específicas (tiempo, porcentaje, cantidad, tasa)
2. **Agnósticos de tecnología**: Sin mencionar frameworks, lenguajes, bases de datos ni herramientas
3. **Enfocados en el usuario**: Describir resultados desde la perspectiva del usuario/negocio, no los detalles internos del sistema
4. **Verificables**: Poder probarse/validarse sin conocer los detalles de implementación

**Buenos ejemplos**:

- "Los usuarios pueden completar el checkout en menos de 3 minutos"
- "El sistema soporta 10,000 usuarios concurrentes"
- "El 95% de las búsquedas devuelve resultados en menos de 1 segundo"
- "La tasa de finalización de tareas mejora un 40%"

**Malos ejemplos** (enfocados en implementación):

- "El tiempo de respuesta de la API es menor a 200ms" (demasiado técnico, usa "Los usuarios ven los resultados al instante")
- "La base de datos puede manejar 1000 TPS" (detalle de implementación, usa una métrica orientada al usuario)
- "Los componentes de React se renderizan eficientemente" (específico del framework)
- "La tasa de aciertos de la caché Redis es superior al 80%" (específico de la tecnología)

## Hecho cuando

- [ ] La especificación fue escrita en `SPEC_FILE` y validada contra la checklist de calidad
- [ ] Los hooks de extensión se despacharon u omitieron según las reglas en Hooks obligatorios posteriores a la ejecución de arriba
- [ ] Se informó la finalización al usuario con el directorio de la funcionalidad, la ruta del spec y los resultados de la checklist
