---
name: "speckit-clarify"
description: "Identifica áreas subespecificadas en la especificación de la funcionalidad actual haciendo hasta 5 preguntas de aclaración muy específicas y codificando las respuestas de vuelta en la especificación."
argument-hint: "Áreas opcionales a aclarar en la especificación"
compatibility: "Requiere la estructura de proyecto de spec-kit con el directorio .specify/"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/clarify.md"
user-invocable: true
disable-model-invocation: false
---


## Entrada del usuario

```text
$ARGUMENTS
```

DEBES considerar la entrada del usuario antes de continuar (si no está vacía).

## Verificaciones previas a la ejecución

**Verificar hooks de extensión (antes de la aclaración)**:
- Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si existe, léelo y busca entradas bajo la clave `hooks.before_clarify`
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

Objetivo: Detectar y reducir la ambigüedad o los puntos de decisión faltantes en la especificación de la funcionalidad activa y registrar las aclaraciones directamente en el archivo de especificación.

Nota: Se espera que este flujo de aclaración se ejecute (y se complete) ANTES de invocar `/speckit-plan`. Si el usuario indica explícitamente que está omitiendo la aclaración (por ejemplo, un spike exploratorio), puedes continuar, pero debes advertir que el riesgo de retrabajo posterior aumenta.

Pasos de ejecución:

1. Ejecuta `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` desde la raíz del repositorio **una vez** (modo combinado `--json --paths-only` / `-Json -PathsOnly`). Parsea los campos mínimos del payload JSON:
   - `FEATURE_DIR`
   - `FEATURE_SPEC`
   - (Opcionalmente captura `IMPL_PLAN`, `TASKS` para futuros flujos encadenados.)
   - Si el parseo del JSON falla, aborta e indica al usuario que vuelva a ejecutar `/speckit-specify` o que verifique el entorno de la rama de la funcionalidad.
   - Para comillas simples en argumentos como "I'm Groot", usa la sintaxis de escape: por ejemplo 'I'\''m Groot' (o comillas dobles si es posible: "I'm Groot").

2. **SI EXISTE**: Carga `.specify/memory/constitution.md` para conocer los principios del proyecto y las restricciones de gobernanza.

3. Carga el archivo de especificación actual. Realiza un análisis estructurado de ambigüedad y cobertura usando esta taxonomía. Para cada categoría, marca el estado: Clara / Parcial / Faltante. Produce un mapa de cobertura interno usado para la priorización (no muestres el mapa en bruto a menos que no se vaya a hacer ninguna pregunta).

   Alcance funcional y comportamiento:
   - Objetivos principales del usuario y criterios de éxito
   - Declaraciones explícitas de fuera de alcance
   - Diferenciación de roles de usuario / personas

   Dominio y modelo de datos:
   - Entidades, atributos, relaciones
   - Reglas de identidad y unicidad
   - Ciclo de vida / transiciones de estado
   - Supuestos de volumen de datos / escala

   Interacción y flujo de UX:
   - Recorridos / secuencias críticas del usuario
   - Estados de error / vacío / carga
   - Notas de accesibilidad o localización

   Atributos de calidad no funcionales:
   - Rendimiento (objetivos de latencia, throughput)
   - Escalabilidad (horizontal/vertical, límites)
   - Confiabilidad y disponibilidad (uptime, expectativas de recuperación)
   - Observabilidad (señales de logging, métricas, tracing)
   - Seguridad y privacidad (autenticación/autorización, protección de datos, supuestos de amenazas)
   - Restricciones de cumplimiento / regulatorias (si las hay)

   Integración y dependencias externas:
   - Servicios/APIs externos y modos de falla
   - Formatos de importación/exportación de datos
   - Supuestos de protocolo/versionado

   Casos límite y manejo de fallas:
   - Escenarios negativos
   - Limitación de tasa / throttling
   - Resolución de conflictos (por ejemplo, ediciones concurrentes)

   Restricciones y compromisos (tradeoffs):
   - Restricciones técnicas (lenguaje, almacenamiento, hosting)
   - Compromisos explícitos o alternativas rechazadas

   Terminología y consistencia:
   - Términos canónicos del glosario
   - Sinónimos evitados / términos obsoletos

   Señales de finalización:
   - Verificabilidad de los criterios de aceptación
   - Indicadores medibles al estilo Definición de Terminado

   Misceláneo / marcadores de posición:
   - Marcadores TODO / decisiones sin resolver
   - Adjetivos ambiguos ("robusto", "intuitivo") sin cuantificar

   Para cada categoría con estado Parcial o Faltante, agrega una oportunidad de pregunta candidata a menos que:
   - La aclaración no cambiaría materialmente la implementación ni la estrategia de validación
   - Es mejor diferir la información a la fase de planificación (anótalo internamente)

