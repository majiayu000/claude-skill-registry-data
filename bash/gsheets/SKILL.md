---
name: gsheets
category: productivity
description: Read, write, format, and manage Google Sheets. Use when the user shares a sheets.google.com or docs.google.com/spreadsheets URL, asks to read or summarize spreadsheet data, wants cells written, formatted, sorted, merged, or validated, wants rows/columns inserted or deleted, wants charts, pivot tables, or tables added, wants CSV imported, or wants a spreadsheet created, copied, shared, or exported. Don't use for Google Docs, Slides, or Drive file management.
---

# Google Sheets

Work with a Google Sheet the user names or links to. Everything here assumes you
already have the **spreadsheet ID** — the segment between `/d/` and `/edit` in a
`https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit` URL.

> [!CAUTION]
>
> `mutate delete-sheet`, `mutate delete-rows`, `mutate delete-cols`, and `mutate
> clear` permanently remove data. **Never** run a destructive command the user
> did not explicitly ask for.
>
> `mutate delete` permanently deletes an entire spreadsheet document. Never use
> it unless the user asks explicitly; ask for confirmation and wait for the
> answer before executing. The command also requires `--confirm`.
>
> **Never** share a spreadsheet with a broad audience, a public link, or a whole
> organization. The user already has access to anything created on their behalf
> — let them handle sharing unless they explicitly instruct otherwise.

## Setup and Authentication

`gsheets auth status` is the only way to tell whether you are logged in. Do not
run `--help`, search the filesystem or environment for tokens, check another
plugin's login, or run an operational command before logging in. Follow these
steps exactly.

**1. Register and check.** Run this skill's script with `auth status`. It
downloads the CLI, registers `gsheets` on the agent's `PATH` (not the user's
shell), and reports whether you are logged in:

```bash
<path/to/this/skill>/scripts/gsheets auth status
```

```powershell
# Windows (PowerShell)
& "<path\to\this\skill>\scripts\gsheets.cmd" auth status
```

Every later call is just `gsheets`. Never ask the user to run it; they cannot.
If it reports `Logged in`, you are ready.

**2. Log in for the user.** Start this as a background command:

```bash
gsheets auth login
```

It prints an authorization URL and exits on its own once the user approves. Read
the URL from the task's log, open it in the user's browser or hand them the
link, then stop and wait. Confirm with `gsheets auth status`.

## Usage

Do every Google Sheets operation — reading, writing, formatting, creating,
exporting — through `gsheets`. Commands are split into two namespaces:
`readonly` for anything that only reads, `mutate` for anything that changes the
spreadsheet. Run `gsheets --help`, or `gsheets <namespace> <command> --help`, to
confirm the exact flags of any command below.

Two rules the CLI's own help will not tell you:

-   **Never run a destructive command the user did not ask for.** Deleting a
    spreadsheet, a sheet, or rows, and clearing a range, all discard data with
    no undo on the user's side. Ask first and wait for an answer.
-   **Write the narrowest range that does the job.** Rewriting a whole sheet to
    change a few cells destroys formatting, formulas, and validation rules that
    were never yours to touch.

## Recipes

**Read data (readonly):**

```bash
gsheets readonly read SPREADSHEET_ID 'Sheet1!A1:D10'
gsheets readonly read-all SPREADSHEET_ID
gsheets readonly read-links SPREADSHEET_ID 'Sheet1!A1:D10'   # embedded hyperlinks, rich-text links, and smart chips
gsheets readonly info SPREADSHEET_ID
gsheets readonly list-sheets SPREADSHEET_ID
gsheets readonly list-named-ranges SPREADSHEET_ID
gsheets readonly list-filter-views SPREADSHEET_ID
gsheets readonly list "Quarterly Results"                    # search spreadsheets in Drive
gsheets readonly list-revisions SPREADSHEET_ID               # revision history
gsheets readonly inspect-cell SPREADSHEET_ID 'Sheet1!B4'     # deep cell and error diagnostics
gsheets readonly get-settings SPREADSHEET_ID                 # locale and timezone properties
gsheets readonly list-comments SPREADSHEET_ID                # comment threads and replies
```

**Write data (mutate):**

