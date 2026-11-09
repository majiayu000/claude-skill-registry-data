---
name: auditar-codigo
description: >-
  (Repos de codigo · desarrollo) Correr los CHEQUEOS DE ENTREGA sobre un cambio antes del
  Merge Request: lo que es propio de este pipeline y ningun revisor generico puede saber —
  que el cambio respete el contrato de la Tarea, que no cruce los limites del modulo, que la
  lista "Tests a escribir PRIMERO" este cubierta, que el fragmento OpenAPI este consolidado
  y que NO haya PHI ni secretos en el diff. NO es un revisor de codigo generico: la
  calidad del codigo es del control 5-bis (code-review.md; /code-review en Claude Code). Usar
  cuando se pida "revisá el MR", "chequeos de entrega", "revisá el diff antes de subirlo",
  "/auditar-codigo". NO audita la evidencia del ciclo TDD (eso es verificar-tdd) ni la salud
  del repo en reposo (eso es diagnosticar-repo). NO escribe codigo de produccion.
  Espanol (Argentina).
---

# Auditar código — chequeos de entrega

> **Esta skill NO es un revisor de código genérico, y es a propósito.**
> Para la **calidad del código** —corrección, limpieza, reuso, convenciones— está la revisión por
> dimensiones de `code-review.md` (control 5-bis), hecha por otro agente en cualquier motor; en Claude
> Code `/code-review` es un atajo válido. Esa parte **no vive acá**.
>
> Lo que queda es lo que **un revisor genérico no puede hacer, por más profundo que sea**: no sabe
> cuál es tu Tarea, ni tu lista «Tests a escribir PRIMERO», ni tu fragmento OpenAPI, ni tus
> marcadores de PHI (dato personal o sensible real: en el código y los fixtures van `<persona>`,
> `<documento>`, `<identificador>`, `<telefono>`, `<direccion>`, `<dato-sensible>`, nunca el
> dato), ni dónde están los límites de tus módulos. Eso es de **este** pipeline.
>
> **Estos chequeos corren SIEMPRE, en las cuatro herramientas**, después de la revisión de código. Saltearlos deja **PHI y secretos sin ejecutor** justo en el
> paso previo al Merge Request, y nadie más lo cubre.

## La pregunta que contesta esta skill

**¿La entrega cumple lo que este pipeline exige?** Contrato de la Tarea, límites del módulo, tests cubiertos, sin PHI ni secretos.
La frontera con los otros controles está en **una sola tabla**: «Quién contesta qué», en
`cerebro-digital/configuracion-ia/orquestador-desarrollo.md` del núcleo. No se repite acá para que no diverja.

Un cambio puede tener **TDD impecable, estar bien escrito y no cumplir la entrega** —por
ejemplo, con un `<persona>` real filtrado en un fixture. Por eso son cuatro preguntas distintas.

## Un solo modo: sobre el diff

Corre **sobre lo que cambió**, antes del Merge Request. *(El modo `--repo` se eliminó: mirar
el repo en reposo es de `diagnosticar-repo`, y tenerlo acá duplicaba esa frontera.)*

## El diff: desde la base anotada, y sale de git

Lo que se audita es `git diff <sha-base>...HEAD` más `git diff HEAD` (lo no commiteado), con el
`<sha-base>` que el orquestador anotó al abrir el worktree y que viene en la misión. **La base no se
adivina** (ni `main`, ni `develop`, ni `@{upstream}`): si la misión no la trae, es `SIN DATOS`. El diff
sale de git, nunca del servidor de repositorios: no depende de `gh`, `glab` ni de la VPN.

## Primero el script, después el criterio

`bin/auditar-diff.py` del repositorio del Cerebro lee las líneas agregadas del diff (la misma cascada de
abajo, más lo no commiteado) y marca **secretos** (HALLAZGO) y **posibles datos personales** (aviso: se
leen uno por uno), la elegibilidad (diff vacío → `SIN DATOS`; sólo documentación → aviso) y si la rama
nombra la Tarea:

```bash
python <ruta del repositorio del Cerebro>/bin/auditar-diff.py --repo <worktree> --base <base> --id <ID>
```

Lo que el script marca no se discute; lo que avisa, se lee. Un script que no corrió es `SIN DATOS`.
El contrato, los límites de módulo y la cobertura de la lista siguen siendo de esta skill.

## Los 4 chequeos de entrega

1. **Elegibilidad**: diff vacío, solo documentación, o mismo sha ya revisado → **frena y dice por qué**.
2. **Tarea referenciada** y objetivo coincidente.
3. **Fragmento OpenAPI consolidado** → invoca `armar-swagger` (sólo si la Tarea toca la capa `api`; si no, `N/A`).
4. **PHI y secretos** en el diff (PHI = dato personal o sensible real: va el marcador, nunca el dato).

