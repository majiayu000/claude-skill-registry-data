---
name: redactar-tarea
description: >-
  Convertir un ticket POBRE (texto suelto, "ver adjunto", un link, o el ID de una
  tarjeta de Azure DevOps) en un work item PROFESIONAL, detallado y listo para
  pegar o crear en el board. Usar cuando se pida "redactá/mejorá esta historia",
  "escribí el ticket", "hacé los criterios de aceptación", "pasá esto a Gherkin",
  "convertí este bug en un ticket", "está lista para el sprint / cumple el DoR",
  "/redactar-tarea". Decide primero el TIPO (Historia / Tarea / Bug / Habilitador
  técnico / Spike). TODO en español (Argentina), Gherkin incluido
  (Dado/Cuando/Entonces). PHI PROHIBIDO (marcadores). NO inventa: lo faltante se
  marca "pendiente" y se pregunta, esperando confirmación humana. SOLO redacta:
  no escribe en Azure (para eso está la skill cargar-a-azure).
---

# Redactar tarea

> **Tablero local (`DEC-006`):** si el proyecto usa el tablero local, «el board» es `cerebro-digital/<modulo>/backlog/`
> y se opera con `bin/tablero-local.py`, con los mismos GATEs y sin MCP (detalle: `backlog/README.md` del módulo).
> Con Azure DevOps, Jira u otro tablero, las operaciones se traducen con la tabla de `integracion-azure-mcp/00-index.md`.

Convierte una entrada pobre en un work item profesional, en español, listo para
pegar campo por campo en el board. Esta skill **solo redacta**: deja el texto
pegable. Escribir en el board es otra skill: [[cargar-a-azure]].

## Regla de oro (cultura del equipo)

- **NO INVENTAR.** Lo que no está confirmado se marca como **pendiente** y se
  pregunta al usuario. Nunca completar datos de negocio, actores, reglas o
  valores por suposición.
- **Redactá EXACTAMENTE lo pedido: un ítem.** Si piden una tarea, redactás **una**;
  no generás varias historias ni un árbol. Bajar una ficha/módulo entero al board
  es otra skill ([[sincronizar-backlog]]).
- **PHI PROHIBIDO.** Nada de datos personales sensibles o personales reales. Usar marcadores:
  `<persona>`, `<documento>`, `<identificador>`, `<dato-sensible>`, `<telefono>`, `<direccion>`.
- **Respetar la provenance.** Si hay fuentes con distinta autoridad, gana la de
  mayor jerarquía; ante conflicto, se anota el desvío, no se elige en silencio.
- **Lo definido no se pregunta.** Lo que ya definen el Cerebro, la maqueta vigente o una
  respuesta anterior del humano se aplica y se lista; una recomendación técnica clara, también
  ([[AGENTS]] §«Fuentes que deciden»). Lo que queda se pregunta **todo junto**, numerado y con
  una recomendación por pregunta.
- **Un solo tag temático, techo duro.** El campo Etiquetas lleva **una** etiqueta
  (el tema, sin prefijo, kebab-case) — nunca el nombre del producto/repo (`<producto>`,
  `modulo-ejemplo`) ni el slice/sub-flujo como tag aparte. Detalle:
  [[organizacion-y-trazabilidad]] §1.
- **Silencio al entregar.** Al terminar, devolver el ticket pegable e ir al grano;
  sin relleno ni auto-elogio.
- **Español (Argentina)** en todo, incluido el Gherkin.

## Flujo

### 1. Conseguir la entrada
- Si el usuario pasó **texto**, se trabaja con ese texto.
- Si pasó un **ID de Azure** (p. ej. `#12345`), leerlo **solo lectura** con el MCP
  (`get_work_item`, y `get_work_item_comments` si hace falta el hilo). Ver
  [[integracion-azure-mcp/00-index]]. Si no hay MCP configurado, pedir al usuario
  que pegue el contenido.

