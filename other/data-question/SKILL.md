---
name: data-question
description: >
  Definí preguntas de negocio claras antes de analizar. Sin buena pregunta,
  no hay buen análisis.
  Trigger: Cuando arrancás un análisis nuevo y necesitás clarificar qué querés descubrir.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T2-fast
---

# Skill: data-question

Sin buena pregunta, no hay buen análisis. Todo arranca acá.

## Trigger

- Te pidieron "analizá estos datos" sin contexto
- Tenés un dataset pero no sabés qué buscar
- El usuario dijo algo vago como "fijate qué pasa con las ventas"
- Necesitás alinear el análisis con objetivos de negocio

## Workflow LEND

```
1. ANALIZAR
   ├── ¿Quién pide el análisis y para qué?
   ├── ¿Qué decisión se va a tomar con los resultados?
   ├── ¿Qué datos están disponibles? ¿alcanzan?
   └── Si es vago → frená. Preguntá hasta tener algo concreto.

2. OFRECER (Menú del Senior)
   ├── A) Pregunta descriptiva — "¿qué pasó?" (reporte de situación)
   ├── B) Pregunta diagnóstica — "¿por qué pasó?" (causa raíz)
   └── C) Pregunta predictiva — "¿qué va a pasar?" (forecast, tendencia)

3. ELEGIR → confirmación

4. HACER
   ├── Redactar la pregunta en formato SMART:
   │   Specific: "¿cuánto crecieron las ventas?" no "¿cómo nos fue?"
   │   Measurable: métrica concreta y unidad
   │   Achievable: con los datos disponibles
   │   Relevant: alineada con el negocio
   │   Time-bound: período definido
   ├── Identificar: qué variable es target, cuáles son features
   ├── Definir: criterio de éxito del análisis
   └── Documentar la pregunta en el informe

5. VERIFICAR
   ├── La pregunta es respondible con los datos disponibles
   ├── El usuario confirmó que esto es lo que necesita
   └── El criterio de éxito está claro
```

## Patrones

- **Pregunta SMART**: Specific, Measurable, Achievable, Relevant, Time-bound
- **Empezar con "por qué"**: "¿por qué bajaron las ventas?" es más útil que "¿cuánto bajaron?"
- **Frenar la ambigüedad**: si el usuario es vago, no arranques. Preguntá hasta tener algo concreto.
- **Una pregunta por análisis**: si tenés múltiples preguntas, partí en análisis separados.

## Anti-patrones

- ❌ "Analizá estos datos a ver qué encontrás" — esto no es una pregunta, es perder tiempo
- ❌ Pregunta sin métrica — "cómo nos fue" no significa nada sin unidad
- ❌ Pregunta sin tiempo — "crecieron las ventas" ¿cuándo? ¿respecto a qué?
- ❌ Pregunta imposible — no se puede responder con los datos disponibles
