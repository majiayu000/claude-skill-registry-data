---
name: auditar-tarea
description: >-
  (Solo lectura, adversarial) Auditar UNA Tarea técnica ya escrita —el segundo chequeo, hecho
  por un agente DISTINTO del que la redactó— con foco en la lista "Tests a escribir PRIMERO":
  que no falte ningún caso (cada validación, cada Caso de error, cada código del contrato
  OpenAPI, cada [RN-…] y cada Escenario del padre tienen su test), que ningún test sobre, que
  cada test sea VERIFICABLE (input concreto → resultado concreto), que PUEDA FALLAR (salvo
  guardarraíl declarado) y que cada ítem tenga UNA sola condición. Usar cuando se pida "auditá
  la tarea", "revisá los tests de la #NNNNN", "doble chequeo de la tarjeta", "¿esta Tarea está
  lista para desarrollar?", "/auditar-tarea". OPCIONAL: corre sólo a pedido y NO es requisito
  para arrancar el desarrollo (lo que encuentre queda como pendiente en la tarjeta). NO
  redacta, NO corrige, NO escribe en el board: devuelve hallazgos y preguntas. Español
  (Argentina).
---

# Auditar tarea

Audita **una** Tarea técnica contra su Historia padre. Es el **segundo chequeo** del
par: el primero lo hace quien escribe la tarjeta ([[cargar-a-azure]] §2b, autochequeo
al momento de escribir); este lo hace **otro agente, en otro turno, sin haber
participado de la redacción** (en modo lote, un sub-agente aparte, con su propio contexto,
cuenta como otro turno).

> **Es opcional y no frena el desarrollo** (decisión de diseño del template). Corre sólo cuando alguien
> la pide. Ni [[tomar-tarea]] ni el orquestador de desarrollo buscan su sello antes de arrancar:
> exigirlo gastaba muchos tokens y volvía a preguntar cosas ya cerradas o que no hacían falta
> para empezar. Lo que encuentre se deja **como pendiente en la tarjeta**, con
> [[comentar-tarea]] §«Pendientes a confirmar», y se mira al cerrarla.

> **Por qué existe esta skill.** La lista «Tests a escribir PRIMERO» es el artefacto
> más crítico de la Tarea, y su modo de falla es **silencioso**: `guiar-tdd` escribe
> **un test por ítem de la lista y nada fuera de ella**. Un caso que falta en la lista
> **no se prueba nunca** — no hay error, no hay warning, el pipeline queda verde y el
> agujero llega a producción. `verificar-tdd` tampoco lo salva: audita que *los tests
> de la lista* tengan su rojo, no que *la lista esté completa*. Nadie, en todo el
> flujo, miraba si a la lista le faltaba algo. Eso audita esta skill.

## Regla de oro

- **Verificador ≠ productor.** Lo corre un agente **distinto** del que redactó o cargó
  la Tarea. Si sos quien la escribió, decilo y **no la audites**: pedí que la tome otro.
- **Adversarial, no complaciente.** El trabajo es **encontrar el hueco**, no confirmar
  que está bien. Una auditoría sin hallazgos es un resultado válido, pero recién
  después de haber buscado en serio.
- **Solo lectura.** No redacta, no corrige, no escribe en el board, no toca el Cerebro.
  Lo que encuentra sale como **hallazgo + pregunta**, nunca como arreglo silencioso.
- **En modo lote ([[planificar-lote]]) cada hallazgo sale marcado F o P.** **F**: lo
  resuelve una fuente (regla del Cerebro, maqueta vigente, respuesta del humano, contrato de
  otra Tarea), y se escribe cuál y el texto exacto del arreglo; lo aplica **el que redactó**,
  no esta skill. **P**: necesita a una persona. Un F sin su fuente escrita es un P.
- **No inventar.** Si falta contexto para juzgar (una `[RN-…]` que no está en el
  Cerebro, un contrato incompleto), se marca **NO AUDITABLE** en ese punto. Nunca se
  supone el comportamiento que "debería" tener.
- **Español (Argentina)**, sin emojis como íconos.

## Insumos (los tres, o no se audita)

