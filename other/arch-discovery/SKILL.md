---
name: arch-discovery
description: Orient quickly in this Deno Fresh 2 codebase — routing, the State/lang middleware, the Deno KV + typed-fixture data layer, islands, and where each kind of thing lives. Use before implementing a feature or when asked how the app is structured.
---

# Architecture discovery

A fast map of kerala-gov-mission-control. Full detail is in
[`CLAUDE.md`](../../../CLAUDE.md) and
[`docs/data/data-model.md`](../../../docs/data/data-model.md).

## Stack

**Deno Fresh 2**, file-based routing in `routes/`. Each route exports a
`handler` (data-loading) and a default page component, wired by the `define`
helper from [`utils.ts`](../../../utils.ts). Server-rendered by default;
`islands/` is the only client-side Preact.

## Where things live

| Need | Location |
| --- | --- |
| A page / endpoint | `routes/**` (e.g. `routes/economy/index.tsx`) |
| Client interactivity | `islands/**` (add only when genuinely needed) |
| Shared server components | `components/**` (`KpiCard`, `MetricChart`, `Header`) |
| Types | `data/types.ts` |
| Data fixtures | `data/*.ts` (typed arrays) |
| KV access layer | `data/db.ts` (`get*`/`list*`/`put*`, `seed`, `SEED_VERSION`) |
| i18n | `data/lang.ts` (`Lang`, `t()`), `_middleware.ts` sets `ctx.state.lang` |
| Styling tokens | `static/styles.css` (`surface-card`, `eyebrow`, `metric-value`) |
| Docs / specs | `docs/**` (`specs/`, `data/`, `plans/`) |

## State & language

`routes/_middleware.ts` reads a `lang` cookie → `ctx.state.lang` ("en"|"ml") and
`state.path`. Components select `name` vs `nameMl` via `t(lang, en, ml)` or a
local `pick(lang, en, ml)`.

## Data layer (read this before touching `data/`)

Fixtures in `data/*.ts` → seeded into **Deno KV** on cold start by
`ensureSeeded()`, keyed off `["meta","seed_version"]`. KV layout is documented
at the top of `data/db.ts`. **Critical:** any fixture shape/content change
requires bumping `SEED_VERSION` or the site serves stale data. The GO ingest
pipeline (`lib/ingest.ts`, `lib/cron.ts`) writes a durable
`["go_ingested"]` mirror that survives reseeds.

## Conventions that will trip you up

- The PostToolUse `deno fmt` hook rewrites `.ts`/`.tsx` on save — re-read before
  a second edit.
- `.env` edits are blocked by a hook; edit by hand.
- Bilingual invariant: never machine-translate Malayalam government terms.

## How to explore

`deno task dev` (localhost:8000). Grep `routes/` for an existing page that does
something similar and mirror its handler/page shape. Use the `Explore` agent for
broad "where is X" sweeps.
