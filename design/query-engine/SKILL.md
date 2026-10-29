---
name: query-engine
description: PlusV1 ERP query/page architecture — every page dataset flows SQL View → Query Master → Page mapping → permission validation → the Generic Operation (GetGridData). Covers Base/Detail queries, filters, operations, Group By, and the tables/ops that implement it.
---

# ERP Query & Page Development

This is the **architecture standard** (the *what* and *why*). Companion skills:
**add-page** = the step-by-step workflow to add one; **code-standards** = SQL &
React conventions; **live-db** = DB access. Full table + SP-operation catalogue
with objectives: `reference/tables-and-sps.txt` in this skill folder.

## Golden rule

**No page retrieves application data from an unmanaged query.** Every page
dataset must flow:

`SQL View → Query Master → Page Query Mapping → permission validation → Generic Operation → frontend`

This holds regardless of the UI — grid, dashboard, cards, charts, lookup, custom
design. The frontend **never** builds SQL, defines views, writes `GROUP BY`,
bypasses Query Master, or enforces authorization on its own. Hiding a field or
component in the UI is not data security — authorization is always server-side,
inside the query the Generic Operation runs.

**No returned data without a permission check — ever.** Any dataset that leaves
the server, from *any* SP including a custom page-business SP, must:
1. come from a query **registered in `V1QueryMaster`** (Base or Detail),
2. be reached only after validating the caller's access — page access
   (`V1UserPagePermissions`) **and** the per-(user, query) row filter
   (`V1UserQueryPermissions.SQLFilter`) applied *inside* the query (admins
   bypass via `IsAdmin=1` / the sysadmin list).

A custom SP does not get to `SELECT` business rows on its own. It resolves the
registered query, applies the same permission layering the Generic Operation
does, then returns. If a custom SP needs a dataset, register the query first.

## Core query rule

Every query a page uses must be (1) registered in **Query Master**
(`V1QueryMaster`), (2) linked to the **Page** (`V1PageQueries`), (3) typed
`Base` | `Detail`, (4) reached only through the Generic Operation.

- **Base query** — the page's primary dataset (one per page). Register a
  `PLS.QV<Name>` view built from the provided SELECT.
- **Detail query** — every additional query the page needs (transaction lines,
  payments, related docs, extra stats…). Save it as `QueryType='Detail'` and the
  engine materialises `PLS.V1QD<name>` from the SELECT automatically (stores
  `QuerySQL = SELECT * FROM that view`).

## New page workflow

1. Receive the SELECT. Never run it from the frontend.
2. **Create the view** — `CREATE VIEW [PLS].[QV<Name>] AS <select>` (schema
   always `PLS`, name always starts `QV`). Detail queries: skip this — save the
   SELECT in Query Master as `Detail` and the SP builds `PLS.V1QD<name>`.
3. **Register in Query Master** — one row per view; type `Base` or `Detail`.
4. **Link to the Page** — `SaveQueryPageRelation` / Query Master "Mapped Page".
5. Page fetches via the Generic Operation only. Verify the mandatory checklist
   below.

## The Generic Operation

`GetGridData` is the single server entry point for **fetch, filter, search,
sort, paginate, Group By, aggregate**. Do not add page-specific fetch ops
without a technical reason Generic Operation cannot meet ("configuration over
hardcoding", "generic over page-specific").

`GetGridData { PageGroupID, QueryID?, Filters?, GroupByIDs? }`:
- resolves the query for the page (Base by default; `QueryID` for a Detail —
  must be linked),
- applies the admin `QueryFilter`, the caller's `V1UserQueryPermissions` row
  filter (admins bypass), and panel filter-link predicates,
- if `GroupByIDs` present, wraps the fully-filtered query and `GROUP BY`s,
- appends `QueryOrderBy`. Returns `State = -1` when nothing is registered.

`View { PageGroupID, QueryID, KeyField, KeyValue }` — a Detail query keyed to one
row (double-click / drawer). Same permission layering; no panel links.

**Page business logic never routes through `Pls.APIPlusOperationV1`.** The router
SP is for the generic engine + metadata + auth only. Any operation tied to one
page's domain — create/update/delete a business record, approve, post, release,
cancel, recalculate, generate a document, run a workflow — lives in its **own
custom SP** (e.g. `Pls.APIPurchaseOrderV1`). It still enforces page/operation
permissions server-side and is wired through the operations layer: the
`V1OperationMaster.Config` JSON names the SP + operation, and the bespoke page
calls it after checking `GetUserAllowedOperations`. See **code-standards → The
router SP vs page-business SPs**.

A custom SP is **not** exempt from the golden rule: any dataset it returns must
still come from a `V1QueryMaster`-registered query with page +
`V1UserQueryPermissions` validation applied server-side. Custom = different SP,
same permission gate.

## Metadata tables (all `[PLS]`)

- `V1PagesAndGroups` — pages/groups tree (`PageGroupID` PK).
- `V1QueryMaster` — `QueryID, QueryName, QueryType, QuerySQL, QueryFilter,
  QueryOrderBy, Operation, ApiUrl, ViewName`. Detail rows carry `ViewName`
  (`V1QD<name>`); the engine runs `SELECT * FROM` it, so a Detail's
  `QueryFilter` / `QueryOrderBy` use the **view's** column names (no source
  aliases). `QueryFilter` / `QueryOrderBy` are never written into `QuerySQL` —
  the engine appends them (or substitutes a `{FILTER}` token).