```bash
gsheets mutate write SPREADSHEET_ID 'Sheet1!A1:B2' "Name,Age|Alice,30"
gsheets mutate write SPREADSHEET_ID 'Sheet1!A1:B2' $'Name,Age\nAlice,30'
gsheets mutate write SPREADSHEET_ID 'Sheet1!A1' "Value with\, a comma"
gsheets mutate append SPREADSHEET_ID 'Sheet1!A1' "Bob,25"
gsheets mutate clear SPREADSHEET_ID 'Sheet1!A1:D10'
gsheets mutate import-csv SPREADSHEET_ID /path/to/data.csv
gsheets mutate find-replace SPREADSHEET_ID --find "old" --replace "new"
gsheets mutate notes SPREADSHEET_ID 'Sheet1!A1' "This is a note"
gsheets mutate add-comment SPREADSHEET_ID "This is a comment" --range 'Sheet1!A1:A1'
gsheets mutate reply-comment SPREADSHEET_ID COMMENT_ID "This is a reply"
gsheets mutate resolve-comment SPREADSHEET_ID COMMENT_ID "Optional resolve message"
```

**Create, delete, copy, and rename (mutate):**

```bash
gsheets mutate create --title "New Spreadsheet"
gsheets mutate delete SPREADSHEET_ID --confirm                       # permanently deletes the document
gsheets mutate rename SPREADSHEET_ID "New File Name"
gsheets mutate copy-spreadsheet SPREADSHEET_ID "Copy Title"
gsheets mutate add-sheet SPREADSHEET_ID --title "Sheet2"
gsheets mutate delete-sheet SPREADSHEET_ID --sheet-id 1
gsheets mutate rename-sheet SPREADSHEET_ID --sheet-id 0 --title "Main"
gsheets mutate copy-sheet SPREADSHEET_ID --sheet-id 0 --dest OTHER_SPREADSHEET_ID
gsheets mutate create-from-template TEMPLATE_ID --title "New" --replacements "{{NAME}}=Alice"
```

**Formatting (mutate):**

```bash
gsheets mutate format SPREADSHEET_ID --sheet-id 0 --start-row 0 --end-row 1 --start-col 0 --end-col 5 --bold --align CENTER --bg-color "#00FF00" --fg-color "#FF0000" --wrap
gsheets mutate set-col-width SPREADSHEET_ID --sheet-id 0 --start-col 0 --end-col 1 --pixels 200
gsheets mutate autosize SPREADSHEET_ID --sheet-id 0 --start-col 0 --end-col 5
gsheets mutate merge SPREADSHEET_ID --sheet-id 0 --start-row 0 --end-row 1 --start-col 0 --end-col 3
gsheets mutate unmerge SPREADSHEET_ID --sheet-id 0 --start-row 0 --end-row 1 --start-col 0 --end-col 3
gsheets mutate freeze SPREADSHEET_ID --sheet-id 0 --rows 1 --cols 1
gsheets mutate borders SPREADSHEET_ID --sheet-id 0 --style SOLID --color "#000000"
gsheets mutate conditional-format SPREADSHEET_ID --sheet-id 0 --start-row 0 --end-row 100 --start-col 0 --end-col 1 --condition NUMBER_GREATER --value "90" --color "#00FF00"
```

**Rows, columns, and data operations (mutate):**

```bash
gsheets mutate sort SPREADSHEET_ID --sheet-id 0 --col 0                 # --asc is default, omit for descending
gsheets mutate insert-rows SPREADSHEET_ID --range 'Sheet1!5:10'         # human-readable ranges work
gsheets mutate delete-rows SPREADSHEET_ID --range 'Sheet1!5:10'
gsheets mutate insert-cols SPREADSHEET_ID --range 'Sheet1!C:D'
gsheets mutate insert-cols SPREADSHEET_ID --sheet-id 0 --start 2 --count 3 --inherit-from-before   # append at the end (start may equal grid size)
gsheets mutate delete-cols SPREADSHEET_ID --range 'Sheet1!C:D'
gsheets mutate copy-paste SPREADSHEET_ID --sheet-id 0 --start-row 0 --end-row 5 --start-col 0 --end-col 2 --dest-row 0 --dest-col 3 --paste-type PASTE_VALUES
gsheets mutate auto-fill SPREADSHEET_ID --sheet-id 0 --start-row 0 --end-row 10 --start-col 0 --end-col 1 --source-end-row 3
gsheets mutate smart-fill SPREADSHEET_ID 'Sheet1!B2'                    # fills down the adjacent contiguous depth
gsheets mutate formula-fill SPREADSHEET_ID --range 'Sheet1!C1:C10' --formula "=B1+A1"   # shifts relative references
gsheets mutate data-validation SPREADSHEET_ID 'Sheet1!B1:B10' --values "Yes,No,Maybe"
gsheets mutate protect SPREADSHEET_ID --range 'Sheet1!A1:D1' --editors "alice@example.com,bob@example.com"
gsheets mutate change-settings SPREADSHEET_ID --locale "de_DE" --timezone "Europe/Berlin"
gsheets mutate add-named-range SPREADSHEET_ID "MyRange" 'Sheet1!A1:D10'
gsheets mutate add-filter-view SPREADSHEET_ID "MyFilter" --sheet-id 0
gsheets mutate delete-filter-view SPREADSHEET_ID 12345
```

