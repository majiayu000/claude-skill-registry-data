---
name: guiar-tdd
description: >-
  (Repo back · desarrollo) Gobernar el ciclo TDD Red-Green-Refactor sobre la lista
  "Tests a escribir PRIMERO" que dejó la Tarea del tablero: primero el test que falla
  (rojo), después el código mínimo que lo hace pasar (verde), después refactor. Si
  detecta código de producción sin su test previo, lo revierte y vuelve a rojo. NO
  genera el código de la solución: gobierna CÓMO se escribe. Los tests se escriben con
  el runner de tests del repo. Usar cuando se pida "guiá el TDD", "arrancá en rojo", "forzá test-first",
  "/guiar-tdd". Español (Argentina).
---

# Guiar TDD (backend)

Hace cumplir el orden test-first sobre la lista de tests que la Tarea del tablero ya trae
cerrada. No escribe la solución: es el árbitro del ciclo.

## Regla de oro
- **Rojo antes que verde, siempre.** No se escribe código de producción sin un test
  que falle primero, y que falle **por la razón correcta**.
- **Código sin test = revertir.** Si aparece implementación sin su test previo, se
  vuelve al último estado en rojo.
- **Un test por ítem** de la lista "Tests a escribir PRIMERO" de la Tarea; no se
  inventan casos fuera de esa lista (si falta uno, no se inventa: se anota como pendiente a
  confirmar en el resumen final, para la tarjeta). Si un ítem **enumera dos comportamientos del mismo
  contrato**, van como **dos aserciones en el mismo test** (un solo `test(rojo): <n>`), no se parte el ítem
  ni se inventa un segundo número; si son de contratos distintos, se anota como pendiente («el ítem n son dos»).
  Un caso que los «Modos de falla» atribuyen al ítem n sin que el ítem lo enumere **no se agrega**: se anota.
- **Un ítem «Esquema»** (la misma condición con varias filas de datos) se escribe como **un
  test parametrizado con una fila por cada fila del ítem**, ni una más ni una menos, cada una
  con su resultado esperado; su `test(rojo)` es uno solo. Cada ítem se lee junto con el
  párrafo «Datos base» de la lista, si lo hay.
- **No inventar comportamiento.** El qué probar sale del contrato OpenAPI y los
  `[RN-…]` de la Tarea, no del criterio del que codea.
- **Modo de pruebas declarado.** Si la Tarea declara `test-después` o `sin tests` **con motivo**
  (esqueleto, configuración, migración, UI puramente visual, spike), el árbitro no exige el rojo
  por ítem pero sí la **red mínima** que ese modo pide (ver `tdd-ciclo-y-evidencia.md` §«Cuándo
  TDD»). Sin motivo escrito, es TDD.
- **Español (Argentina).**

## Flujo (por cada ítem de la lista de la Tarea)
1. **Red:** escribir el test (con el runner de tests del repo); correrlo y verificar que FALLA por
   la razón esperada.
2. **Green:** el código mínimo que lo hace pasar. Nada de más.
3. **Refactor:** limpiar con los tests en verde.
4. Repetir hasta agotar la lista. Al terminar, cada test de la Tarea tiene su caso.

## Evidencia del rojo (obligatoria)

El ciclo no vale **por declaración**: hay que dejar **prueba** de que el test falló antes
de que existiera la solución.

- Al cerrar el paso **Red**, se guarda la **salida del runner** mostrando el test fallando: las **1 a 3 líneas de la aserción**, en el
  **cuerpo del commit `test(rojo)`** (no en un archivo: ahí viaja con la evidencia y no se puede fabricar después).
- **Un rojo válido falla en su aserción.** Si falla por error de compilación, import roto
  o configuración, **NO cuenta como rojo**: hay que llegar a la aserción y fallar ahí.
- Recién con esa evidencia se escribe el código del paso **Green**.
- Cada evidencia queda asociada a **su ítem** de la lista "Tests a escribir PRIMERO".
- **Quien escribe el código NO aprueba su propia evidencia.** Esa auditoría la hace
  `verificar-tdd`, en una pasada separada.

## Test de integración (si la Tarea lo pide)
La Tarea declara **"Requiere test de integración: sí/no"**. Si dice **sí** (toca una
dependencia externa: un sistema externo, una base de datos, una cola), además del ciclo unitario
va un test de integración que ejercita esa dependencia real o su doble controlado. El
orden **no cambia**: primero el test de integración **en rojo**, después el código.

