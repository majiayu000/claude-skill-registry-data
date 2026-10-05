---
name: fst-domain-invariants
description: Verified Otgruzka business invariants — month close, documents, warehouse, payroll, roles, SQL truth, journals.
---

# fst-domain-invariants

Проверенные правила домена. При изменении логики — не нарушать без явного ADR/просьбы.

**Данные прод:** SQL Connect (`OTGRUZKA.md`). **UI канон:** Vercel.

## SQL & anti-wipe

| Invariant | Code |
|-----------|------|
| Mass wipe refused before cloud save | `assertNoMassStoreWipe` — `src/lib/cloud/refuseStoreWipe.ts` |
| SQL sync path | `FstSqlConnectSync.tsx` |
| Policy doc | `OTGRUZKA.md`, `fst-data-integrity.mdc` |

Пороги wipe: employees, users, timesheet cells, auditLog, warehouse, finance, sales, procurement, hrContracts, roleViews/webViews.

## Closed periods

| Domain | Functions |
|--------|-----------|
| Month sheet | `isMonthClosed`, `isMonthWriteLocked`, `setMonthClosed` — `src/lib/monthManage.ts`, `settingsSlice` |
| Warehouse period | `isWarehousePeriodClosed` — `src/lib/warehouse/periodClose.ts` |
| Finance on closed month | guards in `financeSlice.ts` via `isMonthClosed` |

## Timesheet

| Invariant | Code |
|-----------|------|
| Draft batch commit | `commitTimesheetDraft` — `timesheetSlice.ts` |
| Document void | `voidTimesheetEntry` |
| Entry apply/revert | `applyTimesheetEntryChanges`, `revertTimesheetEntryApplied` — `src/lib/timesheetEntries/` |
| Actor permissions | `canMutateTimesheet`, `resolveTimesheetActorUser` — `timesheetGuard.ts` |
| Scope / substitution | `timesheetAccess`, `timesheetScope.ts` |

## Warehouse documents

| Action | Code |
|--------|------|
| Post | `postWarehouseDocument`, `postWarehouseDoc` — `documents.ts`, `warehouseSlice` |
| Unpost | `unpostWarehouseDocument`, `roleAllowsDocumentUnpost` |
| Cancel/void | `cancelWarehouseDocument`, `roleAllowsDocumentCancel` |
| Validation | `validateWarehouseDocumentInput` |
| Statuses | `WarehouseDocumentStatus` — `src/lib/warehouse/types.ts` |

## Procurement → warehouse

Приёмка проводится в складские документы — см. `fst-procurement` + `warehouseSlice` posting paths.

## Production chain (high level)

Sales/director → planner → production requests → formulations/mixer → warehouse movements.<br>
Детали: `docs/ARCHITECTURE.md`, `fst-architecture`.

## Payroll (Georgia)

| Invariant | Code |
|-----------|------|
| Month statement | `monthStatement`, `employeeLedger` — `src/lib/finance/calc.ts` |
| Row pay | `calculateRowPay` — `src/lib/payroll.ts` |
| Rates | `resolvePayRate`, `effectiveHourlyRate` — `payrollRates.ts` |
| Brigadier | `computeBrigadierPay`, `brigadierDateKeys` — `payrollDetail.ts` |

Скил деталей: **`fst-payroll-georgia`**.

## Roles & access

| Invariant | Code |
|-----------|------|
| View access | `canAccessView`, `viewsForUser` — `src/lib/access/permissions.ts` |
| Default role views | `DEFAULT_ROLE_VIEWS` — `roles.ts` |
| Sysadmin | `isSysAdmin`, `canManageAccess` |
| Timesheet brigades | `timesheetAccess` — `timesheetScope.ts` |

Builtin users: **add-only** (`ensureBuiltinWebUsers`) — не перезаписывать прод-учётки seed.

## Journals (mandatory on mutation)

| Layer | API |
|-------|-----|
| Global audit ring | `appendAudit` → `auditLog` |
| Warehouse | `appendWarehouseAudit` |
| Item rename/history | `itemHistories` |
| HR | `appendEmployeeJournal` |

Скил: **`fst-action-journals`**.

## Verification subagent

Before merge: **`project-guardian`** + **`product-verifier`**.
