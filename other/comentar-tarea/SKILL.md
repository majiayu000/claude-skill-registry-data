---
name: comentar-tarea
description: >-
  Agregar un comentario a un work item de Azure DevOps (queda en el Historial /
  Discusión de la tarjeta) y, si hace falta, leer los comentarios existentes. Usar
  cuando se pida "comentá en la #NNNN", "dejá una nota en la tarjeta", "respondé el
  comentario de X", "/comentar-tarea", al TERMINAR UN DESARROLLO (el comentario de
  cierre: rama, Merge Request, resumen técnico y pendientes a confirmar), para dejar un
  hueco o un gris como pendiente, y ANTES DE CERRAR una Tarea (revisar en sus comentarios
  los pendientes sin resolver). Es la
  única escritura que entra en una tarjeta congelada (en un sprint y ya tomada). Leer
  comentarios no requiere permiso; escribir el comentario se hace con confirmación.
  Español (Argentina), sin PHI.
---

# Comentar tarea (comentarios en Azure)

> **Tablero local (`DEC-006`):** si el proyecto usa el tablero local, «el board» es `cerebro-digital/<modulo>/backlog/`
> y se opera con `bin/tablero-local.py`, con los mismos GATEs y sin MCP (detalle: `backlog/README.md` del módulo).
> Con Azure DevOps, Jira u otro tablero, las operaciones se traducen con la tabla de `integracion-azure-mcp/00-index.md`.

Permite **leer** y **dejar** comentarios en un work item. En Azure DevOps el
comentario de una tarjeta se escribe en el campo **Historial / Discusión**
(`System.History`).

## Regla de oro
- **GATE de TABLERO (duro).** La tarjeta debe pertenecer al tablero autorizado (org `{{AZURE_ORG}}` · proyecto `{{AZURE_PROYECTO}}` · team `{{AZURE_TEAM}}`); antes de postear en `System.History` verificá el destino y, si es otro tablero, **no escribas** y mostrá la advertencia ([[tablero-autorizado]]).
- **Leer es libre; escribir con confirmación.** Antes de postear, mostrar el texto y a qué `#ID` va, y esperar tu OK — mostrar y postear son pasos distintos, no el mismo turno. **Los sellos de auditoría de un lote** ([[planificar-lote]]) se publican con el "sí" del cierre del lote: la tabla del cierre muestra el veredicto de cada tarjeta, y el sello es el molde fijo de abajo con esos valores.
- **Sin PHI** en el comentario (marcadores `<persona>`, `<identificador>`… en su lugar). **Español.**
- **No inventar:** si el comentario afirma un dato duro sin confirmar, marcarlo `⚠`.
- **Un comentario es sólo un comentario.** La escritura lleva `System.History` y **ningún otro
  campo**. Colar un cambio de Estado, de Etiquetas o de Descripción en la misma llamada es
  editar la tarjeta con otro nombre, y en una **tarjeta congelada** eso está prohibido
  ([[cambios-en-el-backlog]] §4).
- **Bien formateado, siempre** (ver «Formato», abajo). Un comentario que se lee como un muro
  no lo lee nadie, y entonces no avisa nada.

## Flujo
1. (Opcional) **Leer el hilo:** `get_work_item_comments` del `#ID`.
2. **Redactar** el comentario en español, sin PHI, **en HTML** con el molde que corresponda.
3. **Mostrar** el comentario **como se va a ver** —no el HTML crudo, que nadie puede evaluar— y
   la tarjeta destino (`#ID`).
4. Con tu **OK**, **postear**: `update_work_item` sobre el campo `System.History` —y sólo ese— (así queda en la discusión de la tarjeta).

> Nota: si el servidor MCP expone una herramienta específica para comentar un work
> item, se usa esa; si no, el mecanismo estándar de Azure es `System.History` vía
> `update_work_item`.

## Formato: que se lea bien en Azure

