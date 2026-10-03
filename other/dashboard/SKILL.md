---
name: nuxt-ui-tools-dashboard
description: Use this skill when building analytics dashboards with nuxt-ui-tools as a package consumer. Covers schema and view functions (defineDashboardSchema, defineDashboardView) that take their context as typed params, useDashboard with a getter that rebuilds on input change, typed injection (useDashboardView, injectDashboard, InferDashboard, InferDashboardView), filters declared inline with the f builder and synced with the URL, memory, or an external store (one value per key across views), headless filters, filter controls and the shipped UI (UiDashboardPage, UiDashboardFilters, UiDashboardFilter, UiDashboardViewTabs) with slot overrides, remote paginated pickers and remoteTableOptions, staged queries (essential / background / deferred) with select and dependent requires, lazy enabled conditions on views, queries, and filters (blocks of disabled queries hidden, grids closing up), derived values, views (tabs), query-scoped filters, number formats (presets, Intl options, useDashboardFormat), and the dashboard blocks (stats with trends, goals, and comparisons, stat groups, gauges, unovis charts with highlights, value labels, and totals, lists with progress rings, bars, funnel, alerts, activity feeds, sortable tables, custom widgets) with their automatic loading, error, empty, and refresh states, card menus, header and footer actions, row actions, drill-down and selected state, card tabs, split cards, comparison periods, auto-refresh, and data freshness.
---

# nuxt-ui-tools Dashboard

Use this skill for package-consumer tasks involving:

- `defineDashboardSchema(...)`, `defineDashboardView(...)`, and the functions that wrap them
- `useDashboard(schema)` and `useDashboard(() => accountSchema({ accountId }))`
- typed injection: `useDashboardView(consumptionView)`, `injectDashboard(accountSchema)`,
  `InferDashboard`, `InferDashboardView`
- filters: declared inline with `f`, where they live (`sync`: URL, memory, a store), headless
  filters, one value per key across views
- `UiDashboardPage`: the whole page (header, refresh, pinned tabs and filters, the current view)
- controls (`dashboard.controls.x`) and the shipped UI `UiDashboardFilters`, `UiDashboardFilter`,
  `UiDashboardViewTabs`, a chart's series picked by a filter, a block's drill-down filter chips
- staged queries, `select`, dependent queries (`requires`), and `derive`
- lazy `enabled` conditions on views, queries, and filters
- remote pickers and `remoteTableOptions`
- number formats (`format="integer"`, `Intl.NumberFormat` options, `useDashboardFormat()`)
- `UiDashboardGrid`, `UiDashboardStat`, `UiDashboardWidget`, chart and list blocks, and the rest of
  the block library

Focused references:

- `skills/consumer/dashboard/references/schema.md` — schema and view functions, stages, `select`,
  conditions, views, derive, the facade, rebuilds
- `skills/consumer/dashboard/references/filters.md` — filter kinds and options, sync, URL keys,
  controls, remote pickers
- `skills/consumer/dashboard/references/controls.md` — the filter bar, pills, view tabs, slots,
  binding a control to your own component
- `skills/consumer/dashboard/references/blocks.md` — the page, every block, formats, grid sizing,
  theming

## Setup

The dashboard ships with the module. Queries run through TanStack Query, so the app must install
`VueQueryPlugin` (same requirement as the table). Chart blocks render with unovis, an optional peer
dependency:

```bash
bun add @unovis/vue @unovis/ts
```

Stats, lists, bars, paired bars, funnels, stacked bars, and custom widgets work without unovis.

## The Shape In One Example

A single file is enough for a small dashboard:

```vue
<script setup lang="ts">
const schema = defineDashboardSchema({
  key: 'sales',
  filters: (f) => ({
    period: f.enum([7, 30, 90], {
      defaultValue: 30,
      label: 'Period',
      format: (days) => `${days} days`,
    }),
  }),
  queries: ({ essential, background, filters }) => ({
    summary: essential.query(() => ({
      queryKey: ['sales', 'summary', filters.period],
      queryFn: () => api.sales.summary({ days: filters.period }),
    })),
    daily: background.query({
      defaultValue: [],
      query: () => ({
        queryKey: ['sales', 'daily', filters.period],
        queryFn: () => api.sales.daily({ days: filters.period }),
      }),
    }),
  }),
})

const dashboard = useDashboard(schema)
</script>

<template>
  <UiDashboardPage :dashboard title="Sales">
    <UiDashboardGrid>
      <UiDashboardStat
        size="12 md:4"
        :source="dashboard.summary"
        label="Revenue"
        :value="(summary) => summary.revenue"
        :compare="(summary) => summary.previousRevenue"
        :format="{ currency: 'EUR' }"
      />
      <UiDashboardBarChart
        size="12 lg:8"
        :source="dashboard.daily"
        title="Orders per day"
        :x="(day) => day.date"
        :series="[{ key: 'orders', label: 'Orders', value: (day) => day.orders }]"
        format="integer"
        totals
      />
    </UiDashboardGrid>
  </UiDashboardPage>
</template>
```

What you get without writing it:

- the page: title, today's date and when the data was fetched, the refresh control, and the filter
  bar pinned while the page scrolls
- a "Period 30 days ⌄" pill that picks the period, turns accent when changed, and resets
- `?period=7` in the URL (defaults never reach the URL)
- `summary` fetches first; `daily` fetches once `summary` settles
- each block shows a skeleton while its source loads, a retryable error scoped to that block, an
  empty state, and a thin progress bar whenever a request is in flight (refetch or retry)
