---
name: planificar-lote
description: >-
  (Modo lote / planificación rápida) Derivar en una sola pasada, con agentes en
  paralelo, las Historias de una ficha del Cerebro, las Tareas de varias Historias,
  o las dos cosas, con SOLO DOS turnos humanos: el ARRANQUE (alcance + nivel + todas
  las dudas sin fuente, juntas y con recomendación) y el CIERRE (una tabla con el lote
  entero y UN "sí" que escribe todo: altas, relaciones, ediciones de tarjetas en New,
  sellos de auditoría si se pidió alguna, y la traza en el Cerebro). Lo que definen la
  maqueta vigente o el Cerebro se aplica sin preguntar y se lista. Las auditorías son
  OPCIONALES: corren sólo si se piden (entonces las corre un agente distinto, en
  paralelo) y nunca frenan una fila. Los GATES duros (tablero, nivel, dedup, tarjeta
  congelada, PHI, borrado) siguen iguales. Usar cuando se pida "armá las tareas de
  estas historias", "planificación con los devs", "derivá las historias de la ficha",
  "bajá el lote", "/planificar-lote". NO inventa. Español (Argentina).
---

# Planificar lote

> **Tablero local (`DEC-006`):** si el proyecto usa el tablero local, «el board» es `cerebro-digital/<modulo>/backlog/`
> y se opera con `bin/tablero-local.py`, con los mismos GATEs y sin MCP (detalle: `backlog/README.md` del módulo).
> Con Azure DevOps, Jira u otro tablero, las operaciones se traducen con la tabla de `integracion-azure-mcp/00-index.md`.

Baja **muchos ítems de una vez** —las Historias de una ficha, las Tareas de varias
Historias, o las dos cosas— con dos turnos humanos en lugar de decenas.

> **Por qué existe.** En el proyecto de origen, las Tareas de una Feature (5 Historias,
> 13 Tareas) llevaron **más de cuatro horas** con los devs: contadas sobre las reglas, el flujo
> pedía más de treinta confirmaciones en turnos separados (el nivel por Historia, el análisis
> del set, cada preview, cada sello, cada edición), y además se preguntaba lo que la maqueta y
> el Cerebro ya decían. Ninguna de esas vueltas agregaba control: el control está en los
> GATES duros, y esos quedan; las auditorías independientes pasaron a ser opcionales, a pedido
> (decisión de diseño del template). **Objetivo: ese mismo
> lote en 30 a 40 minutos.**

## Cuándo se usa y cuándo no

| Pedido | Skill |
|---|---|
| Las Tareas de **una o más** Historias ("armá las tareas de F-04 a F-08") | **esta** |
| Las Historias de una ficha, con o sin sus Tareas | **esta**, con la cardinalidad 1:1 de [[sincronizar-backlog]] |
| **Un** ítem suelto | [[redactar-tarea]] + [[cargar-a-azure]] |
| La ficha no tiene el bloque `## Derivación a backlog` cerrado | No se deriva: va a curación ([[cognitive-doc-design]]) |
| Corregir una tarjeta congelada | [[comentar-tarea]] (sólo comentario) |

## Lo que no cambia (ver [[AGENTS]])

- **Tablero autorizado.** Sin MCP, los GATES que leen el tablero dicen **SIN DATOS** y no se escribe.
- **Dedup por ítem.** Un equivalente **bloquea el alta** de ese ítem; un candidato dudoso es pregunta del arranque.
- **Tarjeta congelada** (en un sprint y distinta de `New`): sólo comentario.
- **PHI prohibido**, un solo tag temático, HTML.
- **El lote no borra ni cierra** tarjetas. Eso sigue con dos "sí" y fuera del lote.
- **Las auditorías son opcionales** (decisión de diseño del template): [[auditar-historia]], [[auditar-tarea]] y [[analizar-tareas]] corren **sólo si se piden** —en el pedido o en la respuesta del arranque—, y entonces las corre un agente distinto del que redactó. **Nunca frenan una fila**: lo que encuentren va como **pendiente a confirmar** en la tarjeta ([[comentar-tarea]] §«Pendientes a confirmar»), y el sello no es requisito para desarrollar.
- **No inventar.** Lo que ninguna fuente define se pregunta en el arranque o queda como `⚠` declarado.

