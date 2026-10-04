---
name: "speckit-checklist"
description: "Genera una lista de verificación personalizada para la funcionalidad actual según los requisitos del usuario."
argument-hint: "Dominio o área de enfoque para la lista de verificación"
compatibility: "Requiere la estructura de proyecto de spec-kit con el directorio .specify/"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/checklist.md"
user-invocable: true
disable-model-invocation: false
---


## Propósito de la lista de verificación: "Pruebas unitarias para el español"

**CONCEPTO CRÍTICO**: Las listas de verificación son **PRUEBAS UNITARIAS PARA LA REDACCIÓN DE REQUISITOS**: validan la calidad, claridad y completitud de los requisitos en un dominio dado.

**NO son para verificación/pruebas**:

- ❌ NO "Verificar que el botón haga clic correctamente"
- ❌ NO "Probar que el manejo de errores funcione"
- ❌ NO "Confirmar que la API devuelve 200"
- ❌ NO comprobar si el código/la implementación coincide con el spec

**SÍ son para la validación de la calidad de los requisitos**:

- ✅ "¿Están definidos los requisitos de jerarquía visual para todos los tipos de tarjetas?" (completitud)
- ✅ "¿Está cuantificada la 'visualización prominente' con un tamaño/posicionamiento específico?" (claridad)
- ✅ "¿Son consistentes los requisitos de estado hover en todos los elementos interactivos?" (consistencia)
- ✅ "¿Están definidos los requisitos de accesibilidad para la navegación por teclado?" (cobertura)
- ✅ "¿El spec define qué sucede cuando la imagen del logo no carga?" (casos límite)

**Metáfora**: Si tu spec es código escrito en español, la lista de verificación es su suite de pruebas unitarias. Estás probando si los requisitos están bien redactados, completos, sin ambigüedades y listos para la implementación, NO si la implementación funciona.

## Entrada del usuario

```text
$ARGUMENTS
```

DEBES considerar la entrada del usuario antes de continuar (si no está vacía).

## Verificaciones previas a la ejecución

**Verificar hooks de extensión (antes de generar la lista de verificación)**:
- Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.before_checklist`
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

    Wait for the result of the hook command before proceeding to the Execution Steps.
    ```
    Después de emitir el bloque anterior, DEBES invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma manera en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo, un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.
- Si no hay hooks registrados o `.specify/extensions.yml` no existe, omite silenciosamente

## Pasos de ejecución

1. **Configuración**: Ejecuta `.specify/scripts/bash/check-prerequisites.sh --json` desde la raíz del repositorio y analiza el JSON para obtener FEATURE_DIR y la lista AVAILABLE_DOCS.
   - Todas las rutas de archivo deben ser absolutas.
   - Para comillas simples en argumentos como "I'm Groot", usa la sintaxis de escape: por ejemplo 'I'\''m Groot' (o comillas dobles si es posible: "I'm Groot").

2. **SI EXISTE**: Carga `.specify/memory/constitution.md` para los principios y las restricciones de gobernanza del proyecto.

