---
name: absorber-aplicacion
description: >-
  Tomar una aplicación EXISTENTE (con o sin documentación) y absorberla al ecosistema: inventariarla
  y radiografiarla con scripts (endpoints, entidades, estados, pantallas, reglas candidatas,
  integraciones, permisos, dependencias, cada hecho con archivo:línea), leerla módulo por módulo y
  volcar al Cerebro Digital lo que encierra pasando cada ítem por la Consulta Interactiva de Decisión
  con su marca de confianza. Termina con el Cerebro poblado y la matriz de cobertura: la decisión
  (DEC-004), la red y la ejecución son de planificar-modernizacion, caracterizar-comportamiento y
  modernizar-slice. Sirve también sólo para documentar (ingeniería inversa). Usar cuando se pida
  "absorbé esta app", "hacé ingeniería inversa de esta aplicación", "sacá todo lo que hace este repo
  y metelo en el Cerebro", "/absorber-aplicacion". NO modifica la aplicación: sólo la lee. Español
  (Argentina).
---

# Absorber una aplicación existente

El template también sirve cuando la aplicación **ya existe**. Esta skill la lee entera y la vuelca al
Cerebro con las mismas reglas que un documento funcional (nada entra sin un "sí" por ítem). **Termina
ahí**, con el Cerebro poblado y la matriz de cobertura: qué se hace después con la aplicación (refactor en
el lugar, migración, subir de versión o nada) lo decide la persona en [[planificar-modernizacion]].

> **Es el mismo pipeline, con otra fuente.** Un documento funcional es texto que una persona escribió;
> una aplicación es texto que una máquina ejecuta. Las dos se leen, se proponen como borrador en
> `borrador/`, se validan ítem por ítem y recién entonces entran al Cerebro ([[cerebro-orquestador]]
> §«Flujo de curaduría»). Lo que cambia es que acá la lectura la ordena un inventario.

## Lo que NO hace

- **No toca la aplicación existente.** Ni un archivo, ni un commit, ni una rama. En migración no la toca
  nunca; en refactor la tocan las Tareas del pipeline, con red de tests primero, no esta skill.
- **No decide refactor ni migración.** Eso es [[planificar-modernizacion]]: `DEC-004` la decide la persona y la escribe `cerebro-curator` con su "sí".
- **No infiere reglas de negocio del código sin decirlo.** Una validación en el código es una
  *regla candidata* (`⚠`), no una regla: puede ser un bug. Se marca de dónde sale y se pregunta.
- **No escribe en el Cerebro** por su cuenta: lo hace `cerebro-curator` con lo validado.

## Fase 0 — Encuadre (un turno)

Antes de leer nada, se confirma con el humano, en criollo:

- **Qué aplicación** (ruta local del repositorio o del clon; si no está clonada, se clona **afuera** de este repositorio, en una carpeta que se pregunta).
- **Qué se espera**: **sólo documentarla** (ingeniería inversa: la skill termina en la fase 2, con el Cerebro poblado y la matriz de cobertura; no hay `DEC-004`), refactorizarla, migrarla, o todavía no se sabe (es lo normal).
- **Qué parte**: entera o un módulo. Entera es lo recomendable para el inventario; la lectura fina puede ir por módulo.
- **Si la aplicación todavía no existe** (hay sólo documentación: un Cerebro propio, ADR, `.feature`, notas): **no se absorbe como app**. Los documentos entran por la curaduría de [[cerebro-orquestador]] (borrador en `borrador/`, Consulta Interactiva por ítem), los ADR como `DEC-nnn` heredadas con su fecha y su origen, los `.feature` como Escenarios de sus Historias, las reglas no negociables como candidatas; el inventario y la radiografía se corren recién cuando haya código.
- **Si el proyecto ya trabaja con IA** (tiene `CLAUDE.md`, skills, comandos, `.mcp.json`): se releva primero con `bin/relevar-config-ia.py <repo> --nucleo <núcleo>` y se sigue [adoptar-proyecto-existente.md](../../skills/desarrollo/references/metodo/adoptar-proyecto-existente.md): el repo se enchufa, no se muda; lo durable va al Cerebro ítem por ítem; su `CLAUDE.md` queda corto e importa `AGENTS.md`.
- **Qué NO se puede hacer**: p. ej. "no se toca producción", "no se instala nada", "no se sube código afuera".

## Fase 1 — Inventario (lo cuenta un script)

> Si el proyecto entró por `bin/adoptar-proyecto.py`, el relevamiento, el inventario, la radiografía y los diagramas
> **ya están** en `borrador/adopcion/<fecha>-<nombre>/`: se leen, no se vuelven a correr (misma fecha, mismo código).