4. Genera (internamente) una cola priorizada de preguntas de aclaración candidatas (máximo 5). NO las muestres todas a la vez. Aplica estas restricciones:
    - Máximo de 5 preguntas en total durante toda la sesión.
    - Cada pregunta debe poder responderse con CUALQUIERA de estas opciones:
       - Una selección de opción múltiple breve (2 a 5 opciones distintas y mutuamente excluyentes), O
       - Una respuesta de una palabra / frase corta (restringe explícitamente: "Responde en <=5 palabras").
    - Incluye solo preguntas cuyas respuestas impacten materialmente en la arquitectura, el modelado de datos, la descomposición de tareas, el diseño de pruebas, el comportamiento de UX, la preparación operativa o la validación de cumplimiento.
    - Asegura un balance de cobertura de categorías: intenta cubrir primero las categorías sin resolver de mayor impacto; evita hacer dos preguntas de bajo impacto cuando un área de alto impacto sin resolver (por ejemplo, la postura de seguridad) queda pendiente.
    - Excluye preguntas ya respondidas, preferencias estilísticas triviales o detalles de ejecución de nivel de plan (a menos que bloqueen la corrección).
    - Favorece las aclaraciones que reduzcan el riesgo de retrabajo posterior o eviten pruebas de aceptación desalineadas.
    - Si quedan más de 5 categorías sin resolver, selecciona las 5 principales mediante la heurística (Impacto * Incertidumbre).

5. Bucle secuencial de preguntas (interactivo):
    - Presenta EXACTAMENTE UNA pregunta a la vez.
    - Para preguntas de opción múltiple:
       - **Analiza todas las opciones** y determina la **opción más adecuada** basándote en:
          - Mejores prácticas para el tipo de proyecto
          - Patrones comunes en implementaciones similares
          - Reducción de riesgo (seguridad, rendimiento, mantenibilidad)
          - Alineación con cualquier objetivo o restricción explícita del proyecto visible en la especificación
       - Presenta tu **opción recomendada de forma destacada** al principio con un razonamiento claro (1-2 oraciones explicando por qué es la mejor opción).
       - Formatéalo como: `**Recomendado:** Opción [X] - <razonamiento>`
       - Luego muestra todas las opciones como una tabla Markdown:

       | Opción | Descripción |
       |--------|-------------|
       | A | <Descripción de la opción A> |
       | B | <Descripción de la opción B> |
       | C | <Descripción de la opción C> (agrega D/E según sea necesario hasta 5) |
       | Corta | Proporciona una respuesta corta diferente (<=5 palabras) (Incluye solo si una alternativa de forma libre es apropiada) |

       - Después de la tabla, agrega: `Puedes responder con la letra de la opción (por ejemplo, "A"), aceptar la recomendación diciendo "sí" o "recomendada", o proporcionar tu propia respuesta corta.`
    - Para el estilo de respuesta corta (sin opciones discretas significativas):
       - Proporciona tu **respuesta sugerida** basada en las mejores prácticas y el contexto.
       - Formatéalo como: `**Sugerida:** <tu respuesta propuesta> - <razonamiento breve>`
       - Luego muestra: `Formato: Respuesta corta (<=5 palabras). Puedes aceptar la sugerencia diciendo "sí" o "sugerida", o proporcionar tu propia respuesta.`
    - Después de que el usuario responda:
       - Si el usuario responde "sí", "recomendada" o "sugerida", usa tu recomendación/sugerencia previamente indicada como respuesta.
       - En caso contrario, valida que la respuesta corresponda a una opción o cumpla con la restricción de <=5 palabras.
       - Si es ambigua, pide una desambiguación rápida (el conteo sigue perteneciendo a la misma pregunta; no avances).
       - Una vez que sea satisfactoria, regístrala en memoria de trabajo (aún no escribas en disco) y pasa a la siguiente pregunta en cola.
    - Deja de hacer preguntas cuando:
       - Todas las ambigüedades críticas se resuelvan antes de lo previsto (los elementos en cola restantes se vuelven innecesarios), O
       - El usuario señale finalización ("listo", "bien", "no más"), O
       - Alcances 5 preguntas realizadas.
    - Nunca reveles las preguntas en cola futuras por adelantado.
    - Si no existen preguntas válidas al inicio, reporta inmediatamente que no hay ambigüedades críticas.

