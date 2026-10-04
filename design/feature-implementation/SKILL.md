---
name: feature-implementation
description: Implement a new feature in this Deno Fresh app the project's way — typed fixture → KV accessor + SEED_VERSION bump → server-rendered route/component → bilingual + sourced → deno task check. Use when building a new page, data type, or visual on the dashboard.
---

# Feature implementation

The repeatable path for shipping a feature here, derived from how `/economy` /
the Status Paper were built. Pair with `arch-discovery` (where things live) and
`data-discovery` (sourcing the numbers).

## The loop

1. **Model the data** in `data/types.ts`. Reuse existing types where possible
   (e.g. `KpiTimePoint` for any time-series). Mark optional `*Ml` fields.
2. **Write the fixture** in `data/<thing>.ts` — a typed array. Every published
   figure carries `source` + `sourceUrl` to an **official government** document
   (`data-discovery` skill, `docs/data/source-policy.md`).
3. **Wire the KV layer** in `data/db.ts`: add the `["<thing>", id]` prefix to
   the layout comment + the `seed()` wipe-list + the seed loop, add
   `put*`/`list*`/`get*` accessors, and **bump `SEED_VERSION`**.
4. **Project into the knowledge graph** (only if the entity *relates* to existing
   entities — a leaf with no relationships skips this). Add `<thing>Node` +
   `<thing>Edges` builders and a `sync<Thing>Graph` to `lib/graph.ts`, wire the
   prefix into `buildGraph()`, and call the sync from your `putIngested*` writer.
   Full recipe + the "silently dropped edge" gotcha: `docs/specs/knowledge-graph.md`.
5. **Build the route/component** under `routes/**` / `components/**`.
   Server-render by default; add an island only for real client interactivity.
   Use `define.handlers` + `define.page`, `t(lang, …)`/`pick`, and the CSS
   tokens in `static/styles.css`. For visuals, prefer SSR SVG / daisyUI over a
   chart library (see `components/MetricChart.tsx`).
6. **Bilingual.** Provide verified `*Ml` for new strings. If you can't verify a
   Malayalam government term, leave it unset and set `dataStatus: "tbd"` — never
   guess. Run `/bilingual-audit`.
7. **Nav.** Add the entry to `components/Header.tsx` if it's a top-level page.
8. **Verify.** `deno task check` (fmt + lint + type-check) **and**
   `deno task check:sources`. For data changes, run the relevant reviewer agent
   (`kpi-data-reviewer` / `governance-data-reviewer`). Smoke-test with
   `deno task dev` and, for visuals, a screenshot.

## Gotchas

- The `deno fmt` PostToolUse hook rewrites files on save — **re-read before a
  second edit** or the next edit's `old_string` won't match.
- Forgetting the `SEED_VERSION` bump = the site silently serves stale KV data.
- A graph edge whose **target node isn't projected yet is silently dropped** (no
  dangling edges by design) — seed/rehydrate nodes *before* `buildGraph()` runs.
- `Lang` is exported from `data/lang.ts`, not `data/types.ts`.
- JSX lists need a `key` prop (Fresh lint rule `jsx-key`).

## Definition of done

`deno task check` + `deno task check:sources` green · `SEED_VERSION` bumped ·
bilingual parity (or `tbd`) · every figure government-sourced · a spec note in
`docs/specs/` for non-trivial features.