## Qué se decide sin preguntar (fuentes, en orden)

| # | Fuente | Qué decide |
|---|---|---|
| 1 | **El Cerebro** (`[RN-…]`, `[DEC-…]`, pendientes resueltos, decisiones del día en la ficha) | Reglas, estados, datos, decisiones ya tomadas |
| 2 | **La maqueta vigente**: la que la ficha cita en `fuente_maqueta` | Comportamiento de pantalla: textos, botones, avisos, estados vacíos, formatos, orden de campos, paginación. Una maqueta «propuesta» o que ninguna ficha cita no decide. **Si contradice una regla del Cerebro, gana el Cerebro** y se avisa en el cierre |
| 3 | **Lo que el humano ya respondió**, en esta conversación o en el arranque | Lo respondido no se vuelve a preguntar |
| 4 | **Los contratos ya cargados** (Tareas hermanas, el back que consume el front) | Nombres, códigos, formas |
| 5 | **La recomendación técnica** de la IA, cuando hay una clara | Partición, nombres internos (clases, rutas, nombres de test), patrones del esqueleto. Se aplica y se lista para que el humano la vete. **No decide** códigos HTTP, códigos de error, números de regla ni valores de negocio, y no se guarda en el Cerebro como decisión |

**Se pregunta sólo:** (a) un dato duro sin fuente (`#ID`, versión, valor real, código de un
sistema externo); (b) una regla o un comportamiento que ninguna fuente define **y que cambia
un test o un Escenario**; (c) un choque entre dos fuentes del mismo rango.

## Las cinco fases

### Fase 0 — Preparar (la IA sola; en paralelo)

0. **Lo primero:** `python bin/lote.py preparar <tema> --ficha <ficha>` y `python bin/lote.py tiempos <carpeta> preparar inicio`, así la fase se mide entera (ver el paso 6).
1. Verificar el tablero autorizado y leer las tarjetas involucradas (Estado, Ruta de iteración, Asignado).
2. Leer las fuentes: la ficha y su bloque de derivación, la maqueta, las reglas, los contratos ya cargados.
3. **Dedup por ítem** con [[consultar-backlog]] (tag + documento fuente + objetivo).
4. **Tareas, sólo si se pidió auditoría:** correr [[auditar-historia]] sobre cada Historia padre, **un agente por Historia, en paralelo**. Si no se pidió, este paso no corre.
5. Clasificar cada duda —propia o, si corrieron, de las auditorías— en **F** (la resuelve una fuente: se anota cuál y el arreglo exacto), **R** (recomendación técnica clara) o **P** (necesita a una persona).
6. `python bin/lote.py preparar` (paso 0) crea `borrador/lote-<AAAAMMDD>-<tema>/` con el esqueleto de `CONTEXTO.md`, `items.json` y `tiempos.json`. Cada ítem se anota con `python bin/lote.py item <carpeta> --clave T-01 --tipo Tarea --accion ALTA --titulo "…" --padre "#NNNNN" …`. En `CONTEXTO.md` van el alcance, las fuentes leídas (rutas), lo decidido por F y R con su fuente, las P con su recomendación, la dedup por ítem y el estado de cada tarjeta a editar.

**El lote lo maneja el script, no la memoria de la sesión.** Las carpetas, las misiones de los sub-agentes, las auditorías mecánicas (si se piden), la tabla del cierre y la verificación antes de sellar salen de `bin/lote.py`. Así dos sesiones distintas hacen el mismo lote igual. Cada fase se marca con `python bin/lote.py tiempos <carpeta> <fase> inicio|fin` —las fases son `preparar`, `arranque`, `redactar`, `auditar`, `cierre` y `escribir`—, y el informe de tiempos va al reporte final. La skill corre estos comandos sola; sólo si la herramienta no tiene terminal le pasa a la persona el comando exacto.

### Fase 1 — Arranque (UN turno humano)

Un solo mensaje, en criollo:

