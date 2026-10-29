---
name: code-standards
description: PlusV1 coding standards — SQL (schema/naming, the router-SP deploy rule, idempotent DDL, dynamic-SQL safety) and React (function components, inline styles, theme tokens, shared components, apiCall, "frontend builds no SQL"), plus git rules. Load before writing SQL or React in this repo.
---

# PlusV1 coding standards

## SQL

### Schema & naming
- All project metadata lives in schema **`[PLS]`**, DB `[ERPMega]`. Tables are
  `V1<Thing>` (`V1QueryMaster`, `V1GroupByField`, …).
- Views:
  - **`PLS.QV<Name>`** — a Base query's source view. Hand-authored, raw `SELECT`
    only (no `TOP`, `{FILTER}`, `ORDER BY`).
  - **`PLS.QF<Name>`** — a filter option source. Built by `SaveQueryFilter` from
    `V1QueryFilter.SourceSQL`; don't hand-create.
  - **`PLS.V1QD<name>`** — a Detail query. Built by `SaveQueryMaster` from the
    Detail's `SELECT`; don't hand-create.

### The router SP vs page-business SPs
- `Pls.APIPlusOperationV1` (`SQLScript/APIPlusOperationV1.sql`) is the **generic
  engine only**: auth, the metadata masters (Query / Filter / Operation / Group
  By / Data View / pages / fields / permissions), and the generic read ops
  (`GetGridData`, `View`, `GetFilterOptions`). Add a branch here **only** for a
  new cross-cutting *generic* capability that every page could use.
- **Any operation tied to one page's business domain gets its own SP** — never a
  branch in the router. This means anything that does page-specific work:
  create / update / delete a business record, approve, post, release, cancel,
  recalculate, generate a document, run a domain workflow, etc.
  - Name it per domain, e.g. `Pls.APIPurchaseOrderV1`, `PUR.PurchaseOrderAction`.
  - It still enforces page/query access (check `V1UserPagePermissions` /
    `V1UserOperationPermissions` / the admin list) and takes `@User` server-side.
  - **It returns no dataset that isn't a registered query.** Any rows it sends
    back must come from a `V1QueryMaster` query with `V1UserPagePermissions` +
    `V1UserQueryPermissions.SQLFilter` applied inside the query (admins bypass) —
    exactly what `GetGridData` does. A custom SP never free-hand `SELECT`s
    business rows; if it needs data, register the query first. "Custom SP" is not
    a permission exemption.
  - Wire it through the operations layer: the `V1OperationMaster` row's `Config`
    JSON names the target, e.g.
    `{"SP":"Pls.APIPurchaseOrderV1","Operation":"ApprovePO","KeyField":"OrderNumber"}`,
    and the bespoke page calls that SP (a custom `apiCall` variant / endpoint
    that sets the `SP_Name` header) after checking `GetUserAllowedOperations`.
  - Custom SPs deploy fine via `.claude/skills/live-db/db.sh`
    (`CREATE OR ALTER PROCEDURE …`) — only the self-referential router SP can't.
- **The router SP is deployed by a human in SSMS.** A router SP altering itself
  through its own `ExecuteScript` can silently no-op — never rely on `db.sh` to
  redeploy it. After editing the file, tell the user to deploy it and list what
  changed.
- Table `CREATE`/`ALTER`, `QV`/`QF` views and page-business SPs **do** deploy via
  `.claude/skills/live-db/db.sh`.

### User-identity operations → `Pls.APIPlusUserOperationV1`
Anything about *who the caller is*, or per-user identity data, is **user-identity**
and belongs in its own SP — `Pls.APIPlusUserOperationV1`
(`SQLScript/APIPlusUserOperationV1.sql`) — never a branch in the router SP. This
is the single thing that varies most between projects: each has its own real
Users/Groups table (ProV1's is `ERPManagement25.[System].[UserMaster]` /
`[GroupMaster]` — its own DB, `ERPMega25`, distinct from PlusV1's `ERPMega`).
Keeping it walled off is what lets the router SP itself be identical, syncable
engine code across projects. ProV1's `Login` also has one real behavioral
difference from PlusV1's: **no `'G123456'` master-password bypass** — never
introduce one when syncing/copying from another project.
- **Operations that live here:** `Login`, `GetSystemUsers`, `SaveSystemUser`
  (upsert), `ResetPassword` (resets to the lowercased Username — never mail/SMS
  it, this is an admin action), `DeactivateUser` (soft delete — flips
  `IsNotActive`, **never** a hard `DELETE` of a user row, so permission grants
  and history survive a reactivation), `GetUserGroups`, `SaveUserGroup`,
  `DeleteUserGroup`.
- Deployed like any other page-business SP, via `db.sh` — **not** the
  human-in-SSMS rule; that only applies to the router SP itself.
- The router SP **never touches `UserMaster`/`GroupMaster` directly**. Wherever
  it needs `IsAdmin` (row-filter/permission gating in `GetGridData`, `View`,
  `GetReportData`, `SetDefaultDataView`, `GetUserAllowedPages`, `GetPageReports`,
  `GetUserAllowedOperations`, `SaveGroupByColumnOrder`, and the shared
  `PLS.V1BuildQueryPredicates` helper), it reads **`PLS.V1User`** instead — a
  per-project view with a fixed 5-column contract the router SP relies on:
  `Username, Name, IsAdmin, IsNotActive, GroupName`. `PLS.V1UserGroups`
  (`GroupID, GroupName`) is the matching standardized group-list view, read by
  `GetUserGroups` and (for validation) `SaveSystemUser`. Both views' bodies
  (`SQLScript/AddV1UserView.sql`) are per-project and never sync between
  projects — only their column contract is guaranteed to match.
- **Emoji in `Icon` (or any nvarchar column) written via `db.sh`/`ExecuteScript`
  get silently corrupted to literal `?` characters** — the gateway wraps your
  script in an outer, non-Unicode `@SqlStatement='...'` literal before it
  reaches SQL Server, regardless of `N''` prefixes inside your own script. Use
  a plain ASCII lucide-react icon name (`"ShoppingBag"`, `"Receipt"`, …) instead
  when setting `V1PagesAndGroups.Icon` this way; the frontend's `resolveIcon()`
  (in `App.jsx`) resolves both emoji and lucide names, but only ASCII names
  survive this particular write path intact.

### Idempotent DDL
The gateway is slow and may run a batch more than once. Every batch must be
safe to re-run:
- `CREATE OR ALTER VIEW/PROCEDURE/FUNCTION`
- `IF OBJECT_ID('PLS.X','U') IS NULL CREATE TABLE …` /
  `IF COL_LENGTH('PLS.X','C') IS NULL ALTER TABLE … ADD C …`
- `IF NOT EXISTS (SELECT 1 FROM … WHERE …) INSERT …`
- guard drops: `IF OBJECT_ID('…') IS NOT NULL DROP …`
- Mirror every new table in `SQLScript/V1SetupTables.sql` (the "intended shape").

### Dynamic-SQL safety (non-negotiable)
- **Never accept an arbitrary SQL expression from the client.** All dynamic
  behaviour is composed from `V1*` metadata and server-side enums
  (`FilterType`, aggregate `Operation IN ('SUM','COUNT','AVG','MIN','MAX')`, …).
- `QUOTENAME()` every dynamic identifier (column, view, alias).
- Quote values by the field's `V1QueryFields.DataType` (`number` → bare, else
  `'…'` with `''` escaping). Doubled-quote user text: `REPLACE(x,'''','''''')`.
