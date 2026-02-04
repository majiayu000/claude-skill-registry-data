---
name: epub-visual-auditor
description: Run and interpret visual QA pipeline for EPUB XHTML files. Use when user asks about layout, screenshots, visual issues, or rendering problems in REBRANDED_OUTPUT.
---

# EPUB Visual Auditor Skill

## Purpose

Run the comprehensive visual QA pipeline to detect layout, typography, and rendering issues across all 44 chapter XHTML files in `REBRANDED_OUTPUT/`. Generate screenshots, analyze computed styles, and produce actionable reports.

## When to Invoke

- User asks about visual layout or rendering issues
- User requests screenshot comparison across viewports
- User wants to verify chapter formatting consistency
- User needs a visual audit before publication
- User mentions "how does chapter X look" or "check the layout"

## Workflow

### Step 1: Discover Targets
```bash
python3 scripts/find_44_targets.py \
  --opf REBRANDED_OUTPUT/content.opf \
  --out docs/REBRANDED_VISUAL_AUDIT.json
```

**What it does:**
- Parses `content.opf` spine to extract exactly 44 chapter files in reading order
- Creates initial JSON report with file paths and metadata
- Records selection strategy and any ambiguities

**Expected output:**
- `docs/REBRANDED_VISUAL_AUDIT.json` with 44 entries

### Step 2: Visual Review
```bash
python3 scripts/visual_review.py \
  --root REBRANDED_OUTPUT \
  --targets docs/REBRANDED_VISUAL_AUDIT.json \
  --screenshots-dir docs/screenshots \
  --gallery docs/gallery/index.html
```

**What it does:**
- Launches headless Chromium via Playwright
- Renders each XHTML at two viewports: `768x1024` and `1080x1440`
- Captures screenshots:
  - Title/top-of-document view
  - Worksheets/interactive content
  - Complex layouts (tables, figures, multi-column)
- Computes style samples for h1–h3, paragraphs, lists, images
- Detects layout issues:
  - Missing fonts, suspicious fallbacks
  - Text/image overflow or clipping
  - Images exceeding viewport width
  - Heading hierarchy violations
  - Accessibility issues (alt text, contrast, ARIA)

**Expected output:**
- `docs/screenshots/{basename}/title_768x1024.png` (and 1080x1440 variant)
- `docs/screenshots/{basename}/worksheets_768x1024_p1.png` (if applicable)
- `docs/screenshots/{basename}/complex_768x1024_p1.png` (if applicable)
- Updated JSON with `computed_style_samples`, `issues`, `screenshots` arrays
- `docs/REBRANDED_VISUAL_AUDIT.md` with 44-row summary table

### Step 3: Interpret Results

After visual review completes:

1. **Read the markdown summary:**
   ```bash
   cat docs/REBRANDED_VISUAL_AUDIT.md
   ```

2. **Check for failures:**
   - Look for chapters with "FAIL" verdict
   - Review key issues column for recurring problems

3. **Inspect JSON for details:**
   ```bash
   jq '.files[] | select(.issues | length > 0)' docs/REBRANDED_VISUAL_AUDIT.json
   ```

4. **View screenshots in gallery:**
   - Open `docs/gallery/index.html` in browser
   - Use keyboard navigation to compare viewports

5. **Summarize findings for user:**
   - Report total PASS vs FAIL count
   - Highlight top 3-5 recurring issues
   - Recommend specific CSS or XHTML fixes
   - Link to affected chapter line numbers when possible

## Example Invocation

User: "Can you check if the chapter layouts look good on tablets?"

Agent response:
1. Run Step 1 (discover targets)
2. Run Step 2 (visual review)
3. Wait for completion
4. Read results and provide summary:

```
Visual QA Complete: 44 chapters analyzed
- PASS: 41 chapters
- FAIL: 3 chapters (issues detected)

Common issues found:
1. Chapter IX: Heading hierarchy skip (h1 → h3 without h2) - Line 47
2. Chapter XV: Image overflow on 768px viewport - Line 203
3. Multiple chapters: Missing alt text on decorative images

Recommended fixes:
- Insert missing h2 in Chapter IX
- Add max-width: 100% to image styles
- Add alt="" role="presentation" to decorative images

View full report: docs/REBRANDED_VISUAL_AUDIT.md
Gallery: docs/gallery/index.html
```

## Capabilities

- ✅ Render XHTML with local CSS (no network requests)
- ✅ Capture screenshots at 2 viewport sizes
- ✅ Detect overflow, clipping, font issues
- ✅ Validate heading hierarchy
- ✅ Check image alt text presence
- ✅ Compute style samples for typography analysis
- ✅ Generate interactive screenshot gallery
- ❌ Does NOT modify XHTML or CSS files automatically
- ❌ Does NOT fix issues (only reports them)

## Integration with Other Skills

**Pair with:**
- `css-diagnostics` - After visual audit, analyze CSS coverage for unused rules
- `pdf-parity-checker` - Verify XHTML rendering matches POD PDFs
- `epub-publication-validator` - Run EPUBCheck after fixing visual issues

## Notes

- First run may take 2-3 minutes (Playwright downloads Chromium if needed)
- Subsequent runs are faster (~30 seconds for 44 files)
- Screenshots are cached; delete `docs/screenshots/` to regenerate
- Gallery requires modern browser (Chrome, Firefox, Safari)