## Entrada / Salida
- **Entrada:** la Tarea del tablero: contrato OpenAPI + **tabla de «Especificación cerrada (SDD)»**
  (qué Escenarios de la Historia padre cubre esta Tarea y qué test verifica cada uno) +
  **el cuerpo del Gherkin de esos Escenarios** (los `Dado`/`Cuando`/`Entonces`/`Y`, no solo
  el título: un Escenario suele tener varios pasos observables y la tabla solo trae uno por
  fila — sin el cuerpo no se puede saber si el test cubre el Escenario entero o un pedazo) +
  lista numerada de tests test-first.
- **Salida:** tests + código, con trazabilidad 1:1 contra la lista de la Tarea, y **cada test
  nombrado de forma que se vea a qué Escenario responde** (el número de test que la tabla SDD
  le asignó). Así el que audita puede ir del Escenario al test sin adivinar.

> **Para qué sirve la tabla SDD mientras codeás.** La lista de tests dice *qué* probar; la tabla
> dice *para qué* — qué comportamiento de negocio, escrito en el Gherkin de la Historia, queda
> cubierto cuando ese test se pone verde. Cuando un ítem de la lista es ambiguo, la respuesta está
> en el Escenario al que la tabla lo asocia. Si la tabla dice que esta Tarea cubre **solo parte**
> de un Escenario, **no** implementes la otra parte: es de la Tarea complementaria que la tabla nombra.
> Si la Tarea no trae la tabla, avisá: no pasó el DoR y vas a estar adivinando el porqué.

## Cómo se deja la evidencia del rojo (obligatorio)

Un commit por paso rojo, **antes** del código que lo pone en verde:

```
test(rojo): 3 recurso ya no disponible -> 409 RECURSO_NO_DISPONIBLE
```

Ese commit lleva **solo el test**, nada de producción. Después va el commit de la
implementación. `verificar-tdd` lo audita con `git log`: si el test no precede a su
implementación, el rojo no existió.

**Por qué así y no pegando la salida del runner en un archivo:** un texto pegado es
indistinguible de uno fabricado. Comentar la implementación, correr el runner, pegar el
rojo y descomentar produce exactamente el mismo artefacto que hacer TDD de verdad. El
orden de los commits, en cambio, es un dato del repo que no se escribe desde el chat.

**Los tests declarados guardarraíl no llevan commit de rojo** — nacen verdes a propósito.
**Dos casos que el método blanquea** (si no, el agente improvisa): (a) cuando la clase o la función todavía no
existe, el rojo falla por import y no en la aserción; entonces va **antes** un commit `chore(firma): …` con sólo
las firmas vacías (sin comportamiento), y recién después el `test(rojo)`; `verificar-tdd.py` lo reconoce y no lo
cuenta como producción antes del rojo. (b) Si un ítem **nace verde** porque el verde mínimo de otro ya lo cubre, no
se rompe el otro a propósito: se commitea `test(verde-de-entrada): <n> …` con sólo el test y se anota como
pendiente a confirmar (¿la Tarea debía declararlo guardarraíl?); el verificador lo da por cumplido sin rojo.

- **Si una firma nueva rompe la compilación de un test que ya existía** (un tipo que ganó un campo obligatorio, una
  función que cambió de forma), su **ajuste mínimo va en el mismo `chore(firma)`**: es la consecuencia del cambio de
  forma, no un test nuevo. Cualquier otro cambio a un test existente es un rojo propio, con su commit `test(rojo)`.

Van en su propio commit `test(guardarrail): …` para que se vea que la excepción es
deliberada y no un rojo que faltó.

**Estos commits son de trabajo y no van al Merge Request: no los pushees vos.** Después de la
verificación, y con la aprobación del humano, la rama se reorganiza **por importancia**, uno
por cambio lógico (alrededor de 10 commits, como guía), y el historial de trabajo queda en la
rama `evidencia/<ID>`, que se sube a `origin` como respaldo, sin Merge Request (`orquestador-desarrollo` §«Commits: de trabajo, y pocos en el Merge
Request»).

## Barreras
- No genera la solución "de una"; sin test en rojo no hay código de producción.
- Si la Tarea **no trae** contrato o lista de tests, se frena: no pasó el DoR. Si están pero
  les falta algo puntual (un dato, un caso, una decisión `⚠`), **no se inventa ni se frena**:
  se hace lo que no depende de eso y se devuelve como **pendiente a confirmar**, que queda en
  la tarjeta. Si hace falta contexto de negocio, se usa `consultar-cerebro`.
