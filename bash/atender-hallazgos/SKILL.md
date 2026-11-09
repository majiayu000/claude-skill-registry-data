---
name: atender-hallazgos
description: >-
  Tomar el informe del Doctor y recorrer sus hallazgos UNO POR UNO, en turnos separados,
  proponiendo el arreglo concreto y esperando la decision del humano en cada caso. NO arregla
  sola y NO arregla en lote: cada hallazgo tiene su turno, su propuesta a la vista y su
  respuesta. Tres salidas por hallazgo: arreglar, declararlo aceptado -dejando el motivo
  escrito en el archivo, no solo en el chat- o dejarlo para despues. Al terminar vuelve a
  correr el Doctor con --comparar y muestra el reporte de arreglos, porque un arreglo que no
  se verifico no esta hecho. Usar cuando se pida "atendamos los hallazgos", "vamos uno por uno
  con el informe", "arreglemos lo que encontro el Doctor", "/atender-hallazgos". Espanol
  (Argentina).
---

# Atender hallazgos

Toma el informe del Doctor y lo convierte en **una conversacion ordenada**, hallazgo por
hallazgo, hasta que no quede ninguno sin decision.

> **Por que existe.** El Doctor produce un informe, y el informe se lee y se olvida. Cada
> hallazgo trae su pedido listo para copiar, pero eso depende de que alguien se acuerde de
> copiar todos — y bajo la inercia de trabajar, se copia uno y el resto queda. Esta skill es
> la que garantiza que **ninguno se saltea en silencio**: los recorre todos, y cada uno sale
> con una decision tomada, aunque la decision sea "esto queda para despues".
>
> **Por que NO es un comando que arregla solo.** Se evaluo y se descarto. De las
> sondas del Doctor, solo dos o tres tienen arreglo mecanico; el resto necesita criterio —¿a donde se movio ese
> archivo?, ¿esta skill mezcla dos trabajos o hace uno bien?— y un script no lo tiene. Y para
> las dos o tres mecanicas, un comando no aporta nada que esta conversacion no de ya, con la
> ventaja de que aca se ve lo que se va a tocar antes de tocarlo.

## Regla de oro

**Un hallazgo por turno. Se muestra, se pregunta, se espera.** No se juntan dos en la misma
respuesta ni "para avanzar mas rapido", porque ahi es donde se cuela el que nadie miro.

## Insumos

1. **El informe mas reciente.** El `ultimo.json` del histórico del Doctor (en `doctor/salida/historico`) (o
   `ultimo-back.json` / `ultimo-front.json` segun el alcance) sirve para el PLAN DE TRABAJO:
   trae el veredicto, el resumen y CUANTAS filas tiene cada sonda, y es barato de leer.

   **Pero NO trae las filas**, y este flujo exige mostrar CUALES son los casos, no cuantos.
   Asi que el detalle de cada hallazgo se lee del informe HTML -`doctor/salida/informe.html`-
   o corriendo esa sonda sola con `--solo <nombre>`. Mandar a leer una fuente que no tiene
   el dato que la skill obliga a mostrar es como se termina inventando el detalle.
2. Si no existe, o si el repositorio cambio desde la ultima corrida, **primero se corre el
   Doctor** — no se atiende un informe viejo.

```bash
bash doctor/bin/doctor.sh
```

## Flujo

### 1. Mostrar el plan de trabajo

Se listan los hallazgos **con su cantidad** y se propone un orden, de mas barato a mas caro
—los mecanicos primero, para despejar—. Se muestra y **se termina el turno**: el humano puede
reordenar, sacar alguno o decir por donde arrancar.

```
Encontre 3 hallazgos. Propongo este orden:
  1. Wikilinks que no resuelven — 6 casos, mecanico
  2. Costo de contexto por skill — 3 skills grandes, necesita criterio
  3. Deuda declarada — 223 marcas, es una revision larga
¿Arrancamos por el 1, o preferis otro orden?
```

### 2. Por cada hallazgo, en su propio turno

