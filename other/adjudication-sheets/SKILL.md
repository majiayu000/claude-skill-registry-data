---
name: adjudication-sheets
description: |
  Build human adjudication / hand-labeling sheets from LLM-pipeline data without
  evidence truncation. Use when: (1) preparing a CSV/Excel sheet for a human to
  rule on cases an LLM classifier or rater panel judged, (2) a labeler reports
  "there is no information to label from" or cells look empty in Excel,
  (3) excerpt columns cluster at one exact length (e.g. all 1,500 chars — a hard
  truncation cap). Covers: full rating-basis recovery, Excel 32,767-char cell cap,
  multi-line CSV mangling, ruling dropdowns, companion text files.
author: Claude Code
version: 1.1.0
date: 2026-07-08
---

# Human Adjudication Sheets from LLM-Pipeline Data

## Problem
Adjudication sheets built from pipeline intermediates tend to carry truncated
"excerpt" columns (previews made for machine diffing, not human judging). A human
asked to rule "does this text show X?" on a fragment produces invalid rulings:
the decisive sentence may sit past the cutoff. Separately, multi-line text in CSV
cells renders as broken rows/empty cells in Excel, so the labeler reports "there
is no data here" even when the column is populated.

## Context / Trigger Conditions
- A labeler says the sheet has "no information" — check for embedded newlines in CSV fields first.
- Excerpt lengths cluster at an exact value (all 1,204 / 1,500 / 800 chars) or end with "[…]" — that is a hard cap, not natural length.
- The ruling question is "does the record/text show X?" — the ruling basis must be byte-identical to what the classifier/raters saw, or the ruling grades a different object.

## Solution
1. **Trace the true rating basis from the scoring code, not from intermediates.** Find the line where text is passed to the model (e.g. `prompt = ... + text`) and reproduce that construction exactly. Verify: stored excerpt == full_text[:cap] (0 mismatches), or cache-key match against the LLM request cache.
2. **Deliver .xlsx, not .csv**, for any sheet with multi-line text: wrap_text + frozen header + generous width on evidence columns; data-validation dropdown on the `ruling` column with the exact allowed codes (e.g. E_pos/E_neg/unclear, or 0/1/2/unclear).
3. **Handle the Excel cell cap (32,767 chars) explicitly:** if full text exceeds it, inline the first ~30k ending with a loud marker ("[CONTINUES — see companion file]") AND write the complete text to a per-case `.txt` (header block with case metadata + full text); add a `text_file` path column. Write companion files for ALL cases regardless — they are the comfortable reading surface.
4. Keep the original CSV untouched as the machine-readable artifact; the xlsx is the human ruling surface; harvest rulings from the xlsx.
   **Distribution:** `text_file` paths are project-relative and break the moment the sheet is emailed or copied out of the tree (the labeler asks "where are the attendant/companion files?"). If the labeler is not working inside the project folder, ship ONE zip containing the xlsx and the companion-texts folder side by side, with the instruction: extract together; the file for row X is `<texts_folder>\<case_id>.txt` next to the spreadsheet. Require the FILLED xlsx back and harvest from the returned copy, not the original.
5. Tell the labeler the epistemics: rule from the provided record only; silence = negative; outside research (Google) goes in `ruling_notes`, never the ruling — otherwise the labels leak information the classifier could never see.

## Verification
- No excerpt column has >30% of rows at one exact length; no "[…]" markers remain.
- `pd.read_excel` round-trip shows full lengths (compare min/median/max vs the old excerpts).
- Dropdown rejects free-text entries; a saved test ruling survives reopen.

## Example
Specialist Directors US, 2026-07-08: director sheet excerpts capped at ~1,200 chars (full dossiers up to 4,090); filing sheet capped at 1,500 chars while raters had scored the whole ~80k-char Item 1A — the PI caught both mid-sitting. Fix: `src/director_v1/make_sitting_xlsx.py`, `tools/make_adjudication_v2_xlsx.py` (full-text xlsx + 76 companion txts + dropdowns).

## Notes
- Uniform-length clustering is the fastest tell; check it BEFORE handing any sheet to a human.
- Harvest gotcha: when comparing harvested rulings to prior labels, coerce BOTH sides to numeric first — Excel/pandas round-trips floats as "1.0" vs the dropdown's "1", so a string compare falsely flags every row as a disagreement.
- If the pipeline caches LLM requests content-addressed, verify the rebuilt basis against the cache rather than trusting a deterministic builder to have been stable.
