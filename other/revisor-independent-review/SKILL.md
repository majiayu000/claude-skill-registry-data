---
name: revisor-independent-review
version: 1.0.0
description: "Revision adversarial independiente del trabajo del Builder. Usar para la Capa 1.5 (Persona-2): el Revisor revisa con su propio modelo, nunca el mismo que el Builder. Triggers: /revisor-review, /verify."
triggers: [/revisor-review, /verify]
source_prompt: prompts/revisor_independent_review.md
contract_id: cid-revisor-review-v1
tags: [core, system]
author: agent
role: revisor
stage: review
writes_memory: false
quality_gate: false
disable-model-invocation: true
---

# revisor-independent-review

## Cuándo usar

Cuando se necesita una revision adversarial independiente de la implementacion del Builder.
Usar para la Capa 1.5 (Persona-2) del sistema de 4 capas: el Revisor revisa el trabajo
del Builder con su propio backend/modelo, nunca el mismo que el Builder.

## Cuándo no usar

- Para implementacion de codigo (ese es el Builder).
- Para revision de gobierno/ensemble con propuesta de cambios estructurales (proposer/challenger).
- Para validacion automatica de tests (eso corre la suite canonica, no el Revisor).

## Fuente normativa

Las instrucciones completas del Revisor (identidad, veredicto, alcance, remisiones,
anclaje) viven una vez en el prompt canonico: `prompts/revisor_independent_review.md`.
El prompt es source_of_truth. Esta skill solo apunta.
