---
name: order-board
description: The "Order Board" page design (first built in PlusV1 for Customer Order) -- a Table view plus grouped views (By Customer / By Vendor / By Status ...) switched inside a top filter panel, page-driven checklist filters, an entity drawer, a "party" drawer of open records, and per-record print with a stacked Preview panel. Load when the user says "Order Board", "same design as Customer Order (PlusV1)", or asks to give a page that design.
---

# Order Board -- the Customer Order page design (from PlusV1)

**Name:** *Order Board*. When the user says "use Order Board", "same design as
Customer Order in PlusV1" or "make it like Customer Order", build this.

Copied from PlusV1's `order-board` skill (2026-10-18) and adapted to ProV1. The
shared building blocks were ported then (see "Shared pieces in ProV1"); no ProV1
page uses the design yet, so the reference implementations are PlusV1's.

## Reference implementations (PlusV1 -- read the closest one, copy its structure)

Sibling repo: `/Users/mohamed/Documents/MyProjects/PlusV1`. Page ids there are
PlusV1's, not ProV1's -- look up the ProV1 page by Label.

| PlusV1 page | Files (under `PlusV1/src/`) | Grouped views | Party drawer | Print / Preview |
|---|---|---|---|---|
| Customer Order -- the original | `pages/CustomerOrderPage.jsx`, `pages/CustomerOrderViewDrawer.jsx` | By Customer, By Truck Type | Customer (open orders, state <= 80) | Co_CustomerOrder |
| Shipment Tracking | `pages/logistics/ShipmentTrackingPage.jsx`, `ShipmentViews.jsx` | By Vendor / Status / Assigned To / Item, Calendar | Vendor (open shipments) | -- |
| Purchase Order | `pages/purchasing/PurchaseOrderPage.jsx`, `PurchaseOrderViews.jsx` | By Vendor / Status / Buyer | Vendor (open POs) | PO_PRINT |
| Customer Invoice | `pages/sales/CustomerInvoicePage.jsx` | By Customer / Sales Person | Customer (uncollected) | -- |

**ProV1 (first Order Board page, 2026-10-18):** Customer Order (page 5) --
`src/pages/CustomerOrderPage.jsx` + `src/pages/CustomerOrderBoard.jsx`
(BoardControls / GroupedView / CustomerDrawer / PreviewPanel, reusable
shapes), server `SQLScript/AddCustomerOrderViewsAndFilters.sql`. Views: By
Customer / By Status / By Salesperson; status checklist (LIST link on
OrderState, default New..Confirmed); customer drawer = Detail "Customer Open
Orders" (state <= 80, all dates -- the grid is still limited by the Order Date
panel default, which the server applies when a request sends no date);
CO_PRINT / CO_INVOICE print icon + stacked Preview. Read this one first in ProV1.
GridPage page-driven mode now waits for the panel's seeded defaults
(DynamicFilterBar `onSeed`) before its first load.

When you port one, keep ProV1's own page logic (its drawers, operations, SPs,
request IDs) and take only the *design* -- PlusV1's page code calls PlusV1 ops.
Add the first ProV1 Order Board page to this table.

## Ask first (one AskUserQuestion, multiSelect)

1. Which grouped views besides Table (the natural "by" fields of the record:
   party, status, owner / buyer / sales person, type ...).
2. Which pieces: status checklist, party drawer, print icon + Preview, top
   filter panel. Default: all that apply.

## Shared pieces in ProV1 (ported 2026-10-18)

