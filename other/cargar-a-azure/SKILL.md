---
name: cargar-a-azure
description: >-
  (Avanzada / opcional) Con el MCP de Azure DevOps configurado y un PAT con scope
  de ESCRITURA, crear o actualizar el work item en el board a partir del ticket que
  produjo la skill redactar-tarea (create_work_item / update_work_item). Usar cuando
  se pida "cargá esto a Azure", "creá la tarjeta", "actualizá el work item #ID",
  "subilo al board". Escribir en el board es una acción IRREVERSIBLE: SIEMPRE se
  muestra el diff/preview y se espera un "sí" humano explícito antes de escribir.
  Si no hay MCP o el PAT es de solo lectura, cae a "copiá y pegá a mano" con el
  texto pegable, avisando arriba que no se buscaron duplicados. No entra PHI real; respeta la jerarquía por persona del PAT.
---

# Cargar a Azure

> **Tablero local (`DEC-006`):** si el proyecto usa el tablero local, «el board» es `cerebro-digital/<modulo>/backlog/`
> y se opera con `bin/tablero-local.py`, con los mismos GATEs y sin MCP (detalle: `backlog/README.md` del módulo).
> Con Azure DevOps, Jira u otro tablero, las operaciones se traducen con la tabla de `integracion-azure-mcp/00-index.md`.

Toma el ticket ya redactado (por [[redactar-tarea]]) y lo **crea o actualiza** en
el board vía el MCP de Azure DevOps. Es la única skill del toolkit que **escribe**
en un sistema externo; por eso el control humano es obligatorio.

## Precondiciones (verificar antes de intentar)

1. **MCP configurado.** Servidor `@tiberriver256/mcp-server-azure-devops` vía
   `npx -y`, con las env vars cargadas. Detalle y setup: [[integracion-azure-mcp/00-index]].
2. **PAT con scope de ESCRITURA.** Alta/edición requiere **Work Items (Read & Write)**.
   El PAT lo crea **cada usuario el suyo** (auditoría por persona), con caducidad y
   mínimo scope, y vive como **env var** (`AZDO_PAT`) — **nunca** en un `.md` que la
   IA lea ni pegado en el chat.
3. Si falta el MCP o el PAT es de solo lectura → **no se escribe**: se entrega el
   texto pegable y se le dice al usuario que lo cargue a mano (copiá y pegá). Arriba de
   todo va el aviso *«No busqué duplicados: buscalos vos en el tablero antes de pegar.»*,
   y en el Bloque de GATES la dedup y la tarjeta congelada dicen **SIN DATOS**, nunca OK.

## Flujo

### 1. Confirmar la operación
**Primero, verificar el tablero autorizado** ([[tablero-autorizado]]): el destino debe ser org `{{AZURE_ORG}}` / proyecto `{{AZURE_PROYECTO}}` / team `{{AZURE_TEAM}}`. Si el pedido apunta a otro tablero o no se puede determinar, **frenar** con la advertencia — no se escribe.

Determinar si es **alta** (nuevo) o **edición** (existe `#ID`):
- Alta → `create_work_item` (proyecto, tipo, título, campos).
- Edición → `update_work_item` (ID + campos a cambiar). Antes de editar, leer el
  estado actual con `get_work_item` para armar el diff real y no pisar datos.
  **Si está en un sprint y ya tomada, está congelada: no se edita.** Se frena, se avisa en
  criollo y se ofrece dejar el DIFF como comentario ([[cambios-en-el-backlog]] §4).

