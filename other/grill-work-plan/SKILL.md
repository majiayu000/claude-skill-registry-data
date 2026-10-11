---
name: grill-work-plan
version: 1.0.0
description: Interroga una peticion ambigua, una pregunta a la vez y con respuesta recomendada, para fijar la terminologia antes de crear el work_plan. Usar cuando el requisito del usuario tiene terminos difusos que cambiarian el plan. No usar para un requisito que ya es preciso (ver manager-create-work-plan).
triggers: [/grill-plan, /grill, grill-wp]
author: agent
role: manager
stage: plan
cycle_phase: [F2-contrato]
writes_memory: false
quality_gate: false
tags: [core, system]
---

# grill-work-plan

Skill de interrogacion pre-plan para resolver terminologia ambigua antes de crear un work plan.

## Overview

Esta skill actua como un filtro de claridad antes de la planificacion. Su objetivo es:
1. Identificar terminos ambiguos o fuzzy en el requerimiento del usuario
2. Resolver cada termino con una pregunta a la vez
3. Proporcionar una respuesta recomendada antes de esperar la respuesta del usuario
4. Preferir respuestas derivadas del codebase cuando sea posible
5. Mantener el contexto de dominio compacto usando `PROJECT.md` y `MEMORY.md` por defecto
6. `CONTEXT.md` es opcional y solo se crea cuando aporta valor como glosario separado

## Workflow

### Paso 0: Verificar contexto disponible

Antes de comenzar el interrogatorio, leer el contexto base:

```bash
# Leer contexto base (siempre)
cat PROJECT.md
cat .agent/runtime/memory/MEMORY.md
cat .agent/runtime/memory/observations.jsonl | tail -50

# Leer contexto opcional (si existe)
if test -f CONTEXT.md; then cat CONTEXT.md; fi
```

**Regla:** `PROJECT.md` y `MEMORY.md` son los inputs de contexto por defecto. `CONTEXT.md` vive en la raiz del repositorio y es opcional.

### Paso 1: Identificar terminos ambiguos

Analizar el requerimiento del usuario buscando:
- Terminos tecnicos sin definir
- Acronimos no explicados
- Conceptos de dominio ambiguos
- Alcances fuzzy ("mejorar", "optimizar", "arreglar")
- Dependencias implícitas no declaradas

**Prioridad de preguntas:**
1. Primero: preguntas que el codebase puede responder directamente (buscando en codigo existente)
2. Despues: preguntas de dominio que requieren clarificacion humana
3. Ultimo: preguntas de preferencia de implementacion

### Paso 2: Interrogatorio uno-a-uno

**Regla de oro:** Una pregunta a la vez. No bloquear al usuario con multiples preguntas.

Para cada termino ambiguo:

```markdown
## Pregunta N: [Termino/Concepto]

**Ambiguedad detectada:** [Por que es ambiguo este termino]

**Respuesta recomendada:** [Tu recomendacion basada en PROJECT.md, MEMORY.md o el codebase]

**Justificacion:** [Por que esta recomendacion tiene sentido en este contexto]

**¿Es correcto? (y/n o corrige):**
```

Esperar confirmacion o correccion del usuario antes de continuar.

### Paso 3: Buscar respuestas en el codebase

Cuando un termino pueda resolverse con codigo existente:

```bash
# Buscar definiciones, clases, funciones relacionadas
grep -r "termino" --include="*.py" src/
find . -name "*.py" -exec grep -l "concepto" {} \;

# Buscar en skills existentes
ls skills/
cat skills/*/SKILL.md | grep -i "termino"
```

Si el codebase ya define el termino, usar esa definicion como respuesta recomendada.

### Paso 4: Gestionar CONTEXT.md (opcional)

**Regla:** Solo proponer entrada en `CONTEXT.md` cuando:
- El termino NO esta ya definido en `PROJECT.md` o `MEMORY.md`
- El termino es especifico del dominio del proyecto (no conocimiento general)
- Vale la pena conservar la definicion para futuros WPs

**Formato de propuesta:**

```markdown
**¿Quieres que añada este termino a CONTEXT.md?**

Propuesta de entrada:
```markdown
### [Termino]

[Definicion clara y concisa]

**Ejemplo:** [Ejemplo concreto si aplica]
**Relacionado con:** [Otros terminos del glosario]
```

(y/n):
```

Si el usuario acepta y `CONTEXT.md` no existe, crearlo en la raiz del repositorio.

### Paso 5: Criterios para ADR (Architecture Decision Record)

Un ADR esta justificado cuando se cumple AL MENOS UNA de estas condiciones (mattpocock):

1. **Hard to revert:** La decision es dificil o costosa de revertir una vez implementada
2. **Surprising without context:** La decision seria sorprendente o confusa sin documentacion del por-que
3. **Real trade-off:** Hay compensaciones reales entre opciones (no hay una opcion claramente superior)

