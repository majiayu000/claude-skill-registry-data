---
name: padosoft-admin-interface
description: >-
  Use this skill when building or reviewing an admin/back-office screen with a Laravel API behind it and an
  interactive frontend in front — a filtered listing, a dashboard with KPI cards and charts, an expandable
  table, an export, an autosuggest on a foreign key — and whenever the user says a panel shows a spinner
  forever, an empty result is indistinguishable from a failure, a filter returns everything, an export times
  out, a chart redraws on top of itself, or asks for "the admin page for X". It gives the layer pipeline on
  the server, the data contract across the boundary, and the four states every screen owes its user. Do not
  use it for public storefront pages, for the security review, or for choosing a UI component library.
license: MIT
compatibility: >-
  A Laravel API with a JavaScript frontend — React for new work, though the contract and the layering hold
  for any client. Independent of framework and language versions.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: A back-office screen is a filtered query with a chart on top, and four states that must all exist.
  profiles: laravel
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: admin, backoffice, dashboard, react, ajax, laravel, kpi, chart, table, export, filters
---

# Admin interface

An admin screen is a filtered query with a chart on top, and it fails in the same handful of ways every time:
a spinner with nothing behind it, an empty table that might be a failure, a filter that quietly matches
everything, an export that dies at ten thousand rows.

Two halves — the server pipeline and the client contract — plus **the four states**, which is the section to
read first if you only read one.

---

## 1. The four states are mandatory

Every screen explicitly handles all four. Not one of them is implicit, and a missing one is a broken screen,
not a rough edge.

| State | What the user sees | When |
|---|---|---|
| **Initial / empty** | An empty state with a call to action | First load, no filter applied yet |
| **Loading** | Skeleton or spinner, submit disabled | While fetching |
| **Success** | The data | Response OK |
| **Error** | A visible error, controls re-enabled | Fetch failed, or the response carries an error |

**Empty, missing and broken must look different.** Collapsing them into one blank panel is what makes a
defect unreportable: the user cannot describe what they saw, because they saw nothing. That is the same rule
as **`padosoft-failure-visibility`**, which is where the server side of it lives.

An error state that leaves the submit button disabled is the worst of the four: the screen is now
unrecoverable without a reload.

## 2. Server pipeline — the order matters

Build in this order, because each layer defines the contract of the next:

```
Enum  →  DTO  →  FormRequest  →  Service (query)  →  Service (metrics)  →  Controller  →  Route  →  Export
```

| Layer | Holds |
|---|---|
| **Enum** | The stat/metric types, the periods, the statuses. One source for what the screen can ask for |
| **DTO** | The filter object: typed, explicit, the only thing the services accept |
| **FormRequest** | Validation and normalisation of the HTTP input; it builds the DTO |
| **Service (query)** | The master query. Filtering, grouping and pagination in SQL, not in PHP |
| **Service (metrics)** | KPI and derived values, computed from the same filtered set |
| **Controller** | Translates: DTO in, resource out. No query, no business rule |
| **Route** | In the admin group, with the middleware that group carries |
| **Export** | The same filtered set, streamed |

**The filter DTO is the contract.** When the screen, the export and the KPI cards each build their own
filter, they drift, and the export stops matching what is on screen — which is the bug that gets reported as
"the numbers are wrong".

Caps are part of the contract too: a maximum date range, a maximum number of elements, a page size. Put them
in the DTO and send them to the client (§3) so it can tell the user *before* the request.

## 3. The data contract across the boundary

**The client is configured by the server, in one place, explicitly.** No hardcoded URLs in the frontend, no
global variables, no route helpers embedded in the client bundle.

Send the endpoints and the limits as data — a props object for a React root, a `data-*` payload for a
server-rendered container:

```jsx
<AdminPanel
  endpoints={{ analyze, export: exportUrl, autosuggest, breakdown }}
  limits={{ maxDays, maxItems }}
/>
```

Why it matters beyond tidiness: when the routes live in the server's hands, renaming one is a server change
with a compiler or a route list behind it. When they are strings in the client, renaming one is a silent
404 at runtime, on the screen nobody opened yet.