1. La **Tarea**: contrato técnico, validaciones, casos de error, tabla de Escenarios y
   lista de tests — con la herramienta de lectura del board que tenga el entorno (solo
   lectura), o pegada si este entorno no llega al tablero. En modo lote, el **archivo del
   borrador** (`borrador/lote-*/`), antes de que exista la tarjeta.
2. La **Historia padre**: sobre todo el campo **Criterios de aceptación** (el Gherkin).
   Se consigue con la herramienta de lectura del board que tenga el entorno; si este
   entorno no llega al tablero, se pide pegada. En modo lote, si el lote crea o pisa la
   Historia, su **borrador** (`borrador/lote-*/<clave>-criterios.html`): es la Historia como va a
   quedar, y auditar contra la del tablero daría huecos falsos.
3. Las **reglas citadas** (`[RN-…]` / `[DEC-…]`) en el Cerebro, por su ruta.

Si falta el 1, no hay nada que auditar. Si falta el 2 o el 3, se audita lo que se
puede y el resto sale **NO AUDITABLE** — nunca «cumple» por defecto.

> ### Regla del cero — un conteo vacío NUNCA es un «cumple»
> Casi todos los chequeos de abajo son **conteos contra un insumo externo**: los
> `Escenario:` del padre, las filas de Casos de error, los códigos del contrato. Si ese
> insumo viene **vacío**, el conteo da `0 = 0` y el chequeo **pasa por vacuidad**: no
> porque esté bien, sino porque no había nada que mirar. Es la falla más engañosa de
> todas, porque el reporte sale en verde.
> **Caso concreto y frecuente:** una Historia **sin Gherkin** (el campo Criterios de
> aceptación aparece vacío en la mayoría de las historias del board). Con 0 Escenarios,
> los chequeos 5, 13 y 14 «pasan» y el loop BDD↔TDD **no existe**, sin que ningún
> artefacto lo diga.
> **Por eso:** si un insumo externo viene vacío, el veredicto de ese punto es
> **NO AUDITABLE**, nunca PASA — y hay que decir **cuál** insumo estaba vacío. Si la
> Historia padre no tiene Escenarios, además se reporta que **no pasó su propio DoR**
> ([[definicion-preparado-terminado]]) y que derivar Tareas de ella es prematuro.

## Los 16 chequeos sobre la lista de tests

### Completitud (¿falta algún test?) — es el bloque que evita el daño grave

1. **Cada validación tiene su test — una por regla, no una por campo.** Recorrer
   *Validaciones* y separar cada regla distinta: «obligatoria» y «formato válido» son
   **dos** reglas del mismo campo y necesitan **dos** tests. Una validación sin test es
   código que nadie prueba.
2. **Cada fila de «Casos de error» tiene su test, y el resultado esperado COINCIDE.**
   No alcanza con que la fila tenga un test: hay que comparar, palabra por palabra, el
   **payload de la fila**, el **resultado esperado del test** y el **schema del contrato**.
   Las tres cosas describen el mismo caso y pueden decir cosas distintas sin que nadie lo
   note — p. ej. la fila dice «telefono y email en null», el test dice «el objeto entero
   en null» y el contrato no declara `nullable` en ninguno de los dos. Esa contradicción
   hace imposible que el test y el contrato estén los dos en verde.
3. **Cada código de respuesta Y cada campo del schema tienen test.** Sacar del fragmento
   OpenAPI **todos** los códigos (`200`, `400`, `404`, `409`, `502`…) **y todos los campos
   del cuerpo de éxito**. Un código declarado y no probado es una promesa que nadie
   verifica; un campo declarado y no verificado se puede dejar de devolver sin que ningún
   test se ponga rojo. Chequear también los `nullable`: si un test espera `null` en un
   campo que el contrato no declara nullable, hay contradicción (ver chequeo 2).
   **Y cada valor de un catálogo cerrado.** Si el contrato declara `enum: [A, B, C]`, los
   **tres** tienen que aparecer en algún ítem. Ejercitar dos de tres y rechazar un cuarto
   valor **no prueba que el tercero esté aceptado**: se lo puede dejar afuera del enum y la
   lista entera queda en verde. Se cuentan los valores del enum contra los que aparecen en
   los ítems — no alcanza con ver que «el catálogo está cubierto».