| Piece | ProV1 API |
|---|---|
| Top filter panel | `GridPage gridPresentation={{ filterLayout: 'top' }}` (only `filterLayout` is ported -- PlusV1's `columns` / `appearance` / `compare` / `rowStyle` are **not**; port them with DataGrid support if a page needs them) |
| View switch slot | `GridPage filterExtra={...}` -> `DynamicFilterBar extra={...}` (shown first in the panel, also when collapsed) |
| Page-driven filters | `GridPage extraFilters={[{ LinkID, Values } \| { LinkID, From, To }]}` + `hideFilterFields={['OrderState', ...]}`; `DynamicFilterBar hideFields` |
| Checklist | `src/shared/CheckListDropdown.jsx` -- `{ label, allText, options: [{value,label}], picked, onToggle, onClear, onOnly, minWidth }` |
| Row print icon | `<ReportMenu target="Form" compact reports={reports} context={{ <Key>: id }} />` |
| Stacked Preview | `import { buildReportHTML, previewHTML } from '../shared/ReportMenu.jsx'` -- `buildReportHTML(report, pageGroupId, ctx, { pageSize, orientation })` returns `{ html, layout, meta, params }` and throws `Error` with `.server = true` for a refusal (show its message). ProV1's 4th arg is `opts`, **not** PlusV1's `extras`. `previewHTML(html, layout, { bg, pad })` |
| Money by currency | not shared -- each PlusV1 page defines `ccyText = (t) => Object.entries(t).sort((a, b) => b[1] - a[1]).map(([c, v]) => \`${compact(v)}${c ? ' ' + c : ''}\`).join(' · ') \|\| '0'`; copy it with the page |

## The pieces

### 1. View switch -- inside the filter panel
- `[ ['table','Table',Icon], ['customer','By Customer',Icon], ... ]` segmented
  buttons, orange when active; choice kept in `localStorage` (`<page>View`,
  every read/write in try/catch).
- Passed as `filterExtra` (Table view) / `extra` (grouped views), so it sits
  inside the filter panel in **every** view, next to the page-driven filters.
- Table view = the generic `GridPage` with `gridPresentation={{ filterLayout: 'top' }}`
  so the panel stays on top (no jump to a sidebar when switching).

### 2. Page-driven filters (status checklist, single date, ETA range ...)
- Server: a `V1QueryFilter` + a **panel** link (`UsePanel = 1`) on the Base
  query, e.g. `LIST` on `OrderState`. Hidden from the generic widgets via
  `hideFilterFields` (GridPage) / `hideFields` (DynamicFilterBar).
- Page: reads the link (`GetQueryFilterLinks`, match `QueryField` + `UsePanel`),
  the options (`GetFilterOptions { LinkID }`), and sends
  `{ LinkID, Values }` / `{ LinkID, From, To }` through `extraFilters` (GridPage
  -- it reloads when they change, no Apply gate) or appended to the grouped
  view's `GetGridData` Filters.
- Checklist UI: `CheckListDropdown`.

### 3. Grouped views (`<X>GroupedView`)
- Same Base query rows: `GetGridData { PageGroupID, Filters: [...panel, ...extraFilters] }`
  with its own `DynamicFilterBar layout="top"` (+ `extra={viewSwitch}`,
  `hideFields`, `onApply` -> reload). Grouping is presentation only -- no SQL,
  no Group By config.
- Group row: chevron, icon, key + name (party name clickable -> party drawer),
  status-mix pills with counts, Preview button (if a print exists), then
  right-aligned figures (count, last date, open/outstanding, total by currency
  via `ccyText`).
- Toolbar: title + "· n groups · n records · total", **Sort by** segmented
  (Total / Count / Name / Last ...; click again reverses, arrow shows dir),
  search box (group key/name + record numbers), Expand all / Collapse all,
  and the page's own buttons (+ New, Report).
- Expanded group: a table of its records (record # as an orange underlined
  button -> entity drawer, double-click row also opens it; status pill; money
  right-aligned with currency; print icon cell). Row hover = `--orange-soft`.
- Optional: sortable column headers, expandable record lines with an
  "Expand lines / Collapse lines" toggle capped at 50 records (one request per
  record -- see the rate limit below).

### 4. Entity drawer
- The page's existing drawer if there is one (e.g. ProV1's
  `CustomerOrderViewDrawer.jsx`), else a read-only `DetailsDrawer` reading
  Detail queries with `View` (KeyField = the record key).
- Gate with an operation (`<X>_VIEW`, BackendOperation `View`) -- the page
  checks `user.AllowedOperations`; the server checks the page / query grants.