Siempre las mismas cuatro partes, en este orden:

1. **Que encontro**, en criollo, con los datos concretos. No "hay 6 wikilinks rotos": **cuales**.
2. **Que averigüé.** Antes de proponer, se mira: ¿ese archivo existe con otro nombre?, ¿esa
   skill mezcla dos cosas? La propuesta sale de haber mirado, no de la plantilla del pedido.
3. **Que propongo**, concreto y por caso. Si son seis enlaces, van los seis con su propuesta —
   no una regla general que el humano tenga que aplicar mentalmente.
4. **Las tres salidas**, explicitas:

| Salida | Que pasa |
|---|---|
| **Arreglar** | Se aplica lo propuesto, se muestra el cambio y se commitea |
| **Aceptarlo** | Es una decision, no un error. Se **escribe el motivo EN EL ARCHIVO** para que la proxima corrida no lo vuelva a marcar y, si es deuda de codigo, una fila `DT-nnn` en `<modulo>/aplicacion/deuda.md` con cuando se paga |
| **Dejarlo** | Queda abierto. Se dice por que y de quien depende |

Y **se termina el turno**. No se avanza al siguiente hallazgo sin la respuesta.

> **"Aceptarlo" no es "ignorarlo".** Si la decision se queda en el chat, la proxima corrida lo
> marca de nuevo y alguien lo vuelve a analizar desde cero. Aceptar **obliga a dejar rastro**:
> la seccion declarada en el `SKILL.md`, la entrada en el diccionario de excepciones, la nota
> al pie. Una diferencia declarada es una decision; una sin declarar es un descuido, y desde
> afuera se ven iguales.

### 3. Cerrar con la verificacion

Cuando no queda ningun hallazgo sin decision, se corre:

```bash
bash doctor/bin/doctor.sh --comparar
```

Y se muestra el **reporte de arreglos**: que mejoro, que empeoro, que quedo igual. Recien ahi
se da por cerrada la vuelta.

> **Un arreglo que no se verifico no esta hecho.** Es el mismo principio que rige en las
> tarjetas con la evidencia del ciclo, y no hay razon para relajarlo aca: lo que se cree
> arreglado y no se midio, muchas veces no lo estaba.

## Lo que esta skill NO hace

- **No arregla nada sin mostrarlo primero.** Ni siquiera lo mecanico.
- **No agrupa hallazgos** "porque son parecidos". Cada uno tiene su decision.
- **No decide por el humano** cuando la respuesta depende de conocimiento que no tiene: si el
  arreglo necesita saber algo del negocio, de infraestructura o del equipo funcional, se dice
  **de quien depende** y se pasa al siguiente.
- **No inventa el arreglo.** Si no encontro a donde se movio un archivo, lo dice: "no lo
  encontre, estas son las dos opciones que veo".
- **No toca el Cerebro Digital como contenido de negocio.** Puede corregir un enlace roto o un
  conteo; jamas propone cambios sobre una regla o una ficha — eso es del equipo funcional.

## Barreras

- Cada arreglo se commitea con **el motivo escrito**, no con "fix". El mensaje tiene que
  contestar por que estaba mal, no solo que se cambio.
- **Nunca se borra informacion para poner una sonda en verde.** Un enlace roto se "arregla"
  borrandolo y el informe queda lindo, pero se perdio el dato de que algo falta. Si la salida
  honesta es borrar, se dice **por que** el destino ya no aplica.
- Si durante el recorrido aparece un hallazgo **que no estaba en el informe**, se anota y se
  reporta al final: puede ser una sonda que falta, y eso vale mas que el arreglo puntual.

## Donde entra en el flujo

```
doctor/bin/doctor.sh          ->  informe con N hallazgos
        |
        v
atender-hallazgos             ->  uno por uno, con decision humana en cada uno
        |
        v
doctor/bin/doctor.sh --comparar  ->  reporte de arreglos: que cambio de verdad
```

Detalle de que mide cada sonda y como leer el informe: `doctor/README.md`.
