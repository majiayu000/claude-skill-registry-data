---
name: analizar-tareas
description: >-
  (Solo análisis, no escribe) Chequear la CONSISTENCIA del conjunto de Tareas que salió de
  partir una Historia (el paso "analyze"): que los Contratos OpenAPI no se pisen entre Tareas,
  que cada regla [RN-…] y cada ESCENARIO del Gherkin de la Historia tengan una Tarea que los
  cubra y un test que los verifique (cierre del loop BDD↔TDD), que no haya huecos ni solapes, y
  que una Tarea que declara "requiere test de integración" realmente lo pida en sus tests y en
  su DoD. Usar cuando se pida "analizá las tareas", "chequeá que el set de tareas sea
  coherente", "corré el analyze antes de cerrar la reunión", "/analizar-tareas". Es OPCIONAL:
  corre sólo si se pide, antes de confirmar el alta, y no frena nada: lo que encuentra lo
  devuelve COMO PREGUNTAS y, si no se contestan, queda como pendiente a confirmar en la
  tarjeta. NO inventa, NO escribe en el board. Español (Argentina).
---

# Analizar tareas

Toma el **conjunto de Tareas** que derivó una Historia (propuestas en el preview, o ya
en el board) y verifica que **cierren entre sí** antes de crearlas. Es el paso
`analyze`: no juzga una Tarea aislada (eso lo hace el DoR de [[redactar-tarea]] §3.1),
juzga **el set completo**.

Es una skill de **solo análisis**: lee y reporta. No crea ni edita work items.

## Regla de oro (cultura del equipo)

- **NO decidir en silencio.** Todo choque, hueco o duda se devuelve **como pregunta**
  al humano, con la evidencia. Nunca se resuelve inventando.
- **En modo lote ([[planificar-lote]]) cada hallazgo sale marcado F o P.** **F**: lo
  resuelve una fuente (una regla del Cerebro, la maqueta vigente, una respuesta del humano,
  el contrato de otra Tarea), y se escribe **cuál** y **el arreglo exacto**: lo aplica el que
  redactó, sin preguntar, y queda listado en el cierre. **P**: necesita a una persona, y va al
  cierre como pregunta con recomendación. Un F sin su fuente escrita es un P.
- **NO INVENTAR.** Si falta contexto para juzgar (una `[RN-…]` que no está en el
  Cerebro, un contrato incompleto), se marca `⚠ pendiente` y se pregunta.
- **NO escribe.** Esta skill no toca el board; solo produce el reporte. El alta la
  hace [[sincronizar-backlog]] después del "sí", ya con los choques resueltos.
- **Español (Argentina)**, sin emojis como íconos.

## Qué chequea (sobre el conjunto)

1. **Contratos que no se pisan.** Dos Tareas no pueden definir el **mismo endpoint**
   (`método` + `ruta`) con contratos distintos. Si dos fragmentos OpenAPI colisionan,
   es choque → preguntar cuál vale.
2. **Cobertura de reglas.** Cada `[RN-…]` que la Historia declara debe estar cubierta
   por **al menos una** Tarea (en una validación, un caso de error o un test). Una
   `[RN-…]` sin Tarea es un **hueco** → preguntar a qué Tarea va.
3. **Sin huecos de alcance.** Cada comportamiento/criterio de la Historia debe tener
   su Tarea. Algo de la Historia sin Tarea → hueco.
4. **Sin solapes.** Dos Tareas que hacen **el mismo trabajo** (mismo contrato, misma
   capa) → solape; proponer fusionarlas o delimitarlas → preguntar.
5. **Consistencia de errores/formas.** Códigos y payloads de error coherentes entre
   Tareas que se consumen entre sí (el `404`/`409` que una devuelve, la otra lo espera).
6. **Dependencias resueltas.** Si una Tarea `depende de` otra, esa otra existe en el
   set (o ya en el board); si no, es una dependencia colgada → preguntar.
7. **Cobertura de Escenarios (cierre del loop BDD↔TDD).** Cada **Escenario** del Gherkin
   de la Historia padre (campo Criterios de aceptación) debe aparecer en la tabla
   «Escenarios de la Historia que esta Tarea cubre» de **al menos una** Tarea, y ahí
   debe decir **qué test lo verifica** (la línea «No cubre» al pie de la tabla dice quién lo
   cubre, pero no cuenta como cobertura). Chequear estas formas de falla:
   - Escenario del padre que **ninguna** Tarea tiene como fila (aparecer sólo en «No cubre» no
     cuenta) → **hueco** → preguntar a qué Tarea va. Si el «No cubre» de una Tarea nombra a otra
     que no lo tiene como fila, el puntero es falso → **hueco**.
   - Escenario mencionado **sin** test que lo verifique (columna vacía) → el loop no cierra.
   - Título de Escenario que **no coincide textual** con el del padre → no se puede rastrear;
     pedir que se copie igual.
   - **Cobertura parcial que no suma** (el caso que más se escapa): si una Tarea declara cubrir
     **solo parte** de un Escenario, tiene que existir la Tarea complementaria **y entre todas
     las partes declaradas tiene que quedar el Escenario completo**. Dos formas de falla:
     (a) declara parcialidad y la Tarea complementaria no existe → hueco;
     (b) el Escenario necesita back **y** front y **una sola** Tarea dice cubrirlo entero →
     sospechoso: preguntar si de verdad lo cierra sola. «Al menos una Tarea lo menciona» **no**
     alcanza como prueba de cobertura.
   - **Quién prueba la unión.** Cuando un Escenario se reparte entre dos Tareas, cada una da
     verde por su lado (el front con su simulación del contrato, el back con sus tests) y **nadie corre las dos
     juntas**. Eso no lo tapa «Requiere test de integración», que por definición es para
     dependencias **externas** ([[plantillas/tarea]]). Reportarlo como pregunta abierta:
     *«¿quién verifica este Escenario de punta a punta, y en qué Tarea vive ese test?»*
   Este es el chequeo que evita que BDD y TDD queden como dos listas sueltas que nadie une.
