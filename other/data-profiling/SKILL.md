---
name: data-profiling
description: >
  Profiling automático de datasets — ydata-profiling, pandera, great
  expectations. Entendé cualquier dataset en minutos.
  Trigger: Cuando recibís un dataset nuevo y necesitás entenderlo rápido, o querés un reporte de calidad de datos.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T2-fast
---

# Skill: data-profiling

Profiling automático. En minutos sabés si el dataset es una joya o un desastre.

## Trigger

- Te pasaron un CSV que nunca viste
- Querés un reporte rápido de calidad antes de analizar
- Necesitás documentar la estructura de un dataset
- Vas a presentar un análisis y querés una sección de "calidad de datos"

## Workflow LEND

```
1. ANALIZAR
   ├── Tamaño: filas, columnas, memoria ocupada
   ├── Tipos: ¿Pandas infirió bien? ¿fechas, números, categorías?
   ├── Calidad: nulos %, duplicados %, valores únicos
   └── ¿Hay columnas que deberían estar pero no están?

2. OFRECER (Menú del Senior)
   ├── A) Express — ydata-profiling (pandas_profiling), 1 línea, reporte HTML completo
   ├── B) Custom — profiling manual con describe() + info() + isnull() + duplicated()
   └── C) Schema-based — pandera para validar contra un esquema definido

3. ELEGIR → confirmación

4. HACER
   ├── ydata-profiling: ProfileReport(df, title="Reporte", explorative=True)
   ├── Manual: describe(include='all'), info(), isnull().sum(), duplicated().sum()
   ├── Buscar: valores extremos, categorías con baja frecuencia, columnas constantes
   ├── Pandera: definir schema y validar (para producción)
   └── Guardar reporte en HTML para compartir

5. VERIFICAR
   ├── El reporte cubre todas las variables
   ├── Los problemas de calidad están documentados
   └── El schema pasa si se usa pandera
```

## Patrones

- **Profiling primero**: antes de cualquier análisis, un profiling rápido te ahorra horas de debugging
- **ypdata-profiling para explorar**: reporte interactivo con correlaciones, alerts, muestras
- **Pandera para producción**: define schemas y validalos en pipelines de CI
- **Manual para control fino**: describe + info + isnull + duplicated cuando necesitás decidir

## Anti-patrones

- ❌ No hacer profiling y asumir que los datos están bien
- ❌ Confiar ciegamente en profiling automático — siempre verificá hallazgos raros
- ❌ Ignorar las alertas de ydata-profiling (alta correlación, alta cardinalidad, desbalanceo)
- ❌ No documentar la calidad — "esto estaba medio sucio" no sirve en un informe
