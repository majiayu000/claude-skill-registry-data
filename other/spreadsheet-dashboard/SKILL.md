---
name: spreadsheet-dashboard
description: "Cleans a messy sales or operations spreadsheet (mixed date formats, product names typed different ways, prices stored as text, duplicates, blank, test and dummy rows) and builds an Excel dashboard your team can read: totals at the top, sales by week, best and worst products, a chart. The dashboard runs on formulas over a Data table, so next month's rows update it, and a checker catches the paste-new-rows trap before you send it. Use when someone shares a messy spreadsheet, asks for a dashboard or report from an .xlsx or .csv, or says \"clean this sheet\", \"build me a dashboard\" or \"new month, add this\"."
---

# Spreadsheet Dashboard

Send Claude your messiest spreadsheet and get back a clean Data sheet and a Dashboard sheet built on formulas. Next month, hand it the new export and the same cleaning rules run again.

Never edits the original file. Every removed row is kept on a "Removed" sheet with the reason.

## What you need

- The spreadsheet as `.xlsx` or `.csv`. From Google Sheets: File > Download > Microsoft Excel.
- **Claude Code** with Python, pandas and openpyxl (`pip install pandas openpyxl`). LibreOffice is optional; it lets Claude open the result headless and check the numbers it shows.
- **Claude.ai** works too with code execution on (Settings > Capabilities): upload the file, download the result.
- To try it first: `sample/` has the messy January and February files from the reel (public UCI Online Retail data, CC BY 4.0, credit in `sample/SOURCE.md`).

## Commands

| Command | Does |
|---|---|
| `look at <file>` | Step 1 only. Read only |
| `clean <file> and build a dashboard` | Steps 1 to 4 |
| `add month <file>` | Step 5 |
| `check <dashboard.xlsx>` | Runs `scripts/check_dashboard.py` and explains the result |

## Step 1: Look (read only)

Load every sheet. Report a problems table before changing anything:

Example from the January sample file:

| Problem | Column | Rows | Examples | Proposed fix |
|---|---|---|---|---|
| Dates typed 5 ways | Date | all | `2011-01-05`, `05/01/2011`, `Jan 05 2011`, `5-Jan` | Parse each format; flag any that could be day/month or month/day |
| Same product typed differently | product | top sellers | `PLASTERS IN TIN SPACEBOY`, `plasters in tin spaceboy`, `  Plasters In Tin Spaceboy `, `StarsGift Tape` | Map to one name (list below) |
| Prices as text | price | 387 | `£1.25`, `2,95` | Strip currency, decimal comma to point |
| Exact duplicates | all | 8 | <row numbers> | Remove the second copy |
| Blank rows | all | 5 | <row numbers> | Remove |
| Test or dummy rows | product | 4 | `TEST ORDER - ignore`, `asdf`, `DUMMY DATA` | Remove |

Then ask only the judgement calls, in one message: ambiguous dates (is `04/01` 4 January or April 1?), whether shipping or fees count as products, what to do with zero-price, negative or refund rows, which column identifies an order, and what the team most wants to see.

Save the agreed rules to `cleaning-rules.md`: the product name map, date formats, test-row patterns, and each decision with the owner's answer. Next month reuses this file.

## Step 2: Clean

Write the rules into `clean.py` so the same cleaning can run again. Do it in code, not by hand in the sheet.

- Fix, do not guess. A price or date that fails to parse goes to "Removed" with reason `could not read`, never to a made-up value.
- Product names: trim spaces, fix capitals, then map typos to the name used most often. Do not merge two names unless the owner agreed or they differ only by case, spacing or one letter, and even then show the merges. Similar names can be different products ("12 Pencils Tall Tube" is not "12 Pencil Small Tube").
- Duplicates: only rows identical in every column. Same order number with different lines is not a duplicate.
- Output a count for every reason: `677 rows in, 660 kept: 5 blank, 4 test or dummy, 8 duplicates`.

## Step 3: Build the dashboard

One workbook, `dashboard.xlsx`:

- **Data**: the clean rows as an Excel Table (e.g. `SalesData`). Helper columns (Revenue = Qty x Price, Week start) are calculated columns of that table.
- **Dashboard**, top to bottom: title and a "Data from <first date> to <last date>" line (a formula), 3 to 5 totals (revenue, orders, units, average order), sales by week with a column chart, best 10 and worst 10 products by revenue. Every number is a formula pointing at the Data table. No typed numbers.
- **Removed**: every dropped row with its reason.
- Keep it readable: one font, one accent colour, currency and date formats set, gridlines off on the Dashboard, fits on one landscape page.

### The paste-new-rows trap

The dashboard only updates if new rows actually land inside what the formulas read. In the reel demo the first file looked right and still had this bug. Build it so all four hold:

1. **Name the table columns.** openpyxl writes `Column1`, `Column2`... unless you set them. Then `SalesData[Revenue]` breaks and Excel offers to "repair" the file. Write the header row first and create the table with `tableColumns` whose names equal the header text.
2. **Store formula columns as calculated columns** (`TableColumn(..., calculatedColumnFormula=TableFormula(attr_text="SalesData[[#This Row],[Qty]]*SalesData[[#This Row],[Unit Price]]"))`), so a row pasted into the table gets its Revenue formula.
3. **Point every dashboard formula at the table** (`SUM(SalesData[Revenue])`) or a whole column (`SUM(Data!G:G)`), never a fixed range like `Data!G2:G661`, which stops at today's last row.
4. **Tell the team how to add rows:** paste directly under the last row, into the same columns, with no blank row in between. Excel then grows the table. Google Sheets has no table growth: there use open ranges like `Data!G2:G`.

Also: never open the finished workbook with openpyxl and save it again. openpyxl drops charts it did not create. To add data, rebuild the workbook (step 5).

## Step 4: Verify before saying done

1. Recompute every total on the Dashboard with pandas from the clean data and compare. Any mismatch is a bug, not a rounding note.
2. Run `python scripts/check_dashboard.py dashboard.xlsx`. It must print `RESULT: PASS`.
3. If LibreOffice is installed, convert headless (`soffice --headless --convert-to pdf dashboard.xlsx`) and look at the page: numbers filled in, chart visible, nothing cut off. Say it was checked in LibreOffice, not Excel, and suggest opening it once in Excel before sending it to the team.

## Step 5: Next month (`add month <file>`)

1. Clean the new file with `clean.py` and `cleaning-rules.md`. Map new product names to existing ones where the rules allow; list any new names that look like typos and ask.
2. Refuse to add orders already in the Data sheet. Say how many matched and change nothing.
3. Keep all clean rows in `clean_data.csv` (every month so far) and rebuild `dashboard.xlsx` from it with the same build script, so formulas, formats and the chart stay identical. Keep the previous file as `dashboard_<previous month>.xlsx`.
4. Run step 4 again. Report what moved: totals before and after, the week that changed most, new entries in the best and worst lists.

## Rules

- The original file is never edited or overwritten.
- No number is typed into the Dashboard. If a figure cannot be built from the data, it is left out and named in the report.
- Customer names, emails and phone numbers never appear on the Dashboard; totals only.
- Do not invent targets, last year's figures or reasons for a change. A drop with no cause in the data is "cause not in this data".

## End of every run

1. Rows in, rows kept, rows removed by reason.
2. Files written, with paths.
3. Dashboard totals, with the date range they cover.
4. Verify results: pandas match, checker result, LibreOffice look (or "not checked").
5. Questions waiting for the owner.
6. "The original file was not changed."