4. **Cada `[RN-…]`/`[DEC-…]` citada existe Y dice lo que el test le atribuye.** Dos pasos:
   (a) abrir la regla en el Cerebro por su ruta — si no existe, ese punto es **NO
   AUDITABLE**, nunca «cumple»; (b) leerla y verificar que **contenga el criterio** que el
   test le cuelga. Una decisión que dice «se busca solo por identificador» **no** define el
   formato de la identificador: citarla en un test de formato es **trazabilidad falsa**, y es
   peor que no citar nada porque **simula cobertura**.
5. **Cada Escenario del Gherkin del padre que la Tarea declara cubrir tiene sus tests**, y
   los que cubre **en parte** nombran la Tarea complementaria **con su `#ID`** (el
   Escenario parcial solo se puede seguir si el número está escrito). Contar los
   `Escenario:` del padre contra las filas de la tabla más los títulos de la línea
   «No cubre» del pie ([[plantillas/tarea]]): tienen que dar igual. En modo lote, sobre el
   borrador, un `[T-nn]` vale como `#ID`; se vuelve a mirar después de escribir.

### Calidad (¿los tests sirven?) — sin esto, TDD es teatro

6. **Cada test es VERIFICABLE.** Tiene **input concreto → resultado esperado concreto**.
   «Valida bien la identificador» no es un test: no se sabe qué entra ni qué sale, así que
   dos devs escriben cosas distintas. Debe poder leerse como una aserción.
7. **Un ítem = UNA sola condición.** Prohibido unir dos casos con «o» / «y» en el mismo
   ítem. `guiar-tdd` escribe **un test por ítem**: si el ítem dice «el servicio devuelve
   error **o** timeout», se escribe **uno de los dos** y la otra rama queda sin probar,
   en silencio. Es el modo de falla más peligroso de todo el pipeline, y se detecta
   buscando conjunciones. Si el ítem tiene dos condiciones, el hallazgo es «faltan tests»,
   no «está mal redactado».
   **Un Esquema no es un ítem con dos condiciones.** Un ítem «Esquema» —`N. Esquema —
   <condición>:` y debajo una fila por caso, `<entrada> → <resultado esperado>`, en una lista
   con viñetas— vale como **un** ítem: `guiar-tdd` lo escribe como un test parametrizado con una
   fila por cada fila del ítem, y `verificar-tdd` comprueba que estén todas. Si las filas cambian
   la **condición** y no solo los datos, son ítems distintos y el hallazgo es «faltan tests». Si
   una fila no trae su resultado esperado, es «test no verificable» (chequeo 6).
