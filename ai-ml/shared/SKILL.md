---
name: _shared
description: >
  Referencias compartidas internas para skills SDD. No es una skill invocable.
license: MIT
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Purpose

This directory stores shared reference documents consumed by real SDD skills
(for example: `sdd-phase-common.md`, `persistence-contract.md`).

## Not Invokable

`_shared` is a support package only. Do not invoke it as a skill.

## Model Mapping

El archivo [`models.json`](../models.json) en la raíz del proyecto contiene el catálogo completo de:

- **ML Models**: qué modelos aplicar según skill y tipo de tarea (clasificación, regresión, forecasting, etc.)
- **LLM Models**: qué modelo de lenguaje se recomienda para cada agente y sub-agente del ecosistema

Los skills pueden referenciar este archivo para recomendar modelos específicos según el contexto.
