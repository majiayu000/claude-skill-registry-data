---
name: verificar-tdd
description: >-
  (Repos de front · desarrollo) Auditar la evidencia del ciclo TDD de una Tarea: que cada
  ítem de la lista "Tests a escribir PRIMERO" tenga su prueba de rojo (el test fallando en
  su aserción) ANTES del código, y que el verde final pase. Lo corre un agente SEPARADO del
  que escribió el código. Usar cuando se pida "verificá el TDD", "auditá la evidencia",
  "¿esto cumple test-first?", "/verificar-tdd". NO escribe código de producción ni arregla
  tests: audita y reporta. Español (Argentina).
---

# Verificar TDD (frontend)

Audita que el TDD **haya ocurrido de verdad**, no que se declare. Es el control que
convierte la regla de `guiar-tdd` en evidencia verificable.

## La pregunta que contesta esta skill

**¿El ciclo ocurrió?** Hubo rojo en la aserción antes del código; el verde pasa hoy.
La frontera con los otros controles está en **una sola tabla**: «Quién contesta qué», en
`cerebro-digital/configuracion-ia/orquestador-desarrollo.md` del núcleo. No se repite acá para que no diverja.

Un cambio puede tener **TDD impecable y estar mal hecho**: por eso son auditorías distintas.

## Independencia (la razón de existir)

**Quien escribió el código NO corre esta verificación.** Se ejecuta en una pasada separada,
con contexto propio. Si el mismo agente codea y se aprueba a sí mismo, no hay control —
hay una declaración.

## Regla de oro
- **NO escribe código de producción ni arregla los tests.** Audita y reporta.
- **NO inventa.** Si falta evidencia, se reporta como faltante; nunca se asume que el ciclo
  se cumplió porque la pantalla "se ve bien".
- **Un rojo válido falla en su aserción.** Rojo por import roto, componente inexistente o
  configuración de la API simulada **no cuenta**: se marca como evidencia inválida.
- **Español (Argentina).**

## Primero el script, después el criterio

Lo que es **conteo sobre el historial** lo mide `bin/verificar-tdd.py` del repositorio del Cerebro,
siempre igual y sin tokens: por ítem, que el commit `test(rojo): <n>` traiga sólo tests y tenga un
commit de producción después; los ítems de la lista que no tienen rojo; la rama `evidencia/<ID>` y
que `git diff evidencia/<ID> HEAD` esté vacío.

```bash
python <ruta del repositorio del Cerebro>/bin/verificar-tdd.py --repo <worktree> --base <sha-base> [--items <N>] --id <ID> --modo <tdd|test-despues|caracterizacion|sin-tests> [--motivo "<el motivo escrito en la Tarea>"]
```

El `--modo` es el campo «Modo de pruebas» de la Tarea, **textual**: si la Tarea no lo declara, es `tdd`; un
`test-despues` sin motivo el script lo audita como `tdd` y lo marca. En `test-despues` exige la red mínima
(tests y producción en el rango) en vez del rojo por ítem; en `caracterizacion`, que el primer commit congele
(`test(caracterizacion): …`) antes de tocar producción; en `sin-tests` devuelve `SIN DATOS` con el motivo.
Un `chore(firma): …` (sólo firmas vacías antes del primer rojo) y un `test(verde-de-entrada): <n>` (ítem que nació
verde, pendiente a confirmar) son parte del método (`guiar-tdd`) y el script los reconoce. Lo que el script marca `falta` o `evidencia invalida` no lo da por bueno la skill. Un script que no
corrió es `SIN DATOS`, no OK. Lo que sigue es **lo que pide criterio** y el script no mira: la aserción
literal (punto 1), el verde de hoy (punto 3), el código huérfano y el cierre BDD↔TDD.

## Qué audita (por cada ítem de la lista de la Tarea)
1. **Existe el test** que corresponde a ese ítem, y **la aserción dice lo mismo que el ítem**.
   No alcanza con que el test exista: hay que **citar la línea de la aserción** y comprobar
   que contenga el resultado esperado **literal** del ítem — el código **y** el payload o el
   campo. Un ítem que pide `409 + RECURSO_NO_DISPONIBLE` cubierto por un test que sólo
   asevera `status == 409` **no está cubierto**: el back puede devolver `409` con
   otro código de error y el test sigue verde, mientras el front —que simula el contrato—
   muestra el mensaje equivocado. Es el hueco entre «auditar el texto antes del código»
   (`auditar-tarea`) y «auditar la mecánica después» (este chequeo): nadie compara el ítem
   con el test realmente escrito. El veredicto de este punto se da **por ítem, citando
   archivo y línea**; sin cita, es `evidencia inválida`.
   En un ítem **«Esquema»** se cita la fuente de datos del test parametrizado y se comprueba
   que tenga **cada** fila del ítem con su resultado esperado literal; una fila que falta es
   `falta`.
