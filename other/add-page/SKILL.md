---
name: add-page
description: Step-by-step workflow for adding to the PlusV1 metadata suite — a page, a Base/Detail query (with the PLS.QV view), a filter panel, a permissioned operation, a Group By config, or KPI cards. Includes the column-suggestion ruleset. Load whenever the task is "add / register / wire up" one of these; adding a page also means recommending KPIs.
---

# Adding to the PlusV1 metadata suite

A "page" is a row in `[PLS].[V1PagesAndGroups]`. Groups (`IsGroup = 1`) are
sidebar sections; pages (`IsGroup = 0`) open in a tab. Everything below is
configuration through the admin screens (⚙️ next to the admin name) or `db.sh`
— the `src/` repo is only touched for a **bespoke** page component.

Core rule (see the `query-engine` skill): the frontend never executes or defines
a page's SQL. `SQL View → Query Master → Page↔Query mapping → Generic Operation
(GetGridData) → frontend`.

---

## A. Data-grid page (no code)

1. **Receive the `SELECT`.** Never run it from the frontend.
2. **Create the view** — schema `PLS`, name starts `QV`
   (`PLS.QVCustomerBalance`). Raw `SELECT` only — no `{FILTER}`, no `TOP`, no
   `ORDER BY`. Deploy via `.claude/skills/live-db/db.sh` (approval each time) or
   SSMS.
3. **Create the page** — Group & Page Master → New Group (if needed) → New Page
   (Label, Icon, Parent Group, Sort Order). Note the generated `PageGroupID`.
4. **Register in Query Master** — New:
   - `QuerySQL` = `SELECT * FROM PLS.QV<Name> WHERE 1 = 1 {FILTER}` (+ optional
     `ORDER BY` in the Query OrderBy field, not the SQL).
   - Type = **`Base`**. Mapped Page = step 3.
   - Save → columns auto-discover into `[PLS].[V1QueryFields]`.
5. **Tune columns** — Query Master → Fields tab. Per column: `Label`, `Format`,
   `Width`, `SortOrder`, `Hidden`, `ColorRules`. Hand edits survive re-save.
   Use the suggestion ruleset below.
6. **Recommend KPIs.** Every new page: propose 2–4 summary cards for its Base
   query and, once confirmed, configure them (see "KPI config" below). Do this
   without being asked.
7. **Grant access** — User Permissions → pick user → check the page (+ its
   group). Optional per-user row filter: the Query tab under the page adds a
   `SQLFilter` row in `[PLS].[V1UserQueryPermissions]`.
8. **Done.** The page renders through `GridPage.jsx`, calling `GetGridData` with
   its `PageGroupID`.

## B. Bespoke page (custom React screen)

For the *Order Board* design (PlusV1's Customer Order style: Table + grouped
views, checklist filters, entity / party drawers, print + Preview) load the
**order-board** skill.

For drawers, multi-panel, custom actions.

1. Create the page row (A steps 2–3). Note the `PageGroupID`.
2. `src/pages/<Name>.jsx` — default-export a component taking `{ user, def }`
   (`def.id` = `PageGroupID`). Reuse `GridPage` for the list part where possible.
3. Register in `src/App.jsx` → `PAGE_COMPONENTS`, keyed by the `PageGroupID`.
4. **Every search lookup on the form** (Vendor, Item, Warehouse, …) → register a
   `V1QueryFilter`, link it to this page, served via `GetFilterOptions` (see
   "Search lookups" below). No lookup goes straight to a query from the form.
5. `npx esbuild src/pages/<Name>.jsx --loader:.jsx=jsx --outfile=/dev/null` to
   verify, then `npm run dev` / `npm run build`.
6. **Recommend KPIs** (A step 6) — propose summary cards for the page's Base
   query.
7. Grant access (A step 7) — page grant **and** the Filters-tab grants for its
   lookups.

**Page business operations get their own SP.** Anything a bespoke page does
beyond generic read (create/update/delete a business record, approve, post,
release, cancel, recalculate, generate a document, run a workflow) must be a
dedicated custom SP (e.g. `Pls.APIPurchaseOrderV1`) — never a new branch in
`Pls.APIPlusOperationV1`. Name it per domain, `CREATE OR ALTER` (deploys via
`db.sh`), enforce page/operation permission checks + `@User` server-side, and
wire it through the operations layer (`V1OperationMaster.Config` names the
SP + operation). See **code-standards → The router SP vs page-business SPs**.
Any dataset a custom SP returns still comes from a `V1QueryMaster`-registered
query with `V1UserPagePermissions` + `V1UserQueryPermissions` checks inside it —
no returned rows without a registered query and a permission gate.

Admin maintenance screens (User Master, Group & Page Master, Query Master,
Query Filter, Operation Master, Group By Master, User Permissions) are **not**
pages — they live in `SETTINGS_VIEWS` in `App.jsx`.

---

## Detail query (extra dataset for a page)

1. Query Master → New → Type = **`Detail`**, paste the full `SELECT`
   (no need to create a `QV` view — `SaveQueryMaster` builds
   `[PLS].[V1QD<name>]` and stores `QuerySQL = SELECT * FROM` it).
2. Map it to the page. `Query OrderBy` / `Query Filter` must use the **view's**
   column names (no source aliases).
3. Fetch it with `GetGridData { PageGroupID, QueryID }` (generic grid) or
   `View { PageGroupID, QueryID, KeyField, KeyValue }` (one record, e.g. a
   double-click drawer).

## Filter panel

1. Query Filter (Query Filter Master) → New: `FilterName`, `SourceSQL` (a
   `SELECT id, name FROM …`), `ValueField`, `LabelField`, optional
   `DisplayFields` (comma list — first = bold line) and `OrderBy`. Save builds
   `[PLS].[QF<Name>]`.
2. Group & Page Master → the page → **Filters** tab → add a link: Type first
   (`RANGE`/`MIN`/`LIKE`/`EQUALS`/`LIST`/`DATE_RANGE`), then Filter, Query Field
   (Base-query column), Filter Field (QF-view column), Panel = interactive.
   The **Filters** tab is grid-only (panel widgets + always-applied fixed
   rules, `UsePanel = 1` or Fixed); form/page pickers live on the **Form
   Filter** tab (see below).
3. Optional per-user restriction: User Permissions → the page → Filters tab.

## Search lookups (form/page pickers)

Every Vendor / Item / Warehouse / Buyer / Currency / … picker on a form is a
`V1QueryFilter` **linked to that form/page** — not a frontend query. Same steps
as the filter panel:

1. Query Filter Master → New: the lookup `SELECT`, `ValueField` / `LabelField`
   (+ `DisplayFields` for a two-line result). Builds `[PLS].[QF<Name>]`.
2. Group & Page Master → the form/page → **Form Filter** tab → link it
   (Lookup + Field name + Value Field). Stored as a `V1QueryFilterLink` with
   `UsePanel = 0` and no fixed value. A `QF` registered for another form is
   **not** usable here until it is also linked. (Grid panel filters go on the
   **Filters** tab instead.)
3. User Permissions → the page → **Filters** tab → grant / restrict per user.
4. Frontend: `SearchableSelect` / `FieldAutocompleteInput` call
   `GetFilterOptions { LinkID }` — the server reads the `QF` view with the
   caller's `V1UserFilterPermissions` AND-ed in. No page link ⇒ no data.

Never wire a lookup to a bespoke fetch or a raw query. Form access ≠ lookup access.

## Permissioned operation (e.g. a "View Details" action)

1. Operation Master → New: `OperationKey` (e.g. `PO_VIEW_DETAILS`), Label,
   `BackendOperation` (`View`, or the operation name inside a custom SP for
   business actions), `Config` JSON (e.g. `{"KeyField":"OrderNumber"}`; for a
   business action also `{"SP":"Pls.APIPurchaseOrderV1","Operation":"ApprovePO"}`).
2. Group & Page Master → the page → **Operations** tab → link it, pick the
   page's Detail query, optional config override.
3. User Permissions → the page → Operations tab → tick `CanPerform` per user.
4. Frontend: login fetches `GetUserAllowedOperations`; the bespoke page checks
   the key, then calls `BackendOperation` with the merged config + `QueryID`.

## Printed report (Form or Grid)

Full spec: `query-engine/reference/printed-reports.md`. Steps:

1. Register in **Report Master** (`V1ReportMaster`): `ReportName`, `ReportCode`,
   `ReportType` (`React` — the default for new work — or `Fast`), `IsActive`.
2. Design the React Report in-system (header/footer, fields, table columns,
   formats, totals, grouping, page setup) — stored as metadata.
3. Point it at an **approved data source** — a Query-Master query following the
   normal page/permission rules. No client SQL.
4. Declare parameters (from the current record / selected grid row(s) / an
   approved filter / page context / validated input) — all re-validated server-side.
5. Link it to the **Form** or **Grid** (Page, `IsActive`, `DisplayOrder`,
   `DisplayName`). For a Grid report, set the record scope explicitly
   (selected / filtered / page / all). A Form/Grid can have several reports.
6. Grant per user; the server validates report + data-source + record + field
   access before generating. Test Preview / Print / PDF, and that an
   unauthorised user cannot run it.

## Group By config

1. Group By Master (or Group & Page Master → the page → **Group By** tab):
   name, Active, sort, group-field chips, aggregate rows
   (`field / SUM|COUNT|AVG|MIN|MAX / display name`). Fields must exist in the
   query's `V1QueryFields`.
2. Runtime: the Group By selector appears in the page's filter panel; the
   frontend sends `GetGridData { …, GroupByIDs:[ids] }` — the server builds the
   `GROUP BY`. Never a new view.

## KPI config — recommend on every new page

Whenever you add a page (grid or bespoke), **propose KPIs without being asked**.
KPIs are server-calculated summary cards above the grid, synced to its active
filter/search. Config lives in **Group & Page Master → the page → KPIs** tab
(`V1KPIMaster`); values come from `GetKPIData` — never hardcode, never a view.

1. Look at the Base query's `V1QueryFields` and suggest **2–4** cards, e.g.:
   - a **count** of the main record (`COUNT` of the key, format `integer`) —
     "Total <records>"
   - **`SUM`** of each principal money column (`*Amount`, `Total*`, `*Paid`,
     `*Costed`) — format `currency`, or `compact` (1.2K / 3.4M / 5.6B) when the
     figures run large
   - a **count of a meaningful subset** the user cares about — either a second
     `COUNT` KPI or, if it needs a `WHERE`, note it (a filtered KPI is done by
     the user narrowing the grid; there's no per-KPI predicate)
   - occasionally `AVG` / `MIN` / `MAX` of a qty or lead-time column
2. Each KPI: KPIName (UPPER_SNAKE), DisplayName, Field (a `V1QueryFields`
   column; omit for `COUNT(*)`), Operation (`SUM|COUNT|AVG|MIN|MAX`), Format
   (`number|integer|currency|percent|compact`), DisplayOrder, Active. Always
   name a Format — pick it from the field's meaning (money → `currency` or
   `compact`, a plain tally → `integer`, a ratio → `percent`).
3. Present the list, get a yes, then `SaveKPIMaster` per card (or via the KPIs
   tab). They then render for every user; each can Hide/Show the strip.

---

## Column-suggestion ruleset (Fields tab seeding)

On query save `[PLS].[V1QueryFields]` is seeded; hand edits survive re-save.

**Hide by default:**
- FK id columns with a name/description sibling (`ShipToID` when `ShipToName`
  exists; raw `*State` int vs `*StateDescription`)
- audit fields: `*CreatedBy`, `*CreatedDate`, `*LastMaintBy`, `*LastMaintDate`,
  `*ClosedBy`, `ReleasedBy`
- internal: `*InUse`, `*InUseBy`, `AttachmentFileID`, category id columns

**Format:**
| name / type matches | Format |
|---|---|
| `*Amount`, `Total*`, `*Freight`, `*Insurance`, `*Discount`, `*Paid`, `*Costed` | `number:2` |
| datetime | `date` |
| `*Number`, `*Code`, `*ID`, `PINumber` | `mono` |
| `bit` | `yesno` |
| else | *(blank)* |

**ColorRules** — JSON array, first match wins:
```json
[{ "op": "eq|ne|lt|le|gt|ge|contains|default", "value": <any>,
   "color": "green|amber|red|blue|gray", "badge": true }]
```
| column pattern | rule |
|---|---|
| `*StateDescription` / `*State` text | `contains "Close"`→red badge, `contains "Releas"`→green badge, `default`→blue badge |
| `*TypeDescription` | value-based badge |
| signed amounts | `lt 0`→red |

---

## After SP changes

Any edit to `SQLScript/APIPlusOperationV1.sql` must be **deployed by a human in
SSMS** (the router SP cannot ALTER itself via `ExecuteScript`). Table DDL and
`QV`/`QF` views can go through `db.sh`. Mirror new tables in
`SQLScript/V1SetupTables.sql`.
