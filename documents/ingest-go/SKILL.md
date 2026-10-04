---
name: ingest-go
description: Fetch Kerala Government Orders (GOs), Circulars, and Legislative Bills from official portals, parse the GO number, tag each record to the correct department, and write a typed GovernmentOrder record to data/government-orders.ts. Use whenever adding GOs, Circulars, SROs, or Bills to the dashboard.
disable-model-invocation: true
---

# Ingest Government Order (`ingest-go`)

Adds one or more `GovernmentOrder` records to `data/government-orders.ts`. Every
record must be traceable to a primary source URL and tagged to a department. No
source URL = record does not ship.

Full spec: `docs/plans/ingest-go-spec.md`

---

## Source portals

Fetch from these in priority order:

| Priority | Portal               | URL                                                              | Covers                        |
| -------- | -------------------- | ---------------------------------------------------------------- | ----------------------------- |
| 1        | Document Portal, GoK | https://document.kerala.gov.in                                   | All departments — primary hub |
| 2        | LSG Orders portal    | https://go.lsgkerala.gov.in                                      | LSG-specific only             |
| 3        | Niyamasabha Bills    | https://niyamasabha.nic.in/index.php/business/index/bills_passed | Legislative Bills             |
| 4        | WCD Orders           | https://wcd.kerala.gov.in/gov_orders.php                         | Women & Child Dev only        |

**Tip:** If you have a GO number like `G.O.(P) No.162/2021/Fin`, search it
directly in the document portal's search box to pull the exact PDF link.

---

## Step 1 — Fetch

### Document portal (`document.kerala.gov.in`)

- Default view shows the last 30 days.
- Use **Advanced Search** to filter by department, GO type, and date range.
- Retrieve the PDF URL for each result — this becomes `meta.sourceUrl`.

### Niyamasabha bills

- Navigate to the Bills Passed section.
- Each bill entry should yield a PDF link (`meta.sourceUrl`) and a date.

### Fallback portals

- Use `go.lsgkerala.gov.in` or `wcd.kerala.gov.in/gov_orders.php` only when the
  document portal is missing a specific order.

---

## Step 2 — Parse the GO number

Kerala GO numbers follow this format:

```
G.O.(<type>) No.<number>/<year>/<DeptCode>
```

Examples:

```
G.O.(P) No.162/2021/Fin    → type=P, number=162, year=2021, deptCode=Fin
G.O.(Ms) No.45/2024/Rev    → type=Ms, number=45, year=2024, deptCode=Rev
G.O.(Rt) No.1180/2023/H&FWD → type=Rt, number=1180, year=2023, deptCode=H&FWD
SRO No.12/2024             → type=SRO, number=12, year=2024, deptCode=null
```

Bills and Circulars may not have a structured GO number — record the number
as-is and set `type: "Bill"` or `type: "Circular"` accordingly.

---

## Step 3 — Tag the department (two-stage)

### Stage 1 — GO number suffix (confidence: `high`)

Match `deptCode` (case-insensitive) against this table:

| deptCode         | dept.id                          |
| ---------------- | -------------------------------- |
| Fin              | dept.finance                     |
| Rev              | dept.revenue                     |
| H&FWD, HFWD, HFW | dept.health-family-welfare       |
| GAD, Gen         | dept.cmo                         |
| LSG              | dept.local-self-government       |
| Edu, GEdn        | dept.general-education           |
| HEdn             | dept.higher-education            |
| Home             | dept.home                        |
| PWD              | dept.public-works                |
| Tran             | dept.transport                   |
| Lab              | dept.labour-skills               |
| For              | dept.forest-wildlife             |
| Ind              | dept.industries-commerce         |
| Agri             | dept.agriculture-farmers-welfare |
| Coop             | dept.cooperation                 |
| Fish             | dept.fisheries-harbour           |
| Pwr, Elec        | dept.power                       |
| WR, Irr          | dept.water-resources             |
| SC/ST, SCSTBCD   | dept.scheduled-castes-tribes-bcd |
| WCD              | dept.women-child-development     |
| Tur              | dept.tourism                     |
| Vig              | dept.vigilance                   |
| Exc              | dept.excise                      |
| Plan             | dept.planning-economic-affairs   |
| Dev, Devaswom    | dept.devaswom                    |
| Min              | dept.minority-welfare            |
| IT, ICT          | dept.electronics-it              |
| Cult             | dept.cultural-affairs            |
| Port             | dept.ports                       |
| Yth              | dept.youth-welfare               |
| Law              | dept.law                         |

If matched → set `deptId` and `deptConfidence: "high"`. Skip Stage 2.

### Stage 2 — Keyword fallback (confidence: `medium`)

If Stage 1 didn't match, scan the GO subject line for the `name` or `nameMl` of
each department in `data/departments.ts`. First match wins.

If matched → set `deptId` and `deptConfidence: "medium"`.

### Fallback — ambiguous (confidence: `low`)

If neither stage matched, set `deptId: undefined` and `deptConfidence: "low"`.
Do **not** guess. The UI will render these with a visual caveat.

---

## Step 4 — Build the record

Use this template:

```ts
{
  id: "go.<year>-<deptCode-lower>-<number>",
  goNumber: "<raw GO number string>",
  type: "P",           // P | Ms | Rt | SRO | Circular | Bill
  subject: "<English subject from document>",
  // subjectMl: "<Malayalam subject — only if printed on document; never translate>",
  deptId: "dept.<id>", // omit if deptConfidence is "low"
  deptConfidence: "high", // high | medium | low
  date: "2021-06-15",  // ISO date from the document
  // effectiveDate: "2021-07-01", // only if different from date
  meta: {
    source: "Document Portal, Government of Kerala",
    sourceUrl: "https://document.kerala.gov.in/...", // direct PDF URL — mandatory
    retrievedAt: "<ISO timestamp of this fetch>",
  },
  dataStatus: "verified",
},
```

**ID examples:**

- `G.O.(P) No.162/2021/Fin` → `go.2021-fin-162`
- `G.O.(Rt) No.1180/2023/H&FWD` → `go.2023-hfwd-1180`
- `SRO No.12/2024` → `go.2024-sro-12`
- Circular with no number → `go.<year>-misc-<sequential>`

---

## Step 5 — Tooltip rule (non-negotiable)

Any UI component that renders this record **MUST** display a tooltip showing:

- `meta.source` — the portal name
- `meta.sourceUrl` — as a clickable link

This applies to table rows, cards, and detail views. **No tooltip = no merge.**

---

## Step 6 — After editing

1. Append the new record(s) to `GOVERNMENT_ORDERS` in
   `data/government-orders.ts`
2. Bump `SEED_VERSION` in `data/db.ts`
3. Run `deno task check` — must pass fmt + lint + type check
4. If a UI route exists: verify the record renders with the correct dept badge
   and tooltip

---

## Common mistakes

- **Omitting `meta.sourceUrl`** — this is the single most important field. Every
  GO has a PDF on the portal; find it.
- **Guessing the department when Stage 1 + 2 both fail** — set
  `deptConfidence: "low"` and leave `deptId` undefined. An incorrect tag is
  worse than an untagged record.
- **Machine-translating `subjectMl`** — only populate if the Malayalam subject
  appears on the document itself.
- **Forgetting `SEED_VERSION` bump** — the new record will silently not appear.
- **Using a `/thumb/` or search-result URL as `meta.sourceUrl`** — use the
  direct PDF URL so the link is stable.
