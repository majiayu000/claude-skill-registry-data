---
name: bmc-api-contract-validator
description: >
  Validates API responses against the canonical contract from planilla-inventory
  and DASHBOARD-INTERFACE-MAP. Catches drift before the UI breaks. Use when
  validating API contracts, pre-deploy checks, or after bmcDashboard.js changes.
---

# BMC API Contract Validator

**Before working:** Read `docs/team/knowledge/Contract.md` if it exists.

Valida que las respuestas de la API cumplan el contrato canónico definido por Mapa (planilla-inventory, DASHBOARD-INTERFACE-MAP). Detecta drift antes de que la UI falle.

---

## When to Use

- Después de cambios en `bmcDashboard.js` o `sheets-api-server.js`
- Pre-deploy: validar que los endpoints devuelven la forma esperada
- Cuando Vista reporta "datos no disponibles" o errores de consumo
- Sync: como parte del pre-deploy checklist

---

## Canonical Contracts (from Mapa)

### GET /api/kpi-financiero

```json
{
  "ok": true,
  "pendingPayments": [{ "CLIENTE_NOMBRE", "COTIZACION_ID", "MONTO", "MONEDA", "FECHA_VENCIMIENTO", "ESTADO_PAGO" }],
  "calendar": [{ "date", "total", "byCurrency": {} }],
  "byPeriod": { "estaSemana", "proximaSemana", "esteMes", "total" },
  "byCurrency": { "$": { "total", "estaSemana", "proximaSemana", "esteMes" }, ... },
  "currencies": ["$", "UES", ...],
  "metas": [{ "PERIODO", "TIPO", "META_MONTO", "MONEDA", "NOTAS" }]
}
```

### GET /api/proximas-entregas

```json
{ "ok": true, "data": [{ "COTIZACION_ID", "CLIENTE_NOMBRE", "TELEFONO", "DIRECCION", "FECHA_ENTREGA", ... }] }
```

### GET /api/audit

```json
{ "ok": true, "headers": [], "data": [{ "TIMESTAMP", "ACTION", "ROW", "OLD_VALUE", "NEW_VALUE", "REASON", "USER", "SHEET" }] }
```

---

## Workflow

1. **Read** planilla-inventory.md and DASHBOARD-INTERFACE-MAP.md for contract.
2. **Run** `node scripts/validate-api-contracts.js` (or equivalent) against running server.
3. **Report** pass/fail per endpoint; list missing or unexpected fields.
4. **Update** PROJECT-STATE if drift detected; notify Mapa and Vista via Log.

---

## Script

Run with server at http://localhost:3001 (or BMC_API_BASE env):

```bash
BMC_API_BASE=http://localhost:3001 node scripts/validate-api-contracts.js
```

---

## Reference

- planilla-inventory: `docs/google-sheets-module/planilla-inventory.md`
- DASHBOARD-INTERFACE-MAP: `docs/bmc-dashboard-modernization/DASHBOARD-INTERFACE-MAP.md`
- bmcDashboard.js: `server/routes/bmcDashboard.js`
