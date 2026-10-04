---
name: perf-engineer
description: >
  Performance y load testing — k6, artillery, Lighthouse, profiling de
  código y bases de datos. Identificar y eliminar bottlenecks.
  Trigger: Cuando necesitás hacer load testing, profiling, optimizar performance lenta o identificar bottlenecks.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Skill: perf-engineer

Performance. Medí antes de optimizar. Nunca asumas.

## Trigger

- La app responde lenta
- Querés saber cuántos usuarios soporta antes de caerse
- Una consulta SQL tarda 10 segundos
- Querés optimizar el bundle de frontend o el tiempo de respuesta de API
- Necesitás load testing para un deploy

## Workflow LEND

1. ANALIZAR
   ├── Stack: web (Lighthouse), API (k6/artillery), DB (EXPLAIN ANALYZE), código (cProfile/py-spy)
   ├── Métricas actuales: tiempo de respuesta, throughput, error rate
   ├── Cuello de botella: ¿CPU, memoria, I/O, red, DB?
   └── Objetivo: ¿cuánto querés mejorar? ¿hay SLO definido?

2. OFRECER (Menú del Senior)
   ├── A) Web perf — Lighthouse, Core Web Vitals, lazy loading, imágenes, fuentes
   ├── B) API load testing — k6, escenarios de carga, picos, estrés
   └── C) Profiling profundo — cProfile/py-spy (código), EXPLAIN ANALYZE (DB), flamegraphs

3. ELEGIR → confirmación

4. HACER
   ├── Web: medir LCP/INP/CLS, optimizar imágenes (WebP/AVIF), lazy loading, reducir JS
   ├── API: k6 script con escenarios (carga normal, pico, estrés), umbrales (< 200ms p95)
   ├── DB: EXPLAIN ANALYZE en queries lentas, índices faltantes, conexiones, vacuum
   ├── Código: cProfile/py-spy para encontrar funciones lentas, optimizar loops, cachear
   ├── Reporte: métricas antes/después, gráficos, recomendaciones priorizadas
   └── Cache: Redis, CDN, browser cache, query cache. Cachear todo lo que no cambia seguido

5. VERIFICAR
   ├── Las métricas mejoraron respecto al baseline
   ├── Los tests de carga no rompen nada
   └── No hay regresiones (medir de nuevo después del fix)