6. Integración después de CADA respuesta aceptada (enfoque de actualización incremental):
    - Mantén una representación en memoria de la especificación (cargada una vez al inicio) más el contenido en bruto del archivo.
    - Para la primera respuesta integrada en esta sesión:
       - Asegúrate de que exista una sección `## Clarifications` (créala justo después de la sección contextual/de visión general de más alto nivel según la plantilla de la especificación si falta).
       - Debajo de ella, crea (si no está presente) un subencabezado `### Session YYYY-MM-DD` para hoy.
    - Agrega una línea de viñeta inmediatamente después de la aceptación: `- Q: <pregunta> → A: <respuesta final>`.
    - Luego aplica inmediatamente la aclaración a la(s) sección(es) más apropiada(s):
       - Ambigüedad funcional → Actualiza o agrega una viñeta en Requisitos Funcionales.
       - Interacción del usuario / distinción de actores → Actualiza la subsección de Historias de Usuario o Actores (si existe) con el rol, restricción o escenario aclarado.
       - Forma de los datos / entidades → Actualiza el Modelo de Datos (agrega campos, tipos, relaciones) preservando el orden; anota las restricciones agregadas de forma concisa.
       - Restricción no funcional → Agrega/modifica criterios medibles en Criterios de Éxito > Resultados Medibles (convierte el adjetivo vago en una métrica u objetivo explícito).
       - Caso límite / flujo negativo → Agrega una nueva viñeta bajo Casos Límite / Manejo de Errores (o crea dicha subsección si la plantilla provee un marcador de posición para ello).
       - Conflicto de terminología → Normaliza el término en toda la especificación; conserva el original solo si es necesario agregando `(anteriormente referido como "X")` una vez.
    - Si la aclaración invalida una declaración ambigua anterior, reemplaza esa declaración en lugar de duplicarla; no dejes texto contradictorio obsoleto.
    - Guarda el archivo de especificación DESPUÉS de cada integración para minimizar el riesgo de pérdida de contexto (sobrescritura atómica).
    - Preserva el formato: no reordenes secciones no relacionadas; mantén intacta la jerarquía de encabezados.
    - Mantén cada aclaración insertada mínima y verificable (evita la deriva narrativa).

7. Validación (realizada después de CADA escritura más un pase final):
   - La sesión de Clarifications contiene exactamente una viñeta por respuesta aceptada (sin duplicados).
   - Total de preguntas realizadas (aceptadas) ≤ 5.
   - Las secciones actualizadas no contienen marcadores de posición vagos persistentes que la nueva respuesta debía resolver.
   - No queda ninguna declaración anterior contradictoria (revisa que las alternativas ahora inválidas hayan sido eliminadas).
   - Estructura Markdown válida; los únicos encabezados nuevos permitidos son: `## Clarifications`, `### Session YYYY-MM-DD`.
   - Consistencia terminológica: se usa el mismo término canónico en todas las secciones actualizadas.

8. Escribe la especificación actualizada de vuelta en `FEATURE_SPEC`.

9. **Revalida la Lista de Verificación de Calidad de la Especificación** (si existe):
   - Verifica si `FEATURE_DIR/checklists/requirements.md` existe.
   - Si NO existe, omite este paso silenciosamente.
   - Si existe:
     1. Lee el archivo de la lista de verificación.
     2. Identifica todas las líneas de casilla de verificación de tipo lista de tareas de GitHub — líneas que coincidan con `- [ ]`, `- [x]`, o `- [X]` (sin distinguir mayúsculas/minúsculas, tolerante a espacios en blanco iniciales para elementos anidados) fuera de bloques de código. Ignora todo el demás contenido (encabezados, notas, viñetas que no son casillas, metadatos).
     3. Para cada línea de casilla, registra su estado de marcador actual (marcada o no marcada) y el texto del elemento en una lista de instantánea previa.
     4. Reevalúa cada elemento de casilla contra la especificación **actualizada** (la versión recién guardada en el paso 7).
     5. Para cada elemento de casilla, actualiza solo si el estado marcado/no marcado realmente cambia:
        - Si el elemento ahora pasa y estaba sin marcar: cambia `[ ]` a `[x]`.
        - Si el elemento ahora falla y estaba marcado: cambia `[x]`/`[X]` a `[ ]`.
        - Si el estado no cambia: deja el marcador tal cual (preserva las mayúsculas/minúsculas existentes para evitar diffs cosméticos).
     6. Guarda el archivo de la lista de verificación actualizado. **Alterna solo la parte del marcador `[ ]`/`[x]` de las líneas de casilla cuyo estado haya cambiado.** Todo el demás contenido del archivo — encabezados, metadatos, notas, orden de líneas, espacios en blanco — debe permanecer sin cambios para evitar diffs ruidosos.
     7. Compara la instantánea previa con el estado actual para calcular tres listas para el Reporte de Finalización:
        - **Recién aprobados**: elementos que cambiaron de no marcados a marcados.
        - **Regresiones**: elementos que cambiaron de marcados a no marcados.
        - **Aún sin marcar**: elementos que permanecen sin marcar.
     8. Registra los conteos de aprobación antes/después como elementos de casilla marcados/total (por ejemplo, "12/16 → 15/16 elementos aprobados").

