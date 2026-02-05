---
name: css-diagnostics
description: Analyze CSS coverage, identify unused rules, and detect stylesheet conflicts. Use after visual QA to optimize stylesheets before publication.
---

# CSS Diagnostics Skill

## Purpose

Analyze CSS usage across all 44 XHTML chapters to identify:
- Unused selectors (dead code)
- Classes/IDs used in XHTML but missing in CSS
- Conflicting or redundant rules
- Opportunities for stylesheet consolidation

## When to Invoke

- User asks "are there unused CSS rules?"
- After completing visual QA audit
- Before final EPUB packaging (to reduce file size)
- User mentions slow rendering or bloated stylesheets
- User asks "which CSS rules are actually used?"

## Workflow

### Run CSS Coverage Analysis

```bash
python3 scripts/css_coverage_analyzer.py \
  --root REBRANDED_OUTPUT \
  --targets docs/REBRANDED_VISUAL_AUDIT.json \
  --out docs/CSS_COVERAGE.md
```

**What it does:**
1. Scans all 44 XHTML files for:
   - Classes (`class="..."`)
   - IDs (`id="..."`)
   - Element selectors (h1, p, img, etc.)
2. Parses both CSS files:
   - `REBRANDED_OUTPUT/xhtml/styles/style.css` (digital)
   - `REBRANDED_OUTPUT/xhtml/styles/print-pod.css` (POD print)
3. Generates coverage report:
   - Used selectors (appears in both XHTML and CSS)
   - Unused selectors (in CSS but not used in any XHTML)
   - Missing selectors (in XHTML but not defined in CSS)
   - Redundant rules (duplicate declarations)
4. Outputs:
   - `docs/CSS_COVERAGE.md` (human-readable summary)
   - `docs/CSS_COVERAGE.json` (detailed machine-readable data)

## Interpreting Results

### Coverage Summary

```
CSS Coverage Analysis
=====================

Total selectors defined: 487
Total selectors used: 412
Unused selectors: 75 (15.4%)
Missing definitions: 8 (1.9%)

File sizes:
- style.css: 27.3 KB
- print-pod.css: 9.8 KB
- Combined: 37.1 KB
```

**Metrics:**
- **<10% unused**: Excellent (tight, well-maintained CSS)
- **10-20% unused**: Good (normal for evolving projects)
- **20-40% unused**: Fair (consider cleanup before publication)
- **>40% unused**: Poor (significant bloat, requires refactoring)

### Unused Selectors

Example output:
```
Unused Selectors (75 total)
===========================

.legacy-chapter-title { ... }     # Safe to remove
.old-quiz-style { ... }            # Safe to remove
.experimental-layout { ... }       # Safe to remove
.chapter-summary { ... }           # May be used in future chapters
```

**Action items:**
1. Review each unused selector
2. Verify it's not used in:
   - Templates (may be used when generating new chapters)
   - Future chapters (planned but not yet created)
   - Print-specific layouts (may only appear in POD version)
3. If confirmed unused:
   - Comment out (for testing)
   - Remove entirely (after testing)

### Missing Definitions

Example output:
```
Missing CSS Definitions (8 total)
=================================

.worksheet-answer-box          # Used in chapters 9, 15, 22
.reflection-prompt             # Used in chapters 11, 16, 27
.smart-goal-template           # Used in chapter 40
```

**Action items:**
1. Add definitions to `style.css`:
   ```css
   .worksheet-answer-box {
     border: 1px solid #ccc;
     padding: 1em;
     margin: 1em 0;
     background: #f9f9f9;
   }
   ```
2. Test in visual QA to verify rendering
3. Re-run CSS coverage to confirm

### Conflict Detection

Example output:
```
Potential Conflicts
===================

.chapter-title is defined in:
  - style.css line 147
  - print-pod.css line 89
  (Conflicting font-size values: 2.5rem vs 3rem)

.footnote is defined twice in style.css:
  - Line 203 (font-size: 0.85rem)
  - Line 456 (font-size: 0.9rem)
```

**Action items:**
1. Resolve conflicts by:
   - Using media queries (`@media print { ... }`)
   - Removing duplicate definitions
   - Using more specific selectors
2. Test across viewports to ensure no regressions

## Optimization Opportunities

After running diagnostics, consider:

### 1. Remove Unused Selectors
- Backup current CSS: `cp style.css style.css.backup`
- Remove confirmed dead code
- Re-run visual QA to verify no regressions
- Potential savings: 10-30% file size reduction

### 2. Consolidate Redundant Rules
```css
/* Before */
h1 { font-family: "Cinzel"; font-weight: 700; }
h2 { font-family: "Cinzel"; font-weight: 700; }
h3 { font-family: "Cinzel"; font-weight: 700; }

/* After */
h1, h2, h3 { font-family: "Cinzel"; font-weight: 700; }
```

### 3. Extract Common Patterns
```css
/* Before */
.chapter-intro { margin: 2em 0; padding: 1em; }
.section-intro { margin: 2em 0; padding: 1em; }

/* After */
.intro-block { margin: 2em 0; padding: 1em; }
/* Update XHTML classes accordingly */
```

### 4. Split CSS by Usage
If analysis shows clear separation:
- `typography.css` - Font declarations, text styles
- `layout.css` - Spacing, positioning, grid
- `components.css` - Worksheets, quizzes, callouts
- `print.css` - Print-specific overrides

## Example Invocation

User: "The CSS files seem large. Can you check if there's unused code?"

Agent response:
1. Run CSS coverage analyzer
2. Read `docs/CSS_COVERAGE.md`
3. Summarize findings:

```
CSS Coverage Analysis Complete
===============================

Current state:
- Total CSS: 37.1 KB (487 selectors)
- Used: 412 selectors (84.6%)
- Unused: 75 selectors (15.4%)
- Missing: 8 selectors (need definitions)

Top opportunities:
1. Remove 75 unused selectors → Save ~5.2 KB (14% reduction)
2. Consolidate 12 redundant rules → Save ~0.8 KB
3. Add 8 missing definitions for worksheet elements

Estimated optimized size: 31.9 KB (14% reduction)

Recommended actions:
1. Review unused selectors in CSS_COVERAGE.md
2. Add missing worksheet/reflection styles
3. Test visual QA after changes
4. Consider splitting into modular CSS files

Full report: docs/CSS_COVERAGE.md
```

## Integration with Other Skills

**Run after:**
- `epub-visual-auditor` - Understand which styles are actually rendered

**Run before:**
- `epub-publication-validator` - Clean CSS before final validation
- Final packaging - Smaller CSS = faster EPUB load times

## Notes

- CSS coverage is computed per XHTML file (not live browser rendering)
- Pseudo-classes (`:hover`, `:focus`) may be flagged as unused (ignore these)
- Print-specific rules may only appear when generating PDFs (keep these)
- Some selectors may be defensive (future-proofing) - use judgment before removing
- Re-run coverage after any CSS changes to verify impact