1. **Alcance:** qué se va a crear o editar, una línea por ítem.
2. **Nivel**, si hay Tareas: *«¿Estas Tareas son técnicas, para los devs (contexto dev/planning)? Vale para las Historias #A, #B y #C.»* Una Historia que todavía no existe se nombra con su `[H-nn]` y su título.
3. **Duplicados:** candidatos encontrados (o «0 candidatos en N consultas») y qué se propone.
4. **Preguntas:** todas las P, numeradas, cada una con «Recomiendo: …».
5. Una línea: *«Lo demás sale de la maqueta y del Cerebro; te lo listo en el cierre.»*
6. Una línea, sin pregunta: *«No corro auditoría salvo que me la pidas.»* (Si ya la pidieron en el pedido, se dice que va a correr.)

El mensaje **cierra el turno**: no se redacta nada antes de la respuesta. Si el lote **no tiene
Tareas, ni preguntas, ni duplicados dudosos**, el arranque no se muestra y se pasa a la fase 2.

La respuesta vale entera: «dale», «tu recomendación» o «sí a todo» acepta las recomendaciones
de las preguntas numeradas. **La pregunta del nivel no lleva recomendación y no se da por
contestada con «tu recomendación»**: vale un «sí», «dale» o «sí a todo» dado a ese mensaje.
Una pregunta que quedó sin contestar **no se vuelve a hacer en otro turno**: queda como `⚠`
declarado en la tarjeta, con su recomendación, y se vuelve a listar en el cierre. **Dos
excepciones, porque son GATES:** sin respuesta al nivel, las Tareas de esas Historias **no se
redactan** (el lote sigue sin ellas); y un duplicado dudoso sin respuesta **no se crea**: sale de
la tabla y va al cierre como pregunta.

### Fase 2 — Redactar (un agente por Historia, en paralelo)

- **Misión de cada agente:** es la que imprime `python bin/lote.py mision <carpeta> redactar <clave>`, y no se escribe a mano. El molde (`misiones/redactar.md`) ya trae el objetivo y las rutas (`CONTEXTO.md`, ficha, maqueta, Historia padre). También trae las skills, que no se heredan y hay que pasarlas: [[redactar-tarea]], [[plantillas/tarea]] o [[plantillas/historia-de-usuario]], [[checklists/mapa-campos-azure]] y [[estimar-story-points]].
- **Salida** en la carpeta del lote: `<clave>.html` (Descripción) y, si es Historia, `<clave>-criterios.html`; más `<clave>.json` con título, tipo, padre, puntos, actividad y relaciones.
- Lo que todavía no existe se referencia con **`[T-nn]`** o **`[H-nn]`**: en la fase 5 se reemplaza por el `#ID`.
- Las Tareas siguen el tamaño de [[plantillas/tarea]] §«Tamaño y forma»: **30 tests o menos** (si no alcanza, se parte la Tarea), **una línea por test**, sin repetir texto entre secciones.
- **Si el lote también redacta o pisa la Historia**, sus Tareas se redactan **después** del borrador de la Historia (y, si se pidió auditoría, después de que [[auditar-historia]] corrió sobre él y se aplicaron sus F): las Tareas mapean sus Escenarios.
- **Cada redactor corre el checklist de forma §2b** de [[cargar-a-azure]] sobre su borrador (`python bin/auditar-tarea.py` para una Tarea) y anota el resultado con `lote.py item <carpeta> --clave <clave> --gates "OK"` o `--gates "FRENA: <cuál>"`. No es la auditoría opcional: es el autochequeo de forma de quien escribe, y sin él la columna «GATES y §2b» sale SIN DATOS.
- **Los agentes no le preguntan al humano.** Lo que no pueden resolver lo devuelven como P en su reporte.
- Hasta 8 agentes a la vez. Un archivo, un solo escritor.
- **Si la herramienta no tiene sub-agentes**, las fases 2 y 3 corren en serie, y cada auditoría con contexto propio, sin el de la redacción. Los F los corrige quien redactó o, si ya no está, otro agente que no auditó esa pieza.

### Fase 3 — Auditar (OPCIONAL: sólo si se pidió; agentes distintos de los que redactaron, en paralelo)

**Si nadie pidió auditoría, esta fase no corre** y se pasa al cierre: la columna «Auditoría»
dice *no se pidió* y ninguna fila se frena por eso. Si se pidió, corre así:

