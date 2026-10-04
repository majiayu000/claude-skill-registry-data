---
name: add-kpi
description: Add a new KPI to data/kpis.ts with every defensibility field the README requires (definition EN+ML, source, owner, refresh, target, comparators, direction, civic domain, owner dept). Use when adding any headline or tier-2 KPI.
disable-model-invocation: true
---

# Add KPI

Adds a new KPI fixture to `data/kpis.ts` with the full metadata schema. Every
published number on the dashboard must be defensible in public — that means no
shortcuts on this checklist.

## The defensibility rule

From the README: "A number with no target is propaganda." Same logic applies to
every other field. If you can't fill it, the KPI does not ship — it goes to a
tracking issue instead.

**Tooltip rule (non-negotiable):** Every new piece of information added to the
dashboard MUST display a tooltip that surfaces its source data — at minimum
`meta.source` and, when available, `meta.sourceUrl`. A number the citizen can't
trace back to a primary source is not a public number. No tooltip = no merge.

## Checklist (must all pass before commit)

- [ ] **id** is namespaced as `<domain>.<short-slug>` (e.g.
      `fiscal.debt-to-gsdp`)
- [ ] **title** (English) AND **titleMl** (Malayalam) both present
- [ ] **domain** is one of:
      `fiscal | health | education | livelihood | safety | transport | environment | sustainability | trust | delivery | other`
- [ ] **ownerDeptId** points to a real id in `data/departments.ts` (and
      `contributingDeptIds` if cross-cutting)
- [ ] **value**, **unit**, **target** all set. Target may equal an external
      ceiling (FRBM, SDG, etc.) — note that in `comparators`.
- [ ] **direction**: `higher-better` or `lower-better` — drives ▲/▼ semantics in
      `TrendArrow.tsx`
- [ ] **trend**, **trendDelta**, **trendWindow** describe the most recent change
      with a human-readable window (e.g. "vs last quarter")
- [ ] **status** is hand-set here (production version computes from
      distance-to-target + direction)
- [ ] **comparators[]** include at least one external benchmark (peer state,
      national avg, statutory target). A KPI without comparators looks like an
      unfalsifiable claim.
- [ ] **meta.definition** AND **meta.definitionMl** — a citizen and a journalist
      must read the same definition
- [ ] **meta.source** names the actual document/agency (not "internal
      dashboard")
- [ ] **meta.sourceUrl** when the source is publicly linkable — strongly
      preferred
- [ ] **Tooltip present on the rendered card** — the UI component for this data
      point MUST show a tooltip exposing at least `meta.source` (and
      `meta.sourceUrl` as a link if set). This is mandatory for every new data
      point, not optional.
- [ ] **meta.owner** is the accountable official's designation, not "Mission
      Control"
- [ ] **meta.updateFrequency** matches the source's actual cadence
- [ ] **meta.lastRefreshed** is an ISO datetime with `+05:30` offset

## Template

```ts
{
  id: "<domain>.<slug>",
  title: "<English title>",
  titleMl: "<മലയാളം തലക്കെട്ട്>",
  domain: "<civic-domain>",
  ownerDeptId: "dept.<id>",
  // contributingDeptIds: ["dept.<id>"],
  value: 0,
  unit: "<unit>",
  target: 0,
  direction: "higher-better", // or "lower-better"
  trend: "flat", // up | down | flat
  trendDelta: 0,
  trendWindow: "vs <comparator window>",
  status: "on-track", // on-track | slipping | off-track | improving
  comparators: [
    { label: "<peer / benchmark>", value: 0 },
  ],
  meta: {
    definition: "<one sentence, citizen-readable>",
    definitionMl: "<മലയാളത്തിൽ ഒരു വാക്യം>",
    source: "<Department / agency / report name>",
    sourceUrl: "<https://... if public>",
    owner: "<Designation, e.g. Principal Secretary (Finance)>",
    updateFrequency: "quarterly", // real-time|daily|weekly|monthly|quarterly|annual
    lastRefreshed: "2026-05-18T09:30:00+05:30",
    // methodologyUrl: "<https://... if a methodology note exists>",
  },
},
```

## After editing

1. Append to `HEADLINE_KPIS` array in `data/kpis.ts`
2. Bump `SEED_VERSION` in `data/db.ts` (forces a reseed on next cold start;
   existing index entries get wiped)
3. Run `deno task check` — must pass fmt + lint + type check
4. Verify on `/` — KPI card renders with correct trend arrow and status badge

## Common mistakes

- Using `owner` as the only ownership field — the legacy free-text `owner` stays
  for display, but `ownerDeptId` is the link the governance pages traverse
- Skipping `definitionMl` because "we'll translate later" — bilingual parity is
  a product promise, not a stretch goal
- Setting `direction: higher-better` for a metric like Infant Mortality Rate
  (it's lower-better — fewer dead babies is good)
- Forgetting the `SEED_VERSION` bump — your new KPI silently won't appear
  because seed is idempotent on version match
