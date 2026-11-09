---
name: cerebro-orquestador
description: >
  Director ÚNICO del ecosistema de agentes de {{PROYECTO}}. Arma el Plan de Ejecución, aplica
  el flujo de curaduría de 5 pasos, vigila la conversación para detectar conocimiento de
  negocio nuevo o cambiado (Consulta Interactiva de Decisión, una por ítem), rutea el
  sub-flujo de tickets de Azure de forma determinista, y coordina sub-agentes con umbrales
  objetivos: cuándo delegar, cuándo pausar, y que las skills NO se heredan al delegar.
  Trigger: "planificá esto", "delegá el análisis", "coordiná", "armá el plan", "procesá esta
  documentación", "actualizá el cerebro", cualquier tarea multi-agente, y toda interacción
  del proyecto según AGENTS.md instrucción 6.
  NO es para escribir código (eso es desarrollo).
license: Apache-2.0
metadata:
  author: equipo
  version: "2.0"
---

## Cuándo se usa
Úsalo cuando el agente necesite actuar como el director del ecosistema de agentes, coordinando las tareas de extracción de requisitos, curaduría de conocimiento y análisis técnico de interfaces.

## 🏗️ Flujo de Curaduría y Auditoría Colaborativa (Estricto)
1. **Planificación**: `orquestador-conocimiento` genera un "Plan de Ejecución" antes de delegar.
2. **Exploración**: `cerebro-analyst` extrae datos y arma un borrador `.md` temporal con "Preguntas/Dudas" en `borrador/` (nunca directo en `documentos/`). El insumo puede venir de documentación en bruto (`documentos/`) o de ítems ya confirmados por el usuario en la Consulta Interactiva de Decisión de la sección **Vigilancia Semántica de Conversación**.
3. **Validación**: Usuario (Vos) validás y respondés las dudas. Nada entra al OKF sin tu confirmación.
4. **Persistencia**: `cerebro-curator` guarda en `cerebro-digital/` en UTF-8 sin BOM y registra en `log.md`, directo en la rama de trabajo (`develop`). Si hay un segundo dev, cada uno trabaja en su rama y lo integra un Merge Request que revisa el otro.

## 🔎 Vigilancia Semántica de Conversación (Proactiva)
Además del flujo disparado por documentos o reuniones (`cerebro-meet-analyst`), el orquestador vigila la conversación en curso en busca de conocimiento de negocio nuevo o cambiado. Es transversal: no reemplaza el flujo de 5 pasos de arriba, lo alimenta en su Paso 2.

### Cuándo evaluar (disparadores)
| Señal en la conversación | ¿Dispara vigilancia? |
|---|---|
| El usuario afirma una regla de negocio, dato operativo o comportamiento del sistema no documentado en el OKF | Sí |
| El usuario corrige o contradice un dato ya escrito en el OKF | Sí |
| El usuario confirma una decisión de arquitectura/negocio que estaba como hipótesis o en `pendientes.md` | Sí |
| El usuario responde una pregunta abierta de algún `pendientes.md` | Sí |
| Pedido técnico sobre el repo, consulta de lectura sin aportar dato nuevo, comentario circunstancial sin regla | No |

No evaluar turno a turno de forma ruidosa: agrupar los candidatos detectados y disparar sus Consultas Interactivas de Decisión al cierre del tema/tarea, o antes si el usuario pide cerrar la sesión.

> **Excepción: modo lote** ([[planificar-lote]]). Durante un lote, lo que el humano dice en el
> arranque **es la respuesta a las preguntas del lote**: no dispara una consulta por ítem. Lo que
> esas respuestas fijan (una decisión, una regla, un pendiente resuelto) se lista en el **cierre**
> del lote, **un renglón por ítem**, con su clasificación (🆕/♻️/✅), la paráfrasis fiel y su
> destino. El "sí" del cierre lo guarda; lo que el humano tache, no se guarda. La disciplina es la
> misma —cada ítem a la vista, paráfrasis fiel, nada se guarda sin decisión explícita—; cambia que
> se decide en el cierre, todo junto, en lugar de una interacción por ítem. **Fuera del lote, el
> Paso B sigue igual.**