8. **Cada test PUEDE FALLAR — y se declara si puede tener ROJO PRIMERO.** Preguntarse:
   *«¿qué código, escrito mal, haría que este test se ponga rojo?»*. Si la respuesta es
   «ninguno», el test es decorativo («el endpoint existe», «devuelve un JSON», «no tira
   excepción») → hallazgo.
   **Distinguir dos clases, porque el DoR las trata distinto:**
   - **Test del ciclo (default):** puede y **debe** arrancar en rojo. Entra en la evidencia
     rojo/verde que audita `verificar-tdd`.
   - **Test guardarraíl (regresión):** protege una **ausencia** — «ninguna clase del módulo
     depende de X», «no se filtra ningún campo fuera del contrato». **Nace verde a
     propósito**: su valor es bloquear la regresión futura, no producir el rojo de hoy.
     **Tiene que estar declarado como tal en el ítem**, y el DoD debe **excluirlo** del
     «todos los tests tuvieron su rojo previo». Un guardarraíl sin declarar convierte la
     Tarea en **imposible de cumplir**: `verificar-tdd` va a pedir una evidencia de rojo
     que no puede existir.

   **Dos filtros para no regalar la exención** — declarar guardarraíl **suprime** el commit
   de rojo de ese ítem (`guiar-tdd`), así que la etiqueta tiene que ganarse:
   - **Afirma sobre la FUENTE, no sobre el mismo observable que ya fija un test del ciclo.**
     Una constante, un catálogo, la estructura del módulo, las dependencias del módulo — no
     el DOM renderizado ni el cuerpo de una respuesta que otro test ya asegura.
   - **Ningún otro test de la lista lo implica lógicamente.** Si el test 1 dice «se ven
     **exactamente** estas tres opciones», un test que diga «no aparece esta cuarta opción»
     **no puede ponerse en rojo con el 1 en verde**: no es guardarraíl, es **redundancia**, y
     encima costó un rojo que sí existía. Preguntarse siempre: *«¿qué cambio pone en rojo
     este test y deja los demás en verde?»*. Si no hay ninguno, el ítem sobra (chequeo 13).
   - **Y el filtro de fondo:** en un componente que todavía no existe, ¿este test fallaría en
     el mismo instante que los del ciclo? Si sí, **podía tener rojo primero** y la exención
     no hacía falta.

   > **El ítem tiene que TRAER ESCRITA la respuesta, no dejarla para el auditor.** Todo
   > guardarraíl se redacta con la frase **«se pone en rojo si …»** adentro del ítem, nombrando
   > el cambio concreto que lo haría fallar. Ejemplo válido: *«se pone en rojo si alguien agrega
   > un canal a la constante de catálogo»*. Ejemplo que se cae solo: *«se pone en rojo si el
   > desplegable muestra una opción de más»* — eso ya lo detecta el test que exige «exactamente
   > estas tres».
   > **Si no se puede escribir esa frase, no es un guardarraíl.** Y si la frase describe algo
   > que otro test de la lista ya detecta, tampoco. La exención del rojo se **gana por escrito**:
   > sin esa frase, el auditor lo trata como test del ciclo y exige su rojo previo.
   > *Por qué esta regla:* el criterio anterior decía «protege una ausencia», que **describe cómo
   > se ve** un guardarraíl pero no **cómo verificar si el tuyo lo es** — y «el desplegable no
   > contiene el canal dado de baja» **es** una ausencia, así que la definición vieja admitía
   > justo el caso equivocado. Medido en el proyecto de origen, sobre sus cuatro primeras Tareas reales, con un
   > agente distinto por tarjeta: de las **dos** que reclamaron la exención, **una la tenía mal
   > otorgada** (redundante con su propio test 1), y una tercera dejó sin escribir el guardarraíl
   > que sí le correspondía. La pregunta contrafáctica (*¿qué lo pone en rojo dejando los demás en
   > verde?*) no sale sola al escribir una lista de tests: hay que obligar a escribirla.
9. **Hay al menos una invariante de negocio protegida**, no solo caso feliz + errores de
   formato. La invariante es lo que **nunca** puede pasar aunque el código cambie («un registro vencido
   no aparece en el listado»). Si la lista solo tiene validaciones de
   entrada, la lógica de negocio queda sin red.
10. **No hay tests de implementación.** Un test que se rompe al refactorizar **sin que
    cambie el comportamiento** prueba *cómo* en vez de *qué*. Señales: nombra clases
    internas, cuenta llamadas, depende del orden de ejecución.
    > **Este chequeo NO aplica a los guardarraíles del chequeo 8.** Un test de
    > arquitectura mira la estructura a propósito — esa es su función, no un defecto.
    > La diferencia: el guardarraíl falla cuando alguien **rompe una regla**; el test de
    > implementación falla cuando alguien **mejora el código sin romper nada**.

### Suficiencia (¿la enumeración misma está completa?) — el único bloque que mira hacia afuera

> Los chequeos 1 a 3 miden los tests contra las **listas que la propia Tarea declara**
> (Validaciones, Casos de error, códigos del contrato). Eso deja un agujero de fondo: si
> la enumeración está corta, la Tarea es **internamente perfecta** y pasa todo. Peor: como
> el chequeo 13 castiga los tests que no rastrean a nada, el camino más barato al veredicto
> COMPLETA es **enumerar menos**. Este bloque existe para contrarrestar ese incentivo.