**Azure toma el comentario como HTML.** Un texto plano con saltos de línea llega **pegado en un
solo renglón**: Azure descarta los saltos. Y el markdown (`**`, `-`, `#`, las comillas
invertidas) se ve literal. Por eso todo comentario se arma en HTML, con las mismas etiquetas que
la Descripción ([[checklists/mapa-campos-azure]]):

| Para | Se usa | No se usa |
|---|---|---|
| El renglón de arriba, que dice de qué se trata | `<p><b>…</b></p>` | `<h1>` / `<h2>`: Azure ya pone el título de la tarjeta |
| Secciones | `<h3>`, con un `<hr>` antes de cada `<h3>` **que viene después de otro contenido** | Secciones pegadas: sin el `<hr>` no se ve dónde termina una |
| Prosa | `<p>` | Texto suelto entre etiquetas |
| Datos cortos (rama, commit, veredicto) | `<ul><li><b>Nombre:</b> valor</li></ul>` | Una línea larga con todo separado por `·` |
| Comparar cosas en columnas | `<table>`, con `<th>` en la fila de títulos | Espacios para alinear: en HTML se pierden |
| Líneas que lee una máquina (el sello) | Una por renglón, separadas con `<br>` | Cambiarles el texto |
| Marcadores (`<persona>`, `<veredicto>`) | `&lt;persona&gt;` | `<persona>` sin escapar: **el navegador se lo come** y desaparece sin aviso |

**Nada de estilos inline** (`style=`, colores, tamaños de letra): Azure los filtra o los muestra
distinto según el tema, claro u oscuro.

**En los moldes, todo lo que va entre `&lt; &gt;` se reemplaza** por el dato real. Antes de
mostrar el comentario se revisa que no quede ninguno: **un marcador sin reemplazar no se
postea**, porque en la tarjeta se lee como si fuera el dato. La excepción son los marcadores
de PHI (`&lt;persona&gt;`, `&lt;documento&gt;`…): ésos van a propósito, en lugar del dato real.

**Las @menciones.** Escribir `@Nombre` como texto **no avisa a nadie**: Azure sólo notifica si
la mención va como enlace con el identificador de la persona,
`<a href="#" data-vss-mention="version:2.0,&lt;id-de-la-persona&gt;">@Nombre</a>`. El
identificador sale del campo `System.AssignedTo` que devuelve el MCP. Si no se puede obtener,
se escribe el nombre en negrita y **se avisa que la notificación no sale**, para que se le
avise por otro lado. ⚠ A confirmar en el primer uso real que el MCP devuelve ese identificador.

**El sello de auditoría** ([[auditar-tarea]], [[auditar-historia]]), cuando se pidió una
auditoría, llega como bloque de texto plano. Es constancia, no barrera: nadie lo exige para
arrancar el desarrollo. **No se reescribe**: `bin/verificar-sello` lo lee buscando líneas
exactas, como `Rev auditado: N`, **sobre el texto sin etiquetas**. Sólo se lo formatea para que no quede
en un renglón: la primera línea en `<p><b>…</b></p>` y el resto una por renglón con `<br>`,
**con el mismo texto, espacios incluidos**. Lo único que no se postea es lo que en el bloque de
la skill va después de `<-`: son notas para quien lee la skill, no para la tarjeta. Ejemplo
lleno, del sello de [[auditar-tarea]]:

```html
<p><b>Auditoria de Tarea - auditar-tarea</b></p>
<p>Veredicto: COMPLETA<br>
Fecha: AAAA-MM-DD<br>
Rev de la Tarea auditada: 7<br>
Historia padre: #<ID><br>
Rev de la Historia padre:  12<br>
Escenarios del padre encontrados: 4<br>
Hallazgos: 0  (el detalle, en el reporte)<br>
Pendientes a confirmar:<br>
- Ninguno</p>
```

## Tarjeta congelada: acá sí se escribe

