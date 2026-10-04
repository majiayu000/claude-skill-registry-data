---
name: bmc-mercadolibre-api
description: >-
  Conector Mercado Libre en Calculadora-BMC: arranque de la API (puerto 3001),
  OAuth 2.0 (UY), ngrok/HTTPS, variables .env, verificación (ml:verify), y uso
  de rutas /auth/ml/* y /ml/* (preguntas, órdenes, users/me). Usar cuando el
  usuario o el flujo requieran Mercado Libre, Panelin ML, OAuth ML, ngrok,
  curl a localhost:3001/ml, o cambios en server/index.js / mercadoLibreClient.
---

# BMC — Mercado Libre API (conector + arranque)

**Antes de tocar código:** leer [AGENTS.md](../../AGENTS.md) (raíz del repo) y [docs/ML-OAUTH-SETUP.md](../../docs/ML-OAUTH-SETUP.md).

Este skill une **dos cosas que siempre van juntas** para agentes:

1. **Cómo levantar la API** que sirve el conector ML.
2. **Cómo operar Mercado Libre** vía esa API (OAuth, endpoints, verificación).

Sin la API en marcha, **no hay** llamadas a ML (`/ml/*` devuelve conexión rechazada).

---

## 1. Arranque de la API (obligatorio antes de ML)

| Objetivo | Comando (desde la raíz del repo `Calculadora-BMC`) |
|----------|-----------------------------------------------------|
| Solo API en **:3001** | `npm run start:api` |
| Crear `.env` si no existe (no pisa uno actual) | `npm run env:ensure` |
| **HTTPS para OAuth:** ngrok + API juntos | `npm run ml:local` |
| Solo API sin ngrok | `npm run ml:local:api` |

- **Puerto por defecto:** `3001` (`PORT` en `.env` si aplica).
- **Base local:** `http://localhost:3001`
- **Proceso:** debe quedar **en ejecución** mientras se prueba OAuth o `/ml/*` (terminal abierta o background).

**Variables mínimas** (`.env` en la raíz del repo): `ML_CLIENT_ID`, `ML_CLIENT_SECRET`. Si ML exige **https** en el redirect: `ML_REDIRECT_URI_DEV=https://TU_HOST/auth/ml/callback` (misma URL en [Developers Uruguay](https://developers.mercadolibre.com.uy)).

Documentación de flujo completo: [docs/ML-OAUTH-SETUP.md](../../docs/ML-OAUTH-SETUP.md).  
OAuth oficial + mapeo conceptual: [docs/mercadolibre-developers-auth-authorization-uy.md](../../docs/mercadolibre-developers-auth-authorization-uy.md).

---

## 2. Verificación después de arrancar

Con la API **ya corriendo**, en **otra terminal**:

```bash
npm run ml:verify
```

Comprueba `/health`, `/auth/ml/start?mode=json` y `/auth/ml/status`. Si OAuth está completo: `hasTokens: true` y status **200**.

---

## 3. Superficie HTTP del conector (implementación)

**Código:** [server/index.js](../../server/index.js), cliente: [server/mercadoLibreClient.js](../../server/mercadoLibreClient.js), config: [server/config.js](../../server/config.js).

| Área | Rutas |
|------|--------|
| OAuth | `GET /auth/ml/start`, `GET /auth/ml/callback`, `GET /auth/ml/status` |
| Datos ML (Bearer = token guardado) | `GET /ml/users/me`, `GET /ml/questions`, `GET /ml/questions/:id`, `POST /ml/questions/:id/answer`, `GET /ml/orders`, `GET /ml/orders/:id`, `GET /ml/items/:id` |
| Otros | `GET /health`, `GET /capabilities`, dashboard bajo `/api`, estático `/finanzas` |

**Reglas del repo:** no hardcodear secretos; tokens en almacén local/GCS según config; errores de ML se propagan con el payload que devuelve la API de Mercado Libre.

---

## 4. Uso típico (agente / operador)

1. `npm run env:ensure` (solo si falta `.env`).
2. Completar `ML_*` en `.env`; si hace falta HTTPS, configurar ngrok + `ML_REDIRECT_URI_DEV` + portal ML.
3. `npm run ml:local` **o** `npm run start:api`.
4. Navegador: `https://TU_HOST/auth/ml/start` o `http://localhost:3001/auth/ml/start` según política de redirect.
5. `npm run ml:verify`.
6. Probar: `curl -sS "http://localhost:3001/ml/users/me" | head -c 400`, luego `/ml/questions`, etc.

---

## 5. Cuándo aplicar esta skill

- Arranque o depuración del **servidor** que expone ML.
- OAuth, ngrok, `invalid_query_string`, 403 en órdenes, tokens, refresh.
- Cambios en rutas `/ml/*` o en el cliente ML.
- Instrucciones para **otros agentes** del equipo que deban “incorporar” el mismo flujo: **remitir a este SKILL.md** como paso 0 + [ML-OAUTH-SETUP.md](../../docs/ML-OAUTH-SETUP.md).

---

## 6. Propagación

Si el cambio afecta a integración, dashboard o documentación del equipo: actualizar [docs/team/PROJECT-STATE.md](../../docs/team/PROJECT-STATE.md) y la tabla de propagación en [docs/team/PROJECT-TEAM-FULL-COVERAGE.md](../../docs/team/PROJECT-TEAM-FULL-COVERAGE.md) cuando corresponda.

---

## 7. Recursos adicionales

- Detalle de endpoints y troubleshooting: [reference.md](reference.md)
