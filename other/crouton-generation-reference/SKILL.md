---
name: crouton-generation-reference
layer: stack
description: Verified lookup pack for crouton's schema→CRUD generation domain — the fieldsFile JSON format, the complete field-type catalog with aliases, the naming contract, the exact artifact list one generate run produces, the seed/default-layout pipeline, dialect defaults, and rollback semantics. Use when writing or reviewing a collection schema, when asking "what field types exist / what does `crouton config` actually generate / where did this file name come from / why did I get a pg schema", when a generated file's name or path doesn't match the docs, or when removing/regenerating a collection. Trigger phrases — "what field types are supported", "schema JSON format", "what files does crouton generate", "naming convention for collections", "rollback a collection", "dialect default". The generation WORKFLOW (steps + sign-off gates) lives in the `crouton` skill — this is the reference it doesn't carry.
---

# Crouton Generation Reference

The drift-corrected lookup tables for the generation domain: what a schema file is, what one generate run produces, and exactly how everything is named. Every command/path/line here was verified against the repo on 2026-07-02; where the shipped docs are wrong, this file says so explicitly.

## When to use / when NOT to use

| You need | Go to |
|---|---|
| The generate **workflow** (gather fields → config → schema-review gate → generate → post-gen steps), MCP tool workflow, worked examples | **`crouton` skill** (`.claude/skills/crouton.md`) — defer to it; this file is the lookup pack under it |
| Human sign-off on a data model before generating | **`schema-review` skill** (#314) |
| Migration mechanics, the `.nuxt/hub/db/schema.mjs` build-first gotcha (#523), package-owned tables | **`db-migrations` skill** |
| Why the system is shaped this way (two-halves rule, invariants, registries) | sibling **`crouton-architecture-contract`** |
| Layout engine theory (LayoutTree, viability math, placer internals) | sibling **`crouton-layout-reference`** — §6 here covers only the generate→seed handoff |
| Booting/seeding a running app, inspecting the DB | sibling **`crouton-run-and-operate`** |
| Field-meta long-form descriptions, pagination/FK-filter details, `crouton add`/`init`/`db-pull` | `packages/crouton-cli/CLAUDE.md` (owns them; §9 lists its known-stale spots) |

## Vocabulary (crouton terms, defined once)

- **Collection** — one CRUD entity (e.g. `products`): a generated, self-contained nested Nuxt layer with form, list, composable, team-scoped API, Drizzle schema. Always team-scoped (every row has `teamId`).
- **Layer** — here: the domain folder `layers/<layer>/` grouping collections (e.g. `shop`). (Distinct from Nuxt-layer-as-package; see `crouton-architecture-contract`.)
- **fieldsFile** — the JSON file defining a collection's fields (§1). The input to everything.
- **`crouton.config.js`** — unified config at the app root: collections + targets + dialect for the CLI, `features` flags for the `@fyit/crouton` module. Full key reference: `packages/crouton-cli/CLAUDE.md` "Config File Format".
- **Manifest (`crouton.manifest.ts`)** — per-package declaration of field types, reserved names, detection patterns. The **source of truth for field types** (§2).
- **The CLI** — `packages/crouton-cli`, bins `crouton` (= `crouton-generate`) and `crouton-seed` (verified `package.json` bin map). In an app with `@fyit/crouton-cli` as devDep: `pnpm exec crouton <cmd>`.

## 1. fieldsFile JSON format

Shape (each top-level key is a field name):

```json
{
  "id":         { "type": "string",  "meta": { "primaryKey": true } },
  "name":       { "type": "string",  "meta": { "required": true, "maxLength": 255, "translatable": true } },
  "price":      { "type": "decimal", "meta": { "precision": 10, "scale": 2 } },
  "categoryId": { "type": "string",  "refTarget": "categories" },
  "authorId":   { "type": "string",  "refTarget": "users", "refScope": "adapter" }
}
```

Per-field keys: `type` (§2), `meta` (below), `refTarget` (name of the referenced collection — generates a `CroutonFormReferenceSelect` in the form, an FK query-param filter on the list endpoint, and cache auto-refresh), `refScope` (`'adapter'`/`'external'` for refs outside the generated layers, e.g. `users`; handled in `lib/generators/{form-component,list-component,database-queries}.ts`).

**`meta` keys** are owned by `packages/crouton-cli/CLAUDE.md` "Field Meta Properties" — read the full catalog there. What that doc doesn't say (verified behaviour):

| meta key | Non-obvious verified behaviour |
|---|---|
| `nullable` | `.nullish()` instead of `.optional()` in Zod; `json` and `date` types get `.nullish()` automatically (`generate-collection.ts`) |
| `translatable` | value lives in the collection's `translations` JSON column; root column is a cache/fallback — see trap below |
| `component` | besides overriding the form control, it **triggers that package's generator contribution** via manifest `detects`, even without a feature flag |

**Trap — translatable fields must be `required: false`.** The real value lives in `translations.{locale}.field`; a `NOT NULL` root column fails inserts that only populate translations. (crouton-cli/CLAUDE.md "Why this matters".)

**Three ways a field becomes translatable** (merged, in this priority — verified `generate-collection.ts:678-735`): field-level `meta.translatable: true` → collection-level `translatable: true` in config (auto-detects common names: `name`, `title`, `description`, `label`, `content`, … on string/text fields) → config-level `translations.collections.{plural}: [fields]`.

**Never declare** (auto-generated on every collection): `id, teamId, owner, createdAt, updatedAt, createdBy, updatedBy`; hierarchy adds `parentId, path, depth, order`. Reserved field names additionally include `optimisticId`, `optimisticAction` (verified `packages/crouton-core/crouton.manifest.ts:27-37`). Reserved **collection** names: `api, server, app, pages, components, composables, layouts, middleware, plugins, assets, public, node_modules` (same file, :39-43).

## 2. Field-type catalog

**Source of truth is per-package manifests, not any doc table.** `getTypeMapping()` in `packages/crouton-cli/lib/utils/manifest-loader.ts` (~:297) builds the map from every `crouton.manifest.ts`; core's types live in `packages/crouton-core/crouton.manifest.ts:12-25`. The tables in crouton-cli/CLAUDE.md and crouton-mcp/CLAUDE.md are copies (the MCP one is explicitly a *fallback* used only when manifest loading fails — `packages/crouton-mcp/src/utils/field-types.ts`).

Verified from the core manifest + the SQLite branch of `lib/generators/database-schema.ts:89-100`:

| Type | SQLite column (actual) | Zod | TS | Default | Form component | Aliases |
|---|---|---|---|---|---|---|
| `string` | `text()` | `z.string()` | `string` | `''` | `UInput` | |
| `text` | `text()` | `z.string()` | `string` | `''` | `UTextarea` | |
| `number` | `integer()` | `z.number()` | `number` | `0` | `UInputNumber` | **`integer`** |
| `decimal` | `real()` | `z.number()` | `number` | `0` | `UInputNumber` | |
| `boolean` | `integer({ mode: 'boolean' })` | `z.boolean()` | `boolean` | `false` | `UCheckbox` | |
| `date` | `integer({ mode: 'timestamp' })` | `z.date()` | `Date \| null` | `null` | `CroutonCalendar` | **`datetime`** |
| `json` | `jsonColumn()` | `z.record(z.string(), z.any())` | `Record<string, any>` | `{}` | `UTextarea` | |
| `repeater` | `jsonColumn()` | `z.array(z.any())` (typed when `meta.properties`) | `any[]` | `[]` | `CroutonFormRepeater` | |
| `array` | `text()` | `z.array(z.string())` | `string[]` | `[]` | `UTextarea` | |
| `reference` | `text()` | `z.string()` | `string` | `''` | `CroutonFormReferenceSelect` | |
| `image` | `text()` | `z.string()` | `string` | `''` | `CroutonImageUpload` → assets picker¹ | |
| `file` | `text()` | `z.string()` | `string` | `''` | `CroutonImageUpload` → assets picker¹ | |

¹ `crouton-assets`' manifest declares `detects: { fieldTypes: ['image','file'], refTargetPatterns: ['asset','file','image','media'] }` (verified `packages/crouton-assets/crouton.manifest.ts`), so its generator contribution swaps in `CroutonAssetsPicker` (crop for `image`) whenever those fields appear — no feature flag needed.

Notes:
- `reference` exists as a first-class type, but **in practice relationships are written as `type: "string"` + `refTarget`** — the user-facing table in the `crouton` skill omits `reference` for that reason.
- **Alias resolution (#285):** `loadFields` resolves aliases to their canonical type *before any generator runs* (each mapping entry carries `canonical` — `manifest-loader.ts:303-318`). History: `datetime` once leaked through unresolved → a raw `<UInput>` + a `text` column. Rules of thumb: `number` = integer column; `decimal` = float/`real`; a string-encoded enum (`'0'/'1'/'2'`) is `string`, not `number`.
- Adding a field type = a **manifest** change (plus generator branches) — see crouton-cli/CLAUDE.md "Add a new field type".

## 3. Dialect defaults — split by entry point

Code truth (the docs were corrected to match in the #1073 reshape):

| Entry point | Dialect default | Where |
|---|---|---|
| `crouton <layer> <collection>` (direct generate) | **`sqlite`** | `bin/crouton-generate.js` |
| `crouton init <name>` | **`sqlite`** | `bin/crouton-generate.js` |
| `crouton config` | the config file's `dialect`; **if the config omits it → `'pg'`** | `lib/generate-collection.ts` (the `config` subcommand has no `--dialect` flag at all) |

**Rule: always write `dialect: 'sqlite'` explicitly in `crouton.config.js`** (every in-repo app targets D1/SQLite) — the silent pg fallback on the config path is the trap.

## 4. Naming contract

Everything derives from `toCase()` (`lib/utils/helpers.ts` — real English pluralization via the `pluralize` npm package + `scule` casing; `categories`↔`category` works, naive `+s` does not apply). Given collection **`products`** in layer **`shop`**:

| Artifact | Name | Derivation |
|---|---|---|
| Directory | `layers/shop/collections/products/` | layer + lowercase plural |
| API base | `/api/teams/[id]/shop-products/` | `{layer}-{plural}` |
| Patch/delete route files | `[productId].patch.ts`, `[productId].delete.ts` | `[{singularCamel}Id]` — **NOT `[id]`** (docs say `[id]`; code is `generate-collection.ts:932-937`, fixture confirms `[itemId].patch.ts`) |
| Components | `ShopProductsForm`, `ShopProductsList` | the collection's own `nuxt.config.ts` registers `app/components` with `prefix: 'ShopProducts'`, `global: true` |
| Composable | `useShopProducts` (file `useShopProducts.ts`) | `use{LayerPascal}{PluralPascal}` |
| Registry key in `croutonCollections` | `shopProducts` (+ import `shopProductsConfig`) | `{layerCamel}{PluralPascal}` (`generate-collection.ts:1121-1122`; mirrored by `compose-layout.ts` `registryKeyFor()`) |
| Drizzle schema export | `shopProducts` | same |
| DB table | `shop_products` | `toSnakeCase(\`${layer}_${plural}\`)` (`database-schema.ts:171`; confirmed by a real `seed.json`'s `"table": "bookings_locations"`) |
| Test files | `ShopProducts.test.ts`, `ShopProducts.api.test.ts` | `{LayerPascal}{PluralPascal}` |

**System-collection exception:** a layer named `crouton-*` gets API path `crouton-<collection-kebab>` instead of `{layer}-{plural}` (`generate-collection.ts:882-888`) — e.g. layer `crouton-events` + `collectionEvents` → `/api/teams/[id]/crouton-collection-events/`. Its table is `toSnakeCase('crouton' + Collection)` (`database-schema.ts:168`).

## 5. Exact artifact list of one generate run

Verified against `writeScaffold` (`lib/generate-collection.ts:880-1155`) and on-disk generated collections (`fixtures/minimal/layers/main/collections/items/`, `pocs/booking-demo/layers/bookings/collections/*/`).

Per collection, under `layers/{layer}/collections/{plural}/`:

```
app/components/_Form.vue            # NOTE THE UNDERSCORE — see below. Skipped when
                                    #   formComponent is set (config or auto-detected)
app/components/List.vue
app/components/{FieldPascal}/{Input,Select,CardMini}.vue   # one dir per repeater field
app/composables/use{Layer}{Plurals}.ts   # Zod schema + columns + collection config
server/api/teams/[id]/{layer}-{plural}/
    index.get.ts  index.post.ts  [{singular}Id].patch.ts  [{singular}Id].delete.ts
    [{singular}Id]/move.patch.ts + reorder.patch.ts   # hierarchy only
    reorder.patch.ts                                  # sortable (non-hierarchy) only
server/database/schema.ts           # Drizzle (+ translations JSON column when translatable)
server/database/queries.ts          # getAll* with FK-filter + opt-in pagination overloads
server/database/seed.ts             # only with seed flag (drizzle-seed + Faker)
seed.json                           # always, except hierarchy collections (#298) — editable sample rows
{Layer}{Plurals}.test.ts            # Zod schema-smoke (#785) — skipped by --no-tests / tests:false
{Layer}{Plurals}.api.test.ts        # mocked route-handler test (#791), carries // @ts-nocheck — same gate
types.ts   nuxt.config.ts   README.md
```

**The `_Form.vue` underscore:** the actual filename is `_Form.vue` (`generate-collection.ts:912`) even though the dry-run output prints `Form.vue` (`:825`) and both the `crouton` skill and crouton-cli/CLAUDE.md draw `Form.vue`. It still registers as `{Layer}{Plurals}Form` — the composable's `componentName` field carries the name (verified `fixtures/minimal/.../useMainItems.ts:44`: `componentName: 'MainItemsForm'`).

Side effects beyond the collection dir (config-mode run, same file `:1091-1152` + `runPostGeneration` `:1165-1293`):

| Surface | What happens |
|---|---|
| `layers/{layer}/nuxt.config.ts` | created/updated to extend the collection |
| root `nuxt.config.ts` | `./layers/{layer}` added to `extends`; enabled feature packages synced in |
| `app/app.config.ts` | collection upserted into `croutonCollections` (import + entry) |
| i18n locale JSON | created when the collection has translatable fields |
| `server/database/schema/index.ts` | named schema export added per collection (config mode automates the "manual export" step the `crouton` skill lists) |
| migration | drizzle-kit runs **directly on the resolved schema graph** — no Nuxt build (#1445 WS2). ~2s. On a *cold* scaffold it soft-defers (`↻ Migration deferred … re-run: pnpm db:generate`, exit 0) rather than producing it in the same run — #1457. The old `npx nuxt db generate` 30s-timeout/silent-zero-migrations failure (#523) is **retired by design** on resolver apps; still possible on an external legacy `.nuxt`-bundle scaffold (no app in this repo since #1456) → `db-migrations` skill |
| CSS | Tailwind `@source` directive ensured |
| `.nuxt`-adjacent registries | type registry + **`server/utils/crouton-query-registry.ts`** (lazy per-collection query lookup) |
| **`crouton.layout.json`** (app root) | deterministic default layout (§6) |
| devtools | generation recorded for the DevTools Generators tab |

Real-world caveat: apps generated before #298/#709 (e.g. `apps/velo`, `fixtures/*`) lack `seed.json`-era artifacts at root (`crouton.layout.json`, query registry) — absence there is history, not a bug. `pocs/booking-demo` is a current-pipeline example with all of them.

## 6. Seed + default-layout pipeline (generate → booted app)

Mechanics of `crouton-seed` (discovery/topo-sort/wrangler transport) are owned by `packages/crouton-cli/CLAUDE.md` "App Seeding" — current and accurate. What this reference adds, verified from code:

1. **Layout pass (#709)** — `runPostGeneration` → `lib/compose-layout.ts` `writeDefaultLayout()` calls `composeDefaultLayout` from `@fyit/crouton-layout/app/utils/layout-compose` (a stale comment at the top of compose-layout.ts still says "from crouton-core"; the import at `:16` is truth — it moved in #751) and writes `crouton.layout.json`: `{ id: 'default', renderer, pattern, viable, tree }`. Patterns: `calendar-primary` | `master-detail` | `form-centric` | `stacked` | `empty` (verified `layout-compose.ts:54`). Theory → sibling `crouton-layout-reference`.
   - **Drift hazard (declared in code, `compose-layout.ts:22-26`):** the CLI has no live app.config at generate time, so it hardcodes mirror copies of the block sizing contracts (`CORE_BLOCKS`/`BOOKINGS_BLOCKS`). Changing a `minWidth`/`defaultSize` in `crouton-layout`/`crouton-bookings` app.config **must** be mirrored here — the hazard and the current values are owned by sibling `crouton-layout-reference` §6.
2. **Package seed providers** — `crouton-seed --db <name> [--remote|--dry-run]` collects each package's `<pkg>/seed` provider into idempotent upsert SQL, executed via `wrangler d1 execute`.
3. **Collection fixtures** — each `layers/*/collections/*/seed.json` (`{ table, key, rows }` — verified shape in `pocs/booking-demo`) is upserted with injected system columns + stable `seedId(layer, collection, key)` ids (`lib/seed-app.ts:180-193`).
4. **Layout row** — `collectDefaultLayoutSql` (`seed-app.ts:213-242`) upserts the tree into **`layout_configs` row id `default`** — the row the team layout page loads. NB (code comment): `layout_configs.id` is a **global** PK, so this seeds one default layout for the single seeded team only.

Result: a fresh POC boots laid out, not blank. The layout is data (editable in `CroutonLayout`), never generated `.vue`.

## 7. Deterministic vs AI-assisted

| Deterministic (no LLM anywhere) | AI-assisted (the agent is the intelligence) |
|---|---|
| All template generation (the 16 generators in `lib/generators/` are string templates keyed off the schema) | **Schema design** — the AI writes the fieldsFile; MCP `design_schema`/`init_schema` only feed it reference material |
| Type/alias resolution; Zod/TS/Drizzle mapping (manifest-driven) | The human **schema-review gate** (#314) on top of machine validation |
| MCP `validate_schema` (pure structural check), `dry_run`, `rollback` | Optional runtime AI features (`crouton-ai` translate, alt-text) — not part of generation |
| The default-layout pass — "No LLM" is stated in `compose-layout.ts`'s own header; the LLM `/layout` pass (#711) is gated and out of scope | Layout *iteration* via the agent⇄human ticket loop (sanitizer keeps ingest deterministic) |
| Seeding (SQL assembly, stable ids, topo-sort; Faker field-name heuristics are heuristic, not AI) | |
| Generated tests (samples derived from each field's Zod; no `Date.now()`/`Math.random()`) | |

Practical consequence: generation output is reproducible and diff-reviewable; the only judgment calls are the schema itself and any post-hoc layout edits — which is exactly where the sign-off gates sit.

## 8. Rollback & regeneration semantics

**Rollback** (`crouton rollback <layer> <collection> [--dry-run] [--keep-files] [--force]`) — verified `lib/rollback-collection.ts:252-300`, five steps:

1. delete `layers/{layer}/collections/{plural}/` (skipped by `--keep-files`)
2. remove the schema export from `server/database/schema/index.ts`
3. remove the `croutonCollections` entry + import from `app.config.ts`
4. remove the collection from the layer root `nuxt.config.ts`
5. remove `./layers/{layer}` from the root `nuxt.config.ts` **only if no other collections remain** in the layer

Also: `crouton rollback-bulk --layer=<layer>` / `--config=<path>` (whole layer / everything in a config) and `crouton rollback-interactive` (selection UI). The MCP `rollback` tool **defaults `dryRun: true`** (verified `crouton-mcp/src/tools/rollback.ts:7`); the CLI's does not — pass `--dry-run` yourself first.

**Rollback does NOT touch the database**: no migration is reverted, no table dropped, no rows deleted. Clean those up separately (a follow-up migration, or accept the orphan table on throwaway POCs).

**Regeneration**: re-running `crouton config` / `crouton <layer> <collection>` **overwrites every generated file unconditionally** — `writeScaffold` has no file-existence guard (`fsp.writeFile` loop at `generate-collection.ts:1074-1078`; code-derived, not reproduced end-to-end). Two consequences:
- The generated file headers saying "regeneration requires --force flag" are stale; `--force` actually means (a) proceed despite missing package dependencies (`:747-754`) and (b) override schema-index export conflicts (`:373-384`).
- **Hand edits inside generated files are lost on regeneration — including the "editable" `seed.json`** (it is in the unconditional write list, `:1042-1049`). Edit `seed.json` only if you won't regenerate, or re-apply edits after. If you customize a Form, prefer `formComponent:` (skips `_Form.vue` generation entirely) over editing the generated one.

## 9. Doc drift in this domain

The 2026-07-02 sweep's corrections (docs paths, docs-MCP tool names, dead `nuxt-crouton-*` package paths, the `--dialect` default, `_Form.vue`/`[{singular}Id].patch.ts` filenames, the sync-script extension, the manifest-vs-fallback field-type source) were **applied to the canonical docs in the #1073 reshape** — `.claude/skills/crouton.md`, `packages/crouton-cli/CLAUDE.md`, `packages/crouton-mcp/CLAUDE.md` now match the code. Don't trust this skill over them; if they disagree again, code wins (trust order: sibling `crouton-docs-trust-map` §1) and the fix goes to the canonical doc via the `sync-docs` workflow, not to a table here.

One known drift remains in **code**, not docs: generated file headers still claim "regeneration requires --force" while regeneration actually overwrites unconditionally (§8) — that's a template fix in `packages/crouton-cli/lib/generators/`, not a doc edit.

## Provenance and maintenance

verified: 2026-07-02

Facts verified against: `packages/crouton-cli/{bin/crouton-generate.js, lib/generate-collection.ts, lib/compose-layout.ts, lib/seed-app.ts, lib/rollback-collection.ts, lib/utils/{helpers.ts,manifest-loader.ts}, lib/generators/database-schema.ts, package.json}`, `packages/crouton-core/crouton.manifest.ts`, `packages/crouton-assets/crouton.manifest.ts`, `packages/crouton-layout/app/utils/layout-compose.ts`, `packages/crouton-mcp/src/{index.ts,tools/rollback.ts}`, and on-disk generated output in `fixtures/minimal/` + `pocs/booking-demo/`. Line numbers are anchors from that date and will drift — trust the symbol names over the `:NNN`. Issue numbers (#285, #298, #523, #558, #709, #711, #751, #785, #791) are cited from code comments and discovery-report summaries; check the issue if load-bearing.

Re-verification one-liners:

```bash
# dialect defaults (expect sqlite in bin, || 'pg' in runConfig)
grep -n "dialect" packages/crouton-cli/bin/crouton-generate.js | head -5
grep -n "config.dialect ||" packages/crouton-cli/lib/generate-collection.ts
# field-type catalog + aliases (the source of truth)
sed -n '12,25p' packages/crouton-core/crouton.manifest.ts
# artifact list / filenames (underscore Form, [xId] routes)
grep -n "_Form.vue\|Id].patch" packages/crouton-cli/lib/generate-collection.ts | head -5
# naming (registry key, table name)
grep -n "registryKeyFor\|snakeCaseTableName" packages/crouton-cli/lib/{compose-layout.ts,generators/database-schema.ts}
# layout payload + seed row id
grep -n "id: 'default'\|layout_configs" packages/crouton-cli/lib/{compose-layout.ts,seed-app.ts}
# CLI/manifest/skill field-type sync check
node scripts/validate-field-types-sync.mjs
```