Keep the shape in one typed place shared by the modules below, and derive filter options from the **real
domain** — the enum, the database, the API — never from a hardcoded sample list that will diverge the first
time a value is added.

## 4. Client modules

Split by responsibility, not by screen. Each is independently testable and none of them knows about the DOM
of another:

| Module | Owns |
|---|---|
| `api` | Every call: the CSRF/auth header, the error translation, the abort signal |
| `filters` | The filter state and its widgets, including autosuggest |
| `table` | Rows, sorting, the expandable detail |
| `chart` | Rendering and, crucially, **teardown before re-render** |
| `kpi` | The cards and their thresholds |
| `utils` | Pure formatters — no fetching, no DOM |

Two rules that come from real breakage:

- **Destroy a chart before drawing it again.** A chart library that keeps its own canvas will stack instances
  on a filter change: the visible symptom is a tooltip showing values from a query you ran two filters ago.
- **Delegate events for anything inside a re-rendered list.** A handler bound to a row disappears with the
  row and takes the expand toggle with it.

## 5. Autosuggest on a foreign key

A select over a foreign table is a query, not a dropdown:

- minimum input length before the first request (two characters), so an empty focus does not scan the table;
- a debounce on typing — the request that matters is the one after the user stopped;
- cache the responses for the session;
- **the current value must render even when it is not in the first page of results**: hydrate the selected
  option from the server when the form is rendered, or an edit screen shows an empty box over a set value;
- the endpoint returns id and label only. An autosuggest that returns entities becomes a data leak the day
  someone adds a column.

## 6. Export

The export runs the **same filtered query** as the screen — the same DTO, not a reimplementation — and
streams. Loading the result set into memory to build a file is the pattern that works on the developer's
dataset and dies on production's.

If it can exceed a few seconds, it is a job with a notification, not a synchronous response. A download that
times out behind a proxy leaves no trace anywhere for the user to report.

## 7. Design tokens, and the one exception

Colours, spacing and typography come from the design tokens, in the markup and in any markup the client
injects. A literal hex in a template is the thing that survives a restyle and then looks broken next to
everything else.

**The exception:** a charting or canvas API that receives colours as values cannot resolve CSS variables, so
a resolved value is correct there. Read the token and pass its computed value rather than hardcoding a
different hex — otherwise the chart drifts from the theme, and it drifts silently.

---

## Gotchas

- **A filter that matches everything when it is empty** is the most expensive default in an admin panel: the
  first query of the day scans the table. Decide explicitly what "no filter" means, and prefer requiring one.
- **KPI cards computed from a different query than the table** will disagree, and the user will trust
  neither. One filtered set feeds both.
- **Server-side pagination or nothing.** A table that paginates in the client has already fetched everything.
- **The empty state is not a design nicety**: without it, every failure mode renders identically (§1).
- **An admin route outside the admin group** keeps answering, without that group's auth. The security side is
  in **`padosoft-laravel-security-review`**; the listing that leaks is usually the one added in a hurry.
- **Do not invent the layout.** Read where the neighbouring admin screens put their services, requests and
  client modules before creating files.

## Checklist

- [ ] All four states handled; empty, missing and broken look different; controls re-enabled on error
- [ ] Enum → DTO → FormRequest → Service(query) → Service(metrics) → Controller → Route → Export
- [ ] One filter DTO feeding screen, KPI and export
- [ ] Caps (date range, item count, page size) in the DTO and sent to the client
- [ ] Endpoints and limits passed from the server; no hardcoded URL in the client
- [ ] Client split into api / filters / table / chart / kpi / utils
- [ ] Chart destroyed before re-render; delegated events in re-rendered lists
- [ ] Autosuggest: min length, debounce, cache, selected value hydrated, id+label only
- [ ] Export streams the same filtered query; queued if it can be slow
- [ ] Design tokens everywhere; resolved values only where an API cannot read CSS variables

## Final report

```
Screen: <domain>
Server: enum · dto · request · service(query) · service(metrics) · controller · route · export
Contract: endpoints+limits passed from the server — <where>
States: initial | loading | success | error — all handled? yes/no
Caps: <range> · <items> · <page size>
Export: <sync|queued>, same DTO: yes/no
Open: <…>
```
