---
name: auditar-historia
description: >-
  (Solo lectura, adversarial) Auditar UNA Historia de usuario ya escrita —el segundo chequeo,
  hecho por un agente DISTINTO del que la redactó— antes de derivar Tareas de ella: que el
  Gherkin de los Criterios de aceptación sea VERIFICABLE (un Entonces observable y un
  comportamiento por Escenario, actor explícito, sin "correctamente"), que los Casos de uso y
  los Datos y estados queden cubiertos, que las reglas citadas existan y digan lo que se les
  atribuye, que ningún Entonces afirme sobre un punto que el Cerebro tiene abierto, y que el
  bloque "## Derivación a backlog" de la ficha fuente esté COMPLETO en los dos sentidos. Si el
  Documento fuente es un mockup no bloquea: deja escrito qué queda sin auditar. Usar cuando se
  pida "auditá la historia", "revisá los criterios de la #NNNNN", "¿esta Historia está lista
  para derivar Tareas?", "/auditar-historia". OPCIONAL: corre sólo a pedido y NO frena la
  derivación. NO redacta, NO corrige, NO escribe en el board: devuelve hallazgos y preguntas.
  Español (Argentina).
---

# Auditar historia

Audita **una** Historia de usuario contra su ficha fuente, **antes** de que se deriven
Tareas de ella. Es el equivalente de [[auditar-tarea]] un nivel más arriba, y lo corre
**otro agente, en otro turno, sin haber participado de la redacción** (en modo lote, un
sub-agente aparte, con su propio contexto, cuenta como otro turno).

> **Por qué existe esta skill.** Todo el aparato que protege el nivel Tarea son **conteos
> contra artefactos que produce la Historia** (los `Escenario:` del Gherkin, las `[RN-…]`
> que declara) **o la ficha** (el bloque enumerado). Si esos artefactos están vacíos o mal,
> el aparato de abajo **no falla: da verde**. Se construyó un verificador de precisión
> apoyado sobre un insumo que nadie medía.
>
> Y el costo es asimétrico: un hueco en una Tarea cuesta **una Tarea**. Un hueco en el
> Gherkin o en el bloque de derivación se multiplica por **todas sus Tareas** y —por la
> Regla de cardinalidad, que obliga a copiar la enumeración sin criterio propio— se
> reproduce **idéntico en las cuatro herramientas del ecosistema**. Es el único punto del
> pipeline donde el determinismo juega **en contra**: un flujo que quedó fuera de la
> enumeración no puede volverse Historia **nunca**, en ninguna herramienta.

## Regla de oro

- **Verificador ≠ productor.** Lo corre un agente **distinto** del que redactó la Historia
  o la ficha. Si sos quien la escribió, decilo y **no la audites**.
- **Adversarial.** El trabajo es encontrar el hueco. Una auditoría sin hallazgos es un
  resultado válido, pero recién después de haber buscado en serio.
- **Solo lectura.** No redacta, no corrige, no escribe en el board, **no toca el Cerebro**.
  Lo que encuentra sale como **hallazgo + pregunta**.
- **En modo lote ([[planificar-lote]]) cada hallazgo sale marcado F o P.** **F**: lo
  resuelve una fuente (regla del Cerebro, maqueta vigente, respuesta del humano), y se escribe
  cuál y el texto exacto del arreglo; lo aplica quien redacta, no esta skill. **P**: necesita a
  una persona, y va como pregunta al arranque o al cierre del lote. Una regla que no existe es
  siempre P: ninguna fuente la reemplaza. Un hallazgo del chequeo 19 (un `Entonces` sobre un
  punto que el Cerebro tiene abierto) es F sólo si la maqueta vigente lo define, y entonces va
  también al «Conocimiento para el Cerebro» del cierre como ✅ que resuelve ese `P-nnn`: el "sí"
  del cierre es la decisión. Si nada lo define, es P.
