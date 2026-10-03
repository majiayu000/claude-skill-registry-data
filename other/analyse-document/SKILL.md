---
name: analyse-document
description: "Ingests and analyses a PDF document for a matter. Use when Mandy says 'analyse document', 'ingest', 'read this report', drops a PDF, or refers to a new medical report, IME report, insurer letter, or any document that needs to be added to a matter. Creates structured .extract.json for future reference."
---

# Analyse Document — Ingestion Gateway

## Important
- Manual-only. Never auto-invoke.
- This is the ONE time a full PDF is read (Tier 3).
- Always resolve matter reference first via `_shared/resolve-matter.md`.
- Consult `extract-instructions.md` for detailed extraction guidance.

## Instructions

### Step 0: Resolve Matter
Follow `_shared/resolve-matter.md` to identify the matter.

### Step 1: Identify Document
If filename given: find in `matters/{id}/documents/`.
If no filename: list unanalysed PDFs (those without `.extract.json` sibling) and ask which one.
If file not found:
```
"I can't find that file in matters/{id}/documents/.
Save the PDF there and try again."
```

### Step 2: Check Existing Extract
If `.extract.json` already exists:
```
"This document was analysed on {date} (extract v{version}).
Re-analyse? This will overwrite the existing extract (git preserves the old version)."
```

### Step 3: Read Full Document (Tier 3)
```bash
pdftotext -layout matters/{id}/documents/{filename} -
```
If output is empty: flag as scanned/image PDF. Create minimal extract with `missing_information` flag.

### Step 4: Classify Document Type
Determine type from the document type enum. See Section 4 of the spec for valid types.

### Step 5: Rename File
Apply naming convention: `{type}-{author-or-source}-{date}.pdf`.
Preserve original filename in extract's `original_filename` field.

### Step 6: Build Extract
Follow `extract-instructions.md` and `reference/extract-schema.json` for full schema.
Key sections: metadata, sections with page refs, diagnoses, causation, findings, capacity, treatment, prognosis, impairment, decisions, key quotes, flags, chronology entries.

### Step 7: Cross-Reference
Read existing `.extract.json` files in the same matter.
Flag: contradictions in diagnosis, changed work capacity, conflicting causation, new conditions.

### Step 8: Save and Update
1. Save `.extract.json` alongside the PDF
2. Update `matter.json`: documents array, injury fields, deadlines, dates
3. Update `matters/index.jsonl`
4. Check auto-advance conditions from `rules/stage-expectations.json`. Suggest stage change — confirm first.
5. Append to `activity-log.jsonl`
6. `git -C matters/ add -A && git -C matters/ commit -m "analyse-document: {id} — Ingested {filename}. {n} flags."`

### Step 9: Present
```
DOCUMENT: {type} | {date} | {author} | {pages} pages
KEY FINDINGS: {diagnoses, capacity, causation, impairment, prognosis}
FLAGS: {adverse findings, contradictions — with severity}
DEADLINES TRIGGERED: {any new deadlines}
CONTRADICTIONS: {conflicts with existing documents}
STAGE SUGGESTION: {if auto-advance triggered}
NEXT STEPS: {recommended actions}
```

### Step 10: Proactive Stage Check
Read `rules/stage-expectations.json`. Surface 1-3 overdue/imminent alerts.
Check `dates.limitation_expiry` — alert if within 12 months.

## Error Handling
- **pdftotext not installed:** "Install poppler-utils: `sudo apt install poppler-utils`"
- **Empty PDF output:** "This appears to be a scanned document. Text extraction limited. Key findings will need manual entry."
- **Corrupt PDF:** "Unable to read this PDF. Try re-downloading or re-saving it."
