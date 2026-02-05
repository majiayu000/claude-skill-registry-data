---
name: tweakpane-visual-debugger
description: This skill should be used when debugging visual CSS and layout issues in the tweakpane-table plugin, specifically for investigating column alignment problems between table headers and data rows. Use when columns don't align, widths appear incorrect, or visual inspection of rendered output is needed.
---

# Tweakpane Visual Debugger

## Overview

Debug visual CSS and layout issues in the tweakpane-table plugin using Playwright browser automation. Measure actual element dimensions, compare DOM structures, inspect CSS properties, and identify root causes of alignment problems between table headers and data cells.

## When to Use This Skill

Use this skill in these scenarios:
- Columns don't align between headers and data rows
- CSS changes don't produce expected visual results
- Need to verify actual rendered dimensions vs expected
- Investigating why width properties aren't being applied
- Comparing CSS properties between headers and rows
- User reports "still looks the same" after fixes

## Debugging Workflow

### Step 1: Navigate to Test Page

Open the local test HTML file in the Playwright browser.

**Available test files:**
- `test/simple.html` - Basic 2-column table (Text, List)
- `test/advanced.html` - Complex 5-column table (Name, Type, Link, Trigger, Delete)

**Navigate using absolute path:**

```
Use mcp__playwright__browser_navigate
```

Construct the absolute path from the working directory (`/data/Workspace/helios/tweakpane-table`):

```
file:///data/Workspace/helios/tweakpane-table/test/simple.html
```

### Step 2: Capture Visual State

After navigation, capture both accessibility and visual information:

1. **Take accessibility snapshot:**
   ```
   Use mcp__playwright__browser_snapshot
   ```
   This provides the DOM structure in a text format.

2. **Take visual screenshot:**
   ```
   Use mcp__playwright__browser_take_screenshot
   ```
   Set `fullPage: false` for viewport screenshot, or `fullPage: true` for entire page.
   Save as: `alignment-issue-{timestamp}.png`

### Step 3: Measure Table Elements

Run the comprehensive measurement script to get precise dimensions and CSS properties.

**Execute measure_table.js:**

```
Use mcp__playwright__browser_evaluate

function: Read scripts/measure_table.js file content and pass as the function parameter
```

**Script returns:**
- Header cell dimensions and positions
- Row cell dimensions and positions
- CSS properties (flex, width, padding, margin, etc.)
- Inline styles applied
- Alignment differences calculated automatically

**Analyze the results for:**
- Width differences between header and row cells in same column
- Different flex-basis values
- Different padding/margin
- Missing inline styles (width not applied)

### Step 4: Compare DOM Structure

Run the structure comparison script to identify hierarchy differences.

**Execute compare_structure.js:**

```
Use mcp__playwright__browser_evaluate

function: Read scripts/compare_structure.js file content and pass as the function parameter
```

**Script returns:**
- Full DOM hierarchy for headers and rows
- Path to cells comparison
- Structural differences
- Tag/class mismatches
- CSS property differences at each level

**Look for:**
- Different nesting depths
- Extra wrapper elements in headers vs rows
- Different element types (buttons vs inputs)
- Class name differences

### Step 5: Inspect Specific Elements

If measurement scripts reveal issues, inspect specific elements interactively.

**Check inline styles:**

```javascript
() => {
  const headerCell = document.querySelector('.tp-headv .tp-lblv');
  const rowCell = document.querySelector('.tp-rowv .tp-lblv');

  return {
    header: {
      inlineWidth: headerCell.style.width,
      inlineFlex: headerCell.style.flex,
      allInlineStyles: headerCell.style.cssText
    },
    row: {
      inlineWidth: rowCell.style.width,
      inlineFlex: rowCell.style.flex,
      allInlineStyles: rowCell.style.cssText
    }
  };
}
```

**Check computed styles:**

```javascript
() => {
  const headerCell = document.querySelector('.tp-headv .tp-lblv');
  const rowCell = document.querySelector('.tp-rowv .tp-lblv');
  const hcs = window.getComputedStyle(headerCell);
  const rcs = window.getComputedStyle(rowCell);

  return {
    header: {
      width: hcs.width,
      flex: hcs.flex,
      flexBasis: hcs.flexBasis,
      flexGrow: hcs.flexGrow,
      flexShrink: hcs.flexShrink,
      minWidth: hcs.minWidth,
      maxWidth: hcs.maxWidth,
      padding: hcs.padding,
      boxSizing: hcs.boxSizing
    },
    row: {
      width: rcs.width,
      flex: rcs.flex,
      flexBasis: rcs.flexBasis,
      flexGrow: rcs.flexGrow,
      flexShrink: rcs.flexShrink,
      minWidth: rcs.minWidth,
      maxWidth: rcs.maxWidth,
      padding: rcs.padding,
      boxSizing: rcs.boxSizing
    }
  };
}
```