- **No inventar, y no completar por analogía.** Si una regla citada no existe, **no se
  deduce cuál «debería» ser**: se marca NO AUDITABLE y se pregunta. Proponer la regla que
  falta es exactamente el defecto que esta skill persigue.
- **Español (Argentina)**, sin emojis como íconos.

## Insumos

1. La **Historia**: campo Descripción (bloques *Datos y estados*, *Reglas de negocio*,
   *Casos de uso*, *Documento fuente*) y campo **Criterios de aceptación** (el Gherkin). En
   modo lote, si el lote la crea o la pisa, su **borrador** (`borrador/lote-*/`).
2. La **ficha fuente** del Cerebro que la Historia declara en *Documento fuente*, con su
   bloque **`## Derivación a backlog`** y su prosa completa.
3. Las **reglas citadas**, por su ruta en el Cerebro.

Si falta el 1, no hay nada que auditar. Si falta el 2 o el 3, se audita lo que se puede y
el resto sale **NO AUDITABLE** — nunca «cumple» por defecto.

> ### Regla del cero — un conteo vacío NUNCA es un «cumple»
> Igual que en [[auditar-tarea]]: si un insumo externo viene vacío, el conteo da `0 = 0` y
> el chequeo **pasa por vacuidad**. El caso central de esta skill: **una Historia sin
> Gherkin**. Hoy el campo Criterios de aceptación *«aparece vacío en la mayoría de las
> historias»* ([[criterios-aceptacion-gherkin]]), y con 0 Escenarios **todos** los chequeos
> del loop BDD↔TDD de abajo pasan sin que nada lo diga. Si hay 0 Escenarios, el veredicto
> es **NO AUDITABLE** y la Historia **no deriva Tareas**. Lo mismo vale para cualquier **bloque ausente** de la Historia o de la ficha: ausente no es cumplido.

## Quién la dispara (y quién NO)

> **Es opcional y no frena nada** (decisión de diseño del template). Corre sólo cuando alguien la
> pide —un dev, o quien arma un lote y la quiere—; ni [[sincronizar-backlog]], ni
> [[cargar-a-azure]], ni [[planificar-lote]] la disparan solos, ni buscan su sello para derivar
> Tareas. Exigirla gastaba muchos tokens y volvía a preguntar cosas ya cerradas. Lo que encuentre
> se deja **como pendiente** en la tarjeta ([[comentar-tarea]] §«Pendientes a confirmar»).

**No la invoca el funcional. Nunca.** Él arma las Historias con el conocimiento del OKF y
su mockup, pimponeando con la IA lo que falte — ese flujo **no se toca**.

Si se pide, conviene correrla **del lado dev**, en el momento en que la calidad del
Gherkin empieza a importar de verdad: **cuando se van a derivar Tareas de esa Historia**.
Ahí los Escenarios dejan de ser texto y pasan a ser **tests**, y un `Entonces` que no se
puede observar se convierte en un test que nadie puede escribir.

| Quién | Cuándo | Cómo |
|---|---|---|
| **El funcional** | — | **Nunca la invoca.** Su flujo queda igual |
| **El flujo dev** | Al derivar Tareas ([[sincronizar-backlog]]) o al crear una Tarea contra esa Historia ([[cargar-a-azure]] §3b) | **Sólo si se pide**, después del GATE de NIVEL. No corre sola |
| **Un dev, a mano** | Cuando quiera revisar una Historia antes de tocarla | `/auditar-historia` |
| **El modo lote** ([[planificar-lote]]) | Si quien arma el lote la pide: en la preparación, sobre cada Historia padre; o en la auditoría del lote, sobre cada Historia que el lote redacta o corrige | **Sólo si se pide**, un agente por Historia, en paralelo |

> **Por qué en el lote también corre al crear la Historia.** Las dudas de una Historia aparecen
> cuando se auditan, y si eso pasa recién al derivar Tareas, se pregunta en la reunión con los
> devs lo que se podría haber cerrado antes (el 2026-09-30, dos auditorías dieron decenas de dudas
> en plena planificación). Si la Historia cambia después, el sello vence; re-auditarla es opcional.

