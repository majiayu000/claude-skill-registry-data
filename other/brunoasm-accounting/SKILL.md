---
name: accounting
description: "Process receipts, track expenses in Google Sheets, reconcile records, and generate entertainment supplement tables for Field Museum procurement card accounting"
---

# Accounting Skill

Use this skill when the user wants to:
- Process new receipts and add expense records
- Reconcile receipts against spreadsheet records
- Generate entertainment supplement tables
- Check budget or fund balances
- Organize procurement card accounting

Keywords: receipt, expense, accounting, budget, fund, supplement, p-card, procurement, GL code, reconcile

## Available Resources

- `references/gl_codes.md` — GL code reference table with entertainment flags
- `references/supplement_guide.md` — Supplement form layout and filing rules
- `references/smartdata_reports.md` — SmartData report formats, parsing, the 1% international fee, and pairing rules
- `scripts/parse_smartdata.py` — parses a SmartData Account Statement XLSX and pairs international fees
- `scripts/check_missing_receipts.py` — flags posted charges missing from the expenses sheet

## Session Start

**Run this skill from the accounts and receipts working folder.** Every path below is relative to it, and `{working_folder}` means that directory — the current one. The folder's location is deliberately not recorded in this repo.

**One exception:** `scripts/` and `references/` name this skill's own files and resolve against the **skill's** directory — the one holding this `SKILL.md` — not the working folder. `{skill_dir}` below means that directory; substitute it when running a command, since the current directory is the working folder and `python3 scripts/…` would not be found there. Every other path in this file, `{year}/…` included, is relative to the working folder.

If the current directory holds neither `spreadsheet_links.yaml` nor a `{year}/` directory, this is the wrong folder: say so and ask the user to restart the session from the right one. Do not go searching the filesystem for it.

1. **Detect year**: Determine the current year from today's date. Confirm with the user: "Working on **{year}** expenses — correct?"

2. **Get spreadsheet link**: Check for `spreadsheet_links.yaml` in the working folder.
   - If a link for this year **already exists** in the YAML, show it and ask: "Using this spreadsheet — correct? {url}"
   - If the file is missing or has no entry for this year, ask the user for the Google Sheet link.
   Save/update the link:
   ```yaml
   {year}:
     spreadsheet_id: "{extracted_id}"
     url: "{full_url}"
   ```

3. **Read current expenses**: Detect the environment by testing whether this is a local Mac session — `command -v open` succeeds and the `{year}/receipts/` directory is present. Then:

   - **On cowork (local Mac)**:
     Open the spreadsheet in Chrome so the user can interact with it:
     ```bash
     open -a "Google Chrome" "{full_url}"
     ```
     Also fetch the expenses tab via WebFetch CSV export:
     ```
     https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=expenses
     ```
     If the WebFetch CSV export fails or returns an auth/login page, note this and ask the user to manually export the sheet as CSV and provide the file path.

   - **Not on cowork (cloud/remote — no local receipts tree)**:
     Fetch directly via WebFetch CSV export:
     ```
     https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=expenses
     ```
     If this fails, ask the user to paste the spreadsheet data or provide a downloaded CSV file.

   Parse the expenses data to understand existing records and the receipt numbers already used. **Analyze patterns** in existing records to learn Fund and GL code assignment conventions — e.g., which vendors consistently map to which funds and GL codes. Use these precedents when proposing values for new receipts rather than defaulting to a single fund.

   **Expenses CSV file for `check_missing_receipts.py`** (the *expenses-CSV
   recipe*, referred to by that name from step 8 and Phase 3). That script needs the
   sheet as a *file* on disk; WebFetch yields content in context, not a file. So
   download it with `curl` to a temporary path **outside this repo and outside
   the working folder**, use it, and delete it in the same command:

   ```bash
   curl -sL -o /tmp/expenses_check.csv \
     "https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=expenses" \
     && python3 {skill_dir}/scripts/check_missing_receipts.py "{year}/reports/{file}" \
          --expenses /tmp/expenses_check.csv --json
   rm -f /tmp/expenses_check.csv
   ```

   `{SPREADSHEET_ID}` comes from `spreadsheet_links.yaml` at run time and is
   never written into this file. Keep the `rm -f` in the same invocation and
   unconditional, so a failed check still deletes the file — expense data must
   not linger anywhere outside the working folder, least of all in this repo. If
   `curl` returns an HTML login page instead of CSV, the sheet is not readable by
   link: say so and skip the check rather than running it on a bad file.

