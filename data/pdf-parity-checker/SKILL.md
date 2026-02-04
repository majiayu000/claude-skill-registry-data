---
name: pdf-parity-checker
description: Verify visual and structural parity between XHTML chapters and POD PDF files. Use to ensure print edition matches digital EPUB layout.
---

# PDF Parity Checker Skill

## Purpose

Compare the 44 XHTML chapter files against their corresponding POD (print-on-demand) PDF files to ensure visual and structural consistency. This is critical for maintaining brand quality across digital and print editions.

## When to Invoke

- User asks "do the PDFs match the EPUB chapters?"
- Before sending POD files to IngramSpark or print vendor
- After making changes to XHTML or CSS
- User mentions "print edition" or "PDF consistency"
- User asks "verify the PDFs are up to date"

## Workflow

### Run PDF Parity Verification

```bash
python3 scripts/pdf_verify.py \
  --root REBRANDED_OUTPUT \
  --targets docs/REBRANDED_VISUAL_AUDIT.json \
  --update-json
```

**What it does:**
1. For each of the 44 XHTML files:
   - Locates corresponding PDF in `REBRANDED_OUTPUT/pdf-pod/`
   - Compares:
     - Page count (XHTML rendered vs PDF pages)
     - Media box dimensions (PDF page size)
     - First-page visual hash (downscaled grayscale comparison)
     - Text extraction and paragraph continuity
2. If PDF is missing:
   - Generates temporary reference PDF via headless browser print-to-PDF
   - Uses this for comparison (but does NOT commit to repo)
   - Flags as "MISSING" in report
3. Updates `docs/REBRANDED_VISUAL_AUDIT.json` with:
   - `pdf_check` object for each chapter
   - Fields: `page_count_match`, `bbox_match`, `image_hash_delta`, `pdf_status`

## Comparison Metrics

### 1. Page Count Match

Compares rendered XHTML page count vs PDF page count.

**Example:**
```
Chapter IX: "Unveiling Your Creative Odyssey"
- XHTML rendered: 8 pages (at 6×9" print size)
- PDF actual: 8 pages
- Status: ✅ MATCH
```

**Acceptable variance:**
- Exact match: ✅ PASS
- ±1 page: ⚠️ WARN (minor reflow difference)
- ±2+ pages: ❌ FAIL (significant layout mismatch)

### 2. Media Box (Page Size)

Verifies PDF pages are correct physical dimensions.

**Expected for 6×9" POD:**
- Width: 432 points (6 inches × 72 DPI)
- Height: 648 points (9 inches × 72 DPI)

**Example:**
```
Chapter XV: Media box check
- Expected: 432×648 pt
- Actual: 432×648 pt
- Status: ✅ MATCH
```

### 3. Visual Hash Comparison

Computes perceptual hash of first page to detect visual differences.

**Process:**
1. Render XHTML first page as PNG (grayscale, downscaled to 200×300)
2. Convert PDF first page to PNG (same size)
3. Compute average hash for both
4. Calculate Hamming distance

**Scoring:**
- Hash delta 0-5: ✅ IDENTICAL (perfect match)
- Hash delta 6-15: ✅ SIMILAR (acceptable variance)
- Hash delta 16-30: ⚠️ DIFFERENT (minor layout shift)
- Hash delta >30: ❌ MISMATCH (significant visual difference)

**Example:**
```
Chapter IV: Visual hash comparison
- XHTML hash: d4a3f2c1...
- PDF hash: d4a3f2c1...
- Hamming distance: 3
- Status: ✅ IDENTICAL
```

### 4. Text Extraction

Extracts text from PDF and verifies key content is present.

**Checks:**
- Chapter title appears in first 500 characters
- Heading order matches XHTML heading structure
- Paragraph count is similar (±10%)

**Example:**
```
Chapter XII: Text extraction
- Title found: ✅ "Financial Wisdom"
- Headings: 12 in XHTML, 12 in PDF ✅
- Paragraphs: 84 in XHTML, 83 in PDF ✅ (within 10%)
- Status: ✅ PASS
```

## Interpreting Results

### JSON Output Structure

```json
{
  "file": "REBRANDED_OUTPUT/xhtml/9-chapter-i-unveiling-your-creative-odyssey.xhtml",
  "basename": "9-chapter-i-unveiling-your-creative-odyssey",
  "pdf_check": {
    "pdf_path": "REBRANDED_OUTPUT/pdf-pod/chapters/9-chapter-i-unveiling-your-creative-odyssey.pdf",
    "pdf_status": "ok",
    "page_count_match": true,
    "page_count_xhtml": 8,
    "page_count_pdf": 8,
    "bbox_match": true,
    "bbox_expected": [432, 648],
    "bbox_actual": [432, 648],
    "image_hash_delta": 3,
    "image_hash_verdict": "identical",
    "text_checks": {
      "title_found": true,
      "heading_count_match": true,
      "paragraph_variance_pct": 1.2
    }
  }
}
```

