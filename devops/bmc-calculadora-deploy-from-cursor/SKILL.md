---
name: bmc-calculadora-deploy-from-cursor
description: >
  Ejecuta desde Cursor (agente con terminal) verificación local, smoke a producción,
  checks pre-deploy y guía de deploy Cloud Run (panelin-calc) + Vercel para Calculadora BMC.
  Usar cuando pidan deploy desde este entorno, dejar configurado el flujo, redeploy API/MATRIZ,
  o “hacerlo todo desde Cursor”.
---

# BMC Calculadora — deploy y verificación desde Cursor

**Objetivo:** que el agente en **Cursor** pueda correr **comandos del repo** en tu máquina (o en CI si la tenés cableada) sin inventar URLs ni secretos. Los **logins** (`gcloud`, `vercel`) son **human gates** si no hay sesión activa.

**Fuentes canónicas (leer si hay duda):** [`AGENTS.md`](../../../AGENTS.md), [`docs/procedimientos/CHECKLIST-DEPLOY-PANELIN-CALC-BMC.md`](../../../docs/procedimientos/CHECKLIST-DEPLOY-PANELIN-CALC-BMC.md), [`docs/calculadora/CANONICAL-PRODUCTION.md`](../../../docs/calculadora/CANONICAL-PRODUCTION.md).

---

## Cuándo usar esta skill

- “Deploy desde Cursor”, “redeploy Cloud Run”, “subir API”, “verificar MATRIZ en prod”, “dejar el flujo armado”.
- Después de cambios en `server/` o en rutas `/api/*`.

---

## Pre-requisitos (no commitear)

| Requisito | Para qué |
|-----------|----------|
| Repo clonado en disco | `cd` a la raíz de **Calculadora-BMC** |
| `node`, `npm` | Scripts `package.json` |
| `.env` local (opcional) | `pre-deploy`, `ml:cloud-run` — **no pegar valores en el chat** |
| `gcloud` autenticado | `gcloud auth login` + proyecto `chatbot-bmc-live` |
| `vercel` CLI (opcional) | Solo si deploy frontend desde terminal |

---

## Flujo que el agente debe ejecutar (orden fijo)

### 1) Verificación local (siempre)

Desde la raíz del repo:

```bash
npm run gate:local:full
```

Si falla **lint** o **test**, corregir antes de hablar de deploy.

### 2) Smoke contra API pública (sin levantar servidor)

```bash
npm run smoke:prod
```

Opcional: `BMC_API_BASE=https://TU-SERVICIO.run.app` o `SMOKE_BASE_URL` si probás otro host.  
Crítico: debe pasar **`GET /api/actualizar-precios-calculadora`** (CSV MATRIZ), salvo `SMOKE_SKIP_MATRIZ=1` a propósito.

### 3) Pre-deploy (checklist + contrato si API local)

```bash
npm run pre-deploy
```

Si el script pide API en 3001, levantar en otra terminal `npm run start:api` y repetir, o usar `BMC_API_BASE` apuntando a prod para el paso de contrato (según lo que documente el script).

### 4) Cloud Run (`panelin-calc`)

**No** inventar comando de build: seguir el runbook del checklist o el script que ya use el equipo (p. ej. Cloud Build / Dockerfile del repo).

Constantes típicas del proyecto (confirmar en checklist):

- Proyecto GCP: `chatbot-bmc-live`
- Región: `us-central1`
- Servicio: `panelin-calc`

Comando útil para **URL real**:

```bash
gcloud run services describe panelin-calc --region=us-central1 --project=chatbot-bmc-live --format='value(status.url)'
```

Sincronizar variables desde `.env` (solo si Matias lo pide y el entorno es seguro):

```bash
./run_ml_cloud_run_setup.sh panelin-calc
```

**MATRIZ:** `BMC_MATRIZ_SHEET_ID` debe ser el workbook correcto o omitirse para usar el default en [`server/config.js`](../../../server/config.js) (`1oDMkBgWxX7cu7TpSvuO30tCTUWl68IBDhC4cQTP79Xo`).

### 5) Vercel (frontend)

Si el front está en Vercel: deploy desde dashboard o `vercel --prod` según convención del repo. Ver [`scripts/deploy-vercel.sh`](../../../scripts/deploy-vercel.sh).  
Variables de build: **`VITE_API_URL`** = URL base del API Cloud Run (sin path `/api` extraño; solo origin del servicio).

### 6) Post-deploy mínimo

- `npm run smoke:prod` con la URL canónica.
- Opcional: `curl -sSI "$BASE/api/actualizar-precios-calculadora"` y comprobar `200` + `text/csv`.

### 7) Estado del proyecto

Si hubo cambios de comportamiento o deploy: una línea en [`docs/team/PROJECT-STATE.md`](../../../docs/team/PROJECT-STATE.md) bajo **Cambios recientes** (regla del repo).

---

## Anti-patrones

- No hardcodear sheet IDs nuevos en la skill; usar env + `config.js`.
- No imprimir `API_AUTH_TOKEN`, JSON de service account, ni `ML_CLIENT_SECRET`.
- No marcar “deploy OK” sin **smoke** o evidencia HTTP.
- OAuth Meta / WhatsApp / ML login interactivo → [`docs/team/HUMAN-GATES-ONE-BY-ONE.md`](../../../docs/team/HUMAN-GATES-ONE-BY-ONE.md).

---

## Cómo invocarlo en Cursor

1. **Adjuntar la skill** en el chat (o escribir): *“usá la skill bmc-calculadora-deploy-from-cursor”*.  
2. O **regla de Cursor** (opcional): en *Settings → Rules*, añadir: *“Cuando pida deploy Cloud Run / Vercel / smoke prod de Calculadora BMC, seguir `.cursor/skills/bmc-calculadora-deploy-from-cursor/SKILL.md`.”*

---

## Relación con otros agentes/skills

- Diagnóstico profundo Cloud Run: skill **cloudrun-diagnostics-reporter** (si está disponible).
- Vercel genérico: skill **vercel-deploy** en entorno Codex (no duplicar aquí el detalle de Vercel salvo lo mínimo).
