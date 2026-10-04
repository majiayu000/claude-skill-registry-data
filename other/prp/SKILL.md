---
name: prp
description: "Planificar una feature compleja antes de implementarla. Genera un PRP (Product Requirements Proposal) con objetivo, comportamiento esperado, modelo de datos, y fases de implementación. Activar SIEMPRE antes de bucle-agentico, cuando la tarea involucra múltiples archivos/fases coordinadas, o cuando el usuario dice: planea esto, dame un plan, quiero agregar algo grande, necesito un sistema de X, blueprint esto."
context: fork
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: Generar PRP (Product Requirements Proposal)

> Generar un PRP para: $ARGUMENTS

---

## Qué es un PRP

Un PRP (Product Requirements Proposal) es el **blueprint de una pieza de software**. Define QUÉ construir antes de escribir una sola línea de código.

Es el contrato humano-IA. El humano define el objetivo y el por qué. Jarvis investiga el contexto, propone la arquitectura, y genera el plan de fases. Juntos validan antes de ejecutar.

**Sin PRP**: vibe coding al aire, código espagueti, features que no encajan.
**Con PRP**: arquitectura clara, fases definidas, aprendizajes que persisten (auto-blindaje).

---

## Proceso

### Paso 1: Leer el template base

Lee el template en:
```
C:/Users/w10/.claude/PRPs/prp-base.md
```

### Paso 2: Entrevistar si falta contexto

Si `$ARGUMENTS` no tiene suficiente detalle, hacer preguntas directas:

1. **Objetivo**: ¿Qué quieres construir? (estado final en 1-2 oraciones)
2. **Por qué**: ¿Qué problema resuelve? ¿Cuál es el valor?
3. **Criterios de éxito**: ¿Cómo sabes que está terminado? (3-5 checkboxes medibles)
4. **Restricciones**: ¿Hay algo que NO deba hacer o alguna dependencia crítica?

No hacer las 4 preguntas si el usuario ya dio suficiente contexto.

### Paso 3: Investigar contexto del codebase

Antes de escribir el PRP, investigar:
- **Grep/Glob**: Buscar código existente relacionado con la feature
- **Read**: Leer archivos relevantes para entender patrones actuales
- Buscar features similares ya implementadas para reutilizar patrones

### Paso 4: Generar el PRP

Crear el archivo PRP siguiendo el template de `prp-base.md`:

**Nombre del archivo**: `.claude/PRPs/PRP-XXX-{feature-name}.md`

Donde `XXX` es número secuencial y `{feature-name}` en kebab-case.

**Contenido obligatorio**:
- Objetivo (1-2 oraciones)
- Por Qué (tabla problema/solución + valor)
- Criterios de Éxito (checkboxes medibles)
- Comportamiento Esperado (happy path)
- Contexto (referencias, arquitectura propuesta, modelo de datos si aplica)
- Blueprint (SOLO fases, sin subtareas — las subtareas las genera bucle-agentico)
- Secciones vacías de Aprendizajes, Gotchas, Anti-Patrones

### Paso 5: Presentar al usuario

Mostrar resumen del PRP:
- Objetivo
- Número de fases
- Decisiones de arquitectura clave
- Preguntar si quiere ajustar antes de aprobar

**NO implementar nada todavía.** El PRP debe ser aprobado antes de ejecutar.

---

## Después del PRP

Una vez aprobado, la implementación se hace con el skill `/bucle-agentico`, que usa el PRP como guía para ejecutar fase por fase con mapeo de contexto just-in-time.

Los aprendizajes descubiertos durante la implementación se documentan de vuelta en el PRP (sección Aprendizajes) — **auto-blindaje activo**.

---

## Reglas

- SIEMPRE leer `prp-base.md` antes de generar
- NUNCA generar subtareas dentro de las fases (eso lo hace bucle-agentico)
- NUNCA implementar código en este skill (solo generar el documento)
- SIEMPRE investigar el codebase antes de proponer arquitectura
- El PRP se crea en estado `PENDIENTE` hasta que el usuario apruebe
- Los PRPs viven en `.claude/PRPs/` dentro del proyecto actual