Reglas de comportamiento:

- Si no se encuentran ambigüedades significativas (o todas las posibles preguntas serían de bajo impacto), responde: "No se detectaron ambigüedades críticas que merezcan una aclaración formal." y sugiere continuar.
- Si falta el archivo de especificación, indica al usuario que ejecute primero `/speckit-specify` (no crees una nueva especificación aquí).
- Nunca superes las 5 preguntas totales realizadas (los reintentos de aclaración de una sola pregunta no cuentan como preguntas nuevas).
- Evita preguntas especulativas sobre la pila tecnológica a menos que su ausencia bloquee la claridad funcional.
- Respeta las señales de terminación anticipada del usuario ("detente", "listo", "continúa").
- Si no se hace ninguna pregunta debido a cobertura completa, muestra un resumen de cobertura compacto (todas las categorías Claras) y luego sugiere avanzar.
- Si se alcanza la cuota con categorías de alto impacto sin resolver, márcalas explícitamente bajo Diferidas con la justificación.

Contexto para priorización: $ARGUMENTS

## Hooks Obligatorios de Post-Ejecución

**DEBES completar esta sección antes de reportar la finalización al usuario.**

Verifica si `.specify/extensions.yml` existe en la raíz del proyecto.
- Si no existe, o no hay hooks registrados bajo `hooks.after_clarify`, salta al Reporte de Finalización.
- Si existe, léelo y busca entradas bajo la clave `hooks.after_clarify`.
- Si el YAML no se puede parsear o no es válido, omite la verificación de hooks silenciosamente y continúa al Reporte de Finalización.
- Filtra los hooks donde `enabled` sea explícitamente `false`. Trata los hooks sin un campo `enabled` como habilitados por defecto.
- Para cada hook restante, NO intentes interpretar ni evaluar las expresiones `condition` del hook:
  - Si el hook no tiene campo `condition`, o está vacío/nulo, trata el hook como ejecutable
  - Si el hook define un `condition` no vacío, omite el hook y deja la evaluación de la condición a la implementación de HookExecutor
- Al construir comandos slash a partir de los nombres de comando del hook, reemplaza los puntos (`.`) por guiones (`-`). Por ejemplo, `speckit.git.commit` → `/speckit-git-commit`.
- Para cada hook ejecutable, produce lo siguiente según su bandera `optional`:
  - **Hook obligatorio** (`optional: false`) — **DEBES emitir `EXECUTE_COMMAND:` para cada hook obligatorio**:
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    Después de emitir el bloque anterior DEBES invocar realmente el hook y esperar a que termine antes de continuar. Ejecútalo de la misma forma en que ejecutarías el comando tú mismo en este agente/sesión (la invocación puede diferir del id literal `{command}` mostrado arriba, por ejemplo un agente en modo skills lo ejecuta como `/skill:speckit-...` o `$speckit-...`). Emitir el bloque por sí solo no ejecuta el hook.
  - **Hook opcional** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```

## Reporte de Finalización

Reporta la finalización (después de que termine el bucle de preguntas o de una terminación anticipada):
- Número de preguntas realizadas y respondidas.
- Ruta a la especificación actualizada.
- Secciones tocadas (lista de nombres).
- Estado de la lista de verificación de calidad de la especificación (si `FEATURE_DIR/checklists/requirements.md` fue revalidada): muestra los conteos de aprobación antes/después (por ejemplo, "Spec Quality Checklist: 12/16 → 15/16 items passing") y lista cualquier elemento que haya cambiado de estado — tanto los recién marcados (no marcado → marcado) como cualquier regresión (marcado → no marcado). Si quedan elementos sin marcar, lístalos como áreas que necesitan atención.
- Tabla de resumen de cobertura que liste cada categoría de la taxonomía con Estado: Resuelta (era Parcial/Faltante y se abordó), Diferida (excede la cuota de preguntas o es más adecuada para la planificación), Clara (ya suficiente), Pendiente (aún Parcial/Faltante pero de bajo impacto).
- Si queda alguna Pendiente o Diferida, recomienda si continuar con `/speckit-plan` o ejecutar `/speckit-clarify` nuevamente más adelante después del plan.
- Comando sugerido a continuación.

## Cuándo se considera Hecho

- [ ] Ambigüedades de la especificación identificadas y aclaraciones integradas en el archivo de especificación
- [ ] Lista de verificación de calidad de la especificación revalidada contra la especificación actualizada (si `FEATURE_DIR/checklists/requirements.md` existe)
- [ ] Hooks de extensión despachados u omitidos según las reglas en Hooks Obligatorios de Post-Ejecución arriba
- [ ] Finalización reportada al usuario con preguntas respondidas, secciones tocadas, estado de la lista de verificación y resumen de cobertura