Una tarjeta **en un sprint y ya tomada** (Estado distinto de `New`) queda congelada: no se le
edita nada, sólo se comenta. Esta skill es por donde pasa todo lo que la IA quería cambiar
sobre ella: el DIFF propuesto va **como comentario**, con @mención a quien la tiene, y
aplicarlo lo decide una persona. Detalle: [[cambios-en-el-backlog]] §4.

Sirve para cualquier motivo: que cambió el documento funcional, que una auditoría encontró un
hueco, o que a un equivalente le falta completar un campo.

**Molde del cambio propuesto:**

```html
<p><b>Cambio propuesto</b> · la tarjeta está en el sprint y ya tomada, así que no se editó</p>
<p><a href="#" data-vss-mention="version:2.0,&lt;id-de-la-persona&gt;">@&lt;persona&gt;</a>, &lt;por qué hace falta el cambio: cambió el documento funcional · la auditoría encontró un hueco · le falta un campo&gt;. Revisalo antes de seguir trabajando sobre esta tarjeta.</p>
<hr>
<h3>Qué cambiaría</h3>
<ul>
<li><b>Se agrega:</b> &lt;qué, con su regla [RN-…]&gt;</li>
<li><b>Se modifica:</b> &lt;qué: valor actual → valor nuevo, con su regla&gt;</li>
<li><b>Se quita:</b> &lt;qué, o «nada»&gt;</li>
</ul>
<hr>
<h3>De dónde sale</h3>
<p>&lt;documento y versión, auditoría o pedido que lo origina&gt;</p>
<p><b>Aplicarlo o no lo decide una persona:</b> a mano en Azure, o en un ítem nuevo si lo que cambió es el pedido.</p>
```

Se escribe «se agrega / se modifica / se quita», no `+ ~ -`: los símbolos le sirven al que ya
sabe leer un DIFF, y esta tarjeta la lee un funcional también. Las tres líneas van siempre,
aunque alguna diga «nada»: así se ve que se revisó.

> **Ejemplo lleno** del renglón de la @mención y de una línea: *«@‹persona›, cambió el
> documento funcional. Revisalo antes de seguir trabajando sobre esta tarjeta.»* · *«Se
> modifica: código por defecto 02 → 03 [RN-…-13]»*.

## Comentario de cierre de desarrollo

> **Los datos duros los lee un script.** `bin/datos-cierre.py --repo <worktree> --base <base> --id <ID>`
> devuelve rama, último commit, cantidad de commits, archivos y carpetas tocadas, si está pusheada, el
> respaldo `evidencia/<ID>` y el link para abrir el Merge Request; lo que no pudo leer lo dice. La prosa
> del resumen técnico la pone esta skill con el resumen del worker; los datos no se escriben de memoria.

> **Lo aprendido no se queda en el comentario.** Si el desarrollo confirmó o descubrió algo del
> negocio (una respuesta a un pendiente, una regla precisada), eso va al Cerebro por la Consulta
> Interactiva de Decisión de [[cerebro-orquestador]], no sólo a la tarjeta. El comentario lo lista
> en «Pendientes a confirmar» o en «Conocimiento para el Cerebro»; el Cerebro lo guarda. Y lo que
> el desarrollo mostró de **la aplicación** —qué módulo quedó construido y qué expone, un bug con su
> causa, una deuda aceptada— va a `<modulo>/aplicacion/` (`mapa.md`, `aprendizajes.md`, `deuda.md`),
> con el `#ID` y el Merge Request como fuente.

Cuando termina el desarrollo de una Tarea, **quien lo terminó deja constancia en la tarjeta**:
qué rama, qué Merge Request y qué se hizo. Así la tarjeta cuenta sola cómo se resolvió, sin
tener que ir a buscarlo al código.