> **Por qué, si se pide, conviene correrla acá y no cuando se escribe la Historia.** Poner la auditoría
> en el momento del funcional obligaría a que él invoque algo — y no invoca nada, ni tiene
> por qué. Además sería prematuro: una Historia recién escrita todavía va a cambiar. El
> momento correcto es **el último instante antes de que alguien la use para programar**.
> Si ya hay sello vigente, no se vuelve a auditar.

## Primero, el script

Antes de leer nada a mano, esta skill **corre**:

```
python bin/auditar-historia.py --criterios <criterios.html> --descripcion <descripcion.html> --ficha <ficha.md> --flujo F-nn --json
```

Los Criterios y la Descripción van como archivos: en modo lote son los borradores; si no, se
guardan desde el tablero. El script hace lo que es **conteo y forma**:
- que haya Escenarios y que cada uno tenga su Cuando y su Entonces;
- las palabras vagas en el Entonces;
- que cada Escenario cite una regla, y que la regla exista;
- títulos repetidos y Esquemas sin Ejemplos;
- las reglas de la Historia contra las del `[F-nn]` en la ficha;
- el Documento fuente;
- los puntos abiertos citados;
- el formato.

**Eso no se rehace a mano**: su resultado se copia al reporte. Lo que marca HALLAZGO es
hallazgo, y si no corrió, esos chequeos son SIN DATOS. Si la herramienta no puede correr
comandos, se le pide a la persona ese comando exacto. Abajo, la auditoría hace **sólo** lo que el
script lista en «Lo que este script NO mira», y confirma o descarta sus AVISOS.

## Los 20 chequeos

### Chequeo 1 — ¿Hay ficha fuente? (declarativo, NO bloqueante)

1. **¿El *Documento fuente* resuelve a una ficha del Cerebro con bloque
   `## Derivación a backlog`?** Un mockup `.html`, un acta de reunión o un link a Figma
   **no son una ficha**: son apoyo visual. Se responde **sí o no**, y la respuesta **decide
   qué se puede auditar**, no si se audita.
   - **Si NO hay ficha:** se declara como **un** hallazgo —«la Historia no tiene ficha»— y los
     chequeos **11 a 18** (bloques B y C) se reportan **NO AUDITABLES por falta de ficha**,
     nunca como ocho hallazgos sueltos. **Los otros once chequeos corren igual** y el veredicto
     sale de ellos.
   - **Nunca frena por sí solo la derivación de Tareas.**

   > **Por qué dejó de ser bloqueante.** Hoy los funcionales arman las Historias con el
   > conocimiento del OKF **y un mockup**, y eso es el flujo real del equipo. Hacer que «no hay
   > ficha» valga NO AUDITABLE convertía a esta skill en un muro: ninguna Historia real podía
   > pasar, y con el gate de `sincronizar-backlog` encima, **nada se derivaba nunca**.
   > La medición era correcta, el veredicto estaba mal calibrado.
   >
   > **Y sin ficha sigue habiendo mucho que auditar:** los **once** chequeos que no dependen de
   > ella son los que atrapan un `Entonces` que no se puede observar, un «funciona
   > correctamente», UI sin regla detrás, una `[RN-…]` citada que no existe o que no dice lo que
   > se le atribuye, y —el chequeo 20— **que el documento fuente contradiga las reglas que la
   > Historia cita**. Ese último está pensado **justamente** para el caso del mockup: es el que
   > detecta que la maqueta muestra un canal dado de baja mientras la Historia cita la regla que
   > lo eliminó.
   >
   > **Dónde sí hace falta la ficha: al CREAR el árbol**, no al auditar una Historia que ya
   > existe. El bloque enumerado es lo que fija **cuántas** Historias van (Regla de
   > cardinalidad, [[sincronizar-backlog]]). Auditar y crear son momentos distintos; confundirlos
   > fue el error.

