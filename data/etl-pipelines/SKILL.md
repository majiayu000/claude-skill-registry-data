---
name: etl-pipelines
description: >
  Pipelines ETL/ELT con Pandas — extracción, transformación, carga.
  Automatización de flujos de datos robustos y monitoreables.
  Trigger: Cuando necesitás construir un pipeline de datos, procesar archivos en batch, automatizar transformaciones, o diseñar el flujo de datos de un proyecto.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T2-fast
---

# Skill: etl-pipelines

Pipelines ETL. Que los datos fluyan solos y no se rompan los viernes.

## Trigger

- Necesitás procesar archivos regularmente (diario, semanal)
- Los datos vienen de múltiples fuentes y hay que unificarlos
- Querés automatizar transformaciones que hoy hacés a mano
- El proceso manual ya no escala

## Workflow LEND

```
1. ANALIZAR
   ├── Fuentes: ¿archivos, APIs, DBs, web scraping?
   ├── Frecuencia: one-shot, diaria, tiempo real
   ├── Volumen: ¿MB, GB? ¿crece con el tiempo?
   └── Destino: ¿DB, data lake, CSV, dashboard?

2. OFRECER (Menú del Senior)
   ├── A) Script Python simple — Pandas pipeline, schedule con cron
   ├── B) Pipeline modular — extract + transform + load como funciones separadas
   └── C) Orquestación — Prefect / Dagster con monitoreo, retries, logging

3. ELEGIR → confirmación

4. HACER
   ├── Extraer: leer de fuente (CSV, API, DB), validar que llegaron datos
   ├── Transformar: limpiar, tipar, unificar, calcular
   ├── Cargar: escribir a destino (DB, archivo, API)
   ├── Logging: cada etapa loguea filas procesadas, errores, duración
   ├── Error handling: try/except con reintentos y notificación
   └── Schedule: cron para scripts, scheduler para orquestadores

5. VERIFICAR
   ├── El pipeline corre de principio a fin sin errores
   ├── Los datos cargados coinciden con los datos fuente (mismo count)
   └── Si falla, el error es claro y hay un mecanismo de alerta
```

## Patrones

- **ETL vs ELT**: ETL si transformás antes de cargar. ELT si cargás crudo y transformás en destino.
- **Pipeline idempotente**: correrlo dos veces da el mismo resultado (upsert, no insert duplicado)
- **Logging**: cada etapa registra: qué entró, qué salió, cuánto tardó, errores
- **Incremental**: procesar solo lo nuevo en vez de todo siempre
- **Checkpoint**: guardar el estado para poder retomar desde donde falló

## Anti-patrones

- ❌ Pipeline no idempotente — correrlo dos veces duplica datos
- ❌ Sin logging — cuando falla no sabés en qué paso
- ❌ Todo en un solo script de 500 líneas — partí en etapas
- ❌ Sin manejo de errores — un timeout de API mata todo el pipeline
- ❌ Procesar todo siempre — si solo cambiaron 10 filas, no proceses 10M