**Charts, pivots, tables, sharing, and export:**

```bash
gsheets mutate add-chart SPREADSHEET_ID --sheet-id 0 --chart-type BAR --start-row 0 --end-row 10 --start-col 0 --end-col 2 --title "Sales"
gsheets mutate add-chart SPREADSHEET_ID --sheet-id 0 --chart-type COLUMN --start-row 0 --end-row 10 --start-col 0 --end-col 2 --title "Pillars" --overlay --colors "#4285F4,#EA4335"
gsheets readonly export-chart SPREADSHEET_ID --chart-id 1 --output /tmp/chart.png
gsheets mutate pivot SPREADSHEET_ID --source 'Sheet1!A1:D100' --target-sheet-id 0
gsheets readonly export SPREADSHEET_ID /tmp/export.csv --format csv
gsheets readonly export SPREADSHEET_ID /tmp/export_tab.csv --format csv --sheet "Sheet2"   # specific tab (CSV/TSV only)
gsheets readonly export SPREADSHEET_ID /tmp/page1.png --format png --page 1
gsheets mutate share SPREADSHEET_ID --email user@example.com --role writer
gsheets mutate add-table SPREADSHEET_ID "MyTable" 'Sheet1!A1:D10'
gsheets mutate update-table SPREADSHEET_ID "MyTable" 'Sheet1!A1:D20'
gsheets mutate delete-table SPREADSHEET_ID "MyTable"
gsheets mutate batch SPREADSHEET_ID -f requests.json
gsheets mutate raw-batch SPREADSHEET_ID -f raw_requests.json
```

**Batch operations file (`requests.json`):**

Each op is one of `read`, `write`, `append`, or `clear`. For `write` and
`append`, the `data` field is **required** and must be a 2D array of rows
(`[[...]]`). Unknown JSON fields are rejected — typos surface immediately rather
than silently producing no-op writes.

```json
[
  {"op": "read",   "range": "Sheet1!A1:B2"},
  {"op": "write",  "range": "Sheet1!A1",     "data": [["Critical", "High"]]},
  {"op": "append", "range": "Sheet1!A1",     "data": [["new row"]]},
  {"op": "clear",  "range": "Sheet1!A1:B2"}
]
```

> [!IMPORTANT]
>
> The field is `data`, not `values`. Writing `"values": "X"` fails with `parsing
> batch JSON: json: unknown field "values"`. This is deliberate: the field name
> that used to be silently accepted was a silent-data-loss footgun.

## Commands