4. **Read past supplements**: List and read existing supplement PDFs in `{working_folder}/{year}/supplements/` to learn default patterns for entertainment supplement fields (Persons Involved, Business Purpose). For example, grocery store purchases may consistently use a standard lab group description while restaurant meals may list named attendees. Use these patterns as defaults when proposing supplement data for new entertainment expenses.

5. **Scan receipts folder**: List files in `{working_folder}/{year}/receipts/`. Identify:
   - Highest existing receipt number (pattern: `YYXXX_...`)
   - Any unnumbered files (those not matching the `YYXXX_` prefix pattern)

6. **Read all unnumbered files**: Proactively read the contents of every unnumbered file before presenting anything to the user. Files may have misleading names (e.g., `receipts_2026.pdf`, `Pcard Missing Receipt Form.pdf`). Classify each file by inspection:
   - **Normal receipt**: proceed with processing
   - **Duplicate**: matches an already-numbered receipt — flag for user but don't process
   - **Non-receipt**: forms, summaries, statements — flag for user, skip processing
   - **Unreadable**: image too low-resolution or corrupted — flag and ask user for details

7. **Load SmartData reports**: List `{year}/reports/`. For each `YYYY_MM.xlsx`, run:
   ```bash
   python3 {skill_dir}/scripts/parse_smartdata.py "{year}/reports/{file}" --json
   ```
   Keep the parsed purchases, fee lines, and pairings for use in Phase 1, and note which posting-date windows are covered. See `references/smartdata_reports.md` for the formats, the PDF fallbacks, and what each `problems` reason means.

   **The script exits 1 when `validation.ok` is false, including in `--json` mode.** That is a verdict, not a crash — the JSON on stdout is complete and usable. If `validation.ok` is false, report the failing checks to the user, then **continue using the parse**, treating any fee amount derived from it as unconfirmed until the user says otherwise. The common benign cause is a refund or a real payment in the month: those land in the statement's Payment bucket alongside the fee lines, so `fee_count`/`fee_total` disagree even on a perfectly correct parse. Do not stop work over it.

   If the script instead **errors outright** (a traceback, no JSON), report the error and continue without that report — the reports folder is documented as optional, so its absence is a known-supported state rather than a blocker.

   **Also report, per report loaded:** the number of `problems` entries (fees the parser would not attribute) and the number of `international_without_fee` purchases. Both need the user's eyes and neither shows up in `validation.ok`. Step 1.3 says what to do with each when a receipt reaches it.

   The folder is optional — if it is missing or empty, continue without it and ask per Step 1.3 when a receipt actually needs the information.

8. **Report status**:
   ```
   Year: {year}
   Spreadsheet: {url}
   Existing expense records: {count}
   Reports loaded: {count} covering {posting-date windows}
   Unattributed fee lines / international purchases with no fee: {count} / {count}
   Numbered receipts: {count} (highest: {number})
   Unnumbered files to process: {count}
   {list unnumbered filenames}
   Posted charges not yet recorded: {count}
   ```

   `Posted charges not yet recorded` is the size of `missing_from_sheet` — the
   actionable bucket only, not the other three. Populate it by running
   `check_missing_receipts.py` for each loaded report, using the expenses-CSV
   recipe in step 3 to get the file. If the CSV could not be fetched, print
   `unknown` rather than `0` — an unfetched sheet is not an empty one.

9. Ask the user what they'd like to do: process new receipts, reconcile, check budgets, or generate a supplement.

## Phase 1: Receipt Processing

For each unnumbered file in the receipts folder:

### Step 1.1 — Read the receipt
The file was already read during session start (step 6). Use the extracted contents. If the file was an image too low-resolution to read, acknowledge this immediately and ask the user for: vendor name, amount, date, and description. Do not guess from unreadable images.

From the receipt contents, extract:
- Vendor name
- Date of purchase
- Total amount (including tax)
- Description of items purchased
- Payment method if visible

### Step 1.2 — Propose filename
Generate the next receipt number continuing from the highest existing number:
- Format: `YYXXX_short_description.ext` (keep original file extension)
- Short description: lowercase, underscores, 2-4 words describing the purchase
- Example: `26025_amazon_labsupplies.pdf`

### Step 1.3 — Cross-check against the SmartData report

