---
name: disenar-pruebas
description: >-
  El rol de tester: a partir de una Historia con su Gherkin, armar el plan de pruebas de
  aceptación: qué Escenarios se automatizan de punta a punta y cuáles quedan exploratorios,
  los bordes y los datos de prueba (sin datos de personas), el ambiente y el estado inicial, y
  una lista para recorrer a mano lo que no conviene automatizar. No depende de la herramienta
  ni del tipo de aplicación (web, escritorio, móvil, línea de comandos, API): eso lo fija
  DEC-003 y lo ejecuta automatizar-e2e. Usar cuando se pida "diseñá las pruebas de la Historia
  X", "qué probamos de punta a punta", "armá el plan de pruebas", "/disenar-pruebas". No
  inventa pasos: lo que el Gherkin no dice vuelve como pregunta a la Historia. Español
  (Argentina).
---

# Diseñar las pruebas de una Historia

La capa de aceptación prueba **el sistema**, no las piezas: que la aplicación, de afuera y como la
usa una persona, haga lo que la Historia pidió ([pruebas-de-aceptacion.md](../../skills/desarrollo/references/metodo/pruebas-de-aceptacion.md)).
Esta skill decide **qué** se prueba y **con qué datos**; [[automatizar-e2e]] decide **cómo** se
ejecuta en cada tipo de aplicación.

## Lo que NO hace

- **No inventa Escenarios ni pasos.** El Gherkin de la Historia es la fuente. Si para probar hace
  falta algo que no dice (un dato, un estado previo, qué pasa en un borde), es un hueco de la
  Historia: vuelve como pregunta ([[comentar-tarea]]), no se tapa en el plan.
- **No usa datos de personas.** Fábricas y marcadores (`<persona>`, `<documento>`), siempre.
- **No escribe pruebas** (eso es [[automatizar-e2e]]) ni decide la herramienta (`DEC-003`).

## El plan vive en la tarjeta (no se duplica nada)

La Historia ya trae los Escenarios completos y cada Tarea ya mapea esos Escenarios a sus tests unitarios
(tabla SDD). El plan **no repite nada de eso**: es un **comentario corto en la tarjeta de la Historia**
(`bin/tablero-local.py comentar`, o `comentar-tarea` en Azure) con sólo lo que la tarjeta no dice. Si no
falta nada, el plan es una línea: «se automatizan los Escenarios N y M; el resto queda cubierto por los
unitarios de las Tareas X e Y». Lo que puede faltar:

1. **Qué se automatiza de punta a punta y qué no**, Escenario por Escenario, con el motivo. Lo que la tabla
   SDD ya cubre con unitarios no se vuelve a probar de punta a punta salvo que cruce piezas:

   | Se automatiza | Queda exploratorio |
   |---|---|
   | El camino feliz de cada flujo principal | El estilo visual, el texto de ayuda, lo que cambia seguido |
   | El error visible de cada flujo que da plata | Variantes de borde de una sola pieza (van en el unitario) |
   | Lo que cruza piezas (front + back + base) | Lo que requiere un ambiente que no existe todavía |

   **Pocas y rápidas**: la pirámide manda (muchos unitarios, poquísimas de punta a punta).
2. **Bordes que la tarjeta no tiene**: sólo los que no están ni en el Gherkin ni en los «Modos de falla» de
   las Tareas; cada uno es una pregunta a la Historia, no un caso inventado.
3. **Datos y estado inicial** (si las **Notas para QA** de la Historia ya los traen, no se repiten: se cita la tarjeta): qué datos siembra la suite antes de cada corrida (fábricas, sin
   datos de personas), contra qué ambiente corre, qué usuario de prueba usa y cómo se autentica
   (por variable de entorno; nunca en el archivo).
4. **Lista exploratoria**: lo que una persona recorre a mano en diez minutos, en orden, con qué
   mirar en cada paso. Es parte del plan, no un «después vemos».
5. **Identificadores que el front tiene que exponer** para que las pruebas no sean frágiles: un
   atributo de automatización por control (el patrón lo fija `DEC-003`: `data-testid` o
   `automation-id`), nombre accesible y estado como atributo. Si falta uno, es una Tarea de front.

## Pasos

1. Leer la Historia del tablero (`bin/tablero-local.py ver <id>`, o la tarjeta), sus Tareas (la tabla SDD
   dice qué cubre cada unitario) y la ficha que cita. Sin Gherkin, **se frena**: la Historia se redacta
   primero ([[redactar-tarea]]).
2. Armar el plan con lo que la tarjeta no dice. Lo incierto va `⚠` con su pregunta.
3. Mostrarlo y esperar el «sí». Con el «sí»: el plan queda como comentario en la Historia, las preguntas
   como pendientes, y los Escenarios a automatizar pasan a [[automatizar-e2e]]. Ningún archivo nuevo.

## Barreras

- Un Escenario del Gherkin **no se descarta**: o se automatiza, o queda exploratorio con motivo.
- Sin datos de personas, sin credenciales en archivos, sin ambiente de producción.
- Todo en español (Argentina).

## Cómo entra en el veredicto

| Estado | Cuándo |
|---|---|
| **OK** | Cada Escenario de la Historia tiene su decisión (automatizar o exploratorio), sin repetir lo que la tarjeta ya dice |
| **HALLAZGO** | Un Escenario sin decisión, un paso inventado, un dato de persona |
| **SIN DATOS** | La Historia no tiene Gherkin, o `DEC-003` no fijó el tipo de aplicación |