3. **Clarificar la intención (dinámico)**: Deriva hasta TRES preguntas de clarificación contextuales iniciales (sin catálogo preestablecido). DEBEN:
   - Generarse a partir de la redacción del usuario + señales extraídas del spec/plan/tasks
   - Preguntar solo sobre información que cambie materialmente el contenido de la lista de verificación
   - Omitirse individualmente si ya son inequívocas en `$ARGUMENTS`
   - Preferir la precisión sobre la amplitud

   Algoritmo de generación:
   1. Extraer señales: palabras clave del dominio de la funcionalidad (por ejemplo, auth, latencia, UX, API), indicadores de riesgo ("crítico", "debe", "cumplimiento"), pistas de interesados ("QA", "revisión", "equipo de seguridad") y entregables explícitos ("a11y", "rollback", "contratos").
   2. Agrupar las señales en áreas de enfoque candidatas (máximo 4) clasificadas por relevancia.
   3. Identificar la audiencia y el momento probables (autor, revisor, QA, lanzamiento) si no son explícitos.
   4. Detectar dimensiones faltantes: amplitud del alcance, profundidad/rigor, énfasis en el riesgo, límites de exclusión, criterios de aceptación medibles.
   5. Formular preguntas elegidas entre estos arquetipos:
      - Refinamiento de alcance (por ejemplo, "¿Debería esto incluir puntos de integración con X e Y, o limitarse a la corrección del módulo local?")
      - Priorización de riesgos (por ejemplo, "¿Cuáles de estas posibles áreas de riesgo deberían recibir verificaciones obligatorias?")
      - Calibración de profundidad (por ejemplo, "¿Es esta una lista de verificación ligera previa al commit o una puerta de calidad formal de lanzamiento?")
      - Encuadre de audiencia (por ejemplo, "¿Será usada solo por el autor o también por los pares durante la revisión de PR?")
      - Exclusión de límites (por ejemplo, "¿Deberíamos excluir explícitamente los elementos de ajuste de rendimiento en esta ronda?")
      - Brecha en la clase de escenario (por ejemplo, "No se detectaron flujos de recuperación: ¿están en alcance las rutas de rollback / falla parcial?")

   Reglas de formato de preguntas:
   - Si presentas opciones, genera una tabla compacta con columnas: Opción | Candidato | Por qué importa
   - Limita a un máximo de opciones A–E; omite la tabla si una respuesta libre es más clara
   - Nunca le pidas al usuario que repita lo que ya dijo
   - Evita categorías especulativas (sin inventar). Si hay incertidumbre, pregunta explícitamente: "Confirma si X pertenece al alcance."

   Valores por defecto cuando la interacción no es posible:
   - Profundidad: Estándar
   - Audiencia: Revisor (PR) si está relacionado con código; Autor en caso contrario
   - Enfoque: Los 2 clústeres de mayor relevancia

   Muestra las preguntas (etiquetadas Q1/Q2/Q3). Después de las respuestas: si quedan ≥2 clases de escenario sin resolver (dominio Alterno / Excepción / Recuperación / No funcional), PUEDES hacer hasta DOS preguntas de seguimiento adicionales (Q4/Q5) con una justificación de una línea cada una (por ejemplo, "Riesgo de ruta de recuperación sin resolver"). No excedas cinco preguntas en total. Omite la escalada si el usuario declina explícitamente más preguntas.

4. **Comprender la solicitud del usuario**: Combina `$ARGUMENTS` + las respuestas de clarificación:
   - Deriva el tema de la lista de verificación (por ejemplo, seguridad, revisión, despliegue, ux)
   - Consolida los elementos imprescindibles explícitos mencionados por el usuario
   - Asigna las selecciones de enfoque a la estructura de categorías
   - Infiere cualquier contexto faltante del spec/plan/tasks (NO inventes)

5. **Cargar el contexto de la funcionalidad**: Lee desde FEATURE_DIR:
   - spec.md: Requisitos y alcance de la funcionalidad
   - plan.md (si existe): Detalles técnicos, dependencias
   - tasks.md (si existe): Tareas de implementación

   **Estrategia de carga de contexto**:
   - Carga solo las partes necesarias relevantes para las áreas de enfoque activas (evita volcar el archivo completo)
   - Prefiere resumir las secciones largas en viñetas concisas de escenario/requisito
   - Usa divulgación progresiva: agrega recuperación adicional solo si se detectan brechas
   - Si los documentos fuente son grandes, genera elementos de resumen intermedios en lugar de incrustar texto en bruto