### 5. Party drawer ("all open records of this customer / vendor")
- A Detail query `V1QD<Party>Open<Records>` = the Base view `WHERE <open states>`,
  keyed by the party number, read with `View` -- so it ignores the page's
  filters by design. **Copy the Base query's `V1UserQueryPermissions` rows onto
  it** (same SQLFilter -- e.g. the Sales ID scopes) or users see more than on
  the grid.
- Drawer: header (icon, "Party · open records", number + name), summary cards,
  status chips (All + each with count), the records table (same row component),
  "Preview all" when a print exists. Esc closes.

### 6. Print icon + Preview
- Print icon: `ReportMenu compact` with `reports` fetched once
  (`GetPageReports { PageGroupID, Target: 'Form' }`).
- Preview: side panel (portal) that builds each record's print with
  `buildReportHTML` + `previewHTML`, two at a time, stacked iframes (sections
  need `flexShrink: 0`, re-measure height after load), chips to jump,
  per-record Print, IntersectionObserver for the active chip. The report must
  be registered in Report Master and linked to the page (Form) -- see
  `query-engine/reference/printed-reports.md`.

## Server checklist (one idempotent script `SQLScript/Add<Page>ViewsAndFilters.sql`)
- `SaveQueryFilter` inserts a NEW row unless given a QueryFilterID --
  **always** guard with `IF NOT EXISTS (... FilterName = ...)` (or insert the
  `V1QueryFilter` / `V1QueryFilterLink` rows directly, as the `Register*.sql`
  scripts do).
- Links guarded by `IF NOT EXISTS (... QueryField ... UsePanel = 1)`.
- Fields used by LIST / EQUALS links or as View keys must be registered in
  `V1QueryFields` with the right `DataType` (`number` emits unquoted).
- Detail queries: `CREATE OR ALTER VIEW [PLS].[V1QD...]`, insert into
  `V1QueryMaster` (QueryType `Detail`), map in `V1PageQueries`, register the
  key field.
- Deploy with `.claude/skills/live-db/db.sh` (approval each time). Keep
  literals ASCII where you can: some characters (e.g. `→`) arrive as `?`
  through the gateway even inside `N'...'`; Arabic in `N'...'` has worked.

## Size limits -- check before shipping
- Gateway (`api/Plus.Api`): **10,000 rows** and **8 MB** per result
  (`Gateway:MaxResultRows` / `MaxResultBytes`, max 100,000 / 32 MB), measured as
  UTF-8 JSON **with non-ASCII escaped** (`\uXXXX` = 6 bytes per Arabic char).
  Measure a realistic range: `db.sh --raw` + sum
  `json.dumps(row, separators=(',',':'))` bytes. Over the limit the user sees
  "Result exceeds the size limit. Narrow the filters."
- Fix by: an explicit slim column list in the Base QuerySQL (sort in
  `QueryOrderBy`, never `ORDER BY` in the SQL), heavy text moved to a per-record
  Detail query for the drawer, and a `DATE_RANGE` panel link with
  `FixedFrom` / `FixedTo` tokens (TODAY, MONTH_BEGIN, MONTH_END, YEAR_BEGIN,
  YEAR_END) so a range always applies server-side.
- Gateway rate limit: **120 requests / minute per IP** (hard-coded in
  `Program.cs`, 429 "Too many requests."). Keep per-record fan-out (lines,
  previews) bounded -- two previews at a time, lines capped at 50 records.

## Frontend rules
- Layering: party drawer `zIndex 990` < entity drawer 1000-1200 < Preview 1300
  (< app pop-ups; `CheckListDropdown` popover 2000). View drawers close on
  **Esc**; stacked pop-ups use capture-phase `stopImmediatePropagation`.
- Colours only via `var(--token)` (`src/index.css`); status tones as `[fg, bg]`
  pairs (e.g. `['var(--green)', 'var(--green-soft)']`).
- `npx esbuild <file> --loader:.jsx=jsx --outfile=/dev/null`, then
  `npm run build`. Shipping = push to `main` (GitHub Pages rebuilds).