**Ejemplos que justifican ADR:**
- Elegir una base de datos (SQLite vs PostgreSQL)
- Cambiar un patron arquitectonico (MVC vs CQRS)
- Adoptar una libreria critica con lock-in

**Ejemplos que NO justifican ADR:**
- Nombramiento de variables
- Elecciones de estilo de codigo (ya cubiertas por ruff)
- Decisiones reversibles en minutos

### Paso 6: Handshake de completado

Cuando todos los terminos esten resueltos, emitir EXACTAMENTE:

```
> ✅ Grill completo. Términos resueltos: N. Puedes crear el WP con /plan.
```

Donde `N` es el numero total de terminos resueltos.

**Regla:** Esta linea es el contrato de completado. Sin ella, el Manager no debe proceder a crear el work plan.

## Ejemplo de flujo completo

```
Usuario: "Quiero añadir un sistema de cache para las consultas a la API"

Agente (leyendo contexto):
- PROJECT.md: menciona "API externa de datos meteorologicos"
- MEMORY.md: registra "usar Redis para cache distribuida" (observacion #3)

Agente (Pregunta 1):
## Pregunta 1: Alcance de "cache"

**Ambiguedad detectada:** "cache" puede referirse a:
- Cache en memoria (dict, lru_cache)
- Cache en disco (SQLite, archivos)
- Cache distribuida (Redis, Memcached)

**Respuesta recomendada:** Cache en memoria con lru_cache para MVP

**Justificacion:** MEMORY.md #3 menciona Redis, pero PROJECT.md indica que es un proyecto local.
lru_cache es suficiente para empezar y es reversible. Redis puede añadirse despues si escala.

**¿Es correcto? (y/n o corrige):**

Usuario: "y"

Agente (Pregunta 2):
## Pregunta 2: "consultas a la API"

**Ambiguedad detectada:** ¿Que API? PROJECT.md menciona multiples fuentes.

**Respuesta recomendada:** API meteorologica (openweathermap.org)

**Justificacion:** Es la unica API externa mencionada en PROJECT.md como "activa".

**¿Es correcto? (y/n o corrige):**

Usuario: "y, pero quiero que sea generico para otras APIs despues"

Agente:
**¿Quieres que añada este termino a CONTEXT.md?**

Propuesta de entrada:
```markdown
### Sistema de Cache

Capa de cache abstracta que puede aplicarse a multiples fuentes de datos (APIs, BD, archivos).
Implementacion inicial: lru_cache para MVP. Extension futura: patron Strategy para Redis/otros.

**Relacionado con:** API externa, Sistema de datos
```

(y/n):

Usuario: "y"

Agente:
> ✅ Grill completo. Términos resueltos: 2. Puedes crear el WP con /plan.
```

## Output Format

Al finalizar el interrogatorio:

1. **Handshake de completado (obligatorio):**
   ```
   > ✅ Grill completo. Términos resueltos: N. Puedes crear el WP con /plan.
   ```

2. **CONTEXT.md (opcional, si el usuario acepto entradas):**
   ```markdown
   # Contexto de Dominio

   ## [Termino 1]
   [Definicion]

   ## [Termino 2]
   [Definicion]
   ```

3. **ADR (opcional, si se justifico):**
   - Crear en `.agent/decisions/ADR-YYYY-NNN.md`
   - Seguir plantilla de ADRs existentes

## Constraints

- **SIEMPRE** una pregunta a la vez
- **SIEMPRE** proporcionar respuesta recomendada antes de esperar respuesta
- **SIEMPRE** leer `PROJECT.md` y `MEMORY.md` antes de preguntar
- **NO** asumir conocimiento del usuario sin confirmar
- **NO** crear `CONTEXT.md` sin aprobacion explicita
- **NO** proceder a `/plan` sin el handshake de completado
- **PREFERIR** respuestas derivadas del codebase sobre especulacion

## References

- `PROJECT.md` - Contexto base del proyecto (obligatorio)
- `.agent/runtime/memory/MEMORY.md` - Memoria curada (obligatorio)
- `.agent/runtime/memory/observations.jsonl` - Historial completo (opcional, para busqueda profunda)
- `CONTEXT.md` - Glosario de dominio (opcional, solo si aporta valor)
- `.agent/decisions/` - ADRs existentes (para referencia de formato)

## Integration opcional con manager-create-work-plan

Esta skill es independiente y NO se integra obligatoriamente en `manager-create-work-plan`.

Si el Manager quiere usarla opcionalmente:
1. Verificar si hay ambiguedad en el requerimiento
2. Sugerir: "¿Quieres que ejecute /grill para clarificar terminos antes de planificar?"
3. Si el usuario acepta, ejecutar el flujo de grill
4. Despues del handshake, proceder con `/plan`

**Regla:** La integracion debe ser opt-in, nunca bloqueante.