### 2. Decidir el TIPO primero
Antes de redactar, clasificar. Es la decisión que gobierna la plantilla y los campos
(complementa la Regla de oro «el tipo se decide PRIMERO»). Para que el **mismo insumo
dé siempre el mismo tipo** — y no varíe según el LLM — elegí el **primer renglón cuya
*señal objetiva* se cumpla**; la señal es verificable, no depende de gusto:

| Tipo | Señal objetiva (verificable) | Plantilla |
|---|---|---|
| Bug | Comportamiento **observado ≠ esperado** sobre algo **YA existente**, donde el "esperado" es un comportamiento **previamente especificado / una regla ya definida** (regresión o incumplimiento) — **NO** una mejora nueva; se pueden escribir esperado, obtenido y pasos para reproducir. *(Una mejora sobre lo existente es Historia, no Bug.)* | [[plantillas/bug]] |
| Historia de usuario | **Flujo de negocio con valor para un rol** identificable (incluye **mejoras/altas** de comportamiento); se escribe "Como `<rol>` quiero `<qué>` para `<para qué>`" y se verifica con criterios de aceptación (Gherkin). | [[plantillas/historia-de-usuario]] |
| Habilitador técnico / Spike | Trabajo técnico **sin valor de usuario directo** (deuda, infra, migración) **y que NO es el desglose de una Historia** (eso es Tarea), **o** investigación **time-boxed** con una pregunta a responder (Spike); no produce comportamiento de negocio observable. | [[plantillas/habilitador-tecnico]] |
| Tarea (dev/planning) | **Desglose técnico de UNA Historia** ya existente (con Parent Historia); sin valor de usuario propio. **Solo** con contexto **dev/planning declarado** (ver nota abajo). | [[plantillas/tarea]] |
| Épica / Característica | Agrupadores de alcance mayor; **no se eligen para un ítem suelto** — salen de la derivación de cardinalidad (`[S-nn]`→Épica, `[C-nn]`→Feature). | [[plantillas/epica]] · [[plantillas/caracteristica]] |

Si aun así el tipo es ambiguo, proponer uno y **preguntar** antes de seguir.

> **Tarea = momento dev/planning.** Si el pedido es **crear una Tarea nueva** y **no** viene declarado un contexto de desarrollo/planning explícito (p. ej. "soy dev", "estamos en planning"), **no la cierres como Tarea**: proponé la **Historia** que la engloba, o pedí esa declaración. **El pedido mismo no es la declaración**: «desglosá / creá las tareas de la Historia #NNNN» no alcanza. La pregunta del nivel (o la propuesta de la Historia) **cierra el turno**: no se adjunta un borrador de la Tarea «mientras tanto», **ni el molde vacío** de cómo quedaría. **Corregir una Tarea que ya existe no pasa por acá**: su nivel ya se decidió al crearla (ver el arreglo que pide [[auditar-tarea]]). El default es funcional (hasta Historia); las Tareas técnicas las arma Desarrollo.

### 3. Redactar según la plantilla
Tomar la estructura del dominio y las convenciones de [[conocimiento/00-index]]
(glosario, roles, DoR/DoD, estimación, RNF, antipatrones) y llenar la plantilla
del tipo elegido.

