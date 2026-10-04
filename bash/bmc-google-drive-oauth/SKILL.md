---
name: bmc-google-drive-oauth
description: >-
  Implementación y verificación end-to-end de Google Drive (GIS) en Calculadora-BMC:
  OAuth Web client, VITE_GOOGLE_CLIENT_ID, scripts drive:bootstrap / drive:configure /
  drive:vercel-env, verify de env y de dist, workflows GitHub opt-in. Usar cuando el
  usuario pida Drive, invalid_client, VITE_GOOGLE_CLIENT_ID, automatizar setup GCP/Vercel,
  o “agente Drive OAuth”.
---

# BMC — Google Drive OAuth (GIS) — implementación y verificación

**Código cliente:** [`src/utils/googleDrive.js`](../../src/utils/googleDrive.js) (`VITE_GOOGLE_CLIENT_ID`, scope `drive.file`).

**Plan maestro:** [`docs/GOOGLE-DRIVE-OAUTH-AUTOMATION-PLAN.md`](../../docs/GOOGLE-DRIVE-OAUTH-AUTOMATION-PLAN.md).  
**Setup manual detallado:** [`docs/GOOGLE_DRIVE_SETUP_PROMPT.md`](../../docs/GOOGLE_DRIVE_SETUP_PROMPT.md).  
**Vercel:** [`docs/VERCEL-CALCULADORA-SETUP.md`](../../docs/VERCEL-CALCULADORA-SETUP.md).

**Regla:** no commitear secretos; `VITE_GOOGLE_CLIENT_ID` en **`.env.local`** (gitignored) o variables Vercel; **no** pisar `.env` entero con un solo valor.

---

## 1. Orden de ejecución (implementación / reparación)

**Un solo comando (recomendado):** desde la raíz del repo, con el Client ID copiado de Google Cloud → Credenciales:

```bash
npm run drive:one-shot -- 'TU_CLIENT_ID.apps.googleusercontent.com'
```

Equivale a: bootstrap GCP → `.env.local` → verify env → `drive:vercel-env` → `npm run build` → verify dist. Opciones: `SKIP_VERCEL=1`, `OPEN_CONSOLE=1`. Ver `scripts/drive-oauth-one-shot.sh`.

| Paso | Comando o acción |
|------|-------------------|
| 1. GCP API + enlaces | `npm run drive:bootstrap` — opc. `npm run drive:bootstrap -- --open` |
| 2. Consola Google | Cliente OAuth **Web application**; orígenes JS: `http://localhost:5173`, `https://calculadora-bmc.vercel.app`, origen Cloud Run si aplica; scope consentimiento `drive.file`; usuarios de prueba si la app está en Testing |
| 3. Client ID local | `npm run drive:configure` **o** `./run_drive_setup.sh '<client-id>.apps.googleusercontent.com'` |
| 4. Formato | `npm run verify:google-drive-oauth` |
| 5. Bundle | `npm run build && npm run verify:google-drive-dist` |
| 6. Vercel (CLI) | `npm run drive:vercel-env -- '<client-id>'` luego **redeploy** |
| 7. CI (opt-in) | Actions → **Drive OAuth — verify Client ID** / **… in dist** (`workflow_dispatch`) con secret `VITE_GOOGLE_CLIENT_ID` |

---

## 2. Diagnóstico rápido

| Síntoma | Acción |
|---------|--------|
| `401 invalid_client` / OAuth client not found | El Client ID no existe en el proyecto GCP correcto; recrear credencial y actualizar `.env.local` / Vercel + redeploy |
| `[GDrive] No VITE_GOOGLE_CLIENT_ID` | Falta variable o no reiniciaste Vite tras cambiar `.env*` |
| Prod sin Drive tras cambiar Vercel | `VITE_*` se bakea en **build** — redeploy obligatorio; `verify:google-drive-dist` en CI |

---

## 3. Artefactos que deben existir en el repo

- `scripts/verify-google-drive-oauth-env.mjs`
- `scripts/set-vite-google-client.mjs`
- `scripts/drive-oauth-bootstrap.sh`
- `scripts/vercel-drive-env-push.sh`
- `scripts/verify-vite-google-client-in-dist.mjs`
- `run_drive_setup.sh` (delega en `set-vite-google-client.mjs`)
- `.github/workflows/drive-oauth-verify.yml`
- `.github/workflows/drive-oauth-dist-verify.yml`

---

## 4. Verificación mínima (agente al cerrar tarea)

Desde la raíz del repo:

```bash
npm run verify:google-drive-oauth
npm run verify:google-drive-dist
```

Si no hay Client ID configurado, el segundo comando **omite** (exit 0). Tras cambios en `src/utils/googleDrive.js`: `npm run lint` y `npm run gate:local:full` si tocó UI crítica.

---

## 5. Agente Cursor

Definición recomendada para invocación explícita: [`.cursor/agents/bmc-google-drive-oauth.md`](../../agents/bmc-google-drive-oauth.md) (nombre sugerido en chat: **agente Drive OAuth** o **bmc-google-drive-oauth**).