8. **Coherencia del test de integración.** Si una Tarea declara «Requiere test de
   integración: **sí**», tiene que tener **un test de integración en la lista, una subtarea
   que lo escriba y un ítem en el DoD**. Si declara `sí` y los tests son todos contra dobles,
   es un **defecto silencioso** (el dev cierra la tarea sin haberlo probado nunca de verdad)
   → reportarlo. Al revés también: si hay un test de integración pero arriba dice `no`,
   una de las dos cosas está mal → preguntar cuál.
9. **Campos que no quedan nulos en silencio.** `Esfuerzo original` y `Actividad` presentes en
   cada Tarea. Si no hay estimación, va **0** más la pregunta en «Datos a confirmar» — nunca
   vacío: un campo nulo no se distingue de «nadie lo miró» y no suma al sprint.

## Flujo

### 1. Reunir el conjunto
Tomar las Tareas a analizar: las **propuestas** en el preview de [[sincronizar-backlog]],
o las que ya están en el board bajo una Historia (por MCP, **solo lectura**). Leer
también la **Historia padre** y sus `[RN-…]` (referencia, no copia).

### 2. Correr el script, y después los chequeos de criterio
**Primero el script**, que lo corre esta skill:

```
python bin/analizar-tareas.py --historia <criterios-del-padre.html> [--descripcion <descripcion-del-padre.html>] <tarea-1.html> <tarea-2.html> ... --json
```

Hace lo que es **conteo**:
- cada Escenario con una Tarea que lo tiene como fila (la línea «No cubre» no cuenta);
- que los «No cubre» no apunten a una Tarea que no lo cubre;
- cada regla de la Historia en alguna Tarea;
- endpoints repetidos con contratos distintos;
- el test de integración.

Eso no se rehace a mano. Si no corrió, esos chequeos son SIN DATOS. Si la herramienta no puede
correr comandos, se le pide a la persona ese comando exacto. Después, aplicar **sólo** lo que el
script lista en «Lo que este script NO mira» y confirmar o descartar sus AVISOS. Hoy eso es:
solapes de trabajo, comportamiento de la Historia sin Tarea, coherencia de errores entre Tareas
que se consumen, coberturas parciales que no suman, quién prueba la unión, el test de
integración contra dobles y los campos de Azure. Para cada hallazgo, guardar la **evidencia**
(qué Tareas, qué contrato/regla, qué línea).

### 3. Reportar como preguntas
Devolver un reporte agrupado por tipo de hallazgo. Cada ítem: qué se detectó +
evidencia + **la pregunta al humano** (nunca una decisión tomada). Si no hay
hallazgos, decirlo en una línea: "el set cierra, sin choques".

### 4. No avanzar solo
El reporte **no** dispara ningún alta. Cierra el turno. La creación de las Tareas la
retoma [[sincronizar-backlog]] con las respuestas del humano ya incorporadas.

**En modo lote** el reporte no cierra un turno propio: alimenta el **cierre** de
[[planificar-lote]], donde los F aparecen como aplicados y los P como preguntas.

## Barreras

- **Solo lectura del board.** Si consulta el board, usa herramientas de lectura del
  MCP; nunca `create_work_item`/`update_work_item`.
- **Analizar y crear son turnos distintos** (en modo lote, el turno del cierre es el que separa los dos).
- **PHI prohibido** en el reporte (marcadores `<persona>`, `<documento>`, etc.).

## Contexto adicional

- DoR de una Tarea suelta (no del set): [[redactar-tarea]] §3.1
- Derivar/crear las Tareas tras resolver los choques: [[sincronizar-backlog]]
- Plantilla y contrato de la Tarea: [[plantillas/tarea]]
- Mapeo y trazabilidad: [[organizacion-y-trazabilidad]]

---

### Ejemplo (genérico)

> Se partió la Historia "Suspender una serie" en 3 Tareas: (api) `POST
> /series/{id}/suspender`, (application) caso de uso `SuspendSerie`, (domain) invariante
> "una serie suspendida no admite servicios con fecha >= hoy". `analizar-tareas`
> reporta: la `[RN-MOD-03]` está cubierta por la Tarea de domain (ok); pero el `409
> SERIE_YA_SUSPENDIDA` aparece en el contrato de la Tarea api y **no** hay test que lo
> cubra en la lista test-first → **pregunta**: "¿agrego el caso 409 a los tests de la
> Tarea api, o queda fuera de alcance?". No crea nada; deja la pregunta para la reunión.