6. **Generar la lista de verificación** - Crea "pruebas unitarias para los requisitos":
   - Crea el directorio `FEATURE_DIR/checklists/` si no existe
   - Genera un nombre de archivo único para la lista de verificación:
     - Usa un nombre corto y descriptivo basado en el dominio (por ejemplo, `ux.md`, `api.md`, `security.md`)
     - Formato: `[domain].md`
   - Comportamiento de manejo de archivos:
     - Si el archivo NO existe: Crea un archivo nuevo y numera los elementos comenzando en CHK001
     - Si el archivo existe: Agrega nuevos elementos al archivo existente, continuando desde el último ID CHK (por ejemplo, si el último elemento es CHK015, comienza los nuevos elementos en CHK016)
   - Nunca elimines ni reemplaces el contenido existente de la lista de verificación: siempre preserva y agrega

   **PRINCIPIO FUNDAMENTAL - Prueba los requisitos, no la implementación**:
   Cada elemento de la lista de verificación DEBE evaluar los REQUISITOS EN SÍ MISMOS en cuanto a:
   - **Completitud**: ¿Están presentes todos los requisitos necesarios?
   - **Claridad**: ¿Son los requisitos inequívocos y específicos?
   - **Consistencia**: ¿Se alinean los requisitos entre sí?
   - **Medibilidad**: ¿Pueden los requisitos verificarse objetivamente?
   - **Cobertura**: ¿Se abordan todos los escenarios/casos límite?

   **Estructura de categorías** - Agrupa los elementos por dimensiones de calidad de los requisitos:
   - **Completitud de los requisitos** (¿Están documentados todos los requisitos necesarios?)
   - **Claridad de los requisitos** (¿Son los requisitos específicos e inequívocos?)
   - **Consistencia de los requisitos** (¿Se alinean los requisitos sin conflictos?)
   - **Calidad de los criterios de aceptación** (¿Son medibles los criterios de éxito?)
   - **Cobertura de escenarios** (¿Se abordan todos los flujos/casos?)
   - **Cobertura de casos límite** (¿Están definidas las condiciones límite?)
   - **Requisitos no funcionales** (Rendimiento, Seguridad, Accesibilidad, etc. - ¿están especificados?)
   - **Dependencias y suposiciones** (¿Están documentadas y validadas?)
   - **Ambigüedades y conflictos** (¿Qué necesita clarificación?)

   **CÓMO ESCRIBIR ELEMENTOS DE LA LISTA DE VERIFICACIÓN - "Pruebas unitarias para el español"**:

   ❌ **INCORRECTO** (Prueba la implementación):
   - "Verificar que la página de inicio muestre 3 tarjetas de episodios"
   - "Probar que los estados hover funcionen en escritorio"
   - "Confirmar que el clic en el logo navega al inicio"

   ✅ **CORRECTO** (Prueba la calidad de los requisitos):
   - "¿Se especifica el número exacto y la disposición de los episodios destacados?" [Completitud]
   - "¿Está cuantificada la 'visualización prominente' con un tamaño/posicionamiento específico?" [Claridad]
   - "¿Son consistentes los requisitos de estado hover en todos los elementos interactivos?" [Consistencia]
   - "¿Están definidos los requisitos de navegación por teclado para toda la UI interactiva?" [Cobertura]
   - "¿Se especifica el comportamiento de respaldo cuando la imagen del logo no carga?" [Casos límite]
   - "¿Están definidos los estados de carga para los datos asíncronos de episodios?" [Completitud]
   - "¿El spec define la jerarquía visual para elementos de UI en competencia?" [Claridad]

   **ESTRUCTURA DE LOS ELEMENTOS**:
   Cada elemento debe seguir este patrón:
   - Formato de pregunta que indaga sobre la calidad del requisito
   - Enfocarse en lo que está ESCRITO (o no escrito) en el spec/plan
   - Incluir la dimensión de calidad entre corchetes [Completitud/Claridad/Consistencia/etc.]
   - Referenciar la sección del spec `[Spec §X.Y]` al verificar requisitos existentes
   - Usar el marcador `[Gap]` al verificar requisitos faltantes

   **EJEMPLOS POR DIMENSIÓN DE CALIDAD**:

   Completitud:
   - "¿Están definidos los requisitos de manejo de errores para todos los modos de falla de la API? [Gap]"
   - "¿Están especificados los requisitos de accesibilidad para todos los elementos interactivos? [Completitud]"
   - "¿Están definidos los requisitos de puntos de quiebre móviles para los diseños responsivos? [Gap]"

   Claridad:
   - "¿Está cuantificada la 'carga rápida' con umbrales de tiempo específicos? [Claridad, Spec §NFR-2]"
   - "¿Están definidos explícitamente los criterios de selección de 'episodios relacionados'? [Claridad, Spec §FR-5]"
   - "¿Está definido 'prominente' con propiedades visuales medibles? [Ambigüedad, Spec §FR-4]"

   Consistencia:
   - "¿Se alinean los requisitos de navegación en todas las páginas? [Consistencia, Spec §FR-10]"
   - "¿Son consistentes los requisitos de los componentes de tarjeta entre la página de inicio y la de detalle? [Consistencia]"

   Cobertura:
   - "¿Están definidos los requisitos para escenarios de estado cero (sin episodios)? [Cobertura, Caso límite]"
   - "¿Se abordan los escenarios de interacción concurrente de usuarios? [Cobertura, Gap]"
   - "¿Están especificados los requisitos para fallas de carga de datos parciales? [Cobertura, Flujo de excepción]"

   Medibilidad:
   - "¿Son medibles/verificables los requisitos de jerarquía visual? [Criterios de aceptación, Spec §FR-1]"
   - "¿Puede verificarse objetivamente el 'peso visual equilibrado'? [Medibilidad, Spec §FR-2]"

   **Clasificación y cobertura de escenarios** (enfoque en la calidad de los requisitos):
   - Verifica si existen requisitos para escenarios: Primarios, Alternos, Excepción/Error, Recuperación, No funcionales
   - Para cada clase de escenario, pregunta: "¿Son los requisitos de [tipo de escenario] completos, claros y consistentes?"
   - Si falta una clase de escenario: "¿Están los requisitos de [tipo de escenario] intencionalmente excluidos o faltantes? [Gap]"
   - Incluye resiliencia/rollback cuando ocurre mutación de estado: "¿Están definidos los requisitos de rollback para fallas de migración? [Gap]"

   **Requisitos de trazabilidad**:
   - MÍNIMO: ≥80% de los elementos DEBEN incluir al menos una referencia de trazabilidad
   - Cada elemento debe referenciar: la sección del spec `[Spec §X.Y]`, o usar los marcadores: `[Gap]`, `[Ambiguity]`, `[Conflict]`, `[Assumption]`
   - Si no existe un sistema de ID: "¿Está establecido un esquema de ID para requisitos y criterios de aceptación? [Traceability]"

   **Exponer y resolver problemas** (problemas de calidad de los requisitos):
   Haz preguntas sobre los requisitos en sí mismos:
   - Ambigüedades: "¿Está cuantificado el término 'rápido' con métricas específicas? [Ambigüedad, Spec §NFR-1]"
   - Conflictos: "¿Entran en conflicto los requisitos de navegación entre §FR-10 y §FR-10a? [Conflicto]"
   - Suposiciones: "¿Está validada la suposición de 'API de podcast siempre disponible'? [Suposición]"
   - Dependencias: "¿Están documentados los requisitos de la API externa de podcast? [Dependencia, Gap]"
   - Definiciones faltantes: "¿Está definida la 'jerarquía visual' con criterios medibles? [Gap]"

   **Consolidación de contenido**:
   - Límite suave: Si los elementos candidatos en bruto son > 40, prioriza por riesgo/impacto
   - Combina los casi duplicados que verifican el mismo aspecto del requisito
   - Si hay >5 casos límite de bajo impacto, crea un solo elemento: "¿Se abordan los casos límite X, Y, Z en los requisitos? [Cobertura]"

   **🚫 ABSOLUTAMENTE PROHIBIDO** - Esto convierte la lista en una prueba de implementación, no de requisitos:
   - ❌ Cualquier elemento que comience con "Verificar", "Probar", "Confirmar", "Comprobar" + comportamiento de implementación
   - ❌ Referencias a ejecución de código, acciones del usuario, comportamiento del sistema
   - ❌ "Se muestra correctamente", "funciona adecuadamente", "funciona como se espera"
   - ❌ "Clic", "navegar", "renderizar", "cargar", "ejecutar"
   - ❌ Casos de prueba, planes de prueba, procedimientos de QA
   - ❌ Detalles de implementación (frameworks, APIs, algoritmos)

   **✅ PATRONES REQUERIDOS** - Estos prueban la calidad de los requisitos:
   - ✅ "¿Están [tipo de requisito] definidos/especificados/documentados para [escenario]?"
   - ✅ "¿Está [término vago] cuantificado/clarificado con criterios específicos?"
   - ✅ "¿Son consistentes los requisitos entre [sección A] y [sección B]?"
   - ✅ "¿Puede [requisito] medirse/verificarse objetivamente?"
   - ✅ "¿Se abordan [casos límite/escenarios] en los requisitos?"
   - ✅ "¿El spec define [aspecto faltante]?"