```bash
python bin/inventariar-codigo.py <ruta-de-la-app>          # resumen en criollo
python bin/inventariar-codigo.py <ruta-de-la-app> --json   # para el borrador
```

Devuelve, sin criterio: lenguajes por extensión, archivos de build, pipeline, contenedores,
**contratos de API** (si no hay, es lo primero que falta), migraciones de base, proporción de tests,
deuda declarada, archivos que parecen secretos (sólo nombres), datos del repositorio y el bloque
**«Para DEC-004»**: las filas medibles de la tabla de estrategias de [[planificar-modernizacion]], ya medidas. Se guarda tal
cual en `borrador/absorcion/<fecha>/01-inventario.md` y, con el «sí», es la primera versión de
`<modulo>/aplicacion/mapa.md`. **Si el script no corrió, la fase es `SIN DATOS`**: no se reemplaza
con una impresión.

## Fase 1-bis — Radiografía (lo señala un script)

```bash
python bin/radiografiar-codigo.py <ruta-de-la-app>          # resumen por secciones
python bin/radiografiar-codigo.py <ruta-de-la-app> --json > borrador/absorcion/<fecha>/01b-radiografia.json   # para la matriz de cobertura y el corpus de paridad (armar-corpus.py)
python bin/radiografiar-codigo.py <ruta-de-la-app> --mermaid > borrador/absorcion/<fecha>/01c-diagramas.md   # modulos y ER, en texto
```

Si Archify está instalado en la máquina (opcional, `DEPENDENCIAS-EXTERNAS.md`), el diagrama interactivo
HTML va a `borrador/absorcion/<fecha>/diagramas/`; lo que entra al Cerebro sigue siendo el Mermaid.

Devuelve, **cada hecho con `archivo:línea`**: endpoints implementados y rutas del contrato, entidades,
tablas, enums y campos de estado (candidatos a máquina de estados), pantallas, **reglas candidatas**
(validaciones, condiciones que frenan con su mensaje, constantes con nombre, cambios de estado,
funciones de cálculo), integraciones (clientes HTTP, URLs y conexiones con credenciales enmascaradas,
mensajería, tareas programadas, autenticación), permisos con sus roles, y las dependencias entre módulos
con ciclos y cruces de capa. Se guarda en `borrador/absorcion/<fecha>/01b-radiografia.md`. **La lectura de la
fase 2 empieza por lo que la radiografía señaló**, módulo por módulo, y no al revés. Lo que la radiografía
no reconoce (un stack fuera de sus tablas) se dice; no se completa de memoria. El método entero —fuentes,
marcas de confianza, evidencia, cobertura— está en
[ingenieria-inversa.md](../../skills/desarrollo/references/metodo/ingenieria-inversa.md).

## Fase 2 — Lectura y extracción (criterio, con la Consulta Interactiva)

Se lee de afuera hacia adentro, como manda [entender-codigo-ajeno.md](../../skills/desarrollo/references/metodo/entender-codigo-ajeno.md):
README y contrato → carpetas de primer nivel → **un flujo entero** → los tests → el historial. Por cada
módulo o flujo se completa un borrador en `borrador/absorcion/<fecha>/02-<modulo>.md` con estas
secciones, y **cada ítem** se marca con su origen (`archivo:línea`, test, commit) y su confianza:

| Sección del borrador | Qué va | Cómo se detecta | Destino en el Cerebro |
|---|---|---|---|
| **Entidades y estados** | Los sustantivos del negocio y sus ciclos de vida | Modelos, tablas, enums, transiciones en el código y en los tests | `funcional/<ficha>.md` (glosario y estados) |
| **Roles y permisos** | Quién puede hacer qué | Anotaciones de seguridad, chequeos de rol, pantallas por perfil | `funcional/<ficha>.md` |
| **Reglas candidatas** `⚠` | Validaciones, cálculos, condiciones, límites | Validaciones, ramas condicionales, aserciones de tests | `funcional/<ficha>.md` como `RN-<MOD>-nnn` **sólo si el humano la confirma** |
| **Flujos** | Los casos de uso de punta a punta | Endpoints, pantallas, jobs, colas | `funcional/<ficha>.md` con su bloque `## Derivación a backlog` propuesto `⚠` |
| **Integraciones** | Con qué sistemas habla y cómo | Clientes HTTP, colas, bases, archivos | `contexto.md` §Integraciones |
| **Decisiones implícitas** | Lo que el código decidió sin que nadie lo escribiera | Estructura, patrones, librerías, convenciones | `arquitectura/decisiones.md` como `DEC-nnn` `⚠` |
| **Mapa de lo que existe** | Módulos, qué expone cada uno, integraciones y ambientes reales | Inventario, contratos, pipeline, lectura de un flujo | `aplicacion/mapa.md` |
| **Deuda y riesgos** | Lo que está mal o frágil | TODO/FIXME, tests ausentes, duplicación, secretos en el repo | `aplicacion/deuda.md` (`DT-nnn`) y la tabla de [[planificar-modernizacion]] |
| **Dudas** | Lo que el código no contesta | Comportamientos sin test, ramas muertas, nombres ambiguos | `pendientes.md` |