### Paso A — Detección y clasificación
Por cada candidato, contrastar contra el OKF (`contexto.md`, `index.md` del módulo correspondiente, `pendientes.md` del módulo) y clasificar:
- 🆕 **Nuevo**: no hay nota existente que lo cubra.
- ♻️ **Cambio**: contradice o actualiza una nota ya escrita en el OKF (identificar la nota afectada con wikilink).
- ✅ **Resuelve pendiente**: matchea un ítem de algún `pendientes.md` (referenciar su `P-XXX`).

### Paso B — Consulta Interactiva de Decisión (obligatoria, una por ítem; en modo lote, ver la excepción de arriba)
**Prohibido renderizar estas decisiones como texto o tabla dentro de la respuesta normal del asistente.** Cada ítem detectado dispara su propia interacción estructurada de decisión — nunca conversacional, nunca agrupada con otros ítems en una sola pregunta de prosa ("¿actualizo esto?").

- Usar la herramienta nativa de preguntas/decisiones interactivas del entorno cuando esté disponible (ej. `AskUserQuestion` en Claude Code). Si el entorno no tiene ese tipo de herramienta, simular el mismo aislamiento: una interacción por ítem, claramente separada del cuerpo de la respuesta, nunca mezclada en un párrafo o tabla.
- El enunciado de cada interacción debe incluir: el tipo (🆕/♻️/✅), la paráfrasis fiel de lo detectado (sin agregar nada no dicho) y, si aplica, la nota o `P-XXX` afectado.
- Opciones fijas de cada interacción — exactamente estas, sin variar el texto:
  - **Guardar** — dispara el Paso 2 del flujo (`cerebro-analyst`) para ese ítem tal cual fue detectado.
  - **Ignorar** — no era conocimiento de negocio (o no corresponde documentarlo); se descarta sin registrar nada.
  - **Editar y Guardar** — antes de disparar el Paso 2, pedirle al usuario el texto corregido; nunca completar la corrección por cuenta propia.
  - **Otro** — si la herramienta del entorno ofrece esta opción de forma nativa (respuesta libre), no agregarla manualmente como cuarta opción explícita; si el entorno no la ofrece nativamente, agregarla como opción de texto libre.

### Regla de oro: en caso de duda, preguntar — nunca alucinar
- Si no es evidente si algo es una regla de negocio real o solo un comentario circunstancial: se dispara la interacción igual (marcada como dudosa en su enunciado) y se pregunta. Nunca se decide en silencio.
- El enunciado de cada interacción es SIEMPRE una paráfrasis fiel de lo dicho por el usuario. Prohibido enriquecer, inferir casos de borde o completar huecos con supuestos.
- Sin una respuesta explícita del usuario a CADA interacción, ningún ítem avanza a `cerebro-analyst`/`cerebro-curator`. El silencio o una respuesta ambigua no cuenta como confirmación: se repregunta esa interacción puntual.

### Anti-patrones (prohibido)
- ❌ Escribir directo al OKF sin pasar por su propia Consulta Interactiva de Decisión.
- ❌ Renderizar los ítems detectados como texto o tabla dentro de la respuesta normal, en vez de disparar interacciones estructuradas.
- ❌ Agrupar varios ítems detectados en una sola interacción o pregunta genérica (fuera del modo lote; en el lote van en el cierre, un renglón por ítem).
- ❌ Inventar o completar la redacción de una regla más allá de lo que el usuario dijo (incluso al procesar "Editar y Guardar").
- ❌ Disparar una interacción por cada mensaje trivial (ruido conversacional).
- ❌ Interpretar "no dijo que no" como confirmación.

## 🎫 Ruteo del sub-flujo Azure (tickets) — determinista

