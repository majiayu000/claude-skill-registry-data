---
name: gaas-relatorio-xlsx
description: Build, extend, or improve the in-app XLSX report exporters behind the
  GaaS "Relatório" tab (calendar-estrategico React/TS app). Covers adding a new export
  button + workbook, adding a new sheet/section to an existing report, adding MoM
  (month-over-month) comparison, and reusing the shared ExcelJS report helpers. Use
  this whenever the user asks to create/expand/melhorar a planilha or relatório exportável,
  add a new report view/aba/sheet, add MoM/comparison columns, wire a new "Exportar
  XLSX" button in RelatorioView, or work with crmAquisicaoMonthlyReportExport / midiaPagaMonthlyReportExport
  / aquisicaoCrmExcelExport / rentabilizacaoCrmExcelExport. Trigger even when the
  user only says "expandir os xlsx do relatório", "outra visão da planilha", or names
  a Supabase table (activities, paid_media_metrics, b2c_daily_metrics) as a report
  source.
metadata:
  version: 1.0.0
  origin: claude-projeto
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Relatórios
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# GaaS Relatório XLSX Exporter

Guide for building and extending the browser-side XLSX report exporters in `calendar-estrategico`. These run in the React app (not Python): a button in the Relatório tab fetches from Supabase, builds an ExcelJS workbook in-memory, and triggers a browser download. There is one canonical, validated implementation you mirror for everything new: the CRM monthly MoM report. Copy its shape rather than inventing a new one — consistency is the whole point.

Read [references/architecture.md](references/architecture.md) for the file map and the shared-helper API before writing code. Read [references/patterns.md](references/patterns.md) for copy-ready code (fetch, analysis, writers, reconciliation, download, button wiring). Read [references/validation-harness.md](references/validation-harness.md) to test a new/changed export headlessly (real Supabase data, no browser) before committing.

## The reference implementations

- `src/utils/crmAquisicaoMonthlyReportExport.ts` — the canonical MoM report and the home of every shared helper (`REPORT_COLORS`, `reportDelta`, `reportPctText`, `styleReportDelta`, `setCellValue`, `writeReportHeader`, `writeSectionTitle`, `weekWindows`, `previousWeekWindows`, `monthStart/monthEnd/previousMonthStart`, `MONTHS_PT`, `dayOfMonthReport`, type `WeekWindow`). If you need a helper in a new file, import it from here. If it isn't exported yet, add the `export` keyword — never copy-paste a helper.
- `src/utils/midiaPagaMonthlyReportExport.ts` — the most complete worked example: cards + MoM, per-frente table, weekly pacing (spend & clicks), per-platform, per-creative, plus a validation gate and multi-sheet workbook. Best template for a brand-new report.
- `src/utils/midiaPagaDiarizadoSheet.ts` — a `write<Name>Sheet(workbook, ...)` that appends one sheet to an existing workbook (daily pacing cockpit). Model for "add another sheet".
- `src/utils/aquisicaoCrmExcelExport.ts` — the diarized CRM export; owns `fetchSupabaseRows` (paginated `activities` fetch) and the `downloadBuffer` browser helper pattern.
- `src/components/RelatorioView.tsx` — where the buttons and `useCallback` handlers live (search `exportAquisicaoCrmMonthly` for the pattern to clone).

## When the task is: add a whole new report (new button + file)

1. Create `src/utils/<name>ReportExport.ts`. Import shared helpers from `crmAquisicaoMonthlyReportExport`. Structure the file top-to-bottom: types/consts → classification (if any) → derived-metric helpers → fetch → `build<Name>Analysis()` (aggregation + reconciliation throw) → `write*` section writers → `write<Name>Sheet(workbook, analysis)` → `export async function export<Name>Xlsx(start, end)` wrapper.
2. The wrapper mirrors `exportAquisicaoCrmMonthlyXlsx` (see [references/patterns.md](references/patterns.md)): resolve `monthStart`/`previousMonthStart`, fetch month M and M-1, `await import('exceljs')`, build the workbook, `writeBuffer()`, `downloadBuffer(buffer, ` Report_${MONTHS_PT[m]}_<Tipo>.xlsx `)`.
3. Wire the button in `RelatorioView.tsx`: add an `isExporting<Name>` state, a `export<Name>` `useCallback` (try/catch with `window.alert` on failure, deps `[periodEnd, periodStart]`), and a `<button>` next to the CRM monthly one using the same classes (pick a distinct accent color).
4. Validate headlessly (see below), then build.

