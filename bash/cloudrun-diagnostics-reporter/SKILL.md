---
name: cloudrun-diagnostics-reporter
description: >
  Extracts full state of a Cloud Run service (panelin-calc) via REST API and gcloud
  logging/gsutil, produces a structured diagnostic report and flags persistent anomalies.
  Can open Cloud Console (Run, Logging, Storage) in browser to verify or capture state.
  Use when the user asks for Cloud Run full state, diagnostic report, anomaly report,
  deploy console review, or "ejecutar comandos en consola del deploy y Google Cloud".
---

# Cloud Run Diagnostics & Anomaly Reporter

Analiza el estado completo del servicio Cloud Run **panelin-calc** (proyecto chatbot-bmc-live, us-central1), ejecutando los comandos correctos en Cloud Shell y opcionalmente en el navegador (Cloud Console). Produce un reporte estructurado y detecta **anomalías persistentes**.

## Contexto importante

- `gcloud run services describe` puede fallar con `TypeError: string indices must be integers, not 'str'`. Usar siempre el bypass vía **REST API v2** (script o curl + Python).
- Los comandos que usan `gcloud` (logging, auth) y `gsutil` deben ejecutarse **en Google Cloud Shell**; el agente puede generar el script y las instrucciones, o usar el navegador para abrir Cloud Console y revisar Run / Logging / Storage.

## Orden de ejecución (diagnóstico completo)

Seguir este orden. Si el usuario no tiene Cloud Shell abierto, entregar el script listo para pegar y ejecutar allí.

### 1. Estado del servicio (REST v2 — sin gcloud describe)

Ejecutar el script del repo que usa solo REST:

```bash
# En Cloud Shell (o con CLOUDRUN_ACCESS_TOKEN en otro entorno):
./scripts/cloudrun-full-diagnostic.sh
# O el script reducido solo describe:
./scripts/cloudrun-describe-via-api.sh
```

Si no hay script disponible, usar el one-liner de REST (ver reference.md).

### 2. Errores recientes (logging)

Comandos para ejecutar **en Cloud Shell**:

```bash
# Errores (severity >= ERROR), últimas 24h
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="panelin-calc" AND severity>=ERROR' \
  --project=chatbot-bmc-live --limit=50 --format="table(timestamp,jsonPayload.message)" --freshness=1d 2>/dev/null || true

# Resumen por status HTTP (4xx/5xx)
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="panelin-calc" AND httpRequest.status>=400' \
  --project=chatbot-bmc-live --freshness=7d --limit=500 --format="value(httpRequest.status)" 2>/dev/null | sort | uniq -c | sort -rn
```

### 3. Bucket de tokens (ML OAuth)

```bash
gsutil ls -la gs://panelin-calc-ml-tokens/ 2>/dev/null || echo "Bucket no accesible o vacío"
```

### 4. Anomalías persistentes

Considerar **anomalía persistente** si en los logs aparece de forma repetida (p. ej. mismo mensaje >5 veces en 7 días):

- "OAuth not initialized" / "ML_CLIENT_SECRET"
- 500 en `/auth/ml/start`
- 401 en `/ml/questions`
- 404 en `/auth/ml/callback`, `/favicon.ico`, `/`, `/robots.txt`

Incluir en el reporte una sección **Anomalías persistentes** con: mensaje, cuenta, último timestamp, recomendación.

### 5. (Opcional) Navegador — Cloud Console

Si el agente tiene acceso al browser MCP:

1. Abrir **Cloud Run** → servicio `panelin-calc` → pestaña Métricas/Logs.
2. Abrir **Logging** → filtrar por `resource.labels.service_name="panelin-calc"`.
3. Abrir **Storage** → bucket `panelin-calc-ml-tokens` (si existe).

Usar para verificar estado visual, capturar métricas o confirmar que el reporte generado por comandos es coherente.

## Productos del skill

1. **Reporte de diagnóstico** — Usar la plantilla en `reference.md` (Estado general, Config contenedor, Errores HTTP, Seguridad, Recomendaciones).
2. **Reporte de anomalías persistentes** — Tabla: mensaje o patrón, conteo, último visto, severidad, acción sugerida.
3. **Script listo para Cloud Shell** — `scripts/cloudrun-full-diagnostic.sh` que ejecuta pasos 1–3 y escribe el reporte en stdout o en un archivo.

## Cuándo usar este skill

- "Extraer estado completo del servicio y todo lo que está sucediendo"
- "Reportes ante anomalías persistentes"
- "Ejecutar comandos en la consola del deploy y Google Cloud"
- "Analizar por browser y ejecutar los comandos correctos para revisar y encontrar mejoras"
- "Diagnóstico completo panelin-calc Cloud Run"

## Archivos de referencia

| Archivo | Uso |
|---------|-----|
| [reference.md](reference.md) | Comandos one-liner, plantilla de reporte, heurísticas de anomalía |
| [scripts/cloudrun-full-diagnostic.sh](../../../scripts/cloudrun-full-diagnostic.sh) | Script único para Cloud Shell (REST + logging + gsutil + reporte) |