Cada afirmación lleva su **marca de confianza**: **CONFIRMADO** (sale del código y se cita con
`archivo:línea`), **INFERIDO** (se deduce de un patrón y puede estar mal: entra sólo como `⚠`) o **HUECO**
(el código no lo contesta: `P-nnn`, nunca una suposición). Una regla candidata se presenta con su
evidencia —fragmento de 10 a 20 líneas, test que la cubre o «sin test», lo que no se sabe y una
pregunta— o no se presenta. Al cerrar la fase se entrega la **matriz de cobertura**
(`borrador/absorcion/<fecha>/04-cobertura.md`): cada módulo de la radiografía con su borrador, o marcado
**HUECO: no leído**. Un módulo que nadie leyó no es «sin reglas».

**Cada ítem detectado dispara su propia Consulta Interactiva de Decisión** (Guardar / Ignorar /
Editar y Guardar), con la paráfrasis fiel y el origen a la vista ([[cerebro-orquestador]]
§«Vigilancia Semántica»). Nada entra al Cerebro en bloque. Si son muchos, se agrupan **por módulo**
y se cierran por tandas, como en el modo lote: una tabla por módulo y un "sí" que escribe esa tabla.
Lo validado lo persiste `cerebro-curator` (frontmatter, wikilinks, `log.md`); las fuentes se
registran en `fuentes.md` como `[DOC-nn] Código de <app>, commit <sha>`.

**Sin PHI.** Si en el código, los fixtures o la base hay datos reales de personas, **no se copian al
borrador**: se describe la estructura con marcadores y se anota como riesgo.

## Lo que sigue (otras skills, no ésta)

Con el Cerebro poblado y la matriz de cobertura entregada, esta skill **termina**. Lo que viene tiene dueño:

| Qué | Skill | Qué produce |
|---|---|---|
| Comparar estrategias con la tabla medida, curar cada regla (migrar / descartar / decide el humano), escribir `DEC-004`, ordenar los slices | [[planificar-modernizacion]] | `DEC-004` confirmada, fichas por slice, la tabla de `aplicacion/modernizacion.md` |
| Ponerle la red a un slice: corpus desde la radiografía, golden grabado contra la vieja, tests de caracterización | [[caracterizar-comportamiento]] | `corpus.json`, `golden.json` firmado, commits `test(caracterizacion)` |
| Ejecutar un slice: contrato del código viejo, construcción, paridad, corte con barrera, apagado | [[modernizar-slice]] | el slice avanza en `modernizacion.md` con su evidencia |

Las filas medibles de la decisión ya las trae el inventario (bloque «Para DEC-004»); el método de cada Tarea es
[refactor-y-migracion.md](../../skills/desarrollo/references/metodo/refactor-y-migracion.md). **Sin `DEC-004` confirmada no se arma ningún plan.**

## Barreras

- **Sólo lectura sobre la aplicación existente**, siempre. Si hay que clonarla, afuera de este repositorio y en una carpeta que se pregunta.
- **Nada entra al Cerebro sin la Consulta Interactiva por ítem** (o la tabla por módulo con su "sí").
- **Una regla sacada del código es candidata `⚠` hasta que una persona la confirme.** El código puede estar mal.
- **Sin PHI**: datos reales encontrados en código, fixtures o bases se describen con marcadores y se reportan como riesgo.
- **Refactor o migración lo decide el humano** con la tabla a la vista (`DEC-004`). La skill no arranca el plan sin esa decisión.
- **Un inventario o una radiografía que no corrieron son `SIN DATOS`**, no una descripción de memoria.
- **Una regla candidata sin `archivo:línea` y sin fragmento no se presenta**: es una impresión.
- **La base y los logs se consultan sólo con un "sí"**, por esquema, conteos y agregados; nunca filas con datos de personas.
- Todo en español (Argentina).
