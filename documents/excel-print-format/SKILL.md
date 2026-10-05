---
name: excel-print-format
description: Format Excel workbooks for visually clean printing and presentation, with Chinese office-style typography, mixed Chinese/Latin font handling, visible-area-only print regions, fixed-scale layout when required, width-first page filling, row-height calculation from actual wrapped line counts, group-aware pagination, and dedicated print-sheet fallback for hidden-column-heavy workbooks. Use when the user asks to make a spreadsheet 美观, 适合打印, 适合汇报, 调整打印格式, 排版成 A4 或 A3, 横版竖版优化, or wants an Excel file turned into a polished print-ready version rather than a calculation workbook.
---

# Excel Print Format

## Overview

Use this skill when the user wants an Excel file to look clean, formal, and print-ready.

This skill is separate from `xlsx`. `xlsx` focuses on data, formulas, and workbook logic. This skill focuses on layout, typography, page setup, and printable presentation.

## When To Use

Use this skill when the user asks for any of the following:

- Make an Excel file more beautiful
- Make a sheet suitable for printing
- Choose A4 or A3 automatically
- Optimize portrait vs landscape
- Reformat a table for reporting or leadership review
- Create a print-friendly version of a wide or messy workbook

Do not use this skill as the default tool for:

- complex formula modeling
- data cleaning as the primary goal
- repairing workbook logic
- heavy analytical work where printing is not the goal

For those cases, use `xlsx`.

## Design Goal

This skill should optimize for visual clarity under real print constraints, not for rigid template matching.

Preferred outcomes:

- clean and formal
- readable at normal print size
- dense but not crowded
- visually balanced
- key information obvious at a glance
- minimal wasted space
- the overall content block on each printed page should have a visual aspect ratio close to the selected paper size

## Core Rules

### Typography

Use this default font system unless the user explicitly overrides it:

- main title: `方正小标宋_GBK`
- table headers: `方正黑体_GBK`
- body text: `方正仿宋_GBK`
- notes or remarks: `方正楷体_GBK`
- English letters, digits, and half-width symbols: `Times New Roman`

If the preferred fonts are unavailable, use locally available near-equivalent Chinese fonts while preserving the same role split between title, headers, body text, and notes.

Mixed-content cells should keep Chinese text in the Chinese font and apply `Times New Roman` only to Latin runs. Formula cells may be formatted at the whole-cell level, but do not assume stable rich-text run splitting inside formula results.

### Direct Print Or Print Sheet

If the source sheet prints cleanly, format it directly. If it is a working sheet with many hidden helper columns, dense formulas, or an obviously messy print result, keep the original sheet unchanged and create a continuous print-facing sheet instead.

### Execution Order

1. Fix paper size, orientation, margins, and whether scaling must stay at `100%`.
2. Determine the effective print area from visible content only.
3. Restore hidden-column intent from the original workbook definition when compatibility loading changes it.
4. Set column widths first and fill the printable width before touching row heights.
5. Set row heights from wrapped line counts.
6. Apply visual structure and alignment.
7. Paginate last.

### Wrapped Line Rules

Use these formulas for row-height logic:

- one-line capacity for pure Chinese text:
  `N = W × 6 / F`
- row height:
  `H = (1.25 × F + 1) × (LineCount + 1) - 1.5 × LineCount`

Where:

- `W` = Excel/WPS column width
- `F` = font size
- `LineCount` = maximum wrapped line count among all visible cells in the row

For mixed text, count Chinese/full-width characters as `1` and half-width Latin letters, digits, and punctuation as `0.5`.

### Visual Defaults

- title area is borderless by default
- title-adjacent metadata such as date, unit, scope, or remarks may default to centered alignment when no strong source layout exists, but a clear original alignment should usually be preserved
- regular border weight by default; no bold outer frame unless requested
- white background by default
- text-heavy columns should stay readable rather than being over-compressed
- short text may be centered; longer text should usually be left-aligned
- keep title, unit, date, and remarks compact rather than padding the title block

### Pagination Rules

- paginate only after widths, heights, and structure are stable
- do not use scaling to solve pagination unless the user explicitly allows a bounded final window such as `95%-100%`
- keep section titles off the bottom of a page
- keep vertically merged groups on one page when practical
- prioritize fuller non-last pages; the last page may be relatively sparse

## Validation Checklist

Before considering the layout complete, verify:

- fixed scaling requirements are still respected
- the print area contains only visible, effective content
- hidden helper columns were preserved rather than deleted
- title and section merges do not extend into hidden columns
- rows with the same maximum wrapped line count share the same height
- no cell appears to hide text under the current font, width, and row-height rules
- section titles do not appear at the bottom of a page
- vertical merged groups do not split across pages when they can be moved intact
- English letters and digits appear in `Times New Roman`
- if a dedicated print-facing sheet was created, the original source sheets remain unchanged

## References

For the printable layout rules and the aesthetic decision heuristics, read:

- `references/print-rules.md`

## Resources

### references/

- `references/print-rules.md`: detailed layout and print heuristics

