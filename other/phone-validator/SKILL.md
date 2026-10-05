---
name: phone-validator
description: >
  Score and validate phone numbers via Trestle's phone_intel API, then generate DataSift/REISift-ready CSVs with phone tags for upload. Use whenever someone wants to: validate phones, score activity, check if connected, generate phone tags for DataSift, prepare dial lists, prioritize a call list, identify dead numbers, check line types, or create tiered dial lists. Trigger for "phone validation", "validate phones", "activity score", "phone tags", "tag phones", "dial first", "Trestle", "phone_intel", "dead phones", "line type", "prioritize phones", "DataSift phone upload", "REISift phone tags", "score these phones", or "which numbers should I call first" — use this skill.
---

# Phone Validator & Tagger

Score phone numbers using Trestle's phone_intel API and produce DataSift/REISift-ready
CSVs with phone tags for prioritized dialing.

## What This Skill Does

This skill takes a CSV of phone numbers — typically a DataSift "Phone Enrichment" export
with Phone 1 through Phone 30 columns — runs each unique number through Trestle's Phone
Validation API to get an activity score and line type, then assigns a phone tag tier based
on configurable score thresholds. The output is a two-column CSV (`Phone Number`, `Phone Tag`)
formatted for direct upload to DataSift/REISift using their "Update Data → Tag phones by
phone number" workflow.

## The Pipeline

```
Input CSV (DataSift Phone Enrichment export or any CSV with phone columns)
  → Parse all phone columns (Phone 1 through Phone 30)
    → Deduplicate across all columns and rows (saves API cost)
      → ESTIMATE COST & GET USER CONFIRMATION
        → Trestle phone_intel API (activity_score + line_type)
          → Score-based tier assignment (Dial First, Dial Second, Dial Third, Dial Fourth, Drop)
            → DataSift-ready CSV (Phone Number | Phone Tag)
              → Upload to DataSift via "Update Data → Tag phones by phone number"
```

## How to Execute: Use the Bundled Script

The entire pipeline is handled by `scripts/validate_phones.py`. Always run this script
rather than reimplementing the API calls — it handles rate limiting, error recovery,
progress reporting, and the exact CSV format DataSift expects.

### Step 1: Install Prerequisites

```bash
pip install --break-system-packages requests
```

No other dependencies are needed.

### Step 2: Get the User's Trestle API Key

The script requires a Trestle API key. Check for it in this order:

1. Environment variable: `TRESTLE_API_KEY`
2. Ask the user to provide it

If the user doesn't have one, direct them to https://trestleiq.com to sign up —
they get 25 free queries per product on their trial.

### Step 3: Estimate Cost & Get User Confirmation

**This step is mandatory.** Before making any API calls, always run the script in
estimate mode first. This parses the CSV, counts unique phone numbers across all
columns, deduplicates, and calculates the cost at $0.015 per phone.

```bash
python3 SKILL_DIR/scripts/validate_phones.py \
  --input "path/to/phones.csv" \
  --estimate
```

This will output something like:

```
==================================================
  PHONE VALIDATION COST ESTIMATE
==================================================
  Input file:          Phone Enrichment.csv
  Total phone entries: 9,648
  Unique phones:       3,865
  Duplicates saved:    5,783
  Cost per phone:      $0.015
  ─────────────────────────────────────
  ESTIMATED COST:      $57.98
==================================================
```

Present this to the user and wait for their explicit confirmation before proceeding.
The deduplication savings are worth calling out — in a typical DataSift export, the
same person (and their phones) can appear on multiple rows because they own multiple
properties. The script only charges once per unique phone number.

For programmatic use, `--estimate-json` returns the same data as a JSON object.

### Step 4: Run the Validation

Once the user confirms the cost, run the full validation:

```bash
python3 SKILL_DIR/scripts/validate_phones.py \
  --input "path/to/phones.csv" \
  --output "path/to/output_directory/" \
  --api-key "$TRESTLE_API_KEY"
```

Replace `SKILL_DIR` with the actual path to this skill's directory.

**Optional flags:**

