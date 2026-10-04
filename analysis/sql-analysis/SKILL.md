---
name: sql-analysis
description: >
  Análisis de datos con SQL — joins, window functions, CTEs, subqueries.
  Consultas eficientes y legibles para extraer insights directamente de la DB.
  Trigger: Cuando necesitás consultar bases de datos, hacer análisis en SQL, joins, subqueries, o window functions.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T3-balanced
---

# Skill: sql-analysis

SQL para análisis. No solo SELECT * FROM.

## Trigger

- Los datos están en una base de datos relacional
- Necesitás agregar, filtrar o cruzar tablas grandes
- La pregunta se responde con una consulta SQL directa
- Querés hacer análisis sin mover los datos a Python

## Workflow LEND

```
1. ANALIZAR
   ├── Esquema: ¿qué tablas hay? ¿cómo se relacionan?
   ├── Volumen: ¿cuántas filas? ¿índices? ¿particiones?
   ├── Pregunta: ¿qué datos necesito? ¿en qué granularidad?
   └── SQL o Python? si necesitás transformaciones complejas, Python.

2. OFRECER (Menú del Senior)
   ├── A) Consulta directa — SELECT + WHERE + GROUP BY, simple y rápida
   ├── B) CTE + Window functions — consultas más complejas pero legibles
   └── C) Materialized view — si la consulta se repite, crear vista

3. ELEGIR → confirmación

4. HACER
   ├── FROM + JOINs con cardinalidad clara (1:1, 1:N, N:M)
   ├── WHERE temprano: filtrar antes de agregar
   ├── GROUP BY con agregaciones (SUM, AVG, COUNT, MIN, MAX)
   ├── Window functions para rankings, running totals, YoY
   ├── CTEs para legibilidad (WITH ... AS ...)
   └── ORDER BY + LIMIT al final, EXPLAIN ANALYZE para performance

5. VERIFICAR
   ├── La cardinalidad del JOIN es correcta (no hay duplicación inesperada)
   ├── Los agregados tienen sentido (SUM con GROUP BY correcto)
   └── La consulta corre en tiempo aceptable (< 1s para dashboards)
```

## Patrones

- **WHERE antes de JOIN**: filtrar lo más temprano posible reduce filas a procesar
- **CTE para legibilidad**: partí consultas largas en bloques con WITH
- **Window functions**: ROW_NUMBER(), RANK(), LAG(), LEAD() para análisis sin perder detalle
- **EXPLAIN ANALYZE**: si una consulta es lenta, el plan de ejecución dice por qué
- **Índices**: si filtrás por fecha o cliente seguido, poné un índice

## Anti-patrones

- ❌ SELECT * en producción — trae columnas al pedo, mata performance
- ❌ JOIN sin verificar cardinalidad — un 1:N cuando esperabas 1:1 te duplica filas
- ❌ Filtrar después de GROUP BY — usá HAVING, no WHERE
- ❌ Subqueries correlacionadas — suelen ser lentas. Usá CTE o JOIN
- ❌ No usar índices — consultas de 10 segundos se vuelven 10ms con el índice correcto