### Bloque A — Calidad del Gherkin (campo Criterios de aceptación)

> **Este bloque es un tamiz grueso.** Sus criterios son contables a propósito, y por eso
> dejan pasar Gherkin defectuoso que un humano vería al toque. Que el bloque A pase entero
> **no significa que el Gherkin sea bueno** — significa que no tiene los defectos que se
> pueden contar. Los bloques B y C son los que de verdad separan.

2. **Hay al menos un `Escenario:`.** Cero → **NO AUDITABLE**. (Una Historia sin Escenarios no se deriva igual, pero por el DoR, no por esta auditoría: ver [[sincronizar-backlog]].)
3. **Cada `Escenario:` tiene al menos un `Entonces`** con resultado observable.
4. **Ningún `Entonces` usa vocabulario vacío.** Lista negra: *correctamente, adecuadamente,
   exitosamente, sin problemas, según corresponda, de forma apropiada, de manera adecuada,
   correcto*.
5. **Un comportamiento por Escenario.** Tres señales, no una:
   - ` o ` / ` y también ` dentro de un `Entonces`;
   - un `Y` que introduce un **sujeto distinto** al del `Entonces` anterior;
   - **un `Entonces` que describe un efecto INTERNO** (*consulta, invoca, llama a, registra
     en, persiste*) **seguido de un `Y` observable**. Es el caso que más se escapa: mismo
     sujeto, dos comportamientos, y el primero ni siquiera se puede verificar desde afuera.
6. **Actor explícito y voz activa en cada `Cuando`.** Dos señales:
   - arranca con `se ` (*se registra*, *se envía*, *es enviado*) → esconde quién actúa;
   - **el sujeto es «el sistema»** → gramaticalmente activo, pero igual esconde la acción
     del usuario que dispara el escenario. Un `Cuando` describe lo que **hace alguien**, no
     lo que el sistema hace solo.
7. **Cero UI sin regla detrás.** Lista negra ampliada: *botón, combo, grilla, pestaña, modal,
   columna, checkbox, **tarjeta, ficha, pantalla, alerta, campo, leyenda, mensaje, popup,
   menú***. Si aparece alguna sin `[RN-…]` asociada, el Escenario describe la pantalla en vez
   del comportamiento: se rompe con cualquier rediseño.
8. **Cobertura de caminos:** al menos un caso feliz **y** al menos uno de error o borde.
   Si la Historia **o alguna de las reglas que cita** menciona roles o permisos distintos,
   al menos uno de permiso.
9. **Cero keywords en inglés** (`Given/When/Then/Scenario/Feature/And/But`).
10. **Cada `Escenario:` lleva su `[RN-…]`, esa regla existe, y contiene el criterio que el
    Escenario le atribuye.** Dos trampas frecuentes: la regla existe pero habla de **otro rol,
    otra pantalla u otro sistema**; o el Escenario afirma algo que la regla **no menciona**.
    Las dos son **trazabilidad falsa**: simulan cobertura, y es peor que no citar nada.

### Bloque B — La Historia cierra contra su ficha

> **La Regla del cero también rige acá.** Si un bloque de la Historia **no existe**
> (*Casos de uso*, *Datos y estados (funcional)*), el conteo da `0 = 0` y el chequeo pasaría
> por vacuidad. **Bloque ausente → NO AUDITABLE, nunca PASA**, y se dice cuál falta.

11. **Cada `CU-nn` de *Casos de uso* está cubierto por al menos un Escenario.** Este bloque no
    tenía **ningún consumidor** aguas abajo: se escribía y moría ahí.
12. **Cada campo y cada transición de *Datos y estados (funcional)* aparece en algún Escenario
    o `CU-nn`.** Es el inventario que la Tarea necesita para su Contrato técnico. Si el bloque
    falta, las Tareas hijas armaron su contrato **sin fuente**.
13. **Las `[RN-…]` que la Historia cita son exactamente las que la ficha asigna a su `[F-nn]`.**
    Ninguna de más (alcance inventado), ninguna de menos (regla huérfana: si la Historia
    declara 4 de 21, las otras 17 **no existen para nadie aguas abajo**).
