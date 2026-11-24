---
name: google-sheets
description: This skill should be used when the user asks to read, create, or edit Google Sheets spreadsheets, or manage cell data through the Google Sheets API.
version: 1.1.0
---

# Google Sheets

Read, create, and edit Google Sheets using the Sheets API v4 with a selected Google account.

**IMPORTANT: User approval required for all writes.** Before any create, update, append, or batch update action, show the planned content first and wait for explicit `take off` approval. Do not mutate anything before that approval.

## Configuration

The shared Google credential configuration is defined once in the **google-oauth** skill: `skills/google-oauth/SKILL.md`.

## API Reference

Send every Google API request through `charliebot google request`.
The command mints the selected account's access token inside its own process, so the token never appears in a command, in the output or in a run record.
A JSON body goes in `--json`, which sets `Content-Type: application/json`; `--data-file <path>` reads the body from a file instead.
The command prints the response body on stdout and exits 0 for an HTTP 2xx answer; another status exits 1.

### Choose the Account

Choose the account using the **Accounts** section in the **google-oauth** skill.
Pass `--account <name>` on every request, and omit `--account` for the default account.

If the refresh token is invalid or revoked, follow **Add or Re-Authorize an Account** in the **google-oauth** skill: `skills/google-oauth/SKILL.md`.

### Create a Spreadsheet

```bash
charliebot google request POST https://sheets.googleapis.com/v4/spreadsheets --json '{"properties":{"title":"Spreadsheet Title"}}'
```

After a successful create, return the editor URL:

`https://docs.google.com/spreadsheets/d/{spreadsheetId}/edit`

### Read Spreadsheet Metadata

```bash
charliebot google request GET "https://sheets.googleapis.com/v4/spreadsheets/SPREADSHEET_ID"
```

Returns spreadsheet properties, sheet names, grid dimensions, and other metadata. To list only sheet titles, inspect `sheets[].properties.title` in the response.

### Read Values

```bash
charliebot google request GET "https://sheets.googleapis.com/v4/spreadsheets/SPREADSHEET_ID/values/RANGE"
```

`RANGE` uses A1 notation, e.g. `Sheet1!A1:D10` or `Sheet1!A:A`. The response contains a `values` array of rows.

### Write Values

```bash
charliebot google request PUT "https://sheets.googleapis.com/v4/spreadsheets/SPREADSHEET_ID/values/RANGE?valueInputOption=USER_ENTERED" \
  --json '{"range":"RANGE","majorDimension":"ROWS","values":[["A1 value","B1 value"],["A2 value","B2 value"]]}'
```

`valueInputOption=USER_ENTERED` parses values as if typed into the UI (numbers, dates, formulas are interpreted). Use `RAW` to store literal strings.

### Append Values

```bash
charliebot google request POST "https://sheets.googleapis.com/v4/spreadsheets/SPREADSHEET_ID/values/RANGE:append?valueInputOption=USER_ENTERED" \
  --json '{"range":"RANGE","majorDimension":"ROWS","values":[["A value","B value"]]}'
```

Appends rows after the last row with data in the specified range. The `RANGE` determines which table to append to (e.g. `Sheet1!A:B`).

### Batch Update

Use `spreadsheets.batchUpdate` for structural changes (add/delete sheets, formatting, merge cells, resize, conditional formatting, etc.):

```bash
charliebot google request POST "https://sheets.googleapis.com/v4/spreadsheets/SPREADSHEET_ID:batchUpdate" \
  --json '{"requests":[{"addSheet":{"properties":{"title":"New Sheet"}}}]}'
```

Common request types: `addSheet`, `deleteSheet`, `updateSheetProperties`, `mergeCells`, `repeatCell` (for formatting), `autoResizeDimensions`, `addConditionalFormatRule`.

## Bootstrap / Re-Authorization

Choose an account in the **Accounts** section and follow **Add or Re-Authorize an Account** in the **google-oauth** skill: `skills/google-oauth/SKILL.md`.