| | |
|---|---|
| **Cuándo** | Cuando la Tarea llega al Merge Request —o se pushea la rama, si el equipo mergea en local—: paso 7 del [[orquestador-desarrollo]], o al preparar la entrega en un desarrollo a mano ([[desarrollo]]). **Después** de que corrieron las verificaciones, porque el comentario informa su veredicto |
| **En qué tarjetas** | En **cada Tarea** que ese desarrollo cerró. La Historia padre no se comenta: el comentario ya la nombra, y repetirlo en el padre llena su hilo de ruido |
| **Quién lo postea** | Quien tiene el tablero: el orquestador, con el resumen del worker; en un desarrollo a mano, la misma sesión que programó |
| **Confirmación** | La de siempre: se muestra y se espera el "sí". Si terminan varias Tareas juntas, se muestran todos los comentarios juntos y **un "sí" cubre exactamente ese lote**, como en [[sincronizar-backlog]] |

**Los datos duros salen del repositorio, nunca de la memoria.** La rama y el último commit, de
`git`. El link del Merge Request, leído de GitLab por el MCP, **sólo lectura**: el comentario
**nunca abre ni toca un Merge Request**. Los tests, de la lista «Tests a escribir PRIMERO» y de
los commits `test(rojo)` del historial de trabajo (la rama `evidencia/<ID>`, subida a `origin`). Los
veredictos, de lo que devolvieron las verificaciones.

**La parte en prosa** —qué se hizo, cambios que rompen, lo que quedó afuera— sale de la
**descripción del Merge Request**, que ya tiene esos bloques ([[desarrollo]],
`merge-request.md`). Si no hay Merge Request, sale del **resumen final del worker**, y el
comentario lo dice: *«según el resumen del desarrollo»*. **Lo que no se pudo leer se escribe
`⚠ sin dato`**: una línea vacía no se rellena con lo esperable.

**Molde:**

```html
<p><b>Desarrollo terminado</b> · Tarea #&lt;id&gt; · Historia #&lt;id-del-padre&gt;</p>
<ul>
<li><b>Rama:</b> &lt;rama&gt; (&lt;pusheada | ⚠ sin pushear&gt;)</li>
<li><b>Merge Request:</b> <a href="&lt;link-del-merge-request&gt;">!&lt;número&gt;</a></li>
<li><b>Último commit:</b> &lt;hash corto&gt;</li>
<li><b>Fecha:</b> &lt;AAAA-MM-DD&gt;</li>
</ul>
<hr>
<h3>Qué se hizo</h3>
<p>&lt;dos o tres líneas en criollo: qué cambia para el que usa el sistema&gt;</p>
<hr>
<h3>Resumen técnico</h3>
<ul>
<li><b>Slice:</b> &lt;slice&gt;</li>
<li><b>Contrato:</b> &lt;endpoints tocados, y qué cambió en el openapi.yaml&gt;</li>
<li><b>Tests:</b> &lt;N&gt; de &lt;M&gt; ítems de «Tests a escribir PRIMERO», cada uno con su rojo antes del verde, verificado sobre el historial de trabajo</li>
<li><b>Commits:</b> &lt;cantidad, agrupados por importancia (alrededor de 10)&gt; en el Merge Request (último commit &lt;hash corto&gt; de la rama de la Tarea) · &lt;N&gt; commits de trabajo, verificados antes de reorganizar, en la rama evidencia/&lt;ID&gt; de origin</li>
<li><b>Cambios que rompen:</b> &lt;ninguno | cuáles | ⚠ sin dato&gt;</li>
<li><b>Dependencias nuevas:</b> &lt;ninguna | cuáles | ⚠ sin dato&gt;</li>
</ul>
<hr>
<h3>Verificaciones</h3>
<table>
<tr><th>Control</th><th>Qué contesta</th><th>Veredicto</th></tr>
<tr><td>Quién verificó</td><td>¿Otro agente que el que programó (DEC-005)?</td><td>&lt;motor&gt; v&lt;versión&gt; · &lt;modelo o worktree&gt;</td></tr>
<tr><td>verificar-tdd</td><td>¿Hubo rojo antes del verde?</td><td>&lt;veredicto&gt;</td></tr>
<tr><td>Revisión de código</td><td>¿Está bien escrito?</td><td>&lt;veredicto&gt;</td></tr>
<tr><td>auditar-codigo</td><td>¿Cumple la Tarea, sin PHI ni secretos?</td><td>&lt;veredicto&gt;</td></tr>
</table>
<hr>
<h3>Lo que quedó afuera</h3>
<ul>
<li>&lt;qué no se hizo, y por qué | «Nada» | ⚠ sin dato&gt;</li>
</ul>
<hr>
<h3>Pendientes a confirmar</h3>
<ul>
<li>⚠ &lt;el hueco o el gris&gt; · &lt;qué se hizo mientras tanto&gt; · &lt;qué hace falta para cerrarlo, y quién lo define&gt;</li>
</ul>
```

