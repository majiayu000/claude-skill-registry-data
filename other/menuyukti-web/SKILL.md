---
name: menuyukti-web
description: >-
  Next.js web app (apps/web): GraphQL data fetching, Clerk auth, next-intl, workflow/milestone UI including
  milestone data preview and milestone run settings, API routes and Zod schemas. Use when changing milestone cards,
  BFF routes, workflow timeline types, or web-side GraphQL usage. For performance, caching, and composition
  refactors, also use nextjs-performance, next-cache-components, and vercel-composition-patterns (see
  Companion skills).
---

# Menuyukti: `apps/web`

**Next.js** user-facing app: chat, campaigns, CRUD. **All product data** goes through **GraphQL** (no direct DB). Auth: **Clerk**. Copy: **next-intl** (no hardcoded user-facing strings).

For monorepo boundaries, see [`menuyukti-repo-orientation`](../menuyukti-repo-orientation/SKILL.md). For UI and i18n rules, see [`.cursor/rules/web-conventions.mdc`](../../../.cursor/rules/web-conventions.mdc).

## Companion skills

When implementing in **`apps/web`**, follow these skills in addition to this doc.

### Feature work (default)

- [`vercel-react-best-practices`](../vercel-react-best-practices/SKILL.md) — React and Next.js performance patterns.
- [`next-best-practices`](../next-best-practices/SKILL.md) — Next.js file conventions, RSC boundaries, data fetching.
- [`shadcn`](../shadcn/SKILL.md) — UI components and styling with the project’s shadcn setup.

For **Clerk** (auth, middleware, Server Actions), use [`clerk-nextjs-patterns`](../clerk-nextjs-patterns/SKILL.md).

### Refactors, performance, and composition

When improving an existing implementation (not only greenfield features), also read:

- [`nextjs-performance`](../nextjs-performance/SKILL.md) — Use when tuning Core Web Vitals, bundle size, LCP/INP, images/fonts, or RSC data performance.
- [`next-cache-components`](../next-cache-components/SKILL.md) — Use when adopting Cache Components, PPR, `use cache`, `cacheLife`, `cacheTag`, or `updateTag`.
- [`vercel-composition-patterns`](../vercel-composition-patterns/SKILL.md) — Use when refactoring boolean-prop sprawl, compound components, render props, or flexible public APIs.

## Layout (high level)

| Concern                 | Typical locations                                                                                                                                                                                                 |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| App Router              | [`apps/web/app/`](../../../apps/web/app/)                                                                                                                                                                         |
| Protected shell         | [`apps/web/app/(protected)/`](<../../../apps/web/app/(protected)/>) — `/workflow`, `/analytics`, `/canvas`, `/content`, `/advisor`, …                                                                             |
| GraphQL client          | [`apps/web/lib/graphql/client.ts`](../../../apps/web/lib/graphql/client.ts), [`queries/`](../../../apps/web/lib/graphql/queries/), [`node-schemas/`](../../../apps/web/lib/graphql/node-schemas/)                 |
| Workflow UI             | [`apps/web/app/(protected)/workflow/`](<../../../apps/web/app/(protected)/workflow/>)                                                                                                                             |
| Milestone presets (web) | [`apps/web/lib/milestones/preset-definitions.ts`](../../../apps/web/lib/milestones/preset-definitions.ts), [`node-schemas/milestone-presets.ts`](../../../apps/web/lib/graphql/node-schemas/milestone-presets.ts) |
| API routes (BFF)        | [`apps/web/app/api/`](../../../apps/web/app/api/) — e.g. `/api/workflows/.../milestones/.../run`                                                                                                                  |

Named product features and aliases (e.g. workflow import presets): see [`.agents/menuyukti-features.md`](../../menuyukti-features.md).

Commands: [AGENTS.md](../../../AGENTS.md) § Web.

## Milestone data and run

Milestone **run** uses LangGraph **preset subgraphs** keyed by `milestone.data.presetId` ([`menuyukti-agents`](../menuyukti-agents/SKILL.md)). Milestone data (structured JSON) lives on **`milestonedata`** child nodes; the run BFF calls **`POST .../run`** with `location_id` and `workflow_id` only.

**Chat** (workflow sidebar and `/advisor`) uses a separate ReAct graph with milestone read/write tools — see [`apps/agents/agents/core/chat/tools.py`](../../../apps/agents/agents/core/chat/tools.py) (`get_milestone`, overview, input patches).

### Checklist: new milestone preset (agents + web)

1. **Agents preset** — add `apps/agents/agents/core/milestone_run/<preset_id>/` and `register_preset_runner` ([`menuyukti-agents`](../menuyukti-agents/SKILL.md)).
2. **GraphQL / Zod** — extend `MILESTONE_PRESET_IDS` and milestone data schemas in [`node-schemas/milestone-presets.ts`](../../../apps/web/lib/graphql/node-schemas/milestone-presets.ts).
3. **Web preset catalog** — update [`preset-definitions.ts`](../../../apps/web/lib/milestones/preset-definitions.ts) (create fields, icons, empty data) and timeline UI (preset select, input tabs, preview components).
4. **Eval** — criterion helpers in `milestone_eval/<preset>_eval.py` when needed.
5. **GraphQL export/import** — keep milestone `data` JSON compatible when workflows round-trip ([`menuyukti-graphql`](../menuyukti-graphql/SKILL.md)).

## GraphQL from the web

- Use `graphqlQuery` from [`lib/graphql/client.ts`](../../../apps/web/lib/graphql/client.ts) in Server Components and `app/api/` handlers.
- Validate node `data` JSON with Zod via `parseNodeData` / schemas under `lib/graphql/node-schemas/` — avoid casting.
- Keep server/client boundaries aligned with Next.js conventions ([`next-best-practices`](../next-best-practices/SKILL.md)).

## Related

| Topic          | Skill                                                                  |
| -------------- | ---------------------------------------------------------------------- |
| Milestone run  | [`menuyukti-agents`](../menuyukti-agents/SKILL.md)                     |
| Backend schema | [`menuyukti-graphql`](../menuyukti-graphql/SKILL.md)                   |
| Monorepo map   | [`menuyukti-repo-orientation`](../menuyukti-repo-orientation/SKILL.md) |

## Canonical docs

- [`apps/web/README.md`](../../../apps/web/README.md)
- [`AGENTS.md`](../../../AGENTS.md)

## Progressive disclosure

Split long route or component maps into `reference.md` in this folder if this file grows.
