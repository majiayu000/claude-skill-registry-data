---
name: lend-ai-docs
description: >
  Documentación senior — multi-archivo, Google-style docstrings, ADR.
  GATE OBLIGATORIO post-task: revisar si hay que actualizar docs del proyecto.
  Trigger: Siempre después de cada task (revisar si docs cambiaron),
  o al escribir documentación/generar docstrings/estructurar docs.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
---

# Skill: lend-ai-docs

Documentación senior. Código sin docs es deuda técnica.

## Trigger (SIEMPRE post-task)

- **Terminaste de trabajar → revisá si hay docs que actualizar**
- Creaste o modificaste una función pública → docstring
- Cambiaste estructura, agregaste features, modificaste AGENTS.md
- Tomaste una decisión de arquitectura → ADR
- El proyecto no tiene documentación → arrancala

## Post-Task Docs Review (GATE OBLIGATORIO)

Después de CADA task, antes de commit, revisá:

```
1. ¿Cambió la estructura del proyecto?
   ├── Nuevo agente/skill → AGENTS.md
   ├── Nueva feature pública → README
   └── Cambio arquitectónico → ARCHITECTURE.md

2. ¿Cambió la funcionalidad?
   ├── Nueva API/ruta → README o docs de la API
   ├── Nueva funcionalidad visible → CHANGELOG
   └── Nuevo flag de configuración → README

3. ¿Decisión técnica con tradeoffs?
   └── ADR en docs/adr/ (fecha, contexto, opciones, decisión)

4. Si no hay nada que actualizar → seguí tranqui
```

## Workflow LEND

1. ANALIZAR
   ├── Tipo: docstring (API pública), README (proyecto), ADR (decisión), guía (cómo usar)
   ├── Audiencia: ¿desarrollador, usuario, operador?
   ├── Estado: ¿docs desde cero o actualizar existentes?
   └── Lenguaje: inglés técnico US para código y commits

2. REVISAR (post-task automático, sin menú)
   ├── ¿Hay cambios que afectan docs? (ver checklist arriba)
   ├── Si NO → seguí
   └── Si SÍ → determinar qué docs tocar

3. HACER
   ├── Google-style: Args, Returns, Raises, Examples (cuando aplica)
   ├── README: qué hace, cómo instalar, cómo usar, configuración
   ├── ARCHITECTURE: estructura, agentes, skills, decisiones técnicas
   ├── ADR: título, contexto, opciones, decisión, consecuencias
   └── Inglés técnico US, claro y directo

4. VERIFICAR
   ├── La documentación es útil sin leer el código
   ├── Los ejemplos funcionan (ejecutables)
   └── No hay información desactualizada

## Cognitive Load Patterns (diseñar docs que reduzcan carga mental)

| Patrón | Regla |
|--------|-------|
| **Lead with answer** | Empezá con el outcome, no con el viaje. El lector necesita saber YA qué resuelve esto. |
| **Progressive disclosure** | Mostrá lo esencial primero. Detalles y edge cases después, colapsados o linkeados. |
| **Chunking** | Agrupá en secciones de 3-5 ítems. Nadie procesa una pared de texto. |
| **Signposting** | Cada sección anticipa qué vas a encontrar. "Esto cubre: instalación, configuración, primeros pasos." |
| **Recognition over recall** | No hagas que el lector recuerde info de 3 secciones atrás. Repetí o linkeá. |
| **Review empathy** | Diseñá para el que revisa tu PR: qué leer primero, qué está out of scope, cómo llegaste acá. |

## Default doc shape

```
# Outcome Title (lo que se logra, no lo que se hace)

## Quick path (2-3 pasos para el 80% de los casos)

## Details table (para el 20% que necesita más)

| Qué | Cómo | Cuándo |
|-----|------|--------|
| ... | ...  | ...    |

## Checklist (accionable, con checkboxes)

- [ ] Step 1
- [ ] Step 2

## Next step (una sola acción clara)
```

## PR review doc guidelines

- **What to review first**: los archivos de alto impacto, con justificación
- **What's out of scope**: lo que NO está en este PR (no hagas adivinar al reviewer)
- **Chain context**: si esto es parte de una cadena de PRs, linkealos
- **Test plan**: qué se testeó manualmente y qué automáticamente