14. **La Historia rastrea a un `[F-nn]` concreto y su título describe el mismo alcance.** Un
    título más amplio —o que junta dos alcances— es una bomba con el GATE de dedup: cuando
    llegue el alcance que quedó afuera, va a encontrar esta Historia y **bloquear el alta del
    ítem equivocado**.

### Bloque C — Suficiencia del bloque `## Derivación a backlog`

> El único que mira **hacia afuera**. La Regla de cardinalidad prohíbe crear nodos fuera de la
> enumeración: **lo que falta en la lista no puede nacer nunca**, en ninguna herramienta.
> Si el chequeo 1 falló, estos cuatro se reportan como **derivados** de él.

15. **Prosa → enumeración.** Cada flujo o acción de negocio descripto en la prosa de la ficha
    aparece como `[F-nn]`, **o** está declarado fuera de alcance **por escrito y con motivo**.
16. **Enumeración → prosa.** Cada `[F-nn]` rastrea a un lugar concreto de la ficha. Un
    enumerado sin respaldo es un flujo inventado.
17. **Reparto de reglas sin residuo.** `reglas de la ficha` = `asignadas a algún [F-nn]` +
    `declaradas fuera de alcance con motivo`.
18. **Pendientes abiertos que tocan un `[F-nn]` derivado.** Barrer **las cuatro formas** que
    conviven: `## Dudas y Preguntas`, `## Dudas y preguntas`, `## Pendientes`, y cualquier
    `- [ ]` o marca de alerta suelta.

### Bloque D — Lo que se afirma sin respaldo

19. **Ningún `Entonces` afirma sobre un punto que el Cerebro tiene ABIERTO.** Cruzar el texto
    de cada Escenario contra los pendientes (`P-nnn`, marcas de alerta, «a definir», «en
    discusión», «falta definir», «a confirmar») y contra las reglas en estado PENDIENTE.
    > **Es el mecanismo exacto por el que una duda se vuelve requisito sin que nadie la vote.**
    > Un Escenario afirma un comportamiento que el equipo todavía está discutiendo; baja a las
    > Tareas como dato duro; los tests lo fijan; y queda implementado como si hubiera sido una
    > decisión. El chequeo 18 barre pendientes, pero solo pregunta si tocan un `[F-nn]`: este
    > los cruza contra **el texto de los Escenarios**, que es donde el daño se materializa.
20. **El Documento fuente NO contradice las reglas que la Historia cita.** Leer el contenido
    del fuente —no solo su bloque de derivación— y verificar que lo que muestra siga vigente.
    Un mockup dibujado antes de una decisión puede seguir mostrando el flujo **que esa
    decisión descartó**, y la Historia lo cita como fuente de verdad. Es la dirección inversa
    del drift que [[consultar-backlog]] detecta (doc → ticket): acá se mira **ticket → doc**,
    y hoy no la mira nadie.

### El sello (no es un chequeo: es la salida)

Al terminar, el veredicto **se escribe en la tarjeta** con [[comentar-tarea]] (que pide su
propia confirmación humana —en modo lote, la del cierre—; esta skill no escribe por su cuenta):

```
Auditoria de Historia - auditar-historia
Veredicto: COMPLETA | CON HUECOS | NO AUDITABLE
Fecha: <AAAA-MM-DD>
Rev auditado: <System.Rev al LEER la Historia>   <- el sello mismo suma una revision, y no cuenta
Ficha fuente: <ruta> (ultimo cambio: <fecha>)
Escenarios encontrados: <N>        <- si dice 0, el loop BDD no existe
Hallazgos: <cantidad>
Pendientes a confirmar:
- <hallazgo, una linea, redactado como pendiente>   <- uno por hallazgo; "Ninguno" si no hay
```