2. **Hay evidencia del rojo** previa al código, y falla **en la aserción**.
   La evidencia se lee del **historial de git del worktree**, no de un texto pegado: tiene
   que existir un commit `test(rojo): <n.º de ítem> …` que contenga **solo el test** y sea
   **anterior** al commit que implementa ese ítem. Se verifica con `git log`, que es un dato
   duro y no se puede falsificar desde el chat. Se mira el **historial de trabajo**, antes de
   que la rama se reorganice para el Merge Request; si ya se reorganizó, se mira la rama
   `evidencia/<ID>` (local o `origin/evidencia/<ID>`), y si no existe, es `SIN DATOS`. Un rojo pegado a mano en un `.md` es
   indistinguible de uno fabricado: comentar la implementación, correr el runner, pegar la
   salida roja y descomentar produce exactamente el mismo artefacto.
   **En sólo lectura el rojo se verifica por lectura, sin checkout:** el test del commit `test(rojo)` (su
   aserción) contra el estado de producción del commit anterior (`git show <sha>^:<archivo>`); las líneas de
   la salida roja están en el cuerpo del commit (`git log -1 --format=%B <sha>`) como apoyo, no como prueba.
   **Los tests declarados guardarraíl están exentos de este punto** (nacen verdes a
   propósito); se verifica que estén declarados como tales en la Tarea, no que tengan rojo.
3. **El verde pasa** hoy (se corre el runner de tests del front, no se confía en el reporte).
4. **Cobertura de la lista**: ningún ítem de "Tests a escribir PRIMERO" quedó sin test.
5. **Cobertura del contrato**: está cubierto el caso feliz **y cada 4xx** de la tabla
   "Casos de error" de la Tarea, simulados desde el contrato. **Si la Tarea declara que no toca la API**,
   este punto es `N/A` y se dice así.
6. **Sin tests de implementación**: si un test se rompe al refactorizar sin cambiar el
   comportamiento, se marca como test mal escrito. Los `data-testid`, `data-*` y clases que **el contrato de
   la Tarea fija** no son detalle de implementación: son contrato, y el test tiene que buscarlos.
7. **Cierre del loop BDD↔TDD (contra la Historia padre, no contra la Tarea).** El campo
   **Criterios de aceptación** de la Historia padre viene **pegado en la misión** (lo lee el orquestador,
   que sí tiene el tablero; el verificador no lee el board ni usa MCP); **si la misión no lo trae, decilo y
   marcá el chequeo 7 como SIN DATOS (no se pudo mirar): nunca lo des por cumplido ni reconstruyas el
   Gherkin de memoria** — y contrastarlo con la tabla de
   «Especificación cerrada (SDD)» de la Tarea:
   - cada **Escenario** que la Tarea declara cubrir tiene sus tests **existiendo y en verde**;
   - los títulos de Escenario de la tabla **existen textualmente** en el Gherkin del padre
     (si no coinciden, la trazabilidad es falsa: se reporta, no se corrige por cuenta propia);
   - los Escenarios que la Tarea declara cubrir **solo en parte** nombran la Tarea
     complementaria, y se deja dicho en el veredicto que **el Escenario NO está cerrado
     todavía** — cerrarlo exige que la otra Tarea también esté verde.
   Ojo con el falso verde del front: **la API está simulada, no es el back real**, así que un
   Escenario puede dar verde acá y estar roto contra el back de verdad. Si la tabla dice que el
   Escenario se comparte con una Tarea de backend, decilo explícito en el veredicto.
   Este es el único chequeo que mira el **comportamiento que pidió el negocio**; los otros seis
   miran la mecánica. Que la Tarea esté verde entera **no** prueba que el Escenario esté cerrado.

## Salida

El formato es el bloque canónico `VEREDICTO-INICIO … VEREDICTO-FIN` de [[orquestador-desarrollo]] §«Formato
del veredicto»: esta skill aporta la línea del control 5 (con el resultado del script al lado) y sus
hallazgos, uno por línea, separando `SIN DATOS (no se pudo mirar)` de `SIN DATOS (pendiente declarado)`.

Un veredicto **por ítem** — `cumple` / `evidencia inválida` / `falta` — con la evidencia que
lo respalda. Lo que no cumple se devuelve **como hallazgo o pregunta**, nunca como algo que
el verificador arregle por su cuenta.

## Barreras
- **No autoriza la entrega por sí solo:** aporta evidencia; deciden el humano y la política
  del repo.
- Si la Tarea no trae la lista de "Tests a escribir PRIMERO", se frena y se avisa: la Tarea
  no estaba lista para desarrollarse.
- **Si la Tarea implementa un Escenario de la Historia y no trae la tabla de «Especificación
  cerrada (SDD)», se frena igual**: sin esa tabla no hay contra qué auditar el chequeo 7, y la
  Tarea no pasó el DoR (ver `redactar-tarea` §3.1). Avisar que se despachó una Tarea incompleta
  — no inventar el mapeo para poder seguir. **Ojo con la condición en el front:** acá las Tareas
  no tienen capa `api`/`application`/`domain`, así que el disparador **no** es la capa sino
  «implementa un Escenario». Solo queda exenta la Tarea de **puro UI/config** (una columna en
  una grilla, un texto) que no responde a ningún Escenario del padre.
