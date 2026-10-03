---
name: build-chronology
description: "Builds a medical chronology from all analysed documents in a matter. Use when Mandy says 'build chronology', 'medical chronology', 'timeline', 'history of treatment', or needs a chronological view of medical evidence. Identifies gaps, contradictions, and missing assessments."
---

# Build Chronology

## Important
- Manual-only. Resolve matter first.
- Consult `chronology-format.md` for output structure.
- Uses Tier 1 only — reads .extract.json files, not raw PDFs.

## Instructions

### Step 0: Resolve Matter
Follow `_shared/resolve-matter.md`.

### Step 1: Check for Unanalysed Documents
List PDFs without `.extract.json` siblings.
If found: "There are {n} unanalysed documents. Chronology will be incomplete. Proceed anyway, or `/analyse-document` first?"

### Step 2: Collect Chronology Entries
Read ALL `.extract.json` files in `matters/{id}/documents/` (Tier 1, ~500-800 tokens each).
Collect `chronology_entries` arrays from each extract.

### Step 3: Merge and Sort
Sort all entries by date. Flag duplicates (same date + type + source → keep richest).

### Step 4: Gap Analysis
Identify: treatment gaps (3+ months for same body part), untreated conditions, CoC gaps, contradictions, missing impairment assessments, unexplained capacity changes, missing initial consultation.

### Step 5: Generate
Follow `chronology-format.md` for output structure.
Save to `chronology/chronology-{date}.md`.

### Step 6: Update and Commit
Update `matter.json`. Update index. Log and commit.

### Step 7: Present
Show entry count, date range, sources, gaps, contradictions, and recommended next steps.
Proactive stage check + limitation check.

## Error Handling
- **No extracts found:** "No analysed documents. Run `/analyse-document` first."
- **No chronology entries in extracts:** "Documents were analysed but no dateable events found. Check extracts manually."