**Cómo se mide la vigencia: por lo que cambió, no por cuántas veces se guardó.** En Azure
**toda** escritura directa crea una revisión: el propio sello (un comentario de
[[comentar-tarea]]), asignarla, cambiarle el Estado. Contando `Rev`, el sello **nace
vencido** —sellar ya suma una— y cualquier comentario en la Historia lo vence sin que nadie
haya tocado el Gherkin. Colgarle Tareas hijas **no** lo vence: el vínculo se crea siempre
desde la hija, y un vínculo no es contenido.

La regla: el sello registra **`Rev auditado: N`** (el que tenía al leerla) y queda
**vigente mientras ninguna revisión posterior a `N` haya cambiado Título, Descripción o
Criterios de aceptación**, y la ficha fuente no haya cambiado. Comentarios, Estado, Asignado,
Etiquetas y vínculos no cuentan. **Vence** si cambió alguno de esos tres campos o **la ficha
fuente**. Si no se pudo leer el historial, es **SIN DATOS**, que no es vigente. Lo verifica el
script de solo lectura (el MCP no expone el historial por campo):

```
bash bin/verificar-sello.sh historia <id-historia> <Rev auditado>
```

Sale `0` VIGENTE, `1` VENCIDO o `2` SIN DATOS. Si el SIN DATOS es de **la máquina** (sin
token, sin red, sin Python), el script lo dice y re-auditar **no** lo destraba: se arregla el
acceso. **La ficha fuente la chequea esta skill aparte**: el script mira el board, no el
Cerebro. Se compara la fecha de último cambio de la ficha contra la que anotó el sello. **Agregar «Tickets derivados» o la traza de una derivación no cuenta como cambio de la ficha**: si el único cambio desde el sello es ése (se mira con `git log` de la ficha), el sello sigue vigente.

**Al empezar**, se **lee** si ya hay un sello previo y si sigue vigente con ese criterio.
**Vale solo el más reciente** (el de mayor `Rev auditado`): como un comentario ya no vence
nada, un sello viejo que dijo COMPLETA puede seguir vigente aunque después se haya re-auditado
con CON HUECOS. Manda el último. El sello se postea en HTML ([[comentar-tarea]] §«Formato»): se
lee sobre el texto sin etiquetas.
**El sello no es requisito para derivar Tareas.** Es constancia de lo que se miró y cuándo.
En modo lote, si se pidió la auditoría, vale el veredicto de la preparación (o de la
re-auditoría), y el sello se publica al escribir.

> El sello **no se cuenta como chequeo**: en una primera auditoría siempre faltaría, por
> definición. Que una Historia con Tareas no tenga sello **no es un hallazgo**: la auditoría
> es opcional.

## Veredictos

| Veredicto | Cuándo | Qué significa |
|---|---|---|
| **COMPLETA** | Los 20 chequeos pasan | No se encontró nada que falte |
| **CON HUECOS** | Falta cobertura, o un Escenario no es verificable | Lo que falta se deja como **pendiente a confirmar**. Se puede corregir primero —en modo lote, la corrección entra en el mismo lote— o seguir; **no frena la derivación** |
| **NO AUDITABLE** | 0 Escenarios, o una regla citada no existe | Se dice qué no se pudo mirar, y queda como pendiente. Nunca se da por buena una Historia que no se pudo auditar, pero la auditoría **no frena**. (Con 0 Escenarios no se derivan Tareas igual, por el DoR) |

> **La falta de ficha NO da NO AUDITABLE.** Deja los chequeos 11 a 18 sin poder correr, y eso
> se **declara** en el reporte y en el sello («sin ficha: 11–18 no auditables»), pero el
> veredicto sale de los **once** chequeos que sí corrieron. Una Historia armada sobre OKF +
> mockup puede dar **COMPLETA** — con esa limitación escrita a la vista.

**Si se dan las dos** (faltan cosas **y** hay algo que no se pudo verificar), el veredicto es
**CON HUECOS + NO AUDITABLE en «el punto X»** — se reportan las dos, no se elige una. Se
arreglan por caminos distintos: los huecos los cierra quien redacta; lo no auditable exige
**cargar lo que falta en el Cerebro**.

