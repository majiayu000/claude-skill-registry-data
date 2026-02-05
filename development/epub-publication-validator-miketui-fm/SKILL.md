---
name: epub-publication-validator
description: Run EPUBCheck and Ace accessibility validation. Use before final EPUB packaging or distribution to ensure publication readiness.
---

# EPUB Publication Validator Skill

## Purpose

Validate the EPUB package against EPUB 3.2 specification and WCAG 2.2 AA accessibility standards. This is the final gate before packaging and distributing the EPUB to retailers (Kindle, Apple Books, Kobo, etc.).

## When to Invoke

- User says "validate the EPUB" or "is this ready to publish?"
- Before running `npm run build:epub` for final packaging
- After making changes to XHTML, CSS, or content.opf
- User asks "does this pass EPUBCheck?"
- User mentions accessibility compliance or WCAG

## Workflow

### Step 1: EPUBCheck Validation

```bash
# Validate the entire EPUB package
epubcheck REBRANDED_OUTPUT/ --mode exp --save
```

**What it checks:**
- Package document (content.opf) validity
- Spine order and manifest completeness
- All XHTML files are well-formed XML
- No broken internal links
- Proper mimetype file
- META-INF/container.xml correctness
- Image dimensions and formats
- Font embedding compliance
- Navigation document (nav.xhtml) structure

**Expected output:**
- Pass: "No errors or warnings detected"
- Fail: List of errors with file paths and line numbers

### Step 2: Accessibility Validation (Ace by DAISY)

```bash
# Run Ace accessibility checker
ace -o docs/accessibility-report REBRANDED_OUTPUT/
```

**What it checks:**
- WCAG 2.2 AA compliance
- Image alt text presence and quality
- Heading hierarchy (no skips)
- Color contrast ratios
- ARIA landmark usage
- Language declarations
- Table headers and captions
- Semantic HTML structure

**Expected output:**
- HTML report at `docs/accessibility-report/report.html`
- JSON data at `docs/accessibility-report/ace.json`
- Violations categorized by severity (critical, serious, moderate, minor)

### Step 3: Metadata Completeness Check

```bash
# Extract and validate OPF metadata
python3 scripts/validate_metadata.py --opf REBRANDED_OUTPUT/content.opf
```

**What it checks:**
- Required fields: title, creator, language, identifier (ISBN)
- Recommended fields: publisher, date, subject, description
- Accessibility metadata: accessMode, accessibilityFeature, accessibilitySummary
- Modified date is current
- Subject keywords (should have 3-7 for discoverability)

### Step 4: Cross-Reference Validation

```bash
# Verify all manifest items exist on disk
python3 scripts/verify_asset_references.py --opf REBRANDED_OUTPUT/content.opf
```

**What it checks:**
- All `<item href="...">` files exist
- All images referenced in XHTML are in manifest
- All CSS files referenced exist
- All fonts referenced exist
- No orphaned files (files in directory but not in manifest)

## Interpreting Results

### EPUBCheck Results

**Common errors:**
- `RSC-005`: File not found in ZIP (missing manifest item)
- `OPF-007`: Spine item not in manifest
- `HTM-014`: Invalid XHTML markup
- `CSS-008`: Invalid CSS property value

**How to fix:**
1. Read the error message carefully (includes file path and line number)
2. Open the offending file
3. Fix the issue
4. Re-run EPUBCheck to verify

### Accessibility Results

**Critical violations (must fix):**
- Images missing alt text
- Insufficient color contrast (<4.5:1)
- Heading hierarchy skips
- Missing language declarations

**Serious violations (should fix):**
- Link text not descriptive ("click here")
- Table missing headers
- Form inputs without labels

**Moderate violations (nice to fix):**
- Redundant ARIA attributes
- Overly verbose alt text
- Missing ARIA landmarks

## Example Invocation

User: "Is the EPUB ready to upload to KDP?"

Agent response:
1. Run EPUBCheck
2. Run Ace accessibility check
3. Run metadata validation
4. Run asset reference check
5. Summarize results:

```
EPUB Publication Validation Results
====================================

EPUBCheck: ✅ PASS
- No errors or warnings detected
- All 44 spine items validated
- Manifest complete

Accessibility (Ace): ⚠️ 3 issues found
- CRITICAL: 0
- SERIOUS: 2 (missing alt text on 2 images)
- MODERATE: 1 (redundant ARIA attribute)

Metadata: ✅ COMPLETE
- All required fields present
- ISBN: 978-1-234567-89-0
- Language: en
- Accessibility metadata present

Asset References: ✅ ALL VALID
- 44 XHTML files verified
- 31 images verified
- 6 fonts verified
- No broken links

RECOMMENDATION: Fix 2 missing alt text issues before publication.
See: docs/accessibility-report/report.html for details.
```

## Pre-Publication Checklist

Before final packaging, ensure:

- [ ] EPUBCheck passes with 0 errors and 0 warnings
- [ ] Ace accessibility has 0 critical violations
- [ ] All serious violations addressed or documented
- [ ] Metadata includes ISBN, current date, publisher
- [ ] Tested in Kindle Previewer (for KDP submission)
- [ ] Tested in Apple Books simulator (for Apple Books submission)
- [ ] Tested in Adobe Digital Editions 4.5+
- [ ] Visual QA audit complete (all chapters PASS)
- [ ] PDF parity check complete (if POD edition exists)

## Integration with Other Skills

**Run after:**
- `epub-visual-auditor` - Fix visual issues before validation
- `css-diagnostics` - Remove unused CSS before validation

**Run before:**
- Final EPUB packaging (`npm run build:epub`)
- Distribution to retailers (KDP, Apple Books, IngramSpark)

## Notes

- EPUBCheck should run on the DIRECTORY (not a packaged .epub file) during development
- Ace requires Node.js 18+ and modern browser for report viewing
- Some warnings are acceptable (e.g., unused manifest items for alternate formats)
- Zero-error EPUBCheck is required for Apple Books submission
- Kindle Create and Kindle Previewer may flag additional issues not caught by EPUBCheck
