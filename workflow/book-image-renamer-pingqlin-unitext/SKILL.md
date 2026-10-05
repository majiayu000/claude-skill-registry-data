---
name: book-image-renamer
description: "Identify book photos, extract visible metadata with local OCR, use a local multimodal model to correct OCR ambiguity, and build safe rename plans in the format 原書作者-書名-出版社-年分_ISBN. Use when Codex needs to process folders of book-cover images, distinguish single-book vs multi-book shots, prepare dry-run rename plans, or apply verified book-image renames without directly trusting raw OCR."
metadata:
  runtime_support_files: true
---

# Book Image Renamer

## Overview

Scan a folder of book images, extract OCR text with local PaddleOCR, and build a safe rename plan before any file is renamed.

Use this skill when the folder contains mixed images and only some of them are books, or when multiple shots of the same book need grouped suffixes.

## Workflow

1. Run a scan first:

```powershell
python "$env:USERPROFILE\.codex\skills\book-image-renamer\scripts\book_image_renamer.py" scan "<folder>" --output book_rename_scan.json
```

2. Review `book_rename_scan.json`.
3. Copy `metadata_template` into a separate metadata file and fill only verified edition metadata.
4. Build a rename plan:

```powershell
python "$env:USERPROFILE\.codex\skills\book-image-renamer\scripts\book_image_renamer.py" plan book_rename_scan.json metadata.json --output book_rename_plan.json
```

5. Inspect `book_rename_plan.json`.
6. Apply only from the plan:

```powershell
python "$env:USERPROFILE\.codex\skills\book-image-renamer\scripts\book_image_renamer.py" apply book_rename_plan.json --output book_rename_applied.json
```

## Current Pipeline

The current implementation is intentionally staged:

1. `scan`
   - Preprocess each image into a stable temporary JPEG before OCR.
   - Run local `PaddleOCR`.
   - Produce `ocr_lines`, a fast route (`candidate / review / skip`), and coarse book/title/author/ISBN hints.

2. `curated metadata`
   - Do not trust raw OCR for edition metadata.
   - Keep verified author, title, publisher, year, and ISBN in a separate curated JSON file.
   - Alias group keys may point multiple OCR variants back to the same verified book.

3. `plan`
   - Match each candidate image against curated metadata.
   - Re-evaluate image role using the OCR text only:
     - `front_plain`
     - `front_with_obi`
     - `back`
     - `spine`
     - `interior`
   - Sort same-book images by role before assigning filenames.
   - Avoid collisions by skipping to the next available suffix when a target name already exists.

4. `apply`
   - Rename only items with a generated `suggested_target_name`.
   - Leave unmatched items unchanged.

## Decision Points

- Ask for confirmation only if the user wants to rename images that contain multiple clearly visible books. The default is to leave them unresolved.
- If OCR produces a plausible title and author but publisher, year, or ISBN are still missing, do not rename yet. Record the candidate and continue.
- If the same verified book appears in multiple files, keep the most cover-like image as the base filename and suffix the others.
- Prefer `front_plain` over `front_with_obi`, then `back`, `spine`, and `interior`.
- If no verified metadata match exists, stop at `plan` and keep the original filename.

## Active Handling Policy

Use these rules when the user wants aggressive progress without external ISBN lookup:

- `書名最重要`
  - Prioritize extracting and matching the title above all other fields.
  - If title OCR is clear enough to identify a known book, continue even when author OCR is weak.
- `多本書 = 捨棄不處理`
  - Any image with more than one clearly visible book should be skipped from rename planning.
- `非書封 = 不處理`
  - Magazine pages, catalog pages, interiors without a clear cover, event photos, and non-book images should be skipped.

In this mode, the skill should spend effort on:

1. Clear single-book front covers
2. Back covers with a matching single-book title signal
3. Alias cleanup for noisy OCR title variants

It should not spend effort on:

1. Multi-book scenes
2. Non-cover documents or magazine-like pages
3. Weak matches based only on publisher, translator, or generic promo copy

## Matching Strategy

- Use OCR only to find candidate title, author, ISBN, and role hints.
- Use curated metadata as the source of truth for edition-level filename fields.
- Reuse verified metadata across OCR group variants only when the title/author signal is strong enough.
- Do not auto-promote weak fuzzy matches into rename candidates.

## Manual Alias Playbook

Use this when many images remain at `No verified metadata match` but the photographed book is still recognizable.

1. Open the current plan JSON and group the unresolved items by `candidate_group_key`.
2. Inspect only the first few `ocr_lines` of each group.
3. Look for one of these high-signal patterns:
   - Clear title line
   - Clear author line
   - Back-cover ISBN that already belongs to a verified edition
   - Distinctive subtitle or promo line that obviously belongs to one verified book
4. Add a new alias entry to the curated metadata JSON using the unresolved `candidate_group_key` as the key.
5. Point that alias entry to an already verified metadata record by copying the exact `author`, `title`, `publisher`, `year`, and `isbn`.
6. Re-run `plan`.
7. Only `apply` after checking that the new targets are book-consistent and collision-free.

### Good alias cases

- Front cover OCR is noisy, but the title line is still recognizable.
- Back cover contains a matching ISBN for an already verified edition.
- A book with obi and a plain cover were split into different OCR groups.
- OCR captured a distinctive subtitle that uniquely identifies one verified book.

### Bad alias cases

- Only publisher or imprint is readable.
- Only translator name is readable.
- OCR text could fit multiple books by the same author.
- The image might be a magazine page, catalog page, or multi-book scene.

### Preferred workflow for unresolved batches

1. Rebuild a current scan JSON filtered to files still present in the folder.
2. Run `plan` against the current curated metadata file.
3. Count unresolved `candidate` items.
4. Add only a few high-confidence aliases at a time.
5. Re-run `plan` after each small alias batch.
6. Apply only the newly safe renames.

## Local Dependencies

- `PaddleOCR` with `lang='ch'` is the primary OCR path. It handles mixed Traditional Chinese and Japanese book text better than the lighter OCR path used during evaluation.
- `Heretic` is optional auxiliary help for ambiguous cases. This skill expects an OpenAI-compatible endpoint at `http://127.0.0.1:1234/v1` with model `gemma-4-e4b-it-heretic`.
- Online metadata verification may still be used when the user explicitly wants it, but the core skill must also work in a no-search mode using only the existing curated metadata file.

## Files

- `scripts/book_image_renamer.py`: scans, groups, builds plans, and applies verified renames.
- `references/decision-rules.md`: stable rules for eligibility, metadata, and suffix handling.

Read `references/decision-rules.md` when deciding whether a candidate image is safe to rename.
