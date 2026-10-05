---
name: fst-payroll-georgia
description: >-
  Georgia (FiberCell) timesheet and payroll: month timesheet, brigades, roll
  call, night shifts, cell codes (В/ОО/ПР/X/Н), wages, advances, deductions,
  accrual multipliers, and finance statements. Use when changing табель,
  бригады, перекличка, ночные смены, коды ячеек, зарплата, авансы, удержания,
  or Georgian payroll rules.
---

# FST Payroll — Georgia (FiberCell)

Use when implementing or auditing salary calculation, payroll statements, or matching Excel accrual sheets.

## Source of truth

| Layer | Path |
|-------|------|
| Rates & norms (defaults) | `src/lib/payrollRates.ts` |
| Editable accrual handbook | `settings.payrollAccrual` + `src/lib/finance/payrollAccrualRules.ts` · UI: Справочники → Начисления |
| Row calculation | `src/lib/payroll.ts` |
| Finance aggregation | `src/lib/finance/calc.ts` |
| Excel export | `src/lib/excelExport.ts` (`exportPayrollStatementExcel`) |
| Print statement | `src/components/finance/PrintPayrollStatementSheet.tsx` |
| Screenshot salaries | `fst-web/scripts/salaryScreenshotData.mjs` |

## Hourly rate from monthly salary

- **Norm for rate** = full calendar-month hours by schedule (`fullScheduleMonthHours`): 5/2 = weekdays×shift (minus GE holidays); 2/2 = full cycle month — **not** truncated by hire date / row period.
- Example: hire on the 10th, timesheet plan 128h, July 5/2 norm 184h → `rate = salary / 184`, pay ≈ 128/184×salary if all plan worked.
- Timesheet **plan hours** still show the truncated plan (128); OT Δ uses sheet plan, not the rate norm.
- `SHIFT_MONTH_HOURS` / `SCHEDULE_52_MONTH_HOURS` are deprecated fallbacks only.
- Directory **Справочники → Начисления** edits night/idle/OT % only (not hour norms).

## Accrual flow (plan → fact → pay)

1. **Plan** sets expected shift (used for ОТ/Б/ПР hour basis)
2. **Fact** codes + optional `+N` extra hours + `factHoursOverride` drive pay
3. **`calculateRowPay`** runs live on every finance/payroll view (not stored until month close snapshot)

Per work day:
- Base 100% up to code norm (11, 8, …)
- Hours above norm (override or +N) → OT tiers 110/115/120%
- Night Н → 125% on shift hours + tiers on excess
- ПР → 100% of planned shift hours

## Accrual multipliers (Excel-aligned)

| Component | Code / field | Multiplier |
|-----------|--------------|------------|
| Base shift | 8, 11, 22 | 100% |
| Night | Н | 125% |
| Overtime tier 1 | factExtra 1st hour/day | 110% |
| Overtime tier 2 | 2nd hour | 115% |
| Overtime tier 3 | 3+ hours | 120% |
| Idle | ПР | 30% of planned shift hours |
| Night line (impregnation) | Н + line brigade | +20 ₾ per such night (`settings.payrollAccrual.nightLineFixedGel`), **on top of** 125% hours |
| Vacation | ОТ | plan shift hours × rate |
| Sick | Б | plan shift hours × rate (after finance confirmation) |
| Unpaid | ОО, X | 0 |

Overtime tiers apply **per day** via `factExtraHours` on work-day codes.

Idle (ПР): hours = planned shift for that day, or `effectiveShiftHours(emp)` if plan was off.
Pay at `IDLE_MULTIPLIER = 0.3` (30%).

**Month-Δ path** (`workFactHours > workNorm`):
`workNorm = plan − (ПР in plan + confirmed ОТ + confirmed Б)`.
Base = `workNorm×rate`; OT on `workFact − workNorm` (110%).
ПР/ОТ/Б are paid in their own buckets — never stacked on top of full `plan×rate`.
ПР after reclass is paid at 30%, not 100%.

## PayBreakdown fields

`base`, `night`, `overtime` (sum), `ot110`, `ot115`, `ot120`, `idle`, `vacation`, `sick`, `nightLineBonus`

## Roster gap (June 2026 screenshot)

17 employees were missing from seed; added as `emp-81`…`emp-97` in `src/data/seed-employees.json` with aliases in `salaryScreenshotData.mjs`.

Manual-skip duplicates (do not auto-match): `kvantaliani giorgi`, `rusov giorgi`, `chukuadze beka`, `chilashvili giorgi active`.

## Verification workflow

1. Run `apply-screenshot-salaries --dry-run` against cloud or local employees
2. Compare finance statement totals with Excel «ИТОГО в ЗП»
3. Check breakdown columns: base, night, OT tiers, idle, vacation
4. Print: Finance → Расчётная ведомость → «Печать ведомости»

## Do not

- Reintroduce flat ×1.5 overtime — use tiered rates in `payrollRates.ts`
- Pay ПР as 0 or 100% — idle is **30%** (`IDLE_MULTIPLIER`)
- Change `SHIFT_MONTH_HOURS` without updating `apply-screenshot-salaries.mjs`
