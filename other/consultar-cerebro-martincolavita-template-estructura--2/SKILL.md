---
name: consultar-cerebro
description: >-
  (Repos de front · desarrollo) Traer, SOLO si se pide explícitamente, UNA ficha del
  Cerebro Digital (repo de conocimiento) para tener contexto de negocio mientras se
  desarrolla, resolviendo el puntero "Documento fuente" / [RN-…] que la Tarea del tablero
  ya trae. Read-only y quirúrgico: una ficha por vez, NO el cerebro entero. Por default
  el desarrollo NO consulta el Cerebro (la Tarea es autosuficiente: contrato + tests).
  Usar cuando se pida "traé el contexto del Cerebro de esta Tarea", "mostrame la regla
  [RN-…]", "/consultar-cerebro". NO escribe en el Cerebro. Español (Argentina).
---

# Consultar cerebro (desde el código)

Puente **read-only y bajo pedido** entre el repo de código y el Cerebro Digital. Por
default, desarrollar una Tarea NO necesita el Cerebro: el contrato + los tests de la
Tarea ya encodean el comportamiento. Esta skill se usa solo cuando explícitamente hace
falta el "por qué" de negocio.

## Regla de oro
- **Solo si se pide.** No se consulta el Cerebro en cada Tarea; solo cuando el humano
  lo pide o una `[RN-…]` necesita entenderse.
- **Una ficha por vez.** Se resuelve el puntero exacto que trae la Tarea (`Documento
  fuente` / `[RN-…]`); NO se trae el cerebro entero (economía de tokens).
- **Read-only.** Nunca se escribe ni se edita el Cerebro desde el código.
- **Referencia, no copia.** Se lee para entender; no se pega la ficha dentro del código.
- **Español (Argentina).**

## Flujo
1. Tomar el puntero de la Tarea (`Documento fuente: <ruta/URL>` o `[RN-…]`).
2. Resolver **esa** ficha en el repositorio del Cerebro (por la ruta absoluta que trae la misión), read-only.
3. Devolver solo lo pedido (la regla, el fragmento); no la ficha entera si no hace falta.
4. Seguir el desarrollo. No deja rastro de escritura en el Cerebro.

## Barreras
- Nunca clona ni indexa el Cerebro completo.
- Nunca escribe en el repo de conocimiento.
- Si el puntero no resuelve (ficha movida o inexistente), se avisa y se pregunta.