### 1b. Buscar duplicados (obligatorio, en toda alta) — con evidencia
Antes del preview, buscar en el board si el ítem **ya existe**, usando
`search_work_items` / `list_work_items`, por **tag temático** (trae el subárbol del
tema) + **documento fuente** + **objetivo** (textual), foco en abiertas. **Comparar por
objetivo/alcance, NO por título:** un título distinto no prueba que no sea duplicado
(es la causa #1 de repetidos). **Ante la duda, es duplicado:** cualquier abierto del
mismo tema/doc cuyo objetivo se solape → **posible duplicado → preguntar**, nunca crear
en automático.

Esta búsqueda produce el **Bloque de dedup** que va **sí o sí** en el preview del paso 2
(consultas corridas · candidatos `#ID`+link+estado · veredicto por candidato). Si hay
un **equivalente**, **no crear**: avisar con `#ID`+link y proponer **reutilizar/
actualizar** + **relacionar** (Related). Si hay **solapamiento parcial**, informar y
esperar decisión. Si no se pudo consultar el board (MCP/PAT), **no se escribe**: se
avisa que no se pudo verificar dedup. Detalle: [[deduplicacion-antes-de-crear]].

### 1c. Auditar calidad del equivalente (si 1b encontró uno)
Leer el work item completo (`get_work_item`) y correr el checklist del tipo
([[checklists/checklist-historia]] / [[checklists/checklist-bug]] /
[[checklists/checklist-habilitador]] + [[definicion-preparado-terminado]]).
Para **Épica** va [[checklists/checklist-epica]] y para **Feature**
[[checklists/checklist-caracteristica]]. Son justo los dos nodos que más se reutilizan
(siempre existen, siempre se marcan YA EXISTE), así que este paso es el que más corre:
antes no había checklist para ellos y se evaporaba en silencio. Si
cumple, sigue como "reutilizar/relacionar" sin tocar nada. Si le falta algo, el
preview del paso 2 pasa de "no se crea nada" a un preview de **edición**
(`update_work_item`) con los campos concretos a completar — mismo GATE de
confirmación que un alta. Si el equivalente está **congelado**, lo que le falta va como
comentario, no como edición. Detalle: [[deduplicacion-antes-de-crear]] §Auditoría
de calidad.

### 2. Preview + confirmación humana (obligatorio)
Mostrar exactamente lo que se va a escribir:
- **Bloque de dedup (arriba de todo, obligatorio):** consultas corridas (tag ·
  objetivo · doc fuente) · candidatos `#ID`+link+estado (o "0 candidatos") · veredicto
  por candidato (`equivalente`/`solapa`/`distinto` + por qué). **Sin este bloque el
  preview es inválido y NO se escribe** — da igual que el resto esté perfecto.
- **Alta:** tipo, título, y cada campo con su valor.
- **Edición:** campo por campo, **valor actual → valor nuevo**.
- Incluir el **tag temático — uno solo, techo duro** (sin tag de slice, sin tag de
  producto/repo) — y verificar que la **Descripción** Y los **Criterios de aceptación**
  van en **HTML** válido (no markdown crudo). Los Criterios (Gherkin) llevan **todas las
  keywords en negrita** (`Dado`/`Cuando`/`Entonces`/`Y`/`Pero`), pasos sangrados y un
  `<p>` por escenario — si no, se ven como un muro. Esqueleto: [[checklists/mapa-campos-azure]].

### 2a. Bloque de GATES (obligatorio, arriba de todo) — el gate que no deja rastro no es gate

El preview arranca con esta tabla, **llena**, antes que cualquier otra cosa. Sin ella el
preview es inválido y **no se escribe**, igual que sin el Bloque de dedup.

| Gate | Estado | Evidencia (una línea, concreta) |
|---|---|---|
| **Tablero autorizado** | OK / FRENA / SIN DATOS | org · proyecto · team verificados contra [[tablero-autorizado]] |
| **Tarjeta congelada (solo ediciones)** | OK / FRENA / SIN DATOS | **Ruta de iteración** y **Estado** leídos de la tarjeta. En un sprint y distinto de `New` → FRENA. Sin poder leerlos → SIN DATOS: se trata como congelada y no se edita |
| **NIVEL (solo Tareas)** | OK / FRENA | **La frase textual del humano**, de esta conversación y sobre esta Historia, que declara contexto dev/planning (en modo lote: la respuesta del arranque a la pregunta que nombró esta Historia) |
| **Dedup** | OK / FRENA / SIN DATOS | Consultas corridas · candidatos `#ID` · veredicto por candidato (ver §1b) |
| **Confirmación** | PENDIENTE | Se marca OK recién con el "sí" sobre **el contenido mostrado abajo**, no sobre la propuesta |

**Tres estados, no dos: OK · FRENA · SIN DATOS.** Una fila sólo dice OK con su evidencia a la
vista, y la evidencia no se escribe de memoria:

- **Dedup y Tarjeta congelada leen el tablero.** Sin MCP, o sin haber podido consultarlo, van
  **SIN DATOS** —nunca «OK · 0 candidatos», nunca «OK · no está congelada»—, y con una fila en
  SIN DATOS **no se escribe**. Si se entrega el texto para pegar a mano, arriba de todo va:
  *«No busqué duplicados: buscalos vos en el tablero antes de pegar.»*
- **NIVEL da OK sólo con una cita textual**: la frase del humano, **de esta conversación**, que
  declara contexto dev/planning. El pedido mismo («creá las tareas») **no es** esa frase. Sin la
  cita, la fila dice FRENA, se hace la pregunta del nivel y **el turno termina ahí**: la Tarea no
  se redacta en el mismo turno, ni «de ejemplo», ni como molde vacío.
- **Si el pedido no crea una Tarea** (corregir una existente, una Historia, un Bug), la fila de
  NIVEL dice **no aplica**. Nunca OK: un OK pide una cita, y acá no hay qué citar.
- **Sin MCP, el Tablero autorizado también es SIN DATOS.** Se sabe cuál es el tablero que
  corresponde, pero no se verificó que el destino sea ése: esa verificación es la que da OK.
- **Lo que cuenta el humano no es leer el tablero.** «Está en el Sprint 7 y en New» sirve para
  decidir qué proponer, pero la fila de Tarjeta congelada dice SIN DATOS hasta que se lea la
  tarjeta, porque es la lectura la que confirma el dato.

> **Por qué existe este bloque.** Los GATES eran **instrucciones que el agente tenía que
> acordarse de aplicar**, y bajo la inercia de producir se comprimen: en una corrida real se
> saltearon **cuatro de cuatro** — el de NIVEL no se preguntó (se arrastró una confirmación de
> otra Historia, que la regla prohíbe explícitamente), el de confirmación se dio por cumplido
> con un "sí" sobre la **forma** y no sobre el **contenido**, la dedup se corrió pero se reportó
> en prosa sin el bloque, y el checklist de §2b no se corrió.
> El único control de este toolkit que nunca falla es la dedup, y no falla porque **produce un
> artefacto visible**. Esta tabla le da la misma forma al resto.
> **El gate de NIVEL no se hereda entre Historias.** Cada Historia necesita su declaración,
> dicha por el humano en esta conversación, y la cita textual de dónde se dio — si hay que
> buscarla y no aparece, FRENA. En **modo lote** ([[planificar-lote]]) una sola respuesta
> declara varias Historias si la pregunta del arranque **las nombró a todas**: lo que no se
> hereda es la declaración para una Historia que la pregunta no nombró.

### 2b. Checklist de cierre (MECÁNICO, obligatorio en toda Tarea) — antes del "sí"

Los defectos que se cuelan no son de criterio: son **de conteo**, y por eso se revisan
contando, no releyendo. Esta tabla se **llena y se muestra dentro del preview**; si una
fila da `NO`, se corrige **antes** de pedir confirmación. Un preview de Tarea sin esta
tabla es inválido, igual que sin el bloque de dedup.

**La cuenta la hace el script**, que esta skill corre sola sobre el borrador:
`python bin/auditar-tarea.py <tarea.html> --historia <criterios-del-padre.html>`. Sus chequeos
`2b-n` son las filas de esta tabla. Las filas se llenan con lo que dio el script, no releyendo:
un `HALLAZGO` es `NO`, y si el script no corrió, la fila es `SIN DATOS`. Si la herramienta no
puede correr comandos, se le pide a la persona ese comando exacto. La fila 8 (campos de Azure)
no está en la Descripción: esa se mira a mano. La fila 10 (PHI) el script la mira sólo con una
heurística, así que los nombres, las direcciones y los diagnósticos se leen a mano.

> **Tarea chica de solo UI/config: las filas 4, 5, 6 y 11 se marcan `N/A`, no `NO`.** Esas
> cuatro cuentan tests y Escenarios del bloque SDD, y ese bloque **se borra entero** en una Tarea
> de solo UI/config ([[plantillas/tarea]], [[redactar-tarea]] §3.1). `N/A` es una respuesta
> válida y se escribe; lo que no vale es dejar la fila en blanco. Marcar `NO` ahí obligaría
> a "corregir" algo que tres documentos eximen.

| # | Chequeo (contable, no opinable) | Cómo se verifica |
|---|---|---|
| 1 | **Todas las secciones del esqueleto** están, con el nombre exacto y en orden | Listar los `<h3>` del HTML y compararlos uno a uno contra [[checklists/mapa-campos-azure]]. Se cuentan, no se "revisan". |
| 2 | **Cada `[RN-…]`/`[DEC-…]` citado se usa de verdad acá** | Por cada código citado en *Material de apoyo*, buscarlo en el cuerpo. Si no aparece en ninguna validación, caso de error o test, **sobra**: se saca. Citar la regla de otra Tarea manda al dev al lugar equivocado. |
| 3 | **Cada `#NNNNN` mencionado en el texto tiene su enlace**, y **cada referencia a otra Tarea trae su `#NNNNN`** | Dos direcciones. (a) Extraer los `#NNNNN` del HTML y cotejarlos contra los links del work item: Azure **no** auto-linkea `#NNNNN` dentro de la Descripción, así que sin el Related el dev lo busca a mano. (b) Buscar las menciones **sin número** —«la Tarea de front (Related)», «la Tarea de backend», «ambas en Related»— y reemplazarlas por el `#ID`: la relación existe en Azure pero **no se ve desde el texto**, y un Escenario cubierto en parte no se puede seguir hasta el final. Salió mal en **3 de 3** de las primeras Tareas reales. En modo lote, sobre el borrador, un `[T-nn]` vale como `#ID`; se vuelve a mirar después del reemplazo y de las relaciones. |
| 4 | **Cada número de test aparece en la tabla de Escenarios**, o se declara que no mapea | Comparar el rango de la lista `<ol>` (1..N) contra la unión de la columna «Tests que lo verifican». Un test huérfano es un test que no cierra nada. |
| 5 | **Cada Escenario del padre aparece**: como fila si esta Tarea lo cubre (entero o en parte), o con su título textual en la línea **«No cubre»** al pie de la tabla, con la Tarea que lo cubre | Contar los `Escenario:` del campo Criterios de aceptación del padre, y contar las filas más los títulos de la línea «No cubre». Tienen que dar igual. Una fila «no lo cubre esta Tarea» también vale (es la forma vieja), pero alarga la tarjeta sin agregar nada: la forma corta es la línea al pie ([[plantillas/tarea]]). Que un Escenario no lo cubra **nadie** es otro problema, y lo detecta [[analizar-tareas]] sobre el conjunto, no esta tarjeta. |
| 6 | **Coherencia del test de integración** | Si el Alcance dice `sí`: buscar (a) el test en la lista, (b) la subtarea que lo escribe, (c) el ítem del DoD. Las **tres** o ninguna. |
| 7 | **Toda ruta o documento va como `<a href>`** | Buscar rutas con `/` o `.md` sueltas en el HTML: si no están dentro de un `<a>`, no son clickeables. |
| 8 | **Campos que no quedan nulos en silencio** | `Esfuerzo original` (0 si no hay estimación, nunca vacío), `Actividad`, **un** tag temático, Parent. |
| 9 | **Sin markdown crudo ni escapes rotos** | Buscar fences de código, `**`, `- ` al inicio de línea. Adentro de `<pre>`: `<` y `>` escapados como `&lt;` `&gt;`. |
| 10 | **Sin PHI** | Datos de persona/documento/teléfono reemplazados por marcadores. |
| 11 | **Todo test etiquetado «guardarraíl» trae escrita la frase «se pone en rojo si …»** | Buscar la etiqueta en la lista `<ol>`. Por cada una: ¿está la frase? ¿nombra un cambio que **ningún otro test de la lista** detecte? Si falta la frase, o el cambio ya lo detecta otro test, **se le saca la etiqueta y se le exige su rojo previo**. La exención se gana por escrito, no por costumbre ([[plantillas/tarea]]). |

> **Por qué existe esta tabla.** Se agregó después de que **tres tarjetas seguidas** salieran
> con defectos que se ven recién al releerlas en el board: una regla citada que la Tarea no
> usaba, un `#ID` mencionado sin enlace, un test que no cerraba ningún Escenario y rutas sin
> link. Ninguno era una decisión difícil: los cuatro se detectan **contando**. Releer el
> borrador "con atención" ya se probó y no alcanza — por eso el chequeo es mecánico y va
> **antes** del "sí", no después de escribir.

### 2c. Confirmación

Luego **preguntar y esperar un "sí" explícito**. El "sí" confirma el contenido, el
resultado de dedup **y** el checklist de cierre. Sin confirmación, no se llama a ninguna
herramienta de escritura. Escribir en el board es **irreversible** desde esta skill (no
hay "deshacer").

**En modo lote** ([[planificar-lote]]) el preview de cada ítem es su fila en la tabla del
cierre más su archivo, y el "sí" del cierre vale por esta confirmación para cada ítem de la
tabla. El Bloque de GATES y el checklist de §2b se llenan igual, por ítem, y quedan en el
archivo del lote: se muestran en la tabla como una columna (OK o lo que falló).

### 3. Escribir
Con el "sí" dado, ejecutar `create_work_item` / `update_work_item`. Una sola
operación por confirmación; no encadenar varias escrituras sobre un único "sí" (salvo el
lote confirmado en el cierre de [[planificar-lote]], que escribe exactamente su tabla).

**El Parent va en el alta, desde la hija**: `create_work_item` con `parentId`. Nunca se
edita la Historia para colgarle la Tarea: el MCP escribe sobre el ítem de origen, y así no se
escribe en una tarjeta que no es la que se está cargando. (No vence ningún sello: un vínculo
no es contenido.) Lo mismo con Related: desde la Tarea nueva, no desde una hermana que ya
tiene su sello. Detalle: [[sincronizar-backlog]] §5.

### 3b. Segundo chequeo: opcional, a pedido

El checklist de §2b es un **autochequeo del mismo agente que la escribió**, de forma. El
segundo chequeo de fondo —[[auditar-tarea]] sobre la Tarea, [[auditar-historia]] sobre su
Historia padre— **no se encadena solo** (decisión de diseño del template): corre sólo si alguien lo
pide. Encadenarlo gastaba muchos tokens y volvía a preguntar cosas ya cerradas o que no hacían
falta para arrancar.

Al reportar el alta se ofrece en una línea, sin esperar respuesta: *«Si querés, corro la
auditoría de la #NNNN.»* Si se pide, la corre **otro agente**, y lo que encuentre queda **como
pendiente a confirmar** en la tarjeta ([[comentar-tarea]] §«Pendientes a confirmar»): no frena
el desarrollo.

**En modo lote** ([[planificar-lote]]), si se pidió la auditoría, corre sobre el borrador. Al
crear la tarjeta se verifica que su texto sea igual al archivo auditado (comparando el texto
sin etiquetas y con los espacios normalizados, con los `[T-nn]` ya reemplazados por su `#ID`):
si es igual, se publica el sello con la revisión que quedó; si no, la tarjeta queda **sin
sello**, y eso no frena nada.

### 4. Reportar
Devolver el **ID/URL** del work item creado o actualizado y qué campos quedaron
escritos. Ir al grano (silencio al entregar). Registrar **una fila** en
[[historial/INDICE]] (tema, `#ID`, documento fuente si aplica, resumen de una línea,
puntos): log resumido e indexable, sin copiar el cuerpo del ticket. El `.md`
detallado solo si se promueve a `gold`.

## Barreras (no negociables)

- **GATE de TABLERO (duro).** Solo se escribe en el tablero autorizado (org `{{AZURE_ORG}}` · proyecto `{{AZURE_PROYECTO}}` · team `{{AZURE_TEAM}}`). Antes de `create_work_item`/`update_work_item`, verificá el destino; si es otro tablero o no se puede determinar, **no escribas** y mostrá la advertencia. Detalle: [[tablero-autorizado]].
- **GATE de TARJETA CONGELADA (duro) — se chequea antes que los demás.** Antes de cualquier `update_work_item`, leer `System.IterationPath` y `System.State`. Si la tarjeta está **en un sprint y ya tomada** (Estado distinto de `New`), **no se edita**: ni con uno ni con dos "sí". Lo que se quería cambiar se ofrece **como comentario** con el DIFF, vía [[comentar-tarea]], y aplicarlo lo decide una persona. **Si no se puede leer el sprint o el estado, está congelada.** Detalle: [[cambios-en-el-backlog]] §4.
- **Un solo work item.** Esta skill crea/edita **el** ítem pedido. Para bajar un
  árbol entero (Épica→Features→Historias) es [[sincronizar-backlog]]; para las Tareas de
  una o más Historias, [[planificar-lote]], que aplica esta skill ítem por ítem con un solo
  cierre. Nunca expandir un pedido de un ítem a varios.
- **GATE de deduplicación (duro).** Antes de `create_work_item` se busca por tag + doc fuente + objetivo (comparando **objetivo/alcance, no título**) y el preview lleva el **Bloque de dedup** obligatorio (consultas · candidatos · veredicto); **sin ese bloque no se escribe**. **Ante la duda, es duplicado:** solapa plausible → preguntar, nunca crear. **Nunca** se crea un repetido. Detalle: [[deduplicacion-antes-de-crear]].
- **GATE de EXISTENCIA (bloqueante — encontrar ≠ crear igual).** Si la búsqueda arroja un ticket **equivalente o solapado**, encontrarlo **obliga a frenar**, no a seguir: (1) queda **PROHIBIDO `create_work_item`** para ese ítem; (2) se presenta la lista de existentes (`#ID` + link + estado); (3) se **pregunta explícitamente** si ACTUALIZAR (`update_work_item`) el existente o modificar algo, y se **espera el "sí"**. Jamás se crea un ítem nuevo en paralelo a uno que ya existe. Esta barrera es distinta de "buscar": buscar y encontrar sin frenar es la falla que este gate prohíbe.
- **GATE de NIVEL (bloqueante).** El **tipo** ya viene decidido en [[redactar-tarea]]
  por su tabla **SELECCIÓN DE TIPO (señal objetiva)**; acá se **verifica que sea
  coherente** y no se cambia en silencio. Crear un work item tipo **Tarea** obliga a
  **frenar y confirmar en su propio turno** (en modo lote, el turno de arranque de
  [[planificar-lote]], con la pregunta que nombra las Historias): *«¿esto es contexto dev/planning y esta
  Tarea es técnica, para un dev?»* — un "creá la tarea" **no** alcanza por sí solo como
  declaración. Sin ese "sí" explícito sobre el nivel, **no se crea**: se retiene y se
  pide la declaración (o se propone la Historia que la engloba). Toda Tarea que se cree
  usa la **plantilla detallada** ([[plantillas/tarea]]) con **Contrato técnico**,
  validaciones, casos de error, **Especificación cerrada (SDD)** —con la tabla que mapea
  los **Escenarios del Gherkin de la Historia padre** a los tests— y la lista numerada de
  **Tests a escribir PRIMERO**, más el bloque **Modos de falla evaluados** (una línea por
  familia: cubierta por un test, o descartada con su motivo) — obligatorio si capa
  `api`/`application`/`domain`; es el DoR de [[redactar-tarea]] §3.1, las **cuatro** piezas.
  El default es funcional (Épica/Feature/Historia).
- **[[analizar-tareas]] sobre el conjunto: sólo si se pide** (decisión de diseño del template). No
  corre sola ni frena. Si se pide, corre sobre **todas las hermanas** de la Historia, aunque
  se esté cargando una sola Tarea: es el lugar donde se chequea que **cada Escenario de la
  Historia esté cubierto** y que las coberturas parciales sumen. Lo que aparezca sale **como
  pregunta**, y si no se contesta queda como pendiente a confirmar en la tarjeta (en modo
  lote: lo que resuelve una fuente se corrige con la fuente a la vista, y el resto va al
  cierre).
- **GATE de confirmación — proponer y crear son turnos distintos.** Mostrás el
  preview y esperás; **nunca** proponés y escribís en el mismo turno. El "sí" es por
  operación y por sesión (o por el lote mostrado en el cierre de [[planificar-lote]]); no se
  generaliza una aprobación a la siguiente carga.
- **GATE de BORRADO y EDICIÓN DESTRUCTIVA (duro) — el nivel lo fija el daño.**
  - *Aditivo* (agregar contrato, comentar, pasar a Active, sumar relación): **un** "sí".
  - *Destructivo* (pisar una Descripción/Criterios ya escritos, **vaciar** un campo con
    contenido, Estado terminal *Closed*/*Resolved*): **DOS** "sí" en turnos distintos,
    con el **ANTES y el DESPUÉS** a la vista entre uno y otro. `update_work_item` que
    reemplaza contenido existente **no** es aditivo: cae acá. *Excepción del modo lote:*
    pisar la Descripción o los Criterios de una tarjeta en `New`, sin asignar o asignada a
    quien confirma, con el ANTES guardado y la fila marcada **PISA**, se confirma con el "sí"
    del cierre ([[AGENTS]]). Vaciar un campo y el Estado terminal, nunca en el lote.
  - *Cerrar una Tarea* (*Resolved*/*Closed*): el **primer** aviso lleva los pendientes sin
    resolver de sus comentarios y de su «Datos a confirmar» ([[comentar-tarea]] §«Antes de
    cerrar una Tarea»). Si está congelada, no se cierra desde acá: la cierra una persona.
  - *Borrado* (mover a *Removed* / `delete`): **DOS** "sí", mostrando **qué se borra**
    (título, estado, hijos, relaciones). Solo borrado **reversible** (papelera). El
    **destroy permanente NO lo hace esta skill nunca**: se le pasan los pasos al humano.
  - Las preguntas, **siempre en criollo entendible para funcional o dev** — nunca una
    confirmación técnica que el lector no pueda evaluar (ver el GATE de BORRADO en AGENTS.md).
- **PHI prohibido.** No subir datos personales sensibles/personales reales; van con marcadores
  (`<persona>`, `<documento>`, …).
- **Provenance / autoría.** La escritura queda auditada por el dueño del PAT; no
  usar un PAT ajeno. El token es una **password**: si se expone, se **rota**.
- **No inventar.** Si el ticket tiene un `⚠` **sin declarar** —un valor dudoso afirmado como
  dato, o un pendiente que cambia un test y no figura en «⚠ Datos a confirmar» ni marcado en
  ese test—, no se carga: se vuelve a [[redactar-tarea]] a cerrarlo. Un `⚠` **declarado** (en
  «Datos a confirmar», con su pregunta o su `P-nnn`, su recomendación y la marca en el test)
  es un punto abierto a la vista, y se carga ([[AGENTS]]).

## Contexto adicional

- Setup del MCP y el PAT: [[integracion-azure-mcp/00-index]]
- Mapa de campos del board (qué campo del ticket va a qué campo de Azure):
  [[checklists/mapa-campos-azure]]
- Redacción previa del ticket: [[redactar-tarea]]

---

### Ejemplo (genérico)

> Tras redactar el bug de un listado, el usuario pide "cargalo al tablero". La skill
> arma el preview: tipo **Bug**, título, *Pasos para
> reproducir*, *Gravedad `2-High`*, con `<documento>` como marcador. Pregunta
> "¿Creo la tarjeta con estos campos?". Recién con el "sí" llama a
> `create_work_item` y devuelve el `#ID` y la URL. Si el PAT del usuario fuera solo
> de lectura, en cambio, no escribe: entrega el texto para pegar a mano.