11. **Modos de falla del recurso, declarados o descartados por escrito.** Tienen su sección
    propia en la tarjeta —**«Modos de falla evaluados»**, una línea por familia
    ([[plantillas/tarea]])—; **si esa sección no está, el chequeo es HALLAZGO, no OK**: la
    ausencia del bloque no se puede confundir con «no había nada que declarar». Recorrer las
    familias y verificar que cada una esté **o cubierta o descartada con su motivo**, nunca
    ausente:
    **estado** (la entidad en un estado que no admite la operación), **concurrencia** (dos
    operaciones simultáneas sobre la misma entidad), **autorización** (el usuario no puede
    operar sobre esa entidad), **dependencia caída** (el servicio o la base no responden),
    **límites** (tamaño, cantidad, rango de fechas) e **idempotencia** (repetir la misma
    llamada). Un «no aplica porque …» escrito es una afirmación auditable; el silencio no.
12. **Spec inventada por el redactor.** Cada validación y cada fila de Casos de error tiene
    que rastrear a una `[RN-…]`, al Gherkin del padre o al contrato de un sistema externo.
    Una condición que **decidió el redactor** sin respaldo — un límite de caracteres, un
    código de error, un plazo— es **especificación inventada**: hay que marcarla y
    preguntar de dónde sale. Hoy pasa inadvertida porque los tests que la cubren se ven
    perfectamente trazados… a una línea que alguien escribió de memoria.

### Coherencia (¿la lista cierra con el resto?)

13. **Ningún test sobra.** Cada uno rastrea a una validación, un caso de error, un código
    o campo del contrato, una `[RN-…]` o un Escenario. Un test que no rastrea a nada es
    alcance inventado.
14. **Ningún test depende de un `⚠ pendiente` sin declararlo.** Si el input o el resultado
    esperado no se pueden escribir hasta que el humano responda algo, el ítem tiene que
    decirlo. Escribirlo sin avisar obliga al dev a **inventar el valor**, y ese valor
    inventado queda como si fuera la especificación. Cruzar la lista de tests contra el
    bloque «Datos a confirmar»: **cada pendiente de ese bloque que afecte a un test tiene
    que aparecer marcado en el test**.
    > **Si la sección «Datos a confirmar» no está, este chequeo es HALLAZGO, no OK** — y si
    > está pero vacía sin decir «Ninguno.», también. El cruce es mecánico contra ese bloque:
    > sin bloque da `0 = 0` y **pasa por vacuidad**, que es la Regla del cero de más arriba
    > aplicada a esta misma skill. Una Tarea sin pendientes lo **declara** escribiendo
    > «Ninguno.»; el silencio no es una declaración ([[plantillas/tarea]]).
15. **Coherencia del test de integración y numeración.** Si el Alcance dice «Requiere test
    de integración: sí», tienen que estar las **tres** (test en la lista, subtarea que lo
    escriba, ítem en el DoD). Los tests están numerados y la tabla de Escenarios los
    referencia por número, sin saltos ni números inexistentes.
16. **El resultado esperado de cada test es producible por la CAPA que la Tarea declara.**
    Leer «Capa afectada» del Alcance y contrastarla ítem por ítem contra lo que cada test
    espera. Una Tarea que declara `domain`/`application` y **«no expone endpoint propio»**
    no puede tener tests que esperen un `400` o un `404`: ese código lo emite la capa `api`,
    que la Tarea dice no tener. El test queda **imposible de escribir dentro del alcance**, y
    el dev lo resuelve de una de dos maneras, las dos malas: inventando la capa que la Tarea
    excluyó, o dejando el test sin hacer.
    Y al revés: una Tarea de front cuyos tests **solo asertan sobre el DOM** no verifica el
    objeto que produce, aunque el DoD exija que coincida con el contrato del back — se puede
    renombrar un campo del estado y los siete tests siguen en verde.
    > Se escapa porque **los dos lados están bien por separado**: el alcance es correcto y el
    > test es correcto. Lo que no cierra es la **unión**, y nadie mira una unión salvo que
    > esté escrito que hay que mirarla.

## Flujo

### 1. Conseguir los tres insumos
Leer la Tarea, la Historia padre y las reglas citadas. Si falta alguno, decirlo antes
de empezar y acotar el alcance de la auditoría.

### 2. Correr el script, y después los chequeos de criterio
**Primero el script** —lo corre esta skill, no se le pide a nadie—:

