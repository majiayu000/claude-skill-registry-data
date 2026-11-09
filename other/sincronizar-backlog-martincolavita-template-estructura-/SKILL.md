---
name: sincronizar-backlog
description: >-
  Tomar una ficha del Cerebro Digital (cerebro-digital/) y DERIVAR de ella el árbol
  de tickets de Azure DevOps: Épica → Features → Historias (las Tareas quedan para Dev/planning). Usar cuando
  se pida "bajá esta ficha/módulo al board", "derivá los tickets de esta doc",
  "creá la épica y las historias de X", "sincronizá el backlog con la documentación",
  "armá el backlog de este módulo", "/sincronizar-backlog". Aplica el mapeo OKF→ADO,
  la etiqueta temática, las relaciones (Parent/Related) y el documento fuente por
  referencia. PROPONE el árbol y lo crea por MCP SOLO con confirmación humana
  explícita (escribir en el board es IRREVERSIBLE). Registra los #ID en la ficha
  ("Tickets derivados") y en el historial, siempre POR REFERENCIA. TODO en español;
  PHI PROHIBIDO; no inventa (los #ID son dato duro, ⚠ hasta confirmar).
---

# Sincronizar backlog

> **Tablero local (`DEC-006`):** si el proyecto usa el tablero local, «el board» es `cerebro-digital/<modulo>/backlog/`
> y se opera con `bin/tablero-local.py`, con los mismos GATEs y sin MCP (detalle: `backlog/README.md` del módulo).
> Con Azure DevOps, Jira u otro tablero, las operaciones se traducen con la tabla de `integracion-azure-mcp/00-index.md`.
> La bajada 1:1 del árbol la hace `bin/derivar-a-tablero-local.py <ficha>` (idempotente; sin Tareas); esta skill
> redacta cada nodo después, con `redactar-tarea`.

Toma una **ficha del Cerebro Digital** (`cerebro-digital/`) y baja
de ella el **árbol de work items** al board de Azure DevOps. Es la skill que
**conecta la documentación con el backlog**: doc → tickets → historial.

Escribe en un sistema externo, así que el control humano es obligatorio: **propone
el árbol y solo crea con un "sí" explícito**. La redacción fina de un ticket suelto
la cubre [[redactar-tarea]]; la escritura de un único work item ya redactado, la
cubre [[cargar-a-azure]]. Esta skill orquesta el **alta en lote coherente** desde
una ficha.

**Con más de una Historia, o si también van las Tareas, el trabajo corre con el método de
[[planificar-lote]]:** las dudas sin fuente van todas juntas en el arranque, la redacción corre
en paralelo (y, si se piden, las auditorías, cada una por un agente distinto) y el árbol se escribe con
el "sí" del cierre. Las reglas de esta skill —cardinalidad 1:1, dedup por nodo, tarjeta
congelada, traza— valen igual adentro del lote: el lote cambia **cuándo** se pregunta, no
**qué** se controla.

## Regla de oro (cultura del equipo)

- **Confirmación humana antes de escribir.** El árbol se muestra completo y se
  espera un "sí" del usuario. Sin confirmación no se llama a ninguna herramienta de
  escritura del MCP. Crear/editar es **irreversible** desde acá.
- **NO INVENTAR.** La estructura (qué Épica, qué Features, qué Historias) sale
  **1:1 del bloque `## Derivación a backlog`** de la ficha — no se segmenta la prosa
  «a ojo». Los **#ID son dato duro** (`⚠` hasta que el MCP los devuelva o el usuario
  los confirme). El conteo lo fija la **ficha enumerada**, no el modelo (ver
  [[organizacion-y-trazabilidad]] §5).
- **PHI PROHIBIDO.** Nada de datos reales al board: marcadores `<persona>`,
  `<documento>`, `<identificador>`, `<dato-sensible>`, `<telefono>`, `<direccion>`.