- `V1PageQueries` — M:N page ↔ query.
- `V1QueryFields` — per-query column config; `DataType='number'` drives value
  quoting in generated predicates. Group / aggregate fields are validated
  against this on save.
- `V1UserQueryPermissions` — per-(user, query) `SQLFilter` row filter.
- `V1QueryFilter` (+ `QF*` views), `V1UserFilterPermissions`, `V1QueryFilterLink`
  — the filter-panel system.
- `V1OperationMaster` / `V1PageOperations` / `V1UserOperationPermissions` —
  reusable permissioned actions (see Operations).
- `V1GroupByMaster` / `V1GroupByField` / `V1GroupByAggregate` — Group By configs.
- `V1KPIMaster` / `V1UserKPIVisibility` — KPI summary-card configs + per-user
  Show/Hide (see KPI framework).
- `V1DataViews` / `V1DataViewFields` — per-user saved grid column presentation.
- `V1ReportMaster` / `V1ReportLink` / `V1UserReportPermissions` — Report Master.

## Operations & permissions

Admin screens: **Operation Master** (define ops), **Group & Page Master →
Operations** (link op to page + its query + config override), **User Permissions
→ Operations** (grant per user per page).

Ops: `GetOperationMaster` / `SaveOperationMaster` / `DeleteOperationMaster`,
`GetPageOperations`, `SavePageOperationRelation`, `GetUserOperationPermissions`,
`SaveUserOperationPermission`. `GetUserAllowedOperations { PageGroupID? }` →
`{ PageGroupID, OperationKey, BackendOperation, Config, ConfigOverride, QueryID }`
per allowed (page, op); the frontend merges `ConfigOverride` over `Config`,
checks the key, then calls `BackendOperation` with the merged config + `QueryID`.

## Search lookups (form/page pickers)

**Every search lookup on a form or page is a `V1QueryFilter`, linked to that
form/page, permission-checked server-side** — the same infrastructure as the
filter panel. A Vendor / Item / Warehouse / Buyer / Currency / Payment-Term
picker on "Purchase Order Entry" is not a frontend concern: each one is a
registered `QF` source mapped to the page.

Flow: `lookup SELECT → SaveQueryFilter (builds PLS.QF<Name>) → SaveQueryFilterLink
to the page → V1UserFilterPermissions grant → GetFilterOptions serves it`.

- The frontend **never** issues the lookup query. `SearchableSelect` /
  `FieldAutocompleteInput` call **`GetFilterOptions { LinkID }`** (or
  `{ QueryFilterID }`), which reads the `QF` view with the caller's
  `V1UserFilterPermissions` AND-ed in. No link for this page ⇒ no data.
- A `QF` registered for another form is **not** reusable until it is also linked
  to this page. Access to the form does not grant access to its lookups.
- Bespoke forms included — a custom React form's pickers still resolve through
  `GetFilterOptions` on a page-linked `QF`, never a bespoke fetch.

Admin: **Query Filter Master** (define the `QF`), **Group & Page Master → Filters**
tab (link to the page), **User Permissions → Filters** tab (grant / restrict).

## Printed reports

**Every printed report is registered in Report Master (`V1ReportMaster`) first,
then linked to a Form or a Grid.** No Print button bypasses it; no report runs
client SQL. Two types: **React Report** (designed in-system, layout stored as
metadata — the preferred method for all new work) and **Fast Report** (legacy
only). Full spec: `reference/printed-reports.md`.

- **Data source** = a Query-Master-registered query. Same flow as everything
  else: `report → registered query → page + V1UserQueryPermissions + field
  checks → server operation → report data`.
- **Form report** prints one document (keyed by the current record). **Grid
  report** prints a list from the grid's context; its config **explicitly**
  states the scope (selected row / selected rows / all filtered / current page /
  entire result) — the frontend never decides.
- **Parameters** come only from controlled sources (current record, selected
  grid row(s), an approved filter, page context, validated user input) and are
  re-validated server-side.
- **Permission** is checked server-side before generating: page · Form/Grid ·
  report · data source · requested records · fields. Hiding the Print button is
  not security.
- A React Report is **not** the Data View and **not** Grid Export — it has its
  own registered printable design (Preview / Print / PDF).
- A Form/Grid may expose several reports (`Print ▼`); each is its own
  `V1ReportMaster` row.

## Group By framework