La cobertura de la lista «Tests a escribir PRIMERO» y la evidencia del rojo son del **control 5**
(`verificar-tdd`) y no se repiten acá; los comentarios del Merge Request los lee el orquestador, que sí
tiene las herramientas. Cada pregunta, un solo control.

## Los 2 chequeos de forma que tampoco puede hacer un revisor genérico

1. **Límites de arquitectura** — *hoy no lo verifica nadie más.*
   - **En back** (monolito modular, DEC-002): cada Tarea modifica **un solo módulo** (puede
     *usar* otro). Adentro del módulo: `api → application, domain` · `application → domain` ·
     `infra → application, domain` (implementa `application/gateway` y `application/repository`)
     · `domain →` nada · `exceptions/` la usan todas y sólo depende de `shared.exceptions`.
     Entre módulos se **llama** sólo a la `application` del otro y se pueden importar sus tipos
     de `domain` y `exceptions`; importar `<otro>.api` o `<otro>.infra` es hallazgo. `shared` no
     depende de ningún módulo. Persistir o modificar entidades de otro módulo sólo por sus casos
     de uso (esto lo mira la revisión: la fitness function de arquitectura no distingue lectura
     de escritura).
   - **En front:** import cruzado entre apps (una app que importa código de otra).
   - El día que haya build, esto se muda a una *fitness function* (la de arquitectura del stack,
     o una regla del linter que prohíba esos imports) que **falla el build** — mucho mejor que
     un informe.
2. **Código contra el contrato de la Tarea** — endpoint fuera del contrato OpenAPI, forma de
   respuesta distinta, código de error no declarado.

## Cómo dictamina

El mismo vocabulario que toda la cadena (`orquestador-desarrollo.md` §«Formato del veredicto»):

| Veredicto | Qué exige |
|---|---|
| **HALLAZGO** | Nombro la entrada o el estado que lo dispara **y** la salida incorrecta, **citando `archivo:línea`**; digo si frena |
| **AVISO** (no frena) | El mecanismo es real pero el disparador es incierto; **digo qué lo confirmaría** |
| **SIN DATOS** | No se pudo mirar (el script no corrió, la base no vino, el contrato no existe); se dice qué falta |

**Sesgo declarado: ante la duda es AVISO, no HALLAZGO** (no se afirma lo que no se puede citar). La verificación corre en un **turno separado** y **sin ver el razonamiento del buscador**;
si la herramienta no permite separar contexto, el informe dice textualmente
**"verificación en el mismo contexto — NO independiente"** y baja el peso del veredicto.

## Qué NO hace

- **No revisa calidad de código genérica.** Corrección fina, limpieza, reuso y convenciones son del
  control 5-bis (`code-review.md`).
- **No audita la evidencia TDD.** Eso es el control 5 (`verificar-tdd`) y no se repite acá: cada
  pregunta tiene un solo control.
- No audita el repo en reposo (eso es `diagnosticar-repo`), ni el Cerebro, ni la calidad
  funcional del requerimiento.
- **NO tiene piso de hallazgos.** No existe "reportá al menos N cosas": eso empuja a inventar y
  choca de frente con la regla de no inventar. **Un informe vacío es un resultado válido.**
- **No escribe código de producción.** Si se pide arreglar, **propone y espera el sí**.

## Salida

La línea del control 5-ter del bloque canónico `VEREDICTO-INICIO … VEREDICTO-FIN` ([[orquestador-desarrollo]]
§«Formato del veredicto»): `5-ter auditar-codigo: OK | HALLAZGO | SIN DATOS (<motivo>)`, con el resultado de
`auditar-diff.py` al lado, y debajo un hallazgo por línea: `archivo:línea — qué — por qué frena o no`.
**Pegable, no publica nada**: el Merge Request lo lee y lo comenta el orquestador, que sí tiene las herramientas.

## Lo que deliberadamente NO hace porque es de CI, no de LLM

Tamaño del diff, si se agregaron tests, lockfile actualizado, archivos generados commiteados.
Eso lo resuelven `.gitignore`, un detector de secretos y las reglas del pipeline. Separar esas
dos mitades evita construir un revisor caro que hace trabajo barato.

## Barreras

- No escribe código de producción ni arregla tests.
- No inventa: sin evidencia citable, no hay hallazgo.
- **No autoriza la entrega por sí sola.** Aporta evidencia; deciden el humano y la política del repo.
- Español (Argentina).