Use the reports loaded during session start (step 7). See
`references/smartdata_reports.md` for details.

1. **Payment method**: match the receipt to a parsed purchase by description and
   amount. Descriptions are card descriptors (`AMAZON MKTPL*<id>`,
   `SQ *<merchant>`), so match fuzzily. A match confirms `p-card`. If there is no
   match, ask whether this is a p-card charge that has not posted yet, `finance`,
   or `reimbursement` — never silently default to `p-card`.

2. **Amount**: compare the receipt total to the posted USD amount. If they
   differ, show both and ask which to record. Differences are usually legitimate
   — tips, currency conversion, partial capture, hotel incidentals — so the
   posted amount normally wins, but do not assume it.

3. **International fee**: the charge is international when the report's Country
   is present and not `UNITED STATES`. If no report covers the receipt's period,
   fall back to the heuristic (non-USD receipt, or a vendor outside the US even
   if billed in USD).

   Branches **(a)**, **(b)**, **(c)** and **(e)** are the four ways the parser can
   describe *this* charge; exactly one of them applies, so take that one. Branch
   **(d)** is not reached from the receipt at all — a `no_match` fee has an empty
   `candidates` list, so nothing in the parse links it to any receipt. It is
   reached from the report, must be surfaced on its own, and branch (e) consults
   it before computing anything.

   - **(a) A paired fee line exists** — the charge appears in the parser's
     `pairs`. Use the fee's **actual** amount. No estimate, no computation.

   - **(b) The charge has not posted** — either no report covers its period, or a
     report covers the period but does not list the charge. Compute **1% of the
     posted USD amount, rounded half-up to the cent** and mark it an estimate.

   - **(c) The fee is in `problems` with `reason: "ambiguous"` and this receipt's
     purchase is one of its `candidates`** — several purchases could have
     incurred it. Show the candidates and ask which. When `equivalent` is true,
     say that either assignment gives the same numbers. Never guess the parent.
     If the user rules this receipt's purchase **out** — the fee belongs to a
     different candidate — the purchase has no fee of its own, and the parser
     will not have listed it under `international_without_fee`. Fall through to
     (e) and treat it as a charge whose fee has not posted.

   - **(d) A fee is in `problems` with `reason: "no_match"`** — an orphan. Its
     `candidates` list is empty, so nothing links it to a receipt and there is
     nothing to show. Report its **transaction date and amount** to the user.
     Before assuming it belongs to the receipt in hand, check it against the
     estimated fee rows carried over from the previous statement: a fee that
     posts just after a statement close appears on the *next* statement without
     its parent, and it belongs to that earlier row — Phase 3 step 4 retires it
     there. Never guess a parent.

   - **(e) The report covers the charge, shows no paired fee, and it is not in
     `problems` either** — the parser lists it under `international_without_fee`.
     **First check (d):** if **exactly one** unpaired `no_match` fee in the same
     report shares this charge's transaction date, has an amount equal to 1% of
     the posted USD amount to within a cent, and does not already match an
     estimated row carried over from the previous statement, that fee *is* this
     charge's — use its **actual** figure, say the pairing was made by hand, and
     do not compute an estimate. If two or more fees fit, or the fee also fits a
     previous statement's estimated row, show them and ask rather than choosing:
     the rule against guessing a parent applies to hand matches too.
     Only when no such fee exists, treat the fee as not yet posted: compute **1%
     of the posted USD amount, rounded half-up to the cent**, add the fee row
     marked as an estimate, and tell the user the report showed no fee line for
     that charge. The likely cause is the fee posting just after the statement
     close; Phase 3's estimated-fee check will confirm or correct it once a later
     report covers it.

For an international charge, `Cost` on the main row is the **posted USD amount**,
not the receipt's foreign total, and `notes` carries the original amount,
currency, and conversion rate.

**When a report is needed but missing**: if the receipt's period has no report at
all, ask the user to export that statement month from SmartData into
`{year}/reports/` as `YYYY_MM.xlsx`. Offer to continue meanwhile with a computed
1% estimate and a flagged payment method — a missing report must never block the
work. If a report covers the period but the charge is absent, it simply has not
posted; do not ask for another report.

### Step 1.4 — Propose expense record
Fill in all 10 columns of the expenses tab:

| Field | How to determine |
|-------|-----------------|
| Expense | Brief description of what was purchased. For refunds/credits, match the original expense name from the spreadsheet followed by "(refund)" — e.g., "Claude subscription for students (refund)", not a generic description |
| Vendor | Vendor/merchant name from receipt |
| Cost | Total amount as `$X.XX` (negative for returns/credits) |
| date | Purchase date in `D-Mon-YYYY` format (e.g., `15-Mar-2026`) |
| method | Whatever Step 1.3's payment-method check determined — a report match confirms `p-card`; no match means asking. Never default to `p-card` here |
| Fund | Propose based on patterns learned from existing spreadsheet records for the same vendor or expense type. Only ask the user if no clear precedent exists |
| GL code | Propose based on `references/gl_codes.md` (consult ALL codes, not just commonly used ones) AND patterns from existing spreadsheet records. Only ask the user if no clear precedent exists |
| receipt_number | The `YYXXX` number assigned in Step 1.2 |
| notes | Leave empty unless something notable — **except for an international charge**, where Step 1.3 requires the original amount, currency, and conversion rate here |
| request reimbursement | Leave empty unless user specifies |

**International transaction fee row.** When Step 1.3 found or computed a fee, emit a
**second row** alongside the main one:

| Field | Value |
|-------|-------|
| Expense | `{vendor} — international transaction fee` |
| Vendor | same as the parent row |
| Cost | the actual fee from the report, else 1% of the parent's USD amount rounded half-up to the cent |
| date | the **parent row's** date, so the two rows stay adjacent |
| method | same as the parent row (always `p-card` — a fee row is only ever emitted when the parent is `p-card`; see below) |
| Fund | same as the parent row |
| GL code | same as the parent row |
| receipt_number | same as the parent row |
| notes | `Foreign transaction fee on {parent row's Expense description} (see {receipt_number})` — append `; 1% estimate, verify against statement` when computed rather than read. When the estimate is because the report covered the charge but showed no fee line (`international_without_fee`), also append `; report showed no fee line for this charge` so both facts are on record. When Step 1.3 branch (e) instead matched an unpaired `no_match` fee by hand, the amount is **actual**: append `; fee matched by hand from an unpaired report line` and add no estimate caveat. |

The fee inherits the parent's GL code, so no new GL code is needed. Sharing the
parent's `receipt_number` is expected: Phase 3 already treats one receipt number
covering multiple rows as normal. If the fee's own posting date differs from the
parent's, note it rather than splitting the rows apart.

For `finance` and `reimbursement`, add **no** fee row — the 1% is a card
assessment. Record the USD amount if it is known, from the payer's own statement
or the reimbursement figure, and otherwise ask: no report this skill can read
covers a non-p-card payment. Put the foreign amount in `notes` either way.

### Step 1.5 — Entertainment check
If the GL code is an entertainment code (6455, 6460, 6470, 6475), collect supplement form fields. Use patterns learned from past supplements (read during session start, step 4) to propose defaults:
- **Location**: venue name and city (often derivable from receipt)
- **Persons Involved**: propose based on patterns from past supplements for similar expense types — e.g., grocery/snack purchases may consistently use a standard lab group description, while restaurant meals list named attendees. Only ask the user to confirm or correct, not to provide from scratch
- **Business Purpose**: propose based on past supplement patterns for the same venue or expense type. Only ask to confirm
- **Alcohol**: ask if alcohol was purchased (affects VP approval requirement)

Store this supplement data for Phase 4.

### Step 1.6 — Confirm with user
Present all proposed data clearly and ask for confirmation before proceeding. Show:
- Proposed filename
- All expense record fields
- Entertainment supplement fields (if applicable)

Only after user confirms:
- Rename the file using `mv`
- Add the expense record to the accumulator for Phase 2

### Step 1.7 — Repeat
Move to the next unnumbered file. After all files are processed, proceed to Phase 2.

## Phase 2: Spreadsheet Update

After all receipts are processed:

1. Compile all new expense records using pipe `|` as separator, matching the column order:
   ```
   Expense|Vendor|Cost|date|method|Fund|GL code|receipt_number|notes|request reimbursement
   ```

2. Print the pipe-separated rows directly (do NOT write to a file). Instruct the user:
   - Click on the first empty cell in column A
   - Paste the text
   - Click the small paste icon that appears at the bottom-left
   - Select **Split text to columns**
   - Choose **Custom** separator and type `|`

3. Remind the user to sort the sheet by date after pasting if desired.

## Phase 3: Reconciliation