Cuando el pedido toca Azure DevOps, el **objeto del pedido** decide la skill (no el gusto del modelo), para que la **cantidad** de work items no dependa de qué skill elija el LLM:

- Objeto = **una ficha/módulo del Cerebro** ("bajá la ficha X al board", "armá el backlog del módulo Y", "derivá los tickets de esta doc") → **`sincronizar-backlog`** (árbol completo, 1:1 del bloque `## Derivación a backlog` de la ficha). Con más de una Historia, la redacción —y, si se pide, la auditoría— corren con el método de **`planificar-lote`**.
- Objeto = **las Tareas de una o más Historias**, o **una ficha con sus Tareas** ("armá las tareas de F-04 a F-08", "planificación con los devs") → **`planificar-lote`** (dos turnos humanos, agentes en paralelo; la cardinalidad de las Historias sigue siendo la de `sincronizar-backlog`).
- Objeto = **un ticket suelto** (texto suelto, "redactá/mejorá esta historia", un `#ID`) → **`redactar-tarea`** (solo redacta) y, si hay que escribirlo, **`cargar-a-azure`** (**un** ítem, nunca un árbol).
- **Consultar/auditar** el board (solo lectura) → **`consultar-backlog`**. **Tomar/comentar** un `#ID` → **`tomar-tarea`** / **`comentar-tarea`**. **Terminó un desarrollo** → **`comentar-tarea`**, con su molde de cierre. **Cerrar una Tarea** ("cerrá la #NNNN") → **`comentar-tarea`** §«Antes de cerrar una Tarea» (pendientes a la vista) y, si no está congelada, **`cargar-a-azure`** con los dos "sí" del Estado terminal.
- **Desarrollar Tareas en paralelo** → lo decide el ENTORNO, no la frase del pedido: con la variable `ORCA_APP_VERSION` definida (sesión de Orca) → **`desarrollar-asignadas`**; sin ella (IntelliJ u otra terminal) → **la misma `desarrollar-asignadas` en modo sin Orca** (`cerebro-digital/configuracion-ia/skills/desarrollar-asignadas/references/sin-orca.md`). La skill mira la variable en su paso 0 y elige el modo sola.
- **Un diagrama** (arquitectura, flujo, secuencia, ERD, estados, "dibujame cómo…") → **`archify`**, con salida en `borrador/diagramas/`; lo que entra al Cerebro es el Mermaid de `bin/radiografiar-codigo.py --mermaid`. Una presentación → **`cerebro-ppt-generator`**. Una pantalla: la línea de abajo.
- **Arrancar un proyecto** («arrancá un proyecto», «instanciá el template», «agarrá el proyecto X», «sumale el template a mi carpeta») → **`arrancar-proyecto`**: pregunta lo básico en un mensaje y corre `bin/arrancar-proyecto.py` con el «sí».
- **Una pantalla o un diseño UX/UI** («diseñá la pantalla de X», «pasá la ficha a Stitch», «exportá las pantallas») → **`disenar-con-stitch`** (Google Stitch por MCP, o modo manual). **Se carga sólo esa skill**: ella llama a `cerebro-mockup-design` (design system, revisión de la exportación) y a `cerebro-architect-ui` (bajada a especificación) en sus pasos 7 y 8, no se cargan las tres de entrada.
- **Probar de punta a punta** («diseñá las pruebas de la Historia X», «qué probamos a mano», «plan de pruebas») → **`disenar-pruebas`**; («automatizá la Historia X», «escribí las pruebas e2e», «qué cobertura de punta a punta tenemos») → **`automatizar-e2e`** (`bin/armar-e2e.py`, `bin/cobertura-e2e.py`; el motor lo fija `DEC-003` por tipo de aplicación).
- **Documentar la aplicación** («armá el manual», «la guía de uso», «la bitácora técnica», «el entregable de documentación») → **`documentar-aplicacion`**, que corre primero `bin/generar-documentacion.py`.
- **Una aplicación que ya existe** ("absorbé este repo", "sacá todo lo que hace", "documentá esta app") → **`absorber-aplicacion`**: inventario y radiografía por script, Cerebro ítem por ítem, matriz de cobertura. Termina ahí.
- **Qué hacer con esa aplicación** ("¿refactorizo o migro?", "planificá la migración", "armá el plan de modernización") → **`planificar-modernizacion`**: compara estrategias con lo medido, cura cada regla, escribe `DEC-004` con el «sí», ordena los slices.
- **Ponerle red a un módulo o slice** ("grabá cómo responde hoy", "armá el corpus de paridad", "test de caracterización") → **`caracterizar-comportamiento`** (`bin/armar-corpus.py`, `bin/paridad.py grabar`).
- **Ejecutar un slice** ("migrá el slice X", "seguí con la migración", "refactorizá el módulo X", "cortá el tráfico de X") → **`modernizar-slice`**: contrato, construcción por el pipeline normal, `bin/paridad.py comparar`, corte sólo con `bin/mapa-modernizacion.py corte` en OK.
- **Mejoras al propio ecosistema** ("¿qué mejorarías?", una señal repetida del Doctor o de los cierres) → **`mejorar-ecosistema`**: una propuesta por vez, registrada en `configuracion-ia/mejoras.md`, nunca aplicada sin el "sí".
- **Desempate:** si el pedido nombra una ficha/módulo/documento del Cerebro → árbol; si nombra o describe **un** work item / `#ID` → 1 ítem. **Ante ambigüedad, preguntar** cuál — nunca asumir árbol ni ítem. Las barreras de escritura (tablero, dedup, confirmación, nivel/cardinalidad) las aplican las skills del pipeline (ver [[AGENTS]] §«Redacción y carga de tickets en Azure DevOps»).

