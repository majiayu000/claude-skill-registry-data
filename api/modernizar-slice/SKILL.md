---
name: modernizar-slice
description: >-
  Ejecutar UN slice de la modernización decidida en DEC-004, de punta a punta y con barreras: el
  contrato sacado del código viejo, la construcción por el pipeline normal (Tareas con TDD en el
  repositorio nuevo, o refactor en el lugar sobre la red de caracterización), la paridad contra el
  golden con bin/paridad.py, la clasificación de cada diferencia (bug del port, cambio intencional
  aceptado por una persona, campo volátil), el corte de tráfico sólo con bin/mapa-modernizacion.py
  corte en OK, y el apagado de la vieja con un «sí». Referencias aparte para refactor en el lugar,
  eliminar código muerto y subir de versión. Usar cuando se pida "migrá el slice X", "seguí con
  la migración", "refactorizá el módulo X", "cortá el tráfico de X", "/modernizar-slice". La app
  vieja no se toca; nadie se aprueba a sí mismo; sin paridad no hay corte. Español (Argentina).
---

# Modernizar un slice

Es el ciclo que se repite por cada fila de `aplicacion/modernizacion.md` hasta que la aplicación vieja se
apaga. Lo que hace cada Tarea de código (rojo-verde, evidencia, revisión, Merge Request) sigue siendo el
método de siempre; acá va **la secuencia del slice y sus barreras**. El avance se lee con:

```bash
python bin/mapa-modernizacion.py ver cerebro-digital/<modulo>/aplicacion/modernizacion.md
```

## Lo que NO hace

- **No toca la aplicación vieja**, ni para "ayudar" al corte: el desvío de tráfico es una Tarea aparte, con su "sí".
- **No escribe el golden ni el resultado de paridad.** Los produce `bin/paridad.py`; esta skill los lee.
- **No acepta diferencias.** Una diferencia la acepta una persona, con su nombre en `aceptadas.json`.
- **No corta tráfico ni apaga nada.** Muestra la barrera en OK y lo hace una persona.
- **No empieza un slice con `DEC-004` sin confirmar** ni con el anterior a medias si dependen.

## La secuencia (estados de la tabla)

```
pendiente -> contrato -> red -> construido -> paridad -> cortado -> apagado
```

### 1. Contrato (`pendiente` → `contrato`)
El `openapi.yaml` del slice **se saca del código viejo**: endpoints, formas de respuesta y códigos de error
reales (la radiografía los lista con `archivo:línea`; `armar-swagger` lo consolida). Lo que se quiera
cambiar se cambia **después** de la paridad, como Historia nueva. Si no es una API, el contrato son los
flujos observables: entradas, salidas, pantallas. Refactor en el lugar: el "contrato" son los límites del
módulo escritos ([refactor-en-el-lugar.md](references/refactor-en-el-lugar.md)).

### 2. Red (`contrato` → `red`)
[[caracterizar-comportamiento]]: corpus completo, golden grabado y verificado. **Sin red no se construye.**

### 3. Construcción (`red` → `construido`)
Las Tareas del slice salen de su ficha por el pipeline normal y las ejecuta [[desarrollar-asignadas]] con
TDD. En migración, en el repositorio nuevo con `DEC-002` y `DEC-003`; en refactor, en el mismo repositorio,
módulo por módulo y de adentro hacia afuera, con `--modo caracterizacion` en `verificar-tdd.py`. Una Tarea
que toca dos módulos, o la vieja y la nueva a la vez, se parte.

### 4. Paridad (`construido` → `paridad`)
```bash
python bin/paridad.py comparar --corpus <corpus.json> --golden <golden.json> --nuevo http://127.0.0.1:<puerto-nueva> \
       --volatil /0/fecha --volatil /0/id --aceptadas <aceptadas.json> --json > borrador/paridad/<slice>/<fecha>.json
python bin/paridad.py comparar ... --informe borrador/paridad/<slice>/<fecha>.md
```
Cada diferencia se clasifica **con una persona**, una por una:

| Clase | Qué es | Qué se hace |
|---|---|---|
| **Bug del port** | La nueva contesta distinto y no debía | Tarea de arreglo con rojo normal; se vuelve a comparar |
| **Cambio intencional** | Se decidió no reproducir eso (curaduría: DESCARTAR) | Entra en `aceptadas.json` con `aprobado_por` = la persona, fecha y motivo |
| **Campo volátil** | Fecha, id generado, orden sin garantía | `--volatil <camino completo>` (`/items/0/id`, nunca el nombre suelto: taparía ese campo en todas partes); queda registrado en el resultado y se anota en la ficha del slice |