| Flag | Default | What it does |
|------|---------|-------------|
| `--tiers` | `default` | Tier strategy: `default` (5 tiers) or `custom` |
| `--custom-tiers` | — | JSON string defining custom tier boundaries (see below) |
| `--batch-size` | `10` | Concurrent API requests (respect Trestle's rate limits) |
| `--delay` | `0.1` | Seconds between batches |
| `--phone-column` | auto-detect | Override phone column name |
| `--add-litigator` | `false` | Include litigator risk check (uses Trestle add-on) |
| `--full-report` | `false` | Generate a detailed XLSX report alongside the tag CSV |

### Step 5: Understand the Output

The script produces these files in the output directory:

1. **`phone_tags_for_datasift.csv`** — The primary output. Two columns:
   - `Phone Number` — cleaned 10-digit phone number
   - `Phone Tag` — the assigned tier tag

   This is the file users upload to DataSift. They go to Upload → Update Data →
   "Tag phones by phone number", map the two columns, and the tags propagate across
   all records sharing that phone number.

2. **`validation_results.csv`** — Detailed results with all API data:
   - `phone_number` — the queried number
   - `activity_score` — 0-100 score from Trestle
   - `line_type` — Mobile, Landline, FixedVOIP, NonFixedVOIP, Tollfree, etc.
   - `carrier` — carrier name
   - `is_valid` — whether the number is a valid format
   - `is_prepaid` — prepaid indicator
   - `assigned_tag` — the tier tag assigned
   - `is_litigator_risk` — (if --add-litigator was used)

3. **`summary.txt`** — Human-readable summary with counts per tier, score distribution,
   and line type breakdown.

4. **`validation_report.xlsx`** — (if --full-report) Excel workbook with formatted tables,
   charts for score distribution, and tier breakdowns.

## Input Format: DataSift Phone Enrichment Export

The script is built to work directly with DataSift's "Phone Enrichment" CSV export format.
This is a wide-format file where each record (property/contact) can have up to 30 phone
numbers, each with associated metadata columns:

```
Phone 1, Phone Type 1, Phone Status 1, Phone Tags 1, Phone Is Connected 1,
Phone 2, Phone Type 2, Phone Status 2, Phone Tags 2, Phone Is Connected 2,
...
Phone 30, Phone Type 30, Phone Status 30, Phone Tags 30, Phone Is Connected 30
```

The script automatically detects all `Phone N` columns (1-30) and ignores the metadata
columns (`Phone Type N`, `Phone Status N`, `Phone Tags N`, `Phone Is Connected N`).
It then extracts every phone number across all columns and rows, deduplicates them,
and sends only unique numbers to the API.

The existing Phone Type values from skip tracing (MOBILE, LANDLINE, etc.) are left
untouched — this skill only adds phone tags, it does not modify the type or status fields.

The script also works with simpler CSV formats that just have a `Phone` or `Phone Number`
column.

## Tier Strategy

### Default (5 Tiers)

Five priority buckets that give callers a clear work order without overcomplicating
things. Based on analysis of validated phone numbers against actual Sift call outcomes:

| Score Range | Tag | What to do |
|------------|-----|------------|
| 81–100 | Dial First | Your best numbers — highest activity, highest contact rate. Call these first. |
| 61–80 | Dial Second | Strong numbers with solid activity. Work these after your first batch. |
| 41–60 | Dial Third | Moderate activity — still worth calling if you have capacity. |
| 21–40 | Dial Fourth | Inconsistent activity — get to these last if there's still time on the clock. |
| 0–20 | Drop | Dead or disconnected — not worth the dial time. |

This gives callers a clear work order: burn through Dial First, move to Dial Second,
then Dial Third, and reach into Dial Fourth if there's still time on the clock. Drop
gets excluded entirely.

### Custom Tiers

If you need different boundaries or tag names, pass a JSON object mapping tag names
to score ranges:

```bash
--custom-tiers '{"Priority": [80, 100], "Standard": [50, 79], "Low": [20, 49], "Remove": [0, 19]}'
```

## Line Type Context

The Trestle API returns these line types, which matter for how you contact the number:

| Line Type | What It Means | Implication |
|-----------|--------------|-------------|
| Mobile | Cell phone | Best for calling AND texting |
| Landline | Traditional landline | Call only — cannot receive SMS |
| FixedVOIP | Fixed Voice over IP (cable phone, etc.) | Usually dialable, sometimes textable |
| NonFixedVOIP | Non-fixed VOIP (Google Voice, etc.) | May be temporary/disposable — lower priority |
| Tollfree | 800/888/etc. number | Skip — not a personal number |
| Premium | Premium-rate number | Skip — will cost money to call |
| Voicemail | Voicemail-only service | Skip — no live person |

A key insight from our research: 24% of numbers that Sift labels as "Landline" are actually
FixedVOIP or NonFixedVOIP when checked against Trestle. These are textable numbers being
miscategorized — the detailed `validation_results.csv` output surfaces this with the
`line_type` column so you can identify which "Landline" numbers are actually textable.

## DataSift Upload Workflow

After the script generates `phone_tags_for_datasift.csv`:

1. Log into your DataSift/REISift account
2. Go to **Upload** → select **Update Data**
3. Choose **"Tag phones by phone number"**
4. Upload the CSV file
5. Map `Phone Number` → Phone Number field
6. Map `Phone Tag` → Phone Tag field
7. Complete the upload

The tags will apply across ALL records that share each phone number. So if the same
number appears on 3 different property records, all 3 get the tag.

### Integration / Dialer Workflow

Once tagged, when sending to a dialer integration:

- Go to **Send To** → select your dialer
- Under phone tag filters, select the tier(s) you want to send
- **Important**: Each transfer should only include ONE phone tag tier, because the
  filter requires the number to have ALL selected tags. Send "Dial First" separately
  from "Dial Second", etc.

For non-integrated dialers, use **Export** → filter by the specific phone tag.

## Handling Edge Cases

**Duplicate phone numbers**: The script deduplicates before calling the API to avoid
wasting queries. Each unique number is scored once, and the tag CSV includes one row
per unique number. In a typical DataSift export, the same owner's phones repeat across
multiple property rows — dedup catches all of these.

**Invalid/short numbers**: Numbers that fail Trestle's `is_valid` check get tagged as
"Invalid" and excluded from the tier tagging.

**API errors / timeouts**: The script retries failed requests up to 3 times with
exponential backoff. Permanently failed numbers are logged to `errors.csv`.

**Numbers already tagged in Sift**: Uploading new tags via "Update Data" ADDS to existing
tags — it does not replace them. If you need to remove old tags first, you'd do a
separate "Remove phone tags by phone number" upload.

**Large lists**: Trestle rate-limits API calls. The script defaults to 10 concurrent
requests with 100ms delay between batches. For lists over 10,000 numbers, consider
using Trestle's batch upload product instead.

**No API key available**: If the user doesn't have a Trestle API key and can't get one,
the script can run in `--dry-run` mode which generates the CSV template with placeholder
tags so they can see the format and manually fill in scores later.