7. **Referencia de estructura**: Genera la lista de verificación siguiendo la plantilla canónica en `.specify/templates/checklist-template.md` para el título, la sección de metadatos, los encabezados de categoría y el formato de ID. Si la plantilla no está disponible, usa: título H1, líneas de meta de propósito/creación, secciones de categoría `##` que contengan líneas `- [ ] CHK### <elemento de requisito>` con IDs incrementándose globalmente comenzando en CHK001.

8. **Reporte**: Muestra la ruta completa del archivo de la lista de verificación, la cantidad de elementos, y resume si la ejecución creó un archivo nuevo o agregó a uno existente. Resume:
   - Áreas de enfoque seleccionadas
   - Nivel de profundidad
   - Actor/momento
   - Cualquier elemento imprescindible especificado explícitamente por el usuario que se haya incorporado

**Importante**: Cada invocación del comando `/speckit-checklist` usa un nombre de archivo corto y descriptivo para la lista de verificación, y crea un archivo nuevo o agrega a uno existente. Esto permite:

- Múltiples listas de verificación de diferentes tipos (por ejemplo, `ux.md`, `test.md`, `security.md`)
- Nombres de archivo simples y memorables que indican el propósito de la lista de verificación
- Fácil identificación y navegación en la carpeta `checklists/`

Para evitar desorden, usa tipos descriptivos y limpia las listas de verificación obsoletas cuando termines.

## Tipos de lista de verificación de ejemplo y elementos de muestra

**Calidad de requisitos de UX:** `ux.md`