## When the task is: add a sheet to an existing workbook

Write a `write<Sheet>Sheet(workbook, data, ...)` in its own file that calls `workbook.addWorksheet(...)`, and call it from the wrapper after the other sheets. Preserve sheet order the user expects. Note ExcelJS in the browser cannot render charts — a ported chart-heavy sheet becomes values/tables only; say so.

## When the task is: add MoM / comparison to metrics

Fetch M-1 alongside M, aggregate both, and for each metric emit the value then a Δ cell: `reportPctText(reportDelta(cur, prev))` for the text, `styleReportDelta(cell, delta, invert)` for the color. `invert=false` for volumes (up = green/good); `invert=true` for costs/efficiency like CPC/CPM/CPL/CAC (down = green/good). `reportDelta` returns `null` when the previous value is 0/undefined, which renders as a gray "—" — never a divide-by-zero or a throw.

## Non-negotiables (these hold across every report)

- **Reconciliation gate.** Before returning the workbook, assert that section totals reconcile with the month total (e.g. Σ by-frente spend == Σ by-platform == Σ weekly == month total). Use a cents tolerance (`Math.abs(a-b) <= 0.01`) for summed floats, exact `===` for integer counts. On mismatch `throw new Error('Validação falhou: ...')` so a wrong file is never generated.
- **Classify by the campaign name tag, never by a dirty enum field** (e.g. `objective`). The Mídia Paga frente rules and their exact precedence live in [references/patterns.md](references/patterns.md). Copy the precedence order verbatim.
- **Reuse the visual system.** Freeze `C3` (`xSplit:2, ySplit:2`), Arial, `showGridLines:false`; header row `REPORT_COLORS.slate` on white; cards `REPORT_COLORS.card`; warnings `REPORT_COLORS.note`/`noteText`; TOTAL row `REPORT_COLORS.total`. Number formats: integers `#,##0`, currency `"R$" #,##0.00`, rates `0.00%` (store CTR as the raw fraction, not ×100). Everything flows through `setCellValue`.
- **Keep the caveats.** GaaS data has known traps (platform conversions are events not cards; tracking breakages). If the source report carries a yellow warning box, the new one keeps it — don't silently drop it.

## Validate before you commit

Always exercise a new or changed export against real Supabase data before declaring it done. The app path (button → download) can't run in a headless shell, but every builder is a pure function of its rows, and `supabaseClient.ts` has hardcoded credentials (no `import.meta.env`), so you can bundle a tiny harness with `esbuild` and run it in Node: fetch real rows, call `build*Analysis` + the `write*Sheet` functions, write the `.xlsx`, reopen it, and assert the headline totals reconcile. Full template in [references/validation-harness.md](references/validation-harness.md). Delete the temp harness before committing. Then run `npm run build` and confirm `tsc` is clean on the touched files.

## Committing / deploying (repo gotcha)

The real project repo is the **nested** `calendar-estrategico/` repo (remote `growthafinz/GaaS-Framework-Afinz`), not the git repo rooted at the user's home folder — running git from the project dir resolves to the home repo, which does **not** track these files. Always run git with `-C` pointed at `calendar-estrategico`, and there are usually unrelated uncommitted changes from other work in that repo, so **stage only your specific files by path** (never `git add -A`). Deploy is a push to `main` (that triggers the GaaS deploy) — do it only when the user asks.