**Cómo se llenan los casos que no son el feliz**, sin cambiar la forma:

| Si… | Se escribe |
|---|---|
| La rama no se pusheó | `(⚠ sin pushear)` en lugar de `(pusheada)` |
| El desarrollo tocó dos slices | Los dos, y el motivo: `<slice-1> y <slice-2>, porque …` |
| El contrato no cambió | `sin cambios en el contrato` |
| No se cubrieron todos los ítems de la lista | `<N> de <M>`, y abajo cuáles faltan. **No es un desarrollo terminado**: se dice |
| No hay Merge Request | `todavía no abierto` en lugar del link, y la prosa lleva *«según el resumen del desarrollo»* |
| Un control no corrió | `SIN DATOS` en su fila. No es aprobado |
| Un control dio hallazgos | `HALLAZGO` y, en una línea abajo de la tabla, cuántos y cuál es el bloqueante |
| La fuente dice que no quedó nada afuera | `<li>Nada</li>`. La sección no se borra: su ausencia no dice si se revisó |
| No se pudo leer un dato | `⚠ sin dato` |
| Hay número de Merge Request pero no su link | `!15 (⚠ sin link)`, **sin** `<a>`: un enlace con `href` vacío o inventado lleva a ningún lado |
| No se sabe el slice | `⚠ sin dato`. El slice es uno de los declarados en [[contexto-proyecto]] (`<slice-1>` · `<slice-2>` · `<slice-n>`); **nunca** el nombre del producto |
| No quedó ningún pendiente | `<li>Ninguno</li>`, si el worker lo dijo. La sección no se borra |

**«Ninguno» y «Nada» son datos, no valores por defecto.** Se escriben sólo si la descripción
del Merge Request o el resumen del desarrollo lo dicen. Si no lo dice nadie, va `⚠ sin dato`:
un «ninguno» que nadie afirmó es una afirmación inventada. Lo mismo con «Qué se hizo»: se
copia de la fuente, no se redacta a partir del título de la Tarea.

**Barreras del cierre.**

- **Un veredicto que no corrió es `SIN DATOS`, no aprobado.** Si una verificación dio
  hallazgos, el comentario **lo dice**: no se omite para que la tarjeta quede prolija.
- **El comentario no cambia el Estado.** Pasar la Tarea a *Resolved* o *Closed* no lo hace la
  IA: la tarjeta ya está congelada y el cierre es una decisión de una persona.
- **Sin PHI, sin secretos, sin tokens**, y sin logs pegados: es el mismo cuidado que en la
  descripción del Merge Request, y el comentario queda en Azure para siempre.

## Pendientes a confirmar

Un **hueco o un gris** de una Tarea —un dato que falta, una decisión `⚠` que el Cerebro no
cerró, un caso que la lista de tests no cubre, un hallazgo de una auditoría que alguien pidió—
**no frena el desarrollo** y **no se vuelve a preguntar** en el momento. Se deja escrito en la
tarjeta, para que se resuelva más adelante y se vea al cerrarla (decisión de diseño del template).

