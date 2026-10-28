---
name: exporting-to-google-sheets
description: Push a lead list into a Google Sheet, or read one back. Optional — CSV is the default output and needs no setup. Use only when the user explicitly asks for Google Sheets, a shared spreadsheet, or their team needing live access.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Exporting to Google Sheets

## Read this first
**You almost certainly don't need this.** Every script in this repo writes CSV, which opens in Excel, Numbers, and Google Sheets alike. Google Sheets means a Google Cloud project, an OAuth consent screen, and a `credentials.json` — the single biggest place beginners get stuck.

Only set it up when the user has said they want it: a shared sheet the team edits live, or an existing sheet they're appending to.

## Setup
Full walkthrough: `docs/GOOGLE_SHEETS_SETUP.md`. Short version:

1. console.cloud.google.com → new project
2. Enable the Google Sheets API and the Google Drive API
3. Credentials → OAuth client ID → Desktop app → download JSON
4. Save it as `credentials.json` in the repo root
5. First run opens a browser to authorize, then writes `token.json`

Both files are gitignored. Never commit them.

## Use

```bash
# Scrape straight into a sheet
python -X utf8 scripts/02_local_businesses/gmaps_lead_pipeline.py \
    --search "barbers in Tuscaloosa AL" --limit 25 \
    --sheet-url "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID"

# Push an existing file
python -X utf8 scripts/common/update_sheet.py --input output/leads.csv --sheet-url "https://..."

# Read a sheet back
python -X utf8 scripts/common/read_sheet.py --sheet-url "https://..."
```

Omit `--sheet-url` and nothing Google-related is touched — no browser, no credentials needed.

## Edge cases
- **Browser opens every run** — delete `token.json` and re-authorize once; it's expired or scoped wrong.
- **"credentials.json not found"** — it goes in the repo root, not in `scripts/`.
- **403 on an existing sheet** — the Google account you authorized doesn't have edit access to it.
- **Duplicate rows** — the pipeline dedupes on `lead_id`. Rows added by hand won't have one.
- **Quota errors on big lists** — Sheets rate-limits writes. Under a few thousand rows, prefer CSV.