Elementos de muestra (prueban los requisitos, NO la implementación):

- "¿Están definidos los requisitos de jerarquía visual con criterios medibles? [Claridad, Spec §FR-1]"
- "¿Se especifica explícitamente el número y posicionamiento de los elementos de UI? [Completitud, Spec §FR-1]"
- "¿Están definidos de manera consistente los requisitos de estado de interacción (hover, focus, active)? [Consistencia]"
- "¿Están especificados los requisitos de accesibilidad para todos los elementos interactivos? [Cobertura, Gap]"
- "¿Está definido el comportamiento de respaldo cuando las imágenes no cargan? [Caso límite, Gap]"
- "¿Puede medirse objetivamente la 'visualización prominente'? [Medibilidad, Spec §FR-4]"

**Calidad de requisitos de API:** `api.md`

Elementos de muestra:

- "¿Están especificados los formatos de respuesta de error para todos los escenarios de falla? [Completitud]"
- "¿Están cuantificados los requisitos de limitación de tasa con umbrales específicos? [Claridad]"
- "¿Son consistentes los requisitos de autenticación en todos los endpoints? [Consistencia]"
- "¿Están definidos los requisitos de reintento/tiempo de espera para las dependencias externas? [Cobertura, Gap]"
- "¿Está documentada la estrategia de versionado en los requisitos? [Gap]"

**Calidad de requisitos de rendimiento:** `performance.md`

Elementos de muestra:

- "¿Están cuantificados los requisitos de rendimiento con métricas específicas? [Claridad]"
- "¿Están definidos los objetivos de rendimiento para todos los recorridos críticos del usuario? [Cobertura]"
- "¿Están especificados los requisitos de rendimiento bajo diferentes condiciones de carga? [Completitud]"
- "¿Pueden medirse objetivamente los requisitos de rendimiento? [Medibilidad]"
- "¿Están definidos los requisitos de degradación para escenarios de alta carga? [Caso límite, Gap]"

**Calidad de requisitos de seguridad:** `security.md`

Elementos de muestra:

- "¿Están especificados los requisitos de autenticación para todos los recursos protegidos? [Cobertura]"
- "¿Están definidos los requisitos de protección de datos para información sensible? [Completitud]"
- "¿Está documentado el modelo de amenazas y los requisitos alineados a él? [Trazabilidad]"
- "¿Son consistentes los requisitos de seguridad con las obligaciones de cumplimiento? [Consistencia]"
- "¿Están definidos los requisitos de respuesta ante fallas/brechas de seguridad? [Gap, Flujo de excepción]"

## Antiejemplos: qué NO hacer

**❌ INCORRECTO - Estos prueban la implementación, no los requisitos:**

```markdown
- [ ] CHK001 - Verificar que la landing page muestra 3 tarjetas de episodio [Spec §FR-001]
- [ ] CHK002 - Probar que los estados hover funcionan correctamente en desktop [Spec §FR-003]
- [ ] CHK003 - Confirmar que el clic en el logo navega a la página de inicio [Spec §FR-010]
- [ ] CHK004 - Verificar que la sección de episodios relacionados muestra de 3 a 5 elementos [Spec §FR-005]
```

**✅ CORRECTO - Estos prueban la calidad de los requisitos:**

```markdown
- [ ] CHK001 - ¿Están explícitamente especificados el número y el layout de los episodios destacados? [Completeness, Spec §FR-001]
- [ ] CHK002 - ¿Están definidos de forma consistente los requisitos de estado hover para todos los elementos interactivos? [Consistency, Spec §FR-003]
- [ ] CHK003 - ¿Son claros los requisitos de navegación para todos los elementos de marca clicables? [Clarity, Spec §FR-010]
- [ ] CHK004 - ¿Están documentados los criterios de selección de episodios relacionados? [Gap, Spec §FR-005]
- [ ] CHK005 - ¿Están definidos los requisitos de estado de carga para los datos asíncronos de episodios? [Gap]
- [ ] CHK006 - ¿Pueden medirse objetivamente los requisitos de "jerarquía visual"? [Measurability, Spec §FR-001]
```

**Diferencias clave:**

- Incorrecto: Prueba si el sistema funciona correctamente
- Correcto: Prueba si los requisitos están escritos correctamente
- Incorrecto: Verificación del comportamiento
- Correcto: Validación de la calidad del requisito
- Incorrecto: "¿Hace X?"
- Correcto: "¿Está X claramente especificado?"

## Verificaciones posteriores a la ejecución

**Verificar hooks de extensión (después de generar la lista de verificación)**:
Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.after_checklist`
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