| | |
|---|---|
| **Qué hace quien programa** | Lo que no depende del gris lo hace. Lo que depende de él **no lo inventa**: lo deja afuera, o toma el camino que la Tarea ya escribe, y lo anota como pendiente. Frena sólo si el gris impide **toda** la Tarea |
| **Dónde queda** | En la sección «Pendientes a confirmar» del **comentario de cierre** (molde de arriba), que ya pide su "sí" y no suma un turno. Si no hay comentario de cierre —el desarrollo se cortó, o el pendiente sale de una auditoría—, va en un comentario propio con el molde de abajo |
| **Qué lleva cada uno** | Qué es el gris · qué se hizo mientras tanto · qué hace falta para cerrarlo y quién lo define. Si ya tiene `P-nnn` en el Cerebro, se cita |

**Molde del pendiente suelto:**

```html
<p><b>Pendientes a confirmar</b> · Tarea #&lt;id&gt;</p>
<ul>
<li>⚠ &lt;el hueco o el gris&gt; · &lt;qué se hizo mientras tanto&gt; · &lt;qué hace falta para cerrarlo, y quién lo define&gt;</li>
</ul>
```

Un pendiente que se resuelve se responde en otro comentario —*«Pendiente resuelto: ‹cuál›,
‹cómo›»*—: el original no se edita, así queda la traza.

### Antes de cerrar una Tarea: revisar los pendientes

Cuando se va a **cerrar** una Tarea —pasarla a *Resolved* o *Closed*, o al estado de revisión
al terminar un desarrollo—, **antes** se leen sus
comentarios (`get_work_item_comments`, lectura libre) y su Descripción, y se listan los
**pendientes que no tienen su «Pendiente resuelto»**:

- los de los comentarios «Pendientes a confirmar» y del comentario de cierre;
- de los sellos de auditoría, **sólo el más reciente** (uno posterior deja sin efecto al viejo);
- los `⚠` que siguen en «Datos a confirmar» de la Descripción.

La lista va **en el primer aviso** del cierre:

> *«Antes de cerrar la #NNNN: quedan 2 pendientes sin resolver en sus comentarios — ‹uno›,
> ‹otro›. ¿Querés cerrarla igual?»*

- **No frena el cierre**: lo decide la persona, pero con los pendientes a la vista.
- **Los GATES del cierre no cambian.** Pasar a *Resolved* o *Closed* es edición destructiva:
  dos "sí" en turnos distintos, y la lista de pendientes va en el primero. Si la Tarea está
  **congelada** (en un sprint y ya tomada), la IA no le cambia el Estado: muestra los
  pendientes y la cierra una persona ([[cambios-en-el-backlog]] §4).
- **Sin pendientes**, se dice: *«No quedan pendientes en los comentarios.»*
- **Si no se pudieron leer los comentarios**, es **SIN DATOS**, y se dice: no es «no hay
  pendientes».
- Si no hubo ninguna auditoría y ningún pendiente, no pasa nada: el chequeo da vacío y se sigue.

## Contexto adicional
- Herramientas MCP y flujo de escritura con confirmación: [[integracion-azure-mcp/04-automatizar-con-ia]] · [[integracion-azure-mcp/00-index]].
- Etiquetas HTML que acepta Azure, con los esqueletos de la Descripción: [[checklists/mapa-campos-azure]].
- **Tarjeta congelada** (en un sprint y ya tomada): [[cambios-en-el-backlog]] §4.
- **Pendientes a confirmar** y su revisión antes de cerrar: §«Pendientes a confirmar», arriba.
- **Aviso de cambios (drift):** el protocolo de [[cambios-en-el-backlog]] usa esta skill para el comentario con @mención cuando un doc cambió y hay que avisar a quien trabaja la tarjeta (junto con la etiqueta `cambio-pendiente-lectura`, que en una tarjeta congelada no se pone).

---

### Ejemplo (genérico)
> "Dejá una nota en la #NNNN avisando que falta confirmar la versión." La skill
> redacta el comentario —`<p>Queda ⚠ pendiente confirmar la versión afectada antes de pasar
> a QA.</p>`—, lo muestra como se va a ver, y con tu OK lo postea en el Historial de la
> tarjeta. Sin datos reales de por medio.