### Step 6: Identify Root Cause

Based on measurements and comparisons, identify the root cause:

**Common issues to check:**

1. **Width not applied**
   - Check if inline `width` or `flex` exists on cells
   - Verify width is applied to correct element (`.tp-lblv` not `.tp-lblv_v`)

2. **Flex properties overriding width**
   - Check if `flex: 1` on child `.tp-lblv_v` causes expansion
   - Verify `flex-grow: 0` and `flex-shrink: 0` are set
   - Should use `flex: 0 0 {width}` not just `width`

3. **Structural differences**
   - Different nesting levels between headers and rows
   - Different element types (buttons vs inputs)
   - Extra wrappers in one but not the other

4. **Padding/margin differences**
   - Different padding on header vs row cells
   - Different margin causing spacing issues

5. **Label visibility**
   - Labels visible in headers but hidden in rows
   - Creates extra width in headers

### Step 7: Reference Documentation

For deeper understanding, read the reference documentation:

**Tweakpane DOM structure:**
```
Read references/tweakpane-dom-structure.md
```

Explains:
- Core Tweakpane classes (`.tp-lblv`, `.tp-brkv`, `.tp-rotv`)
- Tweakpane-table plugin structure
- Where width should be applied
- Why `flex` is needed instead of `width`

**Common alignment issues:**
```
Read references/common-alignment-issues.md
```

Catalogs known issues:
- Headers wider than data cells
- Labels visible in wrong places
- Different padding
- Box-sizing mismatches
- Flex direction problems
- Min-width constraints

### Step 8: Report Findings

Structure the debugging report:

```markdown
## Visual Alignment Issue Analysis

### 1. Visual Evidence
[Screenshot showing the alignment issue]

### 2. Measurements
[Table showing header vs row widths for each column]

Column | Header Width | Row Width | Difference | Aligned?
-------|-------------|-----------|------------|----------
0      | 123.5px     | 98.2px    | 25.3px     | ❌
1      | 245.0px     | 245.0px   | 0px        | ✅

### 3. Root Cause
[Explanation of what's wrong]

Example: "Width is being set as inline `width` property, but the child `.tp-lblv_v` element has `flex: 1` which causes it to expand beyond the parent's width constraint."

### 4. CSS/DOM Differences
[List of specific differences between headers and rows]

### 5. Recommended Fix
[Specific code changes with file names and line numbers]

Example:
```javascript
// In src/head.ts line 126:
// Change from:
api.element.style.width = headerParams.width;

// To:
api.element.style.flex = `0 0 ${headerParams.width}`;
```

### 6. Verification Steps
[How to verify the fix works]
```

## Key Files Reference

When implementing fixes, check these files:

- `src/sass/plugin.scss` - CSS styles for table layout
- `src/head.ts` - Header implementation (line ~126: width application)
- `src/row.ts` - Row implementation (line ~112: RowPane.addBinding width application)
- `test/simple.html` - Basic test case
- `test/advanced.html` - Complex test case

## Testing After Fixes

1. Apply the recommended fix
2. Rebuild the plugin: `npm run build:dev`
3. Reload the test page in browser (hard refresh: Ctrl+Shift+R)
4. Re-run measurement scripts to verify alignment
5. Test both simple.html and advanced.html
6. Take new screenshots to confirm fix

## Resources

### scripts/

**measure_table.js** - Comprehensive measurement script that:
- Measures all header and row cell dimensions
- Captures CSS properties (computed and inline)
- Calculates alignment differences automatically
- Returns structured data for analysis

**compare_structure.js** - DOM structure comparison script that:
- Builds hierarchical tree of elements
- Compares header vs row structure
- Identifies tag/class/CSS mismatches
- Reports differences at each nesting level

### references/

**tweakpane-dom-structure.md** - Complete reference for:
- Tweakpane v4 DOM structure
- Core classes and their purposes
- Tweakpane-table plugin structure
- Width application requirements
- Common CSS rules

**common-alignment-issues.md** - Catalog of known issues:
- Issue symptoms and root causes
- Diagnostic procedures
- Solutions with code examples
- Prevention checklist
