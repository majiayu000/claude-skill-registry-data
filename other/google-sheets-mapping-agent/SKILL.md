---
name: google-sheets-mapping-agent
description: >
  Builds an AI agent that maps and works directly on Google Sheets: read (map)
  and write (edit, append, update) via the Sheets API. Documents data types,
  columns, relationships, lookups, calculation logic; implements or extends
  server routes/scripts for get/push. Use when mapping Admin Sheet, CRM_Operativo,
  editing sheet data from the app, or adding new sheet read/write endpoints.
---

# Google Sheets Mapping Agent

Build an agent that **maps** and **works directly on** Google Sheets: map structure (read) and edit/append/update (write) via the Sheets API. Output is a structured map plus code or scripts that get/push data.

## When to Use This Skill

- User asks to map Google Sheets, Admin Sheet, or CRM_Operativo.
- User asks to **work directly on the sheet** (map, edit, read, push).
- Defining or documenting which sheets/columns the system reads from or writes to.
- Adding a new sheet/tab or new API endpoints that read/write Sheets.
- Auditing or documenting data flow: Sheets ↔ API / app.

## Mapping Output Structure

Produce a mapping document that includes:

1. **Sheet inventory** — All relevant tabs (e.g. `CRM_Operativo`, `Parametros`, `Dashboard`, `Data Base`).
2. **Data types and typical values** — Per sheet: identifiers, dates, contact info, categorical (dropdowns), calculated metrics. Include formats (e.g. YYYY-MM-DD) and allowed values.
3. **Relationships and lookups** — Which sheet feeds dropdowns (e.g. `Parametros` → validation lists), which sheet is source for dashboards, backup/mirror sheets.
4. **Calculation logic and automatisms** — ID generation, scoring formulas, priority/alert rules, aggregations (COUNTIFS/SUMIFS). Document formula intent, not only syntax.
5. **Get/Push contract** — Which ranges or columns the system **reads** (GET) and which it **writes** (PUSH); any sync or trigger assumptions.

Use the **Admin Sheet (CRM_Operativo)** example in [reference.md](reference.md) as the canonical template. Adapt names and columns to the target workbook.

## Canonical repo docs (always align with code)

Before proposing column/tab names, read:

- `docs/google-sheets-module/MAPPER-PRECISO-PLANILLAS-CODIGO.md` — **runtime** mapping from `server/routes/bmcDashboard.js`
- `docs/google-sheets-module/SYNC-FULL-TEAM-SHEETS-ACCESS-MAP.md` — which surface calls which API
- `docs/google-sheets-module/planilla-inventory.md` — workbook inventory

Do not invent alternate “official” mapping paths outside these files unless the user explicitly wants a new doc.

## Workflow

1. **Before working:** Read `docs/team/PROJECT-STATE.md` (cambios recientes, pendientes).
2. **Gather** — List sheet names and any existing docs or code that read/write Sheets (e.g. `bmcDashboard.js`, Apps Script, env `BMC_SHEET_ID`).
3. **Inspect** — For each sheet: column headers, sample values, data validation (dropdowns), and formulas in key cells. Prefer one sheet per section.
4. **Document** — Fill the structure above. Use tables for columns (name, type, source/validation, formula/notes).
5. **Get/Push** — Explicitly state: "System GETs: …" and "System PUSHes: …" (ranges, columns, or row append behavior).

## Conventions

- **Identifiers**: Prefer one auto-generated ID per row (e.g. `ROW()-3`); document in "Calculation logic".
- **Dates**: Use ISO date (YYYY-MM-DD) in the map; note if the sheet uses another format for display.
- **Categorical**: List allowed values and the sheet that provides them (e.g. `Parametros`).
- **Calculated fields**: Name the formula purpose (e.g. "Scoring Engine", "Alert System"); keep formula details in reference.md if long.

## Optional Artifacts

- **Schema JSON** — If the codebase expects a schema (e.g. `BMC_SHEET_SCHEMA`), emit a minimal JSON or reference that matches the map.
- **Validation list source** — Table: Column → Parametros range or static list.

## Working Directly on the Sheet (Map, Edit, Read, Push)

The agent does **not** open the Sheet in a browser; it uses the **Sheets API** via backend code or runnable scripts.

- **Map (read)**  
  - Use existing routes: `GET /api/cotizaciones`, `GET /api/proximas-entregas`, `GET /api/pagos-pendientes`, etc. (see `server/routes/bmcDashboard.js`).  
  - Or add a one-off script/route that calls `getSheetData(sheetId, sheetName, ...)` (or `sheets.spreadsheets.values.get`) with the project’s service account (`GOOGLE_APPLICATION_CREDENTIALS`, `BMC_SHEET_ID`) to dump headers + sample rows and infer the map.

- **Edit (write)**  
  - **Append rows**: Same pattern as `handleMarcarEntregado` in `bmcDashboard.js`: `sheets.spreadsheets.values.append` with `range`, `valueInputOption: "USER_ENTERED"`, `requestBody: { values: [row] }`.  
  - **Update cells**: `sheets.spreadsheets.values.update` for a range; or `sheets.spreadsheets.batchUpdate` for delete/move/format.  
  - The agent **implements or extends** `server/routes/bmcDashboard.js` (new route or new handler) or provides a **script** (Node or Python) that uses the same credentials and performs the update. User (or CI) runs the server or script; the agent does not execute live edits itself.

- **Flow**  
  1. Document the map (sheet names, columns, types, GET/PUSH contract) per [reference.md](reference.md).  
  2. For **read**: call existing GET endpoints or add a small script that uses `getSheetData`/values.get.  
  3. For **write**: add a POST route or script that uses values.append / values.update / batchUpdate; ensure `BMC_SHEET_ID` and service account are configured.

## Reference

- Full Admin Sheet (CRM_Operativo) example and Get/Push contract: [reference.md](reference.md).
- Backend read/write implementation: `server/routes/bmcDashboard.js` (`getSheetData`, `handleMarcarEntregado`, values.get, values.append, batchUpdate).