```
python bin/auditar-tarea.py <tarea.html> --historia <criterios-del-padre.html> --json
```

(La Tarea y los Criterios del padre van como archivos: en modo lote son los borradores; si no,
se guardan desde el tablero.) El script hace los chequeos de **conteo y forma**: secciones,
numeración, Escenarios del padre contra la tabla y la línea «No cubre», reglas que existen,
códigos del contrato y filas de Casos de error con su test, test de integración, enlaces,
HTML, guardarraíles, Modos de falla, Datos a confirmar y tamaño. **Esos no se rehacen a mano**:
su resultado se copia al reporte. Lo que el script marca HALLAZGO es hallazgo; si no corrió, esos
chequeos son SIN DATOS. Si esta herramienta no puede correr comandos, se le pide a la persona
ese comando exacto y se espera el resultado.

**Después, sólo los de criterio**: los que el script lista en «Lo que este script NO mira», más
confirmar o descartar sus AVISOS. Para cada hallazgo guardar **qué** falta o sobra y **contra
qué** se detectó (la validación, la fila de la tabla, el código del contrato, el Escenario). Un
hallazgo sin evidencia no se reporta.

### 3. Dar un veredicto por Tarea

| Veredicto | Cuándo | Qué significa |
|---|---|---|
| **COMPLETA** | Los 16 chequeos pasan | No se encontró nada que falte |
| **CON HUECOS** | Falta al menos un test, o hay uno que no puede fallar | Lo que falta se deja como **pendiente a confirmar** en la tarjeta. **No frena el desarrollo** |
| **NO AUDITABLE** | No se consiguió la Historia padre, o una regla citada no existe en el Cerebro | Se dice qué no se pudo mirar, y queda como pendiente. Nunca se da por buena una Tarea que no se pudo auditar, pero **tampoco frena el desarrollo** |

**Tamaño (no cambia el veredicto).** Si la lista pasa de **30 ítems**, el reporte agrega
«conviene partir la Tarea» ([[plantillas/tarea]] §«Tamaño y forma»). No es un hueco: es una
Tarea demasiado grande para leerla y para desarrollarla de un tirón.

**Si se dan las dos a la vez** (faltan tests **y** hay un punto que no se pudo verificar),
el veredicto es **CON HUECOS + NO AUDITABLE en «el punto X»** — se reportan las dos cosas,
no se elige una. Ninguna de las dos frena el desarrollo, pero se arreglan por caminos
distintos: los huecos los cierra quien redacta la tarjeta; lo no auditable exige **cargar
la regla que falta en el Cerebro** o conseguir el insumo. Ocultar una detrás de la otra
deja media Tarea sin arreglar.

### 3-bis. Dejar el veredicto en la tarjeta (constancia, no barrera)

Un veredicto que vive solo en el chat de esta sesión se pierde: mañana otra sesión —u otra
persona, u otro LLM— abre el board y no sabe si se auditó. Por eso, cuando se corre, el
veredicto **se deja en la tarjeta** con [[comentar-tarea]] (que pide su propia confirmación
humana —en modo lote, la del cierre—; esta skill no escribe por su cuenta). Los hallazgos van
en el mismo comentario, como **pendientes a confirmar** ([[comentar-tarea]] §«Pendientes a
confirmar»), para que se vean al cerrar la Tarea. **El sello no habilita ni frena nada:** es
constancia de lo que se miró y cuándo.

```
Auditoria de Tarea - auditar-tarea
Veredicto: COMPLETA | CON HUECOS | NO AUDITABLE
Fecha: <AAAA-MM-DD>
Rev de la Tarea auditada: <System.Rev al LEER la Tarea>
Historia padre: #<ID>
Rev de la Historia padre:  <System.Rev del padre al LEERLA>
Escenarios del padre encontrados: <N>        <- si dice 0, el loop BDD no existe
Hallazgos: <cantidad>  (el detalle, en el reporte)
Pendientes a confirmar:
- <hallazgo, una linea, redactado como pendiente>   <- uno por hallazgo; "Ninguno" si no hay
```

