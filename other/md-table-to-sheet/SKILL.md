---
name: md-table-to-sheet
description: Convert a markdown table to CSV and upload it to Google Drive as a native Google Sheet. Use when the user passes a `@file#Lstart-end` range (from nvim `<leader>yr`) over a markdown table, pastes a table, or says "put this table in a sheet", "upload this to Drive/Sheets", "make a sheet out of this".
argument-hint: "@path/to/file.md#L15-40  [title] [--links url|text|hyperlink|keep]"
allowed-tools: Read, AskUserQuestion, Bash(md2csv:*), Bash(sed:*), Bash(grep:*), Bash(awk:*), Bash(wc:*), Bash(ls:*), Bash(cat:*), mcp__claude_ai_Google_Drive__search_files, mcp__claude_ai_Google_Drive__create_file, mcp__claude_ai_Google_Drive__update_file
---

# Markdown Table → Google Sheet

Concept of operations: the user hands over a **range**; those lines **are** the table.
Take them, convert with `md2csv`, upload the CSV to Drive as a native Google Sheet,
hand back the URL.

`md2csv` is `~/dotfiles/bin/md2csv`, on PATH. The Drive MCP's `create_file` turns an
uploaded `text/csv` body into a real Sheet. This skill is the glue plus the naming and
destination policy.

## Core Recipe

**1. Resolve the range to a file and line numbers.**

`<leader>yr` yields `@file#L15-40` (visual) or `@file#L22` (normal, single line). The path
is `expand('%:.')` — *relative to the nvim cwd*, which for vault work is
`/home/jke/worklog`. Resolve it there when it does not exist relative to the session cwd.

A pasted table with no file? Skip to step 2 with the pasted text as the lines.

**2. Slice the range and pipe it to md2csv.**

```bash
sed -n '15,40p' "$FILE" | md2csv --links hyperlink > "$SCRATCH/<slug>.csv"
```

Stdin, not `md2csv "$FILE" -l 15`, because the range is the user's statement of intent —
and a slice also exports the buffer's *current* table when the user is working from a
range they just selected. Surrounding prose inside the range is harmless: `find_tables`
scans for the header+delimiter pair and ignores the rest.

`--links hyperlink` is this skill's default: `=HYPERLINK("dest","text")` is clickable
*and* labelled in Sheets. `md2csv` falls back to `url` mode for cells that mix prose with
a link, since a formula cannot live inside text. Override with `--links url|text|keep`
on request.

**3. When the slice does not parse, widen once — do not hand-fix it.**

A selection that starts at the first *body* row is not a table: `find_tables` requires a
header plus a delimiter row. `md2csv` exits 2 with `no markdown table found` and — by
design — replays stdin to stdout, so **stdout is the markdown back again, not CSV.** Never
upload the output of a failed run.

Recover by asking the file where the real table is:

```bash
md2csv "$FILE" --list
#   1 table(s):
#     -n 1  line 15  25 rows x 4 cols  url / kind / notes / wikilinked-notes
```

Each entry spans `line L` through `L + 1 + rows`. Take the table whose span overlaps the
requested range, re-run with `-n N`, and **say in the report that the range was widened
and to what**. Several tables overlap, or none do? Show the `--list` output and ask. Do
not guess which table the user meant.

**4. Derive a title, then confirm it.**

Build `YYYY-MM-DD — <subject>`: the date from the source page (a `Journal/` stem) or
today, the subject from the nearest markdown heading above the table, falling back to the
first two header cells. Prefer the heading over the page stem — vault filenames like
`aev rbf patch simtest table formally the 8-27 journal.md` make poor sheet names.

Then **ask the user to accept or override** via `AskUserQuestion`, derived name as the
first option. The title is the only thing that makes an export findable in Drive later,
and renaming after the fact is a second trip.

**5. Resolve the destination folder, creating it at most once.**

```
search_files: query = "title = 'Worklog exports' and mimeType = 'application/vnd.google-apps.folder' and owner = 'me'"
```

Empty → `create_file` with `title: 'Worklog exports'`,
`contentMimeType: 'application/vnd.google-apps.folder'`, no content. Reuse the id
afterwards; never create a second folder of the same name.

**6. Upload as a native Sheet.**

```
create_file:
  title:           <confirmed title>
  parentId:        <Worklog exports folder id>
  textContent:     <the CSV text>
  contentMimeType: "text/csv"
```

Leave `disableConversionToGoogleType` unset — conversion to
`application/vnd.google-apps.spreadsheet` is the entire point, and setting it yields a
CSV attachment Sheets will not open in place. Use `textContent` (md2csv output is UTF-8),
not `base64Content`. Do not set the deprecated `mimeType` field.

**7. Report** the sheet URL, rows × columns, which table was used if it was ambiguous, and
any `md2csv` stderr warning verbatim.

## Variations

- **Local CSV file instead of Drive:** that is nvim's `:MdTableCsv` — `:'<,'>MdTableCsv`,
  `:'a,'bMdTableCsv`, or `:MdTableCsv` with the cursor in the table; it prompts for a
  path. Point the user there rather than writing a file for them.
- **Clipboard instead of Drive:** `sed -n '15,40p' "$FILE" | md2csv --tsv | osc52-copy`,
  then paste into an existing sheet. Beats an upload when the destination already exists.
- **Append to an existing sheet:** `create_file` cannot. Use the clipboard path above.
- **Rename or move a previous export:** `update_file` with `fileId` — title and `parentId`
  only, never content.

## When Applying This Skill

1. Resolve the `@file#L…` path against the nvim cwd (`/home/jke/worklog` for vault work)
   when the relative path misses.
2. Slice the range and pipe it in. Widen via `--list` only when the slice fails to parse,
   and report that you did.
3. Never upload stdout from a nonzero `md2csv` exit — that output is the input replayed.
4. Keep `--links hyperlink` unless told otherwise.
5. Confirm the derived title before uploading — always.
6. Reuse the `Worklog exports` folder; create it only on an empty search.
7. Relay the ragged-row warning (`N row(s) did not match the C-column header;
   padded/truncated`) — it means the sheet will differ from the markdown, and
   `<leader>ma` (`md_table.lua`'s `align()`) is the fix on the markdown side.
