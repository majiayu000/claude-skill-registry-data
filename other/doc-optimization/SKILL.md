---
name: doc-optimization
version: 1.0.0
description: Protocolo medir, mover y verificar para trasladar contenido de un fichero siempre-cargado (CLAUDE.md, AGENTS.md y sus @imports) a una referencia, con guard de no-degradacion de sus consumidores. Usar cuando el cierre transitivo de lo siempre-cargado supera el presupuesto (~5 % de la ventana efectiva). No usar para anadir contenido nuevo, recortar prompts por longitud, acelerar la suite (ver suite-optimization) ni optimizar la memoria (ver memory_optimization).
triggers: [/doc-optimization, doc-optimization, optimizar-documentacion]
author: agent
role: manager
stage: implement
writes_memory: false
quality_gate: false
tags: [core, system, documentation, context, codeonly]
source_prompt: prompts/doc_optimization.md
contract_id: cid-doc-optimization-v1
---

# doc-optimization

Skill para optimizar la documentacion **siempre-cargada** de una raiz basandose en
evidencia medida, no en la apariencia de longitud. Es el hermano de
`suite-optimization`: aquel optimiza SEGUNDOS de suite, este optimiza TOKENS de
contexto. Mismo metodo, otra superficie.

NO reimplementa el metodo: el flujo completo (declarar raiz, medir el cierre
transitivo, clasificar por via de carga y por funcion, las CINCO condiciones, las
trampas verificadas, el guard de no-degradacion) vive en
`prompts/doc_optimization.md`. **El prompt es la fuente de verdad; si algo
diverge, prevalece el prompt.**

## Cuando usarla

- El cierre transitivo de lo `siempre-cargado` de una raiz supera el 5 % de la
  ventana efectiva, y se quiere reducir SIN perder contrato normativo.
- Antes de anadir contenido nuevo a un fichero que ya entra en cada sesion.

## Cuando NO usarla

- Para recortar un `router-condicional` por longitud: su tamano ES su funcion.
- Para editar a mano un fichero `generado`: su tope vive en el script generador.
- Para "acortar porque es largo" sin medir el % sobre la ventana. La apariencia
  de longitud no es evidencia.
- Si no puedes EJECUTAR los consumidores del fichero: sin before/after de su
  salida real no se mueve nada.

## El invariante (unico criterio portable)

> El cierre transitivo de `siempre-cargado` cabe en **<5 % de la ventana efectiva**.

Relativo a proposito: dos raices del mismo sistema no comparten techo de LINEAS
pero si ese porcentaje. Un umbral absoluto de lineas NO es portable y el prompt
lo prohibe como criterio.

## Las CINCO condiciones (detalle en el prompt)

Un bloque solo se mueve si cumple TODAS:

1. **(a) Concentrado** -- seccion contigua de funcion unica.
2. **(b) Destino alcanzable** -- y el destino debe ser `referencia-bajo-demanda` o
   `router-condicional`; mover a `citado-obligatorio` es cambiar de bolsillo.
3. **(c) No es refutacion** -- ni entera ni repartida entre secciones.
4. **(d) Ningun consumidor programatico consume ESE bloque** -- un parser no sigue
   enlaces.
5. **(e) No esta dentro de una seccion que un consumidor extraiga por ENCABEZADO.**

## Trampas verificadas (no re-descubrir)

- **La medicion miente sin raiz declarada:** el mismo `CLAUDE.md` mide 35 lineas
  en el motor, 43 en un destino y 84 en otro. Son tres ficheros distintos con el
  mismo nombre.
- **Contar el fichero suelto miente con `@import`:** `CLAUDE.md` = 35 lineas
  parece holgado, pero arrastra `@AGENTS.md` = 664. El siempre-cargado real es
  699 (7,70 % de 200K, 1,54x su presupuesto).
- **"0 lineas perdidas" es un CONTEO, no un guard:** sustituir el cuerpo de una
  seccion registrada por un puntero dejo la salida del consumidor en 73 chars de
  1553 -- 95 % de perdida -- SIN excepcion y con los tests verdes.

## Guard obligatorio al aplicar

Before/after del fichero **y de la SALIDA de cada consumidor censado**. Si la
seccion extraida encoge, el traslado esta estripando contexto aunque el origen
conserve un puntero. **Si no puedes ejecutar el consumidor, no puedes mover el
bloque.**

## Estados terminales validos

`APLICADO` / `SIN CANDIDATO MOVIBLE` / `NO APLICA` (ya cumple presupuesto) /
`BLOQUEADO` (consumidor no ejecutable o falta la ventana efectiva).

Concluir "aqui no hay nada que recortar" es un RESULTADO, no una corrida fallida.

## Prompt canonico

Leer y aplicar `prompts/doc_optimization.md`. Hereda filosofia CEM de
`prompts/audit_agent_output.md` y la forma de `prompts/suite_optimization.md`.
Expediente de evidencia (mediciones y bucles): `PROPUESTA_doc_optimization.md`
en el `planning/` del destino -- no hace falta para ejecutar.

## Restriccion dura

- SOLO UN fichero por corrida (no un sweep).
- **SUELO:** alcanzado el presupuesto, el protocolo no se aplica mas a ese
  fichero. El objetivo es el invariante, no el minimo.
- Ante duda entre "movible" y "adyacente al error": es adyacente -> NO mover.
- La skill es puntero: no redeclara el metodo. Remite al prompt.
