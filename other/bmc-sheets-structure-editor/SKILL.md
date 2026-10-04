---
name: bmc-sheets-structure-editor
description: >
  Restricted skill for full Google Sheets editing from Cursor only: create
  tabs, dropdown menus (data validation), rows/columns/charts, read automation
  and guides, and customize sheet workflow. Only Matias may perform these
  edits. Use when Matias asks for tabs, drop menus, automation/guides, or
  workflow customization of the BMC sheet.
---

# BMC Sheets Structure Editor (Matias only)

**Before working:** Read `docs/team/knowledge/SheetsStructure.md` if it exists.

**Restriction:** This skill is **only for Matias**. Only Matias may perform structure edits (create tabs, edit rows/columns/charts, etc.). **Only through this Cursor workspace** — not via other tools or by other team members. The Development Team does **not** use this skill to edit the workbook; only Matias does, and only from Cursor.

## When to Use

- Matias asks to **create tabs** (new sheets) in the BMC workbook.
- Matias asks for **dropdown menus** (data validation) — from Parametros or a static list.
- Matias asks to **read automation and guides** (document triggers, formulas, data flow); then design or implement changes.
- Matias asks to **customize workflow** of the sheet (what flows where, when to update, validations, new steps).
- Matias asks to **edit rows, columns**, add/delete dimensions, or bulk-update cells.
- Matias asks to **add or edit charts** in a sheet.
- Matias asks for **any structural or content creation** in the linked Google Sheet (tabs, headers, data validation, formatting, etc.).

If the request comes from someone other than Matias, or outside this Cursor workspace context, do **not** apply structure-editing actions; suggest they contact Matias or use read-only/mapping flows instead.

## Scope of Edits

The agent may **propose or generate** code/scripts that perform:

- **Tabs**: Create new sheets (`addSheet`), delete sheets (`deleteSheet`), rename (`updateSheetProperties`).
- **Rows / columns**: Insert or delete (`insertDimension`, `deleteDimension`), resize.
- **Cells**: Update values or formulas (`values.update`, `values.append`), clear ranges.
- **Charts**: Add or update embedded charts (`addChart`, `updateChartSpec`).
- **Dropdown menus (data validation)**: Set or update validation on a range (list from **Parametros** sheet or static values). See [reference.md](reference.md) § Data validation.
- **Other**: Conditional format, frozen rows/columns, merges — via `batchUpdate` requests.

All edits go through the **Sheets API** (e.g. `server/routes/bmcDashboard.js` pattern: same `spreadsheetId`, same auth). Execution is by **Matias** running the server or script in this workspace (e.g. Cursor terminal).

## Workflow

1. **Confirm context**: Edits are for the BMC workbook, from Cursor, by Matias.
2. **Choose operations**: From [reference.md](reference.md) — e.g. `AddSheet`, `InsertDimension`, `DeleteDimension`, `UpdateCells`, `AddChart`, etc.
3. **Implement**: Add a route in `server/routes/bmcDashboard.js` or a standalone script under `.cursor/skills/bmc-sheets-structure-editor/scripts/` that:
   - Uses `BMC_SHEET_ID` and `GOOGLE_APPLICATION_CREDENTIALS` (same as existing dashboard).
   - Calls `google.sheets({ version: "v4", auth }).spreadsheets.batchUpdate` and/or `values.update` / `values.append` as needed.
4. **No auto-run**: The agent does not execute edits; it produces code. Matias runs the server or script and verifies in the Sheet.

## Conventions

- **Workbook**: The target is the spreadsheet identified by `BMC_SHEET_ID` in config/env.
- **Auth**: Same as `bmcDashboard.js` — `GoogleAuth` with `GOOGLE_APPLICATION_CREDENTIALS`, scope `https://www.googleapis.com/auth/spreadsheets` for write.
- **Idempotency**: Prefer non-destructive ops or clear warnings (e.g. "this will delete sheet X"); avoid blind overwrites of production data.

## Automation, guides, and workflow

- **Read automation**: Use the **mapping agent** (`.cursor/skills/google-sheets-mapping-agent/`) to document existing automation (e.g. formulas, Apps Script triggers if documented in repo). Guides live in `.cursor/SETUP DASHBOARD /README.md` and `docs/bmc-dashboard-modernization/`. The structure editor then implements changes (e.g. new validation, new tab) that align with that automation.
- **Workflow customization**: (1) Map current flow (Parametros → CRM_Operativo → Dashboard, GET/PUSH). (2) Define desired flow (new steps, validations, tabs). (3) Implement via this skill: new tabs, dropdowns, formulas, or routes that read/write the sheet. Optionally add a short “Workflow” section to the mapping doc (e.g. in `reference.md` of the mapping agent) describing the customized flow.

## Reference

- Sheets API structure operations (addSheet, insertDimension, deleteDimension, addChart, **data validation**, etc.): [reference.md](reference.md).
