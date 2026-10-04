---
name: xlsx
description: Create, read, and edit ordinary Excel XLSX workbooks with openpyxl, including data, formulas, formatting, and print layout.
---

# Excel workbooks

openpyxl 3.1.5 is preinstalled. Run scripts with `office-python`. Do not install packages. Restore attachments with materialize_chat_files and copy them into the workspace before editing. Keep the original.

Use `Workbook()` for new files and `load_workbook(path, data_only=False)` for edits. Inspect sheets, formulas, styles, merged cells, and print settings first. `data_only=True` reads cached results and must not be used for an edit/save workflow that needs to preserve formulas. openpyxl does not calculate formulas.

Use formulas where the user needs recalculation, preserve numeric/date types, and apply readable number formats. Set print areas for all intended visible data, column widths, row heights, repeated headers, and sensible page orientation. Fit to page width without forcing a long sheet onto one unreadable page. Do not hide content or narrow a print area to evade review.

Scope is ordinary XLSX. Unsupported features such as macros or modifications that could lose existing shapes require a clear limitation, not a silent lossy rewrite. Inspect and preserve the source before saving a copy.

Call validate_office_file on the saved workbook. It checks the package and readability and uses a temporary LibreOffice Calc copy to check recalculated formulas without overwriting your file. Formula checking uses Calc, not Microsoft Excel; static rendering does not prove external data connections or interactive features work. For formula-driven new workbooks, request recalculation on open with `CalcProperties(fullCalcOnLoad=True)` from `openpyxl.workbook.properties`.

Render every output page with render_office_preview and verify data, headings, formula results, print coverage, clipped cells, and page breaks. Record visual_reviews through validate_office_file with the source_sha256. Any edit requires fresh validation and review. After three unsuccessful repair cycles explain the blocker without attaching the draft. Finish only when approved is true.
