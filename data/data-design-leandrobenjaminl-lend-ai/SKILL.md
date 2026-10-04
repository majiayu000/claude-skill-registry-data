---
name: data-design
description: >
  Diseñá la estrategia de análisis — elegí el enfoque, las herramientas y
  el pipeline antes de escribir código.
  Trigger: Cuando ya tenés clara la pregunta y necesitás decidir cómo abordarla.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T5-deep
---

# Skill: data-design

Diseño de análisis. La pregunta está clara, ahora definí cómo responderla.

## Trigger

- Ya definiste la pregunta de negocio (con data-question)
- Tenés que elegir entre múltiples enfoques técnicos
- No sabés si esto es un trabajo de SQL, Python o Excel
- El proyecto creció y necesitás una arquitectura de análisis

## Workflow LEND

```
1. ANALIZAR
   ├── Pregunta: ¿descriptiva, diagnóstica, predictiva o prescriptiva?
   ├── Datos: ¿cuántos? ¿estructurados? ¿limpios? ¿dónde están?
   ├── Stack: ¿SQL directo, Python, R, o herramienta visual?
   └── Entrega: ¿dashboard, reporte PDF, API, modelo?

2. OFRECER (Menú del Senior)
   ├── A) SQL-first — si los datos están en DB y la pregunta es simple
   ├── B) Python pipeline — si necesitás transformaciones complejas o ML
   └── C) Híbrido — SQL para extracción + Python para análisis + visualización

3. ELEGIR → confirmación

4. HACER
   ├── Definir pipeline de análisis (extracción → limpieza → transformación → análisis → presentación)
   ├── Elegir herramientas: Pandas, Polars, DuckDB, SQLAlchemy
   ├── Estimar tiempo: ¿esto se resuelve en 30 minutos o necesita 2 semanas?
   ├── Identificar riesgos: datos incompletos, leakage, escala
   └── Documentar el diseño antes de implementar

5. VERIFICAR
   ├── El diseño responde la pregunta original sin desviarse
   ├── Las herramientas elegidas son las correctas para el volumen de datos
   └── Hay un plan B si el enfoque principal falla
```

## Patrones

- **Pregunta primero, diseño después**: no diseñes sin saber qué preguntás
- **Lo más simple que funciona**: SQL > Python > Spark. No uses un cañón para una mosca
- **Pipeline explícito**: cada etapa tiene input, transformación y output claros
- **Prototipar rápido**: un MVP de 30 lines vale más que una arquitectura de 2 días

## Anti-patrones

- ❌ Diseñar sin tener clara la pregunta — terminás resolviendo lo que no te pidieron
- ❌ Elegir herramienta por moda y no por necesidad — "usemos Spark" para 10MB de datos
- ❌ Arquitectura sobreingenierizada — pipelines de 10 etapas para una pregunta de 2 variables
- ❌ No considerar el tiempo — "esto es fácil" sin haber visto los datos