| Qué | Skill | Sobre |
|---|---|---|
| Cada Tarea | [[auditar-tarea]] | El archivo del borrador + la Historia padre como va a quedar + las reglas |
| El set de cada Historia | [[analizar-tareas]] | Todas sus Tareas, nuevas y ya cargadas |
| Cada Historia redactada o corregida en el lote | [[auditar-historia]] | El borrador + la ficha |

- **Primero el script:** `python bin/lote.py auditar <carpeta>` corre `auditar-tarea.py`, `auditar-historia.py` y `analizar-tareas.py` sobre todos los borradores, en orden fijo, y deja `auditorias/<clave>.md`. Lo que cuenta el script no lo vuelve a contar un agente.
- **Después, un agente auditor por ítem**, con la misión de `python bin/lote.py mision <carpeta> auditar <clave>`. Revisa **sólo** lo que el script lista en «Lo que este script NO mira» y confirma o descarta sus AVISOS. Su informe va a `auditorias/<clave>-auditor.md`, con una línea `Veredicto:` y una `Huella:`: si el archivo cambió después, el cierre marca la fila **NO SE SELLA** (se escribe igual, sin sello) hasta que se re-audite.
- **Y un auditor por conjunto** (las Tareas de cada Historia), con `python bin/lote.py mision <carpeta> auditar set-<padre>`, que deja `auditorias/set-<padre>-auditor.md`. Las Tareas que ya están en el tablero entran al conjunto con `lote.py item … --accion EXISTE --archivo <guardado>`: se analizan, pero no se escriben. Si el conjunto dio hallazgos, las Tareas lo dicen en la columna «Auditoría» y los hallazgos van como pendientes; si el análisis del conjunto no cierra (sin informe, vencido, SIN DATOS), sus Tareas salen **NO SE SELLA**. Ninguno de los dos frena la fila.
- Cada hallazgo sale marcado **F** o **P**. Los **F** los corrige el agente que redactó (no el auditor), sin preguntar, con la misión de `lote.py mision <carpeta> corregir <clave>`, y quedan listados en el cierre. Los **P** van al cierre.
- **Re-auditoría:** sólo de lo que cambió, por un agente distinto, **una vez**. Si sigue CON HUECOS, va así al cierre, marcado: se carga igual, su sello dirá CON HUECOS y sus hallazgos van como pendientes a confirmar. **No frena el desarrollo.**
- **Ninguna auditoría frena una fila.** Si una auditoría pedida no cierra —quedó vieja porque el archivo cambió, el informe no dice veredicto, o el auditor contradice al script—, la fila dice **NO SE SELLA**: se escribe igual, sin sello.

### Fase 4 — Cierre (UN turno humano)

Un solo mensaje con lo que escribe `python bin/lote.py cierre <carpeta>` en `CIERRE.md`, mostrado tal cual. La tabla sale de los archivos y de las auditorías que se hayan pedido, no de la memoria. Una fila sin el ANTES de un PISA, o sin dedup en un ALTA, sale **FRENA** y no se escribe. La auditoría **nunca** frena: dice *no se pidió*, su veredicto, o **NO SE SELLA** si se pidió y no cierra. El mensaje trae:

1. **La tabla del lote:**

   | # | Acción | Ítem | Padre | Puntos | GATES y §2b | Auditoría | `⚠` abiertos | Dedup | Archivo |
   |---|---|---|---|---|---|---|---|---|---|
   | 1 | ALTA / **PISA** / RELACIÓN | título | `#ID` o `[H-nn]` | n | OK / FRENA: cuál / SIN DATOS | no se pidió / COMPLETA / CON HUECOS / NO SE SELLA: por qué | P-nnn | N consultas · 0 cand. / `#ID` | ruta |

   «GATES y §2b» resume el Bloque de GATES y el checklist de cierre de [[cargar-a-azure]] de ese
   ítem; el detalle queda en su archivo. Una fila con FRENA o SIN DATOS no se escribe.