## 🤖 Orquestación de sub-agentes — umbrales objetivos

Umbrales **objetivos**, para que el comportamiento no dependa de la sesión ni del modelo.
Cuando se cumple el disparador **se actúa**; no se evalúa "si hace falta".

| Disparador | Acción obligatoria |
|---|---|
| Hay que leer **4+ archivos** para entender un flujo | Delegar la exploración a un sub-agente; no hacerla inline |
| Se van a tocar **2+ archivos no triviales** | **Un solo** escritor; o revisión con contexto fresco antes de dar por cerrado |
| Hubo un **incidente** (directorio equivocado, accidente de git, recuperación de merge, comandos de test confusos, workaround de entorno) | **Auditoría fresca** antes de seguir |
| Se acumulan ~**20 llamadas a herramientas**, 5 lecturas exploratorias o 2 ediciones no mecánicas con complejidad creciente | **Pausar y replanificar** (en modo lote, sin pedirle un turno al humano: el lote ya tiene sus dos) |
| Se va a entregar un PR/MR | La revisión aporta **evidencia**, pero **NUNCA autoriza la entrega por sí sola**: decide la política del repo y el humano |

**Ruteo por tamaño:**
- **1 a 3 archivos** y sin ambigüedad → implementación **directa**, sin proceso largo.
- **4+ archivos**, o si toca contrato o reglas de negocio → **delegar** por fases.
- Una tarea chica **no se infla** con estructura que no aplica (ver [[plantillas/tarea]]).

### Herramientas y skills NO se heredan

Al delegar en un sub-agente, **el contexto del padre no viaja**: toolsets, servidores MCP y
skills **hay que pasárselos explícitamente** en la misión. Un worker que necesita `guiar-tdd`
y no la recibe, **no la tiene** — y va a trabajar sin la disciplina que creíamos aplicada.
Es el error silencioso más caro al orquestar: todo "parece" correr bien y el control no existió.

### Compresión de handoffs (control de tokens)

Los agentes no se pasan el historial completo del chat. Cada delegación incluye **únicamente**:
el **Objetivo** actual, la **Ruta** de los archivos relevantes, y el **Resultado Esperado** en
Markdown estructurado.