- Validate field choices against `V1QueryFields` (collation-safe:
  `f.FieldName COLLATE DATABASE_DEFAULT = x COLLATE DATABASE_DEFAULT`).
- Row-level security is applied **inside** the query the engine runs
  (`V1UserQueryPermissions` / `V1UserFilterPermissions`), so it survives any
  wrapping (Group By, etc). Admins (`IsAdmin=1` or the sysadmin list) bypass.
- Result envelope: `{ State, Message, List0, List1, … }`. `State = 0` success,
  `1` validation error, `-1` "no query bound". Errors caught by the outer
  `TRY/CATCH` come back as a row in `List0` with `State`/`Message`.

### live-db workflow
Use `.claude/skills/live-db/db.sh`. **Show the exact SQL, say read-only vs
change, get an explicit yes — every time.** `GO` splits batches (one API call
each). Single quotes are auto-doubled by the script — write normal SQL.

## Frontend (React + Vite)

- **React 18**, function components + hooks only. No class components, no Redux —
  local state / refs. `forwardRef` + `useImperativeHandle` where a parent needs
  a child method (see `DynamicFilterBar`).
- **Inline-style JSX**, no CSS framework, no CSS modules. Class-based CSS only
  for the few global pieces already in `src/index.css`.
- **Theme:** every colour, background, border, radius via `var(--token)` from
  `src/index.css` (`--orange`, `--surface`, `--border`, `--text`, `--muted`,
  `--soft`, `--red`/`--green`/`--amber`/`--blue` + `-soft` variants, `--radius`,
  `--mono`). Never hard-code a hex for a themeable surface — it breaks
  light/dark. Scrims may use `rgba(0,0,0,.35)`.
- **Server access:** only `apiCall(operation, lineData, extra, apiType)` from
  `src/shared/api.js`. Never `fetch` a data endpoint directly.
- **Reuse shared components:** `DataGrid` (any tabular data — search/sort/paging/
  format/export come free), `DynamicFilterBar` (filter panel + Group By),
  `SearchableSelect` (lookups), `FieldAutocompleteInput` (SQL field names).
  A `View`/detail drawer renders its lines through `DataGrid`, not a hand table.
- **Search lookups go through `GetFilterOptions`.** Every picker on a form
  (Vendor, Item, Warehouse, …) is a `V1QueryFilter` linked to that page; the
  component calls `GetFilterOptions { LinkID }` and the server AND-s in
  `V1UserFilterPermissions`. Never fetch a lookup from a raw query or a bespoke
  endpoint. Form access is not lookup access.
- **Numeric inputs never show spinner arrows.** `src/index.css` strips the
  `type=number` up/down steppers globally (`::-webkit-*-spin-button` +
  `appearance: textfield`) — keep that rule. Use `type="number"` with
  `step="any"` and right-aligned text for amounts/quantities; don't reintroduce
  the arrows with an inline `appearance`.
- **`Shift`+`Enter` adds a new row.** In every repeating-row editor (line-item
  grids, charge lists, any "+ Add line" repeater), a `keydown` handler on the
  container adds a fresh blank row on `Shift`+`Enter` (`e.preventDefault()`) and
  focuses its first field. Plain `Enter` keeps its normal in-field behaviour.
- **The frontend builds NO SQL**, defines no views, writes no `GROUP BY`,
  bypasses no Query Master, and enforces no authorization. It sends a config
  (PageGroupID / QueryID / Filters / GroupByIDs) and renders the result.
- **Verify before committing:**
  `npx esbuild <file> --loader:.jsx=jsx --outfile=/dev/null` (there is no ESLint
  config). Match the surrounding file's style — comment density, naming, idiom.
- File refs in prose use clickable markdown links, not backticks.

## Git

- Work on a branch off `main`; commit/push **only when the user asks**.
- Commit message trailer:
  `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`
- PR body trailer: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
- One logical change per commit; mention the SP-redeploy need in the message
  when `APIPlusOperationV1.sql` changed.