| Namespace  | Command                | Description                     |
| ---------- | ---------------------- | ------------------------------- |
| `readonly` | `read`                 | Read range                      |
| `readonly` | `read-all`             | Read all sheets                 |
| `readonly` | `read-links`           | Extract hyperlinks, rich text,  |
:            :                        : and smart chips                 :
| `readonly` | `info`                 | Spreadsheet info                |
| `readonly` | `list`                 | List or search spreadsheets in  |
:            :                        : Drive                           :
| `readonly` | `list-revisions`       | List spreadsheet revision       |
:            :                        : history                         :
| `readonly` | `list-sheets`          | List sheets                     |
| `readonly` | `list-named-ranges`    | List named ranges               |
| `readonly` | `list-filter-views`    | List filter views               |
| `readonly` | `list-comments`        | List comment threads            |
| `readonly` | `get-settings`         | View locale and timezone        |
:            :                        : properties                      :
| `readonly` | `inspect-cell`         | Detailed cell diagnostics       |
:            :                        : (values, formulas, errors)      :
| `readonly` | `export`               | Export spreadsheet (csv, xlsx,  |
:            :                        : pdf, ods, tsv, png)             :
| `readonly` | `export-chart`         | Export chart as image           |
| `mutate`   | `write`                | Write to range                  |
| `mutate`   | `append`               | Append rows                     |
| `mutate`   | `clear`                | Clear range                     |
| `mutate`   | `create`               | Create spreadsheet              |
| `mutate`   | `delete`               | Permanently delete spreadsheet  |
:            :                        : document (`--confirm`)          :
| `mutate`   | `rename`               | Rename spreadsheet document     |
:            :                        : file                            :
| `mutate`   | `copy-spreadsheet`     | Copy entire spreadsheet         |
| `mutate`   | `add-sheet`            | Add sheet                       |
| `mutate`   | `delete-sheet`         | Delete sheet                    |
| `mutate`   | `rename-sheet`         | Rename sheet                    |
| `mutate`   | `copy-sheet`           | Copy sheet to another           |
:            :                        : spreadsheet                     :
| `mutate`   | `format`               | Format range (hex background    |
:            :                        : and text colors)                :
| `mutate`   | `set-col-width`        | Set column width                |
| `mutate`   | `autosize`             | Auto-resize columns             |
| `mutate`   | `merge`                | Merge cells                     |
| `mutate`   | `unmerge`              | Unmerge cells                   |
| `mutate`   | `sort`                 | Sort range                      |
| `mutate`   | `freeze`               | Freeze rows/cols                |
| `mutate`   | `borders`              | Set cell borders (hex color)    |
| `mutate`   | `conditional-format`   | Add conditional formatting      |
| `mutate`   | `insert-rows`          | Insert rows (range or manual    |
:            :                        : offsets)                        :
| `mutate`   | `delete-rows`          | Delete rows (range or manual    |
:            :                        : offsets)                        :
| `mutate`   | `insert-cols`          | Insert columns (range or manual |
:            :                        : offsets)                        :
| `mutate`   | `delete-cols`          | Delete columns (range or manual |
:            :                        : offsets)                        :
| `mutate`   | `copy-paste`           | Copy-paste range (supports      |
:            :                        : paste-type)                     :
| `mutate`   | `auto-fill`            | Auto-fill range (manual         |
:            :                        : coordinates)                    :
| `mutate`   | `smart-fill`           | Auto-fill down, detecting       |
:            :                        : contiguous depth                :
| `mutate`   | `formula-fill`         | Fill formula across range       |
:            :                        : (shifts relative refs)          :
| `mutate`   | `find-replace`         | Find and replace                |
| `mutate`   | `notes`                | Get/set cell notes              |
| `mutate`   | `add-named-range`      | Add a named range               |
| `mutate`   | `import-csv`           | Import CSV file                 |
| `mutate`   | `data-validation`      | Add data validation             |
| `mutate`   | `protect`              | Protect range (range and        |
:            :                        : restricted editors)             :
| `mutate`   | `change-settings`      | Update locale and timezone      |
:            :                        : properties                      :
| `mutate`   | `add-chart`            | Add a chart                     |
| `mutate`   | `add-filter-view`      | Add a filter view               |
| `mutate`   | `delete-filter-view`   | Delete filter view by ID        |
| `mutate`   | `pivot`                | Create pivot table              |
| `mutate`   | `share`                | Share spreadsheet               |
| `mutate`   | `create-from-template` | Create from template            |
| `mutate`   | `add-table`            | Add a structured table          |
| `mutate`   | `update-table`         | Update structured table range   |
| `mutate`   | `delete-table`         | Delete a structured table       |
| `mutate`   | `batch`                | Execute simplified batch        |
:            :                        : operations                      :
| `mutate`   | `raw-batch`            | Execute raw                     |
:            :                        : `BatchUpdateSpreadsheetRequest` :
| `mutate`   | `add-comment`          | Add a comment                   |
| `mutate`   | `reply-comment`        | Reply to a comment              |
| `mutate`   | `resolve-comment`      | Resolve a comment               |

## Tips