La lista «Pendientes a confirmar» del sello es la que mira la revisión **antes de cerrar** la
Tarea ([[comentar-tarea]] §«Antes de cerrar una Tarea»): un hallazgo que sólo vive en el
reporte del chat no aparece ahí.

**Cuándo vence el sello: cuando cambia lo auditado, no cuando se guarda la tarjeta.** En Azure
**toda** escritura directa sobre un work item crea una revisión: el propio sello (un
comentario de [[comentar-tarea]]), asignarla, pasarla a Active, la regla del tablero que
activa al padre cuando un hijo arranca. Ninguna cambia lo que se auditó.

> Por eso la vigencia **no se mide contando `Rev`**. Con «venció si el `Rev` avanzó» el sello
> **nace vencido** —sellar ya suma una revisión— y con «más de uno» cualquier comentario de un
> dev, o colgarle una Tarea hermana a la Historia, frena Tareas sanas. Un control que se
> dispara por cosas que no tocan lo que controla termina ignorado, que es peor que no tenerlo.

Se mira **qué campos** cambió cada revisión posterior. Cuenta como **cambio de contenido**:

| Dónde | Campos que cuentan |
|---|---|
| La Tarea | Título · Descripción (contrato, SDD, tests, modos de falla) · Criterios de aceptación, si el tipo los tiene · de **qué Historia cuelga** |
| La Historia padre | Título · Descripción · Criterios de aceptación |

**No** cuentan: comentarios (incluido el sello), Estado, Asignado, Etiquetas, Iteración, Área,
estimaciones, ni vínculos a otros ítems (hijos, Related).

- **Vigente**: ninguna revisión de la Tarea posterior a `Rev de la Tarea auditada`, ni de la
  Historia posterior a `Rev de la Historia padre`, cambió un campo de contenido, y la Tarea
  sigue colgando de esa misma Historia.
- **Vencido**: alguno cambió — un Escenario nuevo en la Historia, un `Entonces` editado, un
  test sacado de la lista. Esto cubre el agujero de que el sistema audita **un instante** y
  después nadie mira los cambios.
- **SIN DATOS**: no se pudo leer el historial de cambios. **No es vigente.** Si el motivo es
  de la tarjeta, se re-audita. Si es de **la máquina** —sin token, sin red, sin Python— el
  script lo dice, y re-auditar **no** lo destraba: se arregla el acceso y se vuelve a correr.

**Vale solo el sello más reciente.** Como un comentario ya no vence nada, en la tarjeta puede
haber dos sellos que el script da por vigentes. Manda el **último** (el de mayor `Rev de la
Tarea auditada`): si ese no dice **COMPLETA**, sus hallazgos siguen como pendientes, aunque haya
uno anterior que sí.
Un sello **sin** la línea `Historia padre: #<ID>` (formato anterior) es **SIN DATOS** y se
re-audita: el `#ID` **nunca** se completa con el Parent de hoy, porque entonces se compararía
el padre actual contra sí mismo y daría vigente una Tarea que se movió.

**Si la Tarea cambió de Historia**, el script la da vencida y además hay que correr
[[analizar-tareas]] sobre las Tareas de **las dos** Historias: a la de origen le puede haber
quedado un Escenario que solo cubría la Tarea que se fue, y sus hermanas siguen vigentes.

**Cómo se verifica.** `get_work_item` da cómo está la tarjeta **ahora**, no qué cambió en cada
revisión, y el MCP no expone el historial. Lo lee el script de solo lectura, con los números
del sello, parado en la raíz del repositorio:

```
bash bin/verificar-sello.sh tarea <id-tarea> <Rev de la Tarea> <id-historia> <Rev de la Historia>
```

(En PowerShell, `.\bin\verificar-sello.ps1` con los mismos argumentos.) Sale `0` VIGENTE, `1`
VENCIDO —y dice qué revisión cambió qué campo— o `2` SIN DATOS. Entra igual que el MCP: con
`AZDO_PAT` o, si no está, con la sesión de Azure CLI (`az login`); nunca muestra el token y
solo lee del tablero autorizado.

El sello se postea en HTML ([[comentar-tarea]] §«Formato»), así que quien lo busca lo lee
sobre el texto del comentario **sin las etiquetas**, línea por línea.