- the stat's delta and "vs €12,400 previous period" caption, in the current locale
- every accessor (`summary.revenue`, `day.date`) typed from the query result

## Compose A Dashboard From Functions

A dashboard is about something: an account, the workspace a user works in. That context is the
params of a function wrapping the schema, passed by the page and handed on to the views. Filters are
the state the user controls; each view declares its own, inline. Each view is a self-contained
schema in its own file:

```ts
// entities/account/dashboard/activity.ts — one tab
export function accountActivityView(params: { accountId: string; workspace: Workspace }) {
  const { $api, $i18n } = useNuxtApp()
  const year = new Date().getFullYear()

  return defineDashboardView({
    label: () => $i18n.t('account.tabs.activity'),
    enabled: () => params.workspace !== 'client',
    filters: (f) => ({
      year: f.enum(years(), { defaultValue: year, label: () => $i18n.t('filters.year') }),
      product: f.remote(
        remoteTableOptions(
          (request) =>
            $api.accounts.products.queryOptions({
              params: { id: params.accountId },
              body: request,
            }),
          { search: ['name'], option: (product) => ({ label: product.name, value: product.id }) },
        ),
        { label: () => $i18n.t('filters.product') },
      ),
    }),
    queries: ({ essential, filters }) => {
      const usage = () =>
        $api.accounts.usage.queryOptions({
          params: { id: params.accountId },
          query: { year: filters.year, product: filters.product },
        })
      return {
        summary: essential.query({ query: usage, select: (data) => data.summary }),
        months: essential.query({ defaultValue: [], query: usage, select: (data) => data.months }),
      }
    },
  })
}

// entities/account/dashboard/schema.ts
export function accountSchema(params: { accountId: string; workspace: Workspace }) {
  return defineDashboardSchema({
    key: 'account',
    views: {
      activity: accountActivityView(params),
      invoices: accountInvoicesView(params),
    },
  })
}
```

```vue
<!-- pages/accounts/[id].vue: instantiate, then bind -->
<script setup lang="ts">
const route = useRoute()
const { workspace } = useApiContext()
const account = useDashboard(() =>
  accountSchema({ accountId: String(route.params.id), workspace: workspace.value }),
)
</script>
<template>
  <UiDashboardPage :dashboard="account" :title="t('Account')">
    <template #activity><AccountActivity /></template>
    <template #invoices><AccountInvoices /></template>
  </UiDashboardPage>
</template>

<!-- AccountActivity.vue: no props, fully typed, blocks only -->
<script setup lang="ts">
const activity = useDashboardView(accountActivityView)
</script>
<template>
  <UiDashboardGrid variant="panels" columns="2 md:4">
    <UiDashboardStat
      size="1"
      :source="activity.summary"
      label="Units"
      :value="(s) => s.units"
      format="integer"
    />
  </UiDashboardGrid>
</template>
```

The getter runs in setup, and again when what it reads changes (another account, another
workspace): the dashboard rebuilds for the new input behind the same objects, filters keep their
values (they live in the URL), and blocks show their loading state for the new data.

## Rules Of Thumb

- A page instantiates the dashboard and binds components: `useDashboard(...)` in the script,
  `UiDashboardPage` in the template, one slot per view. Never wire a header, a date line, sticky
  tabs, a scroll shadow, or a `v-if` on `dashboard.view.current` by hand; view components contain
  blocks only.
- Pass what the dashboard is about (an id, the audience) as params of the schema function; never
  as a filter synced from the route or a store. Filters are what the user changes.
- Declare filters inline in the schema or view that reads them. A key shared by two views is one
  filter: `year` keeps its value across tabs.
- Schema, view, and query builders may call app-level composables (`useNuxtApp()` for `$i18n` and
  `$api`, a store, `useRoute()`) and `useDashboardFormat()` at the top. A schema function runs
  again outside setup, so it cannot call `useI18n()` or lifecycle hooks.
- Write conditions as lazy callbacks: `enabled: () => can('margin')`. Blocks bound to a disabled
  query render nothing and grids close up, so templates never branch on permissions.
- There is no `.value` anywhere: `dashboard.filters.year`, `dashboard.summary.data`,
  `dashboard.refreshing` are plain reads, and filters are `v-model` targets.
- Bind blocks to resources, not strings: `:source="dashboard.summary"`.
- Put shared calculations in `derive`, not in page `computed`s, so blocks get their state for free.
- Declare presentation on the filter (`label`, `placeholder`, `format`, `columns`) and let the page
  render the bar; slot or bind a control yourself only where a filter needs a custom look.
- Split one response per block with `select` instead of reshaping it in `derive`.
- Use `useDashboardView(view)` / `injectDashboard(schema)` in child components; never prop-drill the
  dashboard or restate its type (`InferDashboard<typeof accountSchema>` names it when you need to).
- Format with presets, `{ currency }`, or `useDashboardFormat()`; do not build
  `Intl.NumberFormat` options in `computed`s.
- Let the engine render filter controls: a chart whose series the user picks binds the control as
  its `series`; a block narrowed by a drill-down value lists its control in `filters`; a header
  link is an action `{ label, to }`; rows that open a page take `to`.
- Drill down by writing a filter from `@select`; show it back with `selected`.
- Compare periods with `f.comparison()` and `resolveDashboardComparisonRange`, then pass `compare`
  accessors to stats and chart series: deltas, captions, and legends follow.
- Call `useDashboard` once in `<script setup>`; all queries and URL bindings are created there.