El verificador de cada Tarea del slice corre la paridad como control propio (la misión la incluye cuando
la Tarea pertenece a un slice en modernización) y la reporta en el renglón `5-quinquies paridad` del bloque
`VEREDICTO`. El resultado de `comparar --json` va **firmado** por el script: es lo que después lee la barrera del
corte. Si la paridad destapa un comportamiento que nadie había curado, es una regla candidata nueva: el slice
**vuelve a `contrato`** hasta que la persona decida (migrar, descartar), y recién entonces sigue. `OK` sólo con cero
diferencias sin aceptar; una aceptada sin nombre de persona sigue siendo `HALLAZGO`.

### 5. Corte (`paridad` → `cortado`)
```bash
python bin/mapa-modernizacion.py corte cerebro-digital/<modulo>/aplicacion/modernizacion.md --slice <slice> --paridad borrador/paridad/<slice>/<fecha>.json
```
Da `OK` sólo si: `DEC-004` confirmada, el slice está en `paridad`, el resultado **lo escribió `paridad.py`** (firma),
es `OK`, reciente, del golden que cita la tabla (se abre y se verifica su firma), sin aceptadas sin aprobar, y la
columna **«Corte aprobado por»** tiene el nombre de una persona (un agente no vale). En un **refactor en el lugar**
no hay tráfico: el corte se prueba con `--veredicto <bloque VEREDICTO del verificador>` (`5 verificar-tdd : OK` en
modo caracterización y cero bloqueantes) y «cortado» significa que el módulo cumple las convenciones. Con `OK` a la vista, **la persona** cambia el enrutado (el proxy, la bandera,
el DNS: lo que el proyecto use) y la tabla pasa a `cortado`. Si hace falta corrida en paralelo antes, la
vieja y la nueva reciben lo mismo un tiempo y se compara con el mismo `paridad.py comparar`.

### 6. Apagado (`cortado` → `apagado`)
Cuando **ningún** flujo usa la vieja (se verifica en el enrutado y en los registros, no se supone), se la
apaga con **dos "sí" en turnos distintos** (es un borrado: mismo nivel que el GATE de BORRADO) y se escribe en
`aplicacion/mapa.md` qué quedó. Los datos siguen
[migracion-de-base.md](../../skills/desarrollo/references/metodo/migracion-de-base.md): contraer recién acá.

## Variantes (referencias)

- [refactor-en-el-lugar.md](references/refactor-en-el-lugar.md): red → límites → forma → reglas, un módulo por vez.
- [codigo-muerto.md](references/codigo-muerto.md): sacar lo que nadie usa, con evidencia convergente y en tandas reversibles.
- [subir-de-version.md](references/subir-de-version.md): framework o lenguaje, en cambios chicos con salida vieja contra nueva.

## Barreras

- **Nadie se aprueba a sí mismo**: el agente que construyó sólo **lista** las diferencias; las acepta una **persona** con su nombre. En modo solo (`DEC-006`) esa persona sos vos, aunque hayas despachado y verificado con agentes; un `aprobado_por` con nombre de agente no vale (`paridad.py` lo rechaza).
- **La evidencia no se fabrica**: golden y resultados de paridad los escribe el script y los firma; un archivo editado vale `SIN DATOS`.
- **Sin paridad OK y reciente, no hay corte.** Sin corte verificado, no hay apagado.
- **La aplicación vieja no se edita nunca** desde este flujo; si hay que tocarla, es una Tarea con su propio "sí" y su propia red.
- **Un slice a la vez por persona**; dos slices en paralelo sólo si no comparten datos ni contrato.
- Todo en español (Argentina). Sin PHI.

## Cómo entra en el veredicto

| Estado | Cuándo |
|---|---|
| **OK** | El slice avanzó un estado con su evidencia: contrato del código viejo, golden que verifica, paridad `OK`, corte con la barrera en `OK` |
| **HALLAZGO** | Una diferencia sin clasificar o aceptada sin persona, un corte sin barrera, la vieja tocada, una Tarea que mezcla dos módulos |
| **SIN DATOS** | La paridad no corrió, el golden no verifica o `DEC-004` no está confirmada |