2. **Aplicado sin preguntar:** una línea por decisión, con su fuente (maqueta, regla, respuesta del arranque, recomendación).
3. **Lo que se pisa:** por cada fila PISA, qué cambia en dos líneas y dónde quedó el ANTES (`borrador/lote-…/antes/<id>.html`).
4. **Conocimiento para el Cerebro:** lo que fijaron las respuestas del arranque (decisiones del día, reglas, pendientes nuevos o resueltos), con su destino. El "sí" lo guarda; lo que el humano tache, no.
5. **Preguntas que quedaron** (P de las auditorías, si corrieron), con recomendación, **por tarjeta**. Las que no se contesten quedan como **pendientes a confirmar** en su tarjeta: no frenan. Esta lista es exactamente lo que se postea en el paso 9 de la fase 5.
6. Una línea sobre los sellos: *«Las tarjetas con auditoría llevan su sello, y sus hallazgos van como pendientes a confirmar (molde de [[comentar-tarea]]).»*, o *«Auditoría: no se pidió. Ninguna tarjeta lleva sello.»*
7. La pregunta: *«¿Escribo todo el lote?»*

**El "sí" cubre exactamente lo que está en el mensaje del cierre**: la tabla, los sellos (si
hubo auditoría), los comentarios de pendientes y el conocimiento para el Cerebro. Si la respuesta cambia o tacha un ítem («sí, pero en la 3 hacé
X»), se escribe el resto, y ese ítem —con lo que depende de él: las Tareas de una Historia que
no se pisa o no se crea, las relaciones que lo nombran— se rehace, se re-audita si hubo auditoría, y se muestra en
un turno más, solo.

### Fase 5 — Escribir y verificar (la IA, con el "sí")

1. **Releer** cada tarjeta que el lote edita o de la que cuelga algo (Estado, Ruta de iteración, Asignado, `System.Rev`). Si cambió desde la fase 0 —la tomó alguien, entró a un sprint, otra mano editó el texto—, esa fila y lo que depende de ella **no se escriben**, y se informa. Antes de las altas se repite la búsqueda de duplicados, rápida: el lote dura media hora y alguien pudo crear lo mismo.
2. **Ediciones** (filas PISA), con el ANTES ya guardado.
3. **Altas de Épicas, Features e Historias**, padre antes que hijo.
4. **Si hubo auditoría, verificar y sellar cada Historia** auditada en el lote cuya columna «Auditoría» trae un veredicto (no *no se pidió* ni NO SE SELLA): su texto en Azure tiene que ser igual al borrador auditado (comparando el texto **sin etiquetas** y con los espacios normalizados: Azure reescribe el HTML), y el `Rev auditado` es la revisión verificada. Una Historia que el lote no tocó se sella con la revisión que leyó la auditoría, y sólo si no cambió desde entonces.
5. **Altas de Tareas** (`create_work_item` con `parentId`); en paralelo.
6. **Reemplazar `[T-nn]`/`[H-nn]`** por su `#ID` en las Descripciones: es el mismo contenido mostrado, con el número que faltaba. Lo hace `python bin/lote.py ids <carpeta> --mapa mapa-ids.json`, que escribe `<archivo>.final.html`: ése es el texto que se carga.
7. **Relaciones** (`manage_work_item_link`), siempre desde la tarjeta nueva.
8. **Si hubo auditoría, verificar y sellar cada Tarea** cuya columna «Auditoría» trae un veredicto (no *no se pidió* ni NO SE SELLA), con la misma comparación del paso 4 (en los dos pasos, se sella sólo si `python bin/lote.py comparar <auditado> <guardado-de-azure> --mapa mapa-ids.json` sale 0; si lo guardado es el JSON del work item, se agrega `--campo System.Description`): `Rev de la Tarea auditada` es la revisión verificada y `Rev de la Historia padre`, la del paso 4.
9. **Pendientes en las tarjetas:** las preguntas del arranque que quedaron sin contestar ya van como `⚠` en «Datos a confirmar» de la propia tarjeta, sin comentario aparte. Las **P de las auditorías** de una tarjeta, tal como se listaron en el punto 5 del cierre, van en su sello si lo lleva; si no lo lleva (NO SE SELLA), en un comentario «Pendientes a confirmar» ([[comentar-tarea]] §«Pendientes a confirmar»). Nada que no estuviera en el cierre.
10. **Traza:** «Tickets derivados» en la ficha y, en el Cerebro, **sólo** el «Conocimiento para el Cerebro» del cierre que el humano no tachó, escrito por `cerebro-curator`. Lo aplicado por recomendación técnica (R) **no** se escribe en el Cerebro como decisión: si no, el lote siguiente lo tomaría como fuente. Más una fila en [[historial/INDICE]] y la firma en `cerebro-digital/log.md`, en una rama `develop` (o la rama propia, si son dos); commit y push sólo si se piden.
11. **Reporte** corto: los `#ID`, lo que quedó abierto y dónde.