A page may show a **Group By** selector listing the active configs for its Base
query (`None` + Group By Vendor / Customer / Item / Month / Year …). Definitions
live in settings, never hardcoded in a page. **Group By is configuration, not a
new query** — many configs share one Base view; do **not** create
`QV…ByVendor` / `QV…ByMonth` views.

A config defines: Group By Name · Query · Group Fields · Aggregate Fields ·
Aggregate Operations (`SUM|COUNT|AVG|MIN|MAX`, server-controlled enum, never user
SQL) · Display Names · Active · Display Order. Group and aggregate fields may
only be chosen from the query's `V1QueryFields`.

Admin: **Settings → Group By Master** (any query) and **Group & Page Master →
Group By** tab (page's Base query). Ops: `GetGroupByMaster { QueryID? }` (List0
configs / List1 fields / List2 aggregates), `SaveGroupByMaster` (upsert +
replace `Fields:["Col",…]` + `Aggregates:[{FieldName,Operation,DisplayName}]`),
`DeleteGroupByMaster`, `GetPageGroupBys { PageGroupID }`.

Runtime: the frontend sends `GetGridData { …, GroupByIDs:[ids] }` (multi-select —
several configs merge: group fields distinct in config-then-field order,
aggregates distinct by field+operation). The engine builds
`SELECT <groupFields>, <OP([f]) AS [DisplayName]>… FROM (<filtered base>) _src
GROUP BY <groupFields> ORDER BY <groupFields>`. Every selected config must be
active for the resolved query. Grouped results render as raw columns; row-`View`
is disabled while grouped. The **Group By selector lives in the Filter Panel**
(`DynamicFilterBar`) when the page has one — a page with only group-by configs
still shows the panel for it, applied on **Apply**; pages with no panel get a
fallback checkbox row in the grid toolbar.

## KPI framework

Configurable **server-calculated summary cards** shown above a page's grid,
synced with the grid's active Filter/Search. **KPI is configuration, not a
view** — one aggregate `SELECT` wraps the page's existing Base query; never a
`QV…Total` view per KPI, never hardcoded in a page component.

A config (`V1KPIMaster`) defines: KPI Name · Display Name · Page · Query
(a Base query linked to the page) · Field · Operation (`SUM|COUNT|AVG|MIN|MAX`,
server enum) · Format (`number|integer|currency|percent|compact` — always set
one) · Display Order ·
Active. Field must be a `V1QueryFields` column of that query (`COUNT` may omit
it → `COUNT(*)`).

Admin: **Group & Page Master → KPIs** tab. Ops: `GetKPIMaster { PageGroupID? }`,
`SaveKPIMaster` (upsert), `DeleteKPIMaster { KPIID }`, `GetPageKPIs
{ PageGroupID }` (active configs for the strip), `GetKPIVisibility` /
`SaveKPIVisibility { PageGroupID, IsHidden }` (per user+page Show/Hide,
`V1UserKPIVisibility`).

Runtime: `GetKPIData { PageGroupID, QueryID?, Filters? }` — **same `Filters` as
the grid, Group By deliberately not passed** (grouping the grid must not change
a KPI). The engine rebuilds the Base query as `SELECT <OP([f]) AS [k_<KPIID>]>…
<FROM/WHERE of the base, TOP + ORDER BY dropped>`, applying the identical
predicates via the shared `PLS.V1BuildQueryPredicates` (QueryFilter +
`V1UserQueryPermissions` row filter + `V1QueryFilterLink` predicates). Every
field is re-checked against `V1QueryFields`, every identifier `QUOTENAME`d.
Returns List0 = one value row (columns `k_<KPIID>`), List1 = KPI meta +
`ColName`. Same page/query permission as `GetGridData`; hidden fields in the UI
are not authorization. `GridPage` renders the strip, recalculates on every
load/Apply/refresh, and remembers Hide/Show.

## Frontend vs backend

**Frontend:** show Group By options, send the selected config + filters / search
/ sort / paging, receive and render. **Backend:** query validation, Query Master
resolution, page/query authorization, filter / sort / paging, Group By /
aggregation, data retrieval, and blocking unauthorised query or field access.
All dynamic behavior comes from controlled metadata — never arbitrary SQL from
the client.

## Mandatory checklist for a new page

- SELECT reviewed · view created under `PLS` · view name starts `QV` · registered
  in Query Master · linked to the Page · type set (`Base` / `Detail`) · page uses
  `GetGridData` (or a custom SP that resolves the registered query) · every
  returned dataset is a registered query with page + `V1UserQueryPermissions`
  checks server-side · **every search lookup on the page is a `V1QueryFilter`
  linked to the page and served by `GetFilterOptions`** · frontend generates no
  SQL · filters / sorting / paging work · configured Group By options work ·
  aggregates validated · **KPIs recommended for the page** (2–4 summary cards on
  its Base query) · unauthorised data cannot be retrieved.
