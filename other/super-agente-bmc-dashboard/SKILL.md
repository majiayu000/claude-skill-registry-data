---
name: super-agente-bmc-dashboard
description: >
  Runs a comprehensive BMC Dashboard health audit in fixed order: log anomaly
  analysis, system state, git history, config, dependencies, API endpoints,
  security, Google Sheets/scopes, viewer and ngrok. Produces a single
  "REPORTE SUPER AGENTE BMC — ESTADO COMPLETO". Use when the user asks for
  super agente bmc, reporte estado completo, analisis anomalias logs bmc,
  auditoria dashboard bmc, or full system health check.
---

# Super Agente BMC Dashboard

Ejecuta una auditoría completa del BMC Dashboard en este orden EXACTO. Produce un único reporte: **REPORTE SUPER AGENTE BMC — ESTADO COMPLETO**.

## Execution Order (Exact)

Seguir este orden sin saltar pasos. Si un paso no aplica, reportar "N/A" con explicación.

### 1. Análisis de Anomalías en Logs

```bash
find . -type f \( -name "*.log" -o -path "*/.codebuddy/logs/*" -o -path "*/logs/*.log" \) -not -path "./node_modules/*" -not -path "./.git/*" 2>/dev/null | head -30
```

Para cada archivo de log encontrado (o en el directorio actual):

```bash
tail -n 500 *.log 2>/dev/null || true
```

Si no hay archivos `.log`: pino escribe a stdout por defecto. Indicar que no hay logs persistentes; sugerir `LOG_LEVEL=debug` y redirección para futuras ejecuciones.

**Heurísticas de anomalía** (ver [reference.md](reference.md)):

- Spikes de errores (tasa por ventana temporal)
- Outliers en timestamps (gaps anómalos)
- Errores únicos/raros (mensajes que aparecen 1–2 veces)
- Bursts de auth failures
- Timeouts repentinos
- Correlación con endpoints, scopes, ngrok

### 2. Estado del Sistema

```bash
curl -s http://localhost:3001/health | jq .
pgrep -fl "node.*server" || lsof -i :3001
```

Verificar puertos: 3001 (API), 3849 (dashboard standalone), 5173 (Vite), 4040 (ngrok inspector).

### 3. Git History

```bash
git log --oneline -20
git status
git branch -a
```

### 4. Config (.env + service-account)

- Verificar `.env` existe y contiene: `BMC_SHEET_ID`, `GOOGLE_APPLICATION_CREDENTIALS`, `ML_CLIENT_ID`, `ML_CLIENT_SECRET`, `VITE_API_URL`, `VITE_GOOGLE_CLIENT_ID`
- Verificar `docs/bmc-dashboard-modernization/service-account.json` existe y es JSON válido

### 5. Dependencias + Lockfile

```bash
npm ls --depth=0
npm audit --audit-level=moderate 2>/dev/null || npm audit
```

Confirmar `package-lock.json` presente y sin drift.

### 6. Endpoints API

Listar todos los endpoints desde `server/index.js` y `server/routes/bmcDashboard.js`. Ver tabla completa en [reference.md](reference.md).

Probar endpoints clave:

```bash
curl -s http://localhost:3001/health | jq .
curl -s http://localhost:3001/api/cotizaciones | jq .ok
```

### 7. Seguridad

- `.env` en `.gitignore` (no commitear)
- `service-account.json` no commitear
- Uso de `WEBHOOK_VERIFY_TOKEN`, `API_AUTH_TOKEN`
- CORS, token storage (file vs GCS)

### 8. Google Sheets + Scopes

- Scopes: `spreadsheets.readonly`, `spreadsheets` (write)
- Sheet ID desde `BMC_SHEET_ID`
- Hojas requeridas: Master_Cotizaciones, Pagos_Pendientes, AUDIT_LOG, Ventas realizadas y entregadas, Metas_Ventas

```bash
curl -s http://localhost:3001/api/cotizaciones | jq .ok
```

### 9. Viewer + ngrok

- Dashboard: `http://localhost:5173` (Finanzas) o `http://localhost:3849` (standalone)
- ngrok: `curl -s http://127.0.0.1:4040/api/tunnels`

---

## Output Template

Emitir un único reporte con esta estructura:

```markdown
# REPORTE SUPER AGENTE BMC — ESTADO COMPLETO

## LOG 5 DÍAS / Análisis Anomalías Logs
[Spikes, outliers, errores raros, riesgos críticos]

## Dependencias
[Status, audit, lockfile]

## Endpoints
[Lista + estado de health]

## Seguridad
[Hallazgos]

## Sheets + Scopes
[Config, verificación]

## Estado Actual + Fixes
[Resumen + recomendaciones accionables]
```

---

## Optional: Run Full Audit Script

Para ejecución automatizada:

```bash
bash .cursor/skills/super-agente-bmc-dashboard/scripts/run_audit.sh
```

El script ejecuta los 9 pasos y produce el reporte estructurado.

---

## File Reference

| File                               | Purpose                                                                 |
|------------------------------------|-------------------------------------------------------------------------|
| [reference.md](reference.md)       | Comandos, heurísticas de anomalía, tabla de endpoints, vars de config |
| [scripts/run_audit.sh](scripts/run_audit.sh) | Script de auditoría completa                                             |