**Si una tarjeta auditada no pasa la verificación, no se sella:** va al reporte, y re-auditarla
es opcional. Sin sello se puede desarrollar igual.

**Si una escritura falla, se frena el lote.** Se informa qué quedó escrito y qué no, y antes de
reintentar un alta se busca por título que no se haya creado igual: un reintento ciego duplica.

## Tiempos esperados (lote de 5 Historias y 13 Tareas)

| Fase | Quién | Tiempo |
|---|---|---|
| 0. Preparar | IA, en paralelo | 5 min |
| 1. Arranque | Humano | 5 min |
| 2. Redactar | IA, un agente por Historia | 10 a 12 min |
| 3. Auditar (sólo si se pidió) | IA, agentes distintos | 0, o 5 a 8 min |
| 4. Cierre | Humano | 5 min |
| 5. Escribir | IA | 5 min |

Lo que más tarda es la revisión del humano en el cierre. Si se alarga, casi siempre es porque
volvieron P que la fase 0 no levantó: anotarlo en el log del lote para afinar la próxima.

## Archivos del lote (`borrador/lote-<AAAAMMDD>-<tema>/`, nunca versionado)

| Archivo | Qué es |
|---|---|
| `CONTEXTO.md` | El brief común: alcance, fuentes, decisiones y su fuente, preguntas |
| `items.json` | Los ítems del lote (lo arma `lote.py item`; `--desde-json` lo completa con `<clave>.json`) |
| `<clave>.html`, `<clave>-criterios.html`, `<clave>.json` | Cada ítem, tal como se va a escribir, y sus datos (título, puntos, actividad, relaciones) |
| `<clave>.final.html`, `<clave>-criterios.final.html` | Los mismos, con los `#ID` reemplazados (`lote.py ids`): es lo que se carga |
| `auditorias/<clave>.md`, `.json`, `.huella.json` | El chequeo mecánico del script y la huella de lo que auditó |
| `auditorias/set-<padre>.md` | El chequeo mecánico del conjunto de Tareas de una Historia |
| `auditorias/<clave>-auditor.md`, `auditorias/set-<padre>-auditor.md` | El informe del auditor (agente), con los F y los P y sus líneas `Veredicto:` y `Huella:` |
| `antes/<id>.html` | Lo que había en cada tarjeta que se pisa |
| `CIERRE.md` | La tabla del cierre, igual a la que se mostró (`lote.py cierre`) |
| `mapa-ids.json` | `[T-nn]` / `[H-nn]` → `#ID`, después de escribir |
| `tiempos.json` | Inicio y fin de cada fase (`lote.py tiempos`) |

## Barreras propias

- **Nada se escribe en el tablero ni en el Cerebro antes del "sí" del cierre.** Antes sólo se escribe en `borrador/`.
- **El "sí" no se generaliza** al lote siguiente.
- **Quien redacta no audita**, y **quien audita no corrige**: corrige el que redactó (cuando se pidió auditoría).
- **Un F sin su fuente escrita es un P.** Decidir en silencio sigue prohibido; lo que cambia es que se decide con la fuente a la vista y se lista.

## Contexto adicional

- Cardinalidad y traza del árbol: [[sincronizar-backlog]] · [[organizacion-y-trazabilidad]]
- Un ítem por vez: [[redactar-tarea]] · [[cargar-a-azure]]
- Auditorías: [[auditar-historia]] · [[auditar-tarea]] · [[analizar-tareas]]
- Sellos y comentarios: [[comentar-tarea]]