- **Historia (los 4 bloques, ver [[plantillas/historia-de-usuario]]):** (1)
  **Funcionalidad** "Como `<rol>` quiero `<qué>` para `<para qué>`" + contexto +
  alcance; (2) **Criterios de aceptación** en Gherkin español (Dado/Cuando/Entonces);
  (3) **Reglas de negocio** con **referencia al OKF** (ruta#ancla) por cada `[RN-…]`;
  (4) **Casos de uso** (alcance de pruebas, mapeados a `[RN-…]`). Siempre la línea
  **Documento fuente**. Y las **Notas para QA** con sus cinco líneas fijas (pantalla y ruta, rol y usuario de
  prueba, datos iniciales con marcadores, identificadores estables que expone el front, ambiente): es lo que la
  prueba de punta a punta necesita y el Gherkin no dice; lo que no se sabe va `⚠`, no se inventa. Debe servir a
  Desarrollo y a Testing sin que nadie tenga que volver a preguntar.
- **Bug:** el cuerpo lleve SIEMPRE los tres bloques:
  1. **Resultado esperado** — qué debería pasar.
  2. **Resultado obtenido** — qué pasa hoy.
  3. **Por qué / contexto** — pasos para reproducir, ambiente, alcance.
  Más severidad/gravedad si el board la usa.
- **Tarea / Habilitador (el detalle que necesita el dev, según la complejidad):**
  siempre el **objetivo**, el **alcance**, la **Definición de terminado** y el
  **Parent**. **Solo para desarrollo pesado** sumá el **vertical slice** + **capa**
  (`api`/`application`/`domain`/`infra`, o front), el **Contrato técnico (entrada/salida)**
  —que para capa `api` se escribe como **fragmento OpenAPI (YAML), no en prosa**—, la
  **especificación cerrada (SDD)** con sus `[RN-…]`, la **lista de "Tests a escribir
  PRIMERO" (TDD test-first)** y si **requiere test de integración**. Para una tarea
  chica **no infles** con secciones que no aplican (ver [[plantillas/tarea]]).

### 3.1 DoR de la Tarea — "lista para desarrollar" (bloqueante)
Una **Tarea** de capa `api`/`application`/`domain` (algo que otro código va a **llamar**)
**no se entrega como "lista"** sin estas cuatro piezas cerradas:
- **Contrato técnico (entrada/salida) cerrado** — así se llama la sección en
  [[plantillas/tarea]]. Para capa `api` va como **fragmento OpenAPI (YAML) parseable**;
  si no es HTTP, la firma entrada/salida. Es lo que después `armar-swagger` consolida y
  el dev implementa.
- **Especificación cerrada (SDD)** con la **tabla de Escenarios de la Historia** que
  esta Tarea cubre, y **qué test verifica cada uno**. Es la **bisagra entre BDD y TDD**: la
  Historia trae el Gherkin (loop externo), la Tarea trae los tests (loop interno), y sin esa
  tabla los dos loops quedan sueltos — nadie puede responder si los tests de la Tarea
  alcanzan para cerrar un Escenario. Los títulos de Escenario se copian **textuales** del
  campo Criterios de aceptación del padre.
- **Lista de "Tests a escribir PRIMERO" (test-first), numerada** — un caso por cada validación y por
  cada fila de "Casos de error". Es lo que después `guiar-tdd` ejecuta en Red-Green-Refactor.
  Va numerada porque la tabla de Escenarios los referencia por número. **Una línea por test**,
  y **30 tests o menos**: si la lista completa no entra, la Tarea es demasiado grande y se
  parte, no se recorta la lista ([[plantillas/tarea]] §«Tamaño y forma»). **Cada ítem enumera un solo
  comportamiento**; si trae dos del mismo contrato (una lista que filtra y la misma con una bandera que no
  filtra), se escriben como dos ítems o se dice en el ítem que son dos aserciones del mismo test. Un ítem que
  va a **nacer verde** por construcción (una idempotencia que ya da el esqueleto, un caso que cubre el verde
  mínimo de otro) se declara **guardarraíl** en la lista, para que el worker no tenga que descubrirlo. Si la
  Tarea toca una **migración de base**, el contrato dice qué pasa con las filas viejas y con las que el código
  viejo inserta durante la ventana (default o `NULL`, y cómo las lee el repositorio), y cómo se arma en un test
  una base «hasta la versión n» (helper de test o parámetro del migrador).
- **Bloque "Modos de falla evaluados"** — una línea por familia (**estado, concurrencia,
  autorización, dependencia caída, límites, idempotencia**), y cada una **o cubierta por un
  test de arriba, o descartada con su motivo escrito**. «Cubierta por el test n» vale sólo si el ítem n
  **enumera ese caso**; si no lo enumera, el caso es un ítem nuevo de la lista, no una nota al pie. Nunca ausente: un «no aplica porque…»
  es una afirmación auditable, el silencio no lo es. Es el bloque que evita que una familia
  entera se escape sin que nadie lo note — en las tres primeras Tareas reales del proyecto de origen, que
  no lo tenían, quedaron **trece familias en silencio** entre las tres, incluida la
  autorización de un endpoint que devuelve datos sensibles. Lo chequea [[auditar-tarea]]
  (chequeo 11).

**Dos chequeos de coherencia, además, antes de dar la Tarea por lista:**
- Si el Alcance técnico dice «Requiere test de integración: **sí**», tiene que haber
  **un test de integración en la lista, una subtarea que lo escriba y un ítem en el DoD**.
  Declararlo y no pedirlo deja que el dev cierre con puros dobles.
- **El campo Esfuerzo original nunca queda nulo en silencio**: si no hay estimación, va **0**
  en el campo **y** la pregunta en «Datos a confirmar». Un campo vacío no se distingue de
  «nadie lo miró» y no suma al sprint.

La skill **GENERA las cuatro** con lo que el usuario/dev aporta; **no** deja el molde de la
plantilla vacío ni con placeholders. Donde falte un dato que la IA **no puede saber** (una
regla de negocio que no está en el Cerebro, un comportamiento ambiguo), se saca como
**pregunta `⚠ pendiente`** —nunca se inventa— y queda **declarada** en «Datos a confirmar», con
su recomendación. Un `⚠` declarado **no** saca a la Tarea de «lista para desarrollar»
(decisión de diseño del template): se desarrolla lo que no depende de él, y ese punto queda como
pendiente a confirmar en la tarjeta ([[comentar-tarea]] §«Pendientes a confirmar»). Lo que sí la deja **NO lista** es que falte una de
las cuatro piezas.

**Exención parcial de la Tarea de front.** Una Tarea de **solo UI/config** (una columna
nueva en una grilla, un texto) está exenta del contrato y del bloque entero. Pero una Tarea
de front que **implementa un Escenario de la Historia** —aunque no tenga capa
`api`/`application`/`domain`— **igual lleva la tabla de Escenarios**: es la mitad visible de
un comportamiento que el back solo cubre a medias, y sin la tabla ese Escenario queda sin
dueño del lado del usuario. Lo que la Tarea de front **no** define es contrato propio:
consume el de las Tareas de backend.

### 3.2 Reparar una Historia existente (cuando [[auditar-historia]] la marcó CON HUECOS)

Esta skill es también la que **cierra el Gherkin de una Historia ya creada**. Es un caso de
uso propio, no un efecto colateral: un veredicto que bloquea y **no tiene destinatario**
termina en que alguien inventa los Escenarios para desbloquear — exactamente lo que todo
este aparato viene a impedir.

- Se toma la Historia por su `#ID` (lectura) más el **reporte de la auditoría**, y se
  reescriben **solo** los bloques observados: Criterios de aceptación, *Casos de uso*,
  *Datos y estados*.
- **Lo que la IA no puede saber NO se completa:** una regla que no está en el Cerebro, un
  comportamiento ambiguo o un estado sin nombre salen como **pregunta `⚠`**. Proponer la
  regla que falta para destrabar es el defecto que la auditoría persigue.
- Se entrega pegable; escribirlo en el board es otro turno ([[cargar-a-azure]]). El sello
  anterior queda vencido, porque cambiaron sus Criterios de aceptación; volver a auditarla es
  opcional.

### 4. Marcar lo pendiente y preguntar
Todo dato faltante se deja como `⚠ pendiente: <qué falta>` **dentro** del ticket
y se lista aparte como preguntas al usuario. **No** se avanza a un ticket "cerrado"
inventando lo que falta. Esperar la confirmación humana con los datos. Las preguntas van
**todas juntas**, numeradas y con una recomendación cada una; en modo lote van al arranque o al
cierre de [[planificar-lote]], nunca en un turno por pregunta.

### 5. Entregar pegable
Salida final: los campos separados y rotulados, alineados con el mapa de campos
del board ([[checklists/mapa-campos-azure]]), listos para copiar uno por uno.

**Descripción, Criterios de aceptación y Pasos para reproducir van en HTML**, con el
esqueleto del tipo que está en [[checklists/mapa-campos-azure]]: `<h3>` con `<hr>` entre
secciones, `<ul>`/`<ol>`, `<table>`, `<pre>` para el contrato, palabras clave del Gherkin en
`<b>` y `&lt; &gt;` en los marcadores. **Nunca markdown**: ni bloques con tres comillas
invertidas, ni `- [ ]`, ni tablas con `|`. Azure los muestra literales y la tarjeta queda
ilegible. En el chat se puede mostrar además cómo se va a ver, pero lo que se pega es el HTML.
**Vale también para los fragmentos**: si se corrige una tarjeta existente, lo que se agrega va
en HTML listo para insertar —una fila `<tr>…</tr>`, un `<li>…</li>`—, nunca una fila con `|`.

**Autochequeo antes de entregar** (mecánico; si uno falla, se corrige antes de mostrar):

| # | Chequeo |
|---|---|
| 1 | **Etiquetas: exactamente una.** No es un slice (`<slice-1>` · `<slice-2>` · `<slice-n>`), ni `<producto>`, ni `modulo-ejemplo`. Si el tema no tiene etiqueta acordada, va con `⚠` |
| 2 | Descripción y Criterios **en HTML**; cero markdown |
| 3 | Cada `[RN-…]` citada **existe en el Cerebro**, y se puede decir en qué archivo. **Y dice lo que se le atribuye**: se lee la regla, no alcanza con encontrar el número. Una regla con un sufijo agregado (`-REV`, `-CONF`) no es esa regla: es una inventada. **Si el pedido choca con una regla** (p. ej. pide validar algo que la regla deja fuera de esta etapa), se frena y se pregunta: no se redacta el arreglo igual |
| 4 | Si el pedido era corregir una tarjeta existente, **se leyó su texto actual** (del tablero o pegado). Si no, no se reconstruyó: se pidió |
| 5 | Todo lo que no se sabe está marcado `⚠`, no rellenado con lo esperable. En particular, **un código HTTP, un código de error o un número de regla** que no figura en la tarjeta ni en el Cerebro va `⚠ a definir`, nunca con un valor que suene bien: un código de estado típico, un nombre de error armado a partir del pedido, o un número de regla correlativo |
| 6 | **No existe ya.** Si al leer el Cerebro aparece un ticket del mismo pedido (el bloque «Tickets derivados» de la ficha, o un `#ID` citado en el flujo), se frena y se pregunta si se actualiza ése: no se redacta uno nuevo en paralelo ([[deduplicacion-antes-de-crear]]) |
| 7 | **El tipo sale de la señal, no del pedido.** Si lo que se describe como falla todavía no existe según el Cerebro (figura como pendiente o fuera de esta etapa), no es un Bug: es una Historia o mejora, y se dice por qué |

## Contexto adicional

- Checklist DoR/DoD y antipatrones: [[conocimiento/00-index]]
- Ejemplos antes → después: [[ejemplos/00-index]]

---

### Ejemplo (genérico)

> Entrada pobre en el tablero: *"Un listado tira error,
> ver adjunto"*. La skill clasifica como **Bug**, y redacta:
> **Esperado:** al abrir un listado se muestran los resultados del filtro.
> **Obtenido:** error técnico 500 al aplicar el filtro por `<documento>`.
> **Por qué / pasos:** 1) entrar al listado; 2) filtrar por documento;
> 3) se corta con 500. Ambiente TEST, versión FE_x.y.z. Gravedad `2-High`.
> ⚠ pendiente: ¿el error es con cualquier documento o solo con uno puntual?
>
> Los datos reales de la persona se enmascaran con `<documento>` (PHI). El ticket queda
> pegable en los campos del board (*Pasos para reproducir*, *Gravedad*), sin tocar
> Azure hasta que el humano confirme.