-   **Creating Spreadsheets with Specific Tabs:** When creating a new
    spreadsheet with a specific tab/sheet name, note that `mutate create`
    generates a default initial tab ("Sheet 1", `--sheet-id 0`). You can either
    repurpose "Sheet 1" by renaming it (`mutate rename-sheet SPREADSHEET_ID
    --sheet-id 0 --title "Desired Tab Name"`) or add the new sheet and delete
    "Sheet 1" (`mutate delete-sheet SPREADSHEET_ID --sheet-id 0`).
-   **CRITICAL:** Never attempt to scrape Google Sheets URLs (e.g.,
    `docs.google.com/spreadsheets/...`) using web reading tools. Always use the
    GSheets CLI commands (`readonly read`, `readonly read-all`) to access
    spreadsheet contents, as the URLs require authentication and will return
    permission errors.
-   **LIMITATION:** Due to Google Sheets API and Drive API limitations, any
    comment created programmatically using `mutate add-comment` with a cell
    range anchor will appear as "Original Content Deleted" (unanchored) in the
    Google Sheets grid Web UI. However, the comment remains fully visible in the
    Sheets "Comment History" sidebar, and it is queryable/writable via the CLI's
    `list-comments`, `reply-comment`, and `resolve-comment` commands.
-   The `mutate format` command uses `--sheet-id`, `--start-row/--end-row`,
    `--start-col/--end-col` (not A1 range notation)
-   The `mutate notes` command takes range and note text as positional arguments
    (not --set flag)
-   Avoid spaces in sheet names when used in range notation; if unavoidable,
    wrap in single quotes: `"'My Sheet'!A1:B5"`
-   Chart types: `BAR`, `LINE`, `AREA` work reliably; `PIE` is listed but not
    supported by the API
-   Use `--json` on read commands to get machine-parseable output
-   Use `--markdown-links` on `readonly read-all` to extract rich-text
    hyperlinks and Smart Chips (Rich Links and People Chips) embedded in cells.
    Without this flag, the API returns only the display text, and hidden link
    targets or smart chip URIs are lost. With the flag, both standard links and
    smart chips (including People Chips as `mailto:` links) are rendered as
    `[display text](URL)`. Can be combined with `--json` to output an array of
    rows containing the markdown-formatted strings.
-   `readonly read-links RANGE` is the dedicated command (vs the
    `--markdown-links` flag above, which is scoped to `read-all`) to pull
    embedded hyperlinks, rich-text links, and Smart Chips (Rich Links and People
    Chips as `mailto:` links) from a specific range, rendered as `[display
    text](URL)`. Add `--json` for an array of rows, or `--debug-cell` to dump
    the raw `CellData` JSON for troubleshooting.
-   Use `--value-render-option FORMULA` on the `readonly read` command to
    retrieve the underlying cell formulas instead of the evaluated values.
-   `readonly export` supports `csv`, `xlsx`, `pdf`, `ods`, `tsv`, and `png`
    formats. When exporting to `csv` or `tsv`, you can use the `--sheet
    "TabName"` flag to export a specific sheet tab by name (by default, Drive
    CSV export only downloads the first tab).
-   Both `|` and `\n` (newline) work as row delimiters in `mutate write` and
    `mutate append` commands. Use `|` for inline values and `$'\n'` for
    multi-row shell input
-   To include a comma inside a cell value, escape it with a backslash: `\,`
-   `batch` requires `data` (not `values`) for `write`/`append` ops; unknown
    fields are rejected by the strict JSON decoder. See "Batch operations file"
    above.
-   `conditional-format --condition NUMBER_BETWEEN` (and `NUMBER_NOT_BETWEEN`,
    `DATE_BETWEEN`, `DATE_NOT_BETWEEN`) accept a comma-separated `--value` pair,
    e.g. `--value "1,10"`. Other conditions still take a single `--value`. For
    bands of multiple ranges (e.g. 1-2, 3-5, 6+), add one rule per band.
-   **Recommended workflow:** Use `readonly export SPREADSHEET_ID page.png
    --format png --page N` to export a specific page as an image, review it
    visually, then iterate on edits

## Global Flags

-   `--json` — output as JSON (works with all read commands)
-   `-v`, `--version` — print the CLI build version
-   `--legacy-mode` — how deprecated/renamed commands are handled: `allowed` |
    `deprecated` (default) | `banned`