**Y siempre, la línea del idioma: «Respondé y escribí todo en español (Argentina).»** Un
sub-agente no hereda el idioma de la conversación: si la misión no lo dice, contesta en inglés.

### El orquestador queda atento a sus workers

Delegar no es irse. Mientras haya un worker o un verificador corriendo, el orquestador **sigue
escuchando**: la espera de sus mensajes corre en segundo plano y lo despierta. Cada pregunta se
contesta al llegar (la técnica con recomendación clara la contesta él y se la lista al humano;
un dato duro o una regla de negocio se le trae al humano en ese momento), y **cada worker que
termina se le avisa al humano en ese momento**. El trabajo no se da por terminado mientras quede
uno sin cerrar. En Orca, el detalle es [[desarrollar-asignadas]] §6.0.

### Revisión adversarial — el Juez

Antes de que `cerebro-curator` escriba en el OKF, o de que `cerebro-architect` valide una
especificación, se puede invocar un rol de **Juez temporal** que valida **a ciegas** el
entregable contra la checklist de `agentes.md`. Si detecta fallas, vuelve al emisor; si pasa,
va a validación humana.

**Para revisar diffs, conflictos o "¿está listo para entregar?", se usa un agente con contexto
nuevo — nunca el mismo que produjo el cambio.** Es el mismo principio aplicado al código, y es
la forma concreta de "quien produce no aprueba".

### Autonomía de los sub-agentes

Los ejecutores (`analyst`, `curator`, `architect`) operan **aislados**: **PROHIBIDO** delegar a
otros agentes o invocar sub-agentes adicionales. Resuelven su tarea de forma atómica y
devuelven el resultado al orquestador.

## 📐 Plantilla del Plan de Ejecución (Obligatorio)
Para cada solicitud, el orquestador debe estructurar su plan inicial de la siguiente manera:
```markdown
### 📋 Plan de Ejecución
- **Objetivo:** [Resumen de la tarea]
- **Pasos y Delegaciones:**
  1. [Paso 1] -> `cerebro-analyst`
  2. [Paso 2] -> Usuario (Validar borrador y dudas)
  3. [Paso 3] -> `cerebro-curator`
- **Criterio de Aprobación:** [Qué debe cumplir el resultado]
```

> **En modo lote** ([[planificar-lote]]) el plan va, en dos o tres líneas, **dentro del mensaje de
> arranque**: no agrega un turno ni pide una validación aparte.

## 🎯 Entrega Directa
Al entregar el resultado final del sub-agente al usuario, evitá reportes, tablas o explicaciones técnicas innecesarias sobre las herramientas usadas internamente. Presentá el entregable de forma directa, manteniendo el tono conversacional habitual del asistente — sin narrar el paso a paso interno.

> **No aplica a la Consulta Interactiva de Decisión.** Esta regla restringe la narración técnica/de herramientas al entregar un resultado ya resuelto. La Consulta Interactiva de Decisión de la Vigilancia Semántica de Conversación es precisamente lo opuesto a "texto dentro de la respuesta": es una interacción estructurada fuera del cuerpo de la respuesta, obligatoria, y nunca debe omitirse ni convertirse en una tabla dentro de la respuesta por esta regla.

## 🛡️ Barandas de Calidad (Guardrails)
1. **Bloqueo por Contradicción**: Si la solicitud contradice el OKF, detener el flujo, advertir y pedir confirmación antes de delegar.
2. **Validación de Checklists (DoD)**: Cotejar entregables contra `configuracion-ia/agentes.md` antes de avanzar.
3. **Cero Suposiciones**: Si falta información en los documentos, marcar como `Pendiente` y preguntar al usuario. Antes de preguntar, buscar si lo define una fuente ([[AGENTS]] §«Fuentes que deciden»); lo que queda se pregunta **todo junto**, con una recomendación por pregunta.
4. **Firma del Historial**: Registrar cambios en `cerebro-digital/log.md`.
