---
name: google-drive-file-processor
description: Workflow and ready-to-import helpers for connecting to Google Drive with a service account, listing folders, and routing files based on MIME type. Use this skill whenever you need to download/export Docs, Sheets, Slides, Forms, or arbitrary binaries and surface their contents as pandas tables or local artifacts.
---

# Google Drive File Processor

Codex already knows the Google APIs exist; what it needs is a self-contained replica of the OpsDashboard helpers. Copying this skill directory into any project gives you `references/google_drive_processing_example.py`, which contains production-ready helpers (`build_drive_clients`, `process_drive_file`, `process_drive_folder`, `fetch_sheet_tables`, etc.) that require only a service-account JSON blob.

## Authentication & secrets
- Store the full service account JSON (plus `folder_id`) under `st.secrets["gdrive_secrets"]` or load it from disk and pass the dict directly to `build_drive_clients`.
- Always request the read-only scopes used here:  
  `https://www.googleapis.com/auth/drive.readonly`, `https://www.googleapis.com/auth/spreadsheets.readonly`, `https://www.googleapis.com/auth/presentations.readonly`.
- Build clients with `service_account.Credentials.from_service_account_info(..., scopes=SCOPES)` and `googleapiclient.discovery.build`.

## Folder listing pattern
1. Pull `folder_id` from the secret, defaulting to whole Drive when missing.
2. Compose the Drive query (`"'<folder_id>' in parents"` plus MIME filters when needed). `src/show_sheet_explorer._fetch_sheet_metadata` shows the paging pattern when you need more than 200 files.
3. Call `drive.files().list(..., includeItemsFromAllDrives=True, supportsAllDrives=True)` and capture `id`, `name`, and `mimeType`.

## MIME routing matrix
Re-use the handlers implemented inside `references/google_drive_processing_example.py`:

| MIME | Handler | Result |
| --- | --- | --- |
| `application/vnd.google-apps.spreadsheet` | `read_google_sheet` + `sheet_rows_to_dataframe` | Dict of tab -> rows/DataFrames |
| `application/vnd.google-apps.presentation` | `read_google_slides` | Returns ordered text snippets |
| `application/vnd.google-apps.document` | `export_google_file(..., target_mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document', suffix='docx')` | Saves `.docx` |
| `application/vnd.google-apps.form` | Emits warning; Drive cannot export responses | None |
| Other `application/vnd.google-apps.*` | `export_google_file(..., target_mime='application/pdf', suffix='pdf')` | Saves `.pdf` |
| Everything else (PPTX, XLSX, PDF, etc.) | `save_binary_file` | Saves raw bytes |

`process_drive_file(...)` already contains this matrix and returns a `dict` describing the work performed (artifact path + metadata). Re-use it instead of re-implementing the branching logic.

## Recommended workflow
1. Build Drive/Sheets/Slides clients once per request and pass them into helpers; cache expensive sheet reads with `@st.cache_data(ttl=3600)` if the UI displays them repeatedly.
2. Iterate files, call the right handler, and collect structured outputs (dataframes, exported files). Persist exports on disk or keep them in memory (BytesIO) before attaching to downstream tasks.
3. When surfacing in Streamlit, expose controls to refresh the cache, filter by sheet name, and show links using `st.data_editor` (see `show_sheet_explorer` for pattern).

## Example resources
- `references/google_drive_processing_example.py` exposes reusable helpers plus `process_drive_folder(...)` and `fetch_sheet_tables(...)`. Import it directly or execute it as a module to download/export folders in other projects—no OpsDashboard dependencies remain.
