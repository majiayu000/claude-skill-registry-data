---
name: automatizar-e2e
description: >-
  El rol de QA automatización: escribir y mantener las pruebas de punta a punta de una Historia
  con el motor que DEC-003 fija según el tipo de aplicación: Playwright para web y Electron (y
  para el front de una app de escritorio con webview, probado en navegador), WebDriver para
  Tauri o escritorio nativo, Appium o Maestro para móvil, un proceso para una línea de comandos,
  HTTP para una API. El esqueleto lo arma bin/armar-e2e.py desde el Gherkin (un test por
  Escenario, con el título textual y la traza Historia #id · Escenario), la skill completa los
  pasos sin inventar, y bin/cobertura-e2e.py dice qué Escenarios quedaron sin prueba. Usar cuando
  se pida "automatizá la Historia X", "escribí las pruebas de punta a punta", "qué cobertura e2e
  tenemos", "/automatizar-e2e". Sin datos de personas; secretos por variable de entorno. Español
  (Argentina).
---

# Automatizar las pruebas de punta a punta

El plan lo arma [[disenar-pruebas]]; acá se **ejecuta**: una prueba por Escenario, contra la
aplicación corriendo, con la herramienta que corresponde al tipo de aplicación. El método de la
capa está en [pruebas-de-aceptacion.md](../../skills/desarrollo/references/metodo/pruebas-de-aceptacion.md).

## El motor lo fija el tipo de aplicación (`DEC-003`)

| Tipo de aplicación | Motor | Esqueleto (`--motor`) | Detalle |
|---|---|---|---|
| **Web** (navegador) | Playwright | `playwright` | [playwright.md](references/playwright.md) |
| **Electron** | Playwright (modo Electron) | `playwright` | [playwright.md](references/playwright.md) |
| **Escritorio con webview** (Tauri, Wails) | Playwright sobre el front en navegador con la API nativa simulada, y WebDriver (`tauri-driver`) para los flujos que tocan el sistema | `playwright` + `proceso` | [otros-tipos.md](references/otros-tipos.md) |
| **Escritorio nativo** (Windows, macOS) | WebDriver de la plataforma (WinAppDriver, XCUITest) o automatización por accesibilidad | `proceso` | [otros-tipos.md](references/otros-tipos.md) |
| **Móvil** | Appium o Maestro | `proceso` | [otros-tipos.md](references/otros-tipos.md) |
| **Línea de comandos** | Ejecutar el proceso y observar salida, archivos y código de salida | `proceso` | [otros-tipos.md](references/otros-tipos.md) |
| **API sin pantalla** | HTTP contra el ambiente (`urllib`, o el cliente del stack) | `http` | [otros-tipos.md](references/otros-tipos.md) |

Si `DEC-003` no fijó el tipo, **se pregunta** y se escribe ahí; la skill no elige.

## Dónde viven

`qa/<app>-e2e/` (o dentro del repo de código si `DEC-003` lo decide): `tests/` (un archivo por
Historia), `objetos/` (un objeto por pantalla o por recurso, con los identificadores estables),
`datos/` (fábricas, sin datos de personas). El plan de [[disenar-pruebas]] es un comentario en la Historia, no un archivo acá. Las
dependencias se instalan **por proyecto, con la persona** (Playwright, Appium…), nunca se
vendorizan; el ambiente y las credenciales van por variable de entorno.

## Pasos

0. **La tarjeta ya tiene todo**: los Escenarios completos en la Historia y, en sus Tareas, la tabla SDD que dice qué
   cubre cada test unitario. De punta a punta se automatiza **sólo lo que cruza piezas** (front + back + base, o
   el sistema entero); los bordes que un unitario ya cubre no se repiten acá. Las **Notas para QA** de la Historia
   traen pantalla y ruta, rol, datos iniciales, identificadores y ambiente: `armar-e2e.py` las usa y avisa lo que falte;
   eso vuelve como pregunta a la Historia, no se completa de memoria.
1. **Esqueleto por script**:
   ```bash
   python bin/armar-e2e.py "#<id>" --motor <playwright|proceso|http> --salida qa/<app>-e2e/tests [--url <base>]
   ```
   Un test por Escenario, con el título textual, la traza `Historia #<id> · Escenario: <título>` y los
   pasos del Gherkin como comentarios; cada uno nace **marcado sin automatizar** (`test.fixme` /
   `unittest.skip`): el esqueleto no es un verde falso. Si el archivo ya existe, el script dice qué
   Escenarios le faltan y no lo pisa.
2. **Completar cada Escenario** siguiendo sus pasos, uno a uno, sin inventar: buscar por rol y nombre
   accesible o por el identificador estable que fija `DEC-003`; esperar estados como atributo, nunca
   dormir segundos fijos; un Escenario, una prueba, un resultado observable. Al terminar, sacar la marca
   de sin automatizar.
3. **Datos y estado**: cada corrida arranca de un estado conocido (siembra propia de la suite); los
   datos salen de `datos/` con marcadores; el usuario de prueba y la URL, del entorno.
4. **Correr contra el ambiente** declarado y mirar el resultado real. Una prueba que «a veces falla»
   se arregla o se saca, no se marca y se sigue.
5. **Cobertura**:
   ```bash
   python bin/cobertura-e2e.py qa/<app>-e2e --historias cerebro-digital/<modulo>/backlog
   ```
   Escenario por Escenario: automatizado, sólo esqueleto o sin prueba. Lo que falta queda a la vista
   en el cierre de la Historia.
6. **Huecos**: si al automatizar aparece algo que el Gherkin no dice (un dato, un estado, un mensaje),
   vuelve como pregunta a la Historia ([[comentar-tarea]]). Si al front le falta un identificador
   estable, es una Tarea de front, no un selector frágil.

## Barreras

- **El Gherkin es la fuente**: ni un paso ni un resultado que la Historia no diga.
- **Sin datos de personas** en pruebas, fábricas ni capturas; **sin secretos** en archivos.
- **Nunca contra producción**; el ambiente se declara y está escrito en `DEC-003`.
- **Un esqueleto no cuenta como prueba**: `cobertura-e2e.py` lo distingue y el cierre lo muestra.
- Todo en español (Argentina).

## Cómo entra en el veredicto

| Estado | Cuándo |
|---|---|
| **OK** | Cada Escenario a automatizar tiene su prueba, con traza, y pasó contra el ambiente declarado |
| **HALLAZGO** | Un Escenario sin prueba o sólo esqueleto en un flujo principal, una prueba sin traza, pasos inventados, un dato de persona |
| **SIN DATOS** | `DEC-003` sin tipo de aplicación o sin ambiente; la suite no corrió |