**En modo lote** ([[planificar-lote]]) se audita el borrador, antes de que exista la tarjeta.
Al escribir, el lote verifica que el texto de la tarjeta sea **igual al archivo auditado** (con
los `[T-nn]` ya reemplazados por su `#ID`; se compara el texto sin etiquetas y con los espacios
normalizados, porque Azure reescribe el HTML) y recién ahí sella, con la revisión que quedó como
`Rev de la Tarea auditada` y, como `Rev de la Historia padre`, la revisión verificada de la
Historia. Si no son iguales, la tarjeta queda **sin sello**, se re-audita si se quiere, y el
sello nuevo pide su propia confirmación ([[comentar-tarea]]). El formato del sello no cambia,
así que `verificar-sello` lo lee igual.

**El sello no es requisito para desarrollar.** Ni el orquestador ni [[tomar-tarea]] lo buscan
antes de arrancar. Si alguien quiere saber si una auditoría sigue al día, corre
`verificar-sello` a mano; su resultado informa, no bloquea.

### 4. Reportar como hallazgos y preguntas
Agrupar por chequeo. Cada ítem: qué se detectó · evidencia · **la pregunta o el test que
falta**, redactado de forma que se pueda pegar en la tarjeta. No corregir la tarjeta:
eso lo hace [[redactar-tarea]] y lo carga [[cargar-a-azure]], con su confirmación. **Si la
Tarea está congelada** (en un sprint y ya tomada), [[cargar-a-azure]] no la edita: el arreglo
va como comentario y lo carga una persona a mano ([[cambios-en-el-backlog]] §4).

## Barreras

- **Solo lectura del board.** Nunca `create_work_item` / `update_work_item`.
- **No corrige.** Propone el texto del test que falta; escribirlo es otro turno y otra skill.
- **No aprueba por cansancio.** Si un punto no se pudo verificar, es NO AUDITABLE, no «cumple».
- **PHI prohibido** en el reporte (marcadores `<persona>`, `<documento>`, etc.).

## Dónde entra en el flujo

```
redactar-tarea (DoR)  ->  [analizar-tareas, a pedido] (el SET cierra entre sí)
        -> cargar-a-azure §2b (1er chequeo: autochequeo al escribir)
        -> [auditar-tarea]    (2do chequeo, OPCIONAL y a pedido: otro agente)   <- esta skill
        -> desarrollo (no espera a esta skill; sus hallazgos quedan como pendientes)
        -> guiar-tdd (escribe un test por ítem)  ->  verificar-tdd (audita el rojo/verde)
```

Los dos chequeos son **distintos a propósito**: el de `cargar-a-azure` es **mecánico y
de forma** (¿están las secciones, los links, los campos?); este es **de fondo** (¿la
lista de tests cubre todo y sirve?). El primero lo hace quien escribe; el segundo, otro.

## Contexto adicional

- DoR de la Tarea: [[redactar-tarea]] §3.1
- Consistencia del conjunto de Tareas (no de una): [[analizar-tareas]]
- Plantilla y secciones: [[plantillas/tarea]]
- Autochequeo al escribir: [[cargar-a-azure]]

---

### Ejemplo (genérico)

> Una Tarea de capa `api` declara en su contrato los códigos `200`, `400`, `404` y `409`,
> y su tabla de «Casos de error» tiene tres filas. La lista de tests trae 4 ítems: caso
> feliz, `400`, `404` e «invariante de negocio».
>
> La auditoría reporta: **CON HUECOS**.
> - *Chequeo 3:* el código **`409` del contrato no tiene test**. Evidencia: aparece en
>   `responses` del fragmento OpenAPI y en la fila 3 de Casos de error, y ningún test lo
>   espera. Test que falta: «recurso ya tomado → `409` + `RECURSO_NO_DISPONIBLE`».
> - *Chequeo 8:* el test «el endpoint responde un JSON válido» **no puede fallar** —
>   ningún error de implementación lo pondría en rojo. Pregunta: ¿qué comportamiento
>   quería proteger ese test?
>
> No corrige la tarjeta: deja los dos ítems redactados para que el humano los apruebe y
> [[cargar-a-azure]] los cargue en otro turno.