Compare receipts folder against spreadsheet records:

1. **Read current expenses** from the spreadsheet (re-fetch via CSV export).
2. **List receipt files** in `{year}/receipts/` matching the `YYXXX_` pattern.
3. **Compare**:
   - **Orphaned receipts**: files in folder with no matching `receipt_number` in the spreadsheet
   - **Missing files**: spreadsheet records whose `receipt_number` has no matching file
   - **Note**: some receipt numbers may cover multiple expense rows (same receipt, multiple items) — this is expected
4. **Confirm estimated fees**: for rows whose notes carry `1% estimate`, check them
   against a report that now covers the period. Correct the cost if it differs and
   drop the estimate caveat once confirmed.

   **Where the actual amount is.** A fee that posted just after the previous
   statement's close lands on the next statement with no parent on it, so the
   parser cannot pair it: it appears in that report's **`problems[*].fee` entries
   with `reason: "no_match"`**, not in `pairs`. Look there. A `no_match` fee whose
   transaction date matches the estimated row and whose amount equals 1% of that
   row's parent cost to within a cent is the confirming figure. If none matches,
   leave the estimate caveat in place and say so — never drop it on the strength
   of a fee you could not identify.
5. **Check for unrecorded charges**: for each `YYYY_MM.xlsx` in `{year}/reports/`,
   get the expenses CSV with the expenses-CSV recipe in Session Start step 3, then
   run:
   ```bash
   python3 {skill_dir}/scripts/check_missing_receipts.py "{year}/reports/{file}" \
       --expenses /tmp/expenses_check.csv --json
   ```
   Delete the CSV afterwards, per that recipe. This script always exits 0 — read
   the buckets, not the exit code.

   Report each bucket separately — `missing_from_sheet` is the actionable list;
   `possible_amount_mismatch` means recorded with a different amount (often the
   receipt's foreign total instead of the posted USD); `ambiguous` needs the user to
   pick; `rows_without_receipt_number` cannot have a receipt file.

   Every charge lands in exactly one of the first three or is matched cleanly and
   reported in none of them. `rows_without_receipt_number` is different in kind —
   it is a subset of the *matched* rows, so it never overlaps the other three and
   its count is not additive with them. One more thing to know when reading the
   output: an unrecorded **fee** never appears in `possible_amount_mismatch`,
   because every fee line carries the same descriptor and so has no vendor words
   to match a row on. It normally lands in `missing_from_sheet` — though if its
   amount and date happen to fit two unclaimed rows it goes to `ambiguous`
   instead, since exact matching runs before the descriptor test.

   State the limits alongside the results: a charge not yet processed is a true
   positive, and early in a cycle the missing list is expected to be long; another
   cardholder's spending never appears in this report; and aggregated monthly rows
   cannot match individual charges. Never create rows or invent receipt numbers
   from this output — report and ask.
6. **Report** findings clearly, listing any discrepancies.

## Phase 4: Entertainment Supplement

Generate the supplement table for a given month:

1. Ask which month to generate (default: current or most recent month with entertainment expenses).
2. Filter entertainment expenses (GL 6455/6460/6470/6475) for that month from the spreadsheet.
3. Combine with the supplement data collected during Phase 1 (if in the same session) or ask the user for missing fields.
4. Format as a table matching the supplement form layout:

   ```
   Date | Location | Persons Involved (Name, Title, Company) | Business Purpose | Total
   -----|----------|------------------------------------------|-----------------|------
   {rows}
                                                                          Total: ${sum}
   ```

5. Output the table as copyable text.
6. Note if any expenses involved alcohol (VP approval required).
7. Remind: save as `supplement_BASM_{YYYY}_{MM}.pdf` in `{year}/supplements/`.

## Phase 5: Budget & Fund Check

On user request:

1. Fetch the **funds** tab via CSV export — show available balances per fund.
2. Fetch the **budget** tab via CSV export — show spending by GL category, flag any over-budget items.
3. Present a concise summary with the most relevant information.

## Communication Guidelines

- Be concise. Lead with the data, not explanations.
- When proposing expense records, present them in a clear table format.
- When multiple receipts need processing, handle them one at a time — don't batch confirmations.
- For the paste block, use pipe `|` as separator. Tab-separated text does not survive copy-paste from Claude, and commas conflict with values. Pipe is safe and Google Sheets supports it via custom separator.
- Always confirm before renaming files or finalizing expense records.