### Markdown Summary

Generated in `docs/REBRANDED_VISUAL_AUDIT.md`:

| File | PDF Status | Page Match | Visual Match | Issues |
|------|------------|------------|--------------|--------|
| 9-chapter-i-... | ✅ OK | ✅ 8 pages | ✅ Identical | None |
| 15-chapter-vi-... | ⚠️ OK | ⚠️ 10 vs 11 | ✅ Similar | +1 page variance |
| 22-chapter-xii-... | ❌ MISSING | N/A | N/A | PDF not found |

## Common Issues and Fixes

### Issue: Page Count Mismatch

**Symptom:** XHTML renders as 8 pages, PDF has 9 pages

**Possible causes:**
1. Extra blank page in PDF (page break issue)
2. Different margin settings between XHTML and PDF export
3. Widow/orphan control differences

**How to fix:**
1. Open PDF in Acrobat to verify blank page
2. Adjust `print-pod.css` orphans/widows settings:
   ```css
   p { orphans: 2; widows: 2; }
   ```
3. Re-export PDF from InDesign or print-to-PDF workflow
4. Re-run parity check to verify

### Issue: Visual Hash Mismatch

**Symptom:** Hash delta >30 (significant visual difference)

**Possible causes:**
1. Font substitution in PDF vs XHTML
2. Image resolution difference
3. Different CSS applied (print vs digital styles)

**How to fix:**
1. Open both side-by-side:
   - XHTML screenshot: `docs/screenshots/{basename}/title_1080x1440.png`
   - PDF page 1: Open in Acrobat, export as PNG
2. Identify visual difference (typography, spacing, images)
3. Adjust `print-pod.css` to match digital rendering
4. Regenerate PDF
5. Re-run parity check

### Issue: Missing PDF

**Symptom:** `pdf_status: "missing"`

**Action:**
1. Check if PDF was not generated yet for this chapter
2. Verify PDF naming matches XHTML basename:
   - XHTML: `9-chapter-i-unveiling-your-creative-odyssey.xhtml`
   - PDF should be: `9-chapter-i-unveiling-your-creative-odyssey.pdf`
3. If PDF exists with different name, rename to match
4. If PDF doesn't exist:
   - Generate from XHTML using print-to-PDF workflow
   - Place in appropriate `pdf-pod/` subdirectory

### Issue: Text Extraction Failure

**Symptom:** `text_checks.title_found: false`

**Possible causes:**
1. PDF is image-only (scanned, not text-based)
2. PDF has font embedding issues (text not extractable)
3. PDF was generated with text as outlines/curves

**How to fix:**
1. Verify PDF is text-based (select text in Acrobat)
2. If image-only, regenerate PDF from source XHTML
3. Ensure fonts are embedded as subsets (not outlines)

## Example Invocation

User: "Are the print PDFs in sync with the latest EPUB chapters?"

Agent response:
1. Run PDF parity checker
2. Read results from updated JSON
3. Summarize:

```
PDF Parity Check Complete
=========================

Total chapters: 44
PDFs verified: 42
Missing PDFs: 2

Results:
✅ PASS: 38 chapters (perfect parity)
⚠️ WARN: 4 chapters (minor variance)
❌ FAIL: 0 chapters (significant mismatch)
🔍 MISSING: 2 chapters (PDFs not found)

Warnings (4 chapters):
- Chapter VI: +1 page variance (11 vs 10) - Extra blank page in PDF
- Chapter XI: Visual hash delta 18 - Minor font rendering difference
- Chapter XV: Text variance 12% - Some paragraphs reflowed
- Chapter XXII: Media box 432×660 - Height should be 648

Missing PDFs (2 chapters):
- 30-SelfAssessment.xhtml (no matching PDF found)
- 43-DoodlePage.xhtml (no matching PDF found)

Recommended actions:
1. Fix page break in Chapter VI
2. Review font settings for Chapter XI
3. Generate missing PDFs for Self-Assessment and Doodle pages
4. Verify media box for Chapter XXII

Full report: docs/REBRANDED_VISUAL_AUDIT.md (PDF Parity column)
Detailed JSON: docs/REBRANDED_VISUAL_AUDIT.json (pdf_check objects)
```

## Integration with Other Skills

**Run after:**
- `epub-visual-auditor` - Ensure XHTML rendering is correct first

**Run before:**
- Sending POD files to print vendor
- Uploading to IngramSpark or KDP Print
- Final publication package

**Pair with:**
- `epub-publication-validator` - Comprehensive pre-publication check

## Notes

- PDF comparison requires `pypdf` and `Pillow` Python libraries
- First run may be slower (generates temporary PDFs for missing files)
- Temporary reference PDFs are stored in `/tmp/` and not committed to repo
- Visual hash comparison is perceptual (small rendering differences are OK)
- Re-run after any CSS or XHTML changes to verify parity maintained