- **Enlazar, no copiar.** La traza doc↔ticket se guarda **por referencia** (ruta
  del doc + #ID de tickets), nunca duplicando el contenido de la ficha ni el del
  ticket. Así la memoria/historial NO crece con el tamaño de los documentos.
- **Español (Argentina)**, sin emojis como íconos.

## Precondiciones

> **El árbol lo cuenta un script.** Antes de redactar un solo nodo se corre
> `python bin/derivar-arbol.py <ficha>`: devuelve las Épicas, Features e Historias 1:1 con sus padres,
> reglas, la etiqueta única y el documento fuente, o dice por qué la ficha **no se deriva** (sin bloque,
> con `⚠`, incoherente). Lo que el script no lista, no se crea; lo que lista, no se funde ni se parte.

1. **Ficha con bloque de derivación enumerado y cerrado.** Solo se derivan al
   backlog fichas que traen el bloque `## Derivación a backlog` con los
   `Slices [S-nn]`, `Capacidades [C-nn]` y `Flujos [F-nn]` **enumerados y
   cerrados** (lo produce la curación; ver [[organizacion-y-trazabilidad]] §5), más
   reglas `[RN-…]` numeradas y etiqueta temática. **Si falta el bloque enumerado, o
   hay `⚠ (pendiente)`, NO se deriva:** se frena y **primero** se
   cierra/enumera en el Cerebro (`cerebro-digital/`) — no se cuenta la ficha «a
   ojo» sobre la prosa. **Integridad referencial:** cada `[C-nn]` debe referenciar un
   `[S-nn]` existente y cada `[F-nn]` un `[C-nn]` existente; si hay una referencia
   colgada (un Parent inexistente), tampoco se deriva — se frena y se pide cerrarla.
   (Por qué el gate: [[criterios-aceptacion-gherkin]] §8 — entra-basura = sale-basura.)
   El estado de la ficha (`F-Draft`/`F-Verified`) es un metadato del ciclo de vida
   general del Cerebro; **no** es condición para derivar — la confirmación humana
   simple del paso 4 (¿creo estos work items?) es la que habilita la escritura.
2. **MCP de Azure configurado y PAT con escritura** (Work Items Read & Write).
   Setup: [[integracion-azure-mcp/00-index]]. Si falta el MCP o el PAT es de solo
   lectura → **no se escribe**: se entrega el árbol propuesto como texto pegable y
   se le dice al usuario que lo cargue a mano.

## Flujo

### 1. Leer la ficha y su bloque de derivación
Leer la ficha del Cerebro Digital indicada (archivo de `cerebro-digital/`). Extraer
el **bloque `## Derivación a backlog`** — los `Slices [S-nn]`, `Capacidades [C-nn]` y
`Flujos [F-nn]` enumerados, que **fijan el árbol** —, más las reglas `[RN-…]`,
etiqueta temática, documento fuente y cualquier `⚠ (pendiente)`. **Si el bloque
enumerado no está** (o hay pendientes que afectan el alcance), **frenar** y pedir
cerrarlo/enumerarlo en el Cerebro (`cerebro-digital/`) — no se deriva sobre prosa
sin enumerar. **Visibilidad (no bloquea):** si la ficha tiene pendientes sin resolver que **no**
afecten el bloque de derivación, avisarlos igual al proponer el árbol. **Buscar las
cuatro formas que conviven hoy en el Cerebro**, no una sola: `## Dudas y Preguntas`,
`## Dudas y preguntas` (minúscula), `## Pendientes` y cualquier `- [ ]` o `⚠` suelto.
Buscar un solo literal hace que el aviso reporte **cero** sobre una ficha que sí tiene
pendientes abiertos — y el humano confirma el árbol sin verlos — no frena la derivación, pero
el humano debe verlo antes de confirmar.

### 2. Aplicar el mapeo por vertical slices → ADO
Descomponer según la arquitectura (**monolito modular por vertical slices**; ver [[organizacion-y-trazabilidad]] §5):

| En el dominio / arquitectura | En Azure DevOps |
|---|---|
| **Vertical slice / dominio** (los slices declarados en [[contexto-proyecto]]) | **Épica** |
| **Capacidad / caso de uso** dentro del slice | **Feature** |
| **Flujo / acción de negocio** | **Historia de usuario** |
| **Desglose técnico** dentro del slice (capas `api`/`application`/`domain`/`infra`) | **Tarea** — *momento dev/planning; NO en el árbol funcional por default* |

**Cardinalidad 1:1 (no segmentar «a ojo»).** El conteo sale del bloque `## Derivación
a backlog` de la ficha: **1 Épica por cada `[S-nn]`** (default 1; nunca inferir slices
no listados), **1 Feature por cada `[C-nn]`** (Parent = Épica de su slice), **1
Historia por cada `[F-nn]`** (Parent = Feature de su capacidad) y **0 Tareas** por
default. Ningún nodo fuera de la enumeración; no se parte ni se fusiona un flujo por
criterio propio. La **unidad de Historia es el flujo listado, NO la pantalla**
(decisión cerrada; ver [[organizacion-y-trazabilidad]] §5).

Completar **cada** work item según su plantilla, **no solo el título**: la **Épica**
([[plantillas/epica]]) y la **Feature** ([[plantillas/caracteristica]]) con objetivo +
alcance + criterios de alto nivel; las **Historias** con criterios en Gherkin
referenciando las `[RN-…]`. La Descripción **y los Criterios de aceptación** se arman
en **HTML** para que se vean bien formateados en el board — los Criterios (Gherkin) con
**todas las keywords en negrita** (`Dado`/`Cuando`/`Entonces`/`Y`/`Pero`), pasos
sangrados y un `<p>` por escenario (si no, se ven como un muro). Esqueleto:
[[checklists/mapa-campos-azure]] §"Esqueleto HTML".

### 3. Adjuntar trazabilidad a cada nodo
A todos los tickets del árbol:

- **Un solo tag temático en CADA nodo, techo duro** (Épica, Feature, Historia **y**
  Tarea — **no solo la Épica**): el **mismo y único** tag temático sin prefijo,
  escrito siempre igual ([[organizacion-y-trazabilidad]] §1). **No** se agrega tag
  de slice ni de sub-flujo (el slice es la Épica), y **nunca** el nombre del
  producto/repo (ej. `<producto>`, `<repositorio>`) como tag adicional.
- **Relaciones** ([[organizacion-y-trazabilidad]] §2): jerárquicas
  Épica→Feature→Historia (Parent/Child) y **Related** entre tickets del mismo tema
  que se tocan. Los vínculos se **proponen** por título/tema; los `#ID` van `⚠`
  hasta materializarse.
- **Documento fuente**: la **ruta/URL de la ficha** (referencia, no contenido;
  [[organizacion-y-trazabilidad]] §3).

### 4. Proponer el árbol y esperar confirmación (obligatorio)
Mostrar el **árbol completo** antes de tocar nada:

```
Épica: <título>                         [tag] [doc fuente]
├─ Feature: <título>                    [Parent: Épica]
│  ├─ Historia: <título>                [Parent: Feature] [Related: …]
│  └─ Historia: <título>                [Parent: Feature]
└─ Feature: <título>
   └─ Historia: <título>
```

Indicar, por nodo: tipo, título, campos clave, etiquetas y relaciones. Marcar qué
es **alta nueva** y qué **ya existe**. **Dedup obligatorio, con evidencia (no solo por
la ficha):** además de los #ID que la ficha ya trae en "Tickets derivados", hacer
**búsqueda activa en el board** por cada nodo propuesto (por **tag temático** — que trae
el subárbol existente — + **documento fuente** + **objetivo**, foco en abiertas),
**comparando por objetivo/alcance, NO por título** (un título distinto no prueba que no
sea duplicado). Cada nodo del árbol lleva su **Bloque de dedup**: consultas corridas +
candidatos (`#ID`+link+estado, o "0") + veredicto, y queda marcado **ALTA NUEVA / YA
EXISTE** (`#ID`+link, reutilizar/actualizar) **/ SOLAPA PARCIAL**. **Ante la duda, es
duplicado:** solapa plausible → marcar posible duplicado y **preguntar**, no crear.
Para cada **YA EXISTE**, correr también la **auditoría de calidad** (checklist del
tipo contra el work item leído completo) y anotar en el árbol qué le falta, si le
falta algo — [[deduplicacion-antes-de-crear]] §Auditoría de calidad. Si un **YA
EXISTE** está en un sprint y ya tomado, se marca además **CONGELADA**: lo que le falta
se propone como comentario, no como edición ([[cambios-en-el-backlog]] §4). Los
equivalentes no se duplican: se reutilizan/actualizan (completando lo que falte)
y se relacionan. **Sin el Bloque de dedup por nodo, el árbol no se escribe.** Sin acceso al
tablero, el Bloque de dedup de cada nodo dice **SIN DATOS** —nunca «0 candidatos»— y el árbol
no se escribe: se entrega como texto con el aviso *«No busqué duplicados: buscalos vos en el tablero
antes de pegar.»* El "sí"
del paso cubre el contenido, el resultado de dedup y esas actualizaciones de completar
campos, no solo las altas nuevas. Luego **preguntar y esperar el "sí" explícito**.

### 5. Crear/actualizar por MCP
**Verificar primero el tablero autorizado** ([[tablero-autorizado]]): todo el lote va a org `{{AZURE_ORG}}` / proyecto `{{AZURE_PROYECTO}}` / team `{{AZURE_TEAM}}`. Si el destino fuera otro o no se puede determinar, **abortar el lote** con la advertencia — no se escribe nada.

Con el "sí" dado, ejecutar en orden padre→hijo:

- `create_work_item` para las altas; `update_work_item` para las ediciones.
- `manage_work_item_link` para materializar Parent/Child y Related. **El Parent se crea
  siempre desde la hija**: `create_work_item` con `parentId`, o `manage_work_item_link` con
  la hija como origen y tipo Parent. **Nunca se edita el padre para colgarle un hijo.** No
  es por el sello —un vínculo no es contenido y no vence ninguno—: es porque el MCP escribe
  sobre el ítem de origen, y así no se escribe en una tarjeta que no es la que se está
  cargando. Lo mismo con
  Related entre Tareas: desde la nueva, no desde la que ya está sellada.
- Resolver los #ID de relaciones con `search_work_items` / `list_work_items` cuando
  haga falta.
- **Al actualizar una tarjeta que está asignada o seguida** (re-sincronización tras
  un cambio del doc), disparar el **protocolo de aviso**: comentario con @mención
  de qué cambió + etiqueta `cambio-pendiente-lectura`, para que quien la trabaja no
  siga sobre una versión vieja. Detalle: [[cambios-en-el-backlog]].
- **Una tarjeta congelada** (en un sprint y ya tomada) **sale del lote de ediciones**: no
  lleva `update_work_item` ni etiqueta. Su DIFF va **como comentario** con @mención, y el
  preview del paso 4 ya la mostró marcada `CONGELADA` para que el "sí" no la incluya por
  error. Detalle: [[cambios-en-el-backlog]] §4.

Escribir el árbol confirmado; no encadenar altas nuevas no incluidas en el "sí".

### 6. Registrar la traza (por referencia) — en la ficha y en el historial
Cerrado el alta:

- **En la ficha del Cerebro Digital:** completar el bloque **"Tickets derivados"**
  con los `#ID`/URL creados (solo los identificadores; nunca copiar el cuerpo de los
  tickets). Esto da la traza doc → tickets.
- **En el historial** ([[historial/INDICE]]): agregar **una fila por ticket** (o una
  por el lote) con tema, `#ID`, documento fuente (ruta de la ficha), resumen de una
  línea y puntos si aplica. Es un **log resumido e indexable**: **referencia, no
  contenido** (ni el cuerpo de la ficha ni el del ticket se copian). El `.md`
  detallado se crea **solo** si el ticket se promueve a `gold`.

### 7. Reportar
Devolver los **#ID/URL** creados o actualizados y qué quedó enlazado. Silencio al
entregar: al grano.

## Barreras (no negociables)

- **GATE de TABLERO (duro).** Todo el árbol se crea **solo** en el tablero autorizado (org `{{AZURE_ORG}}` · proyecto `{{AZURE_PROYECTO}}` · team `{{AZURE_TEAM}}`). Antes del primer `create_work_item`, verificá el destino; si es otro tablero o no se puede determinar, **abortá el lote** y mostrá la advertencia. Detalle: [[tablero-autorizado]].
- **GATE de TARJETA CONGELADA (duro) — se chequea antes que los demás.** Antes de cualquier `update_work_item` del lote, leer `System.IterationPath` y `System.State`. Si la tarjeta está **en un sprint y ya tomada** (Estado distinto de `New`), **no se edita**: ni con uno ni con dos "sí". Lo que se quería cambiar se ofrece **como comentario** con el DIFF, vía [[comentar-tarea]], y aplicarlo lo decide una persona. **Si no se puede leer el sprint o el estado, está congelada.** Detalle: [[cambios-en-el-backlog]] §4.
- **GATE de deduplicación (duro).** Antes de crear cada nodo, búsqueda activa en el board (tag temático + documento fuente + objetivo, foco abiertas), **comparando objetivo/alcance, no título**; cada nodo lleva su **Bloque de dedup** en el árbol del preview y **sin ese bloque el árbol no se escribe**. **Ante la duda, es duplicado** (solapa plausible → preguntar). Los equivalentes NO se duplican (se reutilizan/actualizan y se relacionan). Detalle: [[deduplicacion-antes-de-crear]].
- **GATE de EXISTENCIA (bloqueante — encontrar ≠ crear igual).** Para **cada nodo** marcado `YA EXISTE`: queda **PROHIBIDO `create_work_item`** de ese nodo. Encontrarlo obliga a **frenar** ese nodo, no a crear un paralelo: se presenta el existente (`#ID` + link + estado) y se **pregunta** si ACTUALIZAR (`update_work_item`) o modificar, esperando el "sí" (en modo lote, esa pregunta va en el arranque, junto con las demás). Un lote **nunca** crea nodos nuevos en paralelo a los que la búsqueda ya encontró — aunque la ficha traiga otros nodos que sí son alta nueva, los `YA EXISTE` se excluyen del `create`. Buscar y encontrar sin frenar es exactamente la falla que este gate prohíbe.
- **GATE de NIVEL (duro, bloqueante) — profundidad y amplitud.** *Profundidad:* por default el árbol baja **hasta Historia** (Épica → Feature → Historia); las **Tareas NO se crean**. Bajar a Tareas obliga a **frenar y confirmar en su propio turno** (en modo lote, el de arranque, que nombra las Historias): *«¿esto es contexto dev/planning y estas Tareas son técnicas, para un dev?»* — un "creá las tareas" **no** alcanza por sí solo; sin ese "sí" explícito sobre el nivel, el árbol se queda en Historias. Si se confirma dev/planning, la IA **deriva las Tareas de la Historia** por su estructura técnica (por endpoint/caso de uso y **capa afectada** `api`/`application`/`domain`/`infra` + front, más una Tarea de test de integración si toca una dependencia externa) — el desglose es **juicio técnico de la reunión de devs, NO sale 1:1 de la ficha** como los niveles de arriba. **Cada Tarea usa la plantilla detallada** ([[plantillas/tarea]]) con **Contrato técnico (entrada/salida)** —que para capa `api` va como fragmento OpenAPI (YAML)—, validaciones, casos de error, **Especificación cerrada (SDD)** con la tabla que mapea los **Escenarios del Gherkin de la Historia** a los tests, la **lista de "Tests a escribir PRIMERO" (test-first)** numerada y el bloque **Modos de falla evaluados** (una línea por familia: cubierta por un test, o descartada con su motivo) (obligatorio si capa `api`/`application`/`domain`; DoR en [[redactar-tarea]] §3.1) — no Tareas de una línea. **Las auditorías son opcionales y a pedido** (decisión de diseño del template): [[auditar-historia]] antes de derivar, [[analizar-tareas]] sobre el conjunto y [[auditar-tarea]] sobre cada Tarea **no corren solas** y su sello **no** es requisito para derivar ni para desarrollar. Si alguien las pide, corren como se describe a continuación, y lo que encuentren queda **como pendiente a confirmar** en la tarjeta ([[comentar-tarea]] §«Pendientes a confirmar»), sin frenar. *(Cómo corren cuando se piden:)* [[auditar-historia]] sobre la Historia antes de derivar. Se avisa en criollo («*antes de armar las Tareas voy a auditar la Historia #NNNN, esperá*»), se muestra el veredicto, y se sigue. **El funcional no la invoca nunca**: es del lado dev, después de que el GATE de NIVEL confirmó que estamos en contexto dev/planning (en modo lote, si se pidió, corre en la preparación y sus preguntas van al mismo arranque que la del nivel). Si ya hay un sello **vigente** (vale solo el sello más reciente; guarda el `Rev auditado` y la fecha de la ficha fuente. Son **dos** chequeos: el board, con `bash bin/verificar-sello.sh historia <id-historia> <Rev auditado>` —vigente si ninguna revisión posterior cambió Título, Descripción o Criterios de aceptación; comentarios, Estado y Tareas hijas no cuentan—, y la ficha, comparando su fecha de último cambio contra la del sello, porque el script no mira el Cerebro. Hace falta que pasen los dos; `SIN DATOS` no es vigente. Ver [[auditar-historia]]), **se reusa y no se vuelve a auditar**. Si el veredicto es **CON HUECOS**, no se frena: los hallazgos quedan como pendientes a confirmar, y si el humano prefiere arreglar primero, lo dice. En modo lote ([[planificar-lote]]) los hallazgos que resuelve una fuente se corrigen sin preguntar. **Sin auditoría se derivan Tareas igual**; lo único que no se deriva es una Historia **sin ningún Escenario** —eso no es auditoría, es el DoR: sin Escenarios no hay qué mapear a tests—. Si se pide, **antes de confirmar el alta de las Tareas** se corre **[[analizar-tareas]]** sobre el conjunto (contratos que no se pisan, cada `[RN-]` cubierta, **cada Escenario de la Historia cubierto por alguna Tarea y con test que lo verifique**, coherencia del test de integración, sin huecos ni solapes); lo que aparezca se saca **como pregunta**, no como decisión silenciosa (en modo lote, en el cierre). **Después de crearlas**, si se pide, cada Tarea pasa por **[[auditar-tarea]]** (segundo chequeo, agente distinto); no es requisito para despacharla a desarrollo (en modo lote, si se pidió, corre sobre el borrador antes del cierre, y el sello se publica al escribir): `analizar-tareas` mira que el **conjunto** cierre entre sí, `auditar-tarea` mira que a **cada lista de tests** no le falte un caso. *Amplitud:* el conteo de Épicas/Features/Historias sale **1:1 del bloque `## Derivación a backlog`** de la ficha — **default 1 Épica**; crear >1 Épica exige que la ficha declare **>1 slice**. Nunca inferir el rol ni multiplicar nodos; ante ambigüedad, preguntar.
- **Proponer y crear son turnos distintos.** El paso 4 (mostrar el árbol) **cierra el turno**; el paso 5 (escribir) solo con un "sí" nuevo. Nunca proponer y crear en el mismo turno.
- **Solo para bajar una ficha/módulo ENTERO.** Esta skill arma el árbol en lote. Si
  el pedido es **un** ticket suelto, NO se usa esta skill: se usa
  [[redactar-tarea]] + [[cargar-a-azure]]. Nunca convertir un pedido de un ítem en
  un árbol de muchos.
- **Confirmación humana por operación.** El "sí" es por lote/sesión; no se
  generaliza a la próxima sincronización.
- **No inventar #ID ni estructura como si fuera dato.** Propuesta + confirmación.
- **PHI prohibido** en lo que se escribe al board.
- **Provenance/autoría:** la escritura queda auditada por el dueño del PAT; no usar
  un PAT ajeno. El token es una password: si se expone, se rota.
- **Si la ficha tiene `⚠ (pendiente)` que afectan el alcance, no se deriva:** se
  vuelve al Cerebro (`cerebro-digital/`) a cerrarlos.

## Contexto adicional

- Mapeo, tags, relaciones y documento fuente: [[organizacion-y-trazabilidad]]
- Actualizar tarjetas desfasadas y avisar al equipo (drift): [[cambios-en-el-backlog]]
- Auditar cobertura y detectar desfases (solo lectura): [[consultar-backlog]]
- Chequear la consistencia del set de Tareas antes de cerrar: [[analizar-tareas]]
- Setup MCP / PAT / seguridad: [[integracion-azure-mcp/00-index]]
- Paso previo (dejar la ficha lista): el Cerebro (`cerebro-digital/`)
- Redacción/escritura de un ticket suelto: [[redactar-tarea]] · [[cargar-a-azure]]
- Aprendizaje del toolkit: [[historial/README]]

---

### Ejemplo (genérico)

> Recuadro ilustrativo de un dominio de ejemplo; es solo un
> ejemplo, el tema real lo pone el proyecto destino.
>
> El usuario pide "bajá al board la ficha de Reservas". La ficha
> `cerebro-digital/.../<ficha-reservas>.md` declara en su bloque `## Derivación a
> backlog`: `[S-01]` Reservas · `[C-01]` Reserva de salas · `[F-01]`
> Crear una reserva con validación de disponibilidad · `[F-02]` Cancelar una reserva
> desde el panel. La skill copia eso **1:1** → **Épica** "Reservas" (=S-01) →
> **Feature** "Reserva de salas" (=C-01) → **Historias** F-01 y F-02 (la
> de cancelación Related con "Notificar la cancelación al solicitante"). Todos con tag
> `<etiqueta-tematica>` — **uno solo, sin etiqueta de versión ni de producto, y sin el nombre del slice** — y **Documento fuente** = la ruta
> de la ficha (referencia). Muestra el árbol, pregunta "¿Creo estos **4 work items**
> (1 Épica + 1 Feature + 2 Historias = S-01+C-01+F-01+F-02) con estos enlaces?", y
> recién con el "sí" llama a `create_work_item` +
> `manage_work_item_link`. Devuelve los `#ID`, los anota en el bloque **Tickets
> derivados** de la ficha y agrega una fila en [[historial/INDICE]] con el tema, los
> `#ID` y el `documento_fuente` — sin copiar el contenido de la ficha ni de los tickets. Si el
> PAT fuera de solo lectura, entrega el árbol como texto para cargar a mano.
