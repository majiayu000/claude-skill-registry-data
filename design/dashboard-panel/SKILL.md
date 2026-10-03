---
name: dashboard-panel
description: Add, change or remove a panel on a console dashboard — the dashboards.yaml entry, its i18n keys, the Storybook story, the request-count test and the Typst template. Use whenever a task mentions a dashboard panel, a board, a chart on /admin/* or /settings/overview/*, dashboards.yaml, resolve-dashboard, or a panel type (stat, series, ranked, share, donut, table, latency-cards, latency-series).
---

# Adding or changing a dashboard panel

A dashboard is a **page entry in `apps/console/dashboards.yaml`**, not a container. You almost never
write a React component for a new panel — you write YAML, two locale keys, and a test number.

Read first: `docs/knowledge/dashboards.md` (the contract) and ADR 0015 D1/D2/D2b (the reasoning).

## The sequence

### 1. Edit `apps/console/dashboards.yaml`

Find the page by `route:`. Add the panel to `panels:`.

```yaml
- id: <page-prefix>-<what-it-reads> # unique DOCUMENT-wide, not just page-wide
  type: ranked # one of DASHBOARD_PANEL_TYPES
  title: <page-key>.<panel-id>.title # an i18n KEY, never prose
  subtitle: <page-key>.<panel-id>.subtitle # optional
  span: 1 # 1 or 2
  metric: cost # cost | requests | tokens | latency | derived:<name>
  options: { topN: 6, link: '/admin/usage/actors/:key?type=$lens' }
  query:
    scope: all
    group_by: [model]
    bucket: auto
    limit: 2000 # REQUIRED — never omit
```

Non-negotiables:

- **`limit` is always explicit.** A response the backend truncated must render a caption naming
  that number, not a quietly short chart.
- **Prefix the id per page** (`actor-*`, `channel-*`, `chat-*`). The id is the React key, the
  dedupe attribution, the heading id, the `?<panel-id>-scale=` URL knob and the report's lookup.
- **Reuse an existing query shape if you can.** Panels sharing a fully-resolved query share ONE
  request. Order `group_by` so your panel's own dimension is first, or set `options.dimension`.
- **`$placeholder` must be a filter the page declares.** `$name?` is legal only inside
  `filters.<key>` — never on `scope`/`scope_id`.
- **A ring (`donut`) is a decision, not a default.** Three exist, named in ADR 0015 D2. A per-key
  breakdown is `ranked`.
- **`options.style: stacked-bars` is sanctioned for three panels only** (daily spend x model).
  Every other `series` panel stays lines.

### 2. Add the locale keys — BOTH files

`apps/console/locales/en/dashboards.json` **and** `apps/console/locales/de/dashboards.json`. The
client ships only the active locale, so a missing `de` key renders as a raw key, not English.

Keys needed: `title`, and any of `subtitle`, `options.rowLabel`, `options.unit` you set.

### 3. Update the page's request-count test

Every dashboard page pins panel count and resolved request count. Adding a panel moves at least one.

| Page                                 | Test                                                                                   |
| ------------------------------------ | -------------------------------------------------------------------------------------- |
| `/admin/usage`                       | `apps/console/src/dashboards/admin-usage-page.test.ts` (also pins the 19 ids IN ORDER) |
| `/admin/overview`                    | `apps/console/src/dashboards/admin-overview-page.test.ts`                              |
| the three `/admin/usage` drill-downs | `apps/console/src/dashboards/admin-usage-detail-pages.test.ts`                         |
| the account and settings overviews   | `apps/console/src/dashboards/overview-pages.test.ts`                                   |

**Update the number and say in the PR body why the shape changed. Never delete the assertion.**
If the count did NOT go up, that is the dedupe working — state that too.

### 4. The story needs nothing

`packages/ui-web/src/pages-stories/spec-page.tsx` imports the real `dashboards.yaml` and the real
`locales/en/dashboards.json`. Your panel appears in `Dashboard/FromSpec` automatically. If it renders
with a visible i18n key, step 2 is incomplete.

If you added a new `options.*` knob, thread it through `SpecPanel` in `spec-page.tsx` and add a case
to `apps/console/src/dashboards/spec-page-story-parity.test.tsx` — the story and the console must not
disagree about `style`, `topN` or `link`.

### 5. Templates: only for a NEW route

An existing route's `.typ` template iterates `report.panels` and picks the new one up. A **new**
page entry needs nothing either — `templates/_lib/default.typ` handles it. Add
`apps/console/templates/<route>/report.typ` only when the document needs its own chrome. See the
`report-template` skill.

## Verify — all four, with real output

```sh
pnpm --filter console test          # the spec + page tests
pnpm --filter console typecheck
pnpm --filter @lightbridge/ui-web test
pnpm --filter console build:web     # the REAL Next build (not `build`)
```

Then look at it: `pnpm --filter @lightbridge/ui-web storybook` → `Dashboard/FromSpec`. See the
`console-story-verify` skill.

## Pitfalls that have actually bitten

- **`pnpm --filter console build` does not exist.** The script is `build:web`, and it runs
  `scripts/build-report-charts.mjs` first. Root `pnpm build` (turbo) also works.
- **A YAML typo is a STARTUP failure, not a compile error.** `formatDashboardIssues` names the page
  and the panel id. Read the whole message before guessing.
- **A new panel type needs a renderer in the same change.** `DASHBOARD_PANEL_TYPES`
  (`packages/ui-web/src/sections/dashboard-panels/types.ts`) and `panelRenderers`
  (`.../panel-renderers.tsx`) must cover each other exactly — a test asserts it.
- **Options set in YAML but not threaded into the story oracle silently diverge.** That is what
  `spec-page-story-parity.test.tsx` exists for; it was added after a real divergence.
- **A `stat`/`stat-group` panel gets no Card and no Expand.** That is `SELF_PANELLING_TYPES`, not a
  bug to fix.
- **Never add a legend list under a chart.** Values live on hover (Floating UI tooltip). Standing
  owner ruling.
- **Do not add a caption that claims something the data cannot support.** Read the honest-captions
  list in `docs/knowledge/admin-area.md` before writing a subtitle.
