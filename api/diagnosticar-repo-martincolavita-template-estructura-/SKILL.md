---
name: diagnosticar-repo
description: >-
  Se invoca SOLO de forma explicita (/diagnosticar-repo); NO se carga por contexto y nada del
  ciclo de desarrollo la dispara. Corre el Doctor del proyecto (doctor/bin/doctor.sh o .ps1) y
  explica como leer su informe: guardarrailes, espejos de skills, conteos declarados contra la
  realidad, referencias y wikilinks rotos, estructura prometida contra la materializada,
  asimetria back/front, andamiaje obsoleto, costo de contexto por skill, deuda declarada y COMO
  VENIMOS respecto de la corrida anterior. Con codigo clonado en back/ o front/ mide ademas
  sobre el CODIGO: limites entre modulos y capas, contrato openapi contra los endpoints,
  trazabilidad del test a su Tarea, la costura back-front, duplicacion, dependencias sin usar,
  puertas de seguridad y calidad del build y practicas que el linter no mira. Puede acotarse
  con --repo. CONSUME TOKENS Y TIEMPO: antes de correr muestra que va a hacer y espera un si
  explicito. SOLO LECTURA: no modifica archivos ni el Cerebro; su informe no se versiona.
  Espanol (Argentina).
---

# Diagnosticar repo — la puerta del Doctor

Esta skill **no implementa el diagnostico**: lo corre. El motor vive en `doctor/` y es un
programa de verdad, con su README propio.

> **Por que la skill no lista los comandos de cada sonda.** La version anterior si lo hacia:
> era una skill con ocho bloques de comandos para que el agente los corriera a mano. Al pasar
> el Doctor a codigo, esa lista quedo como una **segunda fuente de verdad** que se desincronizo
> sola — la skill decia una cosa y el programa hacia otra. Ahora hay un solo lugar donde estan
> las sondas: `doctor/doctor.py`.

## Gate de ejecucion (dos turnos, obligatorio)

**Turno 1 — avisar y esperar.** No se corre de una. Primero se dice:

- **Que hace:** recorre los archivos del proyecto y produce un informe HTML.
- **Que NO hace:** no modifica nada, no escribe en el Cerebro, no toca el tablero.
- **Que cuesta:** recorre los archivos del proyecto y corre varios comandos de git. Es rapido en segundos,
  pero leer el informe y actuar sobre el **no lo es** — por eso conviene correrlo a conciencia
  y no por costumbre.
- **Cuanto tarda en leerse:** el informe trae todas las sondas del Doctor (las del proyecto y las del
  codigo; el numero lo imprime el informe). Si solo interesan dos, conviene `--solo`.
- **Que se enciende y que no:** las sondas de codigo solo corren si hay un repositorio
  clonado en `back/` o `front/`. Sin codigo, se saltean y una sola sonda explica por que.

Y **se termina el turno**. Sin un "si" explicito, no se corre.

**Turno 2 — correr y reportar.** Con el si, se ejecuta y se resume el resultado en criollo:
cuantas sondas dieron OK, cuales tienen hallazgo, y **donde quedo el informe**.

## Como se corre

```bash
bash doctor/bin/doctor.sh
```

```powershell
.\doctor\bin\doctor.ps1
```

| Variante | Para que |
|---|---|
| `--repo back` · `--repo front` | Acota a una carpeta — acepta **cualquiera**, no una lista fija. Tres sondas quedan afuera: **asimetria** y **gemelas** porque comparan back contra front, y **conteos** porque mide documentos de la raiz |
| `--comparar` | Ademas del informe, el **reporte de arreglos**: que mejoro, que empeoro y que quedo igual desde la corrida anterior. Es con lo que cierra `atender-hallazgos` |
| `--solo espejos,gemelas` | Corre solo esas sondas |
| `--json` | Resumen por consola, sin escribir archivo. Es el modo para **pasarle el estado a otro agente** como contexto |

El informe queda en `doctor/salida/informe.html` (o `informe-back.html` / `informe-front.html`),
mas una copia fechada en `doctor/salida/historico/`.

## Como se lee el resultado

Tres estados por sonda, y **ninguno es un puntaje**:

| Estado | Que quiere decir |
|---|---|
| **OK** | Se midio y no hay nada que corregir |
| **HALLAZGO** | Se midio y hay algo que arreglar o decidir |
| **SIN DATOS** | **No se pudo medir.** No es aprobado |

> **No hay puntaje unico, y es una decision tomada.** Nada de "82/100": un numero resume de mas,
> da falsa objetividad y esconde justo lo que hay que arreglar. El encabezado dice "N de M
> sondas con datos" y listo.
>
> **Un repositorio vacio no es un repositorio sano.** Por eso `back/` y `front/`, que hoy solo
> tienen su README, salen **grises** con la etiqueta "prometido: todavia sin codigo" en vez de
> verdes. Decir "cero problemas" sobre cero lineas de codigo es mentir con verde.

Cada sonda con hallazgo trae, en su panel del informe: **que significa**, **por que importa**,
los **pasos para arreglarlo**, y un **texto listo para copiar** y pegarle a un asistente, que ya
viene con los datos del hallazgo adentro.

## Alcance y barreras

- **SOLO LECTURA.** No modifica un solo archivo.
- **No toca el Cerebro Digital ni lo funcional.** Los **lee** —las skills viven ahi, y varias
  sondas los recorren— pero **jamas propone cambios sobre su contenido de negocio**. Lo que
  mide son propiedades mecanicas: que un enlace resuelva, que un conteo coincida, que dos
  copias de una skill no hayan divergido.
- **El informe no va al Cerebro.** Es un artefacto **derivado**: se regenera corriendo el
  comando, y por eso `doctor/salida/` esta en el `.gitignore`. El Cerebro guarda conocimiento
  validado por una persona; un informe automatico no es eso. Lo que si es conocimiento son las
  **decisiones** que salen de leerlo, y esas se escriben a mano donde corresponda.
- **No se dispara sola.** Ningun paso del ciclo de desarrollo la invoca. Se corre a mano, por
  hito o antes de un cambio grande — no en cada commit: para eso esta el hook, que es
  instantaneo y bloquea.

## Que NO mide

El cambio por subir (`auditar-codigo`, `/code-review`), el ciclo de TDD (`verificar-tdd`), la tarjeta
(`auditar-tarea`, `auditar-historia`): quien contesta cada pregunta esta en una sola tabla, «Quien contesta que», en
`cerebro-digital/configuracion-ia/orquestador-desarrollo.md` del nucleo. Tampoco mira estilo (formateador y linter)
ni politicas de seguridad (la puerta SAST del pipeline: el Doctor verifica que este puesta y que frene la entrega).

El Doctor mira **el proyecto en reposo**. Ninguna de las otras lo hace, y el no hace ninguna de
las de ellas.

## Detalle completo

`doctor/README.md` — que hace cada sonda, los dos numeros de tokens y por que son dos, el
autocontrol y que promete, el historico, y lo que todavia le falta.