## Quién arregla lo que esta skill encuentra (el hallazgo tiene dueño)

Un hallazgo que no tiene destinatario termina en que alguien **inventa** para
cerrarlo — justo lo que todo este aparato viene a impedir. El reparto es:

| Qué falló | Quién lo arregla |
|---|---|
| Gherkin ausente, vago o mal formado (bloque A) | **[[redactar-tarea]]**, que redacta Historias además de Tareas: toma la Historia existente y cierra sus Criterios de aceptación, preguntando lo que no puede saber |
| `CU-nn` / *Datos y estados* sin cubrir (bloque B) | **[[redactar-tarea]]**, misma pasada |
| Reglas que no existen, o que no dicen lo que se les atribuye (9, 12) | **El equipo funcional**, en el Cerebro. Ninguna skill inventa una regla para destrabar |
| Bloque de derivación incompleto (bloque C) | **`cerebro-analyst` + `cerebro-curator`** con [[cognitive-doc-design]] — proponen, y un humano valida |

> **Si la Historia está congelada** (en un sprint y ya tomada), lo que corrige
> [[redactar-tarea]] no lo carga la IA: va como comentario y **lo carga una persona a mano**
> ([[cambios-en-el-backlog]] §4).

## Barreras

- **Solo lectura del board y del Cerebro.** Nunca `create_work_item`/`update_work_item`, ni
  escritura en `cerebro-digital/`.
- **No corrige.** Propone el texto del Escenario o del `[F-nn]` que falta, para que otro lo
  cargue con su confirmación.
- **No aprueba por cansancio.** Lo que no se pudo verificar es NO AUDITABLE, no «cumple».
- **PHI prohibido** en el reporte (marcadores `<persona>`, `<documento>`, etc.).

## Dónde entra en el flujo

```
ficha del Cerebro (con su bloque de derivacion)
   -> sincronizar-backlog: propone Epica/Feature/Historia, crea con confirmacion
   -> [auditar-historia]  (2do chequeo del nivel funcional, OPCIONAL, a pedido)  <- esta skill
   -> redactar-tarea (DoR) -> [analizar-tareas, a pedido] -> cargar-a-azure
   -> [auditar-tarea]     (2do chequeo del nivel tecnico, OPCIONAL, a pedido)
   -> guiar-tdd -> verificar-tdd
```

## Contexto adicional

- El equivalente un nivel abajo: [[auditar-tarea]]
- Consistencia del conjunto de Tareas: [[analizar-tareas]]
- Cómo se escribe el Gherkin: [[criterios-aceptacion-gherkin]]
- Plantilla y bloques: [[plantillas/historia-de-usuario]]
- Formato del bloque de derivación: [[organizacion-y-trazabilidad]] §5

---

### Ejemplo (genérico)

> Una Historia declara 3 Escenarios; uno dice *«Entonces el sistema procesa correctamente
> la solicitud»*. La ficha fuente enumera 3 flujos, y en su prosa hay un cuarto camino
> («el supervisor también puede ejecutarlo sin solicitud previa») que no está enumerado ni
> declarado fuera de alcance.
>
> La auditoría reporta **CON HUECOS**:
> - *Chequeo 3:* el `Entonces` del Escenario 2 usa «correctamente». No se puede convertir en
>   test; el dev tendría que inventar el criterio. **Pregunta:** ¿qué resultado observable
>   distingue «procesado» de «no procesado»?
> - *Chequeo 14:* el camino del supervisor está en la prosa y no en la enumeración. Por la
>   Regla de cardinalidad **no puede volverse Historia nunca**. **Pregunta:** ¿se agrega como
>   `[F-04]` o se declara fuera de alcance con motivo?
>
> No corrige la ficha ni la Historia: deja los dos ítems redactados para que el humano
> decida y la skill que corresponda los cargue en otro turno.